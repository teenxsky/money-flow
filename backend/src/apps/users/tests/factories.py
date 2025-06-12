from factory.declarations import LazyAttribute
from factory.django import DjangoModelFactory
from faker import Faker

from apps.users.models import User

faker = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = LazyAttribute(lambda o: faker.unique.email())
    password = LazyAttribute(lambda o: faker.password())
    created_at = LazyAttribute(lambda o: faker.past_datetime())
    updated_at = LazyAttribute(lambda o: faker.future_datetime())
    first_name = LazyAttribute(lambda o: faker.first_name())
    last_name = LazyAttribute(lambda o: faker.last_name())
