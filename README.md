# Vulnerabilities MCP Client - Standalone Edition

Standalone MCP (Model Context Protocol) client for integrating smart contract vulnerability search directly into Claude Desktop.

This is a lightweight client that connects to a remote API server to perform vulnerability searches, allowing you to analyze Solidity code and find security issues right from your Claude Desktop chat.

---

## 🎯 What is This?

This MCP client allows you to:
- **Search for vulnerabilities** by Solidity code or natural language descriptions
- **Get detailed analysis** including severity, code examples, and mitigation strategies
- **Integrate seamlessly** with Claude Desktop for real-time security analysis

---

## 📋 Requirements

### System Requirements
- **Python 3.11 or higher**
- **Claude Desktop** (latest version)
- **Internet connection** (for API access)

### Get Your API Key
1. Visit the dashboard at: https://yourdomain.com/dashboard
2. Navigate to **API Keys** section
3. Click **"Create New API Key"**
4. Copy the key (it starts with `sk_`)

⚠️ **Important**: Save your API key securely - it's shown only once!

---

## 🎯 Supported Platforms

This MCP client works with any application supporting the Model Context Protocol:

- ✅ **Claude Desktop** (Anthropic)
- ✅ **Claude CLI** (Command Line Interface)
- ✅ **VS Code** (with Claude extension)
- ✅ **Cursor** (AI-powered editor)
- ✅ **Cline** (VS Code extension)
- ✅ **Any MCP-compatible AI client**

---

## 🚀 Quick Start

### Step 1: Download and Extract

Download this folder and extract it to a location on your computer:
```
Windows: C:\Users\YourName\mcp_server\
macOS:   /Users/yourname/mcp_server/
Linux:   /home/yourname/mcp_server/
```

### Step 2: Install Dependencies

Open a terminal in the `mcp_server` directory and run:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure

1. Copy the example configuration:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file and add your credentials:
   ```ini
   API_KEY=sk_your_api_key_here
   API_URL=https://yourdomain.com
   ```

### Step 4: Test the Client

Test if everything works:

**Windows:**
```bash
python mcp_client.py
```

**macOS/Linux:**
```bash
python3 mcp_client.py
```

You should see:
```
✅ MCP Client starting...
✅ API Server: https://yourdomain.com
✅ API Key: sk_abc123...
```

If you see errors, check your `.env` file configuration.

---

## 🔧 Platform Configuration

### Option 1: Claude Desktop

#### Automatic Setup (Recommended)

Run the setup script:

**Windows:**
```bash
python setup_claude.py
```

**macOS/Linux:**
```bash
python3 setup_claude.py
```

The script will automatically configure Claude Desktop for you.

#### Manual Setup

1. **Find Claude Desktop config file:**
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

2. **Edit the config file** and add the MCP server configuration:

**Windows example:**
```json
{
  "mcpServers": {
    "vulnerabilities": {
      "command": "C:\\Users\\YourName\\mcp_server\\venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourName\\mcp_server\\mcp_client.py"],
      "env": {}
    }
  }
}
```

**macOS/Linux example:**
```json
{
  "mcpServers": {
    "vulnerabilities": {
      "command": "/Users/yourname/mcp_server/venv/bin/python",
      "args": ["/Users/yourname/mcp_server/mcp_client.py"],
      "env": {}
    }
  }
}
```

⚠️ **Important**: 
- Use **absolute paths** to your Python executable and `mcp_client.py`
- On Windows, use double backslashes `\\` in paths
- Make sure the `.env` file is in the same directory as `mcp_client.py`

3. **Restart Claude Desktop**

---

### Option 2: Claude CLI

#### Installation

If you haven't installed Claude CLI yet:

```bash
npm install -g @anthropics/claude-cli
```

#### Configuration

Create or edit `.claude-cli-config.json` in your home directory:

**macOS/Linux:**
```bash
nano ~/.claude-cli-config.json
```

**Windows:**
```bash
notepad %USERPROFILE%\.claude-cli-config.json
```

Add the configuration:

```json
{
  "mcpServers": {
    "vulnerabilities": {
      "command": "/absolute/path/to/mcp_server/venv/bin/python",
      "args": ["/absolute/path/to/mcp_server/mcp_client.py"],
      "env": {}
    }
  }
}
```

**Windows example:**
```json
{
  "mcpServers": {
    "vulnerabilities": {
      "command": "C:\\Users\\YourName\\mcp_server\\venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourName\\mcp_server\\mcp_client.py"],
      "env": {}
    }
  }
}
```

#### Usage

Start Claude CLI with MCP:
```bash
claude --mcp-config ~/.claude-cli-config.json
```

Or if config is in the default location, just:
```bash
claude
```

---

### Option 3: VS Code (with Claude Extension)

#### Prerequisites

