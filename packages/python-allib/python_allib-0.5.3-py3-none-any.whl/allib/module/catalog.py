from enum import Enum
from ..activelearning import ALCatalog
from ..feature_extraction import FECatalog
from ..balancing import BalancerCatalog 
from ..environment import EnvironmentCatalog
from ..machinelearning import MachineLearningCatalog

class ModuleCatalog:
    class AL(ALCatalog):
        pass
    class FE(FECatalog):
        pass
    class BL(BalancerCatalog):
        pass
    class ENV(EnvironmentCatalog):
        pass
    class ML(MachineLearningCatalog):
        pass


class ActiveLearningTasks(Enum):
    TAR = "TAR"
    CLASSIFICATION = "CLASS"

class ApplicationModules(Enum):
    BENCHMARK = "benchmark"
    CREATE_JOBS = "create_jobs"

