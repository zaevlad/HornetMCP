# Quick Start Guide

Get up and running with the Vulnerabilities MCP Client in 5 minutes!

## 🚀 Installation (3 steps)

### 1. Install Python Dependencies

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Credentials

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```ini
API_KEY=sk_your_api_key_here
API_URL=https://yourdomain.com
```

💡 Get your API key from: https://yourdomain.com/dashboard

### 3. Setup Claude Desktop

Run the automatic setup:
```bash
python setup_claude.py
```

Or configure manually (see README.md).

## ✅ Test Installation

Restart Claude Desktop and try:

```
Search for reentrancy vulnerabilities in smart contracts
```

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [EXAMPLES.md](EXAMPLES.md) for usage examples
- Join our community for support

## 🆘 Troubleshooting

**Issue:** Claude doesn't see the tool  
**Fix:** Restart Claude Desktop and check the config paths are absolute

**Issue:** "Invalid API key"  
**Fix:** Verify your API key in `.env` starts with `sk_`

**Issue:** Connection error  
**Fix:** Check `API_URL` in `.env` and your internet connection

For more help, see the [Troubleshooting section](README.md#-troubleshooting) in README.md

