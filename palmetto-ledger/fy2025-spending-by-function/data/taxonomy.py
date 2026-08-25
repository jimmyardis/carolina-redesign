#!/usr/bin/env python3
"""
Palmetto Ledger — FY2025 function taxonomy, v3.
v1 -> v2: added IT keywords found in unclassified residual.
v2 -> v3: expanded from 9 to 17 operational categories; fixed known misses
(GASOLINE, LEASED CAR, INSURANCE-STATE); dissolved Communications into
Telecommunications; split Construction (roads vs buildings), IT (systems vs
telecom), Fleet (vehicles vs travel), Facilities (utilities vs occupancy);
new: Marketing, Security, Testing/Research, Medical Services, Food, Printing
& Mail; routed single-agency education program codes to the aid tier.
Ordered rules, first match wins. Run with --audit to print per-category
top codes and the unclassified residual for spot-checking.
"""
import sys, re, pandas as pd

PASSTHROUGH_RULES = [
    ("Medicaid & Client Medical Assistance", [
        "MED SERVICES", "CASE SERVICES", "CLIENT PAYMENTS", "MEDICAID", "MD SRV", "MD SERV", "CLIENT SERVICES",
    ]),
    ("Aid to Schools, Local Governments & Districts", [
        "STATE AID", "AID SCH", "AID SCHOOL", "AID TO", "AID CNTYS", "AID COUNTIES",
        "AID ENTITIES", "AID-LOCAL", "AID TO DISTRICT", "AID MUNICIPALITIES",
        "ALLOC ", "ALLOCATIONS", "HEX ", "PASS THRU", "PASS-THRU", "TECH BOARD",
        "CERDEP", "SUMMER SCHOOL", "AID CNTY", "AID ST AGENCIES", "AID PRIVATE", "AID MUNIC", "STABILIZATION FUND", "FIRST STEPS", "READING COACHES", "SCHOOL RESOURCE OFFICERS",
        "CAREER & TECHNOLOGY EDUCATION", "ADULT EDUCATION",
        "CAPITAL FUNDING FOR DISADVANTAGED SCHOOLS", "PLANNING DISTRICTS",
        "AID PLANNING", "AID OTHER", "GRANT",
    ]),
    ("Employee Benefits, Retirement & Insurance Plans", [
        "INSURANCE - GROUP PLAN", "DISBURSEMENT - TRUST", "RETIREMENT",
        "INSURANCE - ADMINISTRATION FEE", "EMPLOYER CONTRIBUTIONS",
    ]),
    ("Scholarships & Assistance to Individuals", [
        "SCHOLARSHIP", "HOUSING ASSISTANCE", "TUITION ASSISTANCE", "STIPEND",
        "ALT PLACEMENT", "FOSTER",
    ]),
    ("Debt Service & Financial Obligations", [
        "PRINCIPAL", "INTEREST ON", "DEBT SERVICE", "LOANS AND NOTES",
        "BOND", "AMORTIZATION", "MASTER LEASE ASSET",
    ]),
]

