import uuid
from flask import Blueprint, render_template, session, redirect, url_for
from app.models import Player, Room, User
from app import db
from app.game_logic import assign_word_for_round, assign_imposter_for_room

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
    room = get_current_room()
    if not room:
        room = Room(code="GLOB", status="waiting")
        db.session.add(room)
        db.session.commit()
    elif room.status == "finished":
        Player.query.filter_by(room_id=room.id).delete()
        room.status = "waiting"
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

    return render_template('lobby.html', room=room, user=user, players=current_players)

@pages_bp.route('/game')
def game():
    user = get_current_user()
    if not user:
        return redirect(url_for('pages.signin'))
    room = get_current_room()
    if not room:
        return redirect(url_for('pages.lobby'))

    if room.status != "in_progress":
        new_round = assign_word_for_round(room)
        db.session.add(new_round)
        assign_imposter_for_room(room)
        room.status = "in_progress"
        db.session.commit()

    current_round = room.rounds[-1]
    player = Player.query.filter_by(user_id=user.id, room_id=room.id).first()
    if not player:
        return redirect(url_for('pages.lobby'))
    if player.is_imposter:
        return render_template('game_template.html', round=current_round, is_imposter=True)
    return render_template('game_template.html', round=current_round, is_imposter=False, word=current_round.word)

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

@pages_bp.route('/results')
def results():
    room = get_current_room()
    if not room or not room.rounds:
        return redirect(url_for('pages.lobby'))
    return render_template('results.html', round=room.rounds[-1])