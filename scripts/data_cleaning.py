import numpy as np
import pandas as pd

# 1. Load Data dengan low_memory=False untuk menghilangkan DtypeWarning
file_path = "Airbnb_Open_Data.csv"
df = pd.read_csv(file_path, low_memory=False)

# 2. Standardisasi Nama Kolom (Ubah ke lowercase & ganti spasi dengan underscore)
# Contoh: "Reviews per month" -> "reviews_per_month", "price " -> "price"
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("Nama kolom setelah dibersihkan:")
print(df.columns.tolist())

# 3. Membersihkan Kolom 'price' (Menghapus '$' dan ',' agar bisa diubah ke angka)
if "price" in df.columns:
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

# 4. Cleaning & Fill Missing Values
# Kolom reviews_per_month / number_of_reviews
if "reviews_per_month" in df.columns:
    df["reviews_per_month"] = df["reviews_per_month"].fillna(0)

if "number_of_reviews" in df.columns:
    df["number_of_reviews"] = df["number_of_reviews"].fillna(0)

if "name" in df.columns:
    df["name"] = df["name"].fillna("Unknown")

# 5. Filtering Outliers pada Price
df = df[df["price"].notna() & (df["price"] > 0) & (df["price"] <= 1000)]

# 6. Feature Engineering untuk Analisis Bisnis (Looker & Tableau)
# Cek ketersediaan kolom availability 365
avail_col = (
    "availability_365"
    if "availability_365" in df.columns
    else "availability_365"
)

if avail_col in df.columns and "reviews_per_month" in df.columns:
    df[avail_col] = pd.to_numeric(df[avail_col], errors="coerce").fillna(0)

    # Taksiran hari terisi per tahun
    df["estimated_nights_booked"] = np.minimum(
        365 - df[avail_col], df["reviews_per_month"] * 12 * 2.5
    )
    df["estimated_nights_booked"] = df["estimated_nights_booked"].clip(
        lower=0, upper=365
    )

    # Est. Occupancy Rate (%)
    df["occupancy_rate"] = (df["estimated_nights_booked"] / 365) * 100

    # Estimated Annual Revenue ($)
    df["estimated_revenue"] = df["estimated_nights_booked"] * df["price"]

# 7. Simpan Hasil Cleaning
output_path = "NYC_Airbnb_Cleaned.csv"
df.to_csv(output_path, index=False)
print(f"\nProses selesai! File berhasil disimpan sebagai '{output_path}'")
print(f"Total baris data bersih: {len(df)}")