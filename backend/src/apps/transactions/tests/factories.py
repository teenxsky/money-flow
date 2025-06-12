import random
from datetime import datetime, timedelta

import factory
from factory.declarations import LazyAttribute, SubFactory
from faker import Faker

from apps.reference.tests.factories import (
    CategoryFactory,
    StatusFactory,
    SubcategoryFactory,
    TransactionTypeFactory,
)
from apps.transactions.models import Transaction
from apps.users.tests.factories import UserFactory

faker = Faker()


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    user = SubFactory(UserFactory)
    status = SubFactory(StatusFactory)
    transaction_type = SubFactory(TransactionTypeFactory)
    category = SubFactory(CategoryFactory)
    subcategory = SubFactory(SubcategoryFactory)
    amount = LazyAttribute(lambda _: round(random.uniform(10, 10000), 2))
    comment = LazyAttribute(lambda _: faker.text(max_nb_chars=50))
    created_at = LazyAttribute(
        lambda _: datetime.now() - timedelta(days=random.randint(0, 30))
    )
    updated_at = LazyAttribute(
        lambda o: o.created_at + timedelta(hours=random.randint(0, 48))
    )
