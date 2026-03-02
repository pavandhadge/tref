---
library: python
version: "3.9.0"
category: api
item: python.datetime
type: module
signature: "datetime.datetime.now(), datetime.date.today()"
keywords: ["datetime", "time", "date", "timestamp"]
aliases: ["date time", "timestamps", "time handling"]
intent: "Manipulate dates, times, and timestamps for scheduling, logging, and time-based calculations."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.python.org/3/library/datetime.html"
source_title: "datetime Module"
alternatives:
  - option: "time module"
    reason: "Lower-level time functions, POSIX timestamps."
  - option: "dateutil"
    reason: "Advanced parsing, timezone handling."
  - option: "pendulum"
    reason: "More intuitive API, powerful timezone support."
---

# datetime

## Signature
```python
from datetime import datetime, date, time, timedelta

now = datetime.now()
today = date.today()
dt = datetime(2024, 1, 15, 10, 30, 0)
```

## What It Does
Classes for manipulating dates and times: date, datetime, time, timedelta. Supports arithmetic, formatting, timezones (with pytz or zoneinfo in Python 3.9+).

## Use When
- Timestamps and timestamps.
- Date arithmetic (add days, subtract dates).
- Formatting dates for display.
- Timezone conversions.

## Examples
```python
from datetime import datetime, timedelta

# Current time
now = datetime.now()
utc_now = datetime.utcnow()
timestamp = datetime.timestamp(now)

# Create datetime
dt = datetime(2024, 6, 15, 14, 30, 0)
dt = datetime.fromisoformat("2024-06-15T14:30:00")

# Components
dt.year, dt.month, dt.day
dt.hour, dt.minute, dt.second
dt.weekday()  # 0=Monday

# Arithmetic
tomorrow = dt + timedelta(days=1)
two_hours_later = dt + timedelta(hours=2)
diff = dt2 - dt1  # returns timedelta
```

```python
# Formatting
dt.strftime("%Y-%m-%d %H:%M:%S")  # "2024-06-15 14:30:00"
dt.isoformat()  # "2024-06-15T14:30:00"

# Parsing
dt = datetime.strptime("2024-06-15 14:30", "%Y-%m-%d %H:%M")
```

```python
# Timezone (Python 3.9+)
from datetime import timezone
dt_utc = datetime.now(timezone.utc)
dt_pst = dt_utc.astimezone(timezone(timedelta(hours=-8)))
```

```python
# date object
today = date.today()
d = date(2024, 6, 15)
d.strftime("%B %d, %Y")  # "June 15, 2024"
```

## Returns
datetime, date, time, or timedelta object

## Gotchas / Version Notes
- datetime objects are naive by default (no timezone).
- Use timezone-aware for real applications.
- timedelta has max of 999999999 days.
- Use dateutil for complex parsing.

## References
- datetime docs: https://docs.python.org/3/library/datetime.html
