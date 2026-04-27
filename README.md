# iPayX FX Audit MCP

**Expose hidden bank FX fees in 30 seconds. No signup required.**

The world's first Model Context Protocol server for foreign exchange auditing. Any AI agent (Claude, ChatGPT, Cursor) can audit FX transactions against mid-market rates in real time.

**Live endpoint:** `https://hvujzsdwcoweirroubeh.supabase.co/functions/v1/mcp-server`

## Tools

| Tool | Auth | Cost |
|------|------|------|
| `check_fx_rate` | None | Free forever |
| `audit_transaction` | None | 3 free/month per IP |
| `full_forensic_report` | Bearer token | API key required |

## Quick Start (Claude Desktop)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ipayx-fx": {
      "url": "https://hvujzsdwcoweirroubeh.supabase.co/functions/v1/mcp-server"
    }
  }
}
