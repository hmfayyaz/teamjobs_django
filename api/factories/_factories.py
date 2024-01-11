import datetime
import itertools
import random

import factory
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from api import models
from users.factories import UserFactory

from .utils.addresses import addresses
from .utils.areas import area_manager
from .utils.iterators import RandomCategoryIterator, RandomChoiceIterator


def decreasing_n_choice(n):
    """Choose a number between 0 and n, with decreasing chance"""
    choices = range(0, n + 1)
    weights = [1 * (0.6**i) for i in choices]
    return random.choices(choices, weights)[0]  # nosec B311


def australian_phone_number():
    while True:
        area_code = random.choice([2, 3, 4, 7, 8])  # nosec B311
        end_digits = "".join(map(str, random.choices(range(10), k=8)))  # nosec B311
        yield f"0{area_code}{end_digits}"


class AreaFactory(DjangoModelFactory):
    name: Faker = Faker("city", locale="en_AU")
    state: Faker = Faker("state_abbr", locale="en_AU")

    class Meta:
        model = models.Area
        django_get_or_create = ("name", "state")


class BusinessFactory(DjangoModelFactory):
    name: Faker = Faker("company")
    address: factory.Iterator = factory.Iterator(addresses)
    phone: factory.Iterator = factory.Iterator(australian_phone_number(), cycle=False)
    # phone = Faker("phone_number", locale="en_AU")
    email: Faker = Faker("email")
    contact: factory.SubFactory = factory.SubFactory(UserFactory)

    @factory.lazy_attribute
    def area(self):
        area_dict = area_manager.find_area_for_address(self.address)
        return AreaFactory(**area_dict)

    class Meta:
        model = models.Business


class JobListingFactory(DjangoModelFactory):
    business: factory.SubFactory = factory.SubFactory(BusinessFactory)
    title: Faker = Faker("job")
    category: factory.Iterator = factory.Iterator(RandomCategoryIterator)
    description = Faker("paragraph", nb_sentences=10, variable_nb_sentences=True)
    position_type: factory.Iterator = factory.Iterator(["P", "C", "S"])
    contact_name: Faker = Faker("name")
    contact_email: Faker = Faker("email")
    contact_phone: factory.Iterator = factory.Iterator(
        australian_phone_number(), cycle=False
    )
    listing_expiry = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
        weeks=8
    )

    @post_generation
    def certificates_required(obj, create, extracted, **_):
        if not create:  # pragma: no cover
            return
        if extracted:  # pragma: no cover
            for certs in extracted:
                obj.certificates_required.add(certs)  # pylint: disable=no-member
            return
        num_certificates = decreasing_n_choice(3)
        obj.certificates_required.set(  # pylint: disable=no-member
            itertools.islice(
                RandomChoiceIterator(
                    models.Certificate.objects.filter(state=obj.business.area.state).all
                ),
                num_certificates,
            )
        )

    class Meta:
        model = models.JobListing


class JobApplicationFactory(DjangoModelFactory):
    first_name: Faker = Faker("first_name")
    last_name: Faker = Faker("last_name")
    mobile: Faker = factory.Iterator(australian_phone_number(), cycle=False)
    job_listing: factory.SubFactory = factory.SubFactory(JobListingFactory)
    experience: Faker = Faker("paragraph", nb_sentences=5)

    class Meta:
        model = models.JobApplication
