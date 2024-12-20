from typing import Any, Dict, Set, Literal, Iterable, Mapping, Union

mappables: Set[Mapping] = {dict}
iterables: Set[Iterable] = {list}

key_style: Literal["python", "js"] = "python"


def _string_key(k: Union[str, int]) -> str:
    global key_style
    if key_style == "python":
        return f"['{k}']"
    elif key_style == "js":
        return f".{k}"


def flatten(it: Union[Iterable, Mapping] = None) -> Dict:

    global mappables, iterables

    _mappables = tuple(mappables)
    _iterables = tuple(iterables)
    seen = list()
    ot = dict()

    if isinstance(it, _mappables):
        stack = list((_string_key(k), v) if isinstance(k, str) else (f"[{k}]", v) for k, v in it.items())[::-1]
    elif isinstance(it, _iterables):
        stack = list((f"[{k}]", v) for k, v in enumerate(it))[::-1]

    while stack:
        path, value = stack.pop()
        for ref in seen:
            if value is ref:
                raise ValueError("Circular reference detected")
        if isinstance(value, _mappables):
            seen.append(value)
            if len(value) == 0:
                ot[path] = value
            stack = (
                stack
                + list(
                    (f"{path}{_string_key(k)}", v) if isinstance(k, str) else (f"{path}[{k}]", v)
                    for k, v in value.items()
                )[::-1]
            )
        elif isinstance(value, _iterables):
            seen.append(value)
            if len(value) == 0:
                ot[path] = value
            else:
                stack = stack + list((f"{path}[{k}]", v) for k, v in enumerate(value))[::-1]
        else:
            ot[path] = value
    return ot
