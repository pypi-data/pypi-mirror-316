// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

#pragma once

#include "core_lib_global.h"

#include <iosfwd>
#include <string>

class CORE_LIB_EXPORT Icecream
{
public:
    explicit Icecream(const std::string &flavor);
    virtual Icecream *clone();

    virtual ~Icecream();

    virtual std::string getFlavor() const;

private:
    std::string m_flavor;
};

std::ostream &operator<<(std::ostream &str, const Icecream &i);
