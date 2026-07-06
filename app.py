import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import io
import re
import subprocess
import tempfile
from pathlib import Path
from difflib import SequenceMatcher
import numpy as np
from PIL import Image, ImageEnhance

st.set_page_config(page_title="Portfolio Tracker", page_icon="📈", layout="wide")

ASSETS = [
    {"name": "Savings", "category": "Savings", "subcategory": "Savings", "bucket": "Savings", "pac": 0, "active": "No"},
    {"name": "Core MSCI World", "category": "ETF", "subcategory": "ETF Stock", "bucket": "Stocks", "pac": 1020, "active": "Yes"},
    {"name": "AI & Big Data", "category": "ETF", "subcategory": "ETF Stock", "bucket": "Stocks", "pac": 224, "active": "Yes"},
    {"name": "Physical Gold", "category": "ETF", "subcategory": "ETF Gold", "bucket": "Defensive", "pac": 120, "active": "Yes"},
    {"name": "Global Gov Bond", "category": "ETF", "subcategory": "ETF Bond", "bucket": "Defensive", "pac": 0, "active": "Yes"},
    {"name": "Euro Inflation Linked Gov Bond", "category": "ETF", "subcategory": "ETF Bond", "bucket": "Defensive", "pac": 28, "active": "Yes"},
    {"name": "Core EUR Corp Bond", "category": "ETF", "subcategory": "ETF Bond", "bucket": "Defensive", "pac": 32, "active": "Yes"},
    {"name": "MSCI World Value", "category": "ETF", "subcategory": "ETF Stock", "bucket": "Stocks", "pac": 268, "active": "Yes"},
    {"name": "MSCI EM", "category": "ETF", "subcategory": "ETF Stock", "bucket": "Stocks", "pac": 248, "active": "Yes"},
    {"name": "Defence Tech", "category": "ETF", "subcategory": "ETF Stock", "bucket": "Stocks", "pac": 60, "active": "Yes"},
]

MONTH_END_SEED = [
    ("Oct/25", "Savings", 34010.01), ("Oct/25", "Core MSCI World", 11058), ("Oct/25", "AI & Big Data", 3265),
    ("Oct/25", "Physical Gold", 1792), ("Oct/25", "Global Gov Bond", 1456), ("Oct/25", "Core EUR Corp Bond", 1456),
    ("Oct/25", "MSCI World Value", 1439), ("Oct/25", "MSCI EM", 1233), ("Oct/25", "Defence Tech", 483.20),
    ("Nov/25", "Savings", 35690.22), ("Nov/25", "Core MSCI World", 11303), ("Nov/25", "AI & Big Data", 3177),
    ("Nov/25", "Physical Gold", 1875), ("Nov/25", "Global Gov Bond", 1470), ("Nov/25", "Core EUR Corp Bond", 1478),
    ("Nov/25", "MSCI World Value", 1499), ("Nov/25", "MSCI EM", 1225), ("Nov/25", "Defence Tech", 383.76),
    ("Dec/25", "Savings", 37889.16), ("Dec/25", "Core MSCI World", 11866), ("Dec/25", "AI & Big Data", 3256),
    ("Dec/25", "Physical Gold", 2001), ("Dec/25", "Global Gov Bond", 1547), ("Dec/25", "Core EUR Corp Bond", 1534),
    ("Dec/25", "MSCI World Value", 1651), ("Dec/25", "MSCI EM", 1306), ("Dec/25", "Defence Tech", 402.89),
    ("Jan/26", "Savings", 38095), ("Jan/26", "Core MSCI World", 12365), ("Jan/26", "AI & Big Data", 3215),
    ("Jan/26", "Physical Gold", 2214), ("Jan/26", "Global Gov Bond", 1568), ("Jan/26", "Core EUR Corp Bond", 1592),
    ("Jan/26", "MSCI World Value", 1824), ("Jan/26", "MSCI EM", 1419), ("Jan/26", "Defence Tech", 452.33),
    ("Feb/26", "Savings", 37801), ("Feb/26", "Core MSCI World", 13001), ("Feb/26", "AI & Big Data", 3108),
    ("Feb/26", "Physical Gold", 2540), ("Feb/26", "Global Gov Bond", 1640), ("Feb/26", "Core EUR Corp Bond", 1649),
    ("Feb/26", "MSCI World Value", 2007), ("Feb/26", "MSCI EM", 1544), ("Feb/26", "Defence Tech", 450.32),
    ("Mar/26", "Savings", 39883), ("Mar/26", "Core MSCI World", 13914), ("Mar/26", "AI & Big Data", 2970),
    ("Mar/26", "Physical Gold", 2493), ("Mar/26", "Global Gov Bond", 1666), ("Mar/26", "Core EUR Corp Bond", 1679),
    ("Mar/26", "MSCI World Value", 2387), ("Mar/26", "MSCI EM", 2033), ("Mar/26", "Defence Tech", 439.71),
]

MANUAL_SEED = [
    ("Oct/25", "Core MSCI World", 690.40), ("Oct/25", "AI & Big Data", 101), ("Oct/25", "Physical Gold", 70),
    ("Oct/25", "Global Gov Bond", 52), ("Oct/25", "Core EUR Corp Bond", 54), ("Oct/25", "MSCI World Value", 196.99),
    ("Oct/25", "MSCI EM", 44), ("Nov/25", "Core MSCI World", 486), ("Nov/25", "Physical Gold", 70),
    ("Nov/25", "Global Gov Bond", 52), ("Nov/25", "Core EUR Corp Bond", 54), ("Nov/25", "MSCI World Value", 96),
    ("Nov/25", "MSCI EM", 44), ("Dec/25", "Core MSCI World", 486), ("Dec/25", "Physical Gold", 70),
    ("Dec/25", "Global Gov Bond", 52), ("Dec/25", "Core EUR Corp Bond", 54), ("Dec/25", "MSCI World Value", 96),
    ("Dec/25", "MSCI EM", 44), ("Jan/26", "Core MSCI World", 486), ("Jan/26", "Physical Gold", 70),
    ("Jan/26", "Global Gov Bond", 52), ("Jan/26", "Core EUR Corp Bond", 54), ("Jan/26", "MSCI World Value", 96),
    ("Jan/26", "MSCI EM", 44), ("Feb/26", "Core MSCI World", 486), ("Feb/26", "Physical Gold", 70),
    ("Feb/26", "Global Gov Bond", 52), ("Feb/26", "Core EUR Corp Bond", 54), ("Feb/26", "MSCI World Value", 96),
    ("Feb/26", "MSCI EM", 44), ("Mar/26", "Core MSCI World", 1539.76), ("Mar/26", "Physical Gold", 220.99),
    ("Mar/26", "Global Gov Bond", 52), ("Mar/26", "Core EUR Corp Bond", 54), ("Mar/26", "MSCI World Value", 497),
    ("Mar/26", "MSCI EM", 645.99),
]

MONTHS = [
    "Oct/25", "Nov/25", "Dec/25", "Jan/26", "Feb/26", "Mar/26",
    "Apr/26", "May/26", "Jun/26", "Jul/26", "Aug/26", "Sep/26",
    "Oct/26", "Nov/26", "Dec/26"
]

MONTH_MAP = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

APP_DIR = Path(__file__).resolve().parent
STATE_FILE = APP_DIR / "portfolio_state.json"
LEGACY_XLSX_FILE = APP_DIR / "data.xlsx"
GOOGLE_STATE_WORKSHEET = "portfolio_state"


def month_sort_value(label: str) -> int:
    month, year = label.split("/")
    return (2000 + int(year)) * 100 + MONTH_MAP[month]


