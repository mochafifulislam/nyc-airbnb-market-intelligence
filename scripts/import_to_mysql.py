import numpy as np
import mysql.connector
import pandas as pd

# 1. Baca File CSV dengan low_memory=False
file_path = "NYC_Airbnb_Cleaned.csv"
df = pd.read_csv(file_path, low_memory=False)

# Standardisasi nama kolom (ubah ke lowercase & ganti spasi dengan underscore)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# 2. Pemetaan Nama Kolom (Mencegah KeyError jika nama kolom sedikit berbeda)
# Latitude
if "lat" in df.columns and "latitude" not in df.columns:
    df.rename(columns={"lat": "latitude"}, inplace=True)
# Longitude
if "long" in df.columns and "longitude" not in df.columns:
    df.rename(columns={"long": "longitude"}, inplace=True)
if "long_ " in df.columns and "longitude" not in df.columns:
    df.rename(columns={"long_": "longitude"}, inplace=True)

# Jika kolom latitude/longitude masih tidak ditemukan, buat kolom default (0.0) agar script tidak crash
if "latitude" not in df.columns:
    df["latitude"] = 0.0
if "longitude" not in df.columns:
    df["longitude"] = 0.0

# 3. Penanganan Kolom Wajib Lainnya
required_columns = [
    "id",
    "name",
    "host_id",
    "host_name",
    "neighbourhood_group",
    "neighbourhood",
    "latitude",
    "longitude",
    "room_type",
    "price",
    "minimum_nights",
    "number_of_reviews",
    "reviews_per_month",
    "calculated_host_listings_count",
    "availability_365",
]

# Pastikan semua kolom yang dibutuhkan ada di DataFrame
for col in required_columns:
    if col not in df.columns:
        df[col] = 0 if "count" in col or "nights" in col else "Unknown"

# 4. Filter & Clean Nilai Kosong / Format Data
df_sub = df[required_columns].copy()

# Bersihkan kolom Price (Hapus $ dan koma jika masih ada)
df_sub["price"] = (
    df_sub["price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)
df_sub["price"] = (
    pd.to_numeric(df_sub["price"], errors="coerce").fillna(0).astype(int)
)

# Handling Missing Values
df_sub["name"] = df_sub["name"].fillna("Unknown").astype(str)
df_sub["host_name"] = df_sub["host_name"].fillna("Unknown").astype(str)
df_sub["neighbourhood_group"] = (
    df_sub["neighbourhood_group"].fillna("Unknown").astype(str)
)
df_sub["neighbourhood"] = df_sub["neighbourhood"].fillna("Unknown").astype(str)
df_sub["room_type"] = df_sub["room_type"].fillna("Unknown").astype(str)

df_sub["id"] = (
    pd.to_numeric(df_sub["id"], errors="coerce").fillna(0).astype(int)
)
df_sub["host_id"] = (
    pd.to_numeric(df_sub["host_id"], errors="coerce").fillna(0).astype(int)
)
df_sub["latitude"] = (
    pd.to_numeric(df_sub["latitude"], errors="coerce").fillna(0.0).astype(float)
)
df_sub["longitude"] = (
    pd.to_numeric(df_sub["longitude"], errors="coerce")
    .fillna(0.0)
    .astype(float)
)
df_sub["minimum_nights"] = (
    pd.to_numeric(df_sub["minimum_nights"], errors="coerce")
    .fillna(1)
    .astype(int)
)
df_sub["number_of_reviews"] = (
    pd.to_numeric(df_sub["number_of_reviews"], errors="coerce")
    .fillna(0)
    .astype(int)
)
df_sub["reviews_per_month"] = (
    pd.to_numeric(df_sub["reviews_per_month"], errors="coerce")
    .fillna(0.0)
    .astype(float)
)
df_sub["calculated_host_listings_count"] = (
    pd.to_numeric(df_sub["calculated_host_listings_count"], errors="coerce")
    .fillna(1)
    .astype(int)
)
df_sub["availability_365"] = (
    pd.to_numeric(df_sub["availability_365"], errors="coerce")
    .fillna(0)
    .astype(int)
)

# 5. Koneksi ke MySQL XAMPP
print("Menghubungkan ke MySQL...")
db = mysql.connector.connect(
    host="localhost", user="root", password="", database="nyc_airbnb"
)
cursor = db.cursor()

# Query Insert dengan ON DUPLICATE KEY UPDATE agar tidak eror jika ID sama
insert_query = """
INSERT INTO listings (
    id, name, host_id, host_name, neighbourhood_group,
    neighbourhood, latitude, longitude, room_type, price,
    minimum_nights, number_of_reviews, reviews_per_month,
    calculated_host_listings_count, availability_365
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    price=VALUES(price),
    number_of_reviews=VALUES(number_of_reviews);
"""

# Konversi DataFrame ke List of Tuples
records = [tuple(x) for x in df_sub.values]

print(f"Mulai memasukkan {len(records)} baris data ke MySQL...")

# Proses Upload secara bertahap (batch size 1000 agar cepat)
batch_size = 1000
for i in range(0, len(records), batch_size):
    batch = records[i : i + batch_size]
    cursor.executemany(insert_query, batch)
    db.commit()

print("Selesai! Seluruh data berhasil masuk ke tabel 'listings' di MySQL.")

cursor.close()
db.close()