# Usage Examples

Real-world examples of using the Vulnerabilities MCP Client with Claude Desktop.

---

## 🔍 Search Examples

### Example 1: Search by Vulnerability Type

**You:**
```
Search for reentrancy vulnerabilities in smart contracts
```

**Claude (using search_vulnerabilities):**
```json
{
  "success": true,
  "summary": "Found 15 unique vulnerabilities",
  "total_found": 15,
  "top_results": [
    {
      "rank": 1,
      "title": "Reentrancy in Withdraw Function",
      "severity": "High",
      "final_score": 1.2534,
      "description": "The contract is vulnerable to reentrancy attacks...",
      "code_example": "...",
      "mitigation": "Use checks-effects-interactions pattern..."
    }
  ]
}
```

**Claude's Analysis:**
> I found 15 reentrancy vulnerabilities in the database. The most critical one is a reentrancy attack in the withdraw function with a severity of "High"...

---

### Example 2: Analyze Specific Code

**You:**
```
Can you analyze this Solidity code for vulnerabilities?

pragma solidity ^0.8.0;

contract Bank {
    mapping(address => uint) public balances;
    
    function withdraw() public {
        uint amount = balances[msg.sender];
        require(amount > 0, "No balance");
        
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        balances[msg.sender] = 0;
    }
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
}
```

**Claude's Response:**
> Let me search for similar vulnerabilities...
>
> [Uses search_vulnerabilities with the code]
>
> I found a critical reentrancy vulnerability in your code. The issue is in the `withdraw()` function:
>
> **Problem:** You're updating the balance AFTER the external call, which allows an attacker to recursively call `withdraw()` before the balance is set to 0.
>
> **Fix:**
> ```solidity
> function withdraw() public {
>     uint amount = balances[msg.sender];
>     require(amount > 0, "No balance");
>     
>     balances[msg.sender] = 0;  // Update state BEFORE external call
>     
>     (bool success, ) = msg.sender.call{value: amount}("");
>     require(success, "Transfer failed");
> }
> ```

---

### Example 3: Search by Pattern

**You:**
```
Find vulnerabilities related to integer overflow in token contracts
```

**Claude (using search_vulnerabilities):**
```json
{
  "success": true,
  "summary": "Found 8 unique vulnerabilities",
  "top_results": [
    {
      "rank": 1,
      "title": "Integer Overflow in Transfer",
      "severity": "Medium",
      "code_example": "balances[to] += amount; // Can overflow",
      "mitigation": "Use SafeMath library or Solidity 0.8.0+..."
    }
  ]
}
```

---

### Example 4: General Security Question

**You:**
```
What are the most common security vulnerabilities in Solidity smart contracts?
```

**Claude:**
> Let me search for common vulnerability patterns...
>
> [Uses search_vulnerabilities multiple times]
>
> Based on the vulnerability database, here are the most common security issues:
>
> 1. **Reentrancy Attacks** (High Severity)
>    - Most common in withdrawal functions
>    - Fix: Use checks-effects-interactions pattern
>
> 2. **Integer Overflow/Underflow** (Medium Severity)
>    - Common in arithmetic operations
>    - Fix: Use SafeMath or Solidity 0.8.0+
>
> 3. **Unchecked External Calls** (High Severity)
>    - Ignoring return values
>    - Fix: Always check return values or use transfer()
>
> [Continues with more details...]

---

## 🎯 Advanced Examples

### Example 5: Multi-Step Analysis

**You:**
```
I'm building a DeFi lending protocol. Can you help me identify potential security issues?
```

**Claude:**
> I'll help you analyze common security issues in DeFi lending protocols. Let me search for relevant vulnerabilities...
>
> [Performs multiple searches:]
> - "lending protocol vulnerabilities"
> - "flash loan attacks"
> - "price oracle manipulation"
> - "collateral calculation overflow"
>
> Here's what you need to watch out for:
>
> **1. Flash Loan Attacks**
> [Shows relevant vulnerability with code example]
>
> **2. Price Oracle Manipulation**
> [Shows relevant vulnerability with code example]
>
> **3. Rounding Errors in Interest Calculation**
> [Shows relevant vulnerability with code example]
>
> Would you like me to review your specific contract code?

---

### Example 6: Code Review Session

