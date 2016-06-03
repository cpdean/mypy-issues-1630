from typing import Any, Callable, Generator, Iterable, Tuple, Sized, Union, Optional  # NOQA
import time

from contextlib import contextmanager


class TimeTrackingCursor(object):
    def execute(self, sql):
        # type: (str) -> str
        # note how type annotations omit 'self'
        return sql + "1"

    def executemany(self, sqls):
        # type: (Iterable[str]) -> Iterable[str]
        return [s + "1" for s in sqls]

    def mogrify(self, sql, params=()):
        # type: (str, Iterable[Any]) -> str
        return "mogrified"


class Foo(object):
    def foo_method(self, s):
        # type: (str) -> str
        return s


@contextmanager
def queries_captured():
    # type: () -> Generator[List[Dict[str, str]], None, None]
    '''
    Allow a user to capture just the queries executed during
    the with statement.
    '''

    queries = []

    def wrapper_execute(self, action, sql, params=()):
        # type: (Callable, str, Iterable[Any]) -> None
        # out of habit, omitting 'self'
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

    def cursor_execute(self, sql, params=()):  # type: ignore
        return wrapper_execute(self, super(TimeTrackingCursor, self).execute, sql, params)  # type: ignore
    TimeTrackingCursor.execute = cursor_execute  # type: ignore

    def cursor_executemany(self, sql, params=()):  # type: ignore
        return wrapper_execute(self, super(TimeTrackingCursor, self).executemany, sql, params)  # type: ignore
    TimeTrackingCursor.executemany = cursor_executemany  # type: ignore

    yield queries

    TimeTrackingCursor.execute = old_execute  # type: ignore
    TimeTrackingCursor.executemany = old_executemany  # type: ignore
