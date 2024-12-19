from .constants import MT5ServerConfig
from .pool import MT5ConnectionPools
from .interface import MT5Interface

# Expose MT5Pool as an alias for MT5ConnectionPools
MT5Pool = MT5ConnectionPools

__version__ = "0.1.6"
__all__ = ['MT5Pool', 'MT5ServerConfig', 'MT5Interface']
