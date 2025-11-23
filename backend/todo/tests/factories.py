# todo/tests/factories.py
import factory
from django.contrib.auth import get_user_model
from todo.models import Todo

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "password")


class TodoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Todo

    owner = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence")
