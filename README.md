# prime_factors

Made with python version 3.14

Lint used: Pylint
Formatter: Black Formatter

installation: `pip install -r requirements.txt`

App can be run with: `python prime_factors.py`
Tests with: `pytest -v`

App takes a number as input, finds its unique prime factors, and outputs them to both into the terminal and a text file.
It also use an SQLite3 database, creating it if necessary and retrieves previously computed factors if needed. (app doesn't compute prime factors if found)
