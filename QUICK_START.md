# Quick Start Guide - Preferred Slots Feature

## For End Users

### Add a Preferred Slot (Web UI)

1. Start the Flask app:
   ```bash
   python3 app.py
   ```

2. Open your browser to `http://localhost:5000`

3. Click "Manage Preferred Slots"

4. Fill in the form:
   - **Day of Week**: Select the day (e.g., Wednesday)
   - **Start Time**: Enter in HH:MM format (e.g., 20:00)
   - **End Time**: Enter in HH:MM format (e.g., 21:00)

5. Click "Add Preferred Slot"

6. Your slot is now saved and will be checked hourly!

### Run the Automated System

```bash
python3 queueworker.py
```

Enter your Matchi username and password when prompted.

**The system will:**
- ✓ Check for preferred slots every 60 minutes
- ✓ Attempt to book queued slots every 1 minute
- ✓ Remove expired slots every 1 minute
- ✓ Log all actions to `resources/log.txt`

### View Logs

```bash
tail -f resources/log.txt
```

This shows real-time updates of what the system is doing.

## For Developers

### Key Configuration Variables

**In `queueworker.py`:**
```python
preferred_slot_check_interval_minutes = 60  # How often to check (default: 1 hour)
booking_interval_minutes = 1                # How often to try booking (default: 1 min)
purging_interval_minutes = 1                # How often to clean up (default: 1 min)
```

**In `preferredslots.py`:**
```python
days_ahead=7  # How many days ahead to check (default: 7 days)
```

### Key Functions

**Add a preferred slot programmatically:**
```python
import preferredslots
preferredslots.add_preferred_slot("wednesday", "20:00", "21:00")
```

**Get all preferred slots:**
```python
slots = preferredslots.get_all_preferred_slots()
for slot in slots:
    print(f"{slot.weekday} {slot.start_time}-{slot.end_time}")
```

**Get upcoming dates for preferred slots:**
```python
date_map = preferredslots.get_upcoming_dates_for_preferred_slots(days_ahead=7)
for date, slots in date_map.items():
    print(f"{date}: {slots}")
```

### Database Structure

**preferredslots.json:**
```json
{
  "_default": {
    "1": {
      "weekday": "wednesday",
      "start_time": "20:00",
      "end_time": "21:00"
    }
  }
}
```

**bookingqueue.json:**
```json
{
  "_default": {
    "1": {
      "url": "https://www.matchi.se/bookingPayment/preConfirm?...",
      "date": "2025-10-29",
      "start_time": "20:00",
      "end_time": "21:00"
    }
  }
}
```

## Troubleshooting

### Preferred slots not being found?
- Check that the weekday is spelled correctly (lowercase)
- Ensure time format is HH:MM (24-hour format)
- Verify slots are actually available on Matchi.se
- Check the log file for errors

### System not booking?
- Ensure queueworker.py is running
- Check your Matchi credentials are correct
- Verify you're logged in (check log file)
- Make sure slots are in bookingqueue.json

### How to reset everything?
```bash
# Clear preferred slots
echo '{"_default": {}}' > resources/preferredslots.json

# Clear booking queue
echo '{"_default": {}}' > resources/bookingqueue.json

# Clear logs
> resources/log.txt
```

## Examples

### Example 1: Book tennis every Wednesday evening
```python
preferredslots.add_preferred_slot("wednesday", "20:00", "21:00")
```

### Example 2: Book multiple slots
```python
preferredslots.add_preferred_slot("monday", "07:00", "08:00")
preferredslots.add_preferred_slot("wednesday", "20:00", "21:00")
preferredslots.add_preferred_slot("friday", "18:00", "19:00")
```

### Example 3: Remove a slot
```python
preferredslots.remove_preferred_slot("friday", "18:00", "19:00")
```

## Support

For more details, see:
- `PREFERRED_SLOTS.md` - Detailed feature documentation
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details
- `WORKFLOW.md` - Visual workflow diagrams
- `README.md` - General project information
