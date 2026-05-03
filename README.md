# iPayX FX Audit MCP

**Expose hidden bank FX fees in 30 seconds. No signup required.**

The world's first Model Context Protocol server for foreign exchange forensic auditing. Any AI agent (Claude, Perplexity, Cursor, Copilot) can audit FX transactions against mid-market rates in real time and generate FINTRAC-certified forensic reports.

[![Smithery](https://smithery.ai/badge/@ybolduc/ipayx-fx-auditor)](https://smithery.ai/server/@ybolduc/ipayx-fx-auditor)
[![MCP Registry](https://img.shields.io/badge/MCP%20Registry-Published-blue)](https://registry.modelcontextprotocol.io)

**Live endpoint (Cloudflare):** `https://wild-bird-a412.ybolduc.workers.dev/mcp`

---

## Tools

### `check_fx_rate`
Get the current mid-market exchange rate for any currency pair.

**Parameters:**
- `from_currency` (string) - Source currency code (e.g. `CAD`)
- `to_currency` (string) - Target currency code (e.g. `USD`)

**Auth:** None | **Cost:** Free forever

**Example:**
```json
{ "from_currency": "CAD", "to_currency": "USD" }
```

---

### `audit_transaction`
Audit a specific FX transaction. Compares the rate your bank applied against the real mid-market rate. Returns the hidden spread in basis points, a forensic score 1-10, and the total amount lost to hidden fees.

**Parameters:**
- `amount` (number) - Transaction amount
- `from_currency` (string) - Source currency code
- `to_currency` (string) - Target currency code
- `bank_rate` (number) - The rate your bank applied

**Auth:** None | **Cost:** 3 free/month per IP

**Example:**
```json
{
  "amount": 50000,
  "from_currency": "CAD",
  "to_currency": "USD",
  "bank_rate": 0.685,
  "bank_name": "TD Bank"
}
```

---

### `full_forensic_report`
Generate a complete forensic FX audit report suitable for legal proceedings, CFO review, or FINTRAC compliance documentation. Includes spread history, narrative analysis, and certified audit trail.

**Parameters:**
- `audit_id` (string) - ID from a previous `audit_transaction` call

**Auth:** Bearer token (API key required) | **Cost:** Per report

---

### `compare_fx_sources`
Compare FX rates from multiple sources simultaneously (Twelve Data, Open Exchange Rates). Detects discrepancies and identifies the most favorable rate. Essential for multi-bank or multi-broker comparisons.

**Parameters:**
- `from_currency` (string) - Source currency code
- `to_currency` (string) - Target currency code

**Auth:** None | **Cost:** Free

**Example:**
```json
{ "from_currency": "USD", "to_currency": "CAD" }
```

---

## Quick Start

### Claude Desktop
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "ipayx-fx": {
      "url": "https://wild-bird-a412.ybolduc.workers.dev/mcp"
    }
  }
}
```

### Cursor / Windsurf
```json
{
  "mcpServers": {
    "ipayx-fx": {
      "url": "https://wild-bird-a412.ybolduc.workers.dev/mcp",
      "transport": "streamable-http"
    }
  }
}
```

### Perplexity
Settings → MCP Connectors → Add Remote → paste URL:
```
https://wild-bird-a412.ybolduc.workers.dev/mcp
```

### Smithery CLI
```bash
npx -y smithery skill add ybolduc/ipayx-fx-auditor
```

---

## Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 8-10 | Fair rate | No action needed |
| 5-7 | Moderate markup | Negotiate with bank |
| 1-4 | Excessive hidden fees | Request forensic report |

---

## Compliance

- **FINTRAC MSB Certified:** C10001283
- **Jurisdiction:** Canada (FINTRAC applies to CA operations only)
- **FX Data Sources:** Twelve Data (primary) → Open Exchange Rates (fallback)
- **Weekend/Holiday Logic:** Cached Friday close rate with explicit `source: cached_friday_close` flag

---

## About iPayX Protocol

iPayX Protocol (11850091 Canada Inc.) is the only rail-agnostic FX forensic audit layer for B2B payments. We audit hidden costs regardless of payment rail - SWIFT, SEPA, Stablecoin, or Card.

**Website:** [ipayx.ai](https://www.ipayx.ai) | **Dashboard:** [app.ipayx.ai](https://app.ipayx.ai)
