from typing import get_type_hints
from typing import get_origin
from typing import get_args
from typing import Union
from typing import Any

import re
from dataclasses import dataclass


HEX_REGEX = r'^#[0-9a-fA-F]{6}$'


def _is_optional(field_type) -> bool:
    origin = get_origin(field_type)
    if origin is Union:
        return type(None) in get_args(field_type)
    return False


def check_required_fields(instance: dataclass) -> None:
    annotations = get_type_hints(instance.__class__)
    for field_name, field_type in annotations.items():
        if (not _is_optional(field_type)
                and getattr(instance, field_name) is None):
            raise ValueError(f"Field '{field_name}' cannot be None.")


def check_spaces(field_name: str, field_value: Any) -> None:
    if field_value.count(" "):
        raise ValueError(f"{field_name} cannot contain spaces")


def check_hex_color(field_name: str, field_value: Any) -> None:
    if not re.match(HEX_REGEX, str(field_value)):
        raise ValueError(f"{field_name} isn't correct. "
                         "Should follow this format: #FFFFFF "
                         f"Given ({field_value})")
