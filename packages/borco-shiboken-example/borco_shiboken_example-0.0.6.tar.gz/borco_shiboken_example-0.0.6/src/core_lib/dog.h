#pragma once

#include "core_lib_global.h"

#include <string>

struct CORE_LIB_EXPORT Dog
{
    std::string name;
    std::string bark() const;
};
