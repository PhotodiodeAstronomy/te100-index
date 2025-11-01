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
    "HD": ("Home Depot", "0000354951"),
    "LOW": ("Lowe's", "0000060914"),
    "DG": ("Dollar General", "0000027419"),
    "DLTR": ("Dollar Tree", "0000935703"),
    "BJ": ("BJ's Wholesale", "0001531152"),
    "MSFT": ("Microsoft", "0000789019"),
    "GOOGL": ("Alphabet", "0001652044"),
    "META": ("Meta", "0001326801"),
    "NVDA": ("NVIDIA", "0001045810"),
    "TSLA": ("Tesla", "0001318605"),
    "BRK-B": ("Berkshire Hathaway", "0001067983"),
    "LLY": ("Eli Lilly", "0000059478"),
    "AVGO": ("Broadcom", "0001101239"),
    "JPM": ("JPMorgan Chase", "0000019617"),
    "V": ("Visa", "0001403161"),
    "UNH": ("UnitedHealth", "0000731766"),
    "XOM": ("ExxonMobil", "0000034088"),
    "MA": ("Mastercard", "0001141391"),
    "PG": ("Procter & Gamble", "0000080424"),
    "JNJ": ("Johnson & Johnson", "0000200406"),
    "ABBV": ("AbbVie", "0001551152"),
    "CVX": ("Chevron", "0000093410"),
    "CRM": ("Salesforce", "0001108524"),
    "MRK": ("Merck", "0000310158"),
    "LIN": ("Linde", "0001707925"),
    "NEE": ("NextEra Energy", "0000753309"),
    "AMD": ("AMD", "0000002488"),
    "TMO": ("Thermo Fisher", "0000097745"),
    "BAC": ("Bank of America", "0000070858"),
    "ACN": ("Accenture", "0001467373"),
    "ABT": ("Abbott", "0000001800"),
    "DHR": ("Danaher", "0000313616"),
    "KO": ("Coca-Cola", "0000021344"),
    "NFLX": ("Netflix", "0001065280"),
    "DIS": ("Disney", "0001744489"),
    "TXN": ("Texas Instruments", "0000097476"),
    "ORCL": ("Oracle", "0001341439"),
    "PFE": ("Pfizer", "0000078003"),
    "PM": ("Philip Morris", "0001413329"),
    "INTC": ("Intel", "0000050863"),
    "VZ": ("Verizon", "0000732712"),
    "CSCO": ("Cisco", "0000858877"),
    "CAT": ("Caterpillar", "0000018230"),
    "AMGN": ("Amgen", "0000318154"),
    "QCOM": ("Qualcomm", "0000804328"),
    "HON": ("Honeywell", "0000773840"),
    "RTX": ("RTX", "0000101829"),
    "UNP": ("Union Pacific", "0000100517"),
    "IBM": ("IBM", "0000051143"),
    "GS": ("Goldman Sachs", "0000886982"),
    "SPGI": ("S&P Global", "0000064040"),
    "NOW": ("ServiceNow", "0001373715"),
    "GE": ("GE", "0000040545"),
    "ADBE": ("Adobe", "0000796343"),
    "BKNG": ("Booking", "0001075531"),
    "BLK": ("BlackRock", "0001364742"),
    "NKE": ("Nike", "0000320187"),
    "SYK": ("Stryker", "0000796949"),
    "UPS": ("UPS", "0001090727"),
    "LMT": ("Lockheed Martin", "0000936468"),
    "TJX": ("TJX", "0001091986"),
    "AMT": ("American Tower", "0001053507"),
    "MDT": ("Medtronic", "0001613103"),
    "VRTX": ("Vertex", "0000875320"),
    "ELV": ("Elevance Health", "0001156039"),
    "COP": ("ConocoPhillips", "0001163165"),
    "BMY": ("Bristol Myers", "0000014272"),
    "GILD": ("Gilead", "0000882095"),
    "MU": ("Micron", "0000723125"),
    "ZTS": ("Zoetis", "0001555280"),
    "REGN": ("Regeneron", "0001131227"),
    "SBUX": ("Starbucks", "0000829224"),
    "ADI": ("Analog Devices", "0000006281"),
    "MMC": ("Marsh & McLennan", "0000062709"),
    "SCHW": ("Charles Schwab", "0000316709"),
    "PGR": ("Progressive", "0000315700"),
    "CB": ("Chubb", "0000896159"),
    "MDLZ": ("Mondelez", "0001193125"),
    "T": ("AT&T", "0000732717"),
    "MO": ("Altria", "0000764180"),
    "PLD": ("Prologis", "0001045609"),
    "HUM": ("Humana", "0000049071"),
    "CME": ("CME Group", "0001156375"),
    "DE": ("Deere", "0000315189"),
    "ITW": ("Illinois Tool Works", "0000049826"),
    "BDX": ("Becton Dickinson", "0000010795"),
    "SO": ("Southern Company", "0000092122"),
    "DUK": ("Duke Energy", "0001326160"),
    "D": ("Dominion Energy", "0000715957"),
    "WM": ("Waste Management", "0000823768"),
    "ETN": ("Eaton", "0001551182"),
    "EOG": ("EOG Resources", "0000821189"),
    "SLB": ("Schlumberger", "0000087347"),
    "AON": ("Aon", "0000315293"),
    "MCD": ("McDonald's", "0000063908"),
    "USB": ("U.S. Bancorp", "0000036104"),
    "APD": ("Air Products", "0000002969"),
    "ECL": ("Ecolab", "0000031462"),
    "SHW": ("Sherwin-Williams", "0000089800"),
    "ROP": ("Roper", "0000880622"),
    "GD": ("General Dynamics", "0000040533"),
    "PCAR": ("PACCAR", "0000075362"),
    "AFL": ("Aflac", "0000004977"),
    "ADM": ("ADM", "0000007084"),
    "PSA": ("Public Storage", "0001393311"),
    "OXY": ("Occidental", "0000797460"),
    "FIS": ("Fidelity National", "0000798354"),
    "CCI": ("Crown Castle", "0001051470"),
    "AIG": ("AIG", "0000005272"),
    "KLAC": ("KLA", "0000319201"),
    "SPG": ("Simon Property", "0001063761"),
    "FCX": ("Freeport-McMoRan", "0000831259"),
    "BA": ("Boeing", "0000012927"),
    "STZ": ("Constellation Brands", "0000016918"),
    "COF": ("Capital One", "0000927628"),
    "FDX": ("FedEx", "0001048911"),
    "PPG": ("PPG", "0000079879"),
    "TT": ("Trane Technologies", "0001466258"),
    "C": ("Citigroup", "0000831001"),
    "NSC": ("Norfolk Southern", "0000702165"),
    "TRV": ("Travelers", "0000018717"),
    "WFC": ("Wells Fargo", "0000072971"),
    "BEN": ("Franklin Resources", "0000038777"),
    "DOW": ("Dow", "0001751788"),
    "KMB": ("Kimberly-Clark", "0000055785"),
    "HPQ": ("HP", "0000047217"),
    "EMR": ("Emerson", "0000032604"),
    "PNC": ("PNC", "0000713676"),
    "MS": ("Morgan Stanley", "0000895421"),
    "ZBH": ("Zimmer Biomet", "0001136869"),
    "CTAS": ("Cintas", "0000723254"),
    "VFC": ("VF Corp", "0000103379"),
    "ALL": ("Allstate", "0000899051"),
    "CVS": ("CVS Health", "0000064803")
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
