from factory.django import DjangoModelFactory
from faker import Faker

from apps.users.models import User

faker = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = faker.unique.email()
    password = faker.password()

    created_at = faker.past_datetime()
    updated_at = faker.future_datetime()
    first_name = faker.first_name()
    last_name = faker.last_name()
