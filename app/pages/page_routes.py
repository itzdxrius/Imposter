import uuid

from flask import Blueprint, app, render_template, session, redirect, url_for
from app.models import Player, Room, User
from app import db

pages_bp = Blueprint('pages', __name__)

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

def get_current_room():
    return Room.query.filter_by(code="GLOB").first()

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
    user = get_current_user()
    if not user:
        return redirect(url_for('pages.signin'))
    room = Room.query.filter_by(status='waiting').first()
    if not room:
        room = Room(code="GLOB", status="waiting")
        db.session.add(room)
        db.session.commit()

    existing_player = Player.query.filter_by(user_id=user.id, room_id=room.id).first()

    if not existing_player:
        new_player = Player(
            room_id=room.id,
            user_id=user.id,
            name=user.name,
            session_id=str(uuid.uuid4())
            )
        db.session.add(new_player)
        db.session.commit()

    current_players = Player.query.filter_by(room_id=room.id).all()

    return render_template('lobby.html', room=room,players=current_players)

@pages_bp.route('/game')
def game():
    user = get_current_user()
    if not user:
        return redirect(url_for('pages.signin'))
    room = get_current_room()
    if not room or not room.rounds:
        return redirect(url_for('pages.lobby'))
    current_round = room.rounds[-1]
    player = Player.query.filter_by(user_id=user.id, room_id=room.id).first()
    if not player:
        return redirect(url_for('pages.lobby'))
    if player.is_imposter:
        return render_template('game_template.html', round=current_round)
    return render_template('game_template.html', round=current_round, word=current_round.query)

@pages_bp.route('/results')
def results():
    room = get_current_room()
    if not room or not room.rounds:
        return redirect(url_for('pages.lobby'))
    return render_template('results.html', round=room.rounds[-1])

@pages_bp.route('/profile')
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('pages.signin'))
    return render_template('profile.html', user=user)

@pages_bp.route('/vote')
def vote():
    user = get_current_user()
    if not user:
        return redirect(url_for('pages.signin'))
    room = get_current_room()
    if not room or not room.rounds:
        return redirect(url_for('pages.lobby'))
    current_round = room.rounds[-1]
    player = Player.query.filter_by(user_id=user.id, room_id=room.id).first()
    if not player:
        return redirect(url_for('pages.lobby'))
    return render_template('vote.html', round=current_round, players=room.players)
