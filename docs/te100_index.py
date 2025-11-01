# docs/te100_index.py - FINAL TE + CTE (100% WORKING)
import requests
import pandas as pd

USER_AGENT = "TE100 Index (contact@example.com)"
BASE_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json"

# === FULL 100+ COMPANIES (ONE LINE EACH) ===
COMPANIES = {
    "WMT": ("Walmart", "0000104169"), "COST": ("Costco", "0000909832"), "AMZN": ("Amazon", "0001018724"),
    "AAPL": ("Apple", "0000320193"), "KR": ("Kroger", "0000056873"), "TGT": ("Target", "0000027419"),
    "HD": ("Home Depot", "0000354951"), "LOW": ("Lowe's", "0000060914"), "DG": ("Dollar General", "0000027419"),
    "DLTR": ("Dollar Tree", "0000935703"), "BJ": ("BJ's", "0001531152"), "MSFT": ("Microsoft", "0000789019"),
    "GOOGL": ("Alphabet", "0001652044"), "META": ("Meta", "0001326801"), "NVDA": ("NVIDIA", "0001045810"),
    "TSLA": ("Tesla", "0001318605"), "BRK-B": ("Berkshire", "0001067983"), "LLY": ("Eli Lilly", "0000059478"),
    "AVGO": ("Broadcom", "0001101239"), "JPM": ("JPMorgan", "0000019617"), "V": ("Visa", "0001403161"),
    "UNH": ("UnitedHealth", "0000731766"), "XOM": ("Exxon", "0000034088"), "MA": ("Mastercard", "0001141391"),
    "PG": ("P&G", "0000080424"), "JNJ": ("J&J", "0000200406"), "ABBV": ("AbbVie", "0001551152"),
    "CVX": ("Chevron", "0000093410"), "CRM": ("Salesforce", "0001108524"), "MRK": ("Merck", "0000310158"),
    "LIN": ("Linde", "0001707925"), "NEE": ("NextEra", "0000753309"), "AMD": ("AMD", "0000002488"),
    "TMO": ("Thermo Fisher", "0000097745"), "BAC": ("Bank of America", "0000070858"), "ACN": ("Accenture", "0001467373"),
    "ABT": ("Abbott", "0000001800"), "DHR": ("Danaher", "0000313616"), "KO": ("Coca-Cola", "0000021344"),
    "NFLX": ("Netflix", "0001065280"), "DIS": ("Disney", "0001744489"), "TXN": ("Texas Inst.", "0000097476"),
    "ORCL": ("Oracle", "0001341439"), "PFE": ("Pfizer", "0000078003"), "PM": ("Philip Morris", "0001413329"),
    "INTC": ("Intel", "0000050863"), "VZ": ("Verizon", "0000732712"), "CSCO": ("Cisco", "0000858877"),
    "CAT": ("Caterpillar", "0000018230"), "AMGN": ("Amgen", "0000318154"), "QCOM": ("Qualcomm", "0000804328"),
    "HON": ("Honeywell", "0000773840"), "RTX": ("RTX", "0000101829"), "UNP": ("Union Pacific", "0000100517"),
    "IBM": ("IBM", "0000051143"), "GS": ("Goldman", "0000886982"), "SPGI": ("S&P Global", "0000064040"),
    "NOW": ("ServiceNow", "0001373715"), "GE": ("GE", "0000040545"), "ADBE": ("Adobe", "0000796343"),
    "BKNG": ("Booking", "0001075531"), "BLK": ("BlackRock", "0001364742"), "NKE": ("Nike", "0000320187"),
    "SYK": ("Stryker", "0000796949"), "UPS": ("UPS", "0001090727"), "LMT": ("Lockheed", "0000936468"),
    "TJX": ("TJX", "0001091986"), "AMT": ("American Tower", "0001053507"), "MDT": ("Medtronic", "0001613103"),
    "VRTX": ("Vertex", "0000875320"), "ELV": ("Elevance", "0001156039"), "COP": ("Conoco", "0001163165"),
    "BMY": ("Bristol Myers", "0000014272"), "GILD": ("Gilead", "0000882095"), "MU": ("Micron", "0000723125"),
    "ZTS": ("Zoetis", "0001555280"), "REGN": ("Regeneron", "0001131227"), "SBUX": ("Starbucks", "0000829224"),
    "ADI": ("Analog", "0000006281"), "MMC": ("Marsh", "0000062709"), "SCHW": ("Schwab", "0000316709"),
    "PGR": ("Progressive", "0000315700"), "CB": ("Chubb", "0000896159"), "MDLZ": ("Mondelez", "0001193125"),
    "T": ("AT&T", "0000732717"), "MO": ("Altria", "0000764180"), "PLD": ("Prologis", "0001045609"),
    "HUM": ("Humana", "0000049071"), "CME": ("CME Group", "0001156375"), "DE": ("Deere", "0000315189"),
    "ITW": ("Illinois Tool", "0000049826"), "BDX": ("Becton", "0000010795"), "SO": ("Southern Co", "0000092122"),
    "DUK": ("Duke", "0001326160"), "WM": ("Waste Mgmt", "0000823768"), "ETN": ("Eaton", "0001551182"),
    "EOG": ("EOG", "0000821189"), "SLB": ("Schlumberger", "0000087347"), "AON": ("Aon", "0000315293"),
    "MCD": ("McDonald's", "0000063908"), "USB": ("U.S. Bancorp", "0000036104"), "APD": ("Air Products", "0000002969"),
    "ECL": ("Ecolab", "0000031462"), "SHW": ("Sherwin", "0000089800"), "ROP": ("Roper", "0000880622"),
    "GD": ("General Dynamics", "0000040533"), "PCAR": ("PACCAR", "0000075362"), "AFL": ("Aflac", "0000004977"),
    "ADM": ("ADM", "0000007084"), "PSA": ("Public Storage", "0001393311"), "OXY": ("Occidental", "0000797460"),
    "FIS": ("Fidelity", "0000798354"), "CCI": ("Crown Castle", "0001051470"), "AIG": ("AIG", "0000005272"),
    "KLAC": ("KLA", "0000319201"), "SPG": ("Simon", "0001063761"), "FCX": ("Freeport", "0000831259"),
    "BA": ("Boeing", "0000012927"), "STZ": ("Constellation", "0000016918"), "COF": ("Capital One", "0000927628"),
    "FDX": ("FedEx", "0001048911"), "PPG": ("PPG", "0000079879"), "TT": ("Trane", "0001466258"),
    "C": ("Citigroup", "0000831001"), "NSC": ("Norfolk", "0000702165"), "TRV": ("Travelers", "0000018717"),
    "WFC": ("Wells Fargo", "0000072971"), "BEN": ("Franklin", "0000038777"), "DOW": ("Dow", "0001751788"),
    "KMB": ("Kimberly-Clark", "0000055785"), "HPQ": ("HP", "0000047217"), "EMR": ("Emerson", "0000032604"),
    "PNC": ("PNC", "0000713676"), "MS": ("Morgan Stanley", "0000895421"), "ZBH": ("Zimmer", "0001136869"),
    "CTAS": ("Cintas", "0000723254"), "VFC": ("VF Corp", "0000103379"), "ALL": ("Allstate", "0000899051"),
    "CVS": ("CVS Health", "0000064803")
}

