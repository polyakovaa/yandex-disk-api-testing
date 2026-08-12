import string

from faker import Faker


class RandomUtils:
    _faker = Faker()

    @classmethod
    def generate_string_field(cls, length: int) -> str:
        return "".join(
            cls._faker.random_choices(elements=string.ascii_lowercase, length=length)
        )
