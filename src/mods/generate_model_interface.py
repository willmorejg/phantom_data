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
"""Interface for generating fake data models."""

from abc import abstractmethod
from mimesis import Generic
from sqlmodel import SQLModel


class DataModelInterface(SQLModel):
    """Abstract base class for data model interfaces."""

    @classmethod
    @abstractmethod
    def generate_data(cls, fake: Generic) -> "DataModelInterface":
        """Populate the data model with fake data."""

    @classmethod
    def fields(cls) -> list[str]:
        """Convert the data model instance to a list of field names."""
        return list(cls.model_fields.keys())