def month_label_to_timestamp(label: str) -> pd.Timestamp:
    month, year = label.split("/")
    return pd.Timestamp(year=2000 + int(year), month=MONTH_MAP[month], day=1)


def month_value_to_label(value) -> str:
    ts = pd.to_datetime(value)
    return ts.strftime("%b/%y")


def eur0(value: float) -> str:
    sign = "-" if value < 0 else ""
    value = abs(float(value))
    s = f"{value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sign}€ {s}"


def pct1(value: float) -> str:
    return f"{value:.1f}%"


def perf_color(value):
    if value is None or pd.isna(value):
        return "#94a3b8"
    return "#22c55e" if value >= 0 else "#ef4444"


def perf_arrow(value):
    if value is None or pd.isna(value):
        return ""
    return "↗" if value >= 0 else "↘"


def seed_data():
    assets_df = pd.DataFrame(ASSETS)
    month_end_df = pd.DataFrame(MONTH_END_SEED, columns=["month", "asset", "value"])
    month_end_df["value"] = pd.to_numeric(month_end_df["value"], errors="coerce").fillna(0.0)
    manual_df = pd.DataFrame(MANUAL_SEED, columns=["month", "asset", "amount"])
    manual_df["amount"] = pd.to_numeric(manual_df["amount"], errors="coerce").fillna(0.0)

    pac_rows = []
    for month in MONTHS:
        if month_sort_value(month) >= month_sort_value("Apr/26"):
            for _, row in assets_df[assets_df["category"] == "ETF"].iterrows():
                pac_rows.append({
                    "month": month,
                    "asset": row["name"],
                    "mode": "Auto" if float(row["pac"]) > 0 else "No",
                    "amount": float(row["pac"]),
                })
    pac_df = pd.DataFrame(pac_rows)
    return assets_df, month_end_df, manual_df, pac_df


def ensure_pac_rows(assets_df, pac_df):
    pac_df = pac_df.copy()
    if pac_df.empty:
        pac_df = pd.DataFrame(columns=["month", "asset", "mode", "amount"])

    existing = set()
    if not pac_df.empty:
        existing = set(zip(pac_df["month"], pac_df["asset"]))

    pac_rows = []
    etf_df = assets_df[assets_df["category"] == "ETF"]
    for month in MONTHS:
        if month_sort_value(month) < month_sort_value("Apr/26"):
            continue
        for _, row in etf_df.iterrows():
            key = (month, row["name"])
            if key in existing:
                continue
            pac_rows.append(
                {
                    "month": month,
                    "asset": row["name"],
                    "mode": "Auto" if float(row["pac"]) > 0 else "No",
                    "amount": float(row["pac"]),
                }
            )

    if pac_rows:
        pac_df = pd.concat([pac_df, pd.DataFrame(pac_rows)], ignore_index=True)

    return pac_df


def normalize_state_frames(assets_df, month_end_df, manual_df, pac_df):
    assets_df = assets_df.copy()
    month_end_df = month_end_df.copy()
    manual_df = manual_df.copy()
    pac_df = pac_df.copy()

    if assets_df.empty:
        assets_df = pd.DataFrame(columns=["name", "category", "subcategory", "bucket", "pac", "active"])
    if month_end_df.empty:
        month_end_df = pd.DataFrame(columns=["month", "asset", "value"])
    if manual_df.empty:
        manual_df = pd.DataFrame(columns=["month", "asset", "amount"])
    if pac_df.empty:
        pac_df = pd.DataFrame(columns=["month", "asset", "mode", "amount"])

    assets_df["pac"] = pd.to_numeric(assets_df.get("pac"), errors="coerce").fillna(0.0)

    if not month_end_df.empty:
        month_end_df["value"] = pd.to_numeric(month_end_df["value"], errors="coerce").fillna(0.0)
        month_end_df["sort"] = month_end_df["month"].apply(month_sort_value)
        month_end_df = month_end_df.sort_values(["sort", "asset"]).drop(columns="sort").reset_index(drop=True)

    if not manual_df.empty:
        manual_df["amount"] = pd.to_numeric(manual_df["amount"], errors="coerce").fillna(0.0)
        manual_df["sort"] = manual_df["month"].apply(month_sort_value)
        manual_df = manual_df.sort_values(["sort", "asset"]).drop(columns="sort").reset_index(drop=True)

    pac_df = ensure_pac_rows(assets_df, pac_df)
    if not pac_df.empty:
        pac_df["amount"] = pd.to_numeric(pac_df["amount"], errors="coerce").fillna(0.0)
        pac_df["sort"] = pac_df["month"].apply(month_sort_value)
        pac_df = pac_df.sort_values(["sort", "asset"]).drop(columns="sort").reset_index(drop=True)

    return assets_df, month_end_df, manual_df, pac_df


def normalize_performance_df(performance_df):
    performance_df = performance_df.copy()
    if performance_df.empty:
        return pd.DataFrame(columns=["month", "asset", "performance"])
    for col in ["month", "asset", "performance"]:
        if col not in performance_df.columns:
            performance_df[col] = np.nan
    performance_df = performance_df[["month", "asset", "performance"]].copy()
    performance_df["performance"] = pd.to_numeric(performance_df["performance"], errors="coerce")
    performance_df = performance_df.dropna(subset=["month", "asset", "performance"])
    performance_df["sort"] = performance_df["month"].apply(month_sort_value)
    return performance_df.sort_values(["sort", "asset"]).drop(columns="sort").reset_index(drop=True)


