# Building tref

To build `tref` from source, you need to have `setuptools` and `wheel` installed. You can install them using `pip`:

```bash
pip install setuptools wheel
```

Once you have the build tools installed, you can build the project by running the following command in the root of the project:

```bash
python -m build
```

This will create a `dist` directory containing the build artifacts. The `.whl` file in this directory is the wheel that can be installed using `pip`.

## How it works

The build process is configured using the `pyproject.toml` file. Here's a breakdown of the relevant parts:

*   **`[build-system]`**: This section specifies the build backend and its requirements. In our case, we are using `setuptools` as the build backend.

*   **`[project]`**: This section contains the metadata for the project, such as the name, version, and dependencies.

*   **`[project.scripts]`**: This section defines the command-line scripts that should be created when the project is installed. In our case, we are creating a `tref` command that calls the `main` function in the `tref.__main__` module.

*   **`[tool.setuptools]`**: This section contains `setuptools`-specific configuration. We are using it to specify the packages that should be included in the build.

*   **`setup.cfg`**: This file is used to configure `setuptools`. We are using it to tell `setuptools` to include package data.

*   **`MANIFEST.in`**: This file is used to specify which non-Python files should be included in the package. We are using it to include the `defaultCheatsheets` directory.

When you run `python -m build`, the build backend reads the configuration from these files and creates the build artifacts.
