from faker import Faker


class UserDataGenerator:
    def __init__(self, **kwargs):
        self.fake = Faker()
        self.data = {
            "id": kwargs.get("id", self.fake.uuid4()) if kwargs.get("id") is not "" else "",
            "name": kwargs.get("name") or self.fake.first_name() if kwargs.get("name") is not "" else "",
            "surname": kwargs.get("surname") or self.fake.last_name() if kwargs.get("surname") is not "" else "",
            "phone": kwargs.get("phone") or self.fake.phone_number() if kwargs.get("phone") is not "" else "",
            "age": kwargs.get("age") or self.fake.random_int(min=18, max=65) if kwargs.get("age") is not "" else ""
        }
        for key in kwargs.get("fields_to_exclude", []):
            if key in self.data:
                del self.data[key]
