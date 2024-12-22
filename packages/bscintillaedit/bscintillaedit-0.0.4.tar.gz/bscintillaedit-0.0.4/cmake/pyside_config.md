# pyside_config.py

The `pyside_config.py` script is a copy of `examples/utils/pyside_config.py` from the `PySide` source code.

No changes have been done to this file, nor should be made in the future, so that updating it can be done by simply downloading a new version from the `PySide` source code.

If the new version breaks something, the fixes should be done in the code using this script.

## Using

Get all available options:

```bash
python cmake/pyside_config.py
```

> ```txt
> --shiboken-module-path      : ***/.venv/Lib/site-packages/shiboken6
> --shiboken-generator-path   : ***/.venv/Lib/site-packages/shiboken6_generator
> ...
> ```

Get a specific option:

```bash
python cmake/pyside_config.py --shiboken-module-path
```

> ```txt
> ***/.venv/Lib/site-packages/shiboken6
> ```

## Updating

To update the `pyside_config.py` script, just download a new version from the `PySide` repo.

For example, the `6.8.1` version of this file can be retrieved from <https://code.qt.io/cgit/pyside/pyside-setup.git/plain/examples/utils/pyside_config.py?h=6.8.1>.

## License

The original file is released under Qt-Commercial OR BSD-3-Clause.
