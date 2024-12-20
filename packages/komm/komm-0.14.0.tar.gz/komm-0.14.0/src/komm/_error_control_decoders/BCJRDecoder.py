from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from .. import abc
from .._error_control_convolutional import TerminatedConvolutionalCode
from .._util.bit_operations import int_to_bits
from .._util.decorators import vectorized_method


@dataclass
class BCJRDecoder(abc.BlockDecoder[TerminatedConvolutionalCode]):
    r"""
    Bahl–Cocke–Jelinek–Raviv (BCJR) decoder for [terminated convolutional codes](/ref/TerminatedConvolutionalCode). For more details, see <cite>LC04, Sec. 12.6</cite>.

    Parameters:
        code: The terminated convolutional code to be used for decoding.
        snr: The signal-to-noise ratio (SNR) of the channel (linear, not decibel).

    Notes:
        - Input type: `soft`.
        - Output type: `soft`.

    # `__call__`

    :::komm.abc.BlockDecoder.BlockDecoder.__call__

    Examples:
        >>> convolutional_code = komm.ConvolutionalCode(feedforward_polynomials=[[0b11, 0b1]], feedback_polynomials=[0b11, 0b11])
        >>> code = komm.TerminatedConvolutionalCode(convolutional_code, num_blocks=3, mode="zero-termination")
        >>> decoder = komm.BCJRDecoder(code, snr=0.25)
        >>> decoder([-0.8, -0.1, -1.0, +0.5, +1.8, -1.1, -1.6, +1.6])
        array([-0.47774884, -0.61545527,  1.03018771])
    """

    code: TerminatedConvolutionalCode
    snr: float = 1.0

    def __post_init__(self) -> None:
        self._fsm = self.code.convolutional_code.finite_state_machine()
        num_states = self._fsm.num_states
        if self.code.mode == "direct-truncation":
            self._initial_state_distribution = np.eye(1, num_states, 0)
            self._final_state_distribution = np.ones(num_states) / num_states
        elif self.code.mode == "zero-termination":
            self._initial_state_distribution = np.eye(1, num_states, 0)
            self._final_state_distribution = np.eye(1, num_states, 0)
        elif self.code.mode == "tail-biting":
            raise NotImplementedError("algorithm not implemented for 'tail-biting'")

        n = self.code.convolutional_code.num_output_bits
        self._cache_polar = (-1) ** int_to_bits(range(2**n), width=n)

    def _metric_function(self, y: int, z: float) -> float:
        return 2.0 * self.snr * np.dot(self._cache_polar[y], z)

    @vectorized_method
    def _decode(self, r: npt.NDArray[np.floating]) -> npt.NDArray[np.integer]:
        n = self.code.convolutional_code.num_output_bits
        mu = self.code.convolutional_code.memory_order

        input_posteriors = self._fsm.forward_backward(
            observed_sequence=r.reshape(-1, n),
            metric_function=self._metric_function,
            initial_state_distribution=self._initial_state_distribution,
            final_state_distribution=self._final_state_distribution,
        )

        if self.code.mode == "zero-termination":
            input_posteriors = input_posteriors[:-mu]

        return np.log(input_posteriors[:, 0] / input_posteriors[:, 1])
