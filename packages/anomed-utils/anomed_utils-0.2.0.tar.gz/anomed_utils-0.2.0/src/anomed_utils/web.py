import json
from io import BytesIO
from typing import Any

import falcon
import numpy as np


class StaticJSONResource:
    """Any JSON serializable object, representing a "static" resource (i.e. a
    resource that does not depend on request parameters).

    The object will be represented as a plain JSON string, when a GET request is
    invoked."""

    def __init__(self, obj: Any):
        """
        Parameters
        ----------
        obj : Any
            A JSON serializable object, i.e. is should be compatible with
            `json.dumps`.
        """
        self._obj = obj

    def on_get(self, _, resp: falcon.Response):
        resp.text = json.dumps(self._obj)


def named_ndarrays_to_bytes(named_arrays: dict[str, np.ndarray]) -> bytes:
    """Convert named NumPy arrays to a compressed bytes sequence.

    Use this for example as payload data in a POST request.

    Parameters
    ----------
    named_arrays : dict[str, np.ndarray]
        The named NumPy arrays.

    Returns
    -------
    bytes
        A compressed bytes sequence.

    Notes
    -----
    This is the inverse to `bytes_to_named_ndarrays`.
    """
    compressed_arrays = BytesIO()
    np.savez_compressed(compressed_arrays, **named_arrays)
    return compressed_arrays.getvalue()


def bytes_to_named_ndarrays(data: bytes) -> dict[str, np.ndarray]:
    """Convert a bytes sequence of named (and compressed) NumPy arrays back to
    arrays.

    Use this for example to retrieve NumPy arrays from an HTTP response.

    Parameters
    ----------
    data : bytes
        The bytes representation of a (compressed)

    Returns
    -------
    dict[str, np.ndarray]
        The named arrays.

    Raises
    ------
    OSError
        If the input file does not exist or cannot be read.
    ValueError
        If the file contains an object array.


    Notes
    -----
    This in the inverse to `named_ndarrays_to_bytes`.
    """
    arrays = np.load(BytesIO(data))
    return {name: arrays[name] for name in arrays.files}
