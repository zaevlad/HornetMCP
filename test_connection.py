"""
Test script to verify MCP client connection and API functionality

This script helps you test your configuration before integrating with Claude Desktop.
"""
import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from mcp_client import VulnerabilitiesMCPClient


async def test_configuration():
    """Test configuration loading"""
    print("=" * 60)
    print("Step 1: Testing Configuration")
    print("=" * 60)
    
    try:
        config = Config.load()
        print("✅ Configuration loaded successfully")
        print(f"   API URL: {config.api_url}")
        print(f"   API Key: {config.api_key[:10]}..." + ("*" * 20))
        return config
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease check:")
        print("1. .env file exists in the same directory")
        print("2. API_KEY and API_URL are set correctly")
        print("3. API_KEY starts with 'sk_'")
        return None


async def test_api_connection(config: Config):
    """Test API connection"""
    print("\n" + "=" * 60)
    print("Step 2: Testing API Connection")
    print("=" * 60)
    
    client = VulnerabilitiesMCPClient(
        api_key=config.api_key,
        api_url=config.api_url
    )
    
    # Test with a simple query
    test_query = "reentrancy attack"
    print(f"\nSending test query: '{test_query}'")
    print("Please wait...")
    
    try:
        result = await client.search_vulnerabilities(test_query)
        
        if result.get("success"):
            print("✅ API connection successful!")
            print(f"   Found {result.get('total_found', 0)} vulnerabilities")
            
            if result.get("top_results"):
                print("\n   First result:")
                first = result["top_results"][0]
                print(f"   - Title: {first.get('title', 'N/A')}")
                print(f"   - Severity: {first.get('severity', 'N/A')}")
                print(f"   - Score: {first.get('final_score', 0)}")
            
            return True
        else:
            error = result.get("error", "Unknown error")
            print(f"❌ API returned error: {error}")
            
            if "Invalid API key" in error:
                print("\nTroubleshooting:")
                print("- Check that your API key is correct")
                print("- Verify the key is active in your dashboard")
                print("- Try creating a new API key")
            elif "Quota exceeded" in error:
                print("\nTroubleshooting:")
                print("- Check your quota in the dashboard")
                print("- Wait for monthly quota reset")
                print("- Upgrade to a higher plan")
            elif "Connection error" in error:
                print("\nTroubleshooting:")
                print("- Check your internet connection")
                print("- Verify the API_URL is correct")
                print("- Try accessing the API URL in your browser")
            
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


async def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("MCP Client Connection Test")
    print("=" * 60 + "\n")
    
    # Step 1: Test configuration
    config = await test_configuration()
    if not config:
        print("\n" + "=" * 60)
        print("❌ Test Failed: Configuration Error")
        print("=" * 60)
        sys.exit(1)
    
    # Step 2: Test API connection
    success = await test_api_connection(config)
    
    # Final results
    print("\n" + "=" * 60)
    if success:
        print("✅ All Tests Passed!")
        print("=" * 60)
        print("\nYour MCP client is ready to use with Claude Desktop!")
        print("\nNext steps:")
        print("1. Run: python setup_claude.py")
        print("2. Restart Claude Desktop")
        print("3. Ask Claude: 'What tools do you have available?'")
    else:
        print("❌ Tests Failed")
        print("=" * 60)
        print("\nPlease fix the errors above and try again.")
        print("For more help, see README.md or contact support.")
        sys.exit(1)
    
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        sys.exit(1)

