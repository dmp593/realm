from decimal import Decimal, InvalidOperation
from typing import Optional


def str2decimal(raw_value: str, raise_exception: bool = False, default: Optional[Decimal] = None) -> Optional[Decimal]:
    """
    Convert a string to a Decimal.

    Args:
        raw_value (str): The string to convert.
        raise_exception (bool): Whether to raise an exception on failure.
        default (Optional[Decimal]): The default value to return if conversion fails and raise_exception is False.

    Returns:
        Optional[Decimal]: The converted decimal value, or the default value if conversion fails and raise_exception is False.
    """
    try:
        return Decimal(raw_value)
    except (InvalidOperation, TypeError, ValueError) as e:
        if raise_exception:
            raise e
        return default
