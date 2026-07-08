import random
from app.models import Player, Round

#pexels functiion for image api
from app.pexels_api.pexels_client import get_reveal_image
WORD_LIST = [
    "Beach", "Pizza", "Hospital", "Guitar", "Volcano",
    "Library", "Astronaut", "Umbrella", "Castle", "Waterfall",
    "Bicycle", "Snowman", "Desert", "Circus", "Lighthouse",
    "Backpack", "Thunderstorm", "Pirate", "Treehouse", "Submarine",
    "Campfire", "Skyscraper", "Volleyball", "Cactus", "Igloo",
    "Parachute", "Telescope", "Waterpark", "Mountain", "Kitchen",
    "Airport", "Jungle", "Robot", "Fireworks", "Aquarium",
    "Blanket", "Spaceship", "Bakery", "Farm", "Chessboard",
    "Rainbow", "Tent", "Museum", "Skateboard", "Glacier",
    "Restaurant", "Bridge", "Wizard", "Trampoline", "Reef",
    "Elevator", "Windmill", "Piano", "Canoe", "Greenhouse",
    "Tornado", "Compass", "Vineyard", "Stadium", "Cave",
    "Trolley", "Lantern", "Hammock", "Bonfire", "Observatory",
    "Ferry", "Meadow", "Drone", "Barn", "Snorkel",
    "Bunker", "Carousel", "Chest", "Motorcycle", "Pyramid",
    "Sled", "Fountain", "Cabin", "Kite", "Marketplace",
    "Subway", "Junkyard", "Orchard", "Rooftop", "Canyon",
    "Sailboat", "Quarry", "Tundra", "Wagon", "Skyline",
    "Tower", "Cove", "Diner", "Garage", "Attic",
    "Playground", "Zoo", "Harbor", "Vault", "Sandcastle"
]

def assign_word():
    return random.choice(WORD_LIST)

def assign_imposter(player_ids):
    if not player_ids:
        raise ValueError("Player IDs list cannot be empty.")
    return random.choice(player_ids)

def update_user_stats(user, won):
    user.games_played += 1
    if won:
        user.games_won += 1
    return user

def determine_winner(votes, imposter_id):
    if not votes:
        return {"outcome": "No votes cast", "winner": None, "imposter_id": imposter_id}
    tally = {}
    for voted in votes.values():
        if voted is None:
            continue
        tally[voted] = tally.get(voted, 0) + 1
    if not tally:
        return {"outcome": "everyone skipped", "winner": None, "imposter_id": imposter_id}
    max_votes = max(tally.values())
    winners = [pid for pid, count in tally.items() if count == max_votes]
    if len(winners) > 1:
        return {"outcome": "tie", "winner": None, "imposter_id": imposter_id}
    voted_out = winners[0]
    outcome = "imposter wins" if voted_out == imposter_id else "players win"
    return {"outcome": outcome, "winner": voted_out, "imposter_id": imposter_id}

def assign_word_for_round(room):
    word = assign_word()

    pexels_data = get_reveal_image(word)

    #extracts only the image link for the frontend
    image_url = pexels_data.get('reveal_image')

    return Round(room_id=room.id, word=word, reveal_image_url=image_url)

def assign_imposter_for_room(room):
    players = list(room.players)
    if not players:
      return None
    imposter_id = assign_imposter([player.id for player in players])

    imposter_player = None
    for player in players:
      is_imposter = (player.id == imposter_id)
      player.is_imposter = is_imposter

      if is_imposter:
        imposter_player = player

    return imposter_player

def update_stats_for_player(player, won):
    if player.user is None:
        return None
    return update_user_stats(player.user, won)

def determine_round_winner(players, votes, imposter_player, award_point=True):
    result = determine_winner(votes, imposter_player.id)
    if award_point and result["outcome"] in ("players win", "imposter wins"):
        imposter_won = (result["outcome"] == "imposter wins")
        for player in players:
            is_imposter = (player.id == imposter_player.id)
            update_stats_for_player(player, won=(is_imposter == imposter_won))
    return result

def serialize_players(room_id):
    players = Player.query.filter_by(room_id=room_id).all()
    return [
        {"id": p.id, "name": p.name, "picture": p.user.picture if p.user else None}
        for p in players
    ]