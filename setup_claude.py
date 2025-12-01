"""
Automatic Claude Desktop setup for MCP client
Script automatically finds Claude Desktop config and adds MCP server
"""
import json
import os
import sys
import platform
from pathlib import Path


def get_claude_config_path() -> Path:
    """Determine path to Claude Desktop config depending on OS"""
    system = platform.system()
    
    if system == "Windows":
        # Windows: %APPDATA%\Claude\claude_desktop_config.json
        appdata = os.getenv("APPDATA")
        if not appdata:
            raise ValueError("APPDATA environment variable not found")
        return Path(appdata) / "Claude" / "claude_desktop_config.json"
    
    elif system == "Darwin":
        # macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    
    elif system == "Linux":
        # Linux: ~/.config/Claude/claude_desktop_config.json
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    
    else:
        raise ValueError(f"Unsupported operating system: {system}")


def get_python_path() -> str:
    """Get path to Python in virtual environment"""
    # Check if script is running in venv
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # We are in venv
        if platform.system() == "Windows":
            python_path = Path(sys.prefix) / "Scripts" / "python.exe"
        else:
            python_path = Path(sys.prefix) / "bin" / "python"
        
        return str(python_path.resolve())
    else:
        # Not in venv, use current Python
        print("⚠️  Warning: Not running in a virtual environment")
        print("   It's recommended to use venv for isolation")
        return sys.executable


def get_mcp_client_path() -> str:
    """Get path to mcp_client.py"""
    script_dir = Path(__file__).parent.resolve()
    client_path = script_dir / "mcp_client.py"
    
    if not client_path.exists():
        raise FileNotFoundError(f"mcp_client.py not found at {client_path}")
    
    return str(client_path)


def load_or_create_config(config_path: Path) -> dict:
    """Load existing config or create new one"""
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ Loaded existing config from {config_path}")
            return config
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Failed to parse existing config: {e}")
            print("   Creating backup and starting fresh")
            # Create backup
            backup_path = config_path.with_suffix('.json.backup')
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    with open(backup_path, 'w', encoding='utf-8') as bf:
                        bf.write(f.read())
                print(f"   Backup saved to {backup_path}")
            return {"mcpServers": {}}
    else:
        print(f"ℹ️  Config file doesn't exist, will create new one")
        # Create directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)
        return {"mcpServers": {}}


def add_mcp_server(config: dict, python_path: str, client_path: str) -> dict:
    """Add MCP server to config"""
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Check if configuration already exists
    if "vulnerabilities" in config["mcpServers"]:
        print("⚠️  Warning: 'vulnerabilities' MCP server already exists in config")
        response = input("   Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("   Keeping existing configuration")
            return config
    
    # Add or update configuration
    config["mcpServers"]["vulnerabilities"] = {
        "command": python_path,
        "args": [client_path],
        "env": {}
    }
    
    print("✅ Added 'vulnerabilities' MCP server to config")
    return config


def save_config(config_path: Path, config: dict):
    """Save config"""
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ Config saved to {config_path}")


def verify_env_file():
    """Verify .env file exists"""
    env_path = Path(__file__).parent / ".env"
    env_example_path = Path(__file__).parent / ".env.example"
    
    if not env_path.exists():
        print("\n⚠️  Warning: .env file not found")
        if env_example_path.exists():
            print("   Please copy .env.example to .env and configure it:")
            print(f"   cp {env_example_path} {env_path}")
        else:
            print("   Please create .env file with your API credentials:")
            print("   API_KEY=sk_your_api_key_here")
            print("   API_URL=https://yourdomain.com")
        return False
    
    # Check .env file contents
    with open(env_path, 'r') as f:
        content = f.read()
    
    has_api_key = 'API_KEY=' in content or 'MCP_API_KEY=' in content
    has_api_url = 'API_URL=' in content or 'MCP_API_URL=' in content
    
    if not has_api_key:
        print("\n⚠️  Warning: API_KEY not found in .env")
        return False
    
    if not has_api_url:
        print("\n⚠️  Warning: API_URL not found in .env")
        return False
    
    print("✅ .env file configured")
    return True


def main():
    """Main function"""
    print("=" * 60)
    print("Claude Desktop MCP Setup")
    print("=" * 60)
    print()
    
    try:
        # 1. Check .env file
        print("Step 1: Checking .env configuration...")
        env_ok = verify_env_file()
        print()
        
        # 2. Determine paths
        print("Step 2: Detecting paths...")
        config_path = get_claude_config_path()
        python_path = get_python_path()
        client_path = get_mcp_client_path()
        
        print(f"   Config path: {config_path}")
        print(f"   Python path: {python_path}")
        print(f"   Client path: {client_path}")
        print()
        
        # 3. Load config
        print("Step 3: Loading Claude Desktop config...")
        config = load_or_create_config(config_path)
        print()
        
        # 4. Add MCP server
        print("Step 4: Configuring MCP server...")
        config = add_mcp_server(config, python_path, client_path)
        print()
        
        # 5. Save config
        print("Step 5: Saving configuration...")
        save_config(config_path, config)
        print()
        
        # 6. Final message
        print("=" * 60)
        print("✅ Setup completed successfully!")
        print("=" * 60)
        print()
        
        if not env_ok:
            print("⚠️  Next steps:")
            print("   1. Configure your .env file with API credentials")
            print("   2. Restart Claude Desktop")
        else:
            print("Next steps:")
            print("   1. Restart Claude Desktop")
            print("   2. Open a new chat")
            print("   3. Ask: 'What tools do you have available?'")
            print("   4. Test: 'Search for reentrancy vulnerabilities'")
        
        print()
        print("If you encounter any issues:")
        print("   - Check Claude Desktop logs")
        print("   - Verify paths in the config are correct")
        print("   - Make sure .env file is configured")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease configure Claude Desktop manually.")
        print("See README.md for instructions.")
        sys.exit(1)


if __name__ == "__main__":
    main()

