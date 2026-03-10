from week_schedule import WeekSchedule, Race
import datetime as dt

MARATHON_DISTANCE_KM = 42.195
KM_PER_MILE = 1.609344


# Returns the date of the next weekday (e.g., 0 for Monday) after a given date.
def next_weekday(date: dt.date, weekday: int):
    days_ahead = weekday - date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return date + dt.timedelta(days_ahead)


class MarathonPlan:
    def __init__(self, weeks=12, base=40.0, peak=100.0, race: Race = None, units='km'):
        assert weeks > 1, "a training plan must span more than 1 week"
        assert 0 < base <= peak, "base must be between 0 and peak distance"
        self._weeks = weeks
        self._base_distance = base
        self._peak_distance = peak
        self._race = race or Race('', dt.date.today() + dt.timedelta(weeks=weeks), MARATHON_DISTANCE_KM)
        self._start_date = next_weekday(self._race.date() - dt.timedelta(weeks=weeks), 0)
        self._units = units
        self._week_schedule = self._build_schedule(weeks, race)

    def _build_schedule(self, weeks: int, race: Race) -> list[WeekSchedule]:
        schedule: list[WeekSchedule] = []
        distance = self._base_distance
        delta = (4 / 3) *(self._peak_distance - self._base_distance) / (weeks - 1)
        for week_no in range(1, weeks - 1):
            taper = 0.8 if (week_no % 4) == 0 else 1
            schedule.append(WeekSchedule(week_no, self._week_date(week_no), taper * distance))
            if taper == 1:
                distance += delta
        peak_distance = schedule[-1].total_distance()
        schedule.append(WeekSchedule(weeks - 1, self._week_date(weeks - 1), peak_distance * 0.75))
        schedule.append(WeekSchedule(weeks, self._week_date(weeks), peak_distance * 0.55, race=race))
        return schedule

    def _week_date(self, week_no):
        return self._start_date + dt.timedelta(weeks=week_no)

    def week_schedule(self) -> list[WeekSchedule]:
        return self._week_schedule

    def base_distance(self) -> float:
        return self._base_distance

    def peak_distance(self) -> float:
        return self._peak_distance

    def total_distance(self) -> float:
        return sum(s.total_distance for s in self._week_schedule)

    def race_distance(self) -> float:
        return MARATHON_DISTANCE_KM if self._units == 'km' else MARATHON_DISTANCE_KM / KM_PER_MILE

    def report(self) -> str:
        return '\n'.join(week.report(self._units) for week in self._week_schedule)

    def weeks_duration(self):
        return len(self._week_schedule)

    def weeks(self) -> int:
        return self._weeks
