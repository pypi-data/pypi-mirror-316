import numpy
import h5py
from hdf5array import Hdf5CompressedSparseMatrix
import delayedarray
import tempfile
import scipy.sparse

from utils import chunk_shape

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def _mockup(mat):
    _, path = tempfile.mkstemp(suffix=".h5")
    name = "whee"

    with h5py.File(path, "w") as handle:
        handle.create_dataset(name + "/data", data=mat.data, compression="gzip")
        handle.create_dataset(name + "/indices", data=mat.indices, compression="gzip")
        handle.create_dataset(name + "/indptr", data=mat.indptr, compression="gzip")

    return path, name


def test_Hdf5CompressedSparseMatrix_column():
    shape = (100, 80)
    y = scipy.sparse.random(*shape, 0.1).tocsc()
    path, group = _mockup(y)
    arr = Hdf5CompressedSparseMatrix(path, group, shape=shape, by_column=True)

    assert arr.shape == shape
    assert arr.dtype == y.dtype
    assert chunk_shape(arr) == (100, 1)
    assert (delayedarray.to_dense_array(arr) == y.toarray()).all()
    assert not delayedarray.is_masked(arr)

    # Check that consecutive slicing works as expected.
    slices = (slice(30, 90), slice(20, 60))
    ref = y[slices].toarray()
    ranges = [range(*s.indices(shape[i])) for i, s in enumerate(slices)]
    assert (delayedarray.extract_dense_array(arr, (*ranges,)) == ref).all()

    out = delayedarray.extract_sparse_array(arr, (*ranges,))
    assert isinstance(out, delayedarray.SparseNdarray)
    assert (numpy.array(out) == ref).all()

    # Check that non-consecutive slicing works as expected.
    slices = (slice(3, 90, 3), slice(4, 70, 5))
    ref = y[slices].toarray()
    ranges = [range(*s.indices(shape[i])) for i, s in enumerate(slices)]
    assert (delayedarray.extract_dense_array(arr, (*ranges,)) == ref).all()

    out = delayedarray.extract_sparse_array(arr, (*ranges,))
    assert isinstance(out, delayedarray.SparseNdarray)
    assert (numpy.array(out) == ref).all()


def test_Hdf5CompressedSparseMatrix_row():
    shape = (100, 200)
    y = scipy.sparse.random(*shape, 0.1).tocsr()
    path, group = _mockup(y)
    arr = Hdf5CompressedSparseMatrix(path, group, shape=shape, by_column=False)

    assert arr.shape == shape
    assert arr.dtype == y.dtype
    assert chunk_shape(arr) == (1, 200)
    assert (delayedarray.to_dense_array(arr) == y.toarray()).all()

    # Check that consecutive slicing works as expected.
    slices = (slice(10, 80), slice(50, 150))
    ref = y[slices].toarray()
    ranges = [range(*s.indices(shape[i])) for i, s in enumerate(slices)]
    assert (delayedarray.extract_dense_array(arr, (*ranges,)) == ref).all()

    out = delayedarray.extract_sparse_array(arr, (*ranges,))
    assert isinstance(out, delayedarray.SparseNdarray)
    assert (numpy.array(out) == ref).all()

    # Check that non-consecutive slicing works as expected.
    slices = (slice(10, 80, 2), slice(50, 150, 3))
    ref = y[slices].toarray()
    ranges = [range(*s.indices(shape[i])) for i, s in enumerate(slices)]
    assert (delayedarray.extract_dense_array(arr, (*ranges,)) == ref).all()

    out = delayedarray.extract_sparse_array(arr, (*ranges,))
    assert isinstance(out, delayedarray.SparseNdarray)
    assert (numpy.array(out) == ref).all()


def test_Hdf5CompressedSparseMatrix_dtype():
    shape = (55, 45)
    y = (scipy.sparse.random(*shape, 0.2) * 10).tocsc().astype(numpy.int32)
    path, group = _mockup(y)
    arr = Hdf5CompressedSparseMatrix(
        path,
        group,
        shape=shape,
        by_column=True,
        dtype=numpy.int16,
        index_dtype=numpy.uint8,
    )

    assert arr.shape == shape
    assert arr.dtype == numpy.int16
    assert chunk_shape(arr) == (55, 1)

    as_dense = delayedarray.to_dense_array(arr)
    assert (as_dense == y.toarray()).all()
    assert as_dense.dtype == numpy.int16

    as_sparse = delayedarray.to_sparse_array(arr)
    assert (numpy.array(as_sparse) == y.toarray()).all()
    assert as_sparse.dtype == numpy.int16
    assert as_sparse.index_dtype == numpy.uint8


def test_Hdf5CompressedSparseMatrix_properties():
    shape = (100, 200)
    y = scipy.sparse.random(*shape, 0.1).tocsr()
    path, group = _mockup(y)
    arr = Hdf5CompressedSparseMatrix(path, group, shape=shape, by_column=False)

    assert not arr.by_column
    assert arr.path == path
    assert arr.group_name == group
    assert arr.data_name == group + "/data"
    assert arr.indices_name == group + "/indices"
    assert arr.indptr_name == group + "/indptr"

    rewrap = delayedarray.wrap(arr.seed)
    assert isinstance(rewrap, Hdf5CompressedSparseMatrix)


def test_Hdf5CompressedSparseMatrix_to_sparse():
    shape = (100, 200)
    y = scipy.sparse.random(*shape, 0.1).tocsr()
    path, group = _mockup(y)
    arr = Hdf5CompressedSparseMatrix(path, group, shape=shape, by_column=False)

    _to_csr = delayedarray.to_scipy_sparse_matrix(arr, "csr")
    assert isinstance(_to_csr, scipy.sparse.csr_matrix)

    _to_csc = delayedarray.to_scipy_sparse_matrix(arr, "csc")
    assert isinstance(_to_csc, scipy.sparse.csc_matrix)

    _to_coo = delayedarray.to_scipy_sparse_matrix(arr, "coo")
    assert isinstance(_to_coo, scipy.sparse.coo_matrix)
