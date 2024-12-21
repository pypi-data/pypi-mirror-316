set(APP_NAME hello_widget_sample)

set(PROJECT_SOURCES
        main.cpp
        mainwindow.cpp
        mainwindow.h
        mainwindow.ui
)

qt_add_executable(
    ${APP_NAME}
    ${PROJECT_SOURCES}
)

target_link_libraries(
    ${APP_NAME} PRIVATE
    core_lib
)
