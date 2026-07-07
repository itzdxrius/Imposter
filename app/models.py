from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    google_sub = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    picture = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    players = db.relationship('Player', backref='user', lazy=True)

    games_played = db.Column(db.Integer, default=0, nullable=False)
    games_won = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
      return f"<User {self.email}>"

class Room(db.Model):
  __tablename__ = 'rooms'
  id = db.Column(db.Integer, primary_key=True)
  code = db.Column(db.String(4), unique=True, nullable = False)
  status = db.Column(db.String(20), default='waiting')
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  players = db.relationship('Player', backref='room', lazy=True, cascade="all, delete-orphan")
  rounds = db.relationship('Round', backref='room', lazy=True, cascade="all, delete-orphan")

  def __repr__(self):
    return f"<Room{self.code}- {self.status}>"

class Player(db.Model):
  __tablename__ = 'players'


  id = db.Column(db.Integer, primary_key=True)
  room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

  name = db.Column(db.String(50), nullable=False)
  session_id = db.Column(db.String(100), nullable=False)
  is_imposter = db.Column(db.Boolean, default = False)
  score = db.Column(db.Integer, default=0)

  def __repr__(self):
    role = "Imposter" if self.is_imposter else "Crewmate"
    return f"<Player{self.name} ({role})>"

class Round(db.Model):
  __tablename__ = 'rounds'
  id = db.Column(db.Integer, primary_key=True)
  room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)

  query = db.Column(db.String(100), nullable=False)
  reveal_image_url = db.Column(db.String(500), nullable=True)

  def __repr__(self):
    return f"<Round in Room {self.room_id} - Query: {self.query}>"
# class FriendRequest(db.Model):
#     __tablename__ = "friend_requests"

#     id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     status = db.Column(db.String(20), default="pending")  # pending, accepted, rejected
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     sender = db.relationship("User", foreign_keys=[sender_id], backref="sent_requests")
#     receiver = db.relationship("User", foreign_keys=[receiver_id], backref="received_requests")

#     __table_args__ = (
#         db.UniqueConstraint("sender_id", "receiver_id", name="unique_friend_request"),
#     )

# class Friendship(db.Model):
#     __tablename__ = "friendships"

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     friend_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     __table_args__ = (
#         db.UniqueConstraint("user_id", "friend_id", name="unique_friendship"),
#     )

# class Game(db.Model):
#     __tablename__ = "games"

#     id = db.Column(db.Integer, primary_key=True)
#     join_code = db.Column(db.String(10), unique=True, nullable=False)
#     host_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     is_active = db.Column(db.Boolean, default=True, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# class GamePlayer(db.Model):
#     __tablename__ = "game_players"

#     id = db.Column(db.Integer, primary_key=True)
#     game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     joined_at = db.Column(db.DateTime, default=datetime.utcnow)

#     __table_args__ = (
#         db.UniqueConstraint("game_id", "user_id", name="unique_game_player"),
#     )
