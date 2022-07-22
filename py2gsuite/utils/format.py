import pprint
from enum import Enum
from typing import Any, Dict, List, Optional


def class2str(
    obj: object,
    abbreviation: Optional[int] = None,
    format: bool = False,
) -> str:
    """Convert class object to str.

    NOTE:
        Reference is below.
        https://stackoverflow.com/questions/1036409/recursively-convert-python-object-graph-to-dictionary

    Args:
        obj (object): Class object which you want to convert to str.
        abbreviation (Optional[int]): If len(list_object) > abbreviation, abbreviation the result.

    Returns:
        str: str converted from class object.
    """
    return dict2str(class2dict(obj, abbreviation), format=format)


def class2dict(
    obj: object,
    abbreviation: Optional[int] = None,
    class_key: Optional[str] = None,
) -> Dict[str, Any]:
    """[summary]

    Args:
        obj (object): Class object which you want to convert to dict.
        abbreviation (Optional[int]): If len(list_object) > abbreviation, abbreviate the result. Defaults to None.
        class_key (Optional[str]): Class key for dict. Defaults to None.
    """
    if isinstance(obj, dict):
        data: Dict[str, Any] = {}
        for key, item in obj.items():
            data[key] = class2dict(item, abbreviation, class_key)
        return data
    elif isinstance(obj, Enum):
        return str(obj)
    elif hasattr(obj, "_ast"):
        return class2dict(obj._ast(), abbreviation)
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        if abbreviation and len(obj) > abbreviation:
            return f" --- length of element {len(object)} ---,"
        return [class2dict(elem, abbreviation, class_key) for elem in obj]
    elif hasattr(obj, "__dict__"):
        data: Dict[str, Any] = dict(
            [
                (key, class2dict(item, abbreviation, class_key))
                for key, item in obj.__dict__.items()
                if not callable(item) and not key.startswith("_")
            ]
        )
        if class_key is not None and hasattr(obj, "__class__"):
            data[class_key] = obj.__class__.__name__
        return data
    else:
        return obj


def dict2str(dict_obj: Dict[str, Any], format: bool = False) -> str:
    """[str]
    Convert dict object to str.

    Args:
        dict_obj (Dict[str, Any])
        format (bool): Whether format converted str. Defaults to False.

    Returns:
        str_ (str)
    """
    str_: str = pprint.pformat(
        dict_obj,
        indent=1,
        width=120,
        depth=None,
        compact=True,
    )
    if format:
        return "\n" + str_ + "\n"
    return str_


def dict2list(
    dict_obj: Dict[str, Any],
    keys: Optional[List[str]] = None,
) -> List[str]:
    """Convert dict to list of str.

    Args:
        dict_obj (Dict[str, Any])
        keys (Optional[List[str]]): Defaults to None.

    Returns:
        List[str]:
    """
    if keys is not None:
        ret: List[str] = []
        for k in keys:
            ret.append(str(dict_obj[k]))
        return ret

    return list(_get_values(dict_obj))


def _get_values(d: Dict[str, Any]):
    for v in d.values():
        if isinstance(v, dict):
            yield from dict2list(v)
        else:
            yield str(v)