**You:**
```
Review this NFT marketplace contract for security issues:

[Paste your contract code]
```

**Claude:**
> Let me analyze your contract systematically...
>
> [Searches for multiple vulnerability types:]
> - Reentrancy in payment functions
> - Access control issues
> - Front-running vulnerabilities
> - Integer overflow in pricing
>
> **Found Issues:**
>
> 1. ❌ **Critical: Reentrancy in buyNFT()** (Line 45)
>    - [Explanation with fix]
>
> 2. ⚠️ **High: Missing Access Control** (Line 78)
>    - [Explanation with fix]
>
> 3. ⚠️ **Medium: Front-running Risk** (Line 102)
>    - [Explanation with fix]
>
> Would you like me to provide the corrected version?

---

## 💡 Tips for Best Results

### 1. Be Specific
❌ Bad: "security issues"  
✅ Good: "reentrancy vulnerabilities in withdrawal functions"

### 2. Include Code When Possible
❌ Bad: "Is this safe?"  
✅ Good: "Can you check this code for vulnerabilities? [paste code]"

### 3. Ask Follow-up Questions
```
You: "Search for reentrancy attacks"
Claude: [Shows results]
You: "Can you show me a complete secure example?"
Claude: [Provides detailed solution]
```

### 4. Request Explanations
```
You: "Explain why the checks-effects-interactions pattern prevents reentrancy"
Claude: [Uses examples from database to explain]
```

---

## 🔄 Workflow Examples

### Security Audit Workflow

1. **Initial Scan**
   ```
   Search for common vulnerabilities in DeFi contracts
   ```

2. **Specific Analysis**
   ```
   Analyze this contract for [specific vulnerability type]
   ```

3. **Code Review**
   ```
   Review each function for security issues
   ```

4. **Remediation**
   ```
   Show me how to fix [specific issue]
   ```

5. **Verification**
   ```
   Is this corrected version secure?
   ```

---

## 📊 Response Format

Every search returns structured data:

```json
{
  "success": true,
  "summary": "Found X unique vulnerabilities",
  "total_found": X,
  "top_results": [
    {
      "rank": 1,
      "title": "Vulnerability Name",
      "severity": "High|Medium|Low",
      "final_score": 1.23,
      "description": "Detailed description...",
      "code_example": "Vulnerable code example...",
      "mitigation": "How to fix...",
      "category": "Vulnerability category",
      "file_reference": "source_file.json",
      "relevance_scores": [0.95, 0.89],
      "found_in_collections": ["BGE", "UniXcoder"]
    }
  ]
}
```

Claude then formats this into human-readable analysis.

---

## 🎓 Learning Examples

### Example: Understanding a Vulnerability

**You:**
```
I don't understand what a reentrancy attack is. Can you explain with examples?
```

**Claude:**
> Let me search for reentrancy examples...
>
> [Uses search_vulnerabilities("reentrancy attack examples")]
>
> A reentrancy attack happens when a malicious contract calls back into your contract before the first invocation is finished. Here's a real example:
>
> **Vulnerable Code:**
> ```solidity
> // From the vulnerability database:
> [Shows actual vulnerable code example]
> ```
>
> **Attack Scenario:**
> [Explains step-by-step how the attack works]
>
> **Secure Version:**
> [Shows the fixed code]
>
> The key principle is: Always update state BEFORE making external calls.

---

## 🛠️ Integration Examples

### Using with Other Tools

**Example: Combine with Static Analysis**
```
You: "I ran Slither and got this warning: [paste warning]"
Claude: [Searches for related vulnerabilities]
"This warning indicates a potential reentrancy issue..."
```

**Example: Pre-Deployment Checklist**
```
You: "Give me a security checklist for deploying this contract"
Claude: [Searches for common deployment issues]
"Here's a comprehensive checklist based on common vulnerabilities..."
```

---

## 📝 Notes

- Each search query counts toward your monthly quota
- Response time: typically 2-5 seconds
- Rate limit: 10 requests/minute (Free tier)
- All searches are logged in your dashboard

---

## 🆘 Need Help?

If the examples don't work as expected:
1. Check your API quota in the dashboard
2. Verify your internet connection
3. Try simpler queries first
4. Check Claude Desktop logs for errors

For more examples and updates, visit: https://yourdomain.com/docs/examples

