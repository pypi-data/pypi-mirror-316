# Scintilla

Scintilla is cloned as a submodule in `src/core_lib/scintilla` from an
[unofficial repo](https://github.com/borco/scintilla).

## Updating

* go to `src/core_lib/scintilla`
* fetch the latest tags
* switch to the new tag you want
* commit your changes

```bash
pushd src/core_lib/scintilla
git fetch --tags
git tag
git checkout rel-5-5-3
popd
git add src/core_lib/scintilla
git commit -m "updated scintilla to rel-5-5-3"
```
