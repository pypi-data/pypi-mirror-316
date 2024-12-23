# Requirements

To build the `shiboken6` bindings manually, we use:

* C++ compiler (that supports C20 or newer C++ standard)
* Qt 6.8+ headers and libs
* `libclang` 10+
* `cmake` 3.29+
* `ninja`
* Python with development components (headers and libs)
* `uv` to configure and manage a local `.venv` virtual environment (other
  Python environment managers might work, too)

## Windows

### Visual Studio 2022

Install *Visual Studio 2022* with:

* C++ compiler (check **Workload &rarr; Desktop development with C++**)
* `cmake` and `ninja` (check **Installation Details &rarr; Desktop development with C++ &rarr; C++ CMake tools for Windows**)

> [!TIP|label:Using from the command line]
>
> You will have to load the `vcvarsall.bat` before being able to use the
> compiler, `cmake` or `ninja` installed by *Visual Studio 2022* from the
> command line.

### Qt6

Install *Qt6* with:

* Qt6 for *MSVC 2022 64-bit* (for example: **Qt &rarr; Qt 6.X.Y &rarr; MSVC 2022 64-bit**)
* (optional) if you plan to debug the code, install *Qt Debug Information Files*
  (**Qt &rarr; Qt 6.X.Y &rarr; Qt Debug Information Files**)
* (optional) if you want to use *Qt Creator* for development:
  * **Qt Creator &rarr; Qt Creator X.Y.Z**
  * **CDB Debugger Support**
  * **Debugging Tools for Windows**

> [!TIP|label:Using from the command line]
>
> You will have to load the `qtenv2.bat` before being able to compile and link
> with Qt from the command line.

> [!TIP|style:flat|label:CMake and Ninja from Qt]
>
> You only need to install `cmake` and `ninja` from *Qt* installer if you plan to build with
> *MinGW*. Python bindings should be built with *MSVC*, so they are not required by this
> project.

### libclang

Prebuilt `libclang` versions can be found
[here](https://download.qt.io/development_releases/prebuilt/libclang/).

You will need version **10 or newer** to use `shiboken` with Qt 6.0+.

For example, to use `libclang` version 19 on *Windows*:

* create a folder for `libclang` in `C:\libclang`
* download the archived `libclang` in it
* extract the archive
* rename it to `libclang-release_19.1.0`

> [!TIP]
>
> Storing the version in a subdirectory of `C:\libclang` allows us to easily
> switch between `libclang` versions, if needed.
