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
"""Data generator for the Person model."""

from mimesis import Gender, Generic

from .generate_model_interface import DataModelInterface
from .person_model import Person


class PersonDataGenerator(Person, DataModelInterface):
    """Generates fake :class:`Person` records.

    This class mixes the core :class:`Person` data model with the
    :class:`DataModelInterface` contract so that it can act both as a
    concrete person entity and as a factory for producing synthetic data.

    Inheritance from :class:`Person` provides the underlying fields and
    validation for a single person record. Inheritance from
    :class:`DataModelInterface` defines the API (for example, the
    :meth:`generate_data` class method) that all data generators in this
    module are expected to implement.

    Keeping data generation in this separate subclass preserves a clear
    separation of concerns: :class:`Person` remains a plain data model that
    can be used without any dependency on fake data utilities, while
    :class:`PersonDataGenerator` is responsible for creating realistic test
    or seed data for that model.
    """

    @classmethod
    def generate_data(cls, fake: Generic) -> "PersonDataGenerator":
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
