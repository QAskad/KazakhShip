from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from .models import User, Visit, db
from . import db
from datetime import datetime, timedelta

admin = Blueprint('admin', __name__)


@admin.route('/admin')
def admin_panel():
    now = datetime.utcnow()
    last_24_hours = now - timedelta(hours=24)

    new_users_count = User.query.filter(User.created >= last_24_hours).count()

    visits_count = Visit.query.filter(Visit.timestap >= last_24_hours).count()
    users = User.query.all()  
    return render_template('admin.html', users=users, new_users_count=new_users_count, visits_count=visits_count)

def record_user_visit():
    if current_user.is_authenticated:
        visit = Visit(user_id=current_user.id)
        db.session.add(visit)
        db.session.commit()

@admin.route('/admin/block_user/<int:user_id>', methods=['POST'])
def block_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_blocked = True
        user.blocked_until = datetime.utcnow() + timedelta(days=3)
        db.session.commit()
        flash('User has been blocked for 3 days!', category='success')
    else:
        flash('User not found.', category='error')
    return redirect(url_for('admin.admin_panel'))

@admin.route('/admin/unblock_user/<int:user_id>', methods=['POST'])
def unblock_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_blocked = False
        user.blocked_until = None
        db.session.commit()
        flash('User has been unblocked!', category='success')
    else:
        flash('User not found.', category='error')
    return redirect(url_for('admin.admin_panel'))