OPERATIONAL_RULES = [
    # --- negated codes first: "NON-IT & NON-REAL ESTATE" must not match the
    # IT or Real Estate keywords it explicitly negates ---
    ("Professional & Contracted Services", [
        "NON-IT",
    ]),
    # --- claims first: settlements must not fall into legal/professional ---
    ("Insurance, Claims & Risk", [
        "INDEMNITY CLAIMS", "WORKERS COMPENSATION", "INSURANCE-NON STATE",
        "INSURANCE - PROPERTY", "TORT", "LIABILITY", "INSURANCE-STATE",
        "JUST CMP", "SETTLE", "SETTL", "VERDICT", "CLAIMS",
    ]),
    # --- roads before buildings: both mention construction ---
    ("Roads, Bridges & Highways", [
        "ROAD AND BRIDGE", "HIGHWAY MAINTENANCE", "HIGHWAY & ROAD", "HIGHWAYS",
        "BRIDGE", "PAVEMENT", "RESURFAC", "ASPHALT", "MOVING & ADJUSTING", "RAILROAD",
    ]),
    ("Buildings, Land & Capital Construction", [
        "CONSTRUCTION", "ENGINEERING & ARCHITECT", "ARCHITECTURAL", "RENOVATION",
        "CAPITAL IMPROVE", "LAND", "PERMANENT IMPROVEMENT", "UNDERGROUND STORAGE", "CAPITAL OUTLAY", "CAPITAL ASSETS",
    ]),
    # --- telecom before IT: phone codes contain generic tech words ---
    ("Telecommunications & Connectivity", [
        "TELEPHONE", "TELECOM", "CELLULAR", "DATA NETWORK", "VOICE NETWORK", "NETWORK, CIRCUIT", "COMM EQUIP", "COMMUNICATION",
        "POSTAL", "COURIER",
    ]),
    # NOTE: bare "IT" needs word-boundary handling (see classify) — the v1/v2
    # keyword "IT " silently matched "NONPROFIT " and "NON-IT ", misfiling
    # ~$960M of non-IT contract spend into IT. Found in the v3 audit.
    ("Contracts with Governments & Nonprofits", [
        "CONTRACT AGREEMENTS WITH GOVT", "AGREEMENTS WITH GOVT/NONPROFIT",
    ]),
    ("Information Technology", [
        "APPLICATION", "SOFTWARE", "COMPUTER", "SERVER", "CLOUD",
        "LICENSE - IT", "INFORMATION TECH", "SYSTEMS", "INFORMATION SECURITY",
        "DP SERVICES", "END-USER COMPUTING", "PROGRAMS & LICENCES",
        "PROGRAMS & LICENSES", "PRINT & COPY",
    ]),
    # --- marketing before printing: promotional printing is marketing ---
    ("Marketing, Promotion & Public Information", [
        "PROMOTIONAL", "ADVERTISING", "MARKETING", "PUBLICITY", "PUBLIC RELATION",
        "EXHIBIT",
    ]),
    ("Printing, Postage & Mail", [
        "PRINTED ITEMS", "POSTAGE", "PRINTING", "MAIL", "FREIGHT",
    ]),
    ("Utilities", [
        "UTILITIES", "ELECTRICITY", "WATER & SEWER", "NATURAL GAS", "GARBAGE",
    ]),
    ("Rent, Leases & Facilities Operations", [
        "REAL ESTATE", "RENT", "LEASE BUILD", "LEASE - BUILD", "JANITORIAL", "HVAC", "GROUNDS",
        "BUILDING MAINT", "FACILITY", "MOWING",
    ]),
    ("Security & Protective Services", [
        "SECURITY SERV", "SECURITY CONTRACT", "GUARD",
    ]),
    ("Medical & Health Services (operational)", [
        "MEDICAL & HEALTH", "PSYCHIATRIC", "DENTAL SERV", "PHARMACY SERV",
        "NURSING SERV", "LABORATORY SERV",
    ]),
    ("Testing, Research & Appraisal", [
        "TESTING SERVICES", "RESEARCH SURVEY", "APPRAIS", "LABORATORY ANALYSIS",
    ]),
    # --- travel before fleet: subsistence/lodging aren't vehicles ---
    ("Travel, Lodging & Per Diem", [
        "TRAVEL", "SUBSISTENCE", "LODGING", "MEALS", "AIRFARE", "MILEAGE",
        "REGISTRATION FEE",
    ]),
    ("Vehicles, Fuel & Fleet", [
        "MOTOR VEHICLE", "FLEET", "FUEL", "GASOLINE", "LEASED CAR", "BUSES",
        "VEHICLE", "AVIATION", "WATERCRAFT", "AIRCRAFT", "HELICOPTER",
    ]),
    ("Food & Provisions", [
        "FOOD", "DIETARY", "MEAL SERVICE",
    ]),
    ("Professional & Contracted Services", [
        "NON-IT", "PROFESS SERVICES", "PROFESSIONAL SERV", "OTHER CONTRACT SERVICES",
        "OTHER CONTRACTUAL SERVICES", "CONTRACTUAL SERVICES", "CONTRACT AGREEMENTS", "CONSULT", "LEGAL",
        "AUDIT ACCOUNTING FINANCE", "TEMPORARY SERVICES", "MANAGEMENT SERV",
        "SRVCS,MAINT&WARR",
    ]),
    ("Supplies, Equipment & Materials", [
        "SUPPLIES", "INSTRUCTIONAL MATERIALS", "UNIFORM", "EQUIPMENT", "FURNISHINGS", "LOW VALUE ASSETS", "PURCHASED RESALE",
        "FURNITURE", "INVENTORY",
    ]),
    ("Personnel, Training & Memberships", [
        "CLASS POS", "UNCLASS POS", "SALAR", "WAGES", "OVERTIME", "DUES",
        "TRAINING", "EDUCATION - EMPLOYEE", "TUITION REIMB", "RECRUIT",
        "EMPLOYEE AWARD",
    ]),
]


def classify(name):
    if not isinstance(name, str):
        return ("Unclassified", "Unclassified")
    u = name.upper()
    # standalone word "IT" (not NON-IT, not the tail of NONPROFIT) => IT
    IT_WORD = re.search(r"(?<![A-Z-])IT(?![A-Z])", u) is not None
    for area, keys in PASSTHROUGH_RULES:
        for k in keys:
            if k.upper() in u:
                return ("Formula & Transfers", area)
    for area, keys in OPERATIONAL_RULES:
        for k in keys:
            if k.upper() in u:
                return ("Operational", area)
    if IT_WORD:
        return ("Operational", "Information Technology")
    return ("Unclassified", "Unclassified")


def load():
    df = pd.read_pickle('/home/claude/.tmp/zbb/fy25.pkl')
    codes = df[['acct', 'acct_name']].drop_duplicates(subset=['acct'])
    codes[['tier', 'fa']] = codes['acct_name'].apply(lambda n: pd.Series(classify(n)))
    return df.merge(codes[['acct', 'tier', 'fa']], on='acct', how='left'), codes


if __name__ == "__main__":
    df, codes = load()
    if "--audit" in sys.argv:
        print("== CATEGORY TOTALS ==")
        t = df.groupby(['tier', 'fa']).agg(spend=('amt', 'sum'),
                                           agencies=('agency', 'nunique'))
        t = t.join(codes.groupby(['tier', 'fa']).size().rename('codes'))
        print(t.sort_values(['tier', 'spend'], ascending=[True, False])
               .assign(spend=lambda d: (d.spend/1e6).round(1)).to_string())
        print("\n== TOP CODES PER OPERATIONAL CATEGORY (spot-check) ==")
        ops = df[df.tier == 'Operational']
        for fa in ops.fa.unique():
            top = (ops[ops.fa == fa].groupby('acct_name').amt.sum()
                   .sort_values(ascending=False).head(6))
            print(f"\n[{fa}]")
            for n, v in top.items():
                print(f"   {n[:64]:<66} ${v/1e6:>8.1f}M")
        print("\n== REMAINING UNCLASSIFIED (top 30) ==")
        u = (df[df.tier == 'Unclassified'].groupby('acct_name')
             .agg(spend=('amt', 'sum'), agencies=('agency', 'nunique'))
             .sort_values('spend', ascending=False))
        print(f"codes: {len(u)}   dollars: ${u.spend.sum()/1e6:.0f}M "
              f"({u.spend.sum()/df.amt.sum()*100:.1f}%)")
        print(u.head(30).assign(spend=lambda d: (d.spend/1e6).round(2)).to_string())
