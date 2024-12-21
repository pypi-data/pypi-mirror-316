"""Example package using `shiboken6` to create Python bindings for C++ classes.
"""

# the binding will not load if we don't explicitly importing PySide6.QtWidgets
import PySide6.QtWidgets

# import the C++ classes wrapped by the binding
from .borco_shiboken_example import (
    Dog,
    Truck,
    Icecream,
)

# make the C++ classes wrapped by binding available directly from the python
# package
__all__ = [
    "Dog",
    "Truck",
    "Icecream",
]