def fetch_financials(cik):
    url = BASE_URL.format(cik.zfill(10))
    headers = {"User-Agent": USER_AGENT}
    try:
        data = requests.get(url, headers=headers, timeout=15).json()
        facts = data.get("facts", {}).get("us-gaap", {})

        # Revenue
        rev_tag = facts.get("Revenues") or facts.get("SalesRevenueNet") or facts.get("RevenueFromContractWithCustomerExcludingAssessedTax")
        if not rev_tag: return None, None, None, None
        rev_units = rev_tag.get("units", {}).get("USD", [])
        annual_revs = [v for v in rev_units if v.get("form") in ["10-K", "20-F"]]
        if not annual_revs: return None, None, None, None
        latest_rev = max(annual_revs, key=lambda x: x["end"])
        total_rev = latest_rev["val"]
        end_date = latest_rev["end"][:10]

        # Net Income
        ni_tag = facts.get("NetIncomeLoss") or facts.get("ProfitLoss")
        if not ni_tag: return total_rev, None, total_rev, end_date
        ni_units = ni_tag.get("units", {}).get("USD", [])
        annual_nis = [v for v in ni_units if v.get("form") in ["10-K", "20-F"]]
        if not annual_nis: return total_rev, None, total_rev, end_date
        latest_ni = max(annual_nis, key=lambda x: x["end"])
        net_income = latest_ni["val"]

        # CONSUMER REVENUE
        consumer_rev = total_rev
        if cik == "0001018724": consumer_rev -= 190000000000  # Amazon AWS
        elif cik == "0000320193": consumer_rev -= 85000000000   # Apple Services
        elif cik == "0001652044": consumer_rev -= 240000000000  # Google Ads
        elif cik == "0001326801": consumer_rev -= 134000000000  # Meta Ads
        elif cik == "0000789019": consumer_rev -= 88000000000   # Microsoft Cloud
        elif cik == "0001744489": consumer_rev -= 29000000000   # Disney Parks

        return total_rev, net_income, consumer_rev, end_date
    except Exception as e:
        print(f"Error {cik}: {e}")
        return None, None, None, None

results = []
for ticker, (name, cik) in COMPANIES.items():
    total_rev, ni, consumer_rev, end_date = fetch_financials(cik)
    if total_rev and ni and total_rev > 0:
        te = (1 - ni / total_rev) * 100
        cte = (1 - ni / consumer_rev) * 100 if consumer_rev > 0 else te
        results.append({
            "Rank": 0, "Ticker": ticker, "Company": name, "Period End": end_date,
            "Revenue ($B)": round(total_rev / 1e9, 2),
            "Consumer Rev ($B)": round(consumer_rev / 1e9, 2),
            "Net Income ($B)": round(ni / 1e9, 2),
            "TE (%)": round(te, 2),
            "CTE (%)": round(cte, 2),
            "Insight": f"{round(te,1)}¢ TE | {round(cte,1)}¢ CTE"
        })

if results:
    df = pd.DataFrame(results).sort_values("TE (%)", ascending=False)
    df["Rank"] = range(1, len(df) + 1)
    df.to_json("docs/te100_latest.json", orient="records", indent=2)
    df.to_csv("docs/te100_latest.csv", index=False)
    print(f"Success: {len(df)} companies")
