# Changelog

All notable changes to the Vulnerabilities MCP Client will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-19

### Added
- Initial release of standalone MCP client
- REST API integration for vulnerability search
- Configuration via environment variables (.env file)
- Automatic Claude Desktop setup script
- Comprehensive documentation (README, QUICKSTART, EXAMPLES)
- Support for Windows, macOS, and Linux
- Error handling and user-friendly error messages
- Formatted search results for better readability

### Features
- **search_vulnerabilities** tool for Claude Desktop
- Searches by code snippets or natural language descriptions
- Returns top 5 most relevant vulnerabilities with details
- Severity scoring and ranking
- Support for multiple vulnerability collections (BGE, UniXcoder)

### Documentation
- Detailed README with installation and troubleshooting
- Quick start guide for fast setup
- Usage examples and best practices
- API reference documentation

### Security
- API key authentication
- Secure credential storage via .env file
- .gitignore to prevent credential leaks

---

For more information, see the [README](README.md).

