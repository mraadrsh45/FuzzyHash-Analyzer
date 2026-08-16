from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if session.get('user_id'):
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Welcome back, {user.username} (SOC Forensic Analyst).', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password. (Default demo: admin / admin123)', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out of FuzzyHash Analyzer session.', 'info')
    return redirect(url_for('auth.login'))
