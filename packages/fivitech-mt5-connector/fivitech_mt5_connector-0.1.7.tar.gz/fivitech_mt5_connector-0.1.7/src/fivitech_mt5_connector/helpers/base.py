from typing import Optional, Union
from datetime import datetime
from ..pool import mt5_pools
from ..exceptions import MT5ConnectionError
import MT5Manager

class MT5BaseHelper:
    """Base helper class with common MT5 functionality"""
    
    @staticmethod
    def get_connection(server_id=None, server_type=None):
        """Get MT5 connection based on server_id or server_type"""
        if server_id is not None:
            return mt5_pools.get_by_id(server_id)
        elif server_type is not None:
            return mt5_pools.get_by_type(server_type)
        raise ValueError("Either server_id or server_type must be provided")

    @classmethod
    def get_server_time(cls, server_id=None, server_type=None) -> int:
        """Get MT5 server time as Unix timestamp"""
        connection = cls.get_connection(server_id, server_type)
        if not connection or not connection.manager:
            raise MT5ConnectionError("MT5 connection or manager not available")
        return connection.manager.TimeServer()

    @classmethod
    def convert_to_server_time(
        cls,
        dt: Union[datetime, int],
        server_id: Optional[int] = None,
        server_type: Optional[str] = None
    ) -> int:
        """Convert datetime or timestamp to server time"""
        # Convert input to timestamp if it's a datetime
        if isinstance(dt, datetime):
            local_ts = int(dt.timestamp())
        else:
            local_ts = int(dt)
        server_time = cls.get_server_time(server_id, server_type)
        time_diff = server_time - int(datetime.now().timestamp())
        
        return local_ts + time_diff 