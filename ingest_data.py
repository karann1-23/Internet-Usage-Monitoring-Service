import pandas as pd
from models import Usage, SessionLocal

# Read the CSV file
df = pd.read_csv("usage.csv")

# Remove leading/trailing spaces from column names
df.columns = df.columns.str.strip()

# Create a database session
db = SessionLocal()

for _, row in df.iterrows():
    usage = Usage(
        username=row["username"],
        mac_address=row["mac_address"],
        start_time=row["start_time"],
        usage_time=row["usage_time"],
        upload=float(row["upload"]),
        download=float(row["download"])
    )
    db.add(usage)

db.commit()
db.close()
print("Data ingested successfully!")