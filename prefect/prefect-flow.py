"""iPayX FX Audit — Prefect Horizon Flow
Distributes FX audit workloads via Prefect's orchestration layer.
Deploy on Prefect Cloud or self-hosted Prefect server.

Install: pip install prefect httpx
Deploy: prefect deploy prefect-flow.py:fx_audit_flow --name ipayx-fx-audit
"""
import os
import httpx
from prefect import flow, task, get_run_logger
from datetime import datetime
from typing import Optional

IPAYX_MCP_URL = "https://wild-bird-a412.ybolduc.workers.dev/mcp"
IPAYX_API_KEY = os.environ.get("IPAYX_API_KEY", "")


@task(name="call-ipayx-mcp", retries=2, retry_delay_seconds=5)
def call_mcp_tool(method: str, tool_name: str, arguments: dict) -> dict:
    """Call iPayX MCP server via JSON-RPC 2.0."""
    logger = get_run_logger()
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {"name": tool_name, "arguments": arguments},
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {IPAYX_API_KEY}",
        "Accept": "application/json, text/event-stream",
    }
    with httpx.Client(timeout=30) as client:
        response = client.post(IPAYX_MCP_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        logger.info(f"[iPayX] {tool_name} → {result.get('result', {})!r}")
        return result


@task(name="check-fx-rate")
def check_fx_rate(from_currency: str, to_currency: str) -> dict:
    """Get live mid-market FX rate. Free, no quota."""
    return call_mcp_tool(
        method="tools/call",
        tool_name="check_fx_rate",
        arguments={"from_currency": from_currency, "to_currency": to_currency},
    )


@task(name="audit-fx-transaction")
def audit_transaction(
    from_currency: str,
    to_currency: str,
    amount_debited: float,
    amount_received: float,
    transaction_date: str,
    company_id: Optional[str] = None,
) -> dict:
    """Audit a single FX transaction. Returns spread bps + FX Score 0-10."""
    args = {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount_debited": amount_debited,
        "amount_received": amount_received,
        "transaction_date": transaction_date,
    }
    if company_id:
        args["company_id"] = company_id
    return call_mcp_tool(
        method="tools/call",
        tool_name="audit_transaction",
        arguments=args,
    )


@flow(
    name="iPayX FX Audit Flow",
    description="Forensic FX audit pipeline using iPayX MCP. Detects hidden bank spreads.",
    version="1.2.1",
)
def fx_audit_flow(
    transactions: list[dict],
    from_currency: str = "CAD",
    to_currency: str = "USD",
):
    """Main Prefect flow: audits a batch of FX transactions.

    Args:
        transactions: List of dicts with keys: amount_debited, amount_received, date
        from_currency: Base currency (debited)
        to_currency: Target currency (received)

    Returns:
        List of audit results with FX scores
    """
    logger = get_run_logger()
    logger.info(f"Starting iPayX FX Audit Flow — {len(transactions)} transactions")

    # Get live rate first (free check)
    rate_result = check_fx_rate(from_currency=from_currency, to_currency=to_currency)
    logger.info(f"Live mid-market rate: {rate_result}")

    # Audit each transaction
    results = []
    for tx in transactions:
        result = audit_transaction(
            from_currency=from_currency,
            to_currency=to_currency,
            amount_debited=tx["amount_debited"],
            amount_received=tx["amount_received"],
            transaction_date=tx.get("date", datetime.today().strftime("%Y-%m-%d")),
            company_id=tx.get("company_id"),
        )
        results.append(result)

    logger.info(f"Audit complete — {len(results)} transactions processed")
    return results


if __name__ == "__main__":
    # Example: audit 3 CAD→USD transactions
    sample_transactions = [
        {"amount_debited": 138250, "amount_received": 100000, "date": "2026-05-01"},
        {"amount_debited": 69800,  "amount_received": 50000,  "date": "2026-04-15"},
        {"amount_debited": 415000, "amount_received": 300000, "date": "2026-03-20"},
    ]
    fx_audit_flow(transactions=sample_transactions, from_currency="CAD", to_currency="USD")
