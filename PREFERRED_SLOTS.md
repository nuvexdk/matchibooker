# Preferred Slots Feature

## Overview
The preferred slots feature allows you to define time slots by weekday and time (e.g., "Wednesday 20:00-21:00") that should be automatically booked when they become available.

## How It Works

1. **Define Preferred Slots**: Use the web UI to specify your preferred time slots by:
   - Selecting the day of the week (Monday-Sunday)
   - Setting the start time (HH:MM format)
   - Setting the end time (HH:MM format)

2. **Automatic Checking**: The system runs every hour (configurable in `queueworker.py`) to:
   - Check if your preferred slots are available in the next 7 days
   - Automatically add available preferred slots to the booking queue
   - Log the action for transparency

3. **Automatic Booking**: The existing booking system runs every minute to:
   - Attempt to book all slots in the queue
   - Remove successfully booked slots from the queue

## Usage

### Web Interface

1. Navigate to the home page
2. Click "Manage Preferred Slots"
3. Add your preferred time slots:
   - Select day of week
   - Enter start time (e.g., 20:00)
   - Enter end time (e.g., 21:00)
   - Click "Add Preferred Slot"
4. View and manage your preferred slots
5. Remove slots you no longer want

### Queue Worker

Run the queue worker to enable automatic checking and booking:

```bash
python3 queueworker.py
```

Enter your Matchi credentials when prompted. The worker will:
- Check for preferred slots every 60 minutes (default)
- Attempt to book queued slots every 1 minute
- Purge expired slots every 1 minute

### Configuration

In `queueworker.py`, you can adjust:
- `preferred_slot_check_interval_minutes = 60` - How often to check for preferred slots
- `booking_interval_minutes = 1` - How often to attempt booking
- `purging_interval_minutes = 1` - How often to remove expired slots

In `preferredslots.py`, you can adjust:
- `days_ahead=7` in `get_upcoming_dates_for_preferred_slots()` - How many days ahead to check

## Files Modified/Added

### New Files
- `preferredslots.py` - Module for managing preferred time slots
- `resources/preferredslots.json` - Database for storing preferred slots
- `templates/preferred.html` - Web UI for managing preferred slots

### Modified Files
- `app.py` - Added routes for preferred slots management
- `queueworker.py` - Added hourly job to check for preferred slots
- `slotqueue.py` - Added function to check and queue preferred slots
- `templates/login.html` - Added link to preferred slots page

## Example

To automatically book a tennis court every Wednesday at 20:00-21:00:

1. Open the web interface
2. Go to "Manage Preferred Slots"
3. Add a new slot:
   - Day: Wednesday
   - Start: 20:00
   - End: 21:00
4. Run the queue worker
5. Every hour, the system will check if Wednesday 20:00-21:00 is available in the next week
6. If available, it will automatically be added to the booking queue
7. The booking system will attempt to book it as soon as possible
