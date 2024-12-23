set(BINDINGS_LIB_NAME bscintillaedit)

shiboken_add_bindings(
    ${BINDINGS_LIB_NAME}
    WRAPPED_LIB core_lib
    BINDINGS_HEADER_FILE ${CMAKE_CURRENT_SOURCE_DIR}/bindings.h
    BINDINGS_TYPESYSTEM_FILE ${CMAKE_CURRENT_SOURCE_DIR}/bindings.xml

    WITH_QT  # include qt and pyside libs when building the bindings lib

    # The names of the generated sources are obtained by converting the class
    # names to lowercase and then appending the "_wrapper.cpp" suffix to them.
    #
    # The wrapper name is not related to the name of the source file where the
    # class is defined in any way.
    #
    # Example: HelloWidget -> hellowidget_wrapper.cpp
    BINDINGS_GENERATED_SOURCES
    ${CMAKE_CURRENT_BINARY_DIR}/${BINDINGS_LIB_NAME}/${BINDINGS_LIB_NAME}_module_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/${BINDINGS_LIB_NAME}/bscintillaedit_wrapper.cpp

    BINDINGS_INCLUDE_DIRS
    ${SHIBOKEN_GENERATOR_INCLUDE_PATH}
    ${SHIBOKEN_PYSIDE_INCLUDE_PATH}
    ${SHIBOKEN_PYSIDE_INCLUDE_PATH}/QtCore
    ${SHIBOKEN_PYSIDE_INCLUDE_PATH}/QtGui
    ${SHIBOKEN_PYSIDE_INCLUDE_PATH}/QtWidgets

    # The libraries that must be linked with the binding library
    BINDINGS_LINK_LIBRARIES
    ${SHIBOKEN_PYSIDE_SHARED_LIBRARIES_CMAKE}
    ${SHIBOKEN_MODULE_SHARED_LIBRARIES_CMAKE}

    SHIBOKEN_GENERATOR_OPTIONS
    --avoid-protected-hack
    --enable-parent-ctor-heuristic
    --enable-pyside-extensions # needed when wrapping Qt widgets
    --enable-return-value-heuristic
    --generator-set=shiboken
    --output-directory=${CMAKE_CURRENT_BINARY_DIR}
    --use-isnull-as-nb_nonzero
    -T${CMAKE_CURRENT_SOURCE_DIR}
    -T${SHIBOKEN_PYSIDE_PATH}/typesystems

    SHIBOKEN_GENERATOR_INCLUDE_OTHER_PATHS
    ${CMAKE_CURRENT_SOURCE_DIR}
)
