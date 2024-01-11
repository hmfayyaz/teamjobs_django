import datetime
import itertools
import random

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from api.factories.utils import iterators

RANDOM_SEED = 0


@pytest.fixture
def from_date():
    return datetime.datetime(2020, 1, 1, 12, 5, 2)


@pytest.fixture
def to_date():
    return datetime.datetime(2020, 1, 1, 14, 0)


@pytest.fixture(autouse=True)
def random_seed():
    random.seed(RANDOM_SEED)


def test_random_choice_iterator():
    random_values = set(
        itertools.islice(iterators.RandomChoiceIterator(range(10)), 1000)
    )
    assert len(random_values) == 10
    assert random_values == {n for n in range(10)}


def test_random_choice_iterator_weights():
    random_values = list(
        itertools.islice(
            iterators.RandomChoiceIterator(range(2), weights=[10, 1]), 1000
        )
    )
    assert random_values.count(0) > random_values.count(1)


def test_random_choice_iterator_size():
    random_values = list(
        itertools.islice(iterators.RandomChoiceIterator(range(2), size=3), 1000)
    )
    assert len(random_values) == 3


def test_random_datetime_generator_to_before_from(from_date, to_date):
    with pytest.raises(ValueError):
        iterators.RandomDateTimeWithinRangeIterator(
            from_date=to_date, to_date=from_date
        )


def test_random_datetime_generator_from_equals_to(from_date):
    with pytest.raises(ValueError):
        iterators.RandomDateTimeWithinRangeIterator(
            from_date=from_date, to_date=from_date
        )


@given(st.datetimes(), st.datetimes())
def test_random_datetime_generator(start_date, end_date):
    assume(start_date < end_date)
    date_iter = iterators.RandomDateTimeWithinRangeIterator(start_date, end_date)
    for instance in itertools.islice(date_iter, 1000):
        assert start_date <= instance <= end_date


def test_random_datetime_iterator_size(from_date, to_date):
    random_values = list(
        itertools.islice(
            iterators.RandomDateTimeWithinRangeIterator(from_date, to_date, size=3),
            1000,
        )
    )
    assert len(random_values) == 3