def normalize_asset_name(value: str) -> str:
    value = str(value or "").lower()
    value = value.replace("&", " and ")
    value = re.sub(r"\b(usd|eur|acc|brokerage|etfs|topics)\b", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    if value.startswith("al big data"):
        value = value.replace("al big data", "ai big data", 1)
    return value


def parse_euro_amount(value: str):
    match = re.search(r"(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?)\s*€?", value)
    if not match:
        return None
    raw = match.group(1).strip()
    if "." in raw and "," in raw:
        normalized = raw.replace(".", "").replace(",", ".")
    elif "," in raw:
        decimals = raw.split(",")[-1]
        normalized = raw.replace(".", "").replace(",", ".") if len(decimals) <= 2 else raw.replace(",", "")
    elif "." in raw:
        decimals = raw.split(".")[-1]
        normalized = raw.replace(".", "") if len(decimals) == 3 else raw
    else:
        normalized = raw
    try:
        return float(normalized)
    except ValueError:
        return None


def looks_like_asset_line(value: str) -> bool:
    cleaned = value.strip()
    if not cleaned:
        return False
    if "%" in cleaned:
        return False
    if parse_euro_amount(cleaned) is not None and " " not in cleaned:
        return False
    lowered = cleaned.lower()
    if lowered in {"brokerage", "etfs and topics"}:
        return False
    return any(ch.isalpha() for ch in cleaned)


def clean_ocr_line(value: str) -> str:
    value = re.sub(r"^[^A-Za-z0-9]+", "", value.strip())
    value = re.sub(r"[^A-Za-z0-9€%&().,\-+\s]+$", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def preprocess_etf_image(image_bytes: bytes) -> Image.Image:
    image = Image.open(io.BytesIO(image_bytes)).convert("L")
    width, height = image.size
    cropped = image.crop((int(width * 0.04), int(height * 0.08), int(width * 0.78), int(height * 0.97)))
    enlarged = cropped.resize((cropped.width * 2, cropped.height * 2))
    contrasted = ImageEnhance.Contrast(enlarged).enhance(2.8)
    sharpened = ImageEnhance.Sharpness(contrasted).enhance(2.0)
    thresholded = sharpened.point(lambda px: 255 if px > 85 else 0)
    return thresholded


def run_tesseract_ocr(image: Image.Image, psm: int) -> str:
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        temp_path = Path(tmp.name)
    try:
        image.save(temp_path)
        result = subprocess.run(
            ["tesseract", str(temp_path), "stdout", "--psm", str(psm)],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    finally:
        temp_path.unlink(missing_ok=True)


@st.cache_resource
def get_rapidocr_engine():
    from rapidocr_onnxruntime import RapidOCR

    return RapidOCR()


@st.cache_resource
def get_google_vision_client():
    from google.cloud import vision
    from google.oauth2 import service_account

    service_account_info = dict(st.secrets["google_service_account"])
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    return vision.ImageAnnotatorClient(credentials=credentials)


def run_rapidocr_lines(image: Image.Image):
    engine = get_rapidocr_engine()
    result, _ = engine(np.array(image))
    if not result:
        return []
    return [item[1] for item in result if len(item) >= 2 and item[1]]


def run_google_vision_lines(image: Image.Image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")

    from google.cloud import vision

    client = get_google_vision_client()
    response = client.document_text_detection(image=vision.Image(content=buffered.getvalue()))
    if response.error.message:
        raise RuntimeError(response.error.message)
    if not response.full_text_annotation or not response.full_text_annotation.text:
        return []
    return response.full_text_annotation.text.splitlines()


def parse_ocr_pairs(ocr_text: str):
    rows = []
    pending_name = None
    for raw_line in ocr_text.splitlines():
        line = clean_ocr_line(raw_line)
        if not line:
            continue
        if "%" in line:
            continue
        amount = parse_euro_amount(line)
        if amount is not None and pending_name:
            rows.append({"raw_name": pending_name, "value": amount})
            pending_name = None
            continue
        if looks_like_asset_line(line):
            pending_name = line
    return rows


def match_extracted_assets(extracted_rows, etf_assets):
    normalized_assets = {asset: normalize_asset_name(asset) for asset in etf_assets}
    matched = []
    unmatched = []
    used_assets = set()

    for row in extracted_rows:
        raw_name = row["raw_name"]
        normalized_raw = normalize_asset_name(raw_name)
        scored = []
        for asset, normalized_asset in normalized_assets.items():
            score = SequenceMatcher(None, normalized_raw, normalized_asset).ratio()
            if normalized_raw in normalized_asset or normalized_asset in normalized_raw:
                score += 0.1
            scored.append((score, asset))
        scored.sort(reverse=True)
        best_score, best_asset = scored[0]
        if best_score >= 0.6 and best_asset not in used_assets:
            used_assets.add(best_asset)
            matched.append(
                {
                    "asset": best_asset,
                    "raw_name": raw_name,
                    "value": row["value"],
                    "match_score": round(min(best_score, 1.0), 2),
                }
            )
        else:
            unmatched.append({"raw_name": raw_name, "value": row["value"]})

    return matched, unmatched


def extract_etf_values_from_image(image_bytes: bytes, etf_assets):
    processed = preprocess_etf_image(image_bytes)
    attempts = []
    for psm in (4, 6, 11):
        try:
            ocr_text = run_tesseract_ocr(processed, psm)
        except FileNotFoundError:
            if get_storage_backend() == "google_sheets":
                try:
                    vision_lines = run_google_vision_lines(processed)
                except Exception as exc:
                    return None, None, f"Google Vision OCR failed: {exc}"
                parsed_rows = parse_ocr_pairs("\n".join(vision_lines))
                matched, unmatched = match_extracted_assets(parsed_rows, etf_assets)
                return matched, unmatched, None

            try:
                rapidocr_lines = run_rapidocr_lines(processed)
            except Exception as exc:
                return None, None, f"OCR fallback failed: {exc}"
            parsed_rows = parse_ocr_pairs("\n".join(rapidocr_lines))
            matched, unmatched = match_extracted_assets(parsed_rows, etf_assets)
            return matched, unmatched, None
        except subprocess.CalledProcessError as exc:
            return None, None, exc.stderr.strip() or "OCR failed."
        parsed_rows = parse_ocr_pairs(ocr_text)
        attempts.append((len(parsed_rows), parsed_rows))

    parsed_rows = max(attempts, key=lambda item: item[0])[1] if attempts else []
    matched, unmatched = match_extracted_assets(parsed_rows, etf_assets)
    return matched, unmatched, None


def calc_month_perf(asset, month, month_end_map, pac_map, manual_map):
    idx = MONTHS.index(month)
    if idx == 0:
        return None
    prev = MONTHS[idx - 1]
    end = month_end_map.get((month, asset), 0)
    prev_end = month_end_map.get((prev, asset), 0)
    flow = pac_map.get((month, asset), 0) + manual_map.get((month, asset), 0)
    if prev_end > 0 and end > 0:
        pnl = end - prev_end - flow
        return pnl / prev_end * 100
    if prev_end == 0 and end > 0 and flow != 0:
        return (end - flow) / abs(flow) * 100
    return None


def calc_month_value_change(asset, month, month_end_map):
    idx = MONTHS.index(month)
    if idx == 0:
        return None
    prev = MONTHS[idx - 1]
    end = month_end_map.get((month, asset), 0)
    prev_end = month_end_map.get((prev, asset), 0)
    if prev_end > 0 and end > 0:
        return (end - prev_end) / prev_end * 100
    return None


def calc_month_net_move(asset, month, month_end_map, pac_map, manual_map):
    idx = MONTHS.index(month)
    if idx == 0:
        return None
    prev = MONTHS[idx - 1]
    end = month_end_map.get((month, asset), 0)
    prev_end = month_end_map.get((prev, asset), 0)
    flow = pac_map.get((month, asset), 0) + manual_map.get((month, asset), 0)
    if end > 0 or prev_end > 0 or flow != 0:
        return end - prev_end - flow
    return None


def state_payload(backup_ts=None):
    return {
        "assets": st.session_state.assets_df.to_dict(orient="records"),
        "month_end": st.session_state.month_end_df.to_dict(orient="records"),
        "manual": st.session_state.manual_df.to_dict(orient="records"),
        "pac": st.session_state.pac_df.to_dict(orient="records"),
        "etf_performance": st.session_state.performance_df.to_dict(orient="records"),
        "backup_ts": backup_ts,
    }


def state_to_json() -> str:
    """Serialize current session state to JSON string, including backup timestamp."""
    from datetime import datetime
    data = state_payload(backup_ts=datetime.now().strftime("%Y-%m-%d %H:%M"))
    return json.dumps(data, indent=2)


def apply_state_payload(data):
    assets_df = pd.DataFrame(data["assets"])
    month_end_df = pd.DataFrame(data["month_end"])
    manual_df = pd.DataFrame(data["manual"])
    pac_df = pd.DataFrame(data["pac"])
    performance_df = pd.DataFrame(data.get("etf_performance", []))
    assets_df, month_end_df, manual_df, pac_df = normalize_state_frames(
        assets_df, month_end_df, manual_df, pac_df
    )
    st.session_state.assets_df = assets_df
    st.session_state.month_end_df = month_end_df
    st.session_state.manual_df = manual_df
    st.session_state.pac_df = pac_df
    st.session_state.performance_df = normalize_performance_df(performance_df)


def get_storage_backend() -> str:
    try:
        has_account = "google_service_account" in st.secrets
        has_sheet = "google_sheet_id" in st.secrets
        if has_account and has_sheet:
            return "google_sheets"
    except Exception:
        pass
    return "local_file"


def get_storage_label() -> str:
    if get_storage_backend() == "google_sheets":
        return f"Google Sheets `{st.secrets['google_sheet_id']}`"
    return f"Local file `{STATE_FILE.name}`"


@st.cache_resource
def get_google_sheet():
    import gspread

    service_account_info = dict(st.secrets["google_service_account"])
    client = gspread.service_account_from_dict(service_account_info)
    return client.open_by_key(st.secrets["google_sheet_id"])


def load_state_from_google_sheet():
    try:
        sheet = get_google_sheet()
        worksheet = sheet.worksheet(GOOGLE_STATE_WORKSHEET)
        raw = worksheet.acell("B2").value
        if not raw:
            return "Google Sheet is empty."
        return load_state_from_json(raw)
    except Exception as e:
        return str(e)


def persist_state_to_google_sheet():
    try:
        payload = state_payload()
        sheet = get_google_sheet()
        try:
            worksheet = sheet.worksheet(GOOGLE_STATE_WORKSHEET)
        except Exception:
            worksheet = sheet.add_worksheet(title=GOOGLE_STATE_WORKSHEET, rows=10, cols=2)

        worksheet.update(
            "A1:B4",
            [
                ["key", "value"],
                ["state_json", json.dumps(payload)],
                ["updated_at", pd.Timestamp.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")],
                ["source", "streamlit_app"],
            ],
        )
        return None
    except Exception as e:
        return str(e)


def persist_state_to_disk():
    try:
        payload = state_payload()
        tmp_path = STATE_FILE.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp_path.replace(STATE_FILE)
        return None
    except Exception as e:
        return str(e)


def load_state_from_json(raw: str):
    """Load session state from JSON string. Returns error string or None."""
    try:
        data = json.loads(raw)
        apply_state_payload(data)
        return None
    except Exception as e:
        return str(e)


def persist_state():
    if get_storage_backend() == "google_sheets":
        return persist_state_to_google_sheet()
    return persist_state_to_disk()


def load_state_from_excel(path: Path):
    try:
        assets_src = pd.read_excel(path, sheet_name="Assets")
        month_end_src = pd.read_excel(path, sheet_name="Month_End")
        manual_src = pd.read_excel(path, sheet_name="Transactions_Manual")
        pac_src = pd.read_excel(path, sheet_name="Transactions_PAC")

        assets_df = assets_src.rename(
            columns={
                "Asset": "name",
                "Category": "category",
                "Subcategory": "subcategory",
                "Bucket": "bucket",
                "Monthly_PAC": "pac",
                "Active?": "active",
            }
        )[["name", "category", "subcategory", "bucket", "pac", "active"]]

        month_end_df = month_end_src.rename(
            columns={"Month": "month", "Asset": "asset", "End_Value": "value"}
        )[["month", "asset", "value"]]
        if not month_end_df.empty:
            month_end_df["month"] = month_end_df["month"].apply(month_value_to_label)

        manual_df = manual_src.rename(
            columns={"Month": "month", "Asset": "asset", "Amount": "amount"}
        )[["month", "asset", "amount"]]
        if not manual_df.empty:
            manual_df["month"] = manual_df["month"].apply(month_value_to_label)

        pac_rows = []
        if not pac_src.empty:
            pac_src = pac_src.copy()
            pac_src["month"] = pac_src["Month"].apply(month_value_to_label)
            for (month, asset), group in pac_src.groupby(["month", "Asset"], dropna=False):
                statuses = {str(v).strip() for v in group["Status"].fillna("Auto").tolist()}
                planned = pd.to_numeric(group["Planned_Amount"], errors="coerce")
                actual = pd.to_numeric(group["Actual_Amount"], errors="coerce")
                flow_used = pd.to_numeric(group["Flow_Used"], errors="coerce")

                if statuses == {"No"}:
                    mode = "No"
                    amount = 0.0
                elif "Edited" in statuses:
                    mode = "Edited"
                    amount = float(actual.fillna(flow_used).fillna(planned).fillna(0.0).sum())
                else:
                    mode = "Auto"
                    amount = float(flow_used.fillna(planned).fillna(actual).fillna(0.0).sum())

                pac_rows.append({"month": month, "asset": asset, "mode": mode, "amount": amount})

        pac_df = pd.DataFrame(pac_rows, columns=["month", "asset", "mode", "amount"])
        apply_state_payload(
            {
                "assets": assets_df.to_dict(orient="records"),
                "month_end": month_end_df.to_dict(orient="records"),
                "manual": manual_df.to_dict(orient="records"),
                "pac": pac_df.to_dict(orient="records"),
                "etf_performance": [],
            }
        )
        return None
    except Exception as e:
        return str(e)


def _latest_data_month() -> str:
    """Returns the latest month label that has any month-end data."""
    me = st.session_state.month_end_df
    if me.empty:
        return MONTHS[0]
    months_present = me["month"].unique().tolist()
    months_present.sort(key=month_sort_value)
    return months_present[-1]


def _next_entry_month() -> str:
    latest = _latest_data_month()
    latest_idx = MONTHS.index(latest)
    return MONTHS[min(latest_idx + 1, len(MONTHS) - 1)]


if "assets_df" not in st.session_state:
    load_err = None
    if get_storage_backend() == "google_sheets":
        load_err = load_state_from_google_sheet()
        if load_err is None:
            st.session_state.data_source = GOOGLE_STATE_WORKSHEET
    elif STATE_FILE.exists():
        load_err = load_state_from_json(STATE_FILE.read_text(encoding="utf-8"))
        if load_err is None:
            st.session_state.data_source = STATE_FILE.name
    if "assets_df" not in st.session_state and LEGACY_XLSX_FILE.exists():
        load_err = load_state_from_excel(LEGACY_XLSX_FILE)
        if load_err is None:
            st.session_state.data_source = LEGACY_XLSX_FILE.name
            persist_state()
    if "assets_df" not in st.session_state:
        assets_df, month_end_df, manual_df, pac_df = seed_data()
        assets_df, month_end_df, manual_df, pac_df = normalize_state_frames(
            assets_df, month_end_df, manual_df, pac_df
        )
        st.session_state.assets_df = assets_df
        st.session_state.month_end_df = month_end_df
        st.session_state.manual_df = manual_df
        st.session_state.pac_df = pac_df
        st.session_state.performance_df = pd.DataFrame(columns=["month", "asset", "performance"])
        st.session_state.data_source = "seed_data"
    if load_err:
        st.session_state.init_load_error = load_err

# track last backup timestamp across downloads
if "last_backup_ts" not in st.session_state:
    st.session_state.last_backup_ts = None
if "last_modified_ts" not in st.session_state:
    st.session_state.last_modified_ts = None
if "performance_df" not in st.session_state:
    st.session_state.performance_df = pd.DataFrame(columns=["month", "asset", "performance"])
if "data_source" not in st.session_state:
    st.session_state.data_source = GOOGLE_STATE_WORKSHEET if get_storage_backend() == "google_sheets" else (STATE_FILE.name if STATE_FILE.exists() else "seed_data")
if "init_load_error" not in st.session_state:
    st.session_state.init_load_error = None

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💾 Backup & Restore")
    st.caption(f"Storage attivo: {get_storage_label()}")
    st.caption(f"Sorgente iniziale caricata: `{st.session_state.data_source}`")
    if st.session_state.init_load_error:
        st.error(f"Init load error: {st.session_state.init_load_error}")

    latest_dm = _latest_data_month()
    last_ts = st.session_state.last_backup_ts

    # status badge
    last_mod = st.session_state.last_modified_ts
    if last_ts is None and last_mod is None:
        st.info("💾 No data saved yet")
    elif last_ts is None and last_mod is not None:
        st.error(f"🔴 Unsaved changes! Data modified: **{last_mod}**")
    elif last_mod is not None and last_mod > last_ts:
        st.error(f"🔴 Backup outdated!\nModified: **{last_mod}**\nLast backup: **{last_ts}**")
    else:
        st.success(f"✅ Up to date — last backup: **{last_ts}**")

    # Download backup
    backup_json = state_to_json()
    filename = f"portfolio_backup_{latest_dm.replace('/', '-')}.json"
    if st.download_button(
        label="⬇️ Save backup",
        data=backup_json,
        file_name=filename,
        mime="application/json",
        use_container_width=True,
    ):
        from datetime import datetime
        st.session_state.last_backup_ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.rerun()

    st.markdown("---")

    # Upload backup
    uploaded = st.file_uploader("⬆️ Load backup", type="json", key="backup_upload", label_visibility="collapsed")
    if uploaded is not None:
        err = load_state_from_json(uploaded.read().decode("utf-8"))
        if err:
            st.error(f"Error loading backup: {err}")
        else:
            persist_err = persist_state()
            if persist_err:
                st.error(f"Auto-save error: {persist_err}")
            else:
                from datetime import datetime
                st.session_state.last_backup_ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.success("Backup restored!")
                st.rerun()

# ── MAIN ──────────────────────────────────────────────────────────────────────
assets_df = st.session_state.assets_df.copy()
month_end_df = st.session_state.month_end_df.copy()
manual_df = st.session_state.manual_df.copy()
pac_df = st.session_state.pac_df.copy()
performance_df = normalize_performance_df(st.session_state.performance_df.copy())

all_assets = assets_df["name"].tolist()
etf_assets = assets_df.loc[assets_df["category"] == "ETF", "name"].tolist()

st.markdown(
    """
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1.25rem;
    max-width: 1500px;
}
.stSelectbox label {
    font-size: 13px !important;
    color: #cbd5e1 !important;
}
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
    min-height: 44px !important;
}
div[data-baseweb="tag"] {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
}
.kpi-card {
    background: linear-gradient(180deg, rgba(15,23,42,0.92), rgba(17,24,39,0.88));
    border: 1px solid rgba(148,163,184,0.16);
    border-radius: 18px;
    padding: 16px 16px;
    min-height: 108px;
    box-shadow: 0 14px 32px rgba(0,0,0,0.24), inset 0 1px 0 rgba(255,255,255,0.04);
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.kpi-label {
    font-size: 12px;
    color: #94a3b8;
    margin-bottom: 10px;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.kpi-value {
    font-size: 24px;
    line-height: 1.1;
    font-weight: 700;
    color: #f8fafc;
    white-space: nowrap;
    text-align: center;
}
.kpi-pos { color: #16a34a; }
.kpi-neg { color: #dc2626; }
.etf-row-card {
    background: linear-gradient(180deg, rgba(15,23,42,0.56), rgba(15,23,42,0.38));
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 12px;
    padding: 8px 12px;
    margin-bottom: 6px;
}
.etf-name {
    font-size: 15px;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1.15;
}
.etf-sub {
    font-size: 11px;
    color: #94a3b8;
    margin-top: 2px;
}
.etf-perf-head {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #94a3b8;
    text-align: center;
    margin-bottom: 2px;
}
.etf-perf-pos {
    font-size: 18px;
    font-weight: 700;
    color: #22c55e;
    text-align: center;
}
.etf-perf-neg {
    font-size: 18px;
    font-weight: 700;
    color: #ef4444;
    text-align: center;
}
.etf-perf-na {
    font-size: 18px;
    font-weight: 700;
    color: #94a3b8;
    text-align: center;
}
.spark-head {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #94a3b8;
    margin-bottom: 4px;
}
</style>
""",
    unsafe_allow_html=True,
)

header_left, header_right = st.columns([8, 1.6])
with header_left:
    st.title("Portfolio Tracker")
with header_right:
    st.markdown("##### Selected month")
    selected_month = st.selectbox(
        "Selected month",
        options=MONTHS,
        index=MONTHS.index(_latest_data_month()),
        label_visibility="collapsed",
    )

st.caption("Month end update, PAC confirmation, manual transactions and add ETF")

month_end_map = {(r.month, r.asset): float(r.value) for r in month_end_df.itertuples(index=False)}
manual_map = manual_df.groupby(["month", "asset"], dropna=False)["amount"].sum().to_dict() if not manual_df.empty else {}

pac_effective = pac_df.copy()
pac_effective["effective_amount"] = pac_effective.apply(lambda r: 0 if r["mode"] == "No" else float(r["amount"]), axis=1)
pac_map = pac_effective.groupby(["month", "asset"])["effective_amount"].sum().to_dict() if not pac_effective.empty else {}
performance_map = performance_df.groupby(["month", "asset"], dropna=False)["performance"].last().to_dict() if not performance_df.empty else {}

selected_idx = MONTHS.index(selected_month)
prev_month = MONTHS[selected_idx - 1] if selected_idx > 0 else None

rows = []
for _, asset_row in assets_df.iterrows():
    asset = asset_row["name"]
    end_value = month_end_map.get((selected_month, asset), 0)
    prev_end = month_end_map.get((prev_month, asset), 0) if prev_month else 0
    pac_flow = pac_map.get((selected_month, asset), 0)
    manual_flow = manual_map.get((selected_month, asset), 0)
    total_flow = pac_flow + manual_flow

    pnl = None
    perf_pct = None
    if end_value != 0 and prev_end != 0:
        pnl = end_value - prev_end - total_flow
        base = prev_end + total_flow / 2
        if base != 0:
            perf_pct = pnl / base * 100

    rows.append({
        "Asset": asset,
        "Category": asset_row["category"],
        "Bucket": asset_row["bucket"],
        "Subcategory": asset_row["subcategory"],
        "End Value": end_value,
        "Prev End": prev_end,
        "PAC Flow": pac_flow,
        "Manual Flow": manual_flow,
        "Total Flow": total_flow,
        "PnL": pnl,
        "Perf %": perf_pct,
    })

summary_df = pd.DataFrame(rows)

portfolio_total = float(summary_df["End Value"].sum())
savings_total = float(summary_df.loc[summary_df["Category"] == "Savings", "End Value"].sum())
etf_total = portfolio_total - savings_total
monthly_etf_transactions = float(summary_df.loc[summary_df["Category"] == "ETF", "Total Flow"].sum())
etf_abs_perf = float(summary_df.loc[(summary_df["Category"] == "ETF") & summary_df["PnL"].notna(), "PnL"].sum())

etf_prev_end = float(summary_df.loc[summary_df["Category"] == "ETF", "Prev End"].sum())
etf_total_flow = float(summary_df.loc[summary_df["Category"] == "ETF", "Total Flow"].sum())
etf_perf_pct = None
if etf_prev_end > 0:
    etf_perf_pct = etf_abs_perf / (etf_prev_end + etf_total_flow / 2) * 100


def render_kpi(col, title, value, tone="default"):
    cls = "kpi-value"
    if tone == "pos":
        cls += " kpi-pos"
    elif tone == "neg":
        cls += " kpi-neg"
    col.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{title}</div>
            <div class="{cls}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


k1, k2, k3, k4, k5, k6 = st.columns(6)
render_kpi(k1, "Portfolio Total", eur0(portfolio_total))
render_kpi(k2, "ETF Total", eur0(etf_total))
render_kpi(k3, "Savings", eur0(savings_total))
render_kpi(k4, "Monthly ETF Transactions", eur0(monthly_etf_transactions))

k5_value = f"{eur0(etf_abs_perf)} <span style='margin-left:8px; vertical-align:middle;'>{perf_arrow(etf_abs_perf)}</span>"
k6_value = "-" if etf_perf_pct is None else f"{pct1(etf_perf_pct)} <span style='margin-left:8px; vertical-align:middle;'>{perf_arrow(etf_perf_pct)}</span>"

render_kpi(k5, "ETF Abs Performance", k5_value, "pos" if etf_abs_perf >= 0 else "neg")
render_kpi(k6, "ETF % Performance", k6_value, "default" if etf_perf_pct is None else ("pos" if etf_perf_pct >= 0 else "neg"))

st.write("")

p1, p2, p3 = st.columns([0.92, 0.92, 1.46], vertical_alignment="top")

with p1:
    st.markdown("<h3 style='height:72px; margin:0; display:flex; align-items:flex-start;'>ETF vs Savings</h3>", unsafe_allow_html=True)
    split_df = pd.DataFrame({"Type": ["ETF", "Savings"], "Value": [etf_total, savings_total]})
    fig_split = go.Figure(data=[go.Pie(
        labels=split_df["Type"],
        values=split_df["Value"],
        hole=0.66,
        sort=False,
        direction="clockwise",
        rotation=180,
        marker=dict(colors=["#1f2937", "#9ca3af"]),
        textposition="inside",
        textinfo="percent"
    )])
    fig_split.update_traces(textfont_size=13, showlegend=True, insidetextorientation="horizontal")
    fig_split.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=34, b=28),
        legend=dict(orientation="h", y=-0.10, x=0.18, traceorder="normal", font=dict(size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_split, use_container_width=True, config={"displayModeBar": False})

with p2:
    st.markdown("<h3 style='height:72px; margin:0; display:flex; align-items:flex-start;'>ETF Stock vs<br>Defensive</h3>", unsafe_allow_html=True)
    bucket_df = summary_df[summary_df["Category"] == "ETF"].groupby("Bucket")["End Value"].sum().reset_index()
    bucket_df["Bucket"] = pd.Categorical(bucket_df["Bucket"], categories=["Stocks", "Defensive"], ordered=True)
    bucket_df = bucket_df.sort_values("Bucket")
    fig_bucket = go.Figure(data=[go.Pie(
        labels=bucket_df["Bucket"],
        values=bucket_df["End Value"],
        hole=0.66,
        sort=False,
        direction="clockwise",
        rotation=180,
        marker=dict(colors=["#334155", "#cbd5e1"]),
        textposition="inside",
        textinfo="percent"
    )])
    fig_bucket.update_traces(textfont_size=13, showlegend=True, insidetextorientation="horizontal")
    fig_bucket.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=34, b=28),
        legend=dict(orientation="h", y=-0.10, x=0.09, traceorder="normal", font=dict(size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_bucket, use_container_width=True, config={"displayModeBar": False})

with p3:
    st.markdown("<h3 style='height:72px; margin:0; display:flex; align-items:flex-start; justify-content:center;'>ETF Split</h3>", unsafe_allow_html=True)
    pie_df = summary_df[(summary_df["Category"] == "ETF") & (summary_df["End Value"] > 0)][["Asset", "End Value"]].copy()
    pie_colors = {
        "Core MSCI World": "#86c5f8",
        "AI & Big Data": "#1273de",
        "Physical Gold": "#f6a6a6",
        "MSCI World Value": "#ff3131",
        "MSCI EM": "#7ae39d",
        "Core EUR Corp Bond": "#33b4ad",
        "Global Gov Bond": "#f4c95d",
        "Euro Inflation Linked Gov Bond": "#8b5cf6",
        "Defence Tech": "#ff9800",
    }
    pie_df["Color"] = pie_df["Asset"].map(pie_colors)
    etf_split_total = pie_df["End Value"].sum()
    pie_df["Share"] = pie_df["End Value"] / etf_split_total * 100 if etf_split_total else 0
    pie_df["Chart Label"] = pie_df["Share"].apply(lambda value: f"{value:.1f}%" if value >= 5 else "")
    fig_pie = go.Figure(data=[go.Pie(
        labels=pie_df["Asset"],
        values=pie_df["End Value"],
        hole=0.58,
        sort=False,
        text=pie_df["Chart Label"],
        textinfo="text",
        textposition="inside",
        textfont_size=12,
        insidetextorientation="horizontal",
        marker=dict(colors=pie_df["Color"]),
        showlegend=False,
        customdata=[eur0(value) for value in pie_df["End Value"]],
        hovertemplate="%{label}<br>%{customdata}<br>%{percent}<extra></extra>",
    )])
    fig_pie.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=34, b=28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    legend_items = []
    for _, r in pie_df.iterrows():
        legend_items.append(
            f"<div title='{r['Asset']}' style='display:grid; grid-template-columns:12px minmax(0,1fr) auto; align-items:center; gap:8px; min-width:0;'><span style='display:inline-block; width:12px; height:12px; border-radius:0; background:{r['Color']};'></span><span style='font-size:11px; color:#e5e7eb; line-height:1.18; white-space:normal;'>{r['Asset']}</span><span style='font-size:10px; color:#94a3b8; white-space:nowrap;'>{r['Share']:.2f}%</span></div>"
        )
    legend_html = "".join(legend_items)
    st.markdown(
        f"<div style='display:grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap:10px 22px; margin-top:2px; width:100%;'>{legend_html}</div>",
        unsafe_allow_html=True,
    )

st.subheader("Portfolio Trend MoM")

trend_rows = []
trend_months = [
    month for month in MONTHS[: selected_idx + 1]
    if not month_end_df.loc[month_end_df["month"] == month].empty
]
for i, month in enumerate(trend_months):
    total = month_end_df.loc[month_end_df["month"] == month, "value"].sum()
    savings = month_end_df.loc[(month_end_df["month"] == month) & (month_end_df["asset"] == "Savings"), "value"].sum()
    etf = total - savings
    mom = None
    if i > 0:
        prev_total = trend_rows[-1]["Total"]
        if prev_total > 0:
            mom = (total - prev_total) / prev_total * 100
    trend_rows.append({"Month": month, "Savings": savings, "ETF": etf, "Total": total, "MoM %": mom})

trend_df = pd.DataFrame(trend_rows)

if not trend_df.empty:
    line_color = "#22c55e"
    if len(trend_df) >= 2 and trend_df.iloc[-1]["Total"] < trend_df.iloc[-2]["Total"]:
        line_color = "#ef4444"

    fig_combo = go.Figure()
    fig_combo.add_bar(
        x=trend_df["Month"],
        y=trend_df["ETF"],
        name="ETF",
        marker_color="#1f2937",
        width=0.30,
        text=[eur0(v) for v in trend_df["ETF"]],
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=12, color="#f8fafc")
    )
    fig_combo.add_bar(
        x=trend_df["Month"],
        y=trend_df["Savings"],
        name="Savings",
        marker_color="#9ca3af",
        width=0.30,
        text=[eur0(v) for v in trend_df["Savings"]],
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=12, color="#111827")
    )
    fig_combo.add_trace(
        go.Scatter(
            x=trend_df["Month"],
            y=trend_df["Total"],
            mode="lines+markers",
            name="Portfolio Total",
            line=dict(color=line_color, width=3, dash="dash"),
            marker=dict(size=7, color=line_color)
        )
    )

    total_label_y = trend_df["Total"] + (trend_df["Total"].max() * 0.004)
    fig_combo.add_trace(
        go.Scatter(
            x=trend_df["Month"],
            y=total_label_y,
            mode="text",
            text=[eur0(v) for v in trend_df["Total"]],
            textfont=dict(size=15, color="#f8fafc"),
            showlegend=False,
            hoverinfo="skip"
        )
    )

    pct_x, pct_y, pct_text = [], [], []
    for idx, row in trend_df.iterrows():
        if idx == 0 or pd.isna(row["MoM %"]):
            continue
        pct_x.append(row["Month"])
        pct_y.append(row["Total"] + (trend_df["Total"].max() * 0.075))
        pct_text.append(pct1(row["MoM %"]))

    fig_combo.add_trace(
        go.Scatter(
            x=pct_x,
            y=pct_y,
            mode="text",
            text=pct_text,
            textfont=dict(color="#cbd5e1", size=13),
            showlegend=False,
            hoverinfo="skip"
        )
    )

    fig_combo.update_layout(
        barmode="stack",
        height=440,
        bargap=0.62,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=1.08, x=0),
        yaxis_title="",
        xaxis_title="",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)"
    )
    fig_combo.update_yaxes(showgrid=True, gridcolor="rgba(203,213,225,0.18)", tickformat=",.0f")
    fig_combo.update_xaxes(showgrid=False)
    st.plotly_chart(fig_combo, use_container_width=True, config={"displayModeBar": False})

perf_mode = st.radio(
    "ETF monthly metric",
    ["Position move excl. contributions", "Position value change"],
    horizontal=True,
    label_visibility="collapsed",
    index=0,
)


def calc_selected_month_metric(asset, month):
    if perf_mode == "Position move excl. contributions":
        return calc_month_perf(asset, month, month_end_map, pac_map, manual_map)
    return calc_month_value_change(asset, month, month_end_map)


def selected_metric_label():
    if perf_mode == "Position move excl. contributions":
        return "position move excl. contributions"
    return "position value"


left_perf_col, right_track_col = st.columns([0.52, 0.48], vertical_alignment="top")

etf_perf_table = []
last_data_idx = max(
    (i for i, m in enumerate(MONTHS) if any(month_end_map.get((m, a), 0) > 0 for a in etf_assets)),
    default=selected_idx
)
months_5m_spark = MONTHS[max(0, last_data_idx - 4): last_data_idx + 1]
for asset in etf_assets:
    current_perf = calc_selected_month_metric(asset, selected_month)
    spark_vals, spark_months = [], []
    for m in months_5m_spark:
        p = calc_selected_month_metric(asset, m)
        if p is not None:
            spark_vals.append(p)
            spark_months.append(m)
    meta = assets_df.loc[assets_df["name"] == asset].iloc[0]
    etf_perf_table.append({
        "asset": asset,
        "subcategory": meta["subcategory"],
        "bucket": meta["bucket"],
        "current_perf": current_perf,
        "spark_months": spark_months,
        "spark_vals": spark_vals,
    })

etf_perf_table = sorted(etf_perf_table, key=lambda x: -999 if x["current_perf"] is None else x["current_perf"], reverse=True)

with left_perf_col:
    st.subheader("ETF Position Move")
    st.caption("Calculated from previous month value, current month buys/sells, and current month-end value. This is not the fund price return.")

    for row in etf_perf_table:
        asset = row["asset"]
        current_perf = row["current_perf"]
        spark_months = row["spark_months"]
        spark_vals = row["spark_vals"]

        outer1, outer2, outer3 = st.columns([0.52, 0.28, 0.88], gap="small", vertical_alignment="center")

        with outer1:
            st.markdown(
                f"""
                <div class="etf-row-card" style="padding:8px 12px; height:62px; display:flex; flex-direction:column; justify-content:center;">
                    <div class="etf-name">{asset}</div>
                    <div class="etf-sub">{row['bucket']} - {row['subcategory']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with outer2:
            perf_cls = "etf-perf-na"
            perf_text = "-"
            move_text = ""
            if current_perf is not None:
                perf_cls = "etf-perf-pos" if current_perf >= 0 else "etf-perf-neg"
                perf_text = f"{perf_arrow(current_perf)} {pct1(current_perf)}"
                net_move = calc_month_net_move(asset, selected_month, month_end_map, pac_map, manual_map)
                if perf_mode == "Position move excl. contributions" and net_move is not None:
                    move_text = f"<div class=\"etf-perf-head\">{eur0(net_move)}</div>"

            st.markdown(
                f"""
                <div class="etf-row-card" style="height:62px; display:flex; flex-direction:column; justify-content:center; align-items:center; padding:6px 10px; text-align:center;">
                    <div class="etf-perf-head">{selected_month}</div>
                    <div class="{perf_cls}">{perf_text}</div>
                    {move_text}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with outer3:
            st.markdown(f'<div class="spark-head" style="margin-bottom:2px; margin-top:2px;">{selected_metric_label().title()} %, last 5 months</div>', unsafe_allow_html=True)
            if len(spark_vals) >= 2:
                fig_spark = go.Figure()
                fig_spark.add_trace(go.Bar(
                    x=spark_months,
                    y=spark_vals,
                    marker_color=["#22c55e" if v >= 0 else "#ef4444" for v in spark_vals],
                    width=0.58,
                    showlegend=False,
                    hovertemplate="%{x}: %{y:.2f}%<extra></extra>",
                ))
                fig_spark.update_layout(
                    height=62,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False, zeroline=True, zerolinecolor="rgba(226,232,240,0.45)", zerolinewidth=1),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig_spark, use_container_width=True, config={"displayModeBar": False})
            else:
                st.caption("No performance data")

with right_track_col:
    st.subheader("MoM ETF Track")
    st.caption(f"Showing {perf_mode.lower()} by month.")

    months_with_data = [m for m in MONTHS if any(month_end_map.get((m, a), 0) > 0 for a in etf_assets)]

    def get_ytd_months(months_available):
        if not months_available:
            return []
        last = months_available[-1]
        yr = last.split("/")[1]
        return [m for m in months_available if m.split("/")[1] == yr]

    ytd_months = get_ytd_months(months_with_data)
    period_options = ["All"] + (["YTD"] if len(ytd_months) > 1 else []) + months_with_data

    fc1, fc2 = st.columns([1, 1])
    with fc1:
        selected_track_etfs = st.multiselect(
            "ETF selection",
            options=etf_assets,
            default=[x for x in ["Core MSCI World", "MSCI EM", "MSCI World Value", "Physical Gold"] if x in etf_assets],
        )
    with fc2:
        period_filter = st.selectbox(
            "Period",
            options=period_options,
            index=0,
            key="track_period_filter",
        )

    if period_filter == "All":
        months_to_show = months_with_data
    elif period_filter == "YTD":
        months_to_show = ytd_months
    else:
        m_idx = months_with_data.index(period_filter) if period_filter in months_with_data else 0
        months_to_show = months_with_data[max(0, m_idx - 1): m_idx + 1]

    mom_data = []
    for asset in selected_track_etfs:
        for m in months_to_show:
            p = calc_selected_month_metric(asset, m)
            if p is not None:
                mom_data.append({"Month": m, "Asset": asset, "Perf": p})

    mom_df = pd.DataFrame(mom_data)
    if not mom_df.empty:
        fig_track = px.line(mom_df, x="Month", y="Perf", color="Asset", markers=True)
        fig_track.update_traces(
            line=dict(width=2.4, shape="linear"),
            marker=dict(size=5),
            hovertemplate="%{fullData.name}<br>%{x}: %{y:.2f}%<extra></extra>",
        )
        fig_track.update_layout(
            height=430,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.02)",
            yaxis_title=f"{selected_metric_label().title()} %",
            xaxis_title="",
            legend=dict(orientation="h", y=-0.10, x=0),
        )
        fig_track.update_yaxes(showgrid=True, gridcolor="rgba(203,213,225,0.18)")
        st.plotly_chart(fig_track, use_container_width=True, config={"displayModeBar": False})

