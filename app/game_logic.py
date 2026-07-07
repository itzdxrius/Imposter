import random

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
    return random.choice(player_ids)

def update_user_stats(user, won):
    user.games_played += 1
    if won:
        user.games_won += 1
    return user

def assign_word_for_round(room):
    word = assign_word()
    return Round(room_id=room.id, query=word)

def assign_imposter_for_room(room):
    players = list(room.players)
    imposter = assign_imposter([player.id for player in players])
    for player in players:
        player.is_imposter = (player.id == imposter)
    for player in players:
        if player.id == imposter:
            return player

def update_stats_for_players(player, won):
    if player.user is None:
        return None
    update_user_stats(player.user, won)