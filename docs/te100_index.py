# docs/te100_index.py - TE + CTE (Consumer Transformation Efficiency)
import requests
import pandas as pd
from datetime import datetime

USER_AGENT = "TE100 Index (contact@example.com)"
BASE_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json"

# === 100+ COMPANIES ===
COMPANIES = {
    "WMT": ("Walmart", "0000104169"), "COST": ("Costco", "0000909832"),
    "AMZN": ("Amazon", "0001018724"), "AAPL": ("Apple", "0000320193"),
    "KR": ("Kroger", "0000056873"), "TGT": ("Target", "0000027419"),
    "HD": ("Home Depot", "0000354951"), "LOW": ("Lowe's", "0000060914"),
    "DG": ("Dollar General", "0000027419"), "DLTR": ("Dollar Tree", "0000935703"),
    "BJ": ("BJ's Wholesale", "0001531152"), "MSFT": ("Microsoft", "0000789019"),
    "GOOGL": ("Alphabet", "0001652044"), "META": ("Meta", "0001326801"),
    "NVDA": ("NVIDIA", "0001045810"), "TSLA": ("Tesla", "0001318605"),
    "BRK-B": ("Berkshire Hathaway", "0001067983"), "LLY": ("Eli Lilly", "0000059478"),
    "AVGO": ("Broadcom", "0001101239"), "JPM": ("JPMorgan Chase", "0000019617"),
    "V": ("Visa", "0001403161"), "UNH": ("UnitedHealth", "0000731766"),
    "XOM": ("ExxonMobil", "0000034088"), "MA": ("Mastercard", "0001141391"),
    "PG": ("Procter & Gamble", "0000080424"), "JNJ": ("Johnson & Johnson", "0000200406"),
    # ... (full list from before — all 100+)
}

def fetch_financials(cik):
    url = BASE_URL.format(cik.zfill(10))
    headers = {"User-Agent": USER_AGENT}
    try:
        data = requests.get(url, headers=headers, timeout=10).json()
        facts = data.get("facts", {}).get("us-gaap", {})

        rev_tag = facts.get("Revenues") or facts.get("SalesRevenueNet")
        ni_tag = facts.get("NetIncomeLoss") or facts.get("ProfitLoss")
        if not rev_tag or not ni_tag: return None, None, None, None

        rev_units = rev_tag.get("units", {}).get("USD", [])
        ni_units = ni_tag.get("units", {}).get("USD", [])
        annual_revs = [v for v in rev_units if v.get("form") in ["10-K", "20-F"]]
        annual_nis = [v for v in ni_units if v.get("form") in ["10-K", "20-F"]]
        if not annual_revs or not annual_nis: return None, None, None, None

        latest_rev = max(annual_revs, key=lambda x: x["end"])
        latest_ni = max(annual_nis, key=lambda x: x["end"])

        total_rev = latest_rev["val"]
        net_income = latest_ni["val"]
        end_date = latest_rev["end"][:10]

        # === ESTIMATE CONSUMER REVENUE ===
        consumer_rev = total_rev
        if cik == "0001018724":  # Amazon
            consumer_rev = total_rev - 190000000000  # ~$190B AWS
        elif cik == "0000320193":  # Apple
            consumer_rev = total_rev - 85000000000   # ~$85B Services
        elif cik == "0001652044":  # Google
            consumer_rev = total_rev - 240000000000  # ~$240B Ads
        # Add more as needed

        return total_rev, net_income, consumer_rev, end_date
    except:
        return None, None, None, None

results = []
for ticker, (name, cik) in COMPANIES.items():
    total_rev, ni, consumer_rev, end_date = fetch_financials(cik)
    if total_rev and ni and total_rev > 0:
        te = (1 - ni / total_rev) * 100
        cte = (1 - ni / consumer_rev) * 100 if consumer_rev > 0 else None
        results.append({
            "Rank": 0, "Ticker": ticker, "Company": name, "Period End": end_date,
            "Revenue ($B)": round(total_rev / 1e9, 2),
            "Net Income ($B)": round(ni / 1e9, 2),
            "TE (%)": round(te, 2),
            "CTE (%)": round(cte, 2) if cte else "N/A",
            "Consumer Insight": f"{round(te,1)}¢ TE | {round(cte,1)}¢ CTE" if cte else f"{round(te,1)}¢ TE"
        })

if results:
    df = pd.DataFrame(results).sort_values("TE (%)", ascending=False)
    df["Rank"] = range(1, len(df) + 1)
    df.to_json("docs/te100_latest.json", orient="records", indent=2)
    df.to_csv("docs/te100_latest.csv", index=False)
