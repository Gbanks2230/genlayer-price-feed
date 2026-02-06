# { "Depends": "py-genlayer:test" }
from genlayer import *


class PriceFeedExample(gl.Contract):
    """
    Example contract demonstrating how to use the PriceFeed Library.
    
    This shows practical use cases like:
    - Price alerts
    - Portfolio tracking
    - Conditional actions based on prices
    """
    
    # Store the price feed library address
    price_feed_address = None
    
    # User alerts
    user_alerts = {}
    
    def __init__(self, price_feed_address):
        """
        Initialize with the PriceFeed library address.
        
        Args:
            price_feed_address: Address of deployed PriceFeedLibrary contract
        """
        self.price_feed_address = price_feed_address
        self.user_alerts = {}
    
    @gl.public.view
    def check_btc_price(self):
        """
        Simple example: Get current Bitcoin price.
        """
        # Call the price feed library
        result = gl.call_contract(
            self.price_feed_address,
            "get_price",
            ["BTC", "usd"]
        )
        
        return {
            "message": f"Current BTC price: ${result['price']:,.2f}",
            "data": result
        }
    
    @gl.public.view
    def check_portfolio_value(self, holdings):
        """
        Calculate total portfolio value based on current prices.
        
        Args:
            holdings: Dict of symbol -> amount (e.g., {"BTC": 0.5, "ETH": 2})
        
        Returns:
            dict: Portfolio value and breakdown
        """
        total_value = 0
        breakdown = {}
        
        for symbol, amount in holdings.items():
            # Get current price
            price_data = gl.call_contract(
                self.price_feed_address,
                "get_price",
                [symbol, "usd"]
            )
            
            if price_data.get("success"):
                price = price_data.get("price", 0)
                value = price * amount
                total_value += value
                
                breakdown[symbol] = {
                    "amount": amount,
                    "price": price,
                    "value": value
                }
        
        return {
            "total_value_usd": total_value,
            "breakdown": breakdown,
            "currency": "USD"
        }
    
    @gl.public.write
    def set_price_alert(self, symbol, threshold, alert_type="above"):
        """
        Set a price alert for a cryptocurrency.
        
        Args:
            symbol: Crypto symbol (e.g., "BTC")
            threshold: Price threshold
            alert_type: "above" or "below"
        """
        user = str(gl.message.sender_address)
        
        if user not in self.user_alerts:
            self.user_alerts[user] = []
        
        alert = {
            "symbol": symbol,
            "threshold": threshold,
            "type": alert_type,
            "active": True
        }
        
        self.user_alerts[user].append(alert)
        
        return {
            "success": True,
            "message": f"Alert set: {symbol} {alert_type} ${threshold}",
            "alert": alert
        }
    
    @gl.public.view
    def check_alerts(self):
        """
        Check if any user alerts have been triggered.
        """
        user = str(gl.message.sender_address)
        
        if user not in self.user_alerts:
            return {
                "success": True,
                "message": "No alerts set",
                "triggered_alerts": []
            }
        
        triggered = []
        
        for alert in self.user_alerts[user]:
            if not alert.get("active"):
                continue
            
            # Check current price
            result = gl.call_contract(
                self.price_feed_address,
                "is_price_above",
                [alert["symbol"], alert["threshold"], "usd"]
            )
            
            if result.get("success"):
                is_above = result.get("is_above")
                current_price = result.get("current_price")
                
                # Check if alert should trigger
                should_trigger = False
                if alert["type"] == "above" and is_above:
                    should_trigger = True
                elif alert["type"] == "below" and not is_above:
                    should_trigger = True
                
                if should_trigger:
                    triggered.append({
                        "symbol": alert["symbol"],
                        "threshold": alert["threshold"],
                        "current_price": current_price,
                        "type": alert["type"]
                    })
        
        return {
            "success": True,
            "triggered_count": len(triggered),
            "triggered_alerts": triggered
        }
    
    @gl.public.view
    def should_buy_signal(self, symbol, ma_threshold):
        """
        Simple buy signal: Check if price is below moving average threshold.
        This is a simplified example - real trading would need more data.
        
        Args:
            symbol: Crypto symbol
            ma_threshold: Price threshold representing moving average
        
        Returns:
            dict: Buy signal recommendation
        """
        price_data = gl.call_contract(
            self.price_feed_address,
            "get_price",
            [symbol, "usd"]
        )
        
        if not price_data.get("success"):
            return price_data
        
        current_price = price_data.get("price", 0)
        change_24h = price_data.get("change_24h", 0)
        
        # Simple logic: Buy if price is below MA and showing positive momentum
        should_buy = current_price < ma_threshold and change_24h > 0
        
        return {
            "success": True,
            "symbol": symbol,
            "current_price": current_price,
            "ma_threshold": ma_threshold,
            "change_24h": change_24h,
            "should_buy": should_buy,
            "reason": "Price below MA with positive momentum" if should_buy else "Conditions not met"
        }
