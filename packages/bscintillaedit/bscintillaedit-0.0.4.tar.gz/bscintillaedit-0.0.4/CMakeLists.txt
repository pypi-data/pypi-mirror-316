cmake_minimum_required(VERSION 3.29)

# ----------------
# CMake policies
# ----------------
cmake_policy(VERSION 3.29)

# Enable policy to not use RPATH settings for install_name on macOS.
if(POLICY CMP0068)
    cmake_policy(SET CMP0068 NEW)
endif()

# --------------------
# Project definition
# --------------------
if(NOT SKBUILD)
    message(STATUS "Running CMake directly.")
    set(SKBUILD_PROJECT_NAME bscintillaedit)
else()
    message(STATUS "Running from 'scikit-build-core'.")
endif()

project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

# ----------------------------------------
# Include local generic cmake extensions
# ----------------------------------------
include(cmake/pretty_print.cmake)

# --------------
# C++ features
# --------------
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ---------
# Options
# ---------
set(BINDINGS_INSTALL_DIR "." CACHE STRING "Folder where to install built bindings.")
set(WITH_BINDINGS FALSE CACHE BOOL "Enable Python bindings.")

include(CMakeDependentOption)

cmake_dependent_option(
    _CPP_DEV_MODE "Enable C++ developer mode." ON "NOT DEFINED SKBUILD" OFF
)

cmake_dependent_option(
    WITH_TESTS "Build tests." ON "_CPP_DEV_MODE" OFF
)

# C++ Sample apps
cmake_dependent_option(
    WITH_SAMPLES "Enable C++ samples." ON "_CPP_DEV_MODE" OFF
)

# ------------------
# Qt configuration
# ------------------
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Core5Compat Widgets)
qt6_standard_project_setup()

# --------------
# C++ core lib
# --------------
add_subdirectory(src/core_lib)

# -------------
# C++ samples
# -------------
if(${WITH_SAMPLES})
    add_subdirectory(samples/cpp/basic)
endif()

# -----------
# C++ tests
# -----------
if(${WITH_TESTS})
    add_subdirectory(tests/cpp/bscintillaedit)
endif()

# -----------------
# Python bindings
# -----------------
if(${WITH_BINDINGS})
    # ------------------
    # Check for Python
    # ------------------
    set(Python_FIND_VIRTUALENV ONLY)
    find_package(
        Python 3
        REQUIRED COMPONENTS Interpreter Development.Module
    )

    # ----------
    # Shiboken
    # ----------
    include(cmake/pyside_config.cmake)
    include(cmake/shiboken.cmake)

    # find shiboken and set some global variables starting with SHIBOKEN_
    find_shiboken()

    # you can inspect the variables created by the 'find_shiboken()' call by
    # uncommenting the line bellow:
    pretty_print_variables(SHIBOKEN_)

    # set some settings common for all shiboken projects
    shiboken_standard_project_setup()

    set(CMAKE_INSTALL_RPATH ${SHIBOKEN_MODULE_PATH})

    add_subdirectory(src/bindings_lib)
endif()
