import csv
import json
import io
from dateutil.relativedelta import *

from ical.calendar import Calendar
from ical.calendar_stream import IcsCalendarStream
from ical.event import Event


def schedule_to_json(schedule_in: list[dict]) -> io.BytesIO:
    json_proxy = io.StringIO()
    json_proxy.write(json.dumps(schedule_in, indent=4, sort_keys=True, default=str))
    return _stringio_to_bytesio(json_proxy)


def schedule_to_csv(schedule_in: list[dict]) -> io.BytesIO:
    csv_proxy = io.StringIO()
    writer = csv.writer(csv_proxy)
    writer.writerow(schedule_in[0].keys())
    for game in schedule_in:
        writer.writerow(game.values())
    return _stringio_to_bytesio(csv_proxy)


def schedule_to_ical(schedule_in: list[dict]) -> io.BytesIO:
    ics_proxy = io.StringIO()
    cal = Calendar()
    for game in schedule_in:
        cal.events.append(
            Event(
                summary=f"{game['away']['abbrev']} at {game['home']['abbrev']}",
                start=game["datetime"],
                end=game["datetime"] + relativedelta(hours=2, minutes=30),
                description="\n".join(game["network"]),
                categories=["NHL"],
                location=f"{game['venue']}",
            )
        )
    ics_proxy.write(IcsCalendarStream.calendar_to_ics(cal))
    return _stringio_to_bytesio(ics_proxy)


def _stringio_to_bytesio(stringio_in: io.StringIO) -> io.BytesIO:
    # Creating the ByteIO object from the StringIO Object
    # See: https://stackoverflow.com/questions/35710361/python-flask-send-file-stringio-blank-files
    stringio_in.seek(0)
    bytes = io.BytesIO()
    bytes.write(stringio_in.getvalue().encode())
    bytes.seek(0)
    return bytes
