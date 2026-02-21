import ctypes
import os
from pathlib import Path


class CMetaArray(ctypes.Structure):
    """Follow the definition of how the struct Array is defined in ./array.h"""

    _fields_ = [
        ("rows", ctypes.c_size_t),
        ("cols", ctypes.c_size_t),
        ("data", ctypes.POINTER(ctypes.c_double)),
    ]


class Array:
    def __init__(self, data=None, lib_path=None):

        if lib_path is None:
            current_dir = Path(__file__).parent.resolve()
            project_root = current_dir.parent.parent
            lib_path = project_root / "build" / "libgel.so"

        self._lib = ctypes.CDLL(os.path.abspath(lib_path))

        if data is not None:
            rows = len(data)
            cols = len(data[0]) if rows > 0 else 0

        # Setup argtypes/restypes
        self._setup_ctypes()

        # Constructor (C Allocation)
        self._ptr = self._lib.gel_array_create(rows, cols)
        if not self._ptr:
            raise MemoryError("C-level Array allocation failed.")

        if data is not None:
            flat = [float(item) for row in data for item in row]
            self.fill(flat)

    @property
    def shape(self):
        return (self._ptr.contents.rows, self._ptr.contents.cols)

    def set_value(self, r, c, val):
        self._lib.gel_array_set.argtypes = [
            ctypes.POINTER(CMetaArray),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_double,
        ]
        return self._lib.gel_array_set(self._ptr, r, c, val)

    def fill(self, flat_list):
        expected_size = self.shape[0] * self.shape[1]
        if len(flat_list) != expected_size:
            raise ValueError(
                f"List size ({len(flat_list)}) does not match."
                f"Array capacity ({expected_size})."
            )

        DoubleArray = ctypes.c_double * expected_size
        buffer = DoubleArray(*flat_list)

        status = self._lib.gel_array_fill_bulk(self._ptr, buffer)

        if status != 0:
            raise RuntimeError("C-level gel_array_fill_bulk failed.")

    def __del__(self):
        """Ensure we don't get any leak memory in C."""
        if hasattr(self, "_ptr") and self._ptr:
            self._lib.gel_array_free(self._ptr)

    def __repr__(self):
        r, c = self.shape
        return f"GEL Array({r}x{c})."

    def __getitem__(self, index):
        # Support array[r, c]
        r, c = index
        return self.get_value(r, c)

    def __setitem__(self, index, value):
        # Support array[r, c] = val
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

    def _setup_ctypes(self):
        # gel_array_create
        self._lib.gel_array_create.argtypes = [ctypes.c_size_t, ctypes.c_size_t]
        self._lib.gel_array_create.restype = ctypes.POINTER(CMetaArray)

        # gel_array_free
        self._lib.gel_array_free.argtypes = [ctypes.POINTER(CMetaArray)]
        self._lib.gel_array_free.restype = None

        # gel_array_fill_bulk
        self._lib.gel_array_fill_bulk.argtypes = [
            ctypes.POINTER(CMetaArray),
            ctypes.POINTER(ctypes.c_double),
        ]
        self._lib.gel_array_fill_bulk.restype = ctypes.c_int

        # gel_array_get
        self._lib.gel_array_get.argtypes = [
            ctypes.POINTER(CMetaArray),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_double),
        ]
        self._lib.gel_array_get.restype = ctypes.c_int

    def get_value(self, r, c):
        out = ctypes.c_double()
        status = self._lib.gel_array_get(self._ptr, r, c, ctypes.byref(out))
        if status != 0:
            raise IndexError(f"Indices ({r}, {c}) out of bounds.")
        return out.value
