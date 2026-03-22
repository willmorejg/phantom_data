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
"""Module for generating fake data."""

from pathlib import Path

import polars as pl
from mimesis import Generic
from mimesis.locales import Locale

from .generate_model_interface import DataModelInterface
from .person_data_generator import PersonDataGenerator


class DataGenerator:
    """Class for generating fake data."""

    def __init__(self):
        """Initialize the DataGenerator."""
        self.fake = Generic(Locale.EN)
        self.working_path = Path.cwd()

    def generate_data(
        self,
        model_class: type[DataModelInterface] = PersonDataGenerator,
        num_records: int = 1000,
    ) -> list[DataModelInterface]:
        """Generate a list of data model instances with fake data.

        Args:
            model_class: The data model class to generate instances of.
            num_records: The number of records to generate.

        Returns:
            A list of DataModelInterface instances populated with fake data.
        """
        return [model_class.generate_data(self.fake) for _ in range(num_records)]

    def generate_dataframe(
        self,
        model_class: type[DataModelInterface] = PersonDataGenerator,
        num_records: int = 1000,
    ) -> pl.DataFrame:
        """Generate a Polars DataFrame with fake data."""
        data = self.generate_data(model_class, num_records)
        return pl.DataFrame([d.model_dump(mode="json") for d in data])

    def generate_csv(
        self,
        model_class: type[DataModelInterface] = PersonDataGenerator,
        num_records: int = 1000,
        file_path: str = "",
    ) -> None:
        """Generate a CSV file with fake data."""
        if not file_path:
            file_path = str(self.working_path / "fake_data.csv")
        df: pl.DataFrame = self.generate_dataframe(model_class, num_records)
        df.write_csv(file_path)
