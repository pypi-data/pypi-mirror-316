import unittest
from collections import deque
from collections.abc import Sequence

from formatted_join import (
  formatted_join,
  formatted_join_conjunction,
  formatted_join_disjunction,
  formatted_join_narrow,
  formatted_join_unit,
)


class TestFormattedJoin(unittest.TestCase):
  def test_empty_list(self) -> None:
    self.assertEqual(formatted_join([]), '')

  def test_single_item(self) -> None:
    self.assertEqual(formatted_join(['Hello']), 'Hello')

  def test_two_items_default(self) -> None:
    self.assertEqual(formatted_join(['Hello', 'World']), 'Hello and World')

  def test_two_items_custom_final_separator(self) -> None:
    self.assertEqual(
      formatted_join(['Hello', 'World'], final_separator=' ~ '), 'Hello ~ World'
    )

  def test_three_items_default_behavior(self) -> None:
    self.assertEqual(formatted_join(['A', 'B', 'C']), 'A, B, and C')

  def test_many_items_penultimate_separator_true(self) -> None:
    self.assertEqual(formatted_join(['A', 'B', 'C', 'D']), 'A, B, C, and D')

  def test_no_penultimate_separator(self) -> None:
    result = formatted_join(
      ['A', 'B', 'C', 'D', 'E'],
      separator=' | ',
      final_separator=' & ',
      use_penultimate_separator=False,
    )
    self.assertEqual(result, 'A | B | C | D & E')

  def test_whitespace_boundaries(self) -> None:
    result = formatted_join(
      ['A', 'B', 'C'],
      separator=', ',
      final_separator=' and ',
      use_penultimate_separator=True,
    )
    self.assertEqual(result, 'A, B, and C')

  def test_formatted_join_custom_separators_no_penultimate(self) -> None:
    items = ['Alpha', 'Bravo', 'Charlie', 'Delta']
    result = formatted_join(
      items,
      separator=' <> ',
      final_separator=' + ',
      use_penultimate_separator=False,
    )
    self.assertEqual(result, 'Alpha <> Bravo <> Charlie + Delta')

  def test_formatted_join_empty_string_items(self) -> None:
    result_three_items = formatted_join(['', 'B', 'C'])
    self.assertEqual(result_three_items, ', B, and C')
    result_two_items = formatted_join(['', ''])
    self.assertEqual(result_two_items, ' and ')


class TestConjunction(unittest.TestCase):
  def test_conjunction_three_items_en(self) -> None:
    self.assertEqual(
      formatted_join_conjunction(['One', 'Two', 'Three'], language='en'),
      'One, Two, and Three',
    )

  def test_conjunction_two_items_en(self) -> None:
    self.assertEqual(
      formatted_join_conjunction(['Spring', 'Summer'], language='en'),
      'Spring and Summer',
    )

  def test_conjunction_three_items_de(self) -> None:
    self.assertEqual(
      formatted_join_conjunction(['Eins', 'Zwei', 'Drei'], language='de'),
      'Eins, Zwei und Drei',
    )

  def test_conjunction_two_items_de(self) -> None:
    self.assertEqual(
      formatted_join_conjunction(['Frühling', 'Sommer'], language='de'),
      'Frühling und Sommer',
    )

  def test_conjunction_fallback_language(self) -> None:
    self.assertEqual(
      formatted_join_conjunction(['One', 'Two', 'Three'], language='fr'),
      'One, Two, and Three',  # Defaults to 'en'
    )


class TestDisjunction(unittest.TestCase):
  def test_disjunction_three_items_en(self) -> None:
    self.assertEqual(
      formatted_join_disjunction(['X', 'Y', 'Z'], language='en'), 'X, Y, or Z'
    )

  def test_disjunction_two_items_en(self) -> None:
    self.assertEqual(
      formatted_join_disjunction(['Monday', 'Tuesday'], language='en'),
      'Monday or Tuesday',
    )

  def test_disjunction_three_items_de(self) -> None:
    self.assertEqual(
      formatted_join_disjunction(['Eins', 'Zwei', 'Drei'], language='de'),
      'Eins, Zwei oder Drei',
    )

  def test_disjunction_two_items_de(self) -> None:
    self.assertEqual(
      formatted_join_disjunction(['Montag', 'Dienstag'], language='de'),
      'Montag oder Dienstag',
    )

  def test_disjunction_fallback_language(self) -> None:
    self.assertEqual(
      formatted_join_disjunction(['X', 'Y', 'Z'], language='fr'),
      'X, Y, or Z',  # Defaults to 'en'
    )


class TestFormattedJoinUnit(unittest.TestCase):
  def test_unit_empty(self) -> None:
    self.assertEqual(formatted_join_unit([]), '')

  def test_unit_single_item(self) -> None:
    self.assertEqual(formatted_join_unit(['X']), 'X')

  def test_unit_two_items(self) -> None:
    self.assertEqual(formatted_join_unit(['A', 'B']), 'A, B')

  def test_unit_multiple_items(self) -> None:
    self.assertEqual(formatted_join_unit(['A', 'B', 'C', 'D']), 'A, B, C, D')


class TestFormattedJoinNarrow(unittest.TestCase):
  def test_narrow_empty(self) -> None:
    self.assertEqual(formatted_join_narrow([]), '')

  def test_narrow_single(self) -> None:
    self.assertEqual(formatted_join_narrow(['Only']), 'Only')

  def test_narrow_multiple(self) -> None:
    self.assertEqual(formatted_join_narrow(['A', 'B', 'C']), 'A B C')

  def test_narrow_special_chars(self) -> None:
    self.assertEqual(
      formatted_join_narrow(['Line1', '-', 'Line2']), 'Line1 - Line2'
    )


class TestSequenceVariations(unittest.TestCase):
  def test_list_formatted_join(self) -> None:
    items = ['A', 'B', 'C']
    self.assertEqual(formatted_join(items), 'A, B, and C')

  def test_tuple_conjunction(self) -> None:
    items = ('X', 'Y')
    self.assertEqual(formatted_join_conjunction(items), 'X and Y')

  def test_range_disjunction(self) -> None:
    items = list(map(str, range(3)))
    self.assertEqual(formatted_join_disjunction(items), '0, 1, or 2')

  def test_deque_unit(self) -> None:
    dq = deque(['a', 'b', 'c'])
    self.assertEqual(formatted_join_unit(dq), 'a, b, c')

  def test_custom_sequence_class_narrow(self) -> None:
    class MySequence(Sequence[str]):
      def __init__(self, data):
        self._data = data

      def __getitem__(self, index):
        return self._data[index]

      def __len__(self):
        return len(self._data)

    custom_seq = MySequence(['foo', 'bar', 'baz'])
    self.assertEqual(formatted_join_narrow(custom_seq), 'foo bar baz')


if __name__ == '__main__':
  unittest.main()
