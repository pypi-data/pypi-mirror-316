from typing import Any, Iterable, Iterator, Optional, Sequence, Tuple, TypeVar, Union

from h5py._hl.dataset import Dataset # type: ignore

import numpy as np
import numpy.typing as npt
from .func import list_unzip
import itertools

KT = TypeVar("KT")
VT = TypeVar("VT")

def get_lists(slices: Iterable[Tuple[int, Optional[int]]]) -> Sequence[int]:
    def convert_back(slice: Tuple[int, Optional[int]]) -> Sequence[int]:
        start, end = slice
        if end is None:
            return [start]
        idxs = list(range(start, end))
        return idxs

    result = list(itertools.chain.from_iterable(map(convert_back, slices)))
    return result


def memslicer(matrix: Union[Dataset, npt.NDArray[Any]], slices: Iterable[Tuple[int, Optional[int]]]) -> npt.NDArray[Any]:
    idxs = get_lists(slices)
    min_idx, max_idx= min(idxs), max(idxs)
    new_idxs = tuple([idx - min_idx for idx in idxs])
    dims = len(matrix.shape)
    
    def get_slice_1d():
        big_slice_mat = matrix[min_idx:(max_idx + 1)]        
        small_slice_mat = big_slice_mat[new_idxs] # type: ignore
        return small_slice_mat
    def get_slice_2d():
        big_slice_mat = matrix[min_idx:(max_idx + 1),:]
        small_slice_mat = big_slice_mat[new_idxs, :] # type: ignore
        return small_slice_mat
   
    if dims == 1:
        mat = get_slice_1d()
        return mat
    if dims == 2:
        mat = get_slice_2d()
        return mat
    raise NotImplementedError("No Slicing for 3d yet")


def slicer(matrix: Union[Dataset, npt.NDArray[Any]], slices: Iterable[Tuple[int, Optional[int]]]) -> npt.NDArray[Any]:
        def get_slices_1d():
            for slice_min, slice_max in slices:
                if slice_max is not None:
                    yield matrix[slice_min:slice_max]
                else:
                    yield matrix[slice_min]
        def get_slices_2d():
            for slice_min, slice_max in slices:
                if slice_max is not None:
                    yield matrix[slice_min:slice_max,:]
                else:
                    yield matrix[slice_min,:]
        dims = len(matrix.shape)
        if dims == 1:
            return np.hstack(list(get_slices_1d())) # type: ignore
        return np.vstack(list(get_slices_2d())) # type: ignore

def matrix_to_vector_list(matrix: npt.NDArray[Any]) -> Sequence[npt.NDArray[Any]]:
    def get_vector(index: int) -> npt.NDArray[Any]:
        return matrix[index, :]
    n_rows = matrix.shape[0]
    rows = range(n_rows)
    return list(map(get_vector, rows))

def matrix_tuple_to_vectors(keys: Sequence[KT], 
                            matrix: npt.NDArray[Any]
                           ) -> Tuple[Sequence[KT], Sequence[npt.NDArray[Any]]]:
    return keys, matrix_to_vector_list(matrix)

def matrix_tuple_to_zipped(keys: Sequence[KT], 
                           matrix: npt.NDArray[Any]) -> Sequence[Tuple[KT, npt.NDArray[Any]]]:
    result = list(zip(keys, matrix_to_vector_list(matrix)))
    return result

def raw_proba_chainer(itera: Iterator[Tuple[Sequence[KT], npt.NDArray[Any]]]) -> Tuple[Sequence[KT], npt.NDArray[Any]]:
    key_lists, matrices = list_unzip(itera)
    keys = list(itertools.chain(*key_lists))
    matrix = np.vstack(matrices)
    return keys, matrix