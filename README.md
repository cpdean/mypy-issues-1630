this demonstrates a bug where mypy will crash when someone incorrectly documents a function that is closed over by a function that
is used in a monkey patch

the expected behavior would be an error informing the user of what they've done wrong, or at least that a given function
is not documented right, rather than a hard crash of mypy

Running the test case:

```
mkvirtualenv testcase -p `which python3`
pip install -r requirements.txt
mypy --fast-parser --silent-imports --py2 --check-untyped-defs --disallow-untyped-defs testcase.py
```

all the above flags to mypy are required for reproducing the bug, running mypy in a different way will
not reproduce the bug
