from marathon_plan import MarathonPlan, MARATHON_DISTANCE_KM
import datetime as dt
from week_schedule import Race


def running_plan():
    race = Race('Chicago Marathon', dt.date(2025, 10, 12), MARATHON_DISTANCE_KM)
    plan = MarathonPlan(12, race=race)
    print(plan.report())


if __name__ == "__main__":
    running_plan()
