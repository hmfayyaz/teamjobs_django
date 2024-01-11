import datetime
import random
from typing import Any, Callable, Sequence

from ... import models


class RandomChoiceIterator:
    """Returns randomly from a number of choices."""

    def __init__(
        self,
        choices: Sequence[Any] | Callable[[], Sequence[Any]],
        weights: list[float | int] | None = None,
        size: int = 0,
    ) -> None:
        """Initialize the iterator

        Args:
            choices: An list of all the possible choices for each iteration
            weights: If present, the relative weight each choice is given
                (length must be equal to that of choices).
            size: How many items to give before raising StopIteration (0 means never)
        """
        self.size = size
        self.count = 0
        self._choices = choices
        self.weights = weights

    def __iter__(self):
        return self

    @property
    def choices(self):
        if callable(self._choices):
            return self._choices()
        return self._choices

    def __next__(self):
        self.count += 1
        if 0 < self.size < self.count:
            raise StopIteration
        return random.choices(self.choices, weights=self.weights)[0]  # nosec B311


class RandomDateTimeWithinRangeIterator:
    def __init__(
        self, from_date: datetime.datetime, to_date: datetime.datetime, size: int = 0
    ):
        """Create an iterator that returns random dates between a range.

        Args:
            from_date: datetime that marks the start of valid dates
            to_date: datetime that marks the end of valid dates
            size: if not zero, the number of items to provide.
        Raises:
            ValueError: if from_date > to_date
        """
        if from_date >= to_date:
            raise ValueError("From date {from_date} must come before to date {to_date}")
        difference = to_date - from_date
        self.from_date = from_date
        self.seconds_range = int(difference.total_seconds())
        self.size = size
        self.count = 0

    def random_timedelta(self):
        seconds = random.randint(0, self.seconds_range)  # nosec B311
        return datetime.timedelta(seconds=seconds)

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        if 0 < self.size < self.count:
            raise StopIteration
        return self.from_date + self.random_timedelta()


RandomCategoryIterator = RandomChoiceIterator(models.Category.objects.all)
RandomCertificateIterator = RandomChoiceIterator(models.Certificate.objects.all)
