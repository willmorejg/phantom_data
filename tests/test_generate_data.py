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
"""Unit tests for the DataGenerator class in the generate_data module."""

from pathlib import Path
from uuid import uuid4

import pytest
import polars as pl
from mimesis import Generic

from mods import DataGenerator, DataModelInterface, PersonDataGenerator
from mods.address_data_generator import AddressDataGenerator


class OrderRecord(DataModelInterface):
    """Test model used to verify interface-based data generation."""

    order_id: str
    city: str

    @classmethod
    def generate_data(cls, fake: Generic) -> "OrderRecord":
        """Populate the model with fake data."""
        return cls(order_id=str(uuid4()), city=fake.address.city())


@pytest.fixture(name="data_generator")
def data_generator_fixture():
    """Fixture to create a DataGenerator instance."""
    return DataGenerator()


def test_generate_data(
    data_generator: DataGenerator,
):  # pylint: disable=redefined-outer-name
    """Test the generate_data method of DataGenerator."""
    num_records = 10
    df = data_generator.generate_data(num_records=num_records)
    assert len(df) == num_records
    assert all(isinstance(record, PersonDataGenerator) for record in df)
    model_list = [record.model() for record in df]
    assert all(isinstance(model, dict) for model in model_list)


def test_generate_data_model_list(
    data_generator: DataGenerator,
):  # pylint: disable=redefined-outer-name
    """Test the generate_data_model_list method of DataGenerator."""
    num_records = 10
    df = data_generator.generate_data_model_list(num_records=num_records)
    assert len(df) == num_records
    assert all(isinstance(record, dict) for record in df)


def test_generate_dataframe(
    data_generator: DataGenerator,
):  # pylint: disable=redefined-outer-name
    """Test the generate_dataframe method of DataGenerator."""
    num_records = 10
    df = data_generator.generate_dataframe(num_records=num_records)
    assert df.shape == (num_records, len(PersonDataGenerator.fields()))
    assert set(df.columns) == set(PersonDataGenerator.fields())


def test_generate_csv(
    data_generator: DataGenerator, tmp_path: Path = Path("./tests/output")
):  # pylint: disable=redefined-outer-name
    """Test the generate_csv method of DataGenerator."""

    num_records = 100
    file_path = tmp_path / "test_fake_data.csv"
    data_generator.generate_csv(num_records=num_records, file_path=str(file_path))
    assert file_path.exists()
    df = pl.read_csv(file_path)
    assert df.shape == (num_records, len(PersonDataGenerator.fields()))
    assert set(df.columns) == set(PersonDataGenerator.fields())


def test_generate_address_csv(
    data_generator: DataGenerator, tmp_path: Path = Path("./tests/output")
):  # pylint: disable=redefined-outer-name
    """Test the generate_csv method of DataGenerator for AddressDataGenerator."""

    num_records = 100
    file_path = tmp_path / "test_fake_addr_data.csv"
    data_generator.generate_csv(
        model_class=AddressDataGenerator,
        num_records=num_records,
        file_path=str(file_path),
    )
    assert file_path.exists()
    df = pl.read_csv(file_path)
    assert df.shape == (num_records, len(AddressDataGenerator.fields()))
    assert set(df.columns) == set(AddressDataGenerator.fields())


def test_generate_data_accepts_any_data_model_interface(
    data_generator: DataGenerator,
) -> None:
    """Test that DataGenerator can use any compatible data model."""
    num_records = 500_000

    df = data_generator.generate_dataframe(
        model_class=OrderRecord, num_records=num_records
    )

    assert df.shape == (num_records, len(OrderRecord.fields()))
    assert set(df.columns) == set(OrderRecord.fields())

    file_path = Path("./tests/output/order_records.csv")
    data_generator.generate_csv(
        model_class=OrderRecord,
        num_records=num_records,
        file_path=str(file_path),
    )

    assert file_path.exists()
    df = pl.read_csv(file_path)
    assert df.shape == (num_records, len(OrderRecord.fields()))
    assert set(df.columns) == set(OrderRecord.fields())

    # added for coverage completeness - verify that the file was created and has the expected number of lines
    file_path = Path.cwd() / "fake_data.csv"
    if file_path.exists():
        file_path.unlink()

    data_generator.generate_csv(
        model_class=OrderRecord,
        num_records=10,
    )
    try:
        assert file_path.exists()
        df = pl.read_csv(file_path)
        assert df.shape == (10, len(OrderRecord.fields()))
        assert set(df.columns) == set(OrderRecord.fields())
    finally:
        if file_path.exists():
            file_path.unlink()  # Clean up the generated file after the test
