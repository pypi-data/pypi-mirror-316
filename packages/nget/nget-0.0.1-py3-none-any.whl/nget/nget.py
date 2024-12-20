from typing import Any, Mapping, Sequence, TypeVar, Union

_T = TypeVar("_T")

_sentinel = object()


def nget(
    structure: Union[Mapping[Any, Any], Sequence[Any]],
    keys: Sequence[Any],
    default: _T = _sentinel,  # type: ignore
) -> Union[Any, _T]:
    """
    Safely retrieving nested values from data structures using a sequence of keys or indexes.

    Args:
        structure (Union[Mapping[Any, Any], Sequence[Any]]): Data structure to get the value from.
        keys (Sequence[Any]): The sequence of keys or indexes to traverse the structure.
        default (Any, optional): The default value to return if the key is not found.

    Returns:
        Any: The value found at the nested location, or the default value if not found.

    Raises:
        KeyError: If a key is not found and no default is provided.
        IndexError: If an index is out of range and no default is provided.
        TypeError: If the structure is not a Mapping or Sequence and no default is provided.
    """
    for key in keys:
        try:
            structure = structure[key]
        except (KeyError, IndexError, TypeError) as ex:
            if default is _sentinel:
                raise ex
            return default
    return structure
