import factory
from django.contrib.auth import get_user_model
from faker import Faker
from faker.factory import Factory


User = get_user_model()

faker = Factory().create()

faker_instance = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.lazy_attribute(lambda _: faker.email())
    first_name = factory.lazy_attribute(lambda _: faker.first_name())
    last_name = factory.lazy_attribute(lambda _: faker.last_name())
    password = factory.lazy_attribute(lambda _: faker.password())
    username = factory.lazy_attribute(lambda _: faker.first_name())
    is_active = True
    is_superuser = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs and kwargs.get("is_superuser") is True:
            return manager.create_superuser(*args, **kwargs)

        return manager.create_user(*args, **kwargs)
