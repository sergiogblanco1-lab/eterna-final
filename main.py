print("🔥 ETERNA MAIN DEFINITIVO BLINDADO 🔥")
print("🔥 WEBHOOK + CALLBACK + EXPERIENCE LOCK + REACTION SAVE 🔥")
print("🔥 FINAL UX LOCKED + CASHOUT HARDENED + SENDER PACK READY 🔥")
print("🔥 REACTION RETRY + ETERNA COMPLETE SAFE VERSION 🔥")
print("🔥 SCHEDULED DELIVERY LOCKED VERSION 🔥")
print("🔥 DELIVERY WORKER REAL VERSION 🔥")
print("🔥 GLOBAL PHONE READY VERSION 🔥")
print("🔥 DELIVERY FEE +2€ ONLY IF SCHEDULED VERSION 🔥")
print("🔥 NO SHARE ORIGINAL VIDEO VERSION 🔥")
print("🔥 VIRAL BLOCK + CALLBACK IDEMPOTENT + SMS RETRY VERSION 🔥")

import html
import json
import mimetypes
import os
import secrets
import sqlite3
import traceback
import uuid
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import boto3
import requests
import stripe
from botocore.client import Config
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

try:
    from twilio.rest import Client
except ImportError:
    Client = None


app = FastAPI(title="ETERNA FINAL PRODUCTO DEFINITIVO")
templates = Jinja2Templates(directory="templates")


# =========================================================
# CONFIG
# =========================================================

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "").strip()
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "").strip()
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "").strip()

PUBLIC_BASE_URL = os.getenv(
    "PUBLIC_BASE_URL",
    "https://eterna-final.onrender.com",
).strip().rstrip("/")

VIDEO_ENGINE_URL = os.getenv(
    "VIDEO_ENGINE_URL",
    "https://eterna-video-engine.onrender.com",
).strip().rstrip("/")

VIDEO_READY_CALLBACK_SECRET = os.getenv(
    "VIDEO_READY_CALLBACK_SECRET",
    "",
).strip()

BASE_PRICE = float(os.getenv("ETERNA_BASE_PRICE", "29"))
CURRENCY = os.getenv("ETERNA_CURRENCY", "eur").strip().lower()

GIFT_COMMISSION_RATE = float(os.getenv("GIFT_COMMISSION_RATE", "0.05"))
FIXED_PLATFORM_FEE = float(os.getenv("ETERNA_FIXED_FEE", "2"))

SCHEDULED_DELIVERY_FEE = float(os.getenv("SCHEDULED_DELIVERY_FEE", "2"))
GIFT_REFUND_DAYS = int(os.getenv("GIFT_REFUND_DAYS", "20"))

R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY", "").strip()
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY", "").strip()
R2_BUCKET = os.getenv("R2_BUCKET", "").strip()
R2_ENDPOINT = os.getenv("R2_ENDPOINT", "").strip().rstrip("/")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL", "").strip().rstrip("/")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
TWILIO_FROM_NUMBER = (
    os.getenv("TWILIO_FROM_NUMBER", "").strip()
    or os.getenv("TWILIO_PHONE_NUMBER", "").strip()
)
SMS_ENABLED = os.getenv("SMS_ENABLED", "1").strip() == "1"

MAX_VIDEO_SIZE = 100 * 1024 * 1024
ALLOWED_VIDEO_TYPES = {
    "video/webm",
    "video/mp4",
    "application/octet-stream",
}

DATA_FOLDER = Path("data")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

VIDEO_FOLDER = Path("videos")
VIDEO_FOLDER.mkdir(parents=True, exist_ok=True)

STATIC_FOLDER = Path("static")
STATIC_FOLDER.mkdir(parents=True, exist_ok=True)

PHOTO_FOLDER = Path("uploads")
PHOTO_FOLDER.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_FOLDER / "eterna.db"

DELIVERY_WORKER_INTERVAL_SECONDS = int(os.getenv("DELIVERY_WORKER_INTERVAL_SECONDS", "15"))
DELIVERY_WORKER_ENABLED = os.getenv("DELIVERY_WORKER_ENABLED", "1").strip() != "0"
DELIVERY_WORKER_STARTED = False
DELIVERY_WORKER_LOCK = threading.Lock()

COOKIE_SECURE = PUBLIC_BASE_URL.startswith("https://")

KNOWN_COUNTRY_CODES = [
    "+351",
    "+57",
    "+54",
    "+52",
    "+49",
    "+44",
    "+39",
    "+34",
    "+33",
    "+1",
]

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

app.mount("/static", StaticFiles(directory=str(STATIC_FOLDER)), name="static")


# =========================================================
# LOG
# =========================================================

def log_info(label: str, value=None):
    if value is None:
        print(f"[INFO] {label}")
    else:
        print(f"[INFO] {label}: {value}")


def log_error(label: str, error: Exception):
    print(f"[ERROR] {label}: {error}")
    traceback.print_exc()


# =========================================================
# DB
# =========================================================

def db_conn():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def column_exists(table_name: str, column_name: str) -> bool:
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    cols = cur.fetchall()
    conn.close()
    return any(col["name"] == column_name for col in cols)


def add_column_if_missing(table_name: str, column_name: str, sql: str):
    if not column_exists(table_name, column_name):
        conn = db_conn()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()


