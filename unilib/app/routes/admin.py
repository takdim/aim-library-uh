from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user
from app import db
from app.models.user import User
from app.models.activity_log import ActivityLog
from app.forms.user_forms import UserCreateForm, UserEditForm
from app.utils.decorators import admin_required
from app.utils.log import log_activity

admin_bp = Blueprint('admin', __name__)


# ── User Management ──────────────────────────────────────────────────────────

@admin_bp.route('/users')
@admin_required
def users_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('dashboard/users/list.html', users=users)


@admin_bp.route('/users/buat', methods=['GET', 'POST'])
@admin_required
def users_create():
    form = UserCreateForm()
    if form.validate_on_submit():
        user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            username=form.username.data,
            role=form.role.data,
            is_active=True,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        log_activity(current_user, 'create_user', 'user', None,
                     f'Membuat akun: {user.username} ({user.role})')
        db.session.commit()
        flash(f'Akun {user.username} berhasil dibuat!', 'success')
        return redirect(url_for('admin.users_list'))
    return render_template('dashboard/users/form.html', form=form, user_obj=None)


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def users_edit(user_id):
    user_obj = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user_obj)
    if form.validate_on_submit():
        # Prevent sole admin from losing admin role
        if user_obj.id == current_user.id and form.role.data != 'admin':
            active_admins = User.query.filter_by(role='admin', is_active=True).count()
            if active_admins <= 1:
                flash('Tidak dapat mengubah role: Anda adalah satu-satunya Admin aktif.', 'danger')
                return redirect(url_for('admin.users_edit', user_id=user_id))

        user_obj.full_name = form.full_name.data
        user_obj.email = form.email.data
        user_obj.username = form.username.data
        user_obj.role = form.role.data
        user_obj.is_active = form.is_active.data

        if form.new_password.data:
            user_obj.set_password(form.new_password.data)

        log_activity(current_user, 'edit_user', 'user', user_obj.id,
                     f'Mengedit akun: {user_obj.username}')
        db.session.commit()
        flash('Akun berhasil diperbarui!', 'success')
        return redirect(url_for('admin.users_list'))
    return render_template('dashboard/users/form.html', form=form, user_obj=user_obj)


@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@admin_required
def users_toggle(user_id):
    user_obj = User.query.get_or_404(user_id)
    if user_obj.id == current_user.id:
        flash('Tidak dapat menonaktifkan akun sendiri.', 'danger')
        return redirect(url_for('admin.users_list'))

    # Safety: don't deactivate last admin
    if user_obj.role == 'admin' and user_obj.is_active:
        active_admins = User.query.filter_by(role='admin', is_active=True).count()
        if active_admins <= 1:
            flash('Tidak dapat menonaktifkan satu-satunya Admin aktif.', 'danger')
            return redirect(url_for('admin.users_list'))

    user_obj.is_active = not user_obj.is_active
    action = 'activate_user' if user_obj.is_active else 'deactivate_user'
    log_activity(current_user, action, 'user', user_obj.id,
                 f'Toggle status akun: {user_obj.username} -> {"aktif" if user_obj.is_active else "nonaktif"}')
    db.session.commit()
    status = 'diaktifkan' if user_obj.is_active else 'dinonaktifkan'
    flash(f'Akun {user_obj.username} berhasil {status}.', 'success')
    return redirect(url_for('admin.users_list'))


@admin_bp.route('/users/<int:user_id>/hapus', methods=['POST'])
@admin_required
def users_delete(user_id):
    user_obj = User.query.get_or_404(user_id)
    if user_obj.id == current_user.id:
        flash('Tidak dapat menghapus akun sendiri.', 'danger')
        return redirect(url_for('admin.users_list'))

    if user_obj.role == 'admin':
        active_admins = User.query.filter_by(role='admin', is_active=True).count()
        if active_admins <= 1:
            flash('Tidak dapat menghapus satu-satunya Admin aktif.', 'danger')
            return redirect(url_for('admin.users_list'))

    log_activity(current_user, 'delete_user', 'user', user_obj.id,
                 f'Menghapus akun: {user_obj.username}')
    db.session.delete(user_obj)
    db.session.commit()
    flash('Akun berhasil dihapus.', 'success')
    return redirect(url_for('admin.users_list'))


# ── Activity Log ─────────────────────────────────────────────────────────────

@admin_bp.route('/logs')
@admin_required
def activity_logs():
    page = request.args.get('page', 1, type=int)
    logs = ActivityLog.query \
                      .order_by(ActivityLog.created_at.desc()) \
                      .paginate(page=page, per_page=20)
    return render_template('dashboard/logs/list.html', logs=logs)
