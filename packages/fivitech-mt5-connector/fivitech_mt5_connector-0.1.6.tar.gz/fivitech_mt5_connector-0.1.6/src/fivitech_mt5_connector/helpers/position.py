import MetaTrader5 as mt5
from typing import List, Optional, Dict, Any

class MT5PositionHelper:
    @staticmethod
    def get_positions(symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all positions or positions for a specific symbol."""
        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        else:
            positions = mt5.positions_get()
            
        if positions is None or len(positions) == 0:
            return []
            
        return [position._asdict() for position in positions]

    @staticmethod
    def get_position(ticket: int) -> Optional[Dict[str, Any]]:
        """Get position details by ticket number."""
        positions = mt5.positions_get(ticket=ticket)
        if positions is None or len(positions) == 0:
            return None
        return positions[0]._asdict()

    @staticmethod
    def close_position(ticket: int, volume: Optional[float] = None) -> bool:
        """Close a position by ticket number. Optionally specify volume for partial close."""
        position = MT5PositionHelper.get_position(ticket)
        if not position:
            return False

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": ticket,
            "symbol": position["symbol"],
            "volume": volume if volume else position["volume"],
            "type": mt5.ORDER_TYPE_SELL if position["type"] == 0 else mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(position["symbol"]).bid if position["type"] == 0 else mt5.symbol_info_tick(position["symbol"]).ask,
            "deviation": 20,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        return result.retcode == mt5.TRADE_RETCODE_DONE

    @staticmethod
    def modify_position(
        ticket: int,
        sl: Optional[float] = None,
        tp: Optional[float] = None
    ) -> bool:
        """Modify stop loss and/or take profit of an existing position."""
        position = MT5PositionHelper.get_position(ticket)
        if not position:
            return False

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": position["symbol"],
        }
        
        if sl is not None:
            request["sl"] = sl
        if tp is not None:
            request["tp"] = tp

        result = mt5.order_send(request)
        return result.retcode == mt5.TRADE_RETCODE_DONE 