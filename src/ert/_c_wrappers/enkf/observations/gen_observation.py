from dataclasses import dataclass
from typing import Tuple

import numpy as np
import numpy.typing as npt

from ert._c_wrappers.enkf import ActiveList
from ert._c_wrappers.enkf.enums import ActiveMode


@dataclass(eq=False)
class GenObservation:
    values: npt.NDArray[np.double]
    stds: npt.NDArray[np.double]
    indices: npt.NDArray[np.int32]
    std_scaling: npt.NDArray[np.double]

    def __eq__(self, other):
        return (
            np.array_equal(self.values, other.values)
            and np.array_equal(self.stds, other.stds)
            and np.array_equal(self.indices, other.indices)
            and np.array_equal(self.std_scaling, other.std_scaling)
        )

    def __len__(self):
        return len(self.values)

    def __getitem__(self, obs_index: int) -> Tuple[float, float]:
        return (self.values[obs_index], self.stds[obs_index])

    def getStdScaling(self, obs_index: int) -> float:
        return self.std_scaling[obs_index]

    def updateStdScaling(self, factor: float, active_list: ActiveList) -> None:
        if active_list.getMode() == ActiveMode.ALL_ACTIVE:
            self.std_scaling = np.full(len(self.values), factor)
        else:
            for i in active_list.get_active_index_list():
                self.std_scaling[i] = factor

    def getIndex(self, obs_index) -> int:
        return self.getDataIndex(obs_index)

    def getDataIndex(self, obs_index: int) -> int:
        return self.indices[obs_index]
