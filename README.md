# RunningPlan

A marathon training plan generator that produces periodised weekly schedules based on an upcoming race date and target mileage.

Create a training plan in the run-up to a major race event, typically a half-marathon or longer.  Tell the plan your current weekly mileage and the maximum peak mileage you want to run per week.  Choose the days of the week you would like to run, the type of running sessions that you want on each day, by setting a running pattern.  The planner will then create the schedule for each day, including the suggested running distance to safely increase mileage and avoid injury.


## Usage

```bash
python running_plan.py
```

This generates a 12-week plan for the Boston Marathon, printing a week-by-week schedule to the terminal.

To create a custom plan:

```python
from marathon_plan import MarathonPlan, MARATHON_DISTANCE_KM
from week_schedule import Race
import datetime as dt

race = Race('Boston Marathon', dt.date(2026, 4, 20), MARATHON_DISTANCE_KM)
plan = MarathonPlan(weeks=16, base=40.0, peak=100.0, race=race)
print(plan.report())
```


## Training Structure

Weekly sessions by default follow the **Lee Grantham Pattern**: Rest, Recovery, Easy, Interval, Rest, Easy, Long run.

Distance progression:
- Linearly increases from `base` to `peak` km over the term of the training plan.
- Every 4th week, training load tapers to 80% of the previous week to allow for recovery.
- A taper in the final 2 weeks: penultimate week at 75%, race week at 55% of peak load.


## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install numpy matplotlib
```

## Tests

```bash
python -m unittest discover tests/ -v
```

