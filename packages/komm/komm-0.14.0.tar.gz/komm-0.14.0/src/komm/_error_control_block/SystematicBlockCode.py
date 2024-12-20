from functools import cached_property

import numpy as np
import numpy.typing as npt
from attrs import field, frozen

from .BlockCode import BlockCode


@frozen(kw_only=True, eq=False)
class SystematicBlockCode(BlockCode):
    r"""
    Systematic linear block code. A *systematic linear block code* is a [linear block code](/ref/BlockCode) in which the information bits can be found in predefined positions in the codeword, called the *information set* $\mathcal{K}$, which is a $k$-sublist of $[0 : n)$; the remaining positions are called the *parity set* $\mathcal{M}$, which is a $m$-sublist of $[0 : n)$. In this case, the generator matrix then has the property that the columns indexed by $\mathcal{K}$ are equal to $I_k$, and the columns indexed by $\mathcal{M}$ are equal to $P$. The check matrix has the property that the columns indexed by $\mathcal{M}$ are equal to $I_m$, and the columns indexed by $\mathcal{K}$ are equal to $P^\transpose$. The matrix $P \in \mathbb{B}^{k \times m}$ is called the *parity submatrix* of the code.

    The constructor expects the parity submatrix and the information set.

    Attributes:
        parity_submatrix: The parity submatrix $P$ the code, which is a $k \times m$ binary matrix.

        information_set: Either an array containing the indices of the information positions, which must be a $k$-sublist of $[0 : n)$, or one of the strings `'left'` or `'right'`. The default value is `'left'`.

    Examples:
        >>> code = komm.SystematicBlockCode(parity_submatrix=[[0, 1, 1], [1, 1, 0]])
        >>> (code.length, code.dimension, code.redundancy)
        (5, 2, 3)
        >>> code.generator_matrix
        array([[1, 0, 0, 1, 1],
               [0, 1, 1, 1, 0]])
        >>> code.check_matrix
        array([[0, 1, 1, 0, 0],
               [1, 1, 0, 1, 0],
               [1, 0, 0, 0, 1]])

        >>> code = komm.SystematicBlockCode(parity_submatrix=[[0, 1, 1], [1, 1, 0]], information_set='right')
        >>> (code.length, code.dimension, code.redundancy)
        (5, 2, 3)
        >>> code.generator_matrix
        array([[0, 1, 1, 1, 0],
               [1, 1, 0, 0, 1]])
        >>> code.check_matrix
        array([[1, 0, 0, 0, 1],
               [0, 1, 0, 1, 1],
               [0, 0, 1, 1, 0]])
    """

    _parity_submatrix: npt.ArrayLike = field(
        default=None, repr=False, alias="parity_submatrix"
    )
    _information_set: npt.ArrayLike | str = field(
        default="left", repr=False, alias="information_set"
    )

    def __repr__(self) -> str:
        args = ", ".join([
            f"parity_submatrix={self.parity_submatrix.tolist()}",
            f"information_set={self.information_set.tolist()}",
        ])
        return f"{self.__class__.__name__}({args})"

    @cached_property
    def parity_submatrix(self) -> npt.NDArray[np.integer]:
        return np.asarray(self._parity_submatrix)

    @cached_property
    def information_set(self) -> npt.NDArray[np.integer]:
        n, k, m = self.length, self.dimension, self.redundancy
        if self._information_set == "left":
            information_set = range(k)
        elif self._information_set == "right":
            information_set = range(m, n)
        else:
            information_set = self._information_set
        try:
            information_set = np.asarray(information_set)
        except TypeError:
            raise ValueError(
                "'information_set' must be either 'left', 'right', or an array of int"
            )
        if (
            information_set.size != k
            or information_set.min() < 0
            or information_set.max() > n
        ):
            raise ValueError("'information_set' must be a 'k'-sublist of 'range(n)'")
        return information_set

    @cached_property
    def parity_set(self) -> npt.NDArray[np.integer]:
        return np.setdiff1d(np.arange(self.length), self.information_set)

    @property
    def dimension(self) -> int:
        return self.parity_submatrix.shape[0]

    @property
    def redundancy(self) -> int:
        return self.parity_submatrix.shape[1]

    @property
    def length(self) -> int:
        return self.dimension + self.redundancy

    @cached_property
    def generator_matrix(self) -> npt.NDArray[np.integer]:
        k, n = self.dimension, self.length
        generator_matrix = np.empty((k, n), dtype=int)
        generator_matrix[:, self.information_set] = np.eye(k, dtype=int)
        generator_matrix[:, self.parity_set] = self.parity_submatrix
        return generator_matrix

    @cached_property
    def check_matrix(self) -> npt.NDArray[np.integer]:
        m, n = self.redundancy, self.length
        check_matrix = np.empty((m, n), dtype=int)
        check_matrix[:, self.information_set] = self.parity_submatrix.T
        check_matrix[:, self.parity_set] = np.eye(m, dtype=int)
        return check_matrix

    def _encode(self, u: npt.NDArray[np.integer]) -> npt.NDArray[np.integer]:
        v = np.empty(u.shape[:-1] + (self.length,), dtype=int)
        v[..., self.information_set] = u
        v[..., self.parity_set] = u @ self.parity_submatrix % 2
        return v

    def _inverse_encode(self, v: npt.NDArray[np.integer]) -> npt.NDArray[np.integer]:
        s = self._check(v)
        if not np.all(s == 0):
            raise ValueError("one or more inputs in 'v' are not valid codewords")
        u = v[..., self.information_set]
        return u

    def _check(self, r: npt.NDArray[np.integer]) -> npt.NDArray[np.integer]:
        r_inf = r[..., self.information_set]
        r_par = r[..., self.parity_set]
        s = (r_inf @ self.parity_submatrix + r_par) % 2
        return s
