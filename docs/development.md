# Prompt-as-Method Development Notes

```shell
poetry install --with development
poetry run python -m prompt_as_method --help
```

## Running unittests (automatically on push)

```shell
poetry run python -m unittest
```

## Running linter (automatically on push)

```shell
poetry run flake8 src --count --max-complexity=10 --max-line-length=127 --statistics
```

## Release new version

- Change `version` in [`pyproject.toml`](../pyproject.toml)
- Add a release via [Github web interface](https://github.com/GESIS-Methods-Hub/prompt-as-method/releases/new), tagged `v<VERSION>`
