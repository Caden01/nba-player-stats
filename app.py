from flask import Flask, render_template, request, jsonify, g, session, flash, redirect
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, Players, Tournaments, Teams, Statistics, Users, Favorites
from forms import RegisterForm, LoginForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "asdfjsldf387fqw398"

connect_db(app)

########################################################
# Signup/login/logout

@app.before_request
def add_user_to_g():
    """Add user to Flask global if logged in"""

    if CURR_USER_KEY in session:
        g.user = Users.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def handle_login(user):
    """Login user"""

    session[CURR_USER_KEY] = user.id

def handle_logout():
    """Logout user"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Creates new user and add to DB if form is valid"""

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = Users.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username is already take")
            return render_template("register.html", form=form)
        
        handle_login(user)
        return redirect("/")
    
    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles the users login"""

    form = LoginForm()

    if form.validate_on_submit():
        user = Users.authenticate(form.username.data, form.password.data)

        if user:
            handle_login(user)
            flash("You're logged in")
            return redirect("/")

        flash("Incorrect username or password")
    
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Handle user logging out"""

    handle_logout()

    return redirect("/")


########################################################
# Main routes

@app.route("/")
def homepage():
    """Show top scorers, assissts, rebounds"""

    points = db.session.execute(db.select(Statistics).order_by(Statistics.points.desc())).scalars()
    assists = db.session.execute(db.select(Statistics).order_by(Statistics.assists.desc())).scalars()
    rebounds = db.session.execute(db.select(Statistics).order_by(Statistics.trb.desc())).scalars()

    if g.user:
        favorites = Favorites.query.all()
        favorites_ids = [fav.player_id for fav in favorites]
        print(favorites_ids)

        return render_template("index.html", points=points, assists=assists, rebounds=rebounds, favorites=favorites_ids)

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
    """Show user profile"""

    if not g.user:
        flash("Access denied", "danger")
        return redirect("/")

    user = Users.query.get_or_404(g.user.id)
    players = Players.query.all()
    favorites = Favorites.query.all()

    favorite_ids = [fav.player_id for fav in favorites]

    return render_template("profile.html", user=user, favorites_ids=favorite_ids, players=players)

@app.route("/suggestions")
def search_suggestions():
    """Gives information to JS file for search suggesions"""

    players = []

    stats = Statistics.query.order_by(Statistics.player_id)
    for stat in stats:
        players.append(stat.players.name)

    return jsonify({"players": players})

@app.route("/<player_id>/favorite", methods=["POST"])
def favorite_player(player_id):
    """Add player to favorites list"""

    if not g.user:
        flash("Access denied", "danger")
        return redirect("/")

    favorited_player = Players.query.get_or_404(player_id)
    favorites = Favorites.query.all()
    
    favorites_ids = [fav.player_id for fav in favorites]

    if favorited_player.id in favorites_ids:
        favorite = Favorites.query.filter_by(player_id=favorited_player.id).first()
        db.session.delete(favorite)
    else:
        favorite = Favorites(
            user_id = g.user.id,
            player_id = favorited_player.id
        )
        db.session.add(favorite)

    db.session.commit()
    
    return redirect("/")

@app.route("/search")
def send_search_value():
    """Retrieves search input value"""

    value = request.args["val"]
    print(value)

    return render_template("base.html", value=value)