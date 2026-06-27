from flask import Blueprint, render_template, abort, redirect, request as flask_request, make_response, url_for
from app.models.news import News
from app.models.statistic import Statistic
from app.models.nav_link import NavLink
from app.models.service import Service
from app.models.profile import ProfileSection

public_bp = Blueprint('public', __name__)


@public_bp.route('/set-lang/<lang>')
def set_lang(lang):
    if lang not in ('id', 'en'):
        lang = 'id'
    next_url = flask_request.referrer or url_for('public.index')
    resp = make_response(redirect(next_url))
    resp.set_cookie('lang', lang, max_age=60 * 60 * 24 * 365, samesite='Lax', httponly=True)
    return resp


@public_bp.route('/')
def index():
    stats = Statistic.query.order_by(Statistic.sort_order).all()
    latest_news = News.query.filter_by(status='published') \
                            .order_by(News.published_at.desc()) \
                            .limit(3).all()
    repositories = NavLink.query.filter_by(type='repository', is_active=True) \
                                .order_by(NavLink.sort_order).all()
    ejournals = NavLink.query.filter_by(type='ejournal', is_active=True) \
                             .order_by(NavLink.sort_order).all()
    services = Service.query.filter_by(is_active=True) \
                            .order_by(Service.sort_order).all()
    fasilitas = ProfileSection.query.filter_by(section_key='fasilitas').first()

    return render_template('public/index.html',
                           stats=stats,
                           latest_news=latest_news,
                           repositories=repositories,
                           ejournals=ejournals,
                           services=services,
                           fasilitas=fasilitas)


@public_bp.route('/berita/<slug>')
def news_detail(slug):
    article = News.query.filter_by(slug=slug, status='published').first_or_404()
    return render_template('public/news_detail.html', article=article)


@public_bp.route('/profil/<section_key>')
def profil(section_key):
    valid_keys = ProfileSection.VALID_KEYS
    if section_key not in valid_keys:
        abort(404)
    section = ProfileSection.query.filter_by(section_key=section_key).first_or_404()
    return render_template('public/profil/index.html', section=section)
