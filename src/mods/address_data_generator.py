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
"""Data generator for the Address model."""

from .generate_model_interface import DataModelInterface
from .address_model import Address


class AddressDataGenerator(Address, DataModelInterface):
    """Generates fake :class:`Address` records.

    This class mixes the core :class:`Address` data model with the
    :class:`DataModelInterface` contract so that it can act both as a
    concrete address entity and as a factory for producing synthetic data.

    Inheritance from :class:`Address` provides the underlying fields and
    validation for a single address record. Inheritance from
    :class:`DataModelInterface` defines the API (for example, the
    :meth:`generate_data` class method) that all data generators in this
    module are expected to implement.

    Keeping data generation in this separate subclass preserves a clear
    separation of concerns: :class:`Address` remains a plain data model that
    can be used without any dependency on fake data utilities, while
    :class:`AddressDataGenerator` is responsible for creating realistic test
    or seed data for that model.
    """

    @classmethod
    def generate_data(cls, fake) -> "AddressDataGenerator":
        """Populate the Address model with fake data."""
        address_line_1 = f"{fake.address.street_number()} {fake.address.street_name()} {fake.address.street_suffix()}"
        address_line_2 = (
            fake.address.secondary_address()
            if fake.random.random()
            < 0.2  # 20% chance of having a secondary address line
            else ""
        )
        zip_code_plus4 = (
            str(fake.numeric.integer_number(start=1, end=9999)).zfill(4)
            if fake.random.random() < 0.8  # 80% chance of having a ZIP+4
            else ""
        )
        return cls(
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=fake.address.city(),
            state=fake.address.state(abbr=True),
            zip_code=fake.address.zip_code(),
            zip_code_plus4=zip_code_plus4,
        )
