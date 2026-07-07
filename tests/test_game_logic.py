from app.game_logic import *
from app.models import *
from app import db



def test_assign_word_returns_word_from_word_list():
    word = assign_word()
    assert word in WORD_LIST

def test_assign_word_is_random():
    results = {assign_word() for _ in range(30)}
    assert len(results) > 1  # Expecting multiple unique words from the list

def test_assign_imposter_picks_from_players():
    players = [1, 2, 3, 4, 5]
    imposter = assign_imposter(players)
    assert imposter in players

def test_assign_imposter_empty_list_raises():
    players = []
    try:
        assign_imposter(players)
        assert False, "Expected ValueError for empty player list"
    except ValueError:
        pass  # Expected exception

def test_update_user_stats_loss(app):
    user = User(google_sub="s2", email="b@example.com", name="B", games_played=2, games_won=1)
    update_user_stats(user, won=False)
    assert user.games_played == 3
    assert user.games_won == 1  # Should not increment games_won

def _make_room_with_players(names, session_prefix="sess"):
    room = Room(code="AB12", status="in-game")
    db.session.add(room)
    db.session.flush()
    players = []
    for i, name in enumerate(names):
        player = Player(name=name, session_id=f"{session_prefix}-{i}", room_id=room.id)
        db.session.add(player)
        players.append(player)
    db.session.commit()
    return room, players

def test_assign_imposter_for_room_marks_exactly_one(app):
    room, players = _make_room_with_players(["Alice", "Bob", "Charlie"])
    imposter = assign_imposter_for_room(room)
    db.session.commit()

    marked = [player for player in Player.query.filter_by(room_id=room.id) if player.is_imposter]
    assert len(marked) == 1
    assert marked[0].id == imposter.id

def test_update_stats_for_with_linked_user(app):
    user = User(google_sub="s3", email="c@example.com", name="C")
    db.session.add(user)
    db.session.commit()
    room, _ = _make_room_with_players(["Charlie"])
    player = Player.query.filter_by(room_id=room.id).first()
    player.user_id = user.id
    db.session.commit()

    update_stats_for_player(player, won=True)
    db.session.commit()

    assert user.games_played == 1
    assert user.games_won == 1

