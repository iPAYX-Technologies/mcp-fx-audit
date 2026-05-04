# Submitting iPayX n8n Workflow to n8n Hub

The workflow `n8n-quickbooks-fx-intelligence.json` in this folder is ready for n8n Hub submission.

## Submission URL
https://n8n.io/workflows/submit

## Required Fields
- **Name**: iPayX FX Intelligence Engine — QuickBooks + AI Forensic Audit
- **Description**: Automatically detects FX transactions in QuickBooks Online, audits them via the iPayX MCP server (spread bps, FX Score 0-10), and generates a DeepSeek + Nemotron forensic narrative. Runs daily via cron.
- **Tags**: finance, fx, audit, quickbooks, mcp, ai-agent, forensic
- **Category**: Finance & Accounting
- **Author**: Yannick Bolduc / iPayX Protocol
- **Source URL**: https://github.com/iPAYX-Technologies/mcp-fx-audit

## Credentials Needed (document in Hub)
1. **iPayX API Key** — get at https://www.ipayx.ai/developers
2. **QuickBooks OAuth2** — standard QB Online OAuth
3. **DeepSeek API Key** — https://platform.deepseek.com
4. **NVIDIA API Key** (Nemotron, optional) — https://build.nvidia.com

## MCP Connection
Add this MCP server in n8n Settings → MCP Servers:
```
URL: https://wild-bird-a412.ybolduc.workers.dev/mcp
Auth: Bearer YOUR_IPAYX_API_KEY
```

## Workflow Screenshot
For Hub submission, screenshot the workflow canvas showing:
- QB trigger → FX scanner → iPayX MCP audit → DeepSeek narrative → Slack/email alert
