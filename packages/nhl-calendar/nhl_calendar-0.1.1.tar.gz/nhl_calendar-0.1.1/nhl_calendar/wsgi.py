from flask import Flask, send_file, render_template
from nhl_calendar.schedule import get_full_season_by_team, NHL_TEAMS
from nhl_calendar.output import schedule_to_csv, schedule_to_ical, schedule_to_json

app = Flask(__name__)


@app.route("/nhl-schedule/<season>/<team>.<output_type>")
@app.route("/nhl-schedule/<team>.<output_type>")
@app.route("/nhl-schedule/<team>")
def schedule(team: str, season: str = "now", output_type: str = "stream"):
    games = get_full_season_by_team(team, season)
    if output_type == "json":
        json_file = schedule_to_json(games)
        return send_file(
            json_file,
            mimetype="text/json",
            as_attachment=True,
            download_name=f"{team}.json",
        )
        return games
    elif output_type == "csv":
        csv_file = schedule_to_csv(games)
        return send_file(
            csv_file,
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"{team}.csv",
        )
    elif output_type == "ics":
        ical_file = schedule_to_ical(games)
        return send_file(
            ical_file,
            mimetype="text/calendar",
            as_attachment=True,
            download_name=f"{team}.ics",
        )
    elif output_type == "stream":
        return games
    else:
        return

@app.route("/")
def index():
   return render_template("index.j2.html", teams=NHL_TEAMS) 
