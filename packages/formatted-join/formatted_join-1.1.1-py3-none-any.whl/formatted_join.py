"""Utility for joining string sequences with flexible separator formatting."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


def _join_two_items(
  items: Sequence[str],
  separator: str,
) -> str:
  """Join exactly two items with a separator.

  Args:
    items: The sequence of strings to join.
    separator: The delimiter between the two elements potentially including a
      trailing space.

  Returns:
    A single string joining both items with the separator.
  """
  first, second = items
  return f'{first}{separator}{second}'


def _join_three_or_more_items(
  items: Sequence[str],
  separator: str,
  final_separator: str,
  use_penultimate_separator: bool,
) -> str:
  """Join a list of more than two items with the specified separators.

  Args:
    items: The sequence of strings to join.
    separator: The standard delimiter for separating elements.
    final_separator: The special delimiter before the last element.
    use_penultimate_separator: Whether to place the standard separator before
      the final_separator.

  Returns:
      A single string joining all items with appropriate separators.
  """
  *all_but_last, last = items
  joined_up_to_penultimate = separator.join(all_but_last)
  if use_penultimate_separator:
    # e.g. 'A, B, C, and D'.
    if (
      separator
      and separator[-1].isspace()
      and final_separator
      and final_separator[0].isspace()
    ):
      return (
        f'{joined_up_to_penultimate}{separator[:-1]}{final_separator}{last}'
      )
    else:
      return f'{joined_up_to_penultimate}{separator}{final_separator}{last}'
  else:
    # e.g. 'A, B, C and D'.
    return f'{joined_up_to_penultimate}{final_separator}{last}'


def formatted_join(
  items: Sequence[str],
  separator: str = ', ',
  final_separator: str = ' and ',
  use_penultimate_separator: bool = True,
) -> str:
  """Joins items into a string with specified separator formatting.

  Args:
    items: The sequence of strings to join.
    separator: The standard delimiter for separating elements. Defaults to ', '.
    final_separator: The special delimiter before the last element. Defaults to
      ' and '.
    use_penultimate_separator: Whether to place the standard separator before
      the final_separator when items length >= 3. Defaults to True.

  Returns:
    A string after joining items with specified separator formatting.
  """
  if not items:
    return ''
  if len(items) == 1:
    return items[0]
  if len(items) == 2:
    return _join_two_items(items, final_separator)
  return _join_three_or_more_items(
    items, separator, final_separator, use_penultimate_separator
  )


@dataclass
class LocalizedConfig:
  separator: str
  final_separator_and: str
  final_separator_or: str
  use_penultimate_separator: bool


_LOCALIZED_CONFIG_BY_LANGUAGE = {
  'en': LocalizedConfig(
    separator=', ',
    final_separator_and=' and ',
    final_separator_or=' or ',
    use_penultimate_separator=True,
  ),
  'de': LocalizedConfig(
    separator=', ',
    final_separator_and=' und ',
    final_separator_or=' oder ',
    use_penultimate_separator=False,
  ),
}


def formatted_join_conjunction(
  items: Sequence[str], language: str = 'en'
) -> str:
  """Joins items with 'and'-based conjunction considering the language."""
  config = _LOCALIZED_CONFIG_BY_LANGUAGE.get(
    language, _LOCALIZED_CONFIG_BY_LANGUAGE['en']
  )
  return formatted_join(
    items,
    separator=config.separator,
    final_separator=config.final_separator_and,
    use_penultimate_separator=config.use_penultimate_separator,
  )


def formatted_join_disjunction(
  items: Sequence[str], language: str = 'en'
) -> str:
  """Joins items with 'or'-based disjunction considering the language."""
  config = _LOCALIZED_CONFIG_BY_LANGUAGE.get(
    language, _LOCALIZED_CONFIG_BY_LANGUAGE['en']
  )
  return formatted_join(
    items,
    separator=config.separator,
    final_separator=config.final_separator_or,
    use_penultimate_separator=config.use_penultimate_separator,
  )


def formatted_join_unit(items: Sequence[str]) -> str:
  """Joins items as a unit formatting i.e., separated by commas."""
  return formatted_join(
    items, separator=', ', final_separator=', ', use_penultimate_separator=False
  )


def formatted_join_narrow(items: Sequence[str]) -> str:
  """Joins items with narrow formatting, i.e., just spaces between them."""
  return ' '.join(items)
