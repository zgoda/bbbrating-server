import factory
from factory.base import Factory, FactoryOptions, OptionDefault

from bbbr.models import User, db

DEFAULT_PASSWORD = 'pass'


class PeeweeOptions(FactoryOptions):

    def _build_default_options(self):
        return super()._build_default_options() + [
            OptionDefault('database', None, inherit=True),
        ]


class PeeweeModelFactory(Factory):

    _options_class = PeeweeOptions

    class Meta:
        abstract = True

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        return target_class.create(**kwargs)


class UserFactory(PeeweeModelFactory):

    class Meta:
        model = User
        database = db

    email = factory.Faker('email')
    name = factory.Sequence(lambda n: f'user {n}')
    password = DEFAULT_PASSWORD
    is_active = True
