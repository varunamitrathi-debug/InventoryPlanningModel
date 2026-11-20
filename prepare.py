"""
Prepare weekly demand for the 30 highest revenue products, UK customers,
December 2010 to November 2011 (52 full weeks), from UCI Online Retail II.
Run:  python prepare.py     (needs pandas and openpyxl)
Input: data/online retail.xlsx   Output: output/sku demand.csv (pasted into the Data sheet)
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent
sheets = pd.read_excel(ROOT / "data" / "online retail.xlsx", sheet_name=None)
df = pd.concat(sheets.values(), ignore_index=True)
df.columns = ["invoice", "stockcode", "description", "quantity", "invoicedate", "price", "customer", "country"]
df["invoice"] = df["invoice"].astype(str)
df = df[~df["invoice"].str.startswith("C") & (df["quantity"] > 0) & (df["price"] > 0)]
df = df[df["country"] == "United Kingdom"]
df["invoicedate"] = pd.to_datetime(df["invoicedate"])
start, end = pd.Timestamp("2010-12-06"), pd.Timestamp("2011-12-05")   # Monday to Monday, 52 weeks
df = df[(df["invoicedate"] >= start) & (df["invoicedate"] < end)]
# Products only, no postage, fees or manual adjustments
df = df[df["stockcode"].astype(str).str.match(r"^\d{5}")]
# One off bulk lines over 10,000 units are excluded: the largest (74,215 storage jars,
# January 2011) was reversed by a cancellation the same day and is not real demand.
excluded = df[df["quantity"] > 10000]
print("Excluded bulk lines:", len(excluded), "units:", int(excluded["quantity"].sum()))
df = df[df["quantity"] <= 10000]
df["revenue"] = df["quantity"] * df["price"]
df["week"] = ((df["invoicedate"] - start).dt.days // 7).astype(int)

top = df.groupby("stockcode")["revenue"].sum().nlargest(30).index
d = df[df["stockcode"].isin(top)]
weekly = d.pivot_table(index="stockcode", columns="week", values="quantity", aggfunc="sum").reindex(columns=range(52)).fillna(0)
out = pd.DataFrame({
    "stockcode": weekly.index.astype(str),
    "description": d.groupby("stockcode")["description"].agg(lambda s: s.mode().iloc[0]).reindex(weekly.index).str.replace("-", " ").str.strip().str.title(),
    "annual units": weekly.sum(axis=1).astype(int),
    "avg weekly units": weekly.mean(axis=1).round(2),
    "sd weekly units": weekly.std(axis=1, ddof=1).round(2),
    "avg selling price gbp": (d.groupby("stockcode")["revenue"].sum() / d.groupby("stockcode")["quantity"].sum()).reindex(weekly.index).round(3),
})
out["annual revenue gbp"] = (d.groupby("stockcode")["revenue"].sum().reindex(weekly.index)).round(0)
out = out.sort_values("annual revenue gbp", ascending=False)
out.to_csv(ROOT / "output" / "sku demand.csv", index=False)
print(out.to_string(index=False))
print("weeks:", weekly.shape[1], " total revenue of top 30:", out["annual revenue gbp"].sum())
