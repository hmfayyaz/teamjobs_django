# Setting up development environment

## Dependencies

### Python

Ensure you have [Python 3.11+](https://www.python.org/downloads/) installed.

### Python Tools

This is used to install some tools in isolated environments

```
$ pip install --user pipx
$ pipx install poetry tox pre-commit
```

## Poetry virtualenv

[Poetry](https://python-poetry.org/) is used to manage dependencies in pyproject.toml

`$ poetry install`

To add a new run time dependency

`$ poetry add some-python-package`

To add a new development dependency

`$ poetry add --group=dev some-dev-python-package`

To update dependencies (within version limits)

`$ poetry update`

## Install pre-commit hooks

We use [pre-commit](https://pre-commit.com/) to ensure all commits meet certain standards. Install the hooks by running

`$ pre-commit install --install-hooks`

You can run pre-commit against all files by running

`$ pre-commit run --all-files`

While running prior to commit, it's normal for the commit to fail if pre-commit modified some files (e.g. with the
black, or isort hooks). Re-stage any files if necessary (see `git status`, and use `git add` where appropriate), the
retry the commit.

## Testing

### Tox

This project uses [tox](https://tox.wiki/en/latest/index.html) and
[pytest](https://docs.pytest.org/en/7.2.x/).

Tests should be run before any pull request, and a bare minimum is writing enough for 100%
code coverage.

There are three tox environments defined, by default running tox with`tox` on the command
line will run all of them.

You can also run a single environment by using `tox -e environment_name`

The environments are:

| environment name | description                             |
|------------------|-----------------------------------------|
| py311            | runs pytest with python 3.11            |
| flake8           | runs flake8 linter over the code base   |
| black            | runs black in check mode, showing diffs |

And at the end of the pytest run you'll be given a coverage report such as this

```
---------- coverage: platform win32, python 3.11.2-final-0 -----------
Name           Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------
api\views.py      26      1      4      1    93%   31
----------------------------------------------------------
TOTAL            314      1     18      1    99%

```

The missing column tells you what exact lines are missing coverage in each file. There's also a browsable html version
in `htmlcov/index.html` as well.

### pytest plugins

We currently use these pytest plugins, many of which offer fixtures or integrations to make life easier.

- [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)
- [pytest-django](https://pytest-django.readthedocs.io/en/latest/)
- [pytest-env](https://github.com/pytest-dev/pytest-env)
- [pytest-factoryboy](https://pytest-factoryboy.readthedocs.io/en/stable/)

### Other testing tools

Other testing related packages, linters in use:

- [factoryboy](https://factoryboy.readthedocs.io/en/stable/index.html)
- [faker](https://faker.readthedocs.io/en/master/)
- [flake8](https://flake8.pycqa.org/en/latest/)
- [hypothesis](https://hypothesis.readthedocs.io/en/latest/)
- [pylint](https://pylint.readthedocs.io/en/latest/index.html)
