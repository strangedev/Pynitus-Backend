"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Noah Hummel

    This file is part of the Pynitus program, see <https://github.com/strangedev/Pynitus>.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Any, Callable, Dict

from Pynitus.Pynitus.util.lists import justList, apply
from Pynitus.Pynitus.util.extended_typing import Maybe, One

from Pynitus.Pynitus.util import tag_support


def __sanitizeString(tag_name: str, string: str) -> Maybe(str):
    if string in tag_support.EMPTY_SYNONYMS:
        return None
    return string


__SANITIZATION_METHODS__ = {
    str: __sanitizeString
}  # type: Dict[type, Callable[[str, One], Maybe(One)]]


def __getSanitizationMethod(tag_type: type) -> Callable[[str, One], Maybe(One)]:
    if tag_type not in __SANITIZATION_METHODS__:
        return lambda t, v: v

    return __SANITIZATION_METHODS__[tag_type]


def __naiveTypeCast(tag_name: str, tag_value: Any) -> tag_support.TagValue:
    primitive_type = tag_support.getPrimitiveType(tag_name)

    try:
        tag_value = primitive_type(tag_value)
    except Exception as e:
        print(e)  # TODO: log
        tag_value = None

    return tag_value


def __convertTagType(tag_name: str, tag_value: Any) -> tag_support.TagValue:

    if tag_support.isListType(tag_name):  # Should this attribute be represented as a list?

        if type(tag_value) is not list:
            tag_value = [tag_value]

        tag_value = justList([__naiveTypeCast(tag_name, v) for v in tag_value])

    else:  # attribute shouldn't be a list.
        if type(tag_value) is list:  # if it's a list though (taglib does this...)...
            if len(tag_value) > 0:  # ... then maybe the first element is usable.
                tag_value = tag_value[0]

        tag_value = __naiveTypeCast(tag_name, tag_value)

    return tag_value


def __sanitizeTagValue(tag_name: str, tag_value: Any) -> tag_support.TagValue:
    sanitization_method = __getSanitizationMethod(tag_support.getPrimitiveType(tag_name))

    def bound_sanitization_method(v: Any) -> Callable[[One], Maybe(One)]:
        return sanitization_method(tag_name, v)

    sanitized_value = apply(bound_sanitization_method, tag_value)

    if type(sanitized_value) is list:
        sanitized_value = justList(sanitized_value)

    return sanitized_value


def __sanitizeTagName(tag_name: str) -> str:
    if tag_name not in tag_support.INTERNAL_NAMES:
        return tag_support.getInternalName(tag_name)
    return tag_name


def sanitizeTag(tag_name: str, tag_value: Any) -> tag_support.TagValue:
    """
    Performs strong type checking and basic sanitization on a tag value.
    Tries to cast and/or convert the value's type to the required type according to TagSupport.
    If the type check fails and the type can't be converted, the value is emptied,
    this means it is set to either None or [], depending on whether the required
    type is a list type or a primitive type.

    After a successful type check, the value is sanitized.

    :param tag_name: The internal name or TagLib identifier of the tag
    :param tag_value: The tag's value
    :return: The sanitized and type checked tag value
    """

    return __sanitizeTagValue(tag_name, __convertTagType(tag_name, tag_value))


def sanitizeTags(tags: Dict[str, Any]) -> Dict[str, tag_support.TagValue]:
    """
    Performs strong type checking and basic sanitization on a complete dict of tag values.
    Tries to cast and/or convert the value types to the required types according to TagSupport.
    If the type check fails and the type can't be converted, the value is emptied,
    this means it is set to either None or [], depending on whether the required
    type is a list type or a primitive type.

    After a successful type check, the value is sanitized.

    :param tags A dict containing internal names or taglib ids and associated tag values
    :return: The sanitized and type checked tag value dict
    """

    tags = {__sanitizeTagName(k): v for k, v in tags.items() if tag_support.isSupported(k)}
    tags = {k: tags.get(k) for k in tag_support.INTERNAL_NAMES}

    return {k: __sanitizeTagValue(k, __convertTagType(k, v)) for k, v in tags.items()}
