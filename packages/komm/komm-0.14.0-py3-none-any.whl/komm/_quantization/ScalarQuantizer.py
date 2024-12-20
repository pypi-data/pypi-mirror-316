import numpy as np
import numpy.typing as npt
from attrs import field, frozen

from .. import abc


@frozen
class ScalarQuantizer(abc.ScalarQuantizer):
    r"""
    General scalar quantizer. It is defined by a list of *levels*, $v_0, v_1, \ldots, v_{L-1}$, and a list of *thresholds*, $t_0, t_1, \ldots, t_L$, satisfying
    $$
        -\infty = t_0 < v_0 < t_1 < v_1 < \cdots < t_{L - 1} < v_{L - 1} < t_L = +\infty.
    $$
    Given an input $x \in \mathbb{R}$, the output of the quantizer is given by $y = v_i$ if and only if $t_i \leq x < t_{i+1}$, where $i \in [0:L)$. For more details, see <cite>Say06, Ch. 9</cite>.

    Attributes:
        levels (Array1D[float]): The quantizer levels $v_0, v_1, \ldots, v_{L-1}$. It should be a list floats of length $L$.

        thresholds (Array1D[float]): The quantizer finite thresholds $t_1, t_2, \ldots, t_{L-1}$. It should be a list of floats of length $L - 1$.

    Examples:
        The $5$-level scalar quantizer whose characteristic (input × output) curve is depicted in the figure below has levels
        $$
            v_0 = -2, ~ v_1 = -1, ~ v_2 = 0, ~ v_3 = 1, ~ v_4 = 2,
        $$
        and thresholds
        $$
            t_0 = -\infty, ~ t_1 = -1.5, ~ t_2 = -0.3, ~ t_3 = 0.8, ~ t_4 = 1.4, ~ t_5 = \infty.
        $$

        <figure markdown>
          ![Scalar quantizer example.](/figures/scalar_quantizer_5.svg)
        </figure>

        >>> quantizer = komm.ScalarQuantizer(levels=[-2.0, -1.0, 0.0, 1.0, 2.0], thresholds=[-1.5, -0.3, 0.8, 1.4])
    """

    levels: npt.NDArray[np.floating] = field(
        converter=np.asarray, repr=lambda x: x.tolist()
    )
    thresholds: npt.NDArray[np.floating] = field(
        converter=np.asarray, repr=lambda x: x.tolist()
    )

    def __attrs_post_init__(self) -> None:
        if self.thresholds.size != self.num_levels - 1:
            raise ValueError("length of 'thresholds' must be 'num_levels - 1'")

        interleaved = np.empty(2 * self.num_levels - 1, dtype=float)
        interleaved[0::2] = self.levels
        interleaved[1::2] = self.thresholds

        if not np.array_equal(np.unique(interleaved), interleaved):
            raise ValueError("invalid values for 'levels' and 'thresholds'")

    @property
    def num_levels(self) -> int:
        r"""
        The number of quantization levels $L$.

        Examples:
            >>> quantizer = komm.ScalarQuantizer(levels=[-2.0, -1.0, 0.0, 1.0, 2.0], thresholds=[-1.5, -0.3, 0.8, 1.4])
            >>> quantizer.num_levels
            5
        """
        return self.levels.size

    def __call__(self, input: npt.ArrayLike) -> npt.NDArray[np.floating]:
        r"""
        Quantizes the input signal.

        Parameters:
            input: The input signal $x$ to be quantized.

        Returns:
            output: The quantized signal $y$.

        Examples:
            >>> quantizer = komm.ScalarQuantizer(levels=[-2.0, -1.0, 0.0, 1.0, 2.0], thresholds=[-1.5, -0.3, 0.8, 1.4])
            >>> x = np.linspace(-2.5, 2.5, num=11)
            >>> y = quantizer(x)
            >>> np.vstack([x, y])
            array([[-2.5, -2. , -1.5, -1. , -0.5,  0. ,  0.5,  1. ,  1.5,  2. ,  2.5],
                   [-2. , -2. , -1. , -1. , -1. ,  0. ,  0. ,  1. ,  2. ,  2. ,  2. ]])
        """
        tiled = np.tile(input, reps=(self.thresholds.size, 1)).transpose()
        output = self.levels[np.sum(tiled >= self.thresholds, axis=1)]
        return output