st.divider()

update_tab, pac_tab, manual_tab, asset_tab = st.tabs(
    ["Update Month End", "Confirm PAC", "Manual Transaction", "Add ETF"]
)

with update_tab:
    st.subheader("Insert month end values")
    draft_month = st.selectbox("Month to update", options=MONTHS, index=MONTHS.index(_next_entry_month()), key="draft_month_end")

    with st.form("month_end_form"):
        month_end_inputs = {}
        cols = st.columns(3)
        savings_assets = [asset for asset in all_assets if asset == "Savings"]
        ranked_etf_assets = sorted(
            [asset for asset in all_assets if asset != "Savings"],
            key=lambda asset: month_end_map.get((draft_month, asset), 0),
            reverse=True,
        )
        ordered_assets = savings_assets + ranked_etf_assets

        for i, asset in enumerate(ordered_assets):
            current_value = month_end_map.get((draft_month, asset), 0)
            with cols[i % 3]:
                month_end_inputs[asset] = st.number_input(
                    asset,
                    min_value=0.0,
                    value=float(current_value),
                    step=100.0,
                    format="%.2f",
                    key=f"month_end_{draft_month}_{asset}",
                )

        save_month_end = st.form_submit_button("Save month end", use_container_width=True)
        if save_month_end:
            updated_rows = [
                {"month": draft_month, "asset": asset, "value": float(value)}
                for asset, value in month_end_inputs.items()
            ]
            new_me = st.session_state.month_end_df[st.session_state.month_end_df["month"] != draft_month].copy()
            new_me = pd.concat([new_me, pd.DataFrame(updated_rows)], ignore_index=True)
            new_me["sort"] = new_me["month"].apply(month_sort_value)
            new_me = new_me.sort_values(["sort", "asset"]).drop(columns="sort").reset_index(drop=True)
            new_me["value"] = pd.to_numeric(new_me["value"], errors="coerce").fillna(0.0)
            st.session_state.month_end_df = new_me
            st.session_state.last_modified_ts = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
            persist_err = persist_state()
            if persist_err:
                st.error(f"Auto-save error: {persist_err}")
            else:
                st.success(f"Month end saved for {draft_month}")
                st.rerun()

