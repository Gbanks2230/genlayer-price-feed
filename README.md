# 📊 GenLayer Price Feed Library

A reusable, open-source library for GenLayer Intelligent Contracts to fetch real-time cryptocurrency prices from external APIs.

[![GenLayer](https://img.shields.io/badge/Built%20on-GenLayer-purple)](https://genlayer.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-live-success)](https://studio.genlayer.com)

## 🎯 What Is This?

This is a **price feed infrastructure library** that allows any GenLayer Intelligent Contract to:
- ✅ Get real-time cryptocurrency prices
- ✅ Track portfolio values
- ✅ Set price alerts
- ✅ Compare token prices
- ✅ Build DeFi applications

**No API keys needed. No complex setup. Just deploy and use.**

## 🚀 Live Deployment

- **Library Contract**: `[0xbe62567d50eb5850f4f68b90a0d5bd68f713946e54ff5b0f7fd50d6141904e32]`
- **Example Contract**: `[0x3fafea1457774d98120e0a7263766928fcd6cb46778bddb5f877e73b408d7ecb]`
- **Network**: GenLayer Testnet
- **Try it**: [GenLayer Studio](https://studio.genlayer.com)

## ⚡ Quick Start

### For Users (No Coding Required)

1. Go to [GenLayer Studio](https://studio.genlayer.com)
2. Connect your wallet
3. Paste the example contract address: `[0x3fafea1457774d98120e0a7263766928fcd6cb46778bddb5f877e73b408d7ecb]`
4. Try these methods:
   - `check_btc_price()` - Get current Bitcoin price
   - `check_portfolio_value({"BTC": 0.5, "ETH": 2})` - Calculate portfolio
   - `set_price_alert("BTC", 100000, "above")` - Set price alert

### For Developers

```python
# In your Intelligent Contract:
from genlayer import *

class MyContract(gl.Contract):
    price_feed_address = "0xbe62567d50eb5850f4f68b90a0d5bd68f713946e54ff5b0f7fd50d6141904e32"
    
    @gl.public.view
    def get_btc_price(self):
        # Call the price feed library
        result = gl.call_contract(
            self.price_feed_address,
            "get_price",
            ["BTC", "usd"]
        )
        
        return f"BTC Price: ${result['price']:,.2f}"
```

## 📋 Features

### Price Feed Library (`price_feed_library.py`)

| Method | Description | Parameters |
|--------|-------------|------------|
| `get_price()` | Get current price of a cryptocurrency | `symbol, currency` |
| `get_multiple_prices()` | Get prices for multiple coins | `symbols[], currency` |
| `compare_prices()` | Compare two cryptocurrencies | `symbol1, symbol2` |
| `is_price_above()` | Check if price exceeds threshold | `symbol, threshold, currency` |
| `get_supported_coins()` | List all supported coins | None |

### Example Contract (`price_feed_example.py`)

| Method | Description | Parameters |
|--------|-------------|------------|
| `check_btc_price()` | Get current Bitcoin price | None |
| `check_portfolio_value()` | Calculate total portfolio value | `holdings{}` |
| `set_price_alert()` | Set a price alert | `symbol, threshold, type` |
| `check_alerts()` | Check triggered alerts | None |
| `should_buy_signal()` | Simple trading signal | `symbol, ma_threshold` |

## 💎 Supported Cryptocurrencies

Currently supports 15+ major cryptocurrencies:

- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)
- Cardano (ADA)
- Polkadot (DOT)
- Avalanche (AVAX)
- Chainlink (LINK)
- Uniswap (UNI)
- Cosmos (ATOM)
- BNB, XRP, DOGE, MATIC, USDT, USDC

*More coins can be easily added!*

## 📖 Usage Examples

### Example 1: Get Current Price

```python
# Get Bitcoin price in USD
result = get_price("BTC", "usd")

# Returns:
{
    "success": true,
    "symbol": "BTC",
    "price": 98750.50,
    "change_24h": 2.5,
    "market_cap": 1950000000000
}
```

### Example 2: Track Portfolio

```python
# Calculate portfolio value
holdings = {
    "BTC": 0.5,
    "ETH": 2,
    "SOL": 10
}

result = check_portfolio_value(holdings)

# Returns:
{
    "total_value_usd": 52875.25,
    "breakdown": {
        "BTC": {"amount": 0.5, "price": 98750, "value": 49375},
        "ETH": {"amount": 2, "price": 1500, "value": 3000},
        "SOL": {"amount": 10, "price": 50.025, "value": 500.25}
    }
}
```

### Example 3: Set Price Alert

```python
# Alert when BTC goes above $100k
set_price_alert("BTC", 100000, "above")

# Later, check if triggered
check_alerts()
```

### Example 4: Compare Cryptocurrencies

```python
# Compare BTC vs ETH
result = compare_prices("BTC", "ETH")

# Returns:
{
    "comparison": "BTC/ETH",
    "price1": 98750,
    "price2": 1500,
    "ratio": 65.83,
    "higher": "BTC"
}
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         Your Intelligent Contract           │
│  (DeFi app, game, prediction market, etc)  │
└─────────────────┬───────────────────────────┘
                  │
                  │ gl.call_contract()
                  │
                  ↓
┌─────────────────────────────────────────────┐
│       Price Feed Library Contract           │
│        (price_feed_library.py)              │
└─────────────────┬───────────────────────────┘
                  │
                  │ gl.exec_llm()
                  │
                  ↓
┌─────────────────────────────────────────────┐
│         CoinGecko API (via LLM)            │
│        Real-time price data                 │
└─────────────────────────────────────────────┘
```

## 🛠️ Installation & Deployment

### Deploy the Library

1. Go to [GenLayer Studio](https://studio.genlayer.com)
2. Upload `price_feed_library.py`
3. No constructor arguments needed
4. Click **Deploy**
5. Copy the contract address

### Deploy the Example

1. Upload `price_feed_example.py`
2. Constructor argument: `<0xbe62567d50eb5850f4f68b90a0d5bd68f713946e54ff5b0f7fd50d6141904e32>`
3. Click **Deploy**
4. Start using it!

### Use in Your Own Contract

```python
# { "Depends": "py-genlayer:test" }
from genlayer import *

class MyDeFiApp(gl.Contract):
    price_feed = "0xbe62567d50eb5850f4f68b90a0d5bd68f713946e54ff5b0f7fd50d6141904e32"
    
    @gl.public.view
    def my_function(self):
        # Use the price feed
        btc_data = gl.call_contract(
            self.price_feed,
            "get_price",
            ["BTC", "usd"]
        )
        
        # Your logic here
        return btc_data
```

## 💡 Use Cases

This library enables you to build:

- 📈 **DeFi Apps** - Lending, borrowing, swaps
- 🎮 **Games** - In-game economies with real prices
- 🔮 **Prediction Markets** - Bet on price movements
- 💰 **Portfolio Trackers** - Monitor holdings on-chain
- 🚨 **Alert Systems** - Get notified on price changes
- 🤖 **Trading Bots** - Automated trading strategies
- 💎 **NFT Pricing** - Dynamic NFT prices based on crypto
- 📊 **Analytics Dashboards** - On-chain price analytics

## 🔐 Security

- ✅ No API keys stored in contracts
- ✅ Uses GenLayer's LLM for secure API calls
- ✅ Price data verified through consensus
- ✅ Open source and auditable
- ✅ Read-only operations for price fetching

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Add More Coins

Edit the `SUPPORTED_COINS` dictionary in `price_feed_library.py`:

```python
SUPPORTED_COINS = {
    "NEWCOIN": "coingecko-id",
    # Add more here
}
```

### Add More Features

- Historical price data
- Price charts
- Multiple currency support (EUR, GBP, etc.)
- Custom price formulas
- Volatility indicators

### Submit Pull Requests

1. Fork the repo
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on [GenLayer](https://genlayer.com)
- Price data from [CoinGecko API](https://www.coingecko.com)
- Inspired by Chainlink Price Feeds

## 📞 Support

- **Issues**: [GitHub Issues](../../issues)
- **GenLayer Discord**: [Join Here](https://discord.gg/genlayer)
- **Documentation**: [GenLayer Docs](https://docs.genlayer.com)

## 🔗 Links

- [GenLayer Website](https://genlayer.com)
- [GenLayer Studio](https://studio.genlayer.com)
- [CoinGecko API](https://www.coingecko.com/en/api)

## 📊 Stats

- **Supported Coins**: 15+
- **Methods**: 5 core + 5 example
- **Dependencies**: GenLayer only
- **Lines of Code**: ~400
- **Gas Efficient**: Optimized calls

## 🎯 Roadmap

- [x] Basic price fetching
- [x] Multiple coin support
- [x] Price alerts
- [x] Portfolio tracking
- [ ] Historical data
- [ ] Price predictions (AI)
- [ ] Multi-currency support
- [ ] Websocket support
- [ ] Price charts
- [ ] Custom indicators

---

<div align="center">

**Built with ❤️ for the GenLayer Community**

⭐ Star this repo if you find it useful!

[Donate](#) • [Follow on X](https://twitter.com/Gbanks2230)

</Gbanks2230>