def init_db():
    conn = db_conn()
    cur = conn.cursor()

    # =========================
    # TABLAS BASE
    # =========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS senders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS recipients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        sender_id INTEGER NOT NULL,
        recipient_id INTEGER NOT NULL,

        message_type TEXT,
        phrase_mode TEXT NOT NULL DEFAULT 'auto',

        phrase_1 TEXT NOT NULL,
        phrase_2 TEXT NOT NULL,
        phrase_3 TEXT NOT NULL,

        gift_amount REAL NOT NULL DEFAULT 0,
        platform_fixed_fee REAL NOT NULL DEFAULT 0,
        platform_variable_fee REAL NOT NULL DEFAULT 0,
        platform_total_fee REAL NOT NULL DEFAULT 0,
        scheduled_delivery_fee REAL NOT NULL DEFAULT 0,
        total_amount REAL NOT NULL DEFAULT 0,

        paid INTEGER NOT NULL DEFAULT 0,
        delivered_to_recipient INTEGER NOT NULL DEFAULT 0,
        reaction_uploaded INTEGER NOT NULL DEFAULT 0,

        cashout_completed INTEGER NOT NULL DEFAULT 0,
        transfer_completed INTEGER NOT NULL DEFAULT 0,
        transfer_in_progress INTEGER NOT NULL DEFAULT 0,
        sender_notified INTEGER NOT NULL DEFAULT 0,

        experience_started INTEGER NOT NULL DEFAULT 0,
        experience_completed INTEGER NOT NULL DEFAULT 0,

        connect_onboarding_completed INTEGER NOT NULL DEFAULT 0,
        gift_refunded INTEGER NOT NULL DEFAULT 0,

        stripe_session_id TEXT,
        stripe_payment_status TEXT,
        stripe_payment_intent_id TEXT,
        stripe_connected_account_id TEXT,
        stripe_transfer_id TEXT,
        stripe_gift_refund_id TEXT,

        recipient_token TEXT NOT NULL UNIQUE,
        sender_token TEXT NOT NULL UNIQUE,

        reaction_video_local TEXT,
        reaction_video_public_url TEXT,
        experience_video_url TEXT,
        share_video_url TEXT,

        gift_refund_deadline_at TEXT,

        recipient_sms_sent_at TEXT,
        sender_sms_sent_at TEXT,
        recipient_sms_sid TEXT,
        sender_sms_sid TEXT,

        recipient_sms_attempts INTEGER NOT NULL DEFAULT 0,
        sender_sms_attempts INTEGER NOT NULL DEFAULT 0,
        recipient_sms_error TEXT,
        sender_sms_error TEXT,

        reaction_upload_pending INTEGER NOT NULL DEFAULT 0,
        reaction_upload_error TEXT,
        eterna_completed INTEGER NOT NULL DEFAULT 0,

        delivery_mode TEXT NOT NULL DEFAULT 'instant',
        scheduled_delivery_at TEXT,
        delivery_locked INTEGER NOT NULL DEFAULT 0,
        delivery_sent INTEGER NOT NULL DEFAULT 0,
        delivery_sent_at TEXT,

        video_render_requested INTEGER NOT NULL DEFAULT 0,
        video_render_requested_at TEXT,

        recipient_session_token TEXT,
        recipient_session_claimed_at TEXT,

        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,

        FOREIGN KEY(sender_id) REFERENCES senders(id),
        FOREIGN KEY(recipient_id) REFERENCES recipients(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT NOT NULL,
        asset_type TEXT NOT NULL,
        file_url TEXT NOT NULL,
        storage_provider TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(order_id) REFERENCES orders(id)
    )
    """)

    conn.commit()
    conn.close()

    # =========================
    # COLUMNAS DINÁMICAS (BLINDADO)
    # =========================

    add_column_if_missing("orders", "message_type", "ALTER TABLE orders ADD COLUMN message_type TEXT")
    add_column_if_missing("orders", "phrase_mode", "ALTER TABLE orders ADD COLUMN phrase_mode TEXT NOT NULL DEFAULT 'auto'")
    add_column_if_missing("orders", "experience_video_url", "ALTER TABLE orders ADD COLUMN experience_video_url TEXT")
    add_column_if_missing("orders", "reaction_video_public_url", "ALTER TABLE orders ADD COLUMN reaction_video_public_url TEXT")
    add_column_if_missing("orders", "reaction_video_local", "ALTER TABLE orders ADD COLUMN reaction_video_local TEXT")
    add_column_if_missing("orders", "share_video_url", "ALTER TABLE orders ADD COLUMN share_video_url TEXT")
    add_column_if_missing("orders", "stripe_session_id", "ALTER TABLE orders ADD COLUMN stripe_session_id TEXT")
    add_column_if_missing("orders", "stripe_payment_status", "ALTER TABLE orders ADD COLUMN stripe_payment_status TEXT")
    add_column_if_missing("orders", "stripe_payment_intent_id", "ALTER TABLE orders ADD COLUMN stripe_payment_intent_id TEXT")
    add_column_if_missing("orders", "stripe_connected_account_id", "ALTER TABLE orders ADD COLUMN stripe_connected_account_id TEXT")
    add_column_if_missing("orders", "stripe_transfer_id", "ALTER TABLE orders ADD COLUMN stripe_transfer_id TEXT")
    add_column_if_missing("orders", "stripe_gift_refund_id", "ALTER TABLE orders ADD COLUMN stripe_gift_refund_id TEXT")
    add_column_if_missing("orders", "gift_refund_deadline_at", "ALTER TABLE orders ADD COLUMN gift_refund_deadline_at TEXT")
    add_column_if_missing("orders", "gift_refunded", "ALTER TABLE orders ADD COLUMN gift_refunded INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "recipient_sms_sent_at", "ALTER TABLE orders ADD COLUMN recipient_sms_sent_at TEXT")
    add_column_if_missing("orders", "sender_sms_sent_at", "ALTER TABLE orders ADD COLUMN sender_sms_sent_at TEXT")
    add_column_if_missing("orders", "recipient_sms_sid", "ALTER TABLE orders ADD COLUMN recipient_sms_sid TEXT")
    add_column_if_missing("orders", "sender_sms_sid", "ALTER TABLE orders ADD COLUMN sender_sms_sid TEXT")
    add_column_if_missing("orders", "recipient_sms_attempts", "ALTER TABLE orders ADD COLUMN recipient_sms_attempts INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "sender_sms_attempts", "ALTER TABLE orders ADD COLUMN sender_sms_attempts INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "recipient_sms_error", "ALTER TABLE orders ADD COLUMN recipient_sms_error TEXT")
    add_column_if_missing("orders", "sender_sms_error", "ALTER TABLE orders ADD COLUMN sender_sms_error TEXT")
    add_column_if_missing("orders", "reaction_upload_pending", "ALTER TABLE orders ADD COLUMN reaction_upload_pending INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "reaction_upload_error", "ALTER TABLE orders ADD COLUMN reaction_upload_error TEXT")
    add_column_if_missing("orders", "eterna_completed", "ALTER TABLE orders ADD COLUMN eterna_completed INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "delivery_mode", "ALTER TABLE orders ADD COLUMN delivery_mode TEXT NOT NULL DEFAULT 'instant'")
    add_column_if_missing("orders", "scheduled_delivery_fee", "ALTER TABLE orders ADD COLUMN scheduled_delivery_fee REAL NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "scheduled_delivery_at", "ALTER TABLE orders ADD COLUMN scheduled_delivery_at TEXT")
    add_column_if_missing("orders", "delivery_locked", "ALTER TABLE orders ADD COLUMN delivery_locked INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "delivery_sent", "ALTER TABLE orders ADD COLUMN delivery_sent INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "delivery_sent_at", "ALTER TABLE orders ADD COLUMN delivery_sent_at TEXT")
    add_column_if_missing("orders", "video_render_requested", "ALTER TABLE orders ADD COLUMN video_render_requested INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "video_render_requested_at", "ALTER TABLE orders ADD COLUMN video_render_requested_at TEXT")
    add_column_if_missing("orders", "recipient_session_token", "ALTER TABLE orders ADD COLUMN recipient_session_token TEXT")
    add_column_if_missing("orders", "recipient_session_claimed_at", "ALTER TABLE orders ADD COLUMN recipient_session_claimed_at TEXT")
init_db()


# =========================================================
# HELPERS BASE
# =========================================================

def now_dt() -> datetime:
    return datetime.now(timezone.utc)


def now_iso() -> str:
    return now_dt().isoformat()


def gift_refund_deadline_iso() -> str:
    return (now_dt() + timedelta(days=GIFT_REFUND_DAYS)).isoformat()


def safe_text(v: str) -> str:
    return html.escape(str(v or "").strip())


def safe_attr(v: str) -> str:
    return html.escape(str(v or "").strip(), quote=True)


def money(v: float) -> str:
    return f"{float(v):.2f}"


def format_amount_display(value) -> str:
    try:
        return f"{float(value):.2f} €".replace(".", ",")
    except Exception:
        return "0,00 €"


def parse_iso_dt(value: str) -> Optional[datetime]:
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def parse_scheduled_delivery_local(delivery_date: str, delivery_time: str) -> Optional[str]:
    delivery_date = (delivery_date or "").strip()
    delivery_time = (delivery_time or "").strip()

    if not delivery_date:
        return None

    if not delivery_time:
        delivery_time = "12:00"

    try:
        naive_local = datetime.fromisoformat(f"{delivery_date}T{delivery_time}")
    except Exception:
        return None

    try:
        if ZoneInfo is not None:
            madrid = ZoneInfo("Europe/Madrid")
            local_dt = naive_local.replace(tzinfo=madrid)
            utc_dt = local_dt.astimezone(timezone.utc)
            return utc_dt.isoformat()
    except Exception:
        pass

    return naive_local.replace(tzinfo=timezone.utc).isoformat()


def scheduled_delivery_display(order: dict) -> str:
    raw = (order.get("scheduled_delivery_at") or "").strip()
    if not raw:
        return "En cuanto esté lista"

    dt = parse_iso_dt(raw)
    if not dt:
        return "En cuanto esté lista"

    try:
        if ZoneInfo is not None:
            madrid = ZoneInfo("Europe/Madrid")
            dt = dt.astimezone(madrid)
    except Exception:
        pass

    return dt.strftime("%d/%m/%Y a las %H:%M")


def normalize_phone(p: str) -> str:
    raw = str(p or "").strip()
    raw = raw.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if raw.startswith("00"):
        raw = raw[2:]
    if raw.startswith("+"):
        raw = raw[1:]
    digits = "".join(ch for ch in raw if ch.isdigit())
    return digits


def to_e164(phone: str) -> str:
    normalized = normalize_phone(phone)
    if not normalized:
        return ""

    if normalized.startswith("34") and len(normalized) == 11:
        return f"+{normalized}"

    if len(normalized) == 9:
        return f"+34{normalized}"

    if len(normalized) >= 10:
        return f"+{normalized}"

    return ""


def build_global_phone(code: str, phone: str) -> str:
    code = (code or "+34").strip()
    phone = (phone or "").strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    if not code.startswith("+"):
        code = f"+{code}"

    if phone.startswith("+"):
        final_phone = phone
    elif phone.startswith("00"):
        final_phone = "+" + phone[2:]
    else:
        final_phone = f"{code}{phone}"

    return final_phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")


def split_phone_for_form(phone: str) -> tuple[str, str]:
    raw = str(phone or "").strip()
    if not raw:
        return "+34", ""

    if not raw.startswith("+"):
        return "+34", raw

    for code in KNOWN_COUNTRY_CODES:
        if raw.startswith(code):
            return code, raw[len(code):]

    return "+34", raw


def new_order_id() -> str:
    return uuid.uuid4().hex[:12]


def new_token() -> str:
    return secrets.token_urlsafe(24)


def detect_video_extension(upload: UploadFile) -> str:
    content_type = (upload.content_type or "").lower().strip()
    filename = (upload.filename or "").lower().strip()
    if filename.endswith(".mp4") or content_type == "video/mp4":
        return "mp4"
    return "webm"


def detect_image_extension(upload: UploadFile) -> str:
    filename = (upload.filename or "").lower().strip()
    content_type = (upload.content_type or "").lower().strip()

    if filename.endswith(".png") or content_type == "image/png":
        return "png"
    if filename.endswith(".webp") or content_type == "image/webp":
        return "webp"
    if filename.endswith(".jpeg") or content_type == "image/jpeg":
        return "jpg"
    if filename.endswith(".jpg") or content_type in {"image/jpg", "image/jpeg"}:
        return "jpg"

    return "jpg"


def build_photo_path(order_id: str, slot_name: str, upload: UploadFile) -> str:
    ext = detect_image_extension(upload)
    folder = PHOTO_FOLDER / order_id
    folder.mkdir(parents=True, exist_ok=True)
    return str(folder / f"{slot_name}.{ext}")


def reaction_video_path(order_id: str, extension: str = "webm") -> str:
    extension = (extension or "webm").lower().strip()
    if extension not in {"webm", "mp4"}:
        extension = "webm"
    return str(VIDEO_FOLDER / f"reaction_{order_id}.{extension}")


def guess_media_type_from_path(path: str) -> str:
    media_type, _ = mimetypes.guess_type(path)
    return media_type or "application/octet-stream"


def guess_media_type_from_url(url: str) -> str:
    raw = (url or "").split("?")[0].lower()
    if raw.endswith(".webm"):
        return "video/webm"
    if raw.endswith(".mp4"):
        return "video/mp4"
    return "video/mp4"


def r2_enabled() -> bool:
    return all([R2_ACCESS_KEY, R2_SECRET_KEY, R2_BUCKET, R2_ENDPOINT, R2_PUBLIC_URL])


def get_r2_client():
    if not r2_enabled():
        return None
    return boto3.client(
        "s3",
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


def upload_video_to_r2(local_path: str, remote_name: str, content_type: str = "video/webm") -> Optional[str]:
    client = get_r2_client()
    if not client:
        return None

    client.upload_file(
        local_path,
        R2_BUCKET,
        remote_name,
        ExtraArgs={"ContentType": content_type},
    )
    return f"{R2_PUBLIC_URL}/{remote_name}"


def insert_asset(order_id: str, asset_type: str, file_url: str, storage_provider: str):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO assets (order_id, asset_type, file_url, storage_provider, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (order_id, asset_type, file_url, storage_provider, now_iso()))
    conn.commit()
    conn.close()


def list_assets(order_id: str):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, order_id, asset_type, file_url, storage_provider, created_at
        FROM assets
        WHERE order_id = ?
        ORDER BY id ASC
    """, (order_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def asset_exists(order_id: str, asset_type: str, file_url: str) -> bool:
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT 1
        FROM assets
        WHERE order_id = ? AND asset_type = ? AND file_url = ?
        LIMIT 1
    """, (order_id, asset_type, file_url))
    row = cur.fetchone()
    conn.close()
    return bool(row)


def get_photo_asset_path(order_id: str, slot_name: str) -> Optional[str]:
    slot_name = (slot_name or "").strip().lower()

    aliases = {slot_name}
    if slot_name.startswith("photo"):
        aliases.add(slot_name.replace("photo", "foto", 1))
    if slot_name.startswith("foto"):
        aliases.add(slot_name.replace("foto", "photo", 1))

    assets = list_assets(order_id)

    for asset in assets:
        asset_type = (asset.get("asset_type") or "").strip().lower()
        file_url = (asset.get("file_url") or "").strip()
        if asset_type in aliases and file_url:
            return file_url

    return None


def original_video_ready(order: dict) -> bool:
    url = (order.get("experience_video_url") or "").strip()
    return bool(url)


def reaction_exists(order: dict) -> bool:
    if order.get("reaction_video_public_url"):
        return True
    local_path = (order.get("reaction_video_local") or "").strip()
    return bool(local_path) and os.path.exists(local_path)


def scheduled_delivery_ready(order: dict) -> bool:
    raw = (order.get("scheduled_delivery_at") or "").strip()
    delivery_mode = (order.get("delivery_mode") or "instant").strip()

    if delivery_mode == "instant":
        return True

    if not raw:
        return True

    dt = parse_iso_dt(raw)
    if not dt:
        return True

    return now_dt() >= dt


def delivery_locked(order: dict) -> bool:
    return bool(order.get("delivery_locked"))


def delivery_already_sent(order: dict) -> bool:
    return bool(order.get("delivery_sent")) or bool(order.get("delivery_sent_at"))


def delivery_is_unlocked(order: dict) -> bool:
    if delivery_already_sent(order):
        return True

    if scheduled_delivery_ready(order):
        return True

    return False


def can_send_recipient_delivery(order: dict) -> tuple[bool, str]:
    if order.get("delivery_sent"):
        return False, "delivery_already_sent"

    if not bool(order.get("paid")):
        return False, "order_not_paid"

    if not original_video_ready(order):
        return False, "original_video_not_ready"

    if delivery_already_sent(order):
        return False, "delivery_already_sent"

    if not scheduled_delivery_ready(order):
        return False, "scheduled_delivery_not_ready"

    return True, "ok"


def is_eterna_complete(order: dict) -> bool:
    return (
        original_video_ready(order)
        and bool(order.get("reaction_uploaded"))
        and reaction_exists(order)
    )


def maybe_mark_eterna_completed(order_id: str) -> dict:
    order = get_order_by_id(order_id)

    if is_eterna_complete(order):
        update_order(
            order_id,
            eterna_completed=1,
            reaction_upload_pending=0,
            reaction_upload_error=None,
        )
    else:
        update_order(order_id, eterna_completed=0)

    return get_order_by_id(order_id)


def video_engine_headers() -> dict:
    headers = {"Content-Type": "application/json"}
    if VIDEO_READY_CALLBACK_SECRET:
        headers["X-Video-Engine-Secret"] = VIDEO_READY_CALLBACK_SECRET
    return headers


def trigger_video_engine(order_id: str, phrases: list[str]) -> dict:
    photos = [
        f"{PUBLIC_BASE_URL}/video/input/{order_id}/photo1",
        f"{PUBLIC_BASE_URL}/video/input/{order_id}/photo2",
        f"{PUBLIC_BASE_URL}/video/input/{order_id}/photo3",
        f"{PUBLIC_BASE_URL}/video/input/{order_id}/photo4",
        f"{PUBLIC_BASE_URL}/video/input/{order_id}/photo5",
        f"{PUBLIC_BASE_URL}/video/input/{order_id}/photo6",
    ]

    payload = {
        "order_id": order_id,
        "photos": photos,
        "phrases": phrases,
    }

    print("🚀 Enviando al video engine...")
    print("🚀 VIDEO_ENGINE_URL:", VIDEO_ENGINE_URL)
    print("🚀 payload:", payload)

    response = requests.post(
        f"{VIDEO_ENGINE_URL}/render",
        json=payload,
        headers=video_engine_headers(),
        timeout=30,
    )

    print("📩 Video engine status:", response.status_code)
    print("📩 Video engine response:", response.text)

    data = {}
    try:
        data = response.json()
    except Exception:
        data = {"raw_text": response.text}

    if not response.ok:
        raise Exception(f"video_engine_http_{response.status_code}: {response.text}")

    return data


# =========================================================
# ORDER HELPERS
# =========================================================

def get_order_by_id(order_id: str):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            o.*,
            s.name AS sender_name,
            s.email AS sender_email,
            s.phone AS sender_phone,
            r.name AS recipient_name,
            r.phone AS recipient_phone
        FROM orders o
        JOIN senders s ON s.id = o.sender_id
        JOIN recipients r ON r.id = o.recipient_id
        WHERE o.id = ?
    """, (order_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return dict(row)


def get_order_by_stripe_session_id(session_id: str):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            o.*,
            s.name AS sender_name,
            s.email AS sender_email,
            s.phone AS sender_phone,
            r.name AS recipient_name,
            r.phone AS recipient_phone
        FROM orders o
        JOIN senders s ON s.id = o.sender_id
        JOIN recipients r ON r.id = o.recipient_id
        WHERE o.stripe_session_id = ?
        LIMIT 1
    """, (session_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Pedido no encontrado por sesión Stripe")
    return dict(row)


def get_order_by_recipient_token_or_404(token: str):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            o.*,
            s.name AS sender_name,
            s.email AS sender_email,
            s.phone AS sender_phone,
            r.name AS recipient_name,
            r.phone AS recipient_phone
        FROM orders o
        JOIN senders s ON s.id = o.sender_id
        JOIN recipients r ON r.id = o.recipient_id
        WHERE o.recipient_token = ?
    """, (token,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Experiencia no encontrada")
    return dict(row)


def get_order_by_sender_token_or_404(token: str):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            o.*,
            s.name AS sender_name,
            s.email AS sender_email,
            s.phone AS sender_phone,
            r.name AS recipient_name,
            r.phone AS recipient_phone
        FROM orders o
        JOIN senders s ON s.id = o.sender_id
        JOIN recipients r ON r.id = o.recipient_id
        WHERE o.sender_token = ?
    """, (token,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Sender pack no encontrado")
    return dict(row)


def update_order(order_id: str, **fields):
    if not fields:
        return

    fields["updated_at"] = now_iso()
    columns = ", ".join([f"{k} = ?" for k in fields.keys()])
    values = list(fields.values()) + [order_id]

    conn = db_conn()
    cur = conn.cursor()
    cur.execute(f"UPDATE orders SET {columns} WHERE id = ?", values)
    conn.commit()
    conn.close()


def sender_pack_url_from_order(order: dict) -> str:
    return f"{PUBLIC_BASE_URL}/sender/{order['sender_token']}"


def recipient_experience_url_from_order(order: dict) -> str:
    return f"{PUBLIC_BASE_URL}/pedido/{order['recipient_token']}"


def build_recipient_message(order: dict) -> str:
    return (
        "ETERNA\n\n"
        "Tienes algo que ver…\n\n"
        f"{recipient_experience_url_from_order(order)}"
    )


def build_sender_ready_message(order: dict) -> str:
    return (
        "Tu ETERNA ha vuelto.\n\n"
        "Al otro lado,\n"
        "algo ha pasado.\n\n"
        f"{sender_pack_url_from_order(order)}"
    )


def try_send_sender_sms(order: dict) -> dict:
    order = get_order_by_id(order["id"])

    if not bool(order.get("paid")):
        return {"ok": False, "reason": "order_not_paid"}

    if not bool(order.get("reaction_uploaded")):
        return {"ok": False, "reason": "reaction_not_uploaded"}

    if not reaction_exists(order):
        return {"ok": False, "reason": "reaction_not_found"}

    attempts = int(order.get("sender_sms_attempts") or 0)

    if bool(order.get("sender_sms_sent_at")):
        return {
            "ok": True,
            "reason": "already_sent",
            "sid": order.get("sender_sms_sid"),
            "sender_sms_sent_at": order.get("sender_sms_sent_at"),
            "sender_sms_attempts": attempts,
            "sender_sms_error": order.get("sender_sms_error"),
        }

    if attempts >= 3:
        return {
            "ok": False,
            "reason": "max_attempts_reached",
            "sender_sms_sent_at": order.get("sender_sms_sent_at"),
            "sender_sms_attempts": attempts,
            "sender_sms_error": order.get("sender_sms_error"),
        }

    message = build_sender_ready_message(order)
    result = send_sms(order.get("sender_phone", ""), message)

    attempts = attempts + 1

    if result.get("ok"):
        sent_at = now_iso()

        update_order(
            order["id"],
            sender_sms_attempts=attempts,
            sender_sms_error=None,
            sender_sms_sid=result.get("sid"),
            sender_sms_sent_at=sent_at,
            sender_notified=1,
        )

        refreshed = get_order_by_id(order["id"])
        return {
            "ok": True,
            "reason": "sent",
            "sid": refreshed.get("sender_sms_sid"),
            "sender_sms_sent_at": refreshed.get("sender_sms_sent_at"),
            "sender_sms_attempts": int(refreshed.get("sender_sms_attempts") or 0),
            "sender_sms_error": refreshed.get("sender_sms_error"),
        }

    update_order(
        order["id"],
        sender_sms_attempts=attempts,
        sender_sms_error=result.get("error") or "sms_error",
    )

    refreshed = get_order_by_id(order["id"])
    return {
        "ok": False,
        "reason": result.get("error") or "sms_error",
        "sender_sms_sent_at": refreshed.get("sender_sms_sent_at"),
        "sender_sms_attempts": int(refreshed.get("sender_sms_attempts") or 0),
        "sender_sms_error": refreshed.get("sender_sms_error"),
    }


def calculate_fees(gift_amount: float, delivery_mode: str) -> dict:
    gift_amount = max(0.0, round(float(gift_amount or 0), 2))
    fixed_fee = round(FIXED_PLATFORM_FEE, 2)
    variable_fee = round(gift_amount * GIFT_COMMISSION_RATE, 2)
    delivery_mode = (delivery_mode or "instant").strip().lower()
    scheduled_fee = round(SCHEDULED_DELIVERY_FEE if delivery_mode == "scheduled" else 0.0, 2)
    total_fee = round(fixed_fee + variable_fee, 2)
    total_amount = round(BASE_PRICE + gift_amount + total_fee + scheduled_fee, 2)
    return {
        "gift_amount": gift_amount,
        "fixed_fee": fixed_fee,
        "variable_fee": variable_fee,
        "total_fee": total_fee,
        "scheduled_delivery_fee": scheduled_fee,
        "total_amount": total_amount,
    }


def get_phrases_by_type(message_type: str):
    phrase_templates = {
        "cumpleanos": [
            "Hoy no es un día cualquiera.",
            "Es tu historia celebrándose.",
            "Y lo mejor… aún está por venir.",
        ],
        "amor": [
            "Si volviera a empezar,",
            "te elegiría otra vez.",
            "Siempre tú.",
        ],
        "familia": [
            "Todo empieza contigo.",
            "Todo vuelve a ti.",
            "Gracias por tanto.",
        ],
        "superacion": [
            "Nunca dejaste de intentarlo.",
            "Y eso lo cambia todo.",
            "Creemos en ti.",
        ],
        "esfuerzo": [
            "Todo lo que has dado",
            "no ha pasado desapercibido.",
            "Y lo valoramos más de lo que imaginas.",
        ],
        "sorpresa": [
            "Pensabas que hoy era un día normal…",
            "Pero alguien ha estado pensando en ti.",
            "Mucho más de lo que imaginas.",
        ],
    }
    return phrase_templates.get(message_type, phrase_templates["sorpresa"])


def twilio_enabled() -> bool:
    return bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER and Client)


def send_sms(phone: str, message: str) -> dict:
    to_phone = to_e164(phone)

    if not to_phone:
        return {"ok": False, "sid": None, "error": "invalid_phone"}

    if not SMS_ENABLED:
        print("🚫 SMS DESACTIVADO POR CONFIG")
        print("🚫 Destino:", to_phone)
        print("🚫 Mensaje:", message)
        return {"ok": False, "sid": None, "error": "sms_disabled_by_config"}

    if not twilio_enabled():
        return {"ok": False, "sid": None, "error": "twilio_not_configured"}

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        sms = client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=to_phone,
        )
        return {"ok": True, "sid": sms.sid, "error": None}
    except Exception as e:
        return {"ok": False, "sid": None, "error": str(e)}


def process_scheduled_recipient_delivery(order_id: str) -> dict:
    order = get_order_by_id(order_id)

    if bool(order.get("delivery_sent")) or bool(order.get("delivery_sent_at")):
        return {
            "ok": True,
            "reason": "already_sent",
            "delivery_sent": True,
            "delivery_sent_at": order.get("delivery_sent_at"),
            "scheduled_delivery_display": scheduled_delivery_display(order),
            "recipient_sms_sent_at": order.get("recipient_sms_sent_at"),
            "recipient_sms_attempts": int(order.get("recipient_sms_attempts") or 0),
            "recipient_sms_error": order.get("recipient_sms_error"),
        }

    attempts = int(order.get("recipient_sms_attempts") or 0)

    if attempts >= 3:
        return {
            "ok": False,
            "reason": "max_attempts_reached",
            "recipient_sms_sent_at": order.get("recipient_sms_sent_at"),
            "recipient_sms_attempts": attempts,
            "recipient_sms_error": order.get("recipient_sms_error"),
        }

    if not bool(order.get("paid")):
        return {
            "ok": False,
            "reason": "order_not_paid",
            "delivery_sent": False,
            "delivery_sent_at": order.get("delivery_sent_at"),
            "scheduled_delivery_display": scheduled_delivery_display(order),
            "recipient_sms_sent_at": order.get("recipient_sms_sent_at"),
            "recipient_sms_attempts": attempts,
            "recipient_sms_error": order.get("recipient_sms_error"),
        }

    if not original_video_ready(order):
        return {
            "ok": False,
            "reason": "original_video_not_ready",
            "delivery_sent": False,
            "delivery_sent_at": order.get("delivery_sent_at"),
            "scheduled_delivery_display": scheduled_delivery_display(order),
            "recipient_sms_sent_at": order.get("recipient_sms_sent_at"),
            "recipient_sms_attempts": attempts,
            "recipient_sms_error": order.get("recipient_sms_error"),
        }

    if not delivery_is_unlocked(order):
        return {
            "ok": False,
            "reason": "scheduled_delivery_not_ready",
            "delivery_sent": False,
            "delivery_sent_at": order.get("delivery_sent_at"),
            "scheduled_delivery_display": scheduled_delivery_display(order),
            "recipient_sms_sent_at": order.get("recipient_sms_sent_at"),
            "recipient_sms_attempts": attempts,
            "recipient_sms_error": order.get("recipient_sms_error"),
        }

    message = build_recipient_message(order)
    result = send_sms(order.get("recipient_phone", ""), message)

    attempts = attempts + 1

    if result.get("ok"):
        sent_at = now_iso()

        update_order(
            order_id,
            recipient_sms_attempts=attempts,
            recipient_sms_error=None,
            recipient_sms_sid=result.get("sid"),
            recipient_sms_sent_at=sent_at,
            delivery_sent=1,
            delivery_sent_at=sent_at,
            delivered_to_recipient=1,
        )

        refreshed = get_order_by_id(order_id)
        return {
            "ok": True,
            "reason": "sent",
            "sid": result.get("sid"),
            "delivery_sent": bool(refreshed.get("delivery_sent")),
            "delivery_sent_at": refreshed.get("delivery_sent_at"),
            "scheduled_delivery_display": scheduled_delivery_display(refreshed),
            "recipient_sms_sent_at": refreshed.get("recipient_sms_sent_at"),
            "recipient_sms_attempts": int(refreshed.get("recipient_sms_attempts") or 0),
            "recipient_sms_error": refreshed.get("recipient_sms_error"),
        }

    update_order(
        order_id,
        recipient_sms_attempts=attempts,
        recipient_sms_error=result.get("error") or "sms_error",
    )

    refreshed = get_order_by_id(order_id)
    return {
        "ok": False,
        "reason": result.get("error") or "sms_error",
        "delivery_sent": bool(refreshed.get("delivery_sent")),
        "delivery_sent_at": refreshed.get("delivery_sent_at"),
        "scheduled_delivery_display": scheduled_delivery_display(refreshed),
        "recipient_sms_sent_at": refreshed.get("recipient_sms_sent_at"),
        "recipient_sms_attempts": int(refreshed.get("recipient_sms_attempts") or 0),
        "recipient_sms_error": refreshed.get("recipient_sms_error"),
    }

# =========================================================
# HELPERS EXTRA
# =========================================================

def compute_cashout_status(order: dict) -> str:
    if bool(order.get("gift_refunded")):
        return "gift_refunded"
    if bool(order.get("cashout_completed")) or bool(order.get("transfer_completed")):
        return "completed"
    if bool(order.get("transfer_in_progress")):
        return "processing"
    if bool(order.get("connect_onboarding_completed")):
        return "ready_to_send"
    return "pending"


def try_acquire_transfer_lock(order_id: str) -> bool:
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE orders
        SET transfer_in_progress = 1,
            updated_at = ?
        WHERE id = ?
          AND COALESCE(transfer_in_progress, 0) = 0
          AND COALESCE(transfer_completed, 0) = 0
        """,
        (now_iso(), order_id),
    )
    conn.commit()
    acquired = cur.rowcount == 1
    conn.close()
    return acquired


def release_transfer_lock(order_id: str):
    update_order(order_id, transfer_in_progress=0)


def try_start_experience(order_id: str) -> str:
    order = get_order_by_id(order_id)

    if not bool(order.get("paid")):
        return "not_paid"

    if not original_video_ready(order):
        return "video_not_ready"

    if bool(order.get("experience_completed")):
        return "already_completed"

    if bool(order.get("experience_started")):
        return "already_started"

    update_order(
        order_id,
        experience_started=1,
        delivered_to_recipient=1,
    )
    return "started"


def render_request_already_marked(order: dict) -> bool:
    return bool(order.get("video_render_requested"))


def mark_video_render_requested(order_id: str):
    update_order(
        order_id,
        video_render_requested=1,
        video_render_requested_at=now_iso(),
    )


def clear_video_render_requested(order_id: str):
    update_order(
        order_id,
        video_render_requested=0,
        video_render_requested_at=None,
    )


def recipient_cookie_name(recipient_token: str) -> str:
    return f"eterna_recipient_session_{recipient_token}"


def get_recipient_cookie_value(request: Request, recipient_token: str) -> str:
    return (request.cookies.get(recipient_cookie_name(recipient_token)) or "").strip()


def has_valid_recipient_session(order: dict, request: Request) -> bool:
    expected = (order.get("recipient_session_token") or "").strip()
    if not expected:
        return False

    got = get_recipient_cookie_value(request, order["recipient_token"])
    if not got:
        return False

    try:
        return secrets.compare_digest(expected, got)
    except Exception:
        return False


def attach_recipient_session_if_needed(order: dict, request: Request, response) -> bool:
    expected = (order.get("recipient_session_token") or "").strip()

    if expected:
        if has_valid_recipient_session(order, request):
            return True
        return False

    new_session = new_token()

    update_order(
        order["id"],
        recipient_session_token=new_session,
        recipient_session_claimed_at=now_iso(),
    )

    response.set_cookie(
        key=recipient_cookie_name(order["recipient_token"]),
        value=new_session,
        max_age=60 * 60 * 24 * 365 * 5,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    return True


def render_viral_block_page() -> HTMLResponse:
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ETERNA</title>
        <style>
            * { box-sizing: border-box; }
            html, body { margin: 0; min-height: 100%; background: #000; }
            body {
                min-height: 100vh;
                background:
                    radial-gradient(circle at top, rgba(255,255,255,0.06), transparent 30%),
                    linear-gradient(180deg, #050505 0%, #000000 100%);
                color: white;
                font-family: Arial, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 24px;
            }
            .wrap {
                width: 100%;
                max-width: 760px;
                margin: 0 auto;
            }
            h1 {
                margin: 0 0 18px 0;
                font-size: 42px;
                line-height: 1.2;
            }
            .main {
                font-size: 22px;
                line-height: 1.8;
                color: rgba(255,255,255,0.88);
            }
            .soft {
                margin-top: 24px;
                font-size: 16px;
                line-height: 1.8;
                color: rgba(255,255,255,0.46);
            }
            .actions {
                display: grid;
                gap: 12px;
                max-width: 420px;
                margin: 34px auto 0 auto;
            }
            .btn {
                display: block;
                width: 100%;
                padding: 17px 22px;
                border-radius: 999px;
                background: white;
                color: black;
                text-decoration: none;
                font-weight: bold;
                font-size: 15px;
            }
            .ghost {
                background: rgba(255,255,255,0.10);
                color: white;
                border: 1px solid rgba(255,255,255,0.10);
            }
        </style>
    </head>
    <body>
        <div class="wrap">
            <h1>Esto no era para ti</h1>
            <div class="main">
                Alguien compartió contigo un acceso privado.<br>
                Pero esta experiencia solo podía vivirse una vez, por quien iba dirigida.
            </div>
            <div class="soft">
                Puedes crear algo igual de especial para otra persona.
            </div>
            <div class="actions">
                <a class="btn" href="/crear">Crear una ETERNA</a>
                <a class="btn ghost" href="/">Volver al inicio</a>
            </div>
        </div>
    </body>
    </html>
    """)


# =========================================================
# STRIPE CONNECT HELPERS
# =========================================================

def get_or_create_connected_account(order: dict) -> str:
    existing = (order.get("stripe_connected_account_id") or "").strip()
    if existing:
        return existing

    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe no configurado")

    account = stripe.Account.create(
        type="express",
        country="ES",
        capabilities={"transfers": {"requested": True}},
        metadata={
            "order_id": order["id"],
            "recipient_name": order.get("recipient_name", ""),
        },
    )
    update_order(order["id"], stripe_connected_account_id=account.id)
    return account.id


def create_connect_onboarding_link(order: dict) -> str:
    account_id = get_or_create_connected_account(order)
    link = stripe.AccountLink.create(
        account=account_id,
        refresh_url=f"{PUBLIC_BASE_URL}/connect/refresh/{order['recipient_token']}",
        return_url=f"{PUBLIC_BASE_URL}/connect/return/{order['recipient_token']}",
        type="account_onboarding",
    )
    return link.url


def refresh_connect_status(order: dict) -> bool:
    account_id = (order.get("stripe_connected_account_id") or "").strip()
    if not account_id:
        return False

    acct = stripe.Account.retrieve(account_id)
    ready = bool(acct.get("details_submitted")) and (
        acct.get("capabilities", {}).get("transfers") == "active"
    )

    update_order(order["id"], connect_onboarding_completed=1 if ready else 0)
    return ready


def process_gift_transfer_for_order(order: dict) -> dict:
    order = get_order_by_id(order["id"])
    gift_amount = float(order.get("gift_amount") or 0)

    if bool(order.get("gift_refunded")):
        return {"status": "gift_already_refunded"}

    if gift_amount <= 0:
        update_order(
            order["id"],
            transfer_completed=1,
            cashout_completed=1,
            transfer_in_progress=0,
            connect_onboarding_completed=1,
        )
        return {"status": "no_gift"}

    if not STRIPE_SECRET_KEY:
        update_order(
            order["id"],
            transfer_completed=1,
            cashout_completed=1,
            transfer_in_progress=0,
            connect_onboarding_completed=1,
        )
        return {"status": "stripe_disabled_test_mode"}

    if not bool(order.get("paid")):
        return {"status": "not_paid"}

    if not bool(order.get("experience_completed")):
        return {"status": "experience_not_completed"}

    if not bool(order.get("connect_onboarding_completed")):
        return {"status": "onboarding_not_ready"}

    if order.get("stripe_transfer_id"):
        update_order(
            order["id"],
            transfer_completed=1,
            cashout_completed=1,
            transfer_in_progress=0,
        )
        return {
            "status": "already_transferred",
            "transfer_id": order.get("stripe_transfer_id"),
        }

    destination = (order.get("stripe_connected_account_id") or "").strip()
    if not destination:
        return {"status": "missing_destination"}

    if not try_acquire_transfer_lock(order["id"]):
        refreshed = get_order_by_id(order["id"])
        if refreshed.get("stripe_transfer_id"):
            return {
                "status": "already_transferred",
                "transfer_id": refreshed.get("stripe_transfer_id"),
            }
        if bool(refreshed.get("gift_refunded")):
            return {"status": "gift_already_refunded"}
        return {"status": "transfer_in_progress"}

    try:
        transfer = stripe.Transfer.create(
            amount=int(round(gift_amount * 100)),
            currency=CURRENCY,
            destination=destination,
            metadata={
                "order_id": order["id"],
                "type": "eterna_gift_transfer",
            },
            transfer_group=f"ETERNA_ORDER_{order['id']}",
        )

        update_order(
            order["id"],
            stripe_transfer_id=transfer.id,
            transfer_completed=1,
            cashout_completed=1,
            transfer_in_progress=0,
        )
        return {"status": "ok", "transfer_id": transfer.id}

    except Exception as e:
        log_error("Transfer error", e)
        update_order(order["id"], transfer_in_progress=0)
        return {
            "status": "error",
            "error": str(e),
            "retry": True,
        }


# =========================================================
# LEGAL
# =========================================================

@app.get("/condiciones", response_class=HTMLResponse)
def condiciones(request: Request):
    return templates.TemplateResponse("condiciones.html", {"request": request})


@app.get("/privacidad", response_class=HTMLResponse)
def privacidad(request: Request):
    return templates.TemplateResponse("privacidad.html", {"request": request})


# =========================================================
# FORM
# =========================================================

def render_create_form() -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Crear ETERNA</title>
        <style>
            * {{ box-sizing: border-box; }}
            html, body {{ margin: 0; min-height: 100%; background: #000; }}
            body {{
                min-height: 100vh;
                background:
                    radial-gradient(circle at top, rgba(255,255,255,0.06), transparent 30%),
                    linear-gradient(180deg, #050505 0%, #000000 100%);
                color: white;
                font-family: Arial, sans-serif;
                padding: 24px;
            }}
            .wrap {{ width: 100%; max-width: 860px; margin: 0 auto; }}
            .card {{
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 28px;
                padding: 28px;
                overflow: hidden;
            }}
            h1 {{
                margin: 0 0 12px 0;
                font-size: 34px;
                text-align: center;
                letter-spacing: 2px;
            }}
            .subtitle {{
                text-align: center;
                color: rgba(255,255,255,0.68);
                line-height: 1.7;
                margin-bottom: 18px;
            }}
            .intro {{
                text-align: center;
                margin: 8px auto 30px auto;
                max-width: 620px;
                min-height: 156px;
            }}
            .intro-line {{
                margin: 0;
                font-size: 20px;
                line-height: 1.8;
                color: rgba(255,255,255,0.92);
                opacity: 0;
                transform: translateY(10px);
                animation: fadeUp 0.8s ease forwards;
            }}
            .intro-line.l1 {{ animation-delay: 0.2s; }}
            .intro-line.l2 {{ animation-delay: 1.4s; }}
            .intro-line.l3 {{ animation-delay: 2.8s; }}
            .intro-line.l4 {{
                animation-delay: 4.2s;
                font-weight: 700;
                letter-spacing: 1.5px;
            }}
            @keyframes fadeUp {{
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            .section {{
                opacity: 0;
                transform: translateY(14px);
                animation: sectionFade 0.8s ease forwards;
            }}
            .section.s1 {{ animation-delay: 0.8s; }}
            .section.s2 {{ animation-delay: 1.1s; }}
            .section.s3 {{ animation-delay: 1.4s; }}
            .section.s4 {{ animation-delay: 1.7s; }}
            .section.s5 {{ animation-delay: 2.0s; }}
            .section.s6 {{ animation-delay: 2.3s; }}
            .section.s7 {{ animation-delay: 2.6s; }}
            @keyframes sectionFade {{
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            .section-title {{
                margin: 22px 0 10px 0;
                font-size: 13px;
                letter-spacing: 1.4px;
                text-transform: uppercase;
                color: rgba(255,255,255,0.55);
            }}
            input, select {{
                width: 100%;
                padding: 15px 16px;
                margin: 8px 0;
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.10);
                background: rgba(255,255,255,0.05);
                color: white;
                outline: none;
                font-size: 15px;
            }}
            select {{
                appearance: none;
                -webkit-appearance: none;
                -moz-appearance: none;
            }}
            input[type="date"],
            input[type="time"] {{
                color-scheme: dark;
            }}
            input::placeholder {{
                color: rgba(255,255,255,0.4);
            }}
            .soft-copy {{
                color: rgba(255,255,255,0.56);
                line-height: 1.8;
                font-size: 14px;
                margin-bottom: 14px;
                text-align: center;
            }}
            .phone-row {{
                display: flex;
                gap: 10px;
                align-items: center;
            }}
            .phone-code {{
                min-width: 120px;
                max-width: 140px;
                flex: 0 0 120px;
            }}
            .phone-input {{
                flex: 1;
            }}
            .photo-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 16px;
                margin-top: 12px;
            }}
            .photo-card {{
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 22px;
                padding: 16px;
            }}
            .photo-label {{
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 1.2px;
                color: rgba(255,255,255,0.45);
                margin-bottom: 8px;
            }}
            .photo-guide {{
                font-size: 15px;
                color: rgba(255,255,255,0.92);
                line-height: 1.5;
                margin-bottom: 12px;
                min-height: 44px;
            }}
            .photo-box {{
                position: relative;
                border: 1px dashed rgba(255,255,255,0.18);
                border-radius: 18px;
                min-height: 210px;
                overflow: hidden;
                background: rgba(255,255,255,0.03);
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 16px;
                cursor: pointer;
            }}
            .photo-box input[type="file"] {{
                position: absolute;
                inset: 0;
                opacity: 0;
                cursor: pointer;
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                z-index: 3;
            }}
            .photo-placeholder {{
                color: rgba(255,255,255,0.58);
                line-height: 1.7;
                font-size: 14px;
                position: relative;
                z-index: 1;
                pointer-events: none;
                max-width: 180px;
            }}
            .photo-preview {{
                position: absolute;
                inset: 0;
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: none;
                z-index: 2;
                border-radius: 18px;
            }}
            .photo-status {{
                margin-top: 10px;
                color: rgba(255,255,255,0.48);
                font-size: 12px;
                line-height: 1.6;
                min-height: 20px;
            }}
            .mini-note {{
                margin-top: 12px;
                color: rgba(255,255,255,0.42);
                font-size: 12px;
                line-height: 1.6;
                text-align: center;
            }}
            .emotion-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 14px;
                margin-top: 12px;
            }}
            .emotion-card {{
                padding: 18px 18px;
                border-radius: 20px;
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                cursor: pointer;
                transition: all 0.25s ease;
            }}
            .emotion-card.selected {{
                border: 1px solid rgba(255,255,255,0.32);
                background: rgba(255,255,255,0.08);
            }}
            .emotion-title {{
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 6px;
            }}
            .emotion-sub {{
                font-size: 13px;
                color: rgba(255,255,255,0.55);
                line-height: 1.45;
            }}
            .mode-box {{
                margin-top: 14px;
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px;
                padding: 12px 14px;
            }}
            .radio-row {{
                display: flex;
                align-items: center;
                gap: 10px;
                margin: 10px 0;
                color: rgba(255,255,255,0.88);
                font-size: 14px;
            }}
            .radio-row input {{
                width: auto;
                margin: 0;
            }}
            .recommended {{
                opacity: 0.5;
                font-size: 12px;
                margin-left: 4px;
            }}
            .phrases-manual.hidden {{
                display: none;
            }}
            .delivery-box {{
                margin-top: 12px;
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px;
                padding: 18px 16px;
            }}
            .delivery-copy {{
                color: rgba(255,255,255,0.86);
                line-height: 1.8;
                font-size: 15px;
                text-align: center;
                margin-bottom: 10px;
            }}
            .delivery-modes {{
                display: grid;
                gap: 12px;
                margin-top: 12px;
            }}
            .delivery-option {{
                border-radius: 18px;
                border: 1px solid rgba(255,255,255,0.08);
                background: rgba(255,255,255,0.04);
                padding: 16px;
            }}
            .delivery-option label {{
                display: block;
                cursor: pointer;
            }}
            .delivery-option-title {{
                font-size: 15px;
                line-height: 1.6;
                color: rgba(255,255,255,0.92);
                font-weight: 600;
            }}
            .delivery-option-sub {{
                margin-top: 6px;
                font-size: 13px;
                line-height: 1.7;
                color: rgba(255,255,255,0.52);
            }}
            .delivery-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                margin-top: 12px;
            }}
            .delivery-grid.hidden {{
                display: none;
            }}
            .delivery-hint {{
                color: rgba(255,255,255,0.48);
                line-height: 1.8;
                font-size: 13px;
                text-align: center;
                margin-top: 10px;
            }}
            .price-box {{
                margin-top: 12px;
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 16px;
                padding: 14px 16px;
                font-size: 14px;
                line-height: 1.8;
                color: rgba(255,255,255,0.82);
            }}
            .hint {{
                margin-top: 12px;
                font-size: 14px;
                line-height: 1.8;
                color: rgba(255,255,255,0.48);
                text-align: center;
            }}
            .buttons {{
                display: grid;
                gap: 12px;
                margin-top: 24px;
            }}
            .btn, button {{
                width: 100%;
                padding: 17px 22px;
                border-radius: 999px;
                border: 0;
                font-weight: bold;
                font-size: 15px;
                text-decoration: none;
                text-align: center;
                cursor: pointer;
            }}
            button {{
                background: white;
                color: black;
            }}
            button:disabled {{
                opacity: 0.7;
                cursor: default;
            }}
            .ghost {{
                display: inline-block;
                background: rgba(255,255,255,0.10);
                color: white;
                border: 1px solid rgba(255,255,255,0.10);
            }}
            .error-box {{
                display: none;
                margin-top: 14px;
                padding: 14px 16px;
                border-radius: 16px;
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.10);
                color: rgba(255,255,255,0.82);
                font-size: 14px;
                line-height: 1.7;
            }}
            @media (max-width: 760px) {{
                .photo-grid,
                .emotion-grid,
                .delivery-grid {{
                    grid-template-columns: 1fr;
                }}
                .phone-row {{
                    flex-direction: row;
                }}
                body {{
                    padding: 16px;
                }}
                .card {{
                    padding: 22px;
                }}
                .intro {{
                    min-height: 170px;
                }}
                .intro-line {{
                    font-size: 18px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="wrap">
            <div class="card">
                <h1>CREAR ETERNA</h1>
                <div class="subtitle">Hay momentos que merecen llegar exactamente cuando deben llegar</div>

                <div class="intro">
                    <p class="intro-line l1">Esto no es un vídeo…</p>
                    <p class="intro-line l2">No es solo un recuerdo…</p>
                    <p class="intro-line l3">Es una espera hecha con intención…</p>
                    <p class="intro-line l4">MAGIA.</p>
                </div>

                <form action="/crear" method="post" enctype="multipart/form-data" id="createForm">
                    <div class="section s1">
                        <div class="section-title">Quién quiere hacer eterno este momento</div>
                        <input name="customer_name" id="customer_name" placeholder="Tu nombre" required>
                        <input name="customer_email" id="customer_email" type="email" placeholder="Tu email">

                        <div class="phone-row">
                            <select name="customer_country_code" id="customer_country_code" class="phone-code">
                                <option value="+34">🇪🇸 +34</option>
                                <option value="+1">🇺🇸 +1</option>
                                <option value="+44">🇬🇧 +44</option>
                                <option value="+33">🇫🇷 +33</option>
                                <option value="+49">🇩🇪 +49</option>
                                <option value="+39">🇮🇹 +39</option>
                                <option value="+52">🇲🇽 +52</option>
                                <option value="+54">🇦🇷 +54</option>
                                <option value="+57">🇨🇴 +57</option>
                                <option value="+351">🇵🇹 +351</option>
                            </select>

                            <input
                                name="customer_phone"
                                id="customer_phone"
                                class="phone-input"
                                placeholder="Tu teléfono"
                                required
                            >
                        </div>
                    </div>

                    <div class="section s2">
                        <div class="section-title">Para quién es esto</div>
                        <input name="recipient_name" id="recipient_name" placeholder="Su nombre" required>

                        <div class="phone-row">
                            <select name="recipient_country_code" id="recipient_country_code" class="phone-code">
                                <option value="+34">🇪🇸 +34</option>
                                <option value="+1">🇺🇸 +1</option>
                                <option value="+44">🇬🇧 +44</option>
                                <option value="+33">🇫🇷 +33</option>
                                <option value="+49">🇩🇪 +49</option>
                                <option value="+39">🇮🇹 +39</option>
                                <option value="+52">🇲🇽 +52</option>
                                <option value="+54">🇦🇷 +54</option>
                                <option value="+57">🇨🇴 +57</option>
                                <option value="+351">🇵🇹 +351</option>
                            </select>

                            <input
                                name="recipient_phone"
                                id="recipient_phone"
                                class="phone-input"
                                placeholder="Su teléfono"
                                required
                            >
                        </div>
                    </div>

                    <div class="section s3">
                        <div class="section-title">Los recuerdos que lo harán volver</div>
                        <div class="soft-copy">
                            Elige 6 fotos que merezcan volver a sentirse.
                        </div>

                        <div class="photo-grid">
                            <div class="photo-card">
                                <div class="photo-label">Foto 1</div>
                                <div class="photo-guide">Una foto suya que diga quién es.</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo1">
                                    <div class="photo-placeholder" id="placeholder_photo1">Toca para elegir una foto de tu galería</div>
                                    <input type="file" name="photo1" id="photo1" accept="image/*" required>
                                </label>
                                <div class="photo-status" id="status_photo1">Aún no has elegido esta foto.</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 2</div>
                                <div class="photo-guide">Un instante que te lleve directo a ella.</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo2">
                                    <div class="photo-placeholder" id="placeholder_photo2">Toca para elegir una foto de tu galería</div>
                                    <input type="file" name="photo2" id="photo2" accept="image/*" required>
                                </label>
                                <div class="photo-status" id="status_photo2">Aún no has elegido esta foto.</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 3</div>
                                <div class="photo-guide">Algo que os una sin necesidad de explicarlo.</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo3">
                                    <div class="photo-placeholder" id="placeholder_photo3">Toca para elegir una foto de tu galería</div>
                                    <input type="file" name="photo3" id="photo3" accept="image/*" required>
                                </label>
                                <div class="photo-status" id="status_photo3">Aún no has elegido esta foto.</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 4</div>
                                <div class="photo-guide">Un recuerdo que todavía vive dentro.</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo4">
                                    <div class="photo-placeholder" id="placeholder_photo4">Toca para elegir una foto de tu galería</div>
                                    <input type="file" name="photo4" id="photo4" accept="image/*" required>
                                </label>
                                <div class="photo-status" id="status_photo4">Aún no has elegido esta foto.</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 5</div>
                                <div class="photo-guide">Una imagen que solo vosotros entendéis.</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo5">
                                    <div class="photo-placeholder" id="placeholder_photo5">Toca para elegir una foto de tu galería</div>
                                    <input type="file" name="photo5" id="photo5" accept="image/*" required>
                                </label>
                                <div class="photo-status" id="status_photo5">Aún no has elegido esta foto.</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 6</div>
                                <div class="photo-guide">La foto que jamás querrías perder.</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo6">
                                    <div class="photo-placeholder" id="placeholder_photo6">Toca para elegir una foto de tu galería</div>
                                    <input type="file" name="photo6" id="photo6" accept="image/*" required>
                                </label>
                                <div class="photo-status" id="status_photo6">Aún no has elegido esta foto.</div>
                            </div>
                        </div>

                        <div class="mini-note">
                            Recomendación: mejor verticales. Idealmente 2 fotos suyas, 2 juntos y 2 finales suyas.
                        </div>
                    </div>

                    <div class="section s4">
                        <div class="section-title">La emoción que quieres dejar</div>

                        <div class="emotion-grid">
                            <div class="emotion-card" data-type="cumpleanos">
                                <div class="emotion-title">Cumpleaños</div>
                                <div class="emotion-sub">Un día que merece quedarse para siempre.</div>
                            </div>
                            <div class="emotion-card" data-type="amor">
                                <div class="emotion-title">Amor</div>
                                <div class="emotion-sub">Cuando lo que sientes ya no cabe dentro.</div>
                            </div>
                            <div class="emotion-card" data-type="familia">
                                <div class="emotion-title">Familia</div>
                                <div class="emotion-sub">Para quien siempre ha estado.</div>
                            </div>
                            <div class="emotion-card" data-type="superacion">
                                <div class="emotion-title">Superación</div>
                                <div class="emotion-sub">Para recordarle todo lo que vale.</div>
                            </div>
                            <div class="emotion-card" data-type="esfuerzo">
                                <div class="emotion-title">Esfuerzo</div>
                                <div class="emotion-sub">Para reconocer lo que a veces no se dice.</div>
                            </div>
                            <div class="emotion-card" data-type="sorpresa">
                                <div class="emotion-title">Sorpresa</div>
                                <div class="emotion-sub">Cuando quieres tocar el corazón sin avisar.</div>
                            </div>
                        </div>

                        <input type="hidden" name="message_type" id="messageType" required>
                    </div>

                    <div class="section s5">
                        <div class="section-title">Las palabras que quieres dejar</div>

                        <div class="mode-box">
                            <div class="radio-row">
                                <input type="radio" id="mode_auto" name="phrase_mode" value="auto" checked>
                                <label for="mode_auto">
                                    Quiero que ETERNA encuentre las palabras
                                    <span class="recommended">(recomendado)</span>
                                </label>
                            </div>

                            <div class="radio-row">
                                <input type="radio" id="mode_manual" name="phrase_mode" value="manual">
                                <label for="mode_manual">Quiero escribir lo que siento</label>
                            </div>
                        </div>

                        <div class="phrases-manual hidden" id="manualPhrases">
                            <input name="phrase_1" id="phrase_1" placeholder="Lo que nunca quieres que olvide" maxlength="160">
                            <input name="phrase_2" id="phrase_2" placeholder="Eso que sientes y a veces no dices" maxlength="160">
                            <input name="phrase_3" id="phrase_3" placeholder="La frase que quieres dejarle para siempre" maxlength="160">
                        </div>
                    </div>

                    <div class="section s6">
                        <div class="section-title">Cuándo debe llegar</div>

                        <div class="delivery-box">
                            <div class="delivery-copy">
                                Puedes dejar que llegue en cuanto esté lista...<br>
                                o programar ese momento íntimo en el que sabes que podrá vivirla de verdad.
                            </div>

                            <div class="delivery-modes">
                                <div class="delivery-option">
                                    <label for="delivery_mode_instant">
                                        <div class="radio-row">
                                            <input type="radio" id="delivery_mode_instant" name="delivery_mode" value="instant" checked>
                                            <span class="delivery-option-title">Enviarlo en cuanto esté listo</span>
                                        </div>
                                        <div class="delivery-option-sub">
                                            Sin coste extra.
                                        </div>
                                    </label>
                                </div>

                                <div class="delivery-option">
                                    <label for="delivery_mode_scheduled">
                                        <div class="radio-row">
                                            <input type="radio" id="delivery_mode_scheduled" name="delivery_mode" value="scheduled">
                                            <span class="delivery-option-title">Guardarlo y entregarlo en un momento exacto</span>
                                        </div>
                                        <div class="delivery-option-sub">
                                            +{money(SCHEDULED_DELIVERY_FEE)}€ para guardarlo y hacer que llegue exactamente cuando tú elijas.
                                        </div>
                                    </label>
                                </div>
                            </div>

                            <div class="delivery-grid hidden" id="scheduledDeliveryGrid">
                                <input
                                    type="date"
                                    name="delivery_date"
                                    id="delivery_date"
                                >
                                <input
                                    type="time"
                                    name="delivery_time"
                                    id="delivery_time"
                                >
                            </div>

                            <div class="delivery-hint">
                                Lo ideal es que pueda vivirlo con calma.<br>
                                Con unos cascos. En silencio. Sin que nadie le moleste.
                            </div>
                        </div>
                    </div>

                    <div class="section s7">
                        <div class="section-title">Dinero a regalar</div>
                        <input
                            name="gift_amount"
                            id="gift_amount"
                            placeholder="Dinero a regalar (€)"
                            type="number"
                            step="0.01"
                            min="0"
                            value="0"
                            required
                        >

                        <div class="price-box">
                            Precio base ETERNA: {money(BASE_PRICE)}€<br>
                            Comisión regalo: {money(FIXED_PLATFORM_FEE)}€ + {(GIFT_COMMISSION_RATE * 100):.0f}% del importe regalado<br>
                            Entrega programada: +{money(SCHEDULED_DELIVERY_FEE)}€ solo si eliges guardarlo y entregarlo en un momento exacto
                        </div>

                        <div class="hint">
                            No solo eliges lo que va a sentir. También eliges cuándo debe ocurrir.
                        </div>

                        <div class="error-box" id="errorBox"></div>

                        <div class="buttons">
                            <button type="submit" id="submitBtn">SEGUIR CREANDO</button>
                            <a class="btn ghost" href="/">Volver</a>
                        </div>
                    </div>
                </form>
            </div>
        </div>

<script>
document.addEventListener("DOMContentLoaded", function () {{

    const STORAGE_KEY = "eterna_create_form_v4";

    const form = document.getElementById("createForm");
    const button = document.getElementById("submitBtn");
    const errorBox = document.getElementById("errorBox");
    const cards = document.querySelectorAll(".emotion-card");
    const messageTypeInput = document.getElementById("messageType");
    const autoRadio = document.getElementById("mode_auto");
    const manualRadio = document.getElementById("mode_manual");
    const manualPhrases = document.getElementById("manualPhrases");
    const deliveryModeInstant = document.getElementById("delivery_mode_instant");
    const deliveryModeScheduled = document.getElementById("delivery_mode_scheduled");
    const scheduledDeliveryGrid = document.getElementById("scheduledDeliveryGrid");

    function showError(message) {{
        if (!errorBox) return;
        errorBox.style.display = "block";
        errorBox.innerText = message || "Ha ocurrido un error.";
    }}

    function clearError() {{
        if (!errorBox) return;
        errorBox.style.display = "none";
        errorBox.innerText = "";
    }}

    function getPersistableData() {{
        return {{
            customer_name: document.getElementById("customer_name")?.value || "",
            customer_email: document.getElementById("customer_email")?.value || "",
            customer_country_code: document.getElementById("customer_country_code")?.value || "+34",
            customer_phone: document.getElementById("customer_phone")?.value || "",
            recipient_name: document.getElementById("recipient_name")?.value || "",
            recipient_country_code: document.getElementById("recipient_country_code")?.value || "+34",
            recipient_phone: document.getElementById("recipient_phone")?.value || "",
            message_type: document.getElementById("messageType")?.value || "",
            phrase_mode: manualRadio && manualRadio.checked ? "manual" : "auto",
            phrase_1: document.getElementById("phrase_1")?.value || "",
            phrase_2: document.getElementById("phrase_2")?.value || "",
            phrase_3: document.getElementById("phrase_3")?.value || "",
            delivery_mode: deliveryModeScheduled && deliveryModeScheduled.checked ? "scheduled" : "instant",
            delivery_date: document.getElementById("delivery_date")?.value || "",
            delivery_time: document.getElementById("delivery_time")?.value || "",
            gift_amount: document.getElementById("gift_amount")?.value || "0"
        }};
    }}

    function saveFormState() {{
        try {{
            localStorage.setItem(STORAGE_KEY, JSON.stringify(getPersistableData()));
        }} catch (e) {{
            console.error("saveFormState error", e);
        }}
    }}

    function restoreFormState() {{
        try {{
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return;

            const data = JSON.parse(raw);

            const ids = [
                "customer_name",
                "customer_email",
                "customer_country_code",
                "customer_phone",
                "recipient_name",
                "recipient_country_code",
                "recipient_phone",
                "phrase_1",
                "phrase_2",
                "phrase_3",
                "delivery_date",
                "delivery_time",
                "gift_amount"
            ];

            ids.forEach((id) => {{
                const el = document.getElementById(id);
                if (el && typeof data[id] !== "undefined") {{
                    el.value = data[id];
                }}
            }});

            if (data.phrase_mode === "manual") {{
                if (manualRadio) manualRadio.checked = true;
                if (autoRadio) autoRadio.checked = false;
            }} else {{
                if (autoRadio) autoRadio.checked = true;
                if (manualRadio) manualRadio.checked = false;
            }}

            if (data.delivery_mode === "scheduled") {{
                if (deliveryModeScheduled) deliveryModeScheduled.checked = true;
                if (deliveryModeInstant) deliveryModeInstant.checked = false;
            }} else {{
                if (deliveryModeInstant) deliveryModeInstant.checked = true;
                if (deliveryModeScheduled) deliveryModeScheduled.checked = false;
            }}

            updatePhraseMode();
            updateDeliveryMode();

            if (data.message_type && messageTypeInput) {{
                messageTypeInput.value = data.message_type;
                cards.forEach((card) => {{
                    if ((card.dataset.type || "") === data.message_type) {{
                        card.classList.add("selected");
                    }} else {{
                        card.classList.remove("selected");
                    }}
                }});
            }}
        }} catch (e) {{
            console.error("restoreFormState error", e);
        }}
    }}

    function bindAutosave() {{
        const selectors = [
            "#customer_name",
            "#customer_email",
            "#customer_country_code",
            "#customer_phone",
            "#recipient_name",
            "#recipient_country_code",
            "#recipient_phone",
            "#phrase_1",
            "#phrase_2",
            "#phrase_3",
            "#delivery_date",
            "#delivery_time",
            "#gift_amount",
            "#mode_auto",
            "#mode_manual",
            "#delivery_mode_instant",
            "#delivery_mode_scheduled"
        ];

        selectors.forEach((selector) => {{
            const el = document.querySelector(selector);
            if (!el) return;

            el.addEventListener("input", saveFormState);
            el.addEventListener("change", saveFormState);
        }});
    }}

    function updatePhraseMode() {{
        if (!manualPhrases) return;

        if (manualRadio && manualRadio.checked) {{
            manualPhrases.classList.remove("hidden");
        }} else {{
            manualPhrases.classList.add("hidden");
        }}

        saveFormState();
    }}

    function updateDeliveryMode() {{
        if (!scheduledDeliveryGrid) return;

        if (deliveryModeScheduled && deliveryModeScheduled.checked) {{
            scheduledDeliveryGrid.classList.remove("hidden");
            document.getElementById("delivery_date").required = true;
            document.getElementById("delivery_time").required = true;
        }} else {{
            scheduledDeliveryGrid.classList.add("hidden");
            document.getElementById("delivery_date").required = false;
            document.getElementById("delivery_time").required = false;
        }}

        saveFormState();
    }}

    cards.forEach((card) => {{
        card.addEventListener("click", function () {{
            cards.forEach((c) => c.classList.remove("selected"));
            card.classList.add("selected");
            if (messageTypeInput) {{
                messageTypeInput.value = card.dataset.type || "";
            }}
            saveFormState();
            clearError();
        }});
    }});

    if (autoRadio) autoRadio.addEventListener("change", updatePhraseMode);
    if (manualRadio) manualRadio.addEventListener("change", updatePhraseMode);
    if (deliveryModeInstant) deliveryModeInstant.addEventListener("change", updateDeliveryMode);
    if (deliveryModeScheduled) deliveryModeScheduled.addEventListener("change", updateDeliveryMode);

    function updatePhotoUI(inputId, file) {{
        const preview = document.getElementById("preview_" + inputId);
        const placeholder = document.getElementById("placeholder_" + inputId);
        const status = document.getElementById("status_" + inputId);

        if (!file) {{
            if (preview) {{
                preview.src = "";
                preview.style.display = "none";
            }}
            if (placeholder) {{
                placeholder.style.display = "block";
            }}
            if (status) {{
                status.innerText = "Aún no has elegido esta foto.";
            }}
            return;
        }}

        const url = URL.createObjectURL(file);

        if (preview) {{
            preview.src = url;
            preview.style.display = "block";
        }}

        if (placeholder) {{
            placeholder.style.display = "none";
        }}

        if (status) {{
            status.innerText = "Foto elegida correctamente.";
        }}
    }}

    function bindPreview(inputId) {{
        const fileInput = document.getElementById(inputId);
        if (!fileInput) return;

        fileInput.addEventListener("change", function () {{
            clearError();

            const file = fileInput.files && fileInput.files[0];
            if (!file) {{
                updatePhotoUI(inputId, null);
                return;
            }}

            if (!(file.type || "").startsWith("image/")) {{
                fileInput.value = "";
                updatePhotoUI(inputId, null);
                showError("Una de las fotos no parece una imagen válida.");
                return;
            }}

            updatePhotoUI(inputId, file);
            saveFormState();
        }});
    }}

    ["photo1", "photo2", "photo3", "photo4", "photo5", "photo6"].forEach(bindPreview);

    function allPhotosPresent() {{
        const ids = ["photo1", "photo2", "photo3", "photo4", "photo5", "photo6"];
        for (const id of ids) {{
            const input = document.getElementById(id);
            if (!input || !input.files || input.files.length === 0) {{
                return false;
            }}
        }}
        return true;
    }}

    function validateBeforeSubmit() {{
        if (!form) {{
            showError("Formulario no disponible.");
            return false;
        }}

        if (!form.checkValidity()) {{
            showError("Revisa los campos. Falta información.");
            return false;
        }}

        const messageType = messageTypeInput ? messageTypeInput.value.trim() : "";
        if (!messageType) {{
            showError("Elige la emoción que quieres dejar.");
            return false;
        }}

        if (!allPhotosPresent()) {{
            showError("Necesitas elegir las 6 fotos.");
            return false;
        }}

        if (manualRadio && manualRadio.checked) {{
            const phrase1 = form.querySelector('input[name="phrase_1"]')?.value.trim();
            const phrase2 = form.querySelector('input[name="phrase_2"]')?.value.trim();
            const phrase3 = form.querySelector('input[name="phrase_3"]')?.value.trim();

            if (!phrase1 || !phrase2 || !phrase3) {{
                showError("Escribe tus 3 frases.");
                return false;
            }}
        }}

        if (deliveryModeScheduled && deliveryModeScheduled.checked) {{
            const deliveryDate = document.getElementById("delivery_date")?.value || "";
            const deliveryTime = document.getElementById("delivery_time")?.value || "";

            if (!deliveryDate || !deliveryTime) {{
                showError("Elige la fecha y la hora de entrega.");
                return false;
            }}

            const deliveryLocal = new Date(deliveryDate + "T" + deliveryTime);
            const now = new Date();

            if (!(deliveryLocal instanceof Date) || isNaN(deliveryLocal.getTime())) {{
                showError("La fecha de entrega no es válida.");
                return false;
            }}

            if (deliveryLocal.getTime() <= now.getTime()) {{
                showError("La fecha de entrega debe estar en el futuro.");
                return false;
            }}
        }}

        const giftAmount = parseFloat(document.getElementById("gift_amount")?.value || "0");
        if (Number.isNaN(giftAmount) || giftAmount < 0) {{
            showError("El importe no es válido.");
            return false;
        }}

        clearError();
        return true;
    }}

    if (!form) return;

    restoreFormState();
    bindAutosave();
    updatePhraseMode();
    updateDeliveryMode();

    form.addEventListener("submit", function (e) {{
        if (!validateBeforeSubmit()) {{
            e.preventDefault();
            return;
        }}

        clearError();

        if (button) {{
            button.disabled = true;
            button.innerText = "Entrando a pago...";
        }}

        try {{
            localStorage.removeItem(STORAGE_KEY);
        }} catch (err) {{
            console.error("localStorage remove error", err);
        }}
    }});

}});
</script>
    </body>
    </html>
    """


async def create_order_and_redirect(
    customer_name: str,
    customer_email: str,
    customer_country_code: str,
    customer_phone: str,
    recipient_name: str,
    recipient_country_code: str,
    recipient_phone: str,
    message_type: str,
    phrase_mode: str,
    phrase_1: str,
    phrase_2: str,
    phrase_3: str,
    delivery_mode: str,
    delivery_date: str,
    delivery_time: str,
    gift_amount: float,
    photo1: UploadFile,
    photo2: UploadFile,
    photo3: UploadFile,
    photo4: UploadFile,
    photo5: UploadFile,
    photo6: UploadFile,
):
    customer_name = (customer_name or "").strip()
    customer_email = (customer_email or "").strip()
    customer_country_code = (customer_country_code or "").strip()
    customer_phone = (customer_phone or "").strip()

    recipient_name = (recipient_name or "").strip()
    recipient_country_code = (recipient_country_code or "").strip()
    recipient_phone = (recipient_phone or "").strip()

    message_type = (message_type or "").strip()
    phrase_mode = (phrase_mode or "auto").strip()

    phrase_1 = (phrase_1 or "").strip()
    phrase_2 = (phrase_2 or "").strip()
    phrase_3 = (phrase_3 or "").strip()

    delivery_mode = (delivery_mode or "instant").strip().lower()
    delivery_date = (delivery_date or "").strip()
    delivery_time = (delivery_time or "").strip()

    if delivery_mode not in {"instant", "scheduled"}:
        raise HTTPException(status_code=400, detail="Modo de entrega no válido")

    if not customer_name:
        raise HTTPException(status_code=400, detail="Tu nombre es obligatorio")

    if not recipient_name:
        raise HTTPException(status_code=400, detail="El nombre del destinatario es obligatorio")

    if not message_type:
        raise HTTPException(status_code=400, detail="Debes elegir una emoción")

    if phrase_mode == "auto":
        phrase_1, phrase_2, phrase_3 = get_phrases_by_type(message_type)
    else:
        if not phrase_1 or not phrase_2 or not phrase_3:
            raise HTTPException(status_code=400, detail="Las 3 frases son obligatorias")

    if len(phrase_1) > 160 or len(phrase_2) > 160 or len(phrase_3) > 160:
        raise HTTPException(status_code=400, detail="Las frases son demasiado largas")

    scheduled_delivery_at = None
    if delivery_mode == "scheduled":
        scheduled_delivery_at = parse_scheduled_delivery_local(delivery_date, delivery_time)
        if not scheduled_delivery_at:
            raise HTTPException(status_code=400, detail="La fecha de entrega no es válida")

        scheduled_dt = parse_iso_dt(scheduled_delivery_at)
        if not scheduled_dt or scheduled_dt <= now_dt():
            raise HTTPException(status_code=400, detail="La fecha de entrega debe estar en el futuro")

    try:
        gift_amount = round(float(gift_amount or 0), 2)
    except Exception:
        raise HTTPException(status_code=400, detail="Importe no válido")

    if gift_amount < 0:
        raise HTTPException(status_code=400, detail="Importe no válido")

    customer_country_code_digits = normalize_phone(customer_country_code)
    recipient_country_code_digits = normalize_phone(recipient_country_code)

    sender_phone_digits = normalize_phone(customer_phone)
    recipient_phone_digits = normalize_phone(recipient_phone)

    if not customer_country_code_digits or not recipient_country_code_digits:
        raise HTTPException(status_code=400, detail="Prefijo telefónico no válido")

    if not sender_phone_digits or not recipient_phone_digits:
        raise HTTPException(status_code=400, detail="Teléfono no válido")

    sender_phone = f"+{customer_country_code_digits}{sender_phone_digits}"
    recipient_phone_norm = f"+{recipient_country_code_digits}{recipient_phone_digits}"

    if not to_e164(sender_phone) or not to_e164(recipient_phone_norm):
        raise HTTPException(status_code=400, detail="Teléfono no válido")

    photos = {
        "photo1": photo1,
        "photo2": photo2,
        "photo3": photo3,
        "photo4": photo4,
        "photo5": photo5,
        "photo6": photo6,
    }

    for slot_name, upload in photos.items():
        if not upload or not upload.filename:
            raise HTTPException(status_code=400, detail=f"Falta {slot_name}")

        content_type = (upload.content_type or "").lower().strip()
        filename = (upload.filename or "").lower().strip()

        is_valid_type = content_type.startswith("image/")
        is_valid_name = (
            filename.endswith(".jpg")
            or filename.endswith(".jpeg")
            or filename.endswith(".png")
            or filename.endswith(".webp")
        )

        if not is_valid_type and not is_valid_name:
            raise HTTPException(status_code=400, detail=f"{slot_name} no es una imagen válida")

    order_id = new_order_id()
    recipient_token = new_token()
    sender_token = new_token()

    fees = calculate_fees(gift_amount, delivery_mode)
    created_at = now_iso()

    conn = db_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO senders (name, email, phone, created_at)
        VALUES (?, ?, ?, ?)
    """, (customer_name, customer_email, sender_phone, created_at))
    sender_id = cur.lastrowid

    cur.execute("""
        INSERT INTO recipients (name, phone, created_at)
        VALUES (?, ?, ?)
    """, (recipient_name, recipient_phone_norm, created_at))
    recipient_id = cur.lastrowid

    placeholders = ", ".join(["?"] * 60)

    cur.execute(f"""
        INSERT INTO orders (
            id, sender_id, recipient_id,
            message_type, phrase_mode,
            phrase_1, phrase_2, phrase_3,
            gift_amount, platform_fixed_fee, platform_variable_fee, platform_total_fee, scheduled_delivery_fee, total_amount,
            paid, delivered_to_recipient, reaction_uploaded,
            cashout_completed, transfer_completed, transfer_in_progress, sender_notified,
            experience_started, experience_completed,
            connect_onboarding_completed, gift_refunded,
            stripe_session_id, stripe_payment_status, stripe_payment_intent_id, stripe_connected_account_id, stripe_transfer_id, stripe_gift_refund_id,
            recipient_token, sender_token,
            reaction_video_local, reaction_video_public_url, experience_video_url, share_video_url,
            gift_refund_deadline_at,
            recipient_sms_sent_at, sender_sms_sent_at, recipient_sms_sid, sender_sms_sid,
            recipient_sms_attempts, sender_sms_attempts, recipient_sms_error, sender_sms_error,
            reaction_upload_pending, reaction_upload_error, eterna_completed,
            delivery_mode, scheduled_delivery_at, delivery_locked, delivery_sent, delivery_sent_at,
            video_render_requested, video_render_requested_at,
            recipient_session_token, recipient_session_claimed_at,
            created_at, updated_at
        )
        VALUES ({placeholders})
    """, (
        order_id, sender_id, recipient_id,
        message_type, phrase_mode,
        phrase_1, phrase_2, phrase_3,
        fees["gift_amount"], fees["fixed_fee"], fees["variable_fee"], fees["total_fee"], fees["scheduled_delivery_fee"], fees["total_amount"],
        0, 0, 0,
        0, 0, 0, 0,
        0, 0,
        0, 0,
        None, None, None, None, None, None,
        recipient_token, sender_token,
        None, None, None, None,
        None,
        None, None, None, None,
        0, 0, None, None,
        0, None, 0,
        delivery_mode, scheduled_delivery_at, 1 if delivery_mode == "scheduled" else 0, 0, None,
        0, None,
        None, None,
        created_at, created_at
    ))

    conn.commit()
    conn.close()

    try:
        for slot_name, upload in photos.items():
            filepath = build_photo_path(order_id, slot_name, upload)

            with open(filepath, "wb") as f:
                while True:
                    chunk = await upload.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)

            insert_asset(
                order_id=order_id,
                asset_type=slot_name,
                file_url=filepath,
                storage_provider="local",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando fotos: {e}")
    finally:
        for upload in photos.values():
            try:
                await upload.close()
            except Exception:
                pass

    if not STRIPE_SECRET_KEY:
        update_order(
            order_id,
            paid=1,
            stripe_payment_status="test_no_stripe",
            gift_refund_deadline_at=gift_refund_deadline_iso(),
            delivery_locked=1 if delivery_mode == "scheduled" else 0,
        )

        try:
            order = get_order_by_id(order_id)
            if not render_request_already_marked(order) and not original_video_ready(order):
                mark_video_render_requested(order_id)
                trigger_video_engine(order_id, [phrase_1, phrase_2, phrase_3])
                print("⏳ Render aceptado por el video engine. Esperando callback.")
        except Exception as e:
            clear_video_render_requested(order_id)
            log_error("video engine test_no_stripe", e)

        return RedirectResponse(url=f"/post-pago/{order_id}", status_code=303)

    try:
        session = stripe.checkout.Session.create(
            client_reference_id=order_id,
            metadata={"order_id": order_id},
            mode="payment",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": CURRENCY,
                        "product_data": {
                            "name": "ETERNA",
                            "description": (
                                f"Base {money(BASE_PRICE)}€ + "
                                f"regalo {money(fees['gift_amount'])}€ + "
                                f"comisión {money(fees['total_fee'])}€ + "
                                f"programación {money(fees['scheduled_delivery_fee'])}€"
                            ),
                        },
                        "unit_amount": int(round(fees["total_amount"] * 100)),
                    },
                    "quantity": 1,
                }
            ],
            success_url=f"{PUBLIC_BASE_URL}/checkout-exito/{order_id}",
            cancel_url=f"{PUBLIC_BASE_URL}/crear",
        )
        update_order(order_id, stripe_session_id=session.id, stripe_payment_status="created")
        return RedirectResponse(url=session.url, status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando checkout Stripe: {e}")


# =========================================================
# HOME / CREATE
# =========================================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/crear", response_class=HTMLResponse)
def crear_get():
    return render_create_form()


@app.post("/crear")
async def crear_post(
    customer_name: str = Form(...),
    customer_email: str = Form(""),
    customer_country_code: str = Form("+34"),
    customer_phone: str = Form(...),
    recipient_name: str = Form(...),
    recipient_country_code: str = Form("+34"),
    recipient_phone: str = Form(...),
    message_type: str = Form(...),
    phrase_mode: str = Form("auto"),
    phrase_1: str = Form(""),
    phrase_2: str = Form(""),
    phrase_3: str = Form(""),
    delivery_mode: str = Form("instant"),
    delivery_date: str = Form(""),
    delivery_time: str = Form(""),
    gift_amount: float = Form(0),
    photo1: UploadFile = File(...),
    photo2: UploadFile = File(...),
    photo3: UploadFile = File(...),
    photo4: UploadFile = File(...),
    photo5: UploadFile = File(...),
    photo6: UploadFile = File(...),
):
    return await create_order_and_redirect(
        customer_name=customer_name,
        customer_email=customer_email,
        customer_country_code=customer_country_code,
        customer_phone=customer_phone,
        recipient_name=recipient_name,
        recipient_country_code=recipient_country_code,
        recipient_phone=recipient_phone,
        message_type=message_type,
        phrase_mode=phrase_mode,
        phrase_1=phrase_1,
        phrase_2=phrase_2,
        phrase_3=phrase_3,
        delivery_mode=delivery_mode,
        delivery_date=delivery_date,
        delivery_time=delivery_time,
        gift_amount=gift_amount,
        photo1=photo1,
        photo2=photo2,
        photo3=photo3,
        photo4=photo4,
        photo5=photo5,
        photo6=photo6,
    )


# =========================================================
# DELIVERY WORKER
# =========================================================

def list_pending_scheduled_deliveries():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id
        FROM orders
        WHERE
            paid = 1
            AND COALESCE(delivery_sent, 0) = 0
            AND COALESCE(experience_video_url, '') <> ''
            AND COALESCE(recipient_sms_attempts, 0) < 3
        ORDER BY created_at ASC
    """)
    rows = cur.fetchall()
    conn.close()
    return [r["id"] for r in rows]


def list_pending_sender_notifications():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id
        FROM orders
        WHERE
            paid = 1
            AND COALESCE(sender_sms_sent_at, '') = ''
            AND COALESCE(reaction_uploaded, 0) = 1
            AND COALESCE(sender_sms_attempts, 0) < 3
        ORDER BY created_at ASC
    """)
    rows = cur.fetchall()
    conn.close()
    return [r["id"] for r in rows]


def process_all_due_scheduled_deliveries() -> list[dict]:
    results = []
    for order_id in list_pending_scheduled_deliveries():
        try:
            result = process_scheduled_recipient_delivery(order_id)
            print("📦 Worker delivery:", order_id, result)
            results.append({
                "order_id": order_id,
                "result": result,
            })
        except Exception as e:
            log_error("delivery_worker_process", e)
            results.append({
                "order_id": order_id,
                "result": {"ok": False, "reason": str(e)},
            })
    return results


def process_all_due_sender_notifications() -> list[dict]:
    results = []
    for order_id in list_pending_sender_notifications():
        try:
            order = maybe_mark_eterna_completed(order_id)
            result = try_send_sender_sms(order)
            print("📩 Worker sender sms:", order_id, result)
            results.append({
                "order_id": order_id,
                "result": result,
            })
        except Exception as e:
            log_error("sender_worker_process", e)
            results.append({
                "order_id": order_id,
                "result": {"ok": False, "reason": str(e)},
            })
    return results


def delivery_worker_loop():
    print("🚀 DELIVERY WORKER STARTED")
    while True:
        try:
            process_all_due_scheduled_deliveries()
            process_all_due_sender_notifications()
        except Exception as e:
            log_error("delivery_worker_loop", e)
        time.sleep(max(5, DELIVERY_WORKER_INTERVAL_SECONDS))


def ensure_delivery_worker_started():
    global DELIVERY_WORKER_STARTED

    if not DELIVERY_WORKER_ENABLED:
        print("⏸ DELIVERY WORKER DISABLED")
        return

    with DELIVERY_WORKER_LOCK:
        if DELIVERY_WORKER_STARTED:
            return

        thread = threading.Thread(
            target=delivery_worker_loop,
            daemon=True,
            name="eterna-delivery-worker",
        )
        thread.start()
        DELIVERY_WORKER_STARTED = True
        print("✅ DELIVERY WORKER THREAD LANZADO")


@app.on_event("startup")
def startup_event():
    ensure_delivery_worker_started()


# =========================================================
# RECIPIENT ENTRY
# =========================================================

@app.get("/pedido/{recipient_token}", response_class=HTMLResponse)
def pedido(request: Request, recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(order.get("paid")):
        title = "Tu ETERNA aún no está lista"
        text = "Todavía estamos esperando a que todo quede preparado."
        soft = "Cuando este momento esté listo de verdad, aquí cambiará solo."
        button_href = "#"
        button_text = "Esperando..."
        disabled = True

    elif not original_video_ready(order):
        title = "Tu ETERNA ya está en camino"
        text = "Estamos terminando de preparar lo que alguien quiso hacerte llegar."
        soft = "El acceso se abrirá solo cuando el vídeo esté listo de verdad."
        button_href = "#"
        button_text = "Preparando..."
        disabled = True

    elif not delivery_is_unlocked(order):
        title = "Aún no es el momento"
        text = "ETERNA ya está guardada."
        soft = (
            f"Todo está preparado para llegar el {scheduled_delivery_display(order)}. "
            "No se abrirá antes."
        )
        button_href = "#"
        button_text = "Esperando su momento..."
        disabled = True

    elif bool(order.get("experience_completed")):
        response = RedirectResponse(url=f"/mi-video/{recipient_token}", status_code=303)
        if not attach_recipient_session_if_needed(order, request, response):
            return render_viral_block_page()
        return response

    else:
        title = "Hay algo para ti"
        text = "Alguien quiso dejarte un momento que no se olvida."
        soft = "Cuando estés listo, entra y vívelo de verdad."
        button_href = f"/experiencia/{recipient_token}"
        button_text = "Entrar"
        disabled = False

    refresh = '<meta http-equiv="refresh" content="6">' if disabled else ""

    button_html = (
        f'<a href="{safe_attr(button_href)}" class="btn">{safe_text(button_text)}</a>'
        if not disabled
        else f'<div class="btn disabled">{safe_text(button_text)}</div>'
    )

    response = HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        {refresh}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ETERNA</title>
        <style>
            * {{ box-sizing: border-box; }}
            html, body {{
                margin: 0;
                min-height: 100%;
                background: #000;
            }}
            body {{
                min-height: 100vh;
                background:
                    radial-gradient(circle at top, rgba(255,255,255,0.06), transparent 30%),
                    linear-gradient(180deg, #050505 0%, #000000 100%);
                color: white;
                font-family: Arial, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 24px;
            }}
            .wrap {{
                width: 100%;
                max-width: 720px;
                margin: 0 auto;
            }}
            .eyebrow {{
                font-size: 13px;
                letter-spacing: 0.16em;
                text-transform: uppercase;
                color: rgba(255,255,255,0.34);
                margin-bottom: 18px;
            }}
            h1 {{
                margin: 0;
                font-size: 48px;
                line-height: 1.12;
                font-weight: 700;
            }}
            .main {{
                margin-top: 24px;
                font-size: 24px;
                line-height: 1.7;
                color: rgba(255,255,255,0.88);
            }}
            .soft {{
                margin: 28px auto 0 auto;
                max-width: 620px;
                font-size: 16px;
                line-height: 1.8;
                color: rgba(255,255,255,0.46);
            }}
            .btn {{
                display: inline-block;
                width: 100%;
                max-width: 420px;
                margin-top: 34px;
                padding: 18px 22px;
                border-radius: 999px;
                background: white;
                color: black;
                text-decoration: none;
                font-weight: bold;
                font-size: 16px;
            }}
            .btn.disabled {{
                background: rgba(255,255,255,0.12);
                color: rgba(255,255,255,0.58);
                cursor: default;
            }}
            @media (max-width: 640px) {{
                h1 {{ font-size: 40px; }}
                .main {{ font-size: 21px; }}
            }}
        </style>
    </head>
    <body>
        <div class="wrap">
            <div class="eyebrow">ETERNA</div>
            <h1>{safe_text(title)}</h1>
            <div class="main">{safe_text(text)}</div>
            <div class="soft">{safe_text(soft)}</div>
            {button_html}
        </div>
    </body>
    </html>
    """)

    if not disabled:
        if not attach_recipient_session_if_needed(order, request, response):
            return render_viral_block_page()

    return response


# =========================================================
# CHECKOUT / WEBHOOK / CALLBACK
# =========================================================

@app.get("/checkout-exito/{order_id}", response_class=HTMLResponse)
def checkout_exito(order_id: str):
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ETERNA</title>
        <style>
            * {{ box-sizing: border-box; }}
            html, body {{ margin: 0; min-height: 100%; background: #000; }}

            body {{
                min-height: 100vh;
                background:
                    radial-gradient(circle at top, rgba(255,255,255,0.06), transparent 30%),
                    linear-gradient(180deg, #050505 0%, #000000 100%);
                color: white;
                font-family: Arial, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 24px;
            }}

            .wrap {{
                width: 100%;
                max-width: 720px;
                margin: 0 auto;
            }}

            .main {{
                font-size: 22px;
                line-height: 1.8;
                color: rgba(255,255,255,0.92);
            }}

            .eterna-text {{
                max-width: 600px;
                margin: 0 auto;
            }}

            .eterna-heart {{
                display: inline-block;
                animation: eternaHeartbeat 3.6s ease-in-out infinite;
            }}

            @keyframes eternaHeartbeat {{
                0%   {{ transform: scale(1); opacity: 0.9; }}
                10%  {{ transform: scale(1.12); opacity: 1; }}
                20%  {{ transform: scale(1); opacity: 0.95; }}

                35%  {{ transform: scale(1.08); opacity: 1; }}
                50%  {{ transform: scale(1); opacity: 0.9; }}

                100% {{ transform: scale(1); opacity: 0.9; }}
            }}

            .eterna-subtext {{
                margin-top: 28px;
                font-size: 16px;
                line-height: 1.8;
                color: rgba(255,255,255,0.72);
            }}

            .buttons {{
                margin-top: 34px;
                display: grid;
                gap: 12px;
                max-width: 420px;
                margin-left: auto;
                margin-right: auto;
            }}

            .btn {{
                display: block;
                width: 100%;
                padding: 17px 22px;
                border-radius: 999px;
                background: white;
                color: black;
                text-decoration: none;
                font-weight: bold;
                font-size: 15px;
            }}

            .ghost {{
                background: rgba(255,255,255,0.10);
                color: white;
                border: 1px solid rgba(255,255,255,0.10);
            }}
        </style>
    </head>

    <body>
        <div class="wrap">

            <div class="main eterna-text">
                Lo que das<br>
                se queda en alguien.<br><br>

                Y un día,<br>
                <span class="eterna-heart">vuelve</span>

                <div class="eterna-subtext">
                    Ahora solo queda esperar<br>
                    a que te alcance la emoción<br>
                    que acaba de nacer al otro lado.
                </div>
            </div>

            <div class="buttons">
                <a class="btn" href="/crear">Crear otra experiencia</a>
                <a class="btn ghost" href="/">Volver</a>
            </div>

        </div>
    </body>
    </html>
    """)


@app.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Falta STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Payload inválido")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Firma inválida")

    if event["type"] != "checkout.session.completed":
        return {"status": "ignored"}

    session = event["data"]["object"]

    order_id = (session.get("client_reference_id") or "").strip()
    if not order_id:
        metadata = session.get("metadata", {}) or {}
        order_id = (metadata.get("order_id") or "").strip()

    if not order_id:
        stripe_session_id = (session.get("id") or "").strip()
        if stripe_session_id:
            try:
                order = get_order_by_stripe_session_id(stripe_session_id)
                order_id = order["id"]
            except Exception:
                order_id = ""

    print("📦 order_id webhook:", order_id)

    if not order_id:
        raise HTTPException(status_code=400, detail="order_id missing")

    try:
        order = get_order_by_id(order_id)
    except Exception:
        raise HTTPException(status_code=404, detail="order_not_found")

    try:
        stripe_payment_status = (session.get("payment_status") or "paid").strip()
        stripe_payment_intent_id = (session.get("payment_intent") or "").strip() or None
        stripe_session_id = (session.get("id") or "").strip() or None

        update_order(
            order_id,
            paid=1,
            stripe_session_id=stripe_session_id or order.get("stripe_session_id"),
            stripe_payment_status=stripe_payment_status,
            stripe_payment_intent_id=stripe_payment_intent_id,
            gift_refund_deadline_at=order.get("gift_refund_deadline_at") or gift_refund_deadline_iso(),
            delivery_locked=1 if (order.get("delivery_mode") or "instant") == "scheduled" else 0,
        )

        order = get_order_by_id(order_id)

        if original_video_ready(order):
            return {
                "status": "ok",
                "reason": "video_already_ready",
                "order_id": order_id,
            }

        if render_request_already_marked(order):
            return {
                "status": "ok",
                "reason": "render_already_requested",
                "order_id": order_id,
            }

        phrases = [
            (order.get("phrase_1") or "").strip(),
            (order.get("phrase_2") or "").strip(),
            (order.get("phrase_3") or "").strip(),
        ]

        try:
            mark_video_render_requested(order_id)
            data = trigger_video_engine(order_id, phrases)
            print("✅ Video engine aceptó el trabajo:", data)
        except Exception as e:
            clear_video_render_requested(order_id)
            log_error("webhook_video_engine", e)
            raise HTTPException(status_code=500, detail=f"video_engine_error: {e}")

        return {"status": "ok", "reason": "render_requested"}

    except Exception as e:
        log_error("webhook", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/internal/video-ready")
async def internal_video_ready(request: Request):
    incoming_secret = (request.headers.get("X-Video-Engine-Secret") or "").strip()

    if VIDEO_READY_CALLBACK_SECRET:
        if incoming_secret != VIDEO_READY_CALLBACK_SECRET:
            return JSONResponse(
                status_code=403,
                content={"status": "error", "reason": "invalid_secret"},
            )

    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "reason": "invalid_json"},
        )

    order_id = (data.get("order_id") or "").strip()
    video_url = (data.get("video_url") or "").strip()

    print("🎬 CALLBACK VIDEO READY")
    print("🎬 order_id:", order_id)
    print("🎬 video_url:", video_url)

    if not order_id or not video_url:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "reason": "missing_data"},
        )

    try:
        order = get_order_by_id(order_id)

        if not bool(order.get("paid")):
            return JSONResponse(
                status_code=400,
                content={"status": "error", "reason": "order_not_paid"},
            )

        existing_video = (order.get("experience_video_url") or "").strip()

        if existing_video:
            print("⚠️ Callback duplicado ignorado")
            return JSONResponse({
                "status": "ok",
                "reason": "video_already_saved",
                "order_id": order_id,
                "video_url": existing_video,
                "recipient_url": recipient_experience_url_from_order(order),
                "sender_url": sender_pack_url_from_order(order),
            })

        update_order(
            order_id,
            experience_video_url=video_url,
            video_render_requested=1,
        )

        if not asset_exists(order_id, "rendered_video", video_url):
            insert_asset(
                order_id=order_id,
                asset_type="rendered_video",
                file_url=video_url,
                storage_provider="video_engine",
            )

        order = get_order_by_id(order_id)

        print("🔥 CALLBACK VIDEO READY 🔥")
        print("🎬 VIDEO GENERADO")
        print("➡️ Recipient experience:", recipient_experience_url_from_order(order))
        print("➡️ Sender pack:", sender_pack_url_from_order(order))
        print("🕒 delivery_mode:", order.get("delivery_mode"))
        print("🕒 scheduled_delivery_at:", order.get("scheduled_delivery_at"))
        print("🕒 scheduled_delivery_display:", scheduled_delivery_display(order))
        print("🕒 scheduled_delivery_ready:", scheduled_delivery_ready(order))
        print("📦 delivery_sent:", bool(order.get("delivery_sent")))

        # SOLO AQUÍ intentamos enviar al regalado,
        # porque aquí ya sabemos que el vídeo real existe.
        delivery_result = process_scheduled_recipient_delivery(order_id)
        print("📩 Resultado entrega programada callback:", delivery_result)

        return JSONResponse({
            "status": "ok",
            "order_id": order_id,
            "video_url": video_url,
            "recipient_url": recipient_experience_url_from_order(order),
            "sender_url": sender_pack_url_from_order(order),
            "delivery_mode": order.get("delivery_mode"),
            "scheduled_delivery_at": order.get("scheduled_delivery_at"),
            "scheduled_delivery_display": scheduled_delivery_display(order),
            "delivery_result": delivery_result,
        })

    except Exception as e:
        log_error("internal_video_ready", e)
        return JSONResponse(
            status_code=500,
            content={"status": "error", "reason": str(e)},
        )


# =========================================================
# POST PAYMENT
# =========================================================

@app.get("/post-pago/{order_id}")
def post_pago(order_id: str):
    order = get_order_by_id(order_id)

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/checkout-exito/{order_id}", status_code=303)

    return RedirectResponse(url=f"/resumen/{order_id}", status_code=303)


@app.get("/resumen/{order_id}", response_class=HTMLResponse)
def resumen(order_id: str):
    order = get_order_by_id(order_id)

    recipient_name = safe_text(order.get("recipient_name") or "esa persona")
    video_ready = original_video_ready(order)
    delivery_sent_flag = bool(order.get("delivery_sent"))
    delivery_display = safe_text(scheduled_delivery_display(order))
    delivery_mode = (order.get("delivery_mode") or "instant").strip()

    sender_code, sender_number = split_phone_for_form(order.get("sender_phone") or "")
    recipient_code, recipient_number = split_phone_for_form(order.get("recipient_phone") or "")

    if delivery_sent_flag:
        status_line = "Tu ETERNA ya ha salido"
        sub_line = f"{recipient_name} ya tiene su mensaje."
        soft_line = "El momento ya está ocurriendo exactamente cuando debía ocurrir."
    elif video_ready and delivery_mode == "scheduled":
        status_line = "Tu ETERNA ya está guardada"
        sub_line = f"Todo quedará listo para llegar el {delivery_display}."
        soft_line = "No se enviará antes. Llegará exactamente cuando debe llegar."
    elif video_ready and delivery_mode == "instant":
        status_line = "Tu ETERNA está lista"
        sub_line = "En cuanto quede procesada del todo, saldrá automáticamente."
        soft_line = "No hace falta esperar una fecha concreta: se enviará en cuanto esté lista."
    else:
        if delivery_mode == "scheduled":
            status_line = "Pago confirmado"
            sub_line = "ETERNA ya se está preparando."
            soft_line = (
                f"Cuando todo esté listo, quedará guardada para llegar el {delivery_display}. "
                "No se enviará antes."
            )
        else:
            status_line = "Pago confirmado"
            sub_line = "ETERNA ya se está preparando."
            soft_line = (
                "En cuanto el vídeo esté terminado de verdad, se enviará automáticamente."
            )

    refresh = '<meta http-equiv="refresh" content="8">' if not delivery_sent_flag else ""

    preload_data = {
        "customer_name": order.get("sender_name") or "",
        "customer_email": order.get("sender_email") or "",
        "customer_country_code": sender_code,
        "customer_phone": sender_number,
        "recipient_name": order.get("recipient_name") or "",
        "recipient_country_code": recipient_code,
        "recipient_phone": recipient_number,
        "message_type": order.get("message_type") or "",
        "phrase_mode": order.get("phrase_mode") or "auto",
        "phrase_1": order.get("phrase_1") or "",
        "phrase_2": order.get("phrase_2") or "",
        "phrase_3": order.get("phrase_3") or "",
        "delivery_mode": order.get("delivery_mode") or "instant",
        "gift_amount": str(order.get("gift_amount") or "0"),
    }

    preload_json = html.escape(json.dumps(preload_data), quote=True)

    extra_fee_line = ""
    if float(order.get("scheduled_delivery_fee") or 0) > 0:
        extra_fee_line = f"""
            <div style="margin-top:10px;font-size:15px;line-height:1.8;color:rgba(255,255,255,0.56);">
                Programación y guardado del momento: {safe_text(format_amount_display(order.get("scheduled_delivery_fee") or 0))}
            </div>
        """

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        {refresh}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ETERNA</title>
    </head>
    <body style="margin:0;min-height:100vh;background:#000;color:white;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;text-align:center;padding:24px;box-sizing:border-box;">
        <div style="max-width:760px;width:100%;">
            <h1 style="font-size:42px;line-height:1.2;margin:0 0 22px 0;font-weight:700;">
                {status_line}
            </h1>

            <div style="font-size:22px;line-height:1.8;color:rgba(255,255,255,0.86);">
                {sub_line}
            </div>

            <div style="margin-top:24px;font-size:17px;line-height:1.8;color:rgba(255,255,255,0.62);">
                Modo de entrega: {"momento exacto" if delivery_mode == "scheduled" else "en cuanto esté lista"}
            </div>

            <div style="margin-top:8px;font-size:16px;line-height:1.8;color:rgba(255,255,255,0.54);">
                {delivery_display}
            </div>

            {extra_fee_line}

            <div style="margin-top:28px;font-size:16px;line-height:1.7;color:rgba(255,255,255,0.45);">
                {soft_line}
            </div>

            <div style="margin-top:34px;display:grid;gap:12px;max-width:420px;margin-left:auto;margin-right:auto;">
                <a
                    href="#"
                    id="createAgainBtn"
                    style="display:block;width:100%;padding:17px 22px;border-radius:999px;background:white;color:black;text-decoration:none;font-weight:bold;font-size:15px;"
                >
                    Crear otra ETERNA
                </a>

                <a
                    href="/"
                    style="display:block;width:100%;padding:17px 22px;border-radius:999px;background:rgba(255,255,255,0.10);color:white;text-decoration:none;font-weight:bold;font-size:15px;border:1px solid rgba(255,255,255,0.10);"
                >
                    Volver al inicio
                </a>
            </div>
        </div>

        <script>
            const STORAGE_KEY = "eterna_create_form_v4";
            const preloadData = JSON.parse("{preload_json}");
            const btn = document.getElementById("createAgainBtn");

            if (btn) {{
                btn.addEventListener("click", function (e) {{
                    e.preventDefault();

                    try {{
                        localStorage.setItem(STORAGE_KEY, JSON.stringify(preloadData));
                    }} catch (err) {{
                        console.error("preload eterna error", err);
                    }}

                    window.location.href = "/crear";
                }});
            }}
        </script>
    </body>
    </html>
    """)


# =========================================================
# EXPERIENCE LOCK
# =========================================================

@app.post("/start-experience")
def start_experience(request: Request, recipient_token: str = Form(...)):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(order.get("paid")):
        raise HTTPException(status_code=403, detail="Pedido no pagado")

    if not original_video_ready(order):
        return JSONResponse({
            "status": "video_not_ready",
            "redirect_url": f"/pedido/{recipient_token}",
        })

    if not delivery_is_unlocked(order):
        return JSONResponse({
            "status": "not_unlocked_yet",
            "redirect_url": f"/pedido/{recipient_token}",
        })

    if not has_valid_recipient_session(order, request):
        return JSONResponse({
            "status": "invalid_access",
            "redirect_url": f"/pedido/{recipient_token}",
        })

    result = try_start_experience(order["id"])

    if result == "not_paid":
        raise HTTPException(status_code=403, detail="Pedido no pagado")

    if result == "video_not_ready":
        return JSONResponse({
            "status": "video_not_ready",
            "redirect_url": f"/pedido/{recipient_token}",
        })

    if result == "already_completed":
        return JSONResponse({
            "status": "already_completed",
            "redirect_url": f"/cobrar/{recipient_token}",
        })

    if result == "already_started":
        return JSONResponse({
            "status": "already_started",
            "redirect_url": f"/mi-video/{recipient_token}",
        })

    return JSONResponse({"status": "ok"})


# =========================================================
# EXPERIENCE (VERSIÓN ESTABLE)
# =========================================================

@app.get("/experiencia/{recipient_token}", response_class=HTMLResponse)
def experiencia(request: Request, recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not original_video_ready(order):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not delivery_is_unlocked(order):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not has_valid_recipient_session(order, request):
        return render_viral_block_page()

    if bool(order.get("experience_completed")):
        return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)

    experience_video_url = (order.get("experience_video_url") or "").strip()
    gift_amount = float(order.get("gift_amount") or 0)

    if gift_amount > 0:
        payoff_title = f"Has recibido {format_amount_display(gift_amount)}"
        payoff_text = "Este momento también llevaba algo más para ti."
        cobrar_title = f"Has recibido {format_amount_display(gift_amount)}"
        cobrar_text = "Estamos guardando este momento mientras te llevamos a continuar."
    else:
        payoff_title = "Esto era para ti"
        payoff_text = "Quédate un segundo más dentro de este momento."
        cobrar_title = "Esto era para ti"
        cobrar_text = "Estamos guardando este momento mientras te llevamos a continuar."

    html_page = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>ETERNA</title>
<style>
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: black;
    overflow: hidden;
    font-family: Arial, sans-serif;
}

body {
    position: fixed;
    inset: 0;
    background: black;
}

.wrap {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: black;
}

video {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
    background: black;
}

.overlay {
    position: absolute;
    inset: 0;
    z-index: 30;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        radial-gradient(circle at top, rgba(255,255,255,0.05), transparent 32%),
        linear-gradient(180deg, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0.90) 100%);
    padding: 28px;
    text-align: center;
}

.overlay.hidden {
    display: none;
}

.overlay-card {
    width: 100%;
    max-width: 560px;
    margin: 0 auto;
}

.eyebrow {
    font-size: 12px;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.36);
    margin-bottom: 24px;
}

.title {
    font-size: 54px;
    line-height: 1.06;
    font-weight: 700;
    margin: 0 0 22px 0;
    color: white;
}

.text {
    font-size: 24px;
    line-height: 1.7;
    color: rgba(255,255,255,0.86);
    margin: 0 auto 22px auto;
    max-width: 520px;
}

.soft {
    font-size: 16px;
    line-height: 1.8;
    color: rgba(255,255,255,0.46);
    margin: 0 auto 34px auto;
    max-width: 460px;
}

.btn {
    display: inline-block;
    min-width: 220px;
    padding: 18px 26px;
    border-radius: 999px;
    border: 0;
    background: white;
    color: black;
    font-weight: 700;
    font-size: 17px;
    cursor: pointer;
}

.btn:disabled {
    opacity: 0.7;
    cursor: default;
}

.payoff {
    position: absolute;
    inset: 0;
    z-index: 35;
    display: none;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 28px;
    background:
        radial-gradient(circle at top, rgba(255,255,255,0.04), transparent 30%),
        linear-gradient(180deg, rgba(0,0,0,0.84) 0%, rgba(0,0,0,0.96) 100%);
}

.payoff.show {
    display: flex;
}

.payoff-card {
    width: 100%;
    max-width: 560px;
    margin: 0 auto;
}

.payoff-title {
    font-size: 46px;
    line-height: 1.12;
    font-weight: 700;
    margin: 0 0 18px 0;
    color: white;
}

.payoff-text {
    font-size: 22px;
    line-height: 1.7;
    color: rgba(255,255,255,0.82);
    margin: 0 auto;
    max-width: 520px;
}

.loader {
    margin-top: 28px;
    font-size: 15px;
    line-height: 1.7;
    color: rgba(255,255,255,0.48);
}

@media (max-width: 720px) {
    .title {
        font-size: 42px;
    }

    .text {
        font-size: 21px;
    }

    .payoff-title {
        font-size: 36px;
    }

    .payoff-text {
        font-size: 19px;
    }
}
</style>
</head>
<body>
<div class="wrap">
    <video
        id="video"
        playsinline
        webkit-playsinline
        preload="auto"
    >
        <source src="__VIDEO_URL__" type="__VIDEO_TYPE__">
    </video>

    <div class="overlay" id="overlay">
        <div class="overlay-card">
            <div class="eyebrow">ETERNA</div>
            <h1 class="title">Shhh…</h1>
            <div class="text">
                Esto no es un vídeo.<br>
                Es un momento que está a punto de ocurrir.
            </div>
            <div class="soft">
                Cuando estés listo, pulsa y vívelo de verdad.
            </div>
            <button class="btn" id="startBtn">Estoy listo</button>
        </div>
    </div>

    <div class="payoff" id="payoff">
        <div class="payoff-card">
            <div class="payoff-title" id="payoffTitle">__PAYOFF_TITLE__</div>
            <div class="payoff-text" id="payoffText">__PAYOFF_TEXT__</div>
            <div class="loader" id="payoffLoader">Guardando este momento…</div>
        </div>
    </div>
</div>

<script>
const startBtn = document.getElementById("startBtn");
const overlay = document.getElementById("overlay");
const video = document.getElementById("video");
const payoff = document.getElementById("payoff");
const payoffLoader = document.getElementById("payoffLoader");
const recipientToken = "__RECIPIENT_TOKEN__";

let stream = null;
let mediaRecorder = null;
let recordedChunks = [];
let finishing = false;
let recordingMimeType = "";
let recordingExtension = "webm";
let experienceStarted = false;
let finishTimeout = null;

function detectRecordingFormat() {
    const candidates = [
        { mimeType: "video/mp4", extension: "mp4" },
        { mimeType: "video/webm;codecs=vp9,opus", extension: "webm" },
        { mimeType: "video/webm;codecs=vp8,opus", extension: "webm" },
        { mimeType: "video/webm", extension: "webm" }
    ];

    if (typeof MediaRecorder === "undefined") {
        throw new Error("media_recorder_not_supported");
    }

    for (const candidate of candidates) {
        try {
            if (!candidate.mimeType || MediaRecorder.isTypeSupported(candidate.mimeType)) {
                return candidate;
            }
        } catch (_) {}
    }

    return { mimeType: "", extension: "webm" };
}

function showSaveError(message) {
    payoff.classList.add("show");
    payoffLoader.innerText = message || "No hemos podido guardar este momento. Vuelve a intentarlo.";
    finishing = false;
    if (startBtn) {
        startBtn.disabled = false;
    }
}

async function stopRecorderSafely() {
    if (!mediaRecorder || mediaRecorder.state === "inactive") {
        return;
    }

    await new Promise((resolve) => {
        let resolved = false;

        const done = () => {
            if (resolved) return;
            resolved = true;
            mediaRecorder.removeEventListener("stop", onStop);
            clearTimeout(timeout);
            resolve();
        };

        const onStop = () => {
            done();
        };

        const timeout = setTimeout(done, 5000);

        mediaRecorder.addEventListener("stop", onStop);

        try {
            mediaRecorder.stop();
        } catch (_) {
            done();
        }
    });
}

async function uploadReactionBlob(blob) {
    const fileName = "reaction." + recordingExtension;
    const fileType = recordingMimeType || blob.type || "application/octet-stream";

    const formData = new FormData();
    formData.append("video", new File([blob], fileName, { type: fileType }));

    const response = await fetch("/upload-reaction/" + recipientToken, {
        method: "POST",
        body: formData
    });

    let data = {};
    try {
        data = await response.json();
    } catch (_) {}

    if (!response.ok) {
        throw new Error(data.detail || "upload_reaction_failed");
    }

    return data;
}

async function finalizeExperienceFlow() {
    if (finishing) return;
    finishing = true;

    payoff.classList.add("show");
    payoffLoader.innerText = "Guardando este momento…";

    try {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            try {
                mediaRecorder.requestData(); // 🔥 CLAVE
            } catch (_) {}

            await new Promise((resolve) => {
                let done = false;

                const finish = () => {
                    if (done) return;
                    done = true;
                    clearTimeout(timeout);
                    resolve();
                };

                const timeout = setTimeout(finish, 2000);

                mediaRecorder.addEventListener("dataavailable", finish, { once: true });

                try {
                    mediaRecorder.stop();
                } catch (_) {
                    finish();
                }
            });
        }
    } catch (e) {
        console.error("recorder stop error", e);
    }

    try {
        if (stream) {
            stream.getTracks().forEach((t) => t.stop());
        }
    } catch (e) {}

    try {
        const blob = new Blob(recordedChunks, {
            type: recordingMimeType || "video/webm"
        });

        console.log("chunks:", recordedChunks.length);
        console.log("blob size:", blob.size);

        if (!blob || blob.size <= 0) {
            throw new Error("empty_recording_blob");
        }

        const formData = new FormData();
        formData.append("video", blob, "reaction.webm");

        await fetch("/upload-reaction/" + recipientToken, {
            method: "POST",
            body: formData
        });

        // 🔥 IMPORTANTE: COBRO DIRECTO
        window.location.replace("/cobrar/" + recipientToken);

    } catch (e) {
        console.error("upload error", e);
        payoffLoader.innerText = "No hemos podido guardar este momento. Vuelve a intentarlo.";
        finishing = false;
        startBtn.disabled = false;
    }
}

function armFinishFallbacks() {
    video.addEventListener("ended", () => {
        finalizeExperienceFlow();
    }, { once: true });

    let fallbackMs = 120000;

    if (Number.isFinite(video.duration) && video.duration > 0) {
        fallbackMs = Math.max(15000, Math.floor(video.duration * 1000) + 2000);
    }

    finishTimeout = setTimeout(() => {
        finalizeExperienceFlow();
    }, fallbackMs);
}

startBtn.addEventListener("click", async () => {
    startBtn.disabled = true;

    try {
        const formData = new FormData();
        formData.append("recipient_token", recipientToken);

        const response = await fetch("/start-experience", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "start_experience_error");
        }

        if (data.redirect_url) {
            window.location.replace(data.redirect_url);
            return;
        }

        video.load();
        await waitForVideoReady();

        overlay.classList.remove("show");
        overlay.classList.add("hidden");
        experienceStarted = true;

        let recordingEnabled = false;

        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });

            const format = detectRecordingFormat();
            recordingMimeType = format.mimeType;
            recordingExtension = format.extension;
            recordedChunks = [];

            mediaRecorder = recordingMimeType
                ? new MediaRecorder(stream, { mimeType: recordingMimeType })
                : new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (e) => {
                if (e.data && e.data.size > 0) {
                    recordedChunks.push(e.data);
                }
            };

            mediaRecorder.onerror = (e) => {
                console.error("mediaRecorder error", e);
            };

            mediaRecorder.start(1000);
            recordingEnabled = true;
            console.log("🎥 grabación iniciada");
        } catch (recordingError) {
            console.error("recording init error", recordingError);
            stream = null;
            mediaRecorder = null;
            recordedChunks = [];
            recordingMimeType = "";
            recordingExtension = "webm";
        }

        armFinishFallbacks();
        await video.play();

        if (!recordingEnabled) {
            console.log("⚠️ experiencia iniciada sin grabación");
        }

    } catch (e) {
        console.error("experience start error", e);
        startBtn.disabled = false;
        alert("No hemos podido iniciar bien este momento.");
    }
});

