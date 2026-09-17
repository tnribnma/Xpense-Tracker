import csv
import io
from app.models.transaction import Transaction
from typing import Sequence

def generate_transactions_csv(transactions: Sequence[Transaction]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["Date", "Description", "Original Amount", "Currency", "Exchange Rate", "Base Amount (USD)"])
    
    for tx in transactions:
        writer.writerow([
            tx.date.strftime("%Y-%m-%d %H:%M:%S"),
            tx.description or "",
            f"{tx.original_amount:.2f}",
            tx.original_currency,
            f"{tx.exchange_rate:.4f}",
            f"{tx.base_amount:.2f}"
        ])
        
    return output.getvalue()