from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Players(db.Model):
    """Players model"""

    __tablename__ = "players"

    id = db.Column(db.Text, primary_key=True, unique=True)
    name = db.Column(db.Text)

    # statistic = db.relationship("Statistics", backref="players")

class Teams(db.Model):
    """Teams model"""

    __tablename__ = "teams"

    id = db.Column(db.Text, primary_key=True, unique=True)
    name = db.Column(db.Text)

    # statistic = db.relationship("Statistics", backref="teams")

class Tournaments(db.Model):
    """Tournaments model"""

    __tablename__ = "tournaments" 

    id = db.Column(db.Text, primary_key=True, unique=True)
    year = db.Column(db.Integer)

    # statistic = db.relationship("Statistics", backref="tournaments")

class Statistics(db.Model):
    """Statistics model"""

    __tablename__ = "statistics"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Text, db.ForeignKey("players.id", ondelete="cascade"), primary_key=True)
    team_id = db.Column(db.Text, db.ForeignKey("teams.id", ondelete="cascade"), primary_key=True)
    tournament_id = db.Column(db.Text, db.ForeignKey("tournaments.id", ondelete="cascade"), primary_key=True)
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

    player = db.relationship("Players", backref="statistics")
    team = db.relationship("Teams", backref="statistics")
    tournament = db.relationship("Tournaments", backref="statistics")

def connect_db(app):
    db.app = app
    db.init_app(app)