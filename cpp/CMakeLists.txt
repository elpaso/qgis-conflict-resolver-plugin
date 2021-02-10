cmake_minimum_required(VERSION 3.10.0)
project(qgispatches VERSION 1.0.0 DESCRIPTION "qgispatches")
set(CMAKE_INCLUDE_CURRENT_DIR ON)
SET(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})
find_package(Qt5 COMPONENTS Core Widgets Gui Xml REQUIRED)
find_package(QGIS REQUIRED)
include_directories(${Qt5Widgets_INCLUDES} ${QGIS_INCLUDE_DIR})

add_library(qgispatches SHARED
    qgispatch.cpp
)

set_target_properties(qgispatches PROPERTIES
    SOVERSION 1
    PUBLIC_HEADER qgispatch.h
)

target_link_libraries(qgispatches ${Qt5Widgets_LIBRARIES} ${Qt5Xml_LIBRARIES} ${QGIS_CORE_LIBRARY})
