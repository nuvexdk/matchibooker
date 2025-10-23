from flask import *
import slotqueue
import preferredslots
import browsing
import ast

app = Flask(__name__)

# setup browser and cookies
browser = browsing.Browser()
default_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/71.0.3578.98 Safari/537.36 "

default_date_format = "%Y-%m-%d"
default_base_url = "https://www.matchi.se"
default_schedule_url = "https://www.matchi.se/book/schedule?name=spangatbk&sport=1&indoor=true&facilityId=55&wl="
available_time_class = "courtLinks"


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/booking", methods=["POST"])
def booking():
    username = request.form["username"]
    password = request.form["password"]

    browser.matchi_login(username, password)
    booking_slots = slotqueue.get_available_slots(browser)

    return render_template("booking.html", booking_slots=booking_slots)


@app.route("/queued", methods=["POST"])
def queued():
    slots = request.form.getlist("slot_checkbox")
    slots_parsed = []
    for slot in slots:
        slot = ast.literal_eval(slot)  # convert string representation of list to python list
        slot_parsed = slotqueue.TimeSlot(slot[0])
        slots_parsed.append(slot_parsed)
        slotqueue.add_entry(slot[0], slot[1], slot[2], slot[3])
    return render_template("queued.html", queued_slots=slots_parsed)


@app.route("/preferred")
def preferred():
    """Display preferred slots management page"""
    preferred_slots = preferredslots.get_all_preferred_slots()
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    return render_template("preferred.html", preferred_slots=preferred_slots, weekdays=weekdays)


@app.route("/add_preferred", methods=["POST"])
def add_preferred():
    """Add a new preferred slot"""
    weekday = request.form["weekday"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    
    try:
        preferredslots.add_preferred_slot(weekday, start_time, end_time)
        return redirect(url_for('preferred'))
    except ValueError:
        return "Error: Invalid weekday specified", 400


@app.route("/remove_preferred", methods=["POST"])
def remove_preferred():
    """Remove a preferred slot"""
    weekday = request.form["weekday"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    
    preferredslots.remove_preferred_slot(weekday, start_time, end_time)
    return redirect(url_for('preferred'))


if __name__ == '__main__':
    app.run()
