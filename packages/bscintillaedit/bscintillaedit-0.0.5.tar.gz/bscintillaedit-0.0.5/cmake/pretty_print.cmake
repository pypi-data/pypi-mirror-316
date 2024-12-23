# Pretty print some text.
#
# Use PREFIX to set a custom prefix string.
function(pretty_print_text)
    cmake_parse_arguments(
        arg
        ""
        "PREFIX"
        ""
        ${ARGN}
    )

    if("${arg_PREFIX}" STREQUAL "")
        set(arg_PREFIX "│ ")
    endif()

    list(JOIN arg_UNPARSED_ARGUMENTS " " _text)
    message(STATUS "${arg_PREFIX}${_text}")
endfunction()

# Pretty print a header.
#
# All arguments are printed after the prefix.
function(pretty_print_header)
    pretty_print_text(${ARGV} PREFIX "╭──── ")
endfunction()

# Pretty print a separator.
#
# All arguments are printed after the prefix.
function(pretty_print_separator)
    pretty_print_text(${ARGV} PREFIX "├──── ")
endfunction()

# Pretty print a footer.
#
# All arguments are printed after the prefix.
function(pretty_print_footer)
    pretty_print_text(${ARGV} PREFIX "╰──── ")
endfunction()

# Pretty print a variable.
#
# The variable is printed as a list if it contains the ";" character
# or if the "AS_LIST" option is set.
function(pretty_print_value name_arg value_arg)
    cmake_parse_arguments(
        arg
        "AS_LIST"
        ""
        ""
        ${ARGN}
    )

    if("${value_arg}" MATCHES ".*;.*" OR arg_AS_LIST)
        pretty_print_text("╭── ${name_arg}:")

        foreach(_item IN LISTS value_arg)
            pretty_print_text("│ ${_item}")
        endforeach()

        pretty_print_text("╰──")
    else()
        pretty_print_text("    ${name_arg}: ${value_arg}")
    endif()
endfunction()

# Pretty print variables starting with a prefix.
function(pretty_print_variables prefix_arg)
    get_cmake_property(_variable_names VARIABLES)

    pretty_print_header("variables starting with: ${prefix_arg}")

    foreach(_variable_name IN LISTS _variable_names)
        if("${_variable_name}" MATCHES "^${prefix_arg}.*")
            pretty_print_value("${_variable_name}" "${${_variable_name}}")
        endif()
    endforeach()

    pretty_print_footer()
endfunction()
