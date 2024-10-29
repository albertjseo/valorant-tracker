import os

from flask import Flask, render_template, request
from markupsafe import Markup
import dotenv
import requests

# creating the app
app = Flask(__name__)

# variable api_key
dotenv.load_dotenv()
API_KEY = os.environ.get("MY_API_KEY")


# creating the routes
@app.route('/', methods=["GET", "POST"])
def landing_page():
    if request.method == "POST":

        # retrieve the user input for the episode and act
        selected_players = request.form.get("players")
        selected_act = request.form.get("acts")

        # connect to valorant content from riot api and query
        contents = requests.get("https://na.api.riotgames.com/val/content/v1/contents",
                                headers={"X-Riot-Token": API_KEY}).json()

        # filter the response to view acts
        act_info = contents["acts"]

        print(act_info)

        # filter for the episode
        episode_id = [act["id"] for act in act_info if act["name"] == selected_act]

        # match the filtered episode with user selected act
        correct_act = {}
        for act in act_info:
            if act["parentId"] == episode_id and act["name"] == selected_act:
                correct_act = act

            print(correct_act)

        # match user response with the filtered view from riot API
        ranked_info = requests.get(
            f"https://na.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{correct_act[0]['id']}",
            headers={"X-Riot-Token": API_KEY}).json()

        # Print name of top 10 players for example
        for player in ranked_info["players"]:
            # leaderboard ranks have no player name available so just print "Unknown player"
            player_name = player.get("gameName", "Unknown player")
            print(player["leaderboardRank"], player_name)

    page = render_template("landing.html")
    return render_template("base.html", content=Markup(page))


if __name__ == '__main__':
    app.run()
