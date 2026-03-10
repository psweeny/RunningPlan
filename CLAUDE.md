# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python marathon training plan generator that creates periodized weekly training schedules.

## Running Tests

```bash
# Run all tests
python -m unittest discover tests/ -v

# Run a single test file
python -m unittest tests.marathon_plan_test -v

# Run a single test
python -m unittest tests.marathon_plan_test.MarathonPlanTest.test_name -v
```

## Running the Application

```bash
python running_plan.py
```

## Architecture

### Core Classes

- **`Session`** (`week_schedule.py`): A single training session with name, date, type, and distance. Session types (enum `SessionType`): Rest, Recovery, Easy, Interval, Long, Race. Pattern codes: `R`=Recovery, `E`=Easy, `I`=Interval, `L`=Long, ` `=Rest.

- **`WeekSchedule`** (`week_schedule.py`): Manages 7 sessions for a week. Built from a pattern string (e.g., `"REI REL"` = Rest, Recovery, Easy, Interval, Rest, Easy, Long). Default is `LEE_GRANTHAM_PATTERN = "REI REL"`. Distributes total weekly distance equally across non-rest sessions.

- **`Race`** (`week_schedule.py`): Subclass of `Session` for race events.

- **`MarathonPlan`** (`marathon_plan.py`): Orchestrates the full training plan. Linearly interpolates distance from `base` to `peak` over the plan weeks, applies an **80% taper every 4th week**, and tapers the final weeks (penultimate at 75%, race week at 55% of peak).

### Key Constants

- `MARATHON_DISTANCE_KM = 42.195` in `marathon_plan.py`
- `LEE_GRANTHAM_PATTERN = "REI REL"` in `week_schedule.py`

### Environment

- Python 3.13.2 via pyenv
- Virtual environment in `.venv/`
- Dependencies: numpy, matplotlib (activate with `source .venv/bin/activate`)
- No `requirements.txt` — dependencies must be installed manually into `.venv`
