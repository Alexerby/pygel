import ctypes
import os
from pathlib import Path
from itertools import chain

LIB_PATH = Path(__file__).parent.parent.parent / "build" / "libgel.so"
_LIB = ctypes.CDLL(os.path.abspath(LIB_PATH))


class CMetaArray(ctypes.Structure):
    """Follow the definition of how the struct Array is defined in ./array.h"""

    _fields_ = [
        ("rows", ctypes.c_size_t),
        ("cols", ctypes.c_size_t),
        ("data", ctypes.POINTER(ctypes.c_double)),
    ]


# gel_array_create
_LIB.gel_array_create.argtypes = [ctypes.c_size_t, ctypes.c_size_t]
_LIB.gel_array_create.restype = ctypes.POINTER(CMetaArray)

# gel_array_free
_LIB.gel_array_free.argtypes = [ctypes.POINTER(CMetaArray)]
_LIB.gel_array_free.restype = None

# gel_array_fill_bulk
_LIB.gel_array_fill_bulk.argtypes = [
    ctypes.POINTER(CMetaArray),
    ctypes.POINTER(ctypes.c_double),
]
_LIB.gel_array_fill_bulk.restype = ctypes.c_int

# gel_array_get
_LIB.gel_array_get.argtypes = [
    ctypes.POINTER(CMetaArray),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_double),
]
_LIB.gel_array_get.restype = ctypes.c_int

# gel_array_add
_LIB.get_array_add.argtypes = [
    ctypes.POINTER(CMetaArray),
    ctypes.POINTER(CMetaArray),
]
_LIB.gel_array_add.restype = ctypes.c_int


class Array:
    def __init__(self, data=None):

        if data is None:
            raise ValueError("Data required for initialization.")

        rows = len(data)
        cols = len(data[0]) if rows > 0 else 0
        total_size = rows * cols

        # Constructor for the C Allocation
        self._ptr = _LIB.gel_array_create(rows, cols)
        if not self._ptr:
            raise MemoryError("C-level Array allocation failed.")

        flat_data = chain.from_iterable(data)

        # TODO: Look closer at performance of this unpacking
        buffer = (ctypes.c_double * total_size)(*flat_data)

        _LIB.gel_array_fill_bulk(self._ptr, buffer)

    @property
    def shape(self) -> tuple[int, int]:
        return (self._ptr.contents.rows, self._ptr.contents.cols)

    def set_value(self, r: int, c: int, val: float):
        """Sets a double-precision value at the specified row and column.

        Args:
            r: row.
            c: column.

        Returns:
            int: 0 on success, -1 if indices are out of bounds.
        """

        _LIB.gel_array_set.argtypes = [
            ctypes.POINTER(CMetaArray),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_double,
        ]

        return _LIB.gel_array_set(self._ptr, r, c, val)

    def fill(self, flat_list: list | list[list]):
        """Populates the array with data from a flattened list.

        Args:
            flat_list: A list of floats with length equal to rows * cols.

        Returns:
            int: 0 on success, -1 if any pointer is NULL.

        Raises:
            ValueError: If the list size does not match array capacity.
            RuntimeError: If the C-level memcpy() fails
        """

        expected_size = self.shape[0] * self.shape[1]
        if len(flat_list) != expected_size:
            raise ValueError(
                f"List size ({len(flat_list)}) does not match."
                f"Array capacity ({expected_size})."
            )

        DoubleArray = ctypes.c_double * expected_size
        buffer = DoubleArray(*flat_list)

        status = _LIB.gel_array_fill_bulk(self._ptr, buffer)

        if status != 0:
            raise RuntimeError("C-level gel_array_fill_bulk failed.")

    def __del__(self):
        """Ensure we don't get any leak memory in C."""
        if hasattr(self, "_ptr") and self._ptr:
            _LIB.gel_array_free(self._ptr)

    def __repr__(self):
        r, c = self.shape
        return f"GEL Array({r}x{c})."

    def __getitem__(self, index):
        """Support array[r, c]."""
        r, c = index
        return self.get_value(r, c)

    def __setitem__(self, index, value):
        """Support array[r, c] = val."""
        r, c = index
        status = self.set_value(r, c, float(value))
        if status != 0:
            raise IndexError(f"Indices ({r}, {c}) out of bounds.")

    def __str__(self):
        r, c = self.shape
        res = []
        for r in range(r):
            row_str = " ".join(f"{self.get_value(r, c):.4f}" for c in range(c))
            res.append(f"[{row_str}]")
        return "\n".join(res)

    def get_value(self, r, c):
        out = ctypes.c_double()
        status = _LIB.gel_array_get(self._ptr, r, c, ctypes.byref(out))
        if status != 0:
            raise IndexError(f"Indices ({r}, {c}) out of bounds.")
        return out.value

