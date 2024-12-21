#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "trans_dp" for configuration "Release"
set_property(TARGET trans_dp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(trans_dp PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libtrans_dp.so"
  IMPORTED_SONAME_RELEASE "libtrans_dp.so"
  )

list(APPEND _cmake_import_check_targets trans_dp )
list(APPEND _cmake_import_check_files_for_trans_dp "${_IMPORT_PREFIX}/lib64/libtrans_dp.so" )

# Import target "transi_dp" for configuration "Release"
set_property(TARGET transi_dp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(transi_dp PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "trans_dp"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libtransi_dp.so"
  IMPORTED_SONAME_RELEASE "libtransi_dp.so"
  )

list(APPEND _cmake_import_check_targets transi_dp )
list(APPEND _cmake_import_check_files_for_transi_dp "${_IMPORT_PREFIX}/lib64/libtransi_dp.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
