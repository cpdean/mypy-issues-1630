from typing import Any, Callable, Generator, Iterable, Tuple, Sized, Union, Optional # NOQA
import time

from contextlib import contextmanager

# note how type annotations omit 'self'
class TimeTrackingCursor(object):
    def cursor_execute(self, sql):
        # type: (str) -> str
        return sql + "1"

    def cursor_execute_many(self, sqls):
        # type: (Iterable[str]) -> Iterable[str]
        return [s + "1" for s in sqls]

@contextmanager
def queries_captured():
    # type: () -> Generator[List[Dict[str, str]], None, None]
    '''
    Allow a user to capture just the queries executed during
    the with statement.
    '''

    queries = []

    # out of habit, omitting 'self'
    def wrapper_execute(self, action, sql, params=()):
        # type: (Callable, str, Iterable[Any]) -> None
        start = time.time()
        try:
            return action(sql, params)
        finally:
            stop = time.time()
            duration = stop - start
            queries.append({
                'sql': self.mogrify(sql, params),
                'time': "%.3f" % duration,
            })

    old_execute = TimeTrackingCursor.execute
    old_executemany = TimeTrackingCursor.executemany

    def cursor_execute(self, sql, params=()): # type: ignore # maybe related to https://github.com/JukkaL/mypy/issues/1167
        return wrapper_execute(self, super(TimeTrackingCursor, self).execute, sql, params) # type: ignore # https://github.com/JukkaL/mypy/issues/1167 # NOQA
    TimeTrackingCursor.execute = cursor_execute # type: ignore # maybe related to https://github.com/JukkaL/mypy/issues/1167

    def cursor_executemany(self, sql, params=()): # type: ignore # maybe related to https://github.com/JukkaL/mypy/issues/1167
        return wrapper_execute(self, super(TimeTrackingCursor, self).executemany, sql, params) # type: ignore # https://github.com/JukkaL/mypy/issues/1167 # NOQA
    TimeTrackingCursor.executemany = cursor_executemany # type: ignore # https://github.com/JukkaL/mypy/issues/1167

    yield queries

    TimeTrackingCursor.execute = old_execute # type: ignore # https://github.com/JukkaL/mypy/issues/1167
    TimeTrackingCursor.executemany = old_executemany # type: ignore # https://github.com/JukkaL/mypy/issues/1167
