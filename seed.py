import requests
import json
from app import app
from models import db, Statistics, Players, Teams, Tournaments

with app.app_context():
    db.drop_all()
    db.create_all()

    response = requests.get("https://nba-stats-db.herokuapp.com/api/playerdata/season/2022")
    results = response.json()["results"]


    teams = []
    seasons = []

    for result in results:


        player = Players(
            id = result["player_name"],
            name = result["player_name"],
            age = result["age"]
            )

        if result["team"] not in teams:
            teams.append(result["team"])
            team = Teams(
                id = result["team"],
                name = result["team"]
                )
         
        if result["season"] not in seasons:
            seasons.append(result["season"])
            tournament = Tournaments(
                id = result["season"],
                year = result["season"]
                )

        statistic = Statistics(
            player_id = player.id, 
            team_id = team.id, 
            tournament_id = tournament.id, 
            games = result["games"],
            games_started = result["games_started"],
            minutes_played = result["minutes_played"], 
            field_goals = result["field_goals"],
            field_attempts = result["field_attempts"],
            field_percent = result["field_percent"],
            three_fg = result["three_fg"],
            three_attempts = result["three_attempts"],
            three_percent = result["three_percent"],
            two_fg = result["two_fg"],
            two_attempts = result["two_attempts"],
            two_percent = result["two_percent"],
            effect_fg_percent = result["effect_fg_percent"],
            ft = result["ft"],
            ft_attempts = result["fta"],
            ft_percent = result["ft_percent"],
            orb = result["ORB"],
            drb = result["DRB"],
            trb = result["TRB"],
            assists = result["AST"],
            steals = result["STL"],
            blocks = result["BLK"],
            tov = result["TOV"],
            pf = result["PF"],
            points = result["PTS"],
        )


        db.session.add(player)
        db.session.add(team)
        db.session.add(tournament)
        db.session.add(statistic)

    db.session.commit()