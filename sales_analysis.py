import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Create sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    price REAL
);
""")

# Insert sample data
sample_data = [
    ("Widget A", 10, 5.0),
    ("Widget B", 7, 8.5),
    ("Widget C", 15, 4.0),
    ("Widget A", 5, 5.0),
    ("Widget B", 8, 8.5),
    ("Widget C", 12, 4.0),
]
cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?);", sample_data)
conn.commit()

# Query total quantity and revenue per product
query = """
SELECT 
    product, 
    SUM(quantity) AS total_quantity, 
    SUM(quantity * price) AS total_revenue
FROM sales
GROUP BY product;
"""
df = pd.read_sql_query(query, conn)
conn.close()

# Print results
print("Sales Summary:")
print(df)

# Plot total revenue per product
plt.figure(figsize=(8, 5))
plt.bar(df['product'], df['total_revenue'], color='skyblue')
plt.xlabel('Product')
plt.ylabel('Total Revenue')
plt.title('Total Revenue per Product')
plt.tight_layout()
plt.savefig("total_revenue_chart.png")
plt.show()
