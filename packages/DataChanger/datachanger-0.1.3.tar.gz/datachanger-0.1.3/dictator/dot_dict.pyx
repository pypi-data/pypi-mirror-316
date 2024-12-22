from cpython.dict cimport PyDict_New, PyDict_SetItem
from json import loads  # For handling JSON data

cdef class DotDict:
    cdef dict __dict__  # Dictionary to store attributes

    def __cinit__(self, input_data=None):
        """Initialize the DotDict with a dictionary or JSON string."""
        self.__dict__ = PyDict_New()
        if input_data:
            self._load_data(input_data)

    cdef void _load_data(self, input_data):
        """Load data from a dictionary or JSON string."""
        if isinstance(input_data, str):
            input_data = loads(input_data)  # Convert JSON string to dict

        if isinstance(input_data, dict):
            self._load_dict(input_data)
        else:
            raise ValueError("Input data must be a dictionary or a valid JSON string.")

    cdef void _load_dict(self, dict input_dict):
        """Load data into the dictionary."""
        cdef object key, value
        for key, value in input_dict.items():
            PyDict_SetItem(self.__dict__, key, self._wrap_value(value))

    cdef object _wrap_value(self, value):
        """Wrap the value into an appropriate type."""
        if isinstance(value, dict):
            return DotDict(value)  # Convert nested dictionaries
        elif isinstance(value, list):
            return self._wrap_iterable(value)  # Handle lists
        elif isinstance(value, tuple):
            return self._wrap_iterable(value)  # Handle tuples
        elif isinstance(value, set):
            return self._wrap_iterable(value)  # Handle sets
        else:
            return value  # Leave primitive values as-is

    cdef object _wrap_iterable(self, iterable):
        """Wrap nested dictionaries inside iterables (list, tuple, set) as DotDict objects."""
        cdef list result = []
        for item in iterable:
            if isinstance(item, dict):
                result.append(DotDict(item))  # Wrap dictionary items as DotDict
            else:
                result.append(item)
        return result

    def __getattr__(self, str name):
        """Handle dynamic attribute access gracefully."""
        try:
            value = self.__dict__[name]
            if isinstance(value, (list, tuple, set)):
                return self._wrap_iterable(value)
            return value
        except KeyError:
            return None  # Return None instead of raising an error for missing attributes

    def __setattr__(self, str name, value):
        """Allow dynamic assignment of attributes."""
        PyDict_SetItem(self.__dict__, name, self._wrap_value(value))

    def to_dict(self):
        """Convert the DotDict into a standard dictionary."""
        return self._convert_to_dict()

    cdef dict _convert_to_dict(self):
        """Recursively convert the DotDict into a standard dictionary."""
        cdef dict output = PyDict_New()
        cdef object key, value
        for key, value in self.__dict__.items():
            if isinstance(value, DotDict):
                PyDict_SetItem(output, key, value.to_dict())
            elif isinstance(value, (list, tuple, set)):
                PyDict_SetItem(output, key, self._convert_iterables(value))
            else:
                PyDict_SetItem(output, key, value)
        return output

    cdef object _convert_iterables(self, iterable):
        """Helper function to convert lists, tuples, and sets."""
        if isinstance(iterable, list):
            return self._wrap_iterable(iterable)
        elif isinstance(iterable, tuple):
            return self._wrap_iterable(iterable)
        elif isinstance(iterable, set):
            return self._wrap_iterable(iterable)
        return iterable
