from .numpy import *
from .aclop import *

try:
    import cupy
    from .cupy import *
    #cp.get_default_memory_pool().free_all_blocks()
except ImportError:
    pass
