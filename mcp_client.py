"""
Standalone MCP Server for integration with Claude Desktop
Uses REST API for searching vulnerabilities in smart contracts

This server is a lightweight client that communicates with a remote API
to get vulnerability search results.
"""
import os
import sys
import json
import asyncio
from typing import Any, Dict, Optional

import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

from config import Config


class VulnerabilitiesMCPClient:
    """MCP Client for searching vulnerabilities via REST API"""
    
    def __init__(self, api_key: str, api_url: str):
        """
        Initialize MCP client
        
        Args:
            api_key: API key for authentication
            api_url: API server URL
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.server = Server("vulnerabilities-mcp-client")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup MCP request handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Returns list of available tools"""
            return [
                Tool(
                    name="search_vulnerabilities",
                    description=(
                        "Search for smart contract vulnerabilities in the database. "
                        "Accepts Solidity code snippets or natural language descriptions of security issues. "
                        "Returns top 5 most relevant vulnerabilities with detailed information including "
                        "descriptions, code examples, and mitigation recommendations."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": (
                                    "Search query - can be Solidity code or natural language description "
                                    "of a vulnerability (e.g., 'reentrancy attack', 'integer overflow', "
                                    "'unchecked external call'). Minimum 3 characters."
                                ),
                                "minLength": 3,
                                "maxLength": 1000
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool call from Claude"""
            
            if name != "search_vulnerabilities":
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": f"Unknown tool: {name}"
                    })
                )]
            
            # Extract query from arguments
            query = arguments.get("query")
            if not query:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": "Missing required parameter: query"
                    })
                )]
            
            # Validate query
            if len(query) < 3:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": "Query must be at least 3 characters long"
                    })
                )]
            
            if len(query) > 1000:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": "Query must be at most 1000 characters long"
                    })
                )]
            
            try:
                # Execute search via REST API
                results = await self.search_vulnerabilities(query)
                
                # Format results for Claude
                return [TextContent(
                    type="text",
                    text=json.dumps(results, indent=2, ensure_ascii=False)
                )]
                
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": f"Error during search: {str(e)}"
                    })
                )]
    
    async def search_vulnerabilities(self, query: str) -> Dict[str, Any]:
        """
        Search vulnerabilities via REST API
        
        Args:
            query: Text query (Solidity code or vulnerability description)
        
        Returns:
            Dict with search results
        """
        url = f"{self.api_url}/api/v1/vulnerabilities/search"
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {"query": query}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                # Check response status
                if response.status_code == 401:
                    return {
                        "success": False,
                        "error": "Invalid API key. Please check your API key in the configuration."
                    }
                
                if response.status_code == 403:
                    return {
                        "success": False,
                        "error": "Quota exceeded. Please upgrade your plan or wait for quota reset."
                    }
                
                if response.status_code == 429:
                    return {
                        "success": False,
                        "error": "Rate limit exceeded. Please wait a moment and try again."
                    }
                
                if response.status_code != 200:
                    return {
                        "success": False,
                        "error": f"API error: {response.status_code} - {response.text}"
                    }
                
                # Parse JSON response
                data = response.json()
                
                # Format results for better readability
                if data.get("success"):
                    formatted_results = {
                        "success": True,
                        "summary": f"Found {data['total_unique_files']} unique vulnerabilities",
                        "total_found": data["total_unique_files"],
                        "top_results": []
                    }
                    
                    # Format top-5 results
                    for idx, vuln in enumerate(data.get("top_5", []), 1):
                        formatted_vuln = {
                            "rank": idx,
                            "title": vuln.get("title", "N/A"),
                            "severity": vuln.get("severity", "N/A"),
                            "final_score": vuln.get("final_score", 0),
                            "description": vuln.get("description", "N/A"),
                            "code_example": vuln.get("code_example", "N/A"),
                            "mitigation": vuln.get("mitigation", "N/A"),
                            "category": vuln.get("category", "N/A"),
                            "file_reference": vuln.get("original_json", "N/A"),
                            "relevance_scores": vuln.get("scores", []),
                            "found_in_collections": vuln.get("found_in_collections", [])
                        }
                        formatted_results["top_results"].append(formatted_vuln)
                    
                    # Add information about additional results
                    if data.get("top_6_10"):
                        formatted_results["additional_results_available"] = len(data["top_6_10"])
                        formatted_results["note"] = f"Found {len(data['top_6_10'])} more results (ranks 6-10)"
                    
                    return formatted_results
                else:
                    return data
                
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "Request timeout. The server took too long to respond."
            }
        except httpx.ConnectError:
            return {
                "success": False,
                "error": f"Connection error. Cannot connect to API server at {self.api_url}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    async def run(self):
        """Run MCP server via stdio"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Entry point for running MCP client"""
    
    # Load configuration
    try:
        config = Config.load()
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Please check your configuration:", file=sys.stderr)
        print("1. Copy .env.example to .env", file=sys.stderr)
        print("2. Edit .env and set your API_KEY and API_URL", file=sys.stderr)
        print("3. Get your API key from: https://yourdomain.com/dashboard", file=sys.stderr)
        sys.exit(1)
    
    # Print startup information
    print(f"✅ MCP Client starting...", file=sys.stderr)
    print(f"✅ API Server: {config.api_url}", file=sys.stderr)
    print(f"✅ API Key: {config.api_key[:10]}...", file=sys.stderr)
    print("", file=sys.stderr)
    
    # Create and run client
    client = VulnerabilitiesMCPClient(
        api_key=config.api_key,
        api_url=config.api_url
    )
    
    try:
        await client.run()
    except KeyboardInterrupt:
        print("\nMCP Client stopped by user", file=sys.stderr)
    except Exception as e:
        print(f"Error running MCP client: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

