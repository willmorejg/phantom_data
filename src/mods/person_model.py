# Copyright 2026 James G Willmore
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A Person model class."""

from mimesis import Generic, Gender
from .generate_model_interface import DataModelInterface


class Person(DataModelInterface):
    """A simple Person model class."""

    name: str
    gender: Gender
    address: str
    birthday: str
    email: str
    password: str

    @classmethod
    def generate_data(cls, fake: Generic) -> "Person":
        """Populate the Person model with fake data."""
        gender: Gender = Gender(fake.choice([Gender.MALE.value, Gender.FEMALE.value]))

        return cls(
            name=fake.person.full_name(gender=gender),
            gender=gender,
            address=fake.address.address(),
            birthday=fake.person.birthdate().isoformat(),
            email=fake.person.email(),
            password=fake.person.password(),
        )
