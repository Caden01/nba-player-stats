from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

class Favorites(db.Model):
    """Favorites model"""

    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    player_id = db.Column(db.Text, db.ForeignKey("players.id"))


class Users(db.Model):
    """Users model"""
     
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)

    favorite = db.relationship("Favorites", backref="users", cascade="all, delete")

    @classmethod
    def signup(cls, username, password, email):
        """Signup user"""

        hashed_password = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = Users(
            username=username,
            password=hashed_password,
            email=email
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Check if username and password match"""

        user = cls.query.filter_by(username=username).first()

        if user:
            auth = bcrypt.check_password_hash(user.password, password)
            if auth:
                return user

        return False



class Players(db.Model):
    """Players model"""

    __tablename__ = "players"

    id = db.Column(db.Text, primary_key=True, unique=True)
    name = db.Column(db.Text)
    age = db.Column(db.Integer)

    favorite = db.relationship("Favorites", backref="players", cascade="all, delete")
    statistic = db.relationship("Statistics", backref="players", cascade="all, delete")

class Teams(db.Model):
    """Teams model"""

    __tablename__ = "teams"

    id = db.Column(db.Text, primary_key=True, unique=True)
    name = db.Column(db.Text)

    statistic = db.relationship("Statistics", backref="teams", cascade="all, delete")

class Tournaments(db.Model):
    """Tournaments model"""

    __tablename__ = "tournaments" 

    id = db.Column(db.Text, primary_key=True, unique=True)
    year = db.Column(db.Integer)

    statistic = db.relationship("Statistics", backref="tournaments", cascade="all, delete")

class Statistics(db.Model):
    """Statistics model"""

    __tablename__ = "statistics"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Text, db.ForeignKey("players.id", ondelete="cascade"))
    team_id = db.Column(db.Text, db.ForeignKey("teams.id", ondelete="cascade"))
    tournament_id = db.Column(db.Text, db.ForeignKey("tournaments.id", ondelete="cascade"))
    games = db.Column(db.Integer)
    games_started = db.Column(db.Integer)
    minutes_played = db.Column(db.Integer)
    field_goals = db.Column(db.Integer)
    field_attempts = db.Column(db.Integer)
    field_percent = db.Column(db.Text)
    three_fg = db.Column(db.Integer)
    three_attempts = db.Column(db.Integer)
    three_percent= db.Column(db.Text)
    two_fg = db.Column(db.Integer)
    two_attempts = db.Column(db.Integer)
    two_percent= db.Column(db.Text)
    effect_fg_percent= db.Column(db.Text)
    ft = db.Column(db.Integer)
    ft_attempts = db.Column(db.Integer)
    ft_percent = db.Column(db.Text)
    orb = db.Column(db.Integer)
    drb = db.Column(db.Integer)
    trb = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    steals = db.Column(db.Integer)
    blocks = db.Column(db.Integer)
    tov = db.Column(db.Integer)
    pf = db.Column(db.Integer)
    points = db.Column(db.Integer)


def connect_db(app):
    db.app = app
    db.init_app(app)