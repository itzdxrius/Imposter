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
