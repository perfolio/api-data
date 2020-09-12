# Contributing to perfolio/data-api

Thanks for considering contributing to a Perfolio Open Source project! All kind of contributions are welcome, but please keep the following guidelines in mind.

## Git workflow

In this repo, we use a master-only workflow.
Please branch from master when implementing features or bug fixes.

### Branching naming convention

All branches must be categorized and prefixed in the following way:

| branch prefix | Purpose                       |
| ------------- | ----------------------------- |
| `feature/`    | A new feature you want to add |
| `fix/`        | Bugfixes                      |
| `docs/`       | All documentation work        |
| `refactor/`   | No new features or bugs       |

## Quickstart

1.  Clone the repository.

        git clone https://github.com/perfolio/data-api.git
        cd data-api

2. Setup venv (optional but recommended).

        python3 -m venv venv
        source venv/bin/activate

3.  Install all dependencies and commit hook (optional).

        pip install -r requirements.txt
        pre-commit install

4.  Create a new feature branch from `master`.

        git checkout -b feature/my-new-feature

5.  Add your feature, tests and documentation.

6.  Push your branch to github.

7.  Submit a pull request into `master`.

## Programming style

### Testing

We appreciate TDD and expect a sufficient code coverage.

Please run your tests with `coverage run --branch --source='src/' src/manage.py test src/ && coverage report --fail-under=50`.

### Documentation

We expect all functions and classes to be documented using docstrings according to Google's [python-styleguide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings).

### Typing

We make use of [type hints](https://docs.python.org/3.6/library/typing.html) for better code readability. If you use VS Code as IDE, we recommend the extension [pylance](https://github.com/microsoft/pylance-release) for type checking.

## Code style

In general we follow Google's [python-styleguide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md) with exceptions where it makes sense. We format and lint our code with [black](https://github.com/psf/black) and [flake8](https://gitlab.com/pycqa/flake8) giving priority to black when conflicts occur.

Please use `black .` to format your code.