with pac_tab:
    st.subheader("Confirm monthly PAC")
    pac_month = st.selectbox("PAC month", options=MONTHS, index=MONTHS.index(_next_entry_month()), key="draft_pac_month")
    pac_view = pac_df[pac_df["month"] == pac_month].copy().sort_values("asset")

    with st.form("pac_form"):
        pac_updates = []
        for asset in etf_assets:
            asset_default = float(assets_df.loc[assets_df["name"] == asset, "pac"].iloc[0])
            existing = pac_view[pac_view["asset"] == asset]
            mode_default = existing["mode"].iloc[0] if not existing.empty else ("Auto" if asset_default > 0 else "No")
            amount_default = float(existing["amount"].iloc[0]) if not existing.empty else asset_default

            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.markdown(f"**{asset}**  \nDefault PAC: {eur0(asset_default)}")
            with c2:
                mode = st.selectbox(f"Mode - {asset}", ["Auto", "Edited", "No"], index=["Auto", "Edited", "No"].index(mode_default), key=f"mode_{pac_month}_{asset}")
            with c3:
                amount = st.number_input(f"Amount - {asset}", min_value=0.0, value=float(amount_default), step=10.0, format="%.2f", key=f"amount_{pac_month}_{asset}")

            pac_updates.append({"month": pac_month, "asset": asset, "mode": mode, "amount": amount})

        save_pac = st.form_submit_button("Save PAC", use_container_width=True)
        if save_pac:
            new_pac = st.session_state.pac_df[st.session_state.pac_df["month"] != pac_month].copy()
            new_pac = pd.concat([new_pac, pd.DataFrame(pac_updates)], ignore_index=True)
            new_pac["sort"] = new_pac["month"].apply(month_sort_value)
            new_pac = new_pac.sort_values(["sort", "asset"]).drop(columns="sort").reset_index(drop=True)
            new_pac["amount"] = pd.to_numeric(new_pac["amount"], errors="coerce").fillna(0.0)
            new_assets = st.session_state.assets_df.copy()
            for row in pac_updates:
                new_assets.loc[new_assets["name"] == row["asset"], "pac"] = float(row["amount"])
            st.session_state.pac_df = new_pac
            st.session_state.assets_df = new_assets
            st.session_state.last_modified_ts = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
            persist_err = persist_state()
            if persist_err:
                st.error(f"Auto-save error: {persist_err}")
            else:
                st.success(f"PAC saved for {pac_month}")
                st.rerun()

