# Environment

* the compiler, `cmake` and `ninja` should be on the path
* `cmake` should be able to find the Qt headers and libs
* the `libclang` location should be exported as `CLANG_INSTALL_DIR`

## Windows

### Manual setup

To manually configure the environment, run these commands in a `cmd` terminal:

```batch
rem setup libclang
export CLANG_INSTALL_DIR="C:\libclang\libclang-release_19.1.0";

rem setup VS2022
"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64

rem save current path
pushd .

rem setup Qt
"C:\Qt\6.8.1\msvc2022_64\bin\qtenv2.bat"

rem restore path
popd

rem setup libclang
set CLANG_INSTALL_DIR="C:\libclang\libclang-release_19.1.0"
```

> [!TIP|style:flat|label:Restoring original folder after running qtenv2]
>
> Running `qtenv2.bat` changes the current folder to the Qt root folder.
> To restore the original folder easily, we store it before running the batch file
> with `pushd .` and restore it afterward with `popd`.

### VSCode

If you use *VSCode*, the workspace is configured to use the `Git Bash (Custom)`
custom terminal profile that automatically:

* loads `vcvarsall.bat` to configure *Visual Studio* C++ toolchain
* loads `qtenv2.bat` to configure *Qt6*
* set extra environment variables
* launches *git bash*

When creating the terminal, *VSCode* executes `.vscode/git_bash_custom.bat`,
passing it the `env` defined in `.vscode/settings.json`, including the
`libclang` location, the location of `vcvarsall.bat` and `qtenv2.bat`:

```javascript
{
    "terminal.integrated.defaultProfile.windows": "Git Bash (Custom)",
    "terminal.integrated.profiles.windows": {
        "Git Bash (Custom)": {
            "path": "C:\\WINDOWS\\System32\\cmd.exe",
            "args": [
                "/C",
                "${workspaceFolder}\\.vscode\\git_bash_custom.bat",
                "x64",
            ],
            "env": {
                "CLANG_INSTALL_DIR": "C:\\libclang\\libclang-release_19.1.0",
                "GIT_BASH": "C:\\Program Files\\Git\\bin\\sh.exe",
                "QTENV2_BAT": "C:\\Qt\\6.8.1\\msvc2022_64\\bin\\qtenv2.bat",
                "VCVARSALL_BAT": "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat",
            }
        }
    },
```
