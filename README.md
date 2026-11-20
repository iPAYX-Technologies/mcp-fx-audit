<!-- mcp-name: io.github.iPAYX-Technologies/mcp-fx-audit -->

# iPayX FX Audit MCP

**Expose hidden bank FX fees in 30 seconds. No signup required.**

A Model Context Protocol server for foreign exchange forensic auditing. Any AI agent (Claude, ChatGPT, Perplexity, Cursor, Copilot) can check live mid-market rates, audit FX transactions against the mid-market rate in real time, and generate a full forensic report.

[![MCP Registry](https://img.shields.io/badge/MCP%20Registry-Published-blue)](https://registry.modelcontextprotocol.io)

**Live endpoint:** `https://mcp.ipayx.ai/mcp`
**Server version:** 1.4.0 — remote, streamable HTTP, no install required.

---

## Tools

### `check_fx_mid_market_rate`
Returns the live mid-market FX rate for a currency pair (Twelve Data, Open Exchange Rates fallback), in both directions. When `bank_rate` is given, the output also includes the spread versus mid-market.

**Parameters:**
- `currency_from` (string, required) - ISO 4217 base currency (e.g. `USD`)
- `currency_to` (string, required) - ISO 4217 quote currency (e.g. `CAD`)
- `bank_rate` (number, optional) - Bank/broker rate to compare against mid-market

**Auth:** None | **Cost:** Free

**Example:**
```json
{ "currency_from": "USD", "currency_to": "CAD" }
```

---

### `audit_fx_transaction`
Audits one currency transaction against the live mid-market rate. Returns an FX score from 1 to 10, a rating, a verdict, the currency pair, amount and date.

**Parameters:**
- `amount` (number, required) - Transaction amount in `currency_from`
- `currency_from` (string, required) - ISO 4217 source currency
- `currency_to` (string, required) - ISO 4217 target currency
- `bank_rate` (number, required) - Rate the bank/broker actually charged
- `language` (string, optional) - `en` or `fr`

**Auth:** None | **Cost:** 3 free audits per IP per calendar month

**Example:**
```json
{
  "amount": 50000,
  "currency_from": "USD",
  "currency_to": "CAD",
  "bank_rate": 1.3750
}
```

---

### `compare_fx_sources`
Compares FX rates side by side: live mid-market, the Stripe FX Quotes API (when `stripe_api_key` is given) and the bank rate. Returns each source's effective rate, markup in basis points, cost per 100,000, FX score, and the lowest-cost source.

**Parameters:**
- `amount` (number, required) - Transaction amount
- `currency_from` (string, required) - Source currency (ISO 4217)
- `currency_to` (string, required) - Target currency (ISO 4217)
- `bank_rate` (number, required) - Rate quoted by the user's bank
- `bank_name` (string, optional) - Name of the bank (e.g. BMO, RBC, Chase)
- `stripe_api_key` (string, optional) - Stripe secret key to fetch a live FX quote

**Auth:** None | **Cost:** Free

**Example:**
```json
{ "amount": 100000, "currency_from": "USD", "currency_to": "CAD", "bank_rate": 1.3750 }
```

---

### `full_forensic_fx_report`
Produces a full FX audit report for one transaction: score, spread, estimated loss, breakdown and routing recommendation.

**Parameters:**
- `amount` (number, required)
- `currency_from` (string, required)
- `currency_to` (string, required)
- `bank_rate` (number, required)
- `company_name` (string, optional) - Company name for the report

**Auth:** Bearer <redacted> — API key from https://www.ipayx.ai/ai-access

---

## Quick Start

### Claude Desktop / Claude (custom connector)
Add a remote connector with the URL:
```
https://mcp.ipayx.ai/mcp
```

### Cursor / Windsurf
```json
{
  "mcpServers": {
    "ipayx-fx": {
      "url": "https://mcp.ipayx.ai/mcp",
      "transport": "streamable-http"
    }
  }
}
```

### Perplexity
Settings → Connectors → Add remote MCP server → paste URL:
```
https://mcp.ipayx.ai/mcp
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

- **Operator:** iPayX (11850091 Canada Inc. operating as iPayX Protocol)
- **FINTRAC MSB:** C10001283
- **Jurisdiction:** Canada
- **FX Data Sources:** Twelve Data (primary) → Open Exchange Rates (fallback)
- **Read-only:** the server never moves money and never executes transfers. Audit information only — not financial advice.

---

## About iPayX Protocol

iPayX Protocol (11850091 Canada Inc.) is a rail-agnostic FX forensic audit layer for B2B payments. We audit hidden costs regardless of payment rail — SWIFT, SEPA or card.

**Website:** [www.ipayx.ai](https://www.ipayx.ai) | **API access:** [ipayx.ai/ai-access](https://www.ipayx.ai/ai-access)