1. Install [Claude for VS Code](https://marketplace.visualstudio.com/items?itemName=Anthropic.claude-vscode) extension

#### Configuration

**Method 1: Through VS Code Settings UI**

1. Open VS Code Settings (`Cmd+,` / `Ctrl+,`)
2. Search for "Claude MCP"
3. Click "Edit in settings.json"
4. Add the configuration

**Method 2: Edit settings.json directly**

1. Open Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`)
2. Select: **Preferences: Open User Settings (JSON)**
3. Add the MCP server configuration:

```json
{
  "claude.mcpServers": {
    "vulnerabilities": {
      "command": "/absolute/path/to/mcp_server/venv/bin/python",
      "args": ["/absolute/path/to/mcp_server/mcp_client.py"],
      "env": {}
    }
  }
}
```

**Windows example:**
```json
{
  "claude.mcpServers": {
    "vulnerabilities": {
      "command": "C:\\Users\\YourName\\mcp_server\\venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourName\\mcp_server\\mcp_client.py"],
      "env": {}
    }
  }
}
```

4. Reload VS Code window

---

### Option 4: Cursor

#### Configuration

**Method 1: User Settings**

1. Open Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`)
2. Select: **Preferences: Open User Settings (JSON)**
3. Add the MCP configuration:

```json
{
  "cursor.mcpServers": {
    "vulnerabilities": {
      "command": "/absolute/path/to/mcp_server/venv/bin/python",
      "args": ["/absolute/path/to/mcp_server/mcp_client.py"],
      "env": {}
    }
  }
}
```

**Method 2: Project Settings**

Create `.cursor/mcp_servers.json` in your project root:

```json
{
  "vulnerabilities": {
    "command": "/absolute/path/to/mcp_server/venv/bin/python",
    "args": ["/absolute/path/to/mcp_server/mcp_client.py"],
    "env": {}
  }
}
```

**Windows example:**
```json
{
  "vulnerabilities": {
    "command": "C:\\Users\\YourName\\mcp_server\\venv\\Scripts\\python.exe",
    "args": ["C:\\Users\\YourName\\mcp_server\\mcp_client.py"],
    "env": {}
  }
}
```

#### Restart Cursor

After configuration, completely restart Cursor.

---

### Option 5: Cline (VS Code Extension)

#### Prerequisites

1. Install [Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) extension for VS Code

#### Configuration

1. Open VS Code Settings
2. Search for "Cline MCP"
3. Add MCP server in Cline settings:

```json
{
  "cline.mcpServers": {
    "vulnerabilities": {
      "command": "/absolute/path/to/mcp_server/venv/bin/python",
      "args": ["/absolute/path/to/mcp_server/mcp_client.py"],
      "env": {}
    }
  }
}
```

Or configure through Cline extension settings UI.

---

### Option 6: Other MCP-Compatible Clients

Any application supporting the Model Context Protocol can use this client.

**Generic Configuration Template:**

```json
{
  "mcpServers": {
    "vulnerabilities": {
      "command": "/path/to/python/executable",
      "args": ["/path/to/mcp_client.py"],
      "env": {}
    }
  }
}
```

**Key Points:**
- Use **absolute paths** for both `command` and `args`
- The `env` field should be empty `{}` (API key is in `.env` file)
- On Windows, use double backslashes: `C:\\Users\\...`

---

## ✅ Verify Installation

1. **Open Claude Desktop**

2. **Check available tools:**
   ```
   What tools do you have available?
   ```
   
   Claude should list `search_vulnerabilities` among available tools.

3. **Test search:**
   ```
   Search for reentrancy vulnerabilities
   ```

### For Claude CLI

1. **Start Claude CLI:**
   ```bash
   claude
   ```

2. **Check tools:**
   ```
   > What tools do you have available?
   ```

3. **Test search:**
   ```
   > Search for reentrancy vulnerabilities in smart contracts
   ```

### For VS Code / Cursor / Cline

1. **Open the AI chat panel**

2. **Ask about available tools:**
   ```
   What MCP tools are available?
   ```

3. **Test search:**
   ```
   Search for integer overflow vulnerabilities
   ```
   
   Or analyze code:
   ```
   Can you analyze this Solidity code for vulnerabilities?
   
   pragma solidity ^0.8.0;
   
   contract Vulnerable {
       mapping(address => uint) public balances;
       
       function withdraw() public {
           uint amount = balances[msg.sender];
           (bool success, ) = msg.sender.call{value: amount}("");
           require(success);
           balances[msg.sender] = 0;
       }
   }
   ```

---

## 💡 Usage Examples

### 1. Search by Vulnerability Type
```
Find vulnerabilities related to integer overflow
```

### 2. Search by Pattern
```
Search for unchecked external call vulnerabilities
```

### 3. Analyze Code
```
Analyze this withdraw function for security issues:

function withdraw(uint amount) public {
    require(balances[msg.sender] >= amount);
    msg.sender.call{value: amount}("");
    balances[msg.sender] -= amount;
}
```

