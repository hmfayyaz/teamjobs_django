import factory
import pytest
from pytest_factoryboy import register

from api import factories, models
from api.factories.utils import joblistings
from api.factories.utils.iterators import RandomChoiceIterator

# register(factories.AreaFactory)
register(factories.BusinessFactory)
register(factories.JobListingFactory)
register(factories.JobApplicationFactory)


# register(factories.JobApplicationExistingListingFactory)


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        joblistings.JobListingsManager.populate_categories()
        joblistings.JobListingsManager.populate_certificates()
        areas = factories.AreaFactory.create_batch(size=10)
        businesses = factories.BusinessFactory.create_batch(
            size=20, area=factory.Iterator(RandomChoiceIterator(areas))
        )
        factories.JobListingFactory.create_batch(
            size=100, business=factory.Iterator(RandomChoiceIterator(businesses))
        )


@pytest.fixture(scope="session")
def areas():
    yield models.Area.objects.all()


@pytest.fixture
def random_areas(areas):
    yield RandomChoiceIterator(areas)


@pytest.fixture
def area(random_areas):
    yield next(random_areas)


@pytest.fixture(scope="session")
def businesses():
    yield models.Business.objects.all()


@pytest.fixture(scope="session")
def job_listings(businesses):
    yield models.JobListing.objects.all()


@pytest.fixture(scope="session")
def categories():
    return models.Category.objects.all()


@pytest.fixture(scope="session")
def random_categories(categories):
    return RandomChoiceIterator(categories)


@pytest.fixture
def category_instance(random_categories):
    return next(random_categories)


@pytest.fixture(scope="session")
def certificates():
    return models.Certificate.objects.all()


@pytest.fixture(scope="session")
def random_certificates(certificates):
    return RandomChoiceIterator(certificates)


@pytest.fixture
def certificate_instance(random_certificates):
    return next(random_certificates)
