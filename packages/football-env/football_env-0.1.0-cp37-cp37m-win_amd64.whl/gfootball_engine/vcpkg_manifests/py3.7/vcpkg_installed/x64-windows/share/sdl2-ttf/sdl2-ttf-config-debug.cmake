#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SDL2::SDL2_ttf" for configuration "Debug"
set_property(TARGET SDL2::SDL2_ttf APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(SDL2::SDL2_ttf PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/debug/lib/SDL2_ttf.lib"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/debug/bin/SDL2_ttf.dll"
  )

list(APPEND _cmake_import_check_targets SDL2::SDL2_ttf )
list(APPEND _cmake_import_check_files_for_SDL2::SDL2_ttf "${_IMPORT_PREFIX}/debug/lib/SDL2_ttf.lib" "${_IMPORT_PREFIX}/debug/bin/SDL2_ttf.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
