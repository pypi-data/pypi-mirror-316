<h1 align="center">Formatted Join ✅</h1>

<h3 align="center">Effortlessly join string sequences with flexible separator formatting for clear, polished output</h3>

<br/>

<p align="center">
<a href="https://raw.githubusercontent.com/sashsinha/formatted-join/main/LICENCE"><img alt="License: MIT" src="https://raw.githubusercontent.com/sashsinha/formatted-join/main/license.svg"></a>
<a href="https://pypi.org/project/formatted-join/"><img alt="PyPI" src="https://img.shields.io/pypi/v/formatted-join"></a>
<a href="https://pypi.org/project/formatted-join/"><img alt="PyPI Status" src="https://img.shields.io/pypi/status/formatted-join"></a>
<a href="https://pepy.tech/project/formatted-join"><img alt="Downloads" src="https://pepy.tech/badge/formatted-join"></a>
</p>

### Installation

#### PyPI
```
pip install formatted-join
```

#### [`uv`](https://github.com/astral-sh/uv)
```
uv add formatted-join
```

### Usage Examples

#### `formatted_join(items: Sequence[str], separator=', ', final_separator=' and ', use_penultimate_separator=True) -> str`
Joins items with flexible separator configuraton.
```py
>>> from formatted_join import formatted_join
>>> formatted_join(['Hello', 'World'])
'Hello and World'
>>> formatted_join(('A', 'B', 'C'))
'A, B, and C'
>>> formatted_join(['X', 'Y', 'Z', 'W'], separator=' | ', final_separator=' & ')
'X | Y | Z & W'
>>> formatted_join(['Solo'])
'Solo'
>>> formatted_join(['', ''])
' and '
>>> formatted_join(
...     items=['Alpha', 'Bravo', 'Charlie', 'Delta'],
...     separator=' | ',
...     final_separator=' & ',
...     use_penultimate_separator=False
... )
'Alpha | Bravo | Charlie & Delta'
>>> formatted_join(['One', 'Two'], final_separator=' ~ ')
'One ~ Two'
```

---

#### `formatted_join_conjunction(items: Sequence[str], language: str = 'en') -> str`
Joins items using a comma and localized* “and” before the last item.
```py
>>> from formatted_join import formatted_join_conjunction
>>> formatted_join_conjunction(['Spring', 'Summer'])
'Spring and Summer'
>>> formatted_join_conjunction(['One', 'Two', 'Three'])
'One, Two, and Three'
>>> formatted_join_conjunction(['Motorcycle', 'Bus', 'Car'], language='en')
'Motorcycle, Bus, and Car'
>>> formatted_join_conjunction(['Motorcycle', 'Bus', 'Car'], language='de')
'Motorcycle, Bus und Car'
```

---

#### `formatted_join_disjunction(items: Sequence[str], language: str = 'en') -> str`
Joins items using a comma and localized* “or” before the last item.
```py
>>> from formatted_join import formatted_join_disjunction
>>> formatted_join_disjunction(['Monday', 'Tuesday'])
'Monday or Tuesday'
>>> formatted_join_disjunction(['X', 'Y', 'Z'])
'X, Y, or Z'
>>> formatted_join_disjunction(['Motorcycle', 'Bus', 'Car'], language='en')
'Motorcycle, Bus, or Car'
>>> formatted_join_disjunction(['Motorcycle', 'Bus', 'Car'], language='de')
'Motorcycle, Bus oder Car'
```

---

#### `formatted_join_unit(items: Sequence[str]) -> str`
Joins items with commas only (no distinct final separator).
```py
>>> from formatted_join import formatted_join_unit
>>> formatted_join_unit(['A'])
'A'
>>> formatted_join_unit(['A', 'B', 'C', 'D'])
'A, B, C, D'
```

---

#### `formatted_join_narrow(items: Sequence[str]) -> str`
Joins items with a single space separating each.
```py
>>> from formatted_join import formatted_join_narrow
>>> formatted_join_narrow(['Only'])
'Only'
>>> formatted_join_narrow(['A', 'B', 'C'])
'A B C'
>>> formatted_join_narrow(['Line1', '-', 'Line2'])
'Line1 - Line2'
```

---- 

#### * Supported languages for `formatted_join_[conjunction|disjunction]`:

| language | and | or   | separator | has penultimate separator |
| -------- | --- | ---- | --------- | ------------------------- |
| en       | and | or   | `', '`    | yes                       |
| de       | und | oder | `', '`    | no                        |

### Development
- Install Dependencies:
  - `uv sync && uv pip install -r pyproject.toml --extra dev`
- Run formater:
  - `uv run ruff check --select I --fix && uv run ruff format`
- Run type checking:
  - `uv run mypy .`
- Run unit tests:
  - `uv run formatted_join_test.py`
