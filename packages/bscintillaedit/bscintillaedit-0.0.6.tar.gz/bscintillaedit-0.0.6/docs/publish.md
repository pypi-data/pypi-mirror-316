# Publishing to PyPI

```bash
rm -rf .venv/ build/ dist/
git tag vX.Y.Z # replace vX.Y.Z with the appropriate tag
git push && git push --tags
uv build
uv publish
```

> [!WARNING|label:Important]
>
> **Increment** the package version in  `src/bscintillaedit/__init__.py` and
> **tag the code** before publishing.

> [!WARNING|label:Important]
>
> Remove the `dist/` folder before publishing, to avoid uploading older
> artifacts to *PyPI*.