document.addEventListener("visibilitychange", () => {
    if (!experienceStarted) return;
    if (document.visibilityState === "hidden") return;
});

window.addEventListener("pagehide", () => {
    if (!experienceStarted) return;
});

window.addEventListener("beforeunload", () => {
    if (!experienceStarted) return;
});
</script>
</body>
</html>
    """

    html_page = html_page.replace("__VIDEO_URL__", safe_attr(experience_video_url))
    html_page = html_page.replace("__VIDEO_TYPE__", safe_attr(guess_media_type_from_url(experience_video_url)))
    html_page = html_page.replace("__RECIPIENT_TOKEN__", safe_attr(recipient_token))
    html_page = html_page.replace("__PAYOFF_TITLE__", safe_text(payoff_title))
    html_page = html_page.replace("__PAYOFF_TEXT__", safe_text(payoff_text))
    html_page = html_page.replace("__COBRAR_TITLE__", safe_text(cobrar_title))
    html_page = html_page.replace("__COBRAR_TEXT__", safe_text(cobrar_text))

    return HTMLResponse(html_page)


# =========================================================
# UPLOAD REACTION (DEFINITIVO + SMS REGALANTE)
# =========================================================

@app.post("/upload-reaction/{recipient_token}")
async def upload_reaction(recipient_token: str, video: UploadFile = File(...)):
    order = get_order_by_recipient_token_or_404(recipient_token)

    print("🎥 UPLOAD REACTION START")
    print("➡️ order_id:", order["id"])

    if not bool(order.get("paid")):
        raise HTTPException(status_code=403, detail="not_paid")

    if not original_video_ready(order):
        raise HTTPException(status_code=403, detail="video_not_ready")

    content_type = (video.content_type or "").lower().strip()
    if content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=400, detail="invalid_video_type")

    data = await video.read()

    if len(data) > MAX_VIDEO_SIZE:
        raise HTTPException(status_code=400, detail="video_too_large")

    extension = detect_video_extension(video)
    local_path = reaction_video_path(order["id"], extension)

    try:
        with open(local_path, "wb") as f:
            f.write(data)

        print("💾 Guardado local:", local_path)

        public_url = None
        try:
            if r2_enabled():
                remote_name = f"reactions/{order['id']}.{extension}"
                public_url = upload_video_to_r2(
                    local_path,
                    remote_name,
                    content_type=content_type
                )
                print("☁️ Subido a R2:", public_url)
        except Exception as e:
            print("⚠️ Error subiendo a R2:", e)

        update_order(
            order["id"],
            reaction_video_local=local_path,
            reaction_video_public_url=public_url,
            reaction_uploaded=1,
            experience_completed=1,
            delivered_to_recipient=1,
            reaction_upload_pending=0,
            reaction_upload_error=None,
        )

        maybe_mark_eterna_completed(order["id"])

        def background_tasks():
            try:
                print("⚙️ BACKGROUND START:", order["id"])

                refreshed = get_order_by_id(order["id"])

                try:
                    process_gift_transfer_for_order(refreshed)
                except Exception as e:
                    log_error("process_gift_transfer_for_order", e)

                refreshed = get_order_by_id(order["id"])

                try:
                    sms_result = try_send_sender_sms(refreshed)
                    print("📩 SENDER SMS RESULT:", sms_result)
                except Exception as e:
                    log_error("try_send_sender_sms", e)

                maybe_mark_eterna_completed(order["id"])

                print("✅ BACKGROUND DONE:", order["id"])
            except Exception as e:
                log_error("BACKGROUND TASK ERROR", e)

        threading.Thread(target=background_tasks, daemon=True).start()

        return JSONResponse({
            "ok": True,
            "redirect": f"/cobrar/{recipient_token}"
        })

    except Exception as e:
        log_error("UPLOAD REACTION ERROR", e)
        raise HTTPException(status_code=500, detail="Error guardando reacción")

# =========================================================
# MI VIDEO (POST EXPERIENCIA)
# =========================================================

@app.get("/mi-video/{recipient_token}", response_class=HTMLResponse)
def mi_video(request: Request, recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not has_valid_recipient_session(order, request):
        return render_viral_block_page()

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not original_video_ready(order):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    video_url = (order.get("experience_video_url") or "").strip()

    if not video_url:
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ETERNA</title>

<style>
html, body {{
    margin: 0;
    padding: 0;
    background: black;
    color: white;
    font-family: Arial, sans-serif;
}}

.container {{
    width: 100%;
    max-width: 760px;
    margin: 0 auto;
    text-align: center;
    padding: 20px;
}}

video {{
    width: 100%;
    height: auto;
    background: black;
}}

h1 {{
    margin-top: 20px;
    font-size: 32px;
}}

.text {{
    margin-top: 16px;
    font-size: 18px;
    line-height: 1.7;
    color: rgba(255,255,255,0.8);
}}

.actions {{
    margin-top: 30px;
    display: grid;
    gap: 12px;
}}

.btn {{
    display: block;
    width: 100%;
    padding: 16px 22px;
    border-radius: 999px;
    font-weight: bold;
    text-decoration: none;
}}

.btn.primary {{
    background: white;
    color: black;
}}

.btn.secondary {{
    background: rgba(255,255,255,0.12);
    color: white;
}}
</style>
</head>

<body>

<div class="container">

    <video controls playsinline>
        <source src="{safe_attr(video_url)}" type="{safe_attr(guess_media_type_from_url(video_url))}">
    </video>

    <h1>Esto ya es tuyo</h1>

    <div class="text">
        Puedes volver a este momento siempre que quieras.<br><br>
        Y si sientes que alguien debería vivir algo así,<br>
        ahora puedes hacerlo.
    </div>

    <div class="actions">
        <a class="btn primary" href="/crear">Crear una ETERNA</a>
        <a class="btn secondary" href="/pedido/{safe_attr(recipient_token)}">Volver al inicio</a>
    </div>

</div>

</body>
</html>
    """)

