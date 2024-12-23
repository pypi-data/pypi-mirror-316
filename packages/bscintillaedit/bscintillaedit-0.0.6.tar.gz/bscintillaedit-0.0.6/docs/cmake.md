# CMake

## Presets

The presets are defined in `CMakePresets.json`.

### venv

This preset uses the *Python* version installed in `.venv` with:

```bash
uv sync
```

#### Workflow

```bash
cmake --workflow --preset venv
```

#### Configure

```bash
cmake --preset venv
```

#### Build

```bash
cmake --preset venv --build
```

#### Testings

Run **C++ tests**:

```bash
ctest --preset venv
```

#### Artifacts

The build artifacts are stored under `build/venv`. To clean them, run:

```bash
rm -rf build/venv
```
