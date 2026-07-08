from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Room, Player, Round, Vote
from app.game_logic import (
    assign_word_for_round, assign_imposter_for_room, determine_round_winner
)

game_bp = Blueprint("game", __name__)

@game_bp.route("/start_round/<int:room_id>", methods=["POST"])
def start_round(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    imposter_player = assign_imposter_for_room(room)
    if not imposter_player:
        return jsonify({"error": "No players in the room to assign an imposter"}), 400

    new_round = assign_word_for_round(room)
    db.session.add(new_round)
    room.status = "in_progress"
    db.session.commit()

    return jsonify({"round_id": new_round.id}), 200


@game_bp.route("/room_status/<int:room_id>", methods=["GET"])
def room_status(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    latest_round = room.rounds[-1] if room.rounds else None
    return jsonify({
        "status": room.status,
        "round_id": latest_round.id if latest_round else None
    }), 200


@game_bp.route("/get_players/<int:room_id>", methods=["GET"])
def get_players(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    return jsonify({
        "players": [{"id": p.id, "name": p.name} for p in room.players]
    }), 200


@game_bp.route("/rounds/<int:round_id>/my_role", methods=["GET"])
def my_role(round_id):
    round_instance = Round.query.get(round_id)
    if not round_instance:
        return jsonify({"error": "Round not found"}), 404

    user_id = session.get("user_id")
    player = Player.query.filter_by(user_id=user_id, room_id=round_instance.room_id).first()
    if not player:
        return jsonify({"error": "Player not found in this round"}), 403

    if player.is_imposter:
        return jsonify({"is_imposter": True, "message": "You are the imposter!"}), 200
    else:
        return jsonify({"is_imposter": False, "word": round_instance.query}), 200


@game_bp.route("/submit_votes/<int:round_id>", methods=["POST"])
def cast_votes(round_id):
    round_instance = Round.query.get(round_id)
    if not round_instance:
        return jsonify({"error": "Round not found"}), 404

    data = request.get_json()
    user_id = session.get("user_id")
    voter = Player.query.filter_by(user_id=user_id, room_id=round_instance.room_id).first()
    if not voter:
        return jsonify({"error": "you are not found in this round"}), 403

    voted_for_id = data.get("voted_for_id")
    voted_for_id = int(voted_for_id) if voted_for_id is not None else None

    vote = Vote.query.filter_by(round_id=round_instance.id, voter_id=voter.id).first()
    if vote is None:
        vote = Vote(round_id=round_instance.id, voter_id=voter.id)
        db.session.add(vote)
    vote.voted_id = voted_for_id
    db.session.commit()

    players = round_instance.room.players
    votes_cast = Vote.query.filter_by(round_id=round_instance.id).count()

    if votes_cast >= len(players):
        votes = {vote.voter_id: vote.voted_id for vote in round_instance.votes}
        imposter_player = next((p for p in players if p.is_imposter), None)
        if imposter_player:
            result = determine_round_winner(players, votes, imposter_player)
            round_instance.outcome = result["outcome"]
            round_instance.winner_id = result["winner"]
            round_instance.imposter_id = result["imposter_id"]
            round_instance.room.status = "waiting"
            db.session.commit()

    return jsonify({"message": "Vote cast successfully"}), 200


@game_bp.route("/get_round_results/<int:round_id>", methods=["GET"])
def get_round_results(round_id):
    round_instance = Round.query.get(round_id)
    if not round_instance:
        return jsonify({"error": "Round not found"}), 404

    return jsonify({
        "round_id": round_instance.id,
        "query": round_instance.query,
        "reveal_image_url": round_instance.reveal_image_url,
        "outcome": round_instance.outcome,
        "winner_id": round_instance.winner_id,
        "imposter_id": round_instance.imposter_id
    }), 200