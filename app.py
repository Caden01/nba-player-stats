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

@app.route("/player")
def player():
    return render_template("player.html")

@app.route("/shots")
def shots():
    return render_template("shots.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")