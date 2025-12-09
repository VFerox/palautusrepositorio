from matchers import And, PlaysIn, HasAtLeast, HasFewerThan, All, Or

class QueryBuilder:
    def __init__(self, matchers=None):
        self._matchers = matchers or []

    def build(self):
        if not self._matchers:
            return All()
        return And(*self._matchers)

    def plays_in(self, team):
        return QueryBuilder(self._matchers + [PlaysIn(team)])

    def has_at_least(self, value, attr):
        return QueryBuilder(self._matchers + [HasAtLeast(value, attr)])

    def has_fewer_than(self, value, attr):
        return QueryBuilder(self._matchers + [HasFewerThan(value, attr)])

    def one_of(self, *builders):
        matchers = [b.build() for b in builders]
        return QueryBuilder(self._matchers + [Or(*matchers)])
