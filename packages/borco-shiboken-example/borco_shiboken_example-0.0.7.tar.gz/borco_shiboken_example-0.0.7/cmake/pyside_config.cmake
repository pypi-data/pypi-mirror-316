# Helper function that runs `pyside_config.py` and returns the output.
# It uses the current python executable.
function(pyside_config option_var)
    set(_default_prefix SHIBOKEN) # prefix used if neither OUTPUT nor PREFIX are not set

    cmake_parse_arguments(
        PARSE_ARGV 1
        arg # prefix
        "AS_LIST" # options
        "OUTPUT;PREFIX" # one value args
        "" # multi value args
    )

    # use python from the virtual environment
    execute_process(
        COMMAND python ${CMAKE_CURRENT_FUNCTION_LIST_DIR}/pyside_config.py ${option_var}
        OUTPUT_VARIABLE _pyside_config_output
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )

    if("${_pyside_config_output}" STREQUAL "")
        message(FATAL_ERROR "Calling \"python ${CMAKE_CURRENT_FUNCTION_LIST_DIR}/pyside_config.py ${option_var}\" returned no output.")
    endif()

    # if the "AS_LIST" is set, replace the spaces with ";" in the pyside_config output
    if(arg_AS_LIST)
        string(REPLACE " " ";" _pyside_config_output "${_pyside_config_output}")
    endif()

    # If the OUTPUT is not set, build the output variable name from the OPTION.
    # The OPTION is converted to uppercase, multiple "-" and "_" are converted to single
    # "_" and the prefix is prepended to result. If the output would start with
    # ${_prefix}_SHIBOKEN_, the SHIBOKEN_ part is dropped.
    if("${arg_OUTPUT}" STREQUAL "")
        if("${arg_PREFIX}" STREQUAL "")
            set(_prefix "${_default_prefix}")
        else()
            set(_prefix "${arg_PREFIX}")
        endif()

        string(TOUPPER "${_prefix}" _prefix)

        set(_out_var "${_prefix}_${option_var}")
        string(TOUPPER "${_out_var}" _out_var)
        string(REGEX REPLACE "(-|_)+" "_" _out_var "${_out_var}")
        string(REGEX REPLACE "^${_prefix}_SHIBOKEN_" "${_prefix}_" _out_var "${_out_var}")
    else()
        set(_out_var "${arg_OUTPUT}")
    endif()

    # return the result to the parent scope
    set(${_out_var} "${_pyside_config_output}" PARENT_SCOPE)
endfunction()
