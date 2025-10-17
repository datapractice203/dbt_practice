import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)

# --- Simulation Window ---
start_window = datetime(2024, 1, 1)
end_window = datetime(2025, 12, 31)

# --- Product Dimension (10 machines) with mapped prices ---
products_data = [
    {"product_id": 1, "category": "Mini Excavator", "weight_range": "2500–4000 lbs", "daily_price": 387.00},
    {"product_id": 2, "category": "Mini Excavator", "weight_range": "10000–14000 lbs", "daily_price": 559.00},
    {"product_id": 3, "category": "Mini Excavator", "weight_range": "15000–20000 lbs", "daily_price": 820.00},
    {"product_id": 4, "category": "Track Excavator", "weight_range": "25000–35000 lbs", "daily_price": 946.00},
    {"product_id": 5, "category": "Track Excavator", "weight_range": "25000–35000 lbs", "daily_price": 946.00},
    {"product_id": 6, "category": "Mini Excavator", "weight_range": "2500–4000 lbs", "daily_price": 387.00},
    {"product_id": 7, "category": "Mini Excavator", "weight_range": "10000–14000 lbs", "daily_price": 559.00},
    {"product_id": 8, "category": "Mini Excavator", "weight_range": "15000–20000 lbs", "daily_price": 820.00},
    {"product_id": 9, "category": "Track Excavator", "weight_range": "25000–35000 lbs", "daily_price": 946.00},
    {"product_id": 10, "category": "Track Excavator", "weight_range": "25000–35000 lbs", "daily_price": 946.00},
]
products_df = pd.DataFrame(products_data)

# --- Customers Dimension ---
customers_df = pd.DataFrame({
    "customer_id": range(1001, 1021),
    "business_name": [f"Contractor_{i}" for i in range(20)],
    "contact_name": [f"Person_{i}" for i in range(20)]
})

# --- Locations Dimension ---
locations_df = pd.DataFrame({
    "location_id": [1, 2, 3],
    "location_name": ["Central Yard", "North Depot", "South Branch"]
})

# --- Generate Rentals with Non-Overlapping Dates per Machine ---
rental_data = []
availability = {pid: [] for pid in products_df["product_id"]}

def get_next_available_range(product_id, min_days=5, max_days=90):
    for _ in range(1000):
        duration = random.randint(min_days, max_days)
        start_candidate = start_window + timedelta(days=random.randint(0, (end_window - start_window).days - duration))
        end_candidate = start_candidate + timedelta(days=duration)

        overlap = any(
            start_candidate < b_end and end_candidate > b_start
            for b_start, b_end in availability[product_id]
        )
        if not overlap:
            availability[product_id].append((start_candidate, end_candidate))
            return start_candidate, end_candidate, duration
    return None, None, None

for _ in range(300):
    product = products_df.sample(1).iloc[0]
    product_id = product["product_id"]
    customer = customers_df.sample(1).iloc[0]
    location = locations_df.sample(1).iloc[0]

    start_date, end_date, rental_days = get_next_available_range(product_id)
    if not start_date:
        continue

    rental_data.append({
        "rental_id": f"R-{random.randint(10000, 99999)}",
        "product_id": product_id,
        "customer_id": customer["customer_id"],
        "location_id": location["location_id"],
        "start_date": start_date,
        "end_date": end_date,
        "rental_days": rental_days,
        "daily_rate": product["daily_price"],
        "total_rental_cost": round(product["daily_price"] * rental_days, 2)
    })

rentals_df = pd.DataFrame(rental_data)

# --- Updated Rental Revenue Targets ---
revenue_targets = []
for year in [2024, 2025]:
    for row in products_df[["category", "weight_range"]].drop_duplicates().itertuples(index=False):
        target_amount = random.randint(400_000, 1_200_000)
        revenue_targets.append({
            "year": year,
            "category": row.category,
            "weight_range": row.weight_range,
            "target_revenue": target_amount
        })

rental_targets_df = pd.DataFrame(revenue_targets)


# --- Shipments Table ---
cities = ["Denver", "Austin", "Phoenix", "Chicago", "Atlanta"]
zip_codes = ["80202", "73301", "85001", "60601", "30301"]
shipment_data = []

for row in rentals_df.itertuples():
    order_date = row.start_date - timedelta(days=random.randint(3, 15))
    delivery_date = order_date + timedelta(days=random.randint(1, 4))
    shipment_data.append({
        "shipment_id": f"S-{random.randint(10000,99999)}",
        "rental_id": row.rental_id,
        "product_id": row.product_id,
        "customer_id": row.customer_id,
        "order_date": order_date,
        "delivery_date": delivery_date,
        "destination_city": random.choice(cities),
        "destination_zip": random.choice(zip_codes)
    })
shipments_df = pd.DataFrame(shipment_data)

# --- Downtime Table ---
downtime_records = []
for product in products_df.itertuples():
    for _ in range(random.randint(1, 3)):
        down_start = start_window + timedelta(days=random.randint(0, 700))
        down_days = random.randint(2, 14)
        down_end = down_start + timedelta(days=down_days)

        if down_end <= end_window:
            downtime_records.append({
                "downtime_id": f"D-{random.randint(10000,99999)}",
                "product_id": product.product_id,
                "downtime_start": down_start,
                "downtime_end": down_end,
                "downtime_days": down_days
            })
downtime_df = pd.DataFrame(downtime_records)

import os

# Get the path to the project root (one level up from this script)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Path to dbt seeds folder
seeds_path = os.path.join(project_root, 'seeds')

# Ensure the folder exists
os.makedirs(seeds_path, exist_ok=True)

# Save CSVs to seeds folder
rentals_df.to_csv(os.path.join(seeds_path, 'rental.csv'), index=False)
locations_df.to_csv(os.path.join(seeds_path, 'location.csv'), index=False)
products_df.to_csv(os.path.join(seeds_path, 'product.csv'), index=False)
customers_df.to_csv(os.path.join(seeds_path, 'customer.csv'), index=False)
rental_targets_df.to_csv(os.path.join(seeds_path, 'rental_target.csv'), index=False)
shipments_df.to_csv(os.path.join(seeds_path, 'shipment.csv'), index=False)
downtime_df.to_csv(os.path.join(seeds_path, 'downtime.csv'), index=False)