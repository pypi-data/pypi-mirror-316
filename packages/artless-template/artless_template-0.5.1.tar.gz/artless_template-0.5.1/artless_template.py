"""The artless and small template library for server-side rendering."""

__author__ = "Peter Bro"
__version__ = "0.5.1"
__license__ = "MIT"
__all__ = ["Component", "Tag", "Template", "aread_template", "read_template"]

from asyncio import to_thread
from functools import lru_cache
from pathlib import Path
from re import compile, escape
from typing import ClassVar, Mapping, Optional, Protocol, runtime_checkable

# Void tags (https://developer.mozilla.org/en-US/docs/Glossary/Void_element),
# without closing scope.
_VOID_TAGS: Mapping[str, bool] = {
    "area": True,
    "base": True,
    "br": True,
    "col": True,
    "embed": True,
    "hr": True,
    "img": True,
    "input": True,
    "link": True,
    "meta": True,
    "source": True,
    "track": True,
    "wbr": True,
}


@runtime_checkable
class Component(Protocol):
    def view(self) -> "Tag": ...


def _read_file_raw(filename: str | Path, /) -> str:
    return open(filename, "r").read()


class Tag:
    __slots__ = ("attrs", "children", "name", "parent", "text")

    def __init__(self, name: str, /, *args) -> None:
        self.name = name.lower()
        self.attrs, self.children, self.text = self._unpack_args(*args)

        self.parent: Optional["Tag"] = None

        for child in self.children:
            if not isinstance(child, self.__class__):
                raise ValueError(f"Child {child} is not a Tag instance!")
            child.parent = self

    def __str__(self) -> str:
        tag = f"<{self.name}"

        for name, value in self.attrs.items():
            tag += f' {name}="{value}"'

        if self.name in _VOID_TAGS:
            tag += " />"
            return tag

        tag += ">"

        for child in self.children:
            tag += str(child)

        tag += f"{self.text}</{self.name}>"

        return tag

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name!r}>"

    @property
    def is_parent(self) -> bool:
        return bool(self.children)

    @property
    def is_leaf(self) -> bool:
        return not bool(self.children)

    def add_child(self, tag: "Tag", /) -> "Tag":
        tag.parent = self
        self.children.append(tag)
        return self

    @staticmethod
    def _unpack_args(*args) -> tuple[Mapping[str, str], list["Tag"], str]:
        if not args:
            return ({}, [], "")

        if len(args) > 3:
            raise ValueError("Too many arguments in constructor!")

        _kwargs = {}

        for _ in range(len(args)):
            value = args[_]

            if not value:
                continue

            if isinstance(value, Mapping):
                name = "attrs"
            elif isinstance(value, (list, tuple)):
                name = "children"
            elif isinstance(value, str):
                name = "text"
            else:
                raise ValueError(f"Invalid type: {type(value)}!")

            _kwargs[name] = value

        return (_kwargs.get("attrs", {}), _kwargs.get("children", []), _kwargs.get("text", ""))


class Template:
    __slots__ = ("content", "name")

    DELIMITER: ClassVar[str] = "@"

    def __init__(self, /, *, name: str | Path, content: str) -> None:
        self.name = name
        self.content = content

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name!r}>"

    def render(self, **context) -> str:
        if not context:
            return self.content

        context = {
            f"{self.DELIMITER}{key}": str(value.view() if isinstance(value, Component) else value)
            for key, value in context.items()
        }
        context_sorted = sorted(context, key=len, reverse=True)
        context_escaped = map(escape, context_sorted)
        replacement_rx = compile("|".join(context_escaped))

        return replacement_rx.sub(lambda match: context[match.group(0)], self.content)


@lru_cache()
def read_template(filename: str | Path, /) -> Template:
    return Template(name=filename, content=_read_file_raw(filename))


async def aread_template(filename: str | Path, /) -> Template:
    return Template(name=filename, content=await to_thread(_read_file_raw, filename))
