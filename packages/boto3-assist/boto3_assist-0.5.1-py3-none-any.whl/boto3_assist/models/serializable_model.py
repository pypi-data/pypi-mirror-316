"""
Geek Cafe, LLC
Maintainers: Eric Wilson
MIT License.  See Project Root for the license information.
"""

from __future__ import annotations
from typing import TypeVar
from boto3_assist.utilities.serialization_utility import Serialization


class SerializableModel:
    """Library to Serialize object to a DynamoDB Format"""

    T = TypeVar("T", bound="SerializableModel")

    @staticmethod
    def map(source: dict | object, target: T, coerce: bool = True) -> T:
        """
        Map the source dictionary to the target object.

        Args:
        - source: The dictionary to map from.
        - target: The object to map to.
        """
        mapped = Serialization.map(source, target, coerce=coerce)
        if mapped is None:
            raise ValueError("Unable to map source to target")

        return mapped
