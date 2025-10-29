# Workflow Diagram

## System Architecture with Preferred Slots

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Interaction                              │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                    ┌──────────────┴───────────────┐
                    │                              │
                    ▼                              ▼
        ┌────────────────────┐         ┌─────────────────────┐
        │   Manual Booking   │         │  Preferred Slots    │
        │   (existing flow)  │         │   (NEW feature)     │
        └────────────────────┘         └─────────────────────┘
                    │                              │
                    │                              │
    1. User selects specific              1. User defines recurring
       slots from available list             slots by weekday + time
                    │                              │
                    │                              │
                    ▼                              ▼
        ┌────────────────────┐         ┌─────────────────────┐
        │ bookingqueue.json  │◄────────│ preferredslots.json │
        │                    │         │                     │
        │ Specific slots to  │         │ Weekday + time      │
        │ book (with dates)  │         │ patterns            │
        └────────────────────┘         └─────────────────────┘
                    │                              │
                    │                              │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │     QueueWorker          │
                    │  (runs continuously)     │
                    └──────────────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
        ┌────────────────┐ ┌──────────────┐ ┌─────────────────────┐
        │  Purge Job     │ │ Booking Job  │ │ Preferred Check Job │
        │  Every 1 min   │ │ Every 1 min  │ │   Every 60 min      │
        └────────────────┘ └──────────────┘ └─────────────────────┘
                    │              │              │
                    │              │              │
                    │              │              └─────────────┐
                    │              │                            │
                    │              │         1. Check Matchi.se for
                    │              │            available slots
                    │              │                            │
                    │              │         2. Match against preferred
                    │              │            patterns (weekday+time)
                    │              │                            │
                    │              │         3. Add matching slots
                    │              │            to bookingqueue.json
                    │              │                            │
                    │              ▼◄───────────────────────────┘
                    │    ┌─────────────────┐
                    │    │  Try to book    │
                    │    │  all queued     │
                    │    │  slots          │
                    │    └─────────────────┘
                    │              │
                    ▼              ▼
            Remove expired   Remove successfully
            slots from       booked slots from
            queue            queue
                    │              │
                    └──────┬───────┘
                           │
                           ▼
                ┌──────────────────┐
                │  resources/      │
                │  log.txt         │
                │                  │
                │  All actions     │
                │  are logged      │
                └──────────────────┘
```

## Example Flow: Wednesday 20:00-21:00

```
Day 0 (Thursday):
  User adds preferred slot: "Wednesday 20:00-21:00"
  ↓
  Stored in preferredslots.json
  
Hour 0:
  QueueWorker checks for available slots
  ↓
  Finds no Wednesday slots available yet (too far ahead)
  
Hour 1:
  QueueWorker checks again (runs every hour)
  ↓
  Finds Wednesday slot available in 6 days
  ↓
  Automatically adds to bookingqueue.json
  
Minute 0-60:
  Booking job tries to book every minute
  ↓
  Successfully books the slot
  ↓
  Removes from bookingqueue.json
  ↓
  Logs success to log.txt
  
Result:
  ✓ User gets their preferred Wednesday slot automatically!
```

## Key Benefits

1. **Set and Forget**: Define preferred slots once, system books them automatically
2. **No Manual Checking**: Hourly automated checking for availability
3. **Fast Booking**: Once found, attempts booking every minute
4. **Transparent**: All actions logged
5. **Flexible**: Works alongside manual slot selection
6. **Recurring**: Same preferred slot applies every week
