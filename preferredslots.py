from datetime import datetime, timedelta
from tinydb import TinyDB, Query
import re

default_date_format = "%Y-%m-%d"
default_time_format = '%H:%M'

# Weekday mapping (Monday=0, Sunday=6)
WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}


class PreferredSlot:
    """Represents a preferred time slot by weekday and time"""
    def __init__(self, weekday, start_time, end_time):
        self.weekday = weekday.lower()
        self.start_time = start_time
        self.end_time = end_time
        if self.weekday not in WEEKDAYS:
            raise ValueError(f"Invalid weekday: {weekday}")
    
    def to_dict(self):
        return {
            "weekday": self.weekday,
            "start_time": self.start_time,
            "end_time": self.end_time
        }
    
    def __repr__(self):
        return f"{self.weekday.capitalize()} {self.start_time}-{self.end_time}"


def add_preferred_slot(weekday, start_time, end_time):
    """Add a preferred slot to the database"""
    db = TinyDB("resources/preferredslots.json")
    slot = PreferredSlot(weekday, start_time, end_time)
    db.insert(slot.to_dict())
    db.close()


def get_all_preferred_slots():
    """Get all preferred slots from the database"""
    db = TinyDB("resources/preferredslots.json")
    slots = []
    for slot_data in db:
        slots.append(PreferredSlot(
            slot_data["weekday"],
            slot_data["start_time"],
            slot_data["end_time"]
        ))
    db.close()
    return slots


def remove_preferred_slot(weekday, start_time, end_time):
    """Remove a preferred slot from the database"""
    db = TinyDB("resources/preferredslots.json")
    SlotQuery = Query()
    db.remove((SlotQuery.weekday == weekday.lower()) & 
              (SlotQuery.start_time == start_time) & 
              (SlotQuery.end_time == end_time))
    db.close()


def get_upcoming_dates_for_preferred_slots(days_ahead=7):
    """
    Get a list of dates for the upcoming preferred slots
    Returns a dict mapping dates to list of preferred slots
    """
    preferred_slots = get_all_preferred_slots()
    date_slot_map = {}
    
    for day_offset in range(0, days_ahead):
        date = datetime.today() + timedelta(days=day_offset)
        weekday_num = date.weekday()
        date_str = date.strftime(default_date_format)
        
        # Find preferred slots for this weekday
        for slot in preferred_slots:
            if WEEKDAYS[slot.weekday] == weekday_num:
                if date_str not in date_slot_map:
                    date_slot_map[date_str] = []
                date_slot_map[date_str].append(slot)
    
    return date_slot_map