with manual_tab:
    st.subheader("Add manual transaction")
    with st.form("manual_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            manual_month = st.selectbox("Month", options=MONTHS, index=MONTHS.index(_next_entry_month()))
        with c2:
            manual_asset = st.selectbox("ETF", options=etf_assets)
        with c3:
            manual_amount = st.number_input("Amount", min_value=0.0, step=10.0, format="%.2f")

        add_manual = st.form_submit_button("Add transaction", use_container_width=True)
        if add_manual and manual_amount > 0:
            new_manual = st.session_state.manual_df.copy()
            new_manual.loc[len(new_manual)] = [manual_month, manual_asset, float(manual_amount)]
            new_manual["amount"] = pd.to_numeric(new_manual["amount"], errors="coerce").fillna(0.0)
            st.session_state.manual_df = new_manual
            st.session_state.last_modified_ts = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
            persist_err = persist_state()
            if persist_err:
                st.error(f"Auto-save error: {persist_err}")
            else:
                st.success("Manual transaction added")
                st.rerun()

with asset_tab:
    st.subheader("Add ETF to portfolio")
    st.caption("Creates the ETF in Assets and lets you set first month end value and PAC immediately.")

    with st.form("add_etf_form"):
        c1, c2 = st.columns(2)
        with c1:
            new_name = st.text_input("ETF name")
            new_subcategory = st.selectbox("Subcategory", ["ETF Stock", "ETF Bond", "ETF Gold"])
            new_bucket = st.selectbox("Bucket", ["Stocks", "Defensive"])
        with c2:
            first_month = st.selectbox("First month", options=MONTHS, index=MONTHS.index(_next_entry_month()))
            first_end_value = st.number_input("First end value", min_value=0.0, step=100.0, format="%.2f")
            new_pac = st.number_input("Monthly PAC", min_value=0.0, step=10.0, format="%.2f")

        add_etf = st.form_submit_button("Add ETF", use_container_width=True)
        if add_etf:
            cleaned_name = new_name.strip()
            if cleaned_name == "":
                st.error("ETF name is required")
            elif cleaned_name in assets_df["name"].tolist():
                st.error("This ETF already exists")
            else:
                new_assets = st.session_state.assets_df.copy()
                new_assets.loc[len(new_assets)] = {
                    "name": cleaned_name,
                    "category": "ETF",
                    "subcategory": new_subcategory,
                    "bucket": new_bucket,
                    "pac": float(new_pac),
                    "active": "Yes",
                }
                new_me = st.session_state.month_end_df.copy()
                new_me.loc[len(new_me)] = {"month": first_month, "asset": cleaned_name, "value": float(first_end_value)}
                new_me["value"] = pd.to_numeric(new_me["value"], errors="coerce").fillna(0.0)

                new_pac_df = st.session_state.pac_df.copy()
                for month in MONTHS:
                    if month_sort_value(month) >= month_sort_value(first_month):
                        new_pac_df.loc[len(new_pac_df)] = {
                            "month": month,
                            "asset": cleaned_name,
                            "mode": "Auto" if float(new_pac) > 0 else "No",
                            "amount": float(new_pac),
                        }

                st.session_state.assets_df = new_assets
                st.session_state.month_end_df = new_me
                st.session_state.pac_df = new_pac_df
                st.session_state.last_modified_ts = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
                persist_err = persist_state()
                if persist_err:
                    st.error(f"Auto-save error: {persist_err}")
                else:
                    st.success(f"{cleaned_name} added to portfolio")
                    st.rerun()
