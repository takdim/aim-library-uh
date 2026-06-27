from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.news import News
from app.models.profile import ProfileSection
from app.models.nav_link import NavLink
from app.models.service import Service
from app.models.statistic import Statistic
from app.forms.news_forms import NewsForm
from app.forms.profile_forms import ProfileSectionForm
from app.forms.nav_link_forms import NavLinkForm
from app.forms.service_forms import ServiceForm
from app.forms.stat_forms import StatisticForm
from app.utils.decorators import staff_required
from app.utils.upload import save_image, delete_image
from app.utils.log import log_activity
from app.utils.sanitize import clean_html

staff_bp = Blueprint('staff', __name__)


# ── Dashboard Home ──────────────────────────────────────────────────────────

@staff_bp.route('/')
@staff_required
def dashboard():
    news_count = News.query.count()
    pub_count = News.query.filter_by(status='published').count()
    return render_template('dashboard/index.html',
                           news_count=news_count,
                           pub_count=pub_count)


# ── Berita ───────────────────────────────────────────────────────────────────

@staff_bp.route('/berita')
@staff_required
def news_list():
    page = request.args.get('page', 1, type=int)
    news = News.query.order_by(News.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('dashboard/news/list.html', news=news)


@staff_bp.route('/berita/buat', methods=['GET', 'POST'])
@staff_required
def news_create():
    form = NewsForm()
    if form.validate_on_submit():
        article = News(
            title=form.title.data,
            title_en=form.title_en.data or None,
            category=form.category.data,
            excerpt=form.excerpt.data,
            excerpt_en=form.excerpt_en.data or None,
            content=clean_html(form.content.data),
            content_en=clean_html(form.content_en.data) if form.content_en.data else None,
            status=form.status.data,
            author_id=current_user.id,
        )
        article.generate_slug()
        if form.status.data == 'published':
            article.publish()

        if form.cover_image.data and form.cover_image.data.filename:
            filename = save_image(form.cover_image.data, subfolder='news')
            if filename:
                article.cover_image = filename

        db.session.add(article)
        log_activity(current_user, 'create_news', 'news', None,
                     f'Membuat berita: {article.title}')
        db.session.commit()
        flash('Berita berhasil dibuat!', 'success')
        return redirect(url_for('staff.news_list'))
    return render_template('dashboard/news/form.html', form=form, article=None)


@staff_bp.route('/berita/<int:news_id>/edit', methods=['GET', 'POST'])
@staff_required
def news_edit(news_id):
    article = News.query.get_or_404(news_id)
    form = NewsForm(obj=article)
    if form.validate_on_submit():
        article.title = form.title.data
        article.title_en = form.title_en.data or None
        article.category = form.category.data
        article.excerpt = form.excerpt.data
        article.excerpt_en = form.excerpt_en.data or None
        article.content = clean_html(form.content.data)
        article.content_en = clean_html(form.content_en.data) if form.content_en.data else None

        if form.status.data == 'published' and article.status == 'draft':
            article.publish()
        elif form.status.data == 'draft':
            article.unpublish()

        if form.cover_image.data and form.cover_image.data.filename:
            if article.cover_image:
                delete_image(article.cover_image)
            filename = save_image(form.cover_image.data, subfolder='news')
            if filename:
                article.cover_image = filename

        article.generate_slug()
        log_activity(current_user, 'edit_news', 'news', article.id,
                     f'Mengedit berita: {article.title}')
        db.session.commit()
        flash('Berita berhasil diperbarui!', 'success')
        return redirect(url_for('staff.news_list'))
    return render_template('dashboard/news/form.html', form=form, article=article)


@staff_bp.route('/berita/<int:news_id>/hapus', methods=['POST'])
@staff_required
def news_delete(news_id):
    article = News.query.get_or_404(news_id)
    if article.cover_image:
        delete_image(article.cover_image)
    log_activity(current_user, 'delete_news', 'news', article.id,
                 f'Menghapus berita: {article.title}')
    db.session.delete(article)
    db.session.commit()
    flash('Berita berhasil dihapus.', 'success')
    return redirect(url_for('staff.news_list'))


@staff_bp.route('/berita/<int:news_id>/toggle', methods=['POST'])
@staff_required
def news_toggle(news_id):
    article = News.query.get_or_404(news_id)
    if article.status == 'published':
        article.unpublish()
        flash('Berita diubah ke Draft.', 'info')
    else:
        article.publish()
        flash('Berita berhasil dipublikasikan!', 'success')
    log_activity(current_user, 'toggle_news_status', 'news', article.id,
                 f'Toggle status berita: {article.title} -> {article.status}')
    db.session.commit()
    return redirect(url_for('staff.news_list'))


# ── Profil ───────────────────────────────────────────────────────────────────

@staff_bp.route('/profil')
@staff_required
def profile_list():
    sections = ProfileSection.query.all()
    return render_template('dashboard/profile/list.html', sections=sections)


@staff_bp.route('/profil/<section_key>/edit', methods=['GET', 'POST'])
@staff_required
def profile_edit(section_key):
    section = ProfileSection.query.filter_by(section_key=section_key).first_or_404()
    form = ProfileSectionForm(obj=section)
    if form.validate_on_submit():
        section.title = form.title.data
        section.title_en = form.title_en.data or None
        section.content = clean_html(form.content.data)
        section.content_en = clean_html(form.content_en.data) if form.content_en.data else None
        section.updated_by = current_user.id
        section.updated_at = datetime.now(timezone.utc)

        if form.image.data and form.image.data.filename:
            filename = save_image(form.image.data, subfolder='profile')
            if filename:
                section.image_url = filename

        log_activity(current_user, 'edit_profile_section', 'profile', section.id,
                     f'Mengedit section: {section.section_key}')
        db.session.commit()
        flash('Section berhasil diperbarui!', 'success')
        return redirect(url_for('staff.profile_list'))
    return render_template('dashboard/profile/edit.html', form=form, section=section)


# ── Nav Links ────────────────────────────────────────────────────────────────

@staff_bp.route('/nav-links')
@staff_required
def nav_links_list():
    repos = NavLink.query.filter_by(type='repository').order_by(NavLink.sort_order).all()
    ejournals = NavLink.query.filter_by(type='ejournal').order_by(NavLink.sort_order).all()
    return render_template('dashboard/nav_links/list.html',
                           repos=repos, ejournals=ejournals)


@staff_bp.route('/nav-links/buat', methods=['GET', 'POST'])
@staff_required
def nav_links_create():
    form = NavLinkForm()
    if form.validate_on_submit():
        link = NavLink(
            type=form.type.data,
            name=form.name.data,
            url=form.url.data,
            description=form.description.data,
            sort_order=form.sort_order.data or 0,
            is_active=form.is_active.data,
        )
        if form.logo.data and form.logo.data.filename:
            filename = save_image(form.logo.data, subfolder='logos')
            if filename:
                link.logo_url = filename
        db.session.add(link)
        log_activity(current_user, 'create_nav_link', 'nav_link', None,
                     f'Membuat link: {link.name}')
        db.session.commit()
        flash('Link berhasil ditambahkan!', 'success')
        return redirect(url_for('staff.nav_links_list'))
    return render_template('dashboard/nav_links/form.html', form=form, link=None)


@staff_bp.route('/nav-links/<int:link_id>/edit', methods=['GET', 'POST'])
@staff_required
def nav_links_edit(link_id):
    link = NavLink.query.get_or_404(link_id)
    form = NavLinkForm(obj=link)
    if form.validate_on_submit():
        link.type = form.type.data
        link.name = form.name.data
        link.url = form.url.data
        link.description = form.description.data
        link.sort_order = form.sort_order.data or 0
        link.is_active = form.is_active.data
        if form.logo.data and form.logo.data.filename:
            filename = save_image(form.logo.data, subfolder='logos')
            if filename:
                link.logo_url = filename
        log_activity(current_user, 'edit_nav_link', 'nav_link', link.id,
                     f'Mengedit link: {link.name}')
        db.session.commit()
        flash('Link berhasil diperbarui!', 'success')
        return redirect(url_for('staff.nav_links_list'))
    return render_template('dashboard/nav_links/form.html', form=form, link=link)


@staff_bp.route('/nav-links/<int:link_id>/hapus', methods=['POST'])
@staff_required
def nav_links_delete(link_id):
    link = NavLink.query.get_or_404(link_id)
    log_activity(current_user, 'delete_nav_link', 'nav_link', link.id,
                 f'Menghapus link: {link.name}')
    db.session.delete(link)
    db.session.commit()
    flash('Link berhasil dihapus.', 'success')
    return redirect(url_for('staff.nav_links_list'))


# ── Services ─────────────────────────────────────────────────────────────────

@staff_bp.route('/layanan')
@staff_required
def services_list():
    services = Service.query.order_by(Service.sort_order).all()
    return render_template('dashboard/services/list.html', services=services)


@staff_bp.route('/layanan/buat', methods=['GET', 'POST'])
@staff_required
def services_create():
    form = ServiceForm()
    if form.validate_on_submit():
        svc = Service(
            title=form.title.data,
            title_en=form.title_en.data or None,
            description=clean_html(form.description.data),
            description_en=clean_html(form.description_en.data) if form.description_en.data else None,
            icon=form.icon.data,
            link_url=form.link_url.data,
            sort_order=form.sort_order.data or 0,
            is_active=form.is_active.data,
        )
        db.session.add(svc)
        log_activity(current_user, 'create_service', 'service', None,
                     f'Membuat layanan: {svc.title}')
        db.session.commit()
        flash('Layanan berhasil ditambahkan!', 'success')
        return redirect(url_for('staff.services_list'))
    return render_template('dashboard/services/form.html', form=form, service=None)


@staff_bp.route('/layanan/<int:svc_id>/edit', methods=['GET', 'POST'])
@staff_required
def services_edit(svc_id):
    svc = Service.query.get_or_404(svc_id)
    form = ServiceForm(obj=svc)
    if form.validate_on_submit():
        svc.title = form.title.data
        svc.title_en = form.title_en.data or None
        svc.description = clean_html(form.description.data)
        svc.description_en = clean_html(form.description_en.data) if form.description_en.data else None
        svc.icon = form.icon.data
        svc.link_url = form.link_url.data
        svc.sort_order = form.sort_order.data or 0
        svc.is_active = form.is_active.data
        log_activity(current_user, 'edit_service', 'service', svc.id,
                     f'Mengedit layanan: {svc.title}')
        db.session.commit()
        flash('Layanan berhasil diperbarui!', 'success')
        return redirect(url_for('staff.services_list'))
    return render_template('dashboard/services/form.html', form=form, service=svc)


@staff_bp.route('/layanan/<int:svc_id>/hapus', methods=['POST'])
@staff_required
def services_delete(svc_id):
    svc = Service.query.get_or_404(svc_id)
    log_activity(current_user, 'delete_service', 'service', svc.id,
                 f'Menghapus layanan: {svc.title}')
    db.session.delete(svc)
    db.session.commit()
    flash('Layanan berhasil dihapus.', 'success')
    return redirect(url_for('staff.services_list'))


# ── Statistics ───────────────────────────────────────────────────────────────

@staff_bp.route('/statistik')
@staff_required
def stats_list():
    stats = Statistic.query.order_by(Statistic.sort_order).all()
    return render_template('dashboard/statistics/list.html', stats=stats)


@staff_bp.route('/statistik/<int:stat_id>/edit', methods=['GET', 'POST'])
@staff_required
def stats_edit(stat_id):
    stat = Statistic.query.get_or_404(stat_id)
    form = StatisticForm(obj=stat)
    if form.validate_on_submit():
        stat.label = form.label.data
        stat.value = form.value.data
        stat.icon = form.icon.data
        stat.sort_order = form.sort_order.data or 0
        log_activity(current_user, 'edit_statistic', 'statistic', stat.id,
                     f'Mengubah statistik: {stat.label} = {stat.value}')
        db.session.commit()
        flash('Statistik berhasil diperbarui!', 'success')
        return redirect(url_for('staff.stats_list'))
    return render_template('dashboard/statistics/edit.html', form=form, stat=stat)


@staff_bp.route('/statistik/buat', methods=['GET', 'POST'])
@staff_required
def stats_create():
    form = StatisticForm()
    if form.validate_on_submit():
        stat = Statistic(
            label=form.label.data,
            value=form.value.data,
            icon=form.icon.data,
            sort_order=form.sort_order.data or 0,
        )
        db.session.add(stat)
        log_activity(current_user, 'create_statistic', 'statistic', None,
                     f'Membuat statistik: {stat.label}')
        db.session.commit()
        flash('Statistik berhasil ditambahkan!', 'success')
        return redirect(url_for('staff.stats_list'))
    return render_template('dashboard/statistics/edit.html', form=form, stat=None)


@staff_bp.route('/statistik/<int:stat_id>/hapus', methods=['POST'])
@staff_required
def stats_delete(stat_id):
    stat = Statistic.query.get_or_404(stat_id)
    log_activity(current_user, 'delete_statistic', 'statistic', stat.id,
                 f'Menghapus statistik: {stat.label}')
    db.session.delete(stat)
    db.session.commit()
    flash('Statistik berhasil dihapus.', 'success')
    return redirect(url_for('staff.stats_list'))
