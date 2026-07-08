from flask import Blueprint, render_template, session, redirect, url_for
from app.models import User

pages_bp = Blueprint('pages', __name__)

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

@pages_bp.route('/')
def signin():
    return render_template('sign_in.html')

@pages_bp.route('/home')
def home():
    user = get_current_user()
    if not user:
        return redirect(url_for('pages.signin'))
    return render_template('home_page.html', user=user)

@pages_bp.route('/lobby')
def lobby():
    return render_template('lobby.html')

@pages_bp.route('/game')
def game():
    return render_template('game.html')

@pages_bp.route('/results')
def results():
    return render_template('results.html')

@pages_bp.route('/profile')
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('pages.signin'))
    return render_template('profile.html', user=user)