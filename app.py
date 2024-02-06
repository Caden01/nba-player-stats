from flask import Flask, render_template, redirect
from models import db, connect_db, Players, Tournaments, Teams, Statistics

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/season")
def season():
    """Show all players with their season stats"""

    players = Players.query.all()
    stats = Statistics.query.all()

    return render_template("season.html", players=players, stats=stats)

@app.route("/playoffs")
def playoffs():
    return render_template("playoffs.html")

@app.route("/players")
def players():
    return render_template("players.html")

@app.route("/player/<player_id>")
def player(player_id):
    """Show specif player stats"""
    
    player =  Statistics.query.filter_by(player_id=player_id).first_or_404()
    players = Players.query.all()
    tournaments = Tournaments.query.all()
    percent = float(player.effect_fg_percent) * 100

    return render_template("player.html", player=player, players=players, tournaments=tournaments, percent=percent)

@app.route("/shots")
def shots():
    return render_template("shots.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")