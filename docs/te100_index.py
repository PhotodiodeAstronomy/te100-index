# docs/te100_index.py - FINAL TE + CTE (100+ companies, NO SYNTAX ERRORS)
import requests
import pandas as pd
from datetime import datetime

USER_AGENT = "TE100 Index (contact@example.com)"
BASE_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json"

# === FULL 100+ COMPANIES ===
COMPANIES = {
    "WMT": ("Walmart", "0000104169"), "COST": ("Costco", "0000909832"),
    "AMZN": ("Amazon", "0001018724"), "AAPL": ("Apple", "0000320193"),
    "KR": ("Kroger", "0000056873"), "TGT": ("Target", "0000027419"),
    "HD": ("Home Depot", "0000354951"), "LOW": ("Lowe's", "0000060914"),
    "DG": ("Dollar General", "0000027419"), "DLTR": ("Dollar Tree", "0000935703"),
    "BJ": ("BJ's", "0001531152"), "MSFT": ("Microsoft", "0000789019"),
    "GOOGL": ("Alphabet", "0001652044"), "META": ("Meta", "0001326801"),
    "NVDA": ("NVIDIA", "0001045810"), "TSLA": ("Tesla", "0001318605"),
    "BRK-B": ("Berkshire", "0001067983"), "LLY": ("Eli Lilly", "0000059478"),
    "AVGO": ("Broadcom", "0001101239"), "JPM": ("JPMorgan", "0000019617"),
    "V": ("Visa", "0001403161"), "UNH": ("UnitedHealth", "0000731766"),
    "XOM": ("Exxon", "0000034088"), "MA": ("Mastercard", "0001141391"),
    "PG": ("P&G", "0000080424"), "JNJ": ("J&J", "0000200406"),
    "ABBV": ("AbbVie", "0001551152"), "CVX": ("Chevron", "0000093410"),
    "CRM": ("Salesforce", "0001108524"), "MRK": ("Merck", "0000310158"),
    "LIN": ("Linde", "0001707925"), "NEE": ("NextEra", "0000753309"),
    "AMD": ("AMD", "0000002488"), "TMO": ("Thermo Fisher", "0000097745"),
    "BAC": ("Bank of America", "0000070858"), "ACN": ("Accenture", "0001467373"),
    "ABT": ("Abbott", "0000001800"), "DHR": ("Danaher", "0000313616"),
    "KO": ("Coca-Cola", "0000021344"), "NFLX": ("Netflix", "0001065280"),
    "DIS": ("Disney", "0001744489"), "TXN": ("Texas Inst.", "0000097476"),
    "ORCL": ("Oracle", "0001341439"), "PFE": ("
