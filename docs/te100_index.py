# docs/te100_index.py - BULLETPROOF VERSION
import requests
import json
import pandas as pd
from datetime import datetime

# === CONFIG ===
USER_AGENT = "TE100 Index (contact@example.com)"
BASE_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json"

# === COMPANIES (Ticker: (Name, CIK)) ===
COMPANIES = {
    "WMT": ("Walmart", "0000104169"),
    "COST": ("Costco", "0000909832"),
    "AMZN": ("Amazon", "0001018724"),
    "AAPL": ("Apple", "0000320193"),
    "KR": ("Kroger", "0000056873"),
    "TGT": ("Target", "0000027419"),
    "HD": ("Home Depot", "0000354951")
}

# === FETCH DATA ===
def fetch_financials(cik):
    url = BASE_URL.format(cik.zfill(10))
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"HTTP {response.status_code} for CIK {cik}")
            return None, None, None
        data = response.json()
        facts = data.get("facts", {}).get("us-gaap", {})

        # Try multiple tags
        rev_tag = facts.get("Revenues") or facts.get("SalesRevenueNet") or facts.get("RevenueFromContractWithCustomerExcludingAssessedTax")
        ni_tag = facts.get("NetIncomeLoss") or facts.get("ProfitLoss")

        if not rev_tag or not ni_tag:
            print(f"Missing tags for CIK {cik}")
            return None, None, None

        rev_units = rev_tag.get("units", {}).get("USD", [])
        ni_units = ni_tag.get("units", {}).get("USD", [])

        # Filter annual filings
        annual_revs = [v for v in rev_units if v.get("form") in ["10-K", "20-F"]]
        annual_nis = [v for v in ni_units if v.get("form") in ["10-K", "20-F"]]

        if not annual_revs or not annual_nis:
            print(f"No annual data for CIK {cik}")
            return None, None, None

        latest_rev = max(annual_revs, key=lambda x: x["end"])
        latest_ni = max(annual_nis, key=lambda x: x["end"])

        return latest_rev["val"], latest_ni["val"], latest_rev["end"][:10]
    except Exception as e:
        print(f"Error fetching CIK {cik}: {e}")
        return None, None, None

# === MAIN ===
print(f"Starting TE 100 update: {datetime.now()}")

results = []
for ticker, (name, cik) in COMPANIES.items():
    print(f"Fetching {ticker} ({name})...")
    rev, ni, end_date = fetch_financials(cik)
    if rev and ni and rev > 0:
        te = (1 - ni / rev) * 100
        results.append({
            "Rank": 0,
            "Ticker": ticker,
            "Company": name,
            "Period End": end_date,
            "Revenue ($B)": round(rev / 1e9, 2),
            "Net Income ($B)": round(ni / 1e9, 2),
            "TE (%)": round(te, 2),
            "Consumer Insight": f"{round(te, 1)}¢ of $1 becomes real value"
        })

if not results:
    print("No data fetched. Check CIKs or network.")
    # Create empty files to avoid crash
    pd.DataFrame([{"Rank": 1, "Ticker": "N/A", "TE (%)": 0, "Consumer Insight": "No data"}]).to_json("docs/te100_latest.json", orient="records")
    pd.DataFrame([{"Rank": 1, "Ticker": "N/A", "TE (%)": 0, "Consumer Insight": "No data"}]).to_csv("docs/te100_latest.csv", index=False)
else:
    df = pd.DataFrame(results).sort_values("TE (%)", ascending=False)
    df["Rank"] = range(1, len(df) + 1)
    df.to_json("docs/te100_latest.json", orient="records", indent=2)
    df.to_csv("docs/te100_latest.csv", index=False)
    print(f"Success! {len(df)} companies updated.")

print("TE 100 update complete.")