# =========================================================
# COBRAR / CONNECT / SENDER PACK
# =========================================================

@app.get("/cobrar/{recipient_token}", response_class=HTMLResponse)
def cobrar(request: Request, recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not has_valid_recipient_session(order, request):
        return render_viral_block_page()

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not bool(order.get("experience_completed")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    gift_amount = float(order.get("gift_amount") or 0)
    cashout_status = compute_cashout_status(order)

    status_title = "Tu momento ya está completo"
    status_text = "Ya puedes volver a ver el vídeo cuando quieras."

    if gift_amount <= 0:
        cashout_line = "Este regalo no incluía dinero."
        primary_button_html = ""
    elif cashout_status == "completed":
        cashout_line = f"Tu regalo de {format_amount_display(gift_amount)} ya ha sido enviado."
        primary_button_html = ""
    elif cashout_status == "processing":
        cashout_line = f"Estamos procesando tu regalo de {format_amount_display(gift_amount)}."
        primary_button_html = ""
    else:
        cashout_line = f"Has recibido {format_amount_display(gift_amount)}."
        primary_button_html = f'''
            <a
                href="/recibir-regalo/{recipient_token}"
                style="display:inline-block;margin-top:18px;padding:16px 28px;border-radius:999px;background:white;color:black;text-decoration:none;font-weight:bold;"
            >
                Recibir mi regalo
            </a>
        '''

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ETERNA</title>
<style>
html, body {{
    margin: 0;
    min-height: 100%;
    background: #000;
}}
body {{
    min-height: 100vh;
    background:
        radial-gradient(circle at top, rgba(255,255,255,0.06), transparent 30%),
        linear-gradient(180deg, #050505 0%, #000000 100%);
    color: white;
    font-family: Arial, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 24px;
}}
.wrap {{
    width: 100%;
    max-width: 760px;
    margin: 0 auto;
}}
h1 {{
    margin: 0 0 18px 0;
    font-size: 42px;
    line-height: 1.2;
}}
.main {{
    font-size: 22px;
    line-height: 1.8;
    color: rgba(255,255,255,0.88);
}}
.soft {{
    margin-top: 24px;
    font-size: 16px;
    line-height: 1.8;
    color: rgba(255,255,255,0.50);
}}
.actions {{
    display: grid;
    gap: 12px;
    max-width: 420px;
    margin: 34px auto 0 auto;
}}
.btn {{
    display: block;
    width: 100%;
    padding: 17px 22px;
    border-radius: 999px;
    background: rgba(255,255,255,0.10);
    color: white;
    text-decoration: none;
    font-weight: bold;
    font-size: 15px;
    border: 1px solid rgba(255,255,255,0.10);
}}
</style>
</head>
<body>
    <div class="wrap">
        <h1>{safe_text(status_title)}</h1>
        <div class="main">{safe_text(status_text)}</div>
        <div class="soft">{safe_text(cashout_line)}</div>
        {primary_button_html}
        <div class="actions">
            <a class="btn" href="/mi-video/{safe_attr(recipient_token)}">Volver a ver el vídeo</a>
        </div>
    </div>
</body>
</html>
    """)


@app.get("/recibir-regalo/{recipient_token}", response_class=HTMLResponse)
def recibir_regalo(request: Request, recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not has_valid_recipient_session(order, request):
        return render_viral_block_page()

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not bool(order.get("experience_completed")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    gift_amount = float(order.get("gift_amount") or 0)
    if gift_amount <= 0:
        return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)

    cashout_status = compute_cashout_status(order)

    if cashout_status == "completed":
        return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)

    if cashout_status == "processing":
        return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)

    connect_url = None
    if not bool(order.get("connect_onboarding_completed")):
        try:
            connect_url = create_connect_onboarding_link(order)
        except Exception as e:
            log_error("create_connect_onboarding_link", e)
            connect_url = None

    if cashout_status == "ready_to_send":
        cta_html = f'''
            <form action="/connect/payout/{recipient_token}" method="post" style="margin-top:30px;">
                <button style="width:100%;max-width:420px;padding:18px 22px;border:none;border-radius:999px;background:white;color:black;font-weight:bold;font-size:16px;cursor:pointer;">
                    Recibir ahora
                </button>
            </form>
        '''
        helper_text = "Tu regalo ya está listo. Solo falta confirmarlo."
    else:
        if connect_url:
            cta_html = f'''
                <a
                    href="{safe_attr(connect_url)}"
                    style="display:inline-block;width:100%;max-width:420px;margin-top:30px;padding:18px 22px;border-radius:999px;background:white;color:black;text-decoration:none;font-weight:bold;font-size:16px;"
                >
                    Continuar
                </a>
            '''
        else:
            cta_html = ""
        helper_text = "Primero necesitamos unos datos básicos para poder enviártelo de forma segura."

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ETERNA</title>
<style>
html, body {{
    margin: 0;
    min-height: 100%;
    background: #000;
}}
body {{
    min-height: 100vh;
    background:
        radial-gradient(circle at top, rgba(255,255,255,0.06), transparent 30%),
        linear-gradient(180deg, #050505 0%, #000000 100%);
    color: white;
    font-family: Arial, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 24px;
}}
.wrap {{
    width: 100%;
    max-width: 760px;
    margin: 0 auto;
}}
h1 {{
    margin: 0 0 18px 0;
    font-size: 42px;
    line-height: 1.15;
}}
.main {{
    font-size: 22px;
    line-height: 1.8;
    color: rgba(255,255,255,0.90);
}}
.soft {{
    margin-top: 20px;
    font-size: 16px;
    line-height: 1.9;
    color: rgba(255,255,255,0.56);
}}
.amount {{
    margin-top: 28px;
    font-size: 18px;
    line-height: 1.8;
    color: rgba(255,255,255,0.76);
}}
.actions {{
    display: grid;
    gap: 12px;
    max-width: 420px;
    margin: 18px auto 0 auto;
}}
.btn {{
    display: block;
    width: 100%;
    padding: 17px 22px;
    border-radius: 999px;
    background: rgba(255,255,255,0.10);
    color: white;
    text-decoration: none;
    font-weight: bold;
    font-size: 15px;
    border: 1px solid rgba(255,255,255,0.10);
}}
</style>
</head>
<body>
    <div class="wrap">
        <h1>Esto también es para ti</h1>
        <div class="main">Has recibido {safe_text(format_amount_display(gift_amount))}.</div>
        <div class="soft">
            No tienes que hacerlo ahora.<br>
            Puedes recogerlo cuando quieras.
        </div>
        <div class="amount">{safe_text(helper_text)}</div>
        {cta_html}
        <div class="actions">
            <a class="btn" href="/cobrar/{safe_attr(recipient_token)}">Ahora no</a>
        </div>
    </div>
</body>
</html>
    """)


@app.get("/connect/refresh/{recipient_token}")
def connect_refresh(recipient_token: str):
    return RedirectResponse(url=f"/recibir-regalo/{recipient_token}", status_code=303)


@app.get("/connect/return/{recipient_token}")
def connect_return(recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    try:
        refresh_connect_status(order)
    except Exception as e:
        log_error("refresh_connect_status", e)

    refreshed = get_order_by_recipient_token_or_404(recipient_token)
    cashout_status = compute_cashout_status(refreshed)

    if cashout_status == "ready_to_send":
        return RedirectResponse(url=f"/recibir-regalo/{recipient_token}", status_code=303)

    return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)


@app.post("/connect/payout/{recipient_token}")
def connect_payout(request: Request, recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not has_valid_recipient_session(order, request):
        return render_viral_block_page()

    try:
        refresh_connect_status(order)
    except Exception as e:
        log_error("refresh_connect_status", e)

    refreshed = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(refreshed.get("connect_onboarding_completed")):
        return RedirectResponse(url=f"/recibir-regalo/{recipient_token}", status_code=303)

    try:
        process_gift_transfer_for_order(refreshed)
    except Exception as e:
        log_error("process_gift_transfer_for_order", e)

    return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)


@app.get("/sender/{sender_token}", response_class=HTMLResponse)
def sender_pack(sender_token: str):
    order = get_order_by_sender_token_or_404(sender_token)

    original_video_url = (order.get("experience_video_url") or "").strip()
    reaction_url = (order.get("reaction_video_public_url") or "").strip()

    if not reaction_url:
        local_path = (order.get("reaction_video_local") or "").strip()
        if local_path and os.path.exists(local_path):
            reaction_url = f"{PUBLIC_BASE_URL}/video/sender-reaction/{sender_token}"

    cashout_status = compute_cashout_status(order)

    sender_status = "Tu ETERNA aún se está cerrando."
    if bool(order.get("eterna_completed")):
        sender_status = "Tu ETERNA ha vuelto."

    cashout_line = ""
    if float(order.get("gift_amount") or 0) > 0:
        if cashout_status == "completed":
            cashout_line = "El regalo económico ya ha sido enviado."
        elif cashout_status == "processing":
            cashout_line = "El regalo económico se está procesando."
        elif cashout_status == "ready_to_send":
            cashout_line = "El regalo económico está listo para enviarse."
        else:
            cashout_line = "El regalo económico sigue pendiente de cobro."

    reaction_block = ""
    if reaction_url:
        reaction_block = f"""
        <div style="margin-top:28px;">
            <div style="margin-bottom:12px;color:rgba(255,255,255,0.62);font-size:15px;">Su reacción</div>
            <video controls playsinline style="width:100%;max-width:420px;background:black;border-radius:18px;">
                <source src="{safe_attr(reaction_url)}" type="{safe_attr(guess_media_type_from_url(reaction_url))}">
            </video>
        </div>
        """
    else:
        reaction_block = """
        <div style="margin-top:28px;color:rgba(255,255,255,0.52);line-height:1.8;">
            La reacción todavía no está lista.
        </div>
        """

    original_block = ""
    if original_video_url:
        original_block = f"""
        <div style="margin-top:28px;">
            <div style="margin-bottom:12px;color:rgba(255,255,255,0.62);font-size:15px;">El vídeo original</div>
            <video controls playsinline style="width:100%;max-width:420px;background:black;border-radius:18px;">
                <source src="{safe_attr(original_video_url)}" type="{safe_attr(guess_media_type_from_url(original_video_url))}">
            </video>
        </div>
        """

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ETERNA</title>
<style>
html, body {{
    margin: 0;
    min-height: 100%;
    background: #000;
}}
body {{
    min-height: 100vh;
    background:
        radial-gradient(circle at top, rgba(255,255,255,0.06), transparent 30%),
        linear-gradient(180deg, #050505 0%, #000000 100%);
    color: white;
    font-family: Arial, sans-serif;
    padding: 24px;
}}
.wrap {{
    width: 100%;
    max-width: 880px;
    margin: 0 auto;
    text-align: center;
}}
h1 {{
    margin: 0 0 18px 0;
    font-size: 42px;
    line-height: 1.2;
}}
.main {{
    font-size: 22px;
    line-height: 1.8;
    color: rgba(255,255,255,0.88);
}}
.soft {{
    margin-top: 20px;
    font-size: 16px;
    line-height: 1.8;
    color: rgba(255,255,255,0.52);
}}
</style>
</head>
<body>
    <div class="wrap">
        <h1>{safe_text(sender_status)}</h1>
        <div class="main">Aquí tienes el pack final.</div>
        <div class="soft">{safe_text(cashout_line)}</div>
        {original_block}
        {reaction_block}
    </div>
</body>
</html>
    """)


# =========================================================
# VIDEO / FILE ROUTES
# =========================================================

@app.get("/video/input/{order_id}/{slot_name}")
def get_video_input(order_id: str, slot_name: str):
    path = get_photo_asset_path(order_id, slot_name)
    if not path:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return FileResponse(
        path,
        media_type=guess_media_type_from_path(path),
        filename=os.path.basename(path),
    )


@app.get("/video/sender-reaction/{sender_token}")
def get_sender_reaction_video(sender_token: str):
    order = get_order_by_sender_token_or_404(sender_token)
    local_path = (order.get("reaction_video_local") or "").strip()

    if not local_path or not os.path.exists(local_path):
        raise HTTPException(status_code=404, detail="Vídeo no encontrado")

    return FileResponse(
        local_path,
        media_type=guess_media_type_from_path(local_path),
        filename=os.path.basename(local_path),
    )


# =========================================================
# OPTIONAL ADMIN
# =========================================================

@app.get("/admin/order/{order_id}")
def admin_order(order_id: str, token: str):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="unauthorized")

    order = maybe_mark_eterna_completed(order_id)
    assets = list_assets(order_id)

    return {
        "order": order,
        "assets": assets,
        "cashout_status": compute_cashout_status(order),
        "original_video_ready": original_video_ready(order),
        "reaction_exists": reaction_exists(order),
        "eterna_completed": bool(order.get("eterna_completed")),
        "scheduled_delivery_ready": scheduled_delivery_ready(order),
        "scheduled_delivery_display": scheduled_delivery_display(order),
        "delivery_locked": bool(order.get("delivery_locked")),
        "delivery_sent": bool(order.get("delivery_sent")),
        "delivery_sent_at": order.get("delivery_sent_at"),
    }


@app.get("/admin/process-scheduled-delivery/{order_id}")
def admin_process_scheduled_delivery(order_id: str, token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    result = process_scheduled_recipient_delivery(order_id)
    updated = get_order_by_id(order_id)

    return JSONResponse({
        "ok": result.get("ok", False),
        "result": result,
        "scheduled_delivery_at": updated.get("scheduled_delivery_at"),
        "scheduled_delivery_display": scheduled_delivery_display(updated),
        "delivery_sent": bool(updated.get("delivery_sent")),
        "delivery_sent_at": updated.get("delivery_sent_at"),
        "recipient_sms_sent_at": updated.get("recipient_sms_sent_at"),
    })


@app.post("/admin/retry-recipient-message/{order_id}")
def admin_retry_recipient_message(order_id: str, request: Request):
    admin_token = (request.query_params.get("token") or request.headers.get("x-admin-token") or "").strip()
    if not ADMIN_TOKEN or admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    order = get_order_by_id(order_id)
    attempts = int(order.get("recipient_sms_attempts") or 0)

    if bool(order.get("delivery_sent")) or bool(order.get("delivery_sent_at")):
        return {
            "ok": True,
            "reason": "already_sent",
            "order_id": order_id,
            "recipient_sms_sent_at": order.get("recipient_sms_sent_at"),
            "recipient_sms_attempts": attempts,
            "recipient_sms_error": order.get("recipient_sms_error"),
            "delivery_sent": bool(order.get("delivery_sent")),
            "delivery_sent_at": order.get("delivery_sent_at"),
        }

    if attempts >= 3:
        return {
            "ok": False,
            "reason": "max_attempts_reached",
            "order_id": order_id,
            "recipient_sms_sent_at": order.get("recipient_sms_sent_at"),
            "recipient_sms_attempts": attempts,
            "recipient_sms_error": order.get("recipient_sms_error"),
            "delivery_sent": bool(order.get("delivery_sent")),
            "delivery_sent_at": order.get("delivery_sent_at"),
        }

    result = process_scheduled_recipient_delivery(order_id)
    result["order_id"] = order_id
    return result


@app.get("/admin/retry-sender-message/{order_id}")
def admin_retry_sender_message(order_id: str, token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    order = maybe_mark_eterna_completed(order_id)
    result = try_send_sender_sms(order)
    updated = get_order_by_id(order_id)

    return JSONResponse({
        "ok": result.get("ok", False),
        "result": result,
        "sender_sms_sent_at": updated.get("sender_sms_sent_at"),
        "sender_sms_sid": updated.get("sender_sms_sid"),
        "sender_sms_attempts": updated.get("sender_sms_attempts"),
        "sender_sms_error": updated.get("sender_sms_error"),
        "eterna_completed": bool(updated.get("eterna_completed")),
    })


@app.get("/admin/delivery-worker-status")
def admin_delivery_worker_status(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    return JSONResponse({
        "delivery_worker_enabled": DELIVERY_WORKER_ENABLED,
        "delivery_worker_started": DELIVERY_WORKER_STARTED,
        "delivery_worker_interval_seconds": DELIVERY_WORKER_INTERVAL_SECONDS,
        "pending_order_ids": list_pending_scheduled_deliveries(),
        "pending_sender_notification_ids": list_pending_sender_notifications(),
    })


@app.get("/admin/process-all-due-deliveries")
def admin_process_all_due_deliveries(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    delivery_results = process_all_due_scheduled_deliveries()
    sender_results = process_all_due_sender_notifications()

    return JSONResponse({
        "ok": True,
        "delivery_count": len(delivery_results),
        "sender_count": len(sender_results),
        "delivery_results": delivery_results,
        "sender_results": sender_results,
    })

# =========================================================
# FINALIZAR EXPERIENCIA (DEFINITIVO)
# =========================================================

@app.get("/finalizar-experiencia/{recipient_token}")
def finalizar_experiencia(request: Request, recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    print("🏁 FINALIZANDO EXPERIENCE:", order["id"])

    if not has_valid_recipient_session(order, request):
        return render_viral_block_page()

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    try:
        update_order(
            order["id"],
            experience_completed=1,
            delivered_to_recipient=1,
            gift_refund_deadline_at=order.get("gift_refund_deadline_at") or gift_refund_deadline_iso(),
        )

        maybe_mark_eterna_completed(order["id"])

    except Exception as e:
        log_error("FINALIZAR EXPERIENCE ERROR", e)

    return RedirectResponse(
        url=f"/cobrar/{recipient_token}",
        status_code=303
    )

# =========================================================
# MAIN
# =========================================================

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port
    )