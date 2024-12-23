#pragma once

#if defined _WIN32 || defined __CYGWIN__
    // Export symbols when creating .dll and .lib, and import them when using .lib.
    #if defined(CORE_LIB_BUILD)
        #define CORE_LIB_EXPORT __declspec(dllexport)
    #else
        #define CORE_LIB_EXPORT __declspec(dllimport)
    #endif
#else
    #define CORE_LIB_EXPORT
#endif
