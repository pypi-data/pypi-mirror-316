set(LIB_NAME core_lib)

qt_add_library(
    ${LIB_NAME} SHARED
    # pure c++ classes
    core_lib_global.h
    icecream.h
    icecream.cpp
    truck.h
    truck.cpp
    dog.h
    dog.cpp
    # qt classes
    hellowidget.h
    hellowidget.cpp
)

target_include_directories(
    ${LIB_NAME} PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(
    ${LIB_NAME} PUBLIC
    Qt6::Widgets
)

# By default the prefix of the shared library is "lib" on UNIX.
# We set it to the empty string "" on all platforms.
set_property(TARGET ${LIB_NAME} PROPERTY PREFIX "")

# Needed mostly on Windows to export symbols, and create a .lib file, otherwise
# the binding library can't link to the sample library.
target_compile_definitions(${LIB_NAME} PRIVATE CORE_LIB_BUILD)