### 4. General Security Questions
```
What are the most common reentrancy attack patterns in Solidity?
```

---

## 🔍 Troubleshooting

### "Configuration error: API_KEY is not set"

**Solution:**
1. Make sure `.env` file exists in the `mcp_server` directory
2. Check that it contains `API_KEY=sk_...`
3. Verify there are no spaces around the `=` sign

### "Connection error. Cannot connect to API server"

**Solution:**
1. Check your internet connection
2. Verify `API_URL` in `.env` is correct
3. Try accessing the URL in your browser: `https://yourdomain.com/api/v1/vulnerabilities/health`

### "Invalid API key"

**Solution:**
1. Check that your API key is correct and starts with `sk_`
2. Verify the key is still active in your dashboard
3. Try creating a new API key

### "Quota exceeded"

**Solution:**
1. Check your current quota in the dashboard
2. Wait for monthly quota reset (beginning of the month)
3. Upgrade to a higher plan if needed

### Platform doesn't see the MCP server

**Solution:**
1. Verify paths in configuration are **absolute** and correct
2. Check that Python path points to the venv Python (not system Python)
3. Make sure `.env` file is in the same directory as `mcp_client.py`
4. Restart the application completely
5. Check application logs:
   - **Claude Desktop:**
     - Windows: `%APPDATA%\Claude\logs\`
     - macOS: `~/Library/Logs/Claude/`
     - Linux: `~/.config/Claude/logs/`
   - **VS Code:** Open Developer Tools (`Help > Toggle Developer Tools`)
   - **Cursor:** Check console in Developer Tools
   - **Claude CLI:** Error messages appear in terminal

### ModuleNotFoundError

**Solution:**
```bash
# Activate venv and reinstall dependencies
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt --force-reinstall
```

---

## 🔐 Security Best Practices

### Protecting Your API Key

1. **Never commit `.env` to version control**
   - The `.gitignore` file already excludes it
   
2. **Don't share your API key**
   - Each user should have their own key
   
3. **Regularly rotate keys**
   - Create new keys periodically
   - Revoke old keys in the dashboard

4. **Monitor usage**
   - Check API usage in your dashboard
   - Set up alerts for unusual activity

### Secure Storage

- Store API keys in a password manager
- Don't include keys in screenshots or logs
- Don't send keys via email or chat

---

## 📊 API Limits

Each API call counts toward your monthly quota:

| Plan | Monthly Quota | Rate Limit |
|------|--------------|------------|
| Free | 100 requests | 10/min |
| Basic | 1,000 requests | 20/min |
| Pro | 10,000 requests | 50/min |
| Enterprise | Unlimited | Custom |

Check your current usage in the dashboard.

---

## 🆘 Support

### Getting Help

- **Documentation:** https://yourdomain.com/docs
- **API Status:** https://status.yourdomain.com
- **Support Email:** support@yourdomain.com

### Reporting Issues

When reporting issues, include:
1. Error message (remove your API key!)
2. Operating system and Python version
3. Claude Desktop version
4. Steps to reproduce the issue

---

## 🔄 Updating

To update the MCP client to the latest version:

```bash
cd mcp_server
git pull origin main  # if using git
pip install -r requirements.txt --upgrade
```

Restart Claude Desktop after updating.

---

## 📝 Configuration Reference

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `API_KEY` or `MCP_API_KEY` | ✅ Yes | Your API authentication key | `sk_abc123...` |
| `API_URL` or `MCP_API_URL` | ✅ Yes | API server URL | `https://yourdomain.com` |

### Claude Desktop Config

```json
{
  "mcpServers": {
    "vulnerabilities": {
      "command": "/path/to/venv/python",
      "args": ["/path/to/mcp_client.py"],
      "env": {}
    }
  }
}
```

**Notes:**
- `command`: Path to Python executable in your virtual environment
- `args`: Path to `mcp_client.py` script
- `env`: Additional environment variables (usually empty, as we use `.env` file)

---

## 🎓 Advanced Usage

### Using Custom API URL

For local development or custom deployments:

```ini
# .env
API_KEY=sk_your_key
API_URL=http://localhost:8000
```

### Multiple Environments

You can maintain multiple configurations:

```bash
# Development
cp .env .env.dev
# Production
cp .env .env.prod
```

Then switch by renaming:
```bash
cp .env.prod .env  # Use production config
```

### Debugging

Enable verbose logging by modifying `mcp_client.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📜 License

This MCP client is provided as-is for use with the vulnerability search API service.

---

## 🙏 Acknowledgments

- **Anthropic** for the Model Context Protocol
- **Claude Desktop** integration framework
- Vulnerability database providers

---

## 📞 Contact

For questions, support, or feedback:
- Website: https://yourdomain.com
- Email: support@yourdomain.com
- Documentation: https://yourdomain.com/docs

Happy secure coding! 🔒✨

