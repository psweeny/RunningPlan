from unittest import TestCase

import numpy as np
import datetime as dt

from marathon_plan import MarathonPlan
from week_schedule import SessionType, Race

MARATHON_KM = 42.195


def weekly_distance_trend(plan):
    x = np.arange(plan.weeks_duration())
    y = np.array(list(week.total_distance() for week in plan.week_schedule()))
    weekly_trend, _ = np.polyfit(x, y, 1)
    return weekly_trend


class MarathonPlanTest(TestCase):

    def test_a_12_week_plan_has_12_weeks(self):
        plan = MarathonPlan(weeks=12)
        self.assertEqual(12, plan.weeks())

    def test_a_12_week_plan_has_a_12_week_schedule(self):
        plan = MarathonPlan(weeks=12)
        self.assertEqual(12, len(plan.week_schedule()))

    def test_a_8_week_plan_has_an_8_week_schedule(self):
        plan = MarathonPlan(weeks=8)
        self.assertEqual(8, len(plan.week_schedule()))

    def test_a_12_week_plan_has_at_least_12_sessions(self):
        plan = MarathonPlan(weeks=12)
        session_count = sum((len(week.sessions()) for week in plan.week_schedule()))
        self.assertTrue(session_count >= 12)

    def test_every_week_has_a_unique_name(self):
        plan = MarathonPlan()
        names = list(week.name() for week in plan.week_schedule())
        self.assertEqual(len(names), len(set(names)))

    def test_every_training_session_has_a_unique_name(self):
        plan = MarathonPlan()
        names = list((session.name() for session in week.sessions()) for week in plan.week_schedule())
        self.assertEqual(len(names), len(set(names)))

    def test_every_training_session_name_is_prefixed_with_its_week_name(self):
        plan = MarathonPlan()
        session_count = sum((len(week.sessions()) for week in plan.week_schedule()))
        prefix_count = 0
        for week in plan.week_schedule():
            for session in week.sessions():
                if session.name().startswith(week.name()):
                    prefix_count += 1
        self.assertEqual(session_count, prefix_count)

    def test_every_week_has_a_long_run(self):
        plan = MarathonPlan()
        self.assertEqual(plan.weeks(), sum(any(s.session_type() == SessionType.Long for s in w.sessions())
                                 for w in plan.week_schedule()))

    def test_every_week_has_a_rest_day(self):
        plan = MarathonPlan()
        self.assertEqual(plan.weeks(), sum(7 - len(w.sessions()) for w in plan.week_schedule()))

    def test_every_week_has_an_interval_session(self):
        plan = MarathonPlan()
        self.assertEqual(plan.weeks(), sum(any(s.session_type() == SessionType.Interval for s in w.sessions())
                                 for w in plan.week_schedule()))

    def test_no_week_has_less_distance_than_the_base(self):
        plan = MarathonPlan()
        self.assertTrue(all(week.total_distance() >= plan.base_distance()
                            for week in plan.week_schedule()))

    def test_no_week_has_more_distance_than_the_peak(self):
        plan = MarathonPlan()
        self.assertTrue(all(week.total_distance() <= plan.peak_distance() + 0.1
                            for week in plan.week_schedule()))

    def test_the_first_week_distance_should_be_the_base(self):
        plan = MarathonPlan()
        first_week = plan.week_schedule()[0]
        self.assertAlmostEqual(first_week.total_distance(), plan.base_distance(), delta=1.0)

    def test_the_last_week_distance_should_be_the_peak(self):
        plan = MarathonPlan()
        last_week = plan.week_schedule()[-1]
        self.assertAlmostEqual(last_week.total_distance(), plan.peak_distance(), delta=1.0)

    def test_race_distance_is_42_km(self):
        self.assertAlmostEqual(MarathonPlan(12).race_distance(), MARATHON_KM, delta=0.1)

    def test_race_distance_is_26_miles(self):
        self.assertAlmostEqual(MarathonPlan(12, units='miles').race_distance(), 26.2, delta=0.1)

    def test_last_run_of_the_plan_is_the_race(self):
        race = Race('London Marathon', dt.date(2026,4,26), MARATHON_KM)
        plan = MarathonPlan(race=race)
        last_session = plan.week_schedule()[-1].sessions()[-1]
        self.assertAlmostEqual(last_session.distance(), MARATHON_KM, delta=1.0)

    def test_last_session_of_the_plan_is_the_race(self):
        race = Race('London Marathon', dt.date(2026,4,26), MARATHON_KM)
        plan = MarathonPlan(race=race)
        last_session = plan.week_schedule()[-1].sessions()[-1]
        self.assertEqual(race, last_session)

    def test_milage_trend_increases_across_the_weeks(self):
        self.assertGreaterEqual(weekly_distance_trend(MarathonPlan(12)), 1.0)

    def test_weekly_milage_increase_is_less_than_ten_percent(self):
        plan = MarathonPlan()
        distance_trend = weekly_distance_trend(plan)
        self.assertLessEqual((distance_trend / plan.base_distance()) * 100, 10.0)

    def test_load_peaks_at_the_third_from_last_week(self):
        schedule = MarathonPlan().week_schedule()
        peak = schedule[-3].total_distance()
        self.assertFalse(any(w.total_distance() > peak for w in schedule), 'no weeks with more load than the peak week')

    def test_tapered_last_week_distance_is_50_to_60_percent_of_peak(self):
        schedule = MarathonPlan().week_schedule()
        peak = schedule[-3].total_distance()
        last = schedule[-1].total_distance()
        pct = (last / peak) * 100
        self.assertTrue(50 <= pct <= 60, f'pct {pct:.1f}% between 50-60%')

    def test_tapered_penultimate_weekly_distance_is_70_to_80_percent_of_peak(self):
        schedule = MarathonPlan().week_schedule()
        peak = schedule[-3].total_distance()
        penultimate = schedule[-2].total_distance()
        pct = (penultimate / peak) * 100
        self.assertTrue(70 <= pct <= 80, f'taper {pct:.1f}% between 70-80%')

    def test_load_tapers_to_80_percent_every_four_weeks(self):
        schedule = MarathonPlan().week_schedule()
        for i in range(3, 12, 4):
            prev = schedule[i-1].total_distance()
            taper = schedule[i].total_distance()
            pct = (taper / prev) * 100
            self.assertAlmostEqual(80.0, pct, msg=f'taper at week {i+1}, {pct:.1f}% is approx 80%', delta=0.05)
