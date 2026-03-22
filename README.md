# phantom_data

A lightweight Python library for generating synthetic fake data, built on [Mimesis](https://mimesis.name/) and [Polars](https://pola.rs/). Define custom data models and export thousands of records to DataFrames or CSV files.

## Features

- **Extensible model interface** — define any data shape by subclassing `DataModelInterface`
- **Built-in `Person` model** — name, gender, address, birthday, email, password
- **Polars DataFrame output** — fast, memory-efficient columnar data
- **CSV export** — write generated data directly to disk
- **High-volume generation** — tested with 500,000+ records

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd phantom_data

# Install with uv
uv sync

# Or with pip
pip install -e .
```

## Quick Start

```python
from mods import DataGenerator, Person

generator = DataGenerator()

# Generate 1000 Person records as a Polars DataFrame
df = generator.generate_data(model_class=Person, num_records=1000)
print(df)

# Write to CSV
generator.generate_csv(model_class=Person, num_records=1000, file_path="people.csv")
```

## Custom Models

Extend `DataModelInterface` to define your own data shape:

```python
from mimesis import Generic
from mods.generate_model_interface import DataModelInterface


class OrderRecord(DataModelInterface):
    order_id: str
    city: str

    @classmethod
    def generate_data(cls, fake: Generic) -> "OrderRecord":
        return cls(
            order_id=fake.code.issn(),
            city=fake.address.city(),
        )


generator = DataGenerator()
df = generator.generate_data(model_class=OrderRecord, num_records=5000)
```

## API Reference

### `DataGenerator`

| Method | Description |
| --- | --- |
| `generate_data(model_class, num_records)` | Returns a `polars.DataFrame` with `num_records` rows |
| `generate_csv(model_class, num_records, file_path)` | Writes generated data to a CSV file |

Both methods default to `model_class=Person` and `num_records=1000`.

### `DataModelInterface`

Abstract base class (extends `SQLModel`) that all data models must implement.

| Method | Description |
| --- | --- |
| `generate_data(cls, fake)` | Abstract classmethod — populate model fields using a Mimesis `Generic` instance |
| `fields(cls)` | Returns a list of field names for the model |

### `Person`

Built-in model with fields: `name`, `gender`, `address`, `birthday`, `email`, `password`.

## Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src

# Lint and format
ruff check src tests
ruff format src tests
```

## License

[Apache License 2.0](LICENSE)
