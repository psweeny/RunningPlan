from enum import Enum
import datetime as dt

LEE_GRANTHAM_PATTERN = "REI REL"


class SessionType(Enum):
    Rest = 0
    Recovery = 1
    Easy = 2
    Interval = 3
    Long = 4
    Race = 5


class Session:
    def __init__(self, name: str, date: dt.date, session_type: SessionType, distance: float):
        self._name = name
        self._date = date
        self._session_type = session_type
        self._distance = distance

    # Returns the name of the training session.
    def name(self):
        return self._name

    def date(self):
        return self._date

    # Returns the type of the training session.
    def session_type(self) -> SessionType:
        return self._session_type

    def distance(self):
        return self._distance

    def report(self, units: str):
        day = self._date.strftime('%A')[:3]
        return f"{day} {self._date} {self._name} {self._session_type.name} {self._distance:.1f}{units}"

    def __str__(self):
        return self.report("")

    def __eq__(self, other):
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


    _TYPE_MAP = {
        ' ': SessionType.Rest,
        'R': SessionType.Recovery,
        'E': SessionType.Easy,
        'I': SessionType.Interval,
        'L': SessionType.Long,
    }

    @classmethod
    def to_session_type(cls, code: str) -> SessionType:
        stype = cls._TYPE_MAP.get(code, None)
        if stype is None:
            raise Exception(f'unknown session type "{code}", expected one of {cls._TYPE_MAP.keys()}')
        return stype


class Race(Session):
    def __init__(self, name: str, date: dt.date, distance: float):
        super().__init__(name, date, SessionType.Race, distance)


class WeekSchedule:

    def __init__(self, week_no: int, date: dt.date, target_distance: float,
                 pattern=LEE_GRANTHAM_PATTERN, race: Race = None):
        assert date.weekday() == 0, "the week should start on Monday"
        self._week_no = week_no
        self._start_date = date
        self._sessions = self._build_week_sessions(target_distance, pattern, race)

    def _build_week_sessions(self, target_distance, pattern, race) -> list[Session]:
        assert len(pattern) == 7, "there should be 7 days (chars) in a weekly training pattern"
        training_days = 7 - pattern.count(' ')
        distance = target_distance / training_days
        sessions = []
        session_no = 1
        for weekday in range(7):
            session_type = Session.to_session_type(pattern[weekday])
            if session_type != SessionType.Rest and distance >= 1.0:
                date = self._start_date + dt.timedelta(days=weekday)
                sessions.append(Session(f'{self.name()}-S{session_no}', date, session_type, distance))
                session_no += 1
        if race is not None:
            # TOTO remove all sessions on or after the race date
            sessions = list(filter(lambda s: s.date() < race.date(), sessions))
            sessions.append(race)
        return sessions

    def __str__(self):
        return self.report("")

    # Returns the training session for the week.
    def sessions(self) -> list[Session]:
        return self._sessions

    # Returns the total distance to be run in the week.
    def total_distance(self) -> float:
        return sum((session.distance() for session in self._sessions), 0.0)

    # Returns the unique name of the week.
    def name(self) -> str:
        return f'W{self._week_no}'

    def report(self, units: str):
        s = '\n'.join(session.report(units) for session in self._sessions)
        return '\n'.join((f"Week {self._week_no}, {self.total_distance():.1f}{units}", s, ""))
