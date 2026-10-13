def register_prompts(mcp, settings=None):
    client = getattr(settings, "client_name", "Peltier Pro")
    provider = getattr(settings, "provider_name", "Zen Business Solutions")

    @mcp.prompt()
    def mcp_welcome():
        """Welcome message for users of this Odoo MCP instance."""
        return f"""Welcome!\n\nYou are connected to the {client} Odoo MCP.\n\nAvailable reporting areas:\n- CRM\n- Sales\n- Accounting\n- Inventory\n- Projects / Tasks\n\nPowered by: {provider}""".strip()

    @mcp.prompt()
    def sales_report_help():
        """Show example prompts for Sales reporting."""
        return f"""Sales reporting examples:\n- Give me this month's sales summary.\n- Who are our top customers?\n- Show sales performance by salesperson.\n- Which confirmed sales orders still need to be invoiced?\n- Which quotations are expiring soon?\n\nPowered by: {provider}""".strip()

    @mcp.prompt()
    def accounting_report_help():
        """Show example prompts for Accounting reporting."""
        return f"""Accounting reporting examples:\n- Show overdue customer invoices.\n- Which invoices are due within the next 7 days?\n- Give me our aged receivables.\n- Give me our aged payables.\n- How much does a customer currently owe us?\n- How much do we currently owe a vendor?\n\nPowered by: {provider}""".strip()

    @mcp.prompt()
    def inventory_report_help():
        """Show example prompts for Inventory reporting."""
        return f"""Inventory reporting examples:\n- Which products are low on stock?\n- Which products are out of stock?\n- Give me an inventory stock summary.\n- Which inventory transfers are late?\n- Show pending incoming receipts.\n- Show pending customer deliveries.\n\nPowered by: {provider}""".strip()

    @mcp.prompt()
    def crm_report_help():
        """Show example prompts for CRM reporting."""
        return f"""CRM reporting examples:\n- Give me an overview of our CRM pipeline.\n- How many opportunities are in each stage?\n- Which opportunities are closing soon?\n- Which opportunities have not been updated recently?\n- Show a salesperson's active CRM pipeline.\n\nPowered by: {provider}""".strip()
