from flask import Flask, render_template, redirect
from models import db, connect_db, Players, Tournaments, Teams, Statistics

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

@app.route("/")
def homepage():
    """Show top scorers, assissts, rebounds"""

    points = db.session.execute(db.select(Statistics).order_by(Statistics.points.desc())).scalars()
    assists = db.session.execute(db.select(Statistics).order_by(Statistics.assists.desc())).scalars()
    rebounds = db.session.execute(db.select(Statistics).order_by(Statistics.trb.desc())).scalars()

    return render_template("index.html", points=points, assists=assists, rebounds=rebounds)

@app.route("/season")
def season():
    """Show all players with their season stats"""

    options = ["Games", "Points", "Assists", "Rebounds", "Alphabetically"]
    players = Players.query.all()
    stats = Statistics.query.order_by(Statistics.player_id)

    return render_template("season.html", players=players, stats=stats, options=options)

@app.route("/season/<option>")
def order(option):
    """Orders list by a certain option user picks"""

    options = ["Games", "Points", "Assists", "Rebounds", "Alphabetically"]
    stats = []

    if option == "Games":
        choice = "Games"
        stats = Statistics.query.order_by(Statistics.games.desc())
    elif option == "Points":
        choice = "Points"
        stats = Statistics.query.order_by(Statistics.points.desc())
    elif option == "Assists":
        choice = "Assists"
        stats = Statistics.query.order_by(Statistics.assists.desc())
    elif option == "Rebounds":
        choice = "Rebounds"
        stats = Statistics.query.order_by(Statistics.trb.desc())
    else:
        choice = "Alphabetically"
        stats = Statistics.query.order_by(Statistics.player_id)
        

    return render_template("order_season.html", stats=stats, options=options, choice=choice)

@app.route("/playoffs")
def playoffs():
    return render_template("playoffs.html")

@app.route("/players")
def players():
    """List of all players"""

    players = Players.query.all()

    return render_template("players.html", players=players)

@app.route("/player/<player_id>")
def player(player_id):
    """Show specif player stats"""
    
    player =  Statistics.query.filter_by(player_id=player_id).first_or_404()
    players = Players.query.all()
    tournaments = Tournaments.query.all()
    percent = round(float(player.effect_fg_percent) * 100, 1)

    return render_template("player.html", player=player, players=players, tournaments=tournaments, percent=percent)

@app.route("/shots/<player_id>")
def shots(player_id):
    """Show shot statistics for a specific player"""

    stats =  Statistics.query.filter_by(player_id=player_id).first_or_404()
    players = Players.query.all()
    tournaments = Tournaments.query.all()
    field_percent = round(float(stats.field_percent) * 100, 1)
    three_percent = round(float(stats.three_percent) * 100, 1)
    two_percent = round(float(stats.two_percent) * 100, 1)
    ft_percent = round(float(stats.ft_percent) * 100, 1)


    return render_template("shots.html", stats=stats, players=players, tournaments=tournaments, field_percent=field_percent, three_percent=three_percent, two_percent=two_percent, ft_percent=ft_percent)

@app.route("/profile")
def profile():
    return render_template("profile.html")