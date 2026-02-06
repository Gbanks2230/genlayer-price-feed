# { "Depends": "py-genlayer:test" }
from genlayer import *
import json


class PriceFeedLibrary(gl.Contract):
    """
    A reusable price feed library for GenLayer Intelligent Contracts.
    
    Fetches real-time cryptocurrency and token prices from CoinGecko API.
    This can be imported and used by any Intelligent Contract that needs price data.
    """
    
    # Supported cryptocurrencies (can be extended)
    SUPPORTED_COINS = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "USDT": "tether",
        "USDC": "usd-coin",
        "BNB": "binancecoin",
        "XRP": "ripple",
        "ADA": "cardano",
        "DOGE": "dogecoin",
        "MATIC": "matic-network",
        "DOT": "polkadot",
        "AVAX": "avalanche-2",
        "LINK": "chainlink",
        "UNI": "uniswap",
        "ATOM": "cosmos"
    }
    
    # Cache for storing recent price data
    price_cache = {}
    last_update = {}
    
    def __init__(self):
        """Initialize the price feed library."""
        self.price_cache = {}
        self.last_update = {}
    
    @gl.public.view
    def get_price(self, symbol, currency="usd"):
        """
        Get the current price of a cryptocurrency.
        
        Args:
            symbol: Crypto symbol (e.g., "BTC", "ETH")
            currency: Target currency (default: "usd")
        
        Returns:
            dict: Price data including current price, 24h change, market cap
        """
        # Normalize symbol
        symbol = symbol.upper()
        currency = currency.lower()
        
        # Validate symbol
        if symbol not in self.SUPPORTED_COINS:
            return {
                "success": False,
                "error": f"Unsupported symbol: {symbol}",
                "supported_coins": list(self.SUPPORTED_COINS.keys())
            }
        
        # Get CoinGecko ID
        coin_id = self.SUPPORTED_COINS[symbol]
        
        # Fetch price from CoinGecko API using LLM
        try:
            prompt = f"""
            Fetch the current price data for {coin_id} from CoinGecko API.
            
            Use this API endpoint:
            https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}&include_24hr_change=true&include_market_cap=true
            
            Return ONLY a JSON object with this exact structure:
            {{
                "price": <current price as number>,
                "change_24h": <24 hour percentage change as number>,
                "market_cap": <market cap as number>
            }}
            
            Do not include any other text, explanations, or markdown formatting.
            """
            
            # Use LLM to fetch the data
            result = gl.exec_llm(prompt)
            
            # Parse the response
            price_data = json.loads(result)
            
            # Store in cache
            cache_key = f"{symbol}_{currency}"
            self.price_cache[cache_key] = price_data
            
            return {
                "success": True,
                "symbol": symbol,
                "currency": currency,
                "price": price_data.get("price"),
                "change_24h": price_data.get("change_24h"),
                "market_cap": price_data.get("market_cap"),
                "timestamp": "current"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to fetch price: {str(e)}",
                "symbol": symbol
            }
    
    @gl.public.view
    def get_multiple_prices(self, symbols, currency="usd"):
        """
        Get prices for multiple cryptocurrencies at once.
        
        Args:
            symbols: List of crypto symbols (e.g., ["BTC", "ETH", "SOL"])
            currency: Target currency (default: "usd")
        
        Returns:
            dict: Price data for all requested symbols
        """
        results = {}
        
        for symbol in symbols:
            price_data = self.get_price(symbol, currency)
            results[symbol] = price_data
        
        return {
            "success": True,
            "currency": currency,
            "count": len(results),
            "prices": results
        }
    
    @gl.public.view
    def compare_prices(self, symbol1, symbol2):
        """
        Compare prices of two cryptocurrencies.
        
        Args:
            symbol1: First crypto symbol
            symbol2: Second crypto symbol
        
        Returns:
            dict: Comparison data
        """
        price1_data = self.get_price(symbol1)
        price2_data = self.get_price(symbol2)
        
        if not price1_data.get("success") or not price2_data.get("success"):
            return {
                "success": False,
                "error": "Failed to fetch one or both prices"
            }
        
        price1 = price1_data.get("price", 0)
        price2 = price2_data.get("price", 0)
        
        ratio = price1 / price2 if price2 > 0 else 0
        
        return {
            "success": True,
            "comparison": f"{symbol1}/{symbol2}",
            "symbol1": symbol1,
            "price1": price1,
            "symbol2": symbol2,
            "price2": price2,
            "ratio": ratio,
            "higher": symbol1 if price1 > price2 else symbol2
        }
    
    @gl.public.view
    def get_supported_coins(self):
        """
        Get list of all supported cryptocurrencies.
        
        Returns:
            dict: List of supported symbols
        """
        return {
            "success": True,
            "count": len(self.SUPPORTED_COINS),
            "supported_coins": list(self.SUPPORTED_COINS.keys())
        }
    
    @gl.public.view
    def is_price_above(self, symbol, threshold, currency="usd"):
        """
        Check if a cryptocurrency price is above a certain threshold.
        Useful for alerts and conditional logic.
        
        Args:
            symbol: Crypto symbol
            threshold: Price threshold
            currency: Target currency
        
        Returns:
            dict: Comparison result
        """
        price_data = self.get_price(symbol, currency)
        
        if not price_data.get("success"):
            return price_data
        
        current_price = price_data.get("price", 0)
        is_above = current_price > threshold
        
        return {
            "success": True,
            "symbol": symbol,
            "current_price": current_price,
            "threshold": threshold,
            "is_above": is_above,
            "difference": current_price - threshold,
            "percentage_diff": ((current_price - threshold) / threshold * 100) if threshold > 0 else 0
        }
