# OpenEO FastAPI

A FastAPI implementation of the OpenEO Api specification.

## Contribute

Included is a vscode dev container which is intended to be used as the development environment for this package. A virtual environment needs to be set up inside the dev container, this is managed by poetry.

#### Setup

1. Run the following commands to initialise poetry venv.
    ```
    # From /openeo-fastapi

    poetry lock

    poetry install --all-extras

    poetry run pre-commit install
    ```

    If you want to add a new dependency. Add it to the pyproject.toml and rerun the two commands again.

    Git is available in the container, so you can commit and push directy to your development branch.

3. You are now ready to write code and run tests!

    Either
    ```
    poetry run python -m pytest
    ```

    Or, run them directly from the testing section of vscode.
