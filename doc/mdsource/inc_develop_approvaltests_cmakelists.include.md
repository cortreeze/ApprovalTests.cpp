

```cmake
cmake_minimum_required(VERSION 3.8 FATAL_ERROR)

project(develop_approvaltests)

enable_testing()

# -------------------------------------------------------------------
# Catch2
set(CATCH_BUILD_TESTING OFF CACHE BOOL "")
add_subdirectory(
        ../Catch2
        ${CMAKE_CURRENT_BINARY_DIR}/catch2_build
)

# -------------------------------------------------------------------
# doctest
add_subdirectory(
        ../doctest
        ${CMAKE_CURRENT_BINARY_DIR}/doctest_build
)


# -------------------------------------------------------------------
# GoogleTest
# Prevent GoogleTest from overriding our compiler/linker options
# when building with Visual Studio
set(gtest_force_shared_crt ON CACHE BOOL "" )
add_subdirectory(
        ../googletest
        ${CMAKE_CURRENT_BINARY_DIR}/googletest_build
)

# -------------------------------------------------------------------
# Boost.ut
# ec49196855078d98738f54023b488b2f85299826 is the first commit that works with FetchContent
# TODO Add a Boost.UT issue asking for option names to have a prefix added
set(BUILD_BENCHMARKS OFF CACHE BOOL "")
set(BUILD_EXAMPLES OFF CACHE BOOL "")
set(BUILD_TESTS OFF CACHE BOOL "")

add_subdirectory(
        ../ut
        ${CMAKE_CURRENT_BINARY_DIR}/ut_build
)

if ("${CMAKE_CXX_COMPILER_ID}" MATCHES "Clang")
    # Turn off some checks for issues that should be fixed in ApprovalTests code
    target_compile_options(boost.ut INTERFACE
            -Wno-newline-eof
            -Wno-shadow-field-in-constructor
            -Wno-weak-vtables
            -Wno-c99-extensions # Needed for Boost.ut, at least in v1.1.6
            )
endif()

# -------------------------------------------------------------------
# ApprovalTests.cpp

set(APPROVAL_TESTS_BUILD_TESTING ON CACHE BOOL "")
set(APPROVAL_TESTS_BUILD_EXAMPLES ON CACHE BOOL "")
set(APPROVAL_TESTS_BUILD_CMAKE_INTEGRATION_TESTING ON CACHE BOOL "")

add_subdirectory(
        ../ApprovalTests.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/approvaltests.cpp_build
)
```
