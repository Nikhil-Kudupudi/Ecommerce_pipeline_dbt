import polars as pl 
from datetime import datetime, timedelta
import random
start_date = datetime(2024, 1, 1)
end_date = start_date + timedelta(days=19)
orders = pl.DataFrame({
"order_id": [f"O{i}" for i in range(1,21)],
"customer_id": [f"C{random.randint(1, 5)}" for i in range(20)],
"order_date": pl.date_range(start_date, end_date, interval="1d", eager=True), 
})

customers = pl.DataFrame({
    "customer_id": [f"C{i}" for i in range(1, 6)],
    "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "email": [f"customer{i}@example.com" for i in range(1, 6)]
})
statuses = [ "Shipped", "Delivered"]
shipments = pl.DataFrame({
    "shipment_id": [f"S{i}" for i in range(1, 21)],
    "order_id": orders["order_id"].to_list(),
    "status": [random.choice(statuses) for i in range(20)],
    "shipped_at": pl.date_range(start_date + timedelta(days=1), end_date + timedelta(days=1), interval="1d", eager=True),
    "delivered_at": pl.date_range(start_date + timedelta(days=2), end_date + timedelta(days=2), interval="1d", eager=True)
})

orders.write_csv("dummy_data/orders.csv")
customers.write_csv("dummy_data/customers.csv")
shipments.write_csv("dummy_data/shipments.csv")

