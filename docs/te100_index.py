# te100_index.py - Auto-run daily
import requests, json, pandas as pd
from datetime import datetime

USER_AGENT = "TE100 Index contact@example.com"
EDGAR_BASE = "https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json"

# Top 10 companies (we'll expand later)
COMPANIES = {
    "WMT": ("Walmart", "0000104169"),
    "COST": ("Costco", "0000909832"),
    "AMZN": ("Amazon", "0001018724"),
    "AAPL": ("Apple", "0000320193"),
    "KR": ("Kroger", "0000056873"),
    "TGT": ("Target", "0000027419"),
    "HD": ("Home Depot", "0000354951"),
    "LOW": ("Lowe's", "0000060914"),
    "DG": ("Dollar General", "0000027419"),
    "DLTR": ("Dollar Tree", "0000935703")
}

def fetch_financials(cik):
    url = EDGAR_BASE.format(cik.zfill(10))
    headers = {"User-Agent": USER_AGENT}
    try:
        data = requests.get(url, headers=headers, timeout=10).json()
        facts = data['facts']['us-gaap']
        
        # Get latest annual
        revs = [v for v in facts.get('Revenues', {}).get('units', {}).get('USD', []) if 'fy' in v.get('form', '')]
        nis = [v for v in facts.get('NetIncomeLoss', {}).get('units', {}).get('USD', []) if 'fy' in v.get('form', '')]
        
        if not revs or not nis: return None, None, None
        rev = max(revs, key=lambda x: x['end'])['val']
        ni = max(nis, key=lambda x: x['end'])['val']
        end = max(revs, key=lambda x: x['end'])['end']
        return rev, ni, end
    except:
        return None, None, None

results = []
for ticker, (name, cik) in COMPANIES.items():
    rev, ni, end = fetch_financials(cik)
    if rev and ni and rev > 0:
        te = (1 - ni/rev) * 100
        results.append({
            "Rank": 0,
            "Ticker": ticker,
            "Company": name,
            "Period End": end[:10],
            "Revenue ($B)": round(rev / 1e9, 2),
            "Net Income ($B)": round(ni / 1e9, 2),
            "TE (%)": round(te, 2),
            "Consumer Insight": f"{round(te,1)}¢ of $1 becomes real value"
        })

df = pd.DataFrame(results).sort_values("TE (%)", ascending=False)
df["Rank"] = range(1, len(df) + 1)
df.to_json("docs/te100_latest.json", orient="records", indent=2)
df.to_csv("docs/te100_latest.csv", index=False)

print(f"TE 100 Updated: {datetime.now()}")
