from typing import Dict, List, Optional, Union
from datetime import datetime
from .base import MT5BaseHelper
from ..pool import mt5_pools
from ..exceptions import MT5ConnectionError, MT5ArchiveError
import MT5Manager

class MT5OrderHelper(MT5BaseHelper):
    
  @staticmethod
  def get_connection(server_id=None, server_type=None):
    """Get MT5 connection based on server_id or server_type"""
    if server_id is not None:
      return mt5_pools.get_by_id(server_id)
    elif server_type is not None:
      return mt5_pools.get_by_type(server_type)
    raise ValueError("Either server_id or server_type must be provided")

  @staticmethod
  async def get_open(login: Union[int, List[int]], server_id=None, server_type=None) -> List[MT5Manager.MTOrder]:
    """
    Get open orders for one or multiple users
    
    Args:
        login: Single user login ID or list of login IDs
        server_id: Optional server ID
        server_type: Optional server type ('demo' or 'live')
        
    Returns:
        List of open orders as dictionaries
        
    Raises:
        ValueError: If login is invalid
        MT5ConnectionError: If connection fails
    """
    # Convert single login to list for uniform processing
    logins = [login] if isinstance(login, int) else login
    
    # Validate all logins
    if not all(isinstance(l, int) and l > 0 for l in logins):
      raise ValueError("All logins must be positive integers")
        
    connection = MT5OrderHelper.get_connection(server_id, server_type)
    if not connection or not connection.manager:
      raise MT5ConnectionError("MT5 connection or manager not available")
        
    try:
      # For single login, use OrderGetOpen
      if len(logins) == 1:
        orders = connection.manager.OrderGetOpen(logins[0])
        if orders is None:
            return []
        print(f"DEBUG: orders: {orders}")
        return orders
          
      # For multiple logins, use OrderGetByLogins
      orders = connection.manager.OrderGetByLogins(logins)
      if orders is None:
        return []
      return orders
            
    except Exception as e:
      error = MT5Manager.LastError()
      raise MT5ConnectionError(f"Failed to get open orders: {error}")
    
  @staticmethod
  async def add(params: Dict, server_id=None, server_type=None) -> MT5Manager.MTOrder:
    """
    Add an open order to the server database
    
    Args:
      params: Dictionary containing order details including:
        - Login: Client login (required)
        - Symbol: Trading instrument (required)
        - Type: Order type (required)
        - Digits: Number of decimal places for the symbol (required)
        - DigitsCurrency: Number of decimal places for the currency (required)
        - ContractSize: Contract size (required)
        - VolumeInitial: Initial volume (required)
        - VolumeCurrent: Current volume (required, must not exceed initial)
        - PriceOrder: Order price (required)
        - State: Order state (required, must be valid open state)
        - Ticket: Optional, if 0 or not provided, server will auto-assign
      server_id: Optional server ID
      server_type: Optional server type ('demo' or 'live')
        
    Returns:
      Added order object as dictionary
        
    Raises:
      ValueError: If required parameters are missing or invalid
      MT5ConnectionError: If connection fails
    """
    # Validate required parameters
    required_fields = ['Login', 'Symbol', 'Type', 'Digits', 'DigitsCurrency', 'ContractSize', 'VolumeInitial', 'VolumeCurrent', 'PriceOrder', 'State']
    for field in required_fields:
        if field not in params:
            raise ValueError(f"{field} is required in params")
            
    connection = MT5OrderHelper.get_connection(server_id, server_type)
    if not connection or not connection.manager:
        raise MT5ConnectionError("MT5 connection or manager not available")
            
    try:
        print(f"\n=== MT5 Order Add Debug ===")
        print(f"1. Connection state: connected={connection._connected}")
        print(f"2. Manager instance available: {connection.manager is not None}")
        
        # Create new order object with manager instance
        print("\n3. Creating order object")
        order = MT5Manager.MTOrder(connection.manager)
        if not order:
            error = MT5Manager.LastError()
            raise MT5ConnectionError(f"Failed to create order object: {error}")
        
        # Set order parameters with proper type conversion
        print("4. Setting order parameters:")
        if 'Login' in params:
            order.Login = int(params['Login'])
            print(f"   - Login: {order.Login}")
        if 'Symbol' in params:
            order.Symbol = str(params['Symbol'])
            print(f"   - Symbol: {order.Symbol}")
        if 'Type' in params:
            try:
                order.Type = int(params['Type'])
                print(f"   - Type: {order.Type}")
            except Exception as e:
                raise ValueError(f"Invalid order type: {params['Type']}")
        if 'Digits' in params:
            order.Digits = int(params['Digits'])
            print(f"   - Digits: {order.Digits}")
        if 'DigitsCurrency' in params:
            order.DigitsCurrency = int(params['DigitsCurrency'])
            print(f"   - DigitsCurrency: {order.DigitsCurrency}")
        if 'ContractSize' in params:
            order.ContractSize = int(params['ContractSize'])
            print(f"   - ContractSize: {order.ContractSize}")
        if 'VolumeInitial' in params:
            try:
                volume = int(params['VolumeInitial'])
                if volume <= 0:
                    raise ValueError("Volume must be positive")
                order.VolumeInitial = volume
                print(f"   - VolumeInitial: {order.VolumeInitial}")
            except (ValueError, OverflowError, TypeError):
                raise ValueError("Volume must be positive")
        if 'VolumeCurrent' in params:
            try:
                volume = int(params['VolumeCurrent'])
                if volume <= 0:
                    raise ValueError("Volume must be positive")
                order.VolumeCurrent = volume
                print(f"   - VolumeCurrent: {order.VolumeCurrent}")
            except (ValueError, OverflowError, TypeError):
                raise ValueError("Volume must be positive")
        if 'PriceOrder' in params:
            order.PriceOrder = float(params['PriceOrder'])
            print(f"   - PriceOrder: {order.PriceOrder}")
        if 'State' in params:
            order.State = int(params['State'])
            print(f"   - State: {order.State}")
        
        # get current timestamp
        time = datetime.now()
        order.TimeSetupMsc = MT5OrderHelper.convert_to_server_time(time, server_id, server_type) * 1000

        # Add order to server
        print("\n5. Adding order to server")
        result = connection.manager.OrderAdd(order)
        if not result:
            error = MT5Manager.LastError()
            raise MT5ConnectionError(f"Failed to add order: {error}")
        
        print("6. Order added successfully")
        print("=== End Debug ===\n")
        
        return order
            
    except ValueError:
        raise
    except Exception as e:
        print(f"\n=== MT5 Error Debug ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        error = MT5Manager.LastError()
        print(f"MT5 Last Error: {error}")
        print("=== End Error Debug ===\n")
        raise MT5ConnectionError(f"Failed to add order: {str(e)}")

  @staticmethod
  async def delete(
      ticket: int,
      server_id=None,
      server_type=None
  ) -> bool:
      """
      Delete a trade order
      
      Args:
          ticket: Order ticket number
          server_id: Optional server ID
          server_type: Optional server type ('demo' or 'live')
          
      Returns:
          bool: True if order was successfully deleted
          
      Raises:
          ValueError: If ticket is invalid
          MT5ConnectionError: If deletion fails or connection error occurs
          
      Note:
          - Order can only be deleted from applications connected to the trade server
            where the order was created
          - Requires RIGHT_TRADE_DELETE and RIGHT_TRADES_MANAGER permissions
      """
      if not isinstance(ticket, int) or ticket <= 0:
          raise ValueError("Ticket must be a positive integer")
            
      connection = MT5OrderHelper.get_connection(server_id, server_type)
      if not connection or not connection.manager:
          raise MT5ConnectionError("MT5 connection or manager not available")
            
      try:
          print(f"\n=== MT5 Order Delete Debug ===")
          print(f"1. Connection state: connected={connection._connected}")
          print(f"2. Manager instance available: {connection.manager is not None}")
          print(f"3. Attempting to delete order ticket: {ticket}")
            
          result = connection.manager.OrderDelete(ticket)
          if not result:
              error = MT5Manager.LastError()
              if error == MT5Manager.MT_RET_ERR_NOTMAIN:
                  raise MT5ConnectionError("Order can only be deleted from the server where it was created")
              elif error == MT5Manager.MT_RET_ERR_NOTFOUND:
                  raise MT5ConnectionError(f"Order with ticket {ticket} not found")
              else:
                  raise MT5ConnectionError(f"Failed to delete order: {error}")
            
          print("4. Order deleted successfully")
          print("=== End Debug ===\n")
            
          return True
            
      except Exception as e:
          print(f"\n=== MT5 Error Debug ===")
          print(f"Error type: {type(e).__name__}")
          print(f"Error message: {str(e)}")
          error = MT5Manager.LastError()
          print(f"MT5 Last Error: {error}")
          print("=== End Error Debug ===\n")
          raise MT5ConnectionError(f"Failed to delete order: {str(e)}")