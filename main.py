print("🔥 ETERNA MAIN DEFINITIVO BLINDADO 🔥")
print("🔥 WEBHOOK + CALLBACK + EXPERIENCE LOCK + REACTION SAVE 🔥")
print("🔥 FINAL UX LOCKED + CASHOUT HARDENED + SENDER PACK READY 🔥")
print("🔥 REACTION RETRY + ETERNA COMPLETE SAFE VERSION 🔥")

import html
import json
import mimetypes
import os
import secrets
import sqlite3
import traceback
import uuid
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

        gift_refund_deadline_at TEXT,

        recipient_sms_sent_at TEXT,
        sender_sms_sent_at TEXT,
        recipient_sms_sid TEXT,
        sender_sms_sid TEXT,

        recipient_sms_attempts INTEGER NOT NULL DEFAULT 0,
        sender_sms_attempts INTEGER NOT NULL DEFAULT 0,
        recipient_sms_error TEXT,
        sender_sms_error TEXT,

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

    add_column_if_missing("orders", "message_type", "ALTER TABLE orders ADD COLUMN message_type TEXT")
    add_column_if_missing("orders", "phrase_mode", "ALTER TABLE orders ADD COLUMN phrase_mode TEXT NOT NULL DEFAULT 'auto'")
    add_column_if_missing("orders", "experience_video_url", "ALTER TABLE orders ADD COLUMN experience_video_url TEXT")
    add_column_if_missing("orders", "reaction_video_public_url", "ALTER TABLE orders ADD COLUMN reaction_video_public_url TEXT")
    add_column_if_missing("orders", "reaction_video_local", "ALTER TABLE orders ADD COLUMN reaction_video_local TEXT")
    add_column_if_missing("orders", "stripe_session_id", "ALTER TABLE orders ADD COLUMN stripe_session_id TEXT")
    add_column_if_missing("orders", "stripe_payment_status", "ALTER TABLE orders ADD COLUMN stripe_payment_status TEXT")
    add_column_if_missing("orders", "stripe_payment_intent_id", "ALTER TABLE orders ADD COLUMN stripe_payment_intent_id TEXT")
    add_column_if_missing("orders", "stripe_connected_account_id", "ALTER TABLE orders ADD COLUMN stripe_connected_account_id TEXT")
    add_column_if_missing("orders", "stripe_transfer_id", "ALTER TABLE orders ADD COLUMN stripe_transfer_id TEXT")
    add_column_if_missing("orders", "gift_refund_deadline_at", "ALTER TABLE orders ADD COLUMN gift_refund_deadline_at TEXT")
    add_column_if_missing("orders", "gift_refunded", "ALTER TABLE orders ADD COLUMN gift_refunded INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "stripe_gift_refund_id", "ALTER TABLE orders ADD COLUMN stripe_gift_refund_id TEXT")
    add_column_if_missing("orders", "recipient_sms_sent_at", "ALTER TABLE orders ADD COLUMN recipient_sms_sent_at TEXT")
    add_column_if_missing("orders", "sender_sms_sent_at", "ALTER TABLE orders ADD COLUMN sender_sms_sent_at TEXT")
    add_column_if_missing("orders", "recipient_sms_sid", "ALTER TABLE orders ADD COLUMN recipient_sms_sid TEXT")
    add_column_if_missing("orders", "sender_sms_sid", "ALTER TABLE orders ADD COLUMN sender_sms_sid TEXT")
    add_column_if_missing("orders", "recipient_sms_attempts", "ALTER TABLE orders ADD COLUMN recipient_sms_attempts INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "sender_sms_attempts", "ALTER TABLE orders ADD COLUMN sender_sms_attempts INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "recipient_sms_error", "ALTER TABLE orders ADD COLUMN recipient_sms_error TEXT")
    add_column_if_missing("orders", "sender_sms_error", "ALTER TABLE orders ADD COLUMN sender_sms_error TEXT")

    add_column_if_missing(
        "orders",
        "reaction_upload_pending",
        "ALTER TABLE orders ADD COLUMN reaction_upload_pending INTEGER NOT NULL DEFAULT 0",
    )
    add_column_if_missing(
        "orders",
        "reaction_upload_error",
        "ALTER TABLE orders ADD COLUMN reaction_upload_error TEXT",
    )
    add_column_if_missing(
        "orders",
        "eterna_completed",
        "ALTER TABLE orders ADD COLUMN eterna_completed INTEGER NOT NULL DEFAULT 0",
    )


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
    return bool((order.get("experience_video_url") or "").strip())


def reaction_exists(order: dict) -> bool:
    if order.get("reaction_video_public_url"):
        return True
    local_path = (order.get("reaction_video_local") or "").strip()
    return bool(local_path) and os.path.exists(local_path)


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
        f"{sender_pack_url_from_order(order)}"
    )


def calculate_fees(gift_amount: float) -> dict:
    gift_amount = max(0.0, round(float(gift_amount or 0), 2))
    fixed_fee = round(FIXED_PLATFORM_FEE, 2)
    variable_fee = round(gift_amount * GIFT_COMMISSION_RATE, 2)
    total_fee = round(fixed_fee + variable_fee, 2)
    total_amount = round(BASE_PRICE + gift_amount + total_fee, 2)
    return {
        "gift_amount": gift_amount,
        "fixed_fee": fixed_fee,
        "variable_fee": variable_fee,
        "total_fee": total_fee,
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


def try_send_recipient_sms(order: dict) -> dict:
    if order.get("recipient_sms_sent_at"):
        return {
            "ok": True,
            "sid": order.get("recipient_sms_sid"),
            "already_sent": True,
            "error": None,
        }

    if not bool(order.get("paid")):
        return {"ok": False, "sid": None, "already_sent": False, "error": "order_not_paid"}

    if not original_video_ready(order):
        return {"ok": False, "sid": None, "already_sent": False, "error": "original_video_not_ready"}

    attempts = int(order.get("recipient_sms_attempts") or 0) + 1
    result = send_sms(order.get("recipient_phone", ""), build_recipient_message(order))

    if result["ok"]:
        update_order(
            order["id"],
            recipient_sms_sent_at=now_iso(),
            recipient_sms_sid=result["sid"],
            recipient_sms_attempts=attempts,
            recipient_sms_error=None,
        )
        return {"ok": True, "sid": result["sid"], "already_sent": False, "error": None}

    update_order(
        order["id"],
        recipient_sms_attempts=attempts,
        recipient_sms_error=result["error"],
    )
    return {"ok": False, "sid": None, "already_sent": False, "error": result["error"]}


def try_send_sender_sms(order: dict) -> dict:
    order = get_order_by_id(order["id"])

    if not is_eterna_complete(order):
        return {
            "ok": False,
            "sid": None,
            "already_sent": False,
            "error": "eterna_not_complete",
        }

    if order.get("sender_sms_sent_at"):
        return {
            "ok": True,
            "sid": order.get("sender_sms_sid"),
            "already_sent": True,
            "error": None,
        }

    attempts = int(order.get("sender_sms_attempts") or 0) + 1
    result = send_sms(order.get("sender_phone", ""), build_sender_ready_message(order))

    if result["ok"]:
        update_order(
            order["id"],
            sender_sms_sent_at=now_iso(),
            sender_sms_sid=result["sid"],
            sender_sms_attempts=attempts,
            sender_sms_error=None,
            sender_notified=1,
        )
        return {"ok": True, "sid": result["sid"], "already_sent": False, "error": None}

    update_order(
        order["id"],
        sender_sms_attempts=attempts,
        sender_sms_error=result["error"],
    )
    return {"ok": False, "sid": None, "already_sent": False, "error": result["error"]}


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

    update_order(
        order_id,
        experience_started=1,
        delivered_to_recipient=1,
    )
    return "started"


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
body {{
    margin: 0;
    background: black;
    color: white;
    font-family: Arial;
    padding: 20px;
}}

.wrap {{ max-width: 700px; margin: auto; }}

input {{
    width: 100%;
    padding: 14px;
    margin: 8px 0;
    border-radius: 12px;
    border: 1px solid #333;
    background: #111;
    color: white;
}}

.photo-box {{
    border: 1px dashed #555;
    border-radius: 14px;
    padding: 10px;
    text-align: center;
    position: relative;
}}

.photo-box img {{
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: none;
    border-radius: 10px;
}}

button {{
    width: 100%;
    padding: 16px;
    border-radius: 999px;
    border: none;
    background: white;
    color: black;
    font-weight: bold;
    margin-top: 20px;
}}

.status {{
    font-size: 12px;
    opacity: 0.6;
}}
</style>
</head>

<body>
<div class="wrap">

<h2>Crear ETERNA</h2>

<form id="form">

<input name="customer_name" placeholder="Tu nombre" required>
<input name="customer_phone" placeholder="Tu teléfono" required>

<input name="recipient_name" placeholder="Nombre destinatario" required>
<input name="recipient_phone" placeholder="Teléfono destinatario" required>

<h3>Fotos</h3>

{''.join([f'''
<div class="photo-box">
    <img id="preview{i}">
    <input type="file" id="photo{i}" accept="image/*" capture="environment" required>
    <div class="status" id="status{i}">Añadir foto</div>
</div>
''' for i in range(1,7)])}

<h3>Frases</h3>
<input name="phrase_1" placeholder="Frase 1">
<input name="phrase_2" placeholder="Frase 2">
<input name="phrase_3" placeholder="Frase 3">

<input name="gift_amount" type="number" value="0">

<button id="submitBtn">CONTINUAR</button>

</form>
</div>

<script>

// ===============================
// COMPRESIÓN IMAGEN (CLAVE)
// ===============================
async function compressImage(file) {{
    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);

    await new Promise(r => img.onload = r);

    const canvas = document.createElement("canvas");
    const maxWidth = 1200;

    const scale = maxWidth / img.width;
    canvas.width = maxWidth;
    canvas.height = img.height * scale;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

    return new Promise(resolve => {{
        canvas.toBlob(blob => {{
            resolve(new File([blob], file.name, {{
                type: "image/jpeg"
            }}));
        }}, "image/jpeg", 0.8);
    }});
}}

// ===============================
// PREVIEW + ESTADO
// ===============================
for (let i = 1; i <= 6; i++) {{
    const input = document.getElementById("photo" + i);
    const preview = document.getElementById("preview" + i);
    const status = document.getElementById("status" + i);

    input.addEventListener("change", () => {{
        const file = input.files[0];
        if (!file) return;

        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";

        status.innerText = "✔ lista";
    }});
}}

// ===============================
// SUBMIT ROBUSTO
// ===============================
document.getElementById("form").addEventListener("submit", async (e) => {{
    e.preventDefault();

    const btn = document.getElementById("submitBtn");
    btn.disabled = true;
    btn.innerText = "Preparando fotos...";

    try {{

        const formData = new FormData();

        // inputs normales
        const inputs = e.target.querySelectorAll("input[name]");
        inputs.forEach(i => {{
            if (i.type !== "file") {{
                formData.append(i.name, i.value);
            }}
        }});

        // fotos comprimidas
        for (let i = 1; i <= 6; i++) {{
            const input = document.getElementById("photo" + i);

            if (!input.files[0]) {{
                alert("Faltan fotos");
                btn.disabled = false;
                return;
            }}

            document.getElementById("status"+i).innerText = "Procesando...";

            const compressed = await compressImage(input.files[0]);

            document.getElementById("status"+i).innerText = "✔ optimizada";

            formData.append("photo"+i, compressed);
        }}

        btn.innerText = "Subiendo...";

        const res = await fetch("/crear", {{
            method: "POST",
            body: formData
        }});

        if (res.redirected) {{
            window.location.href = res.url;
        }} else {{
            const text = await res.text();
            document.body.innerHTML = text;
        }}

    }} catch (err) {{
        console.error(err);
        alert("Error subiendo. Intenta otra vez.");
        btn.disabled = false;
        btn.innerText = "CONTINUAR";
    }}

}});
</script>

</body>
</html>
"""
    


async def create_order_and_redirect(
    customer_name: str,
    customer_email: str,
    customer_phone: str,
    recipient_name: str,
    recipient_phone: str,
    message_type: str,
    phrase_mode: str,
    phrase_1: str,
    phrase_2: str,
    phrase_3: str,
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
    recipient_name = (recipient_name or "").strip()
    message_type = (message_type or "").strip()
    phrase_mode = (phrase_mode or "auto").strip()

    phrase_1 = (phrase_1 or "").strip()
    phrase_2 = (phrase_2 or "").strip()
    phrase_3 = (phrase_3 or "").strip()

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

    try:
        gift_amount = round(float(gift_amount or 0), 2)
    except Exception:
        raise HTTPException(status_code=400, detail="Importe no válido")

    if gift_amount < 0:
        raise HTTPException(status_code=400, detail="Importe no válido")

    sender_phone = normalize_phone(customer_phone)
    recipient_phone_norm = normalize_phone(recipient_phone)

    if not sender_phone or not recipient_phone_norm:
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

    fees = calculate_fees(gift_amount)
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

    placeholders = ", ".join(["?"] * 49)

    cur.execute(f"""
        INSERT INTO orders (
            id, sender_id, recipient_id,
            message_type, phrase_mode,
            phrase_1, phrase_2, phrase_3,
            gift_amount, platform_fixed_fee, platform_variable_fee, platform_total_fee, total_amount,
            paid, delivered_to_recipient, reaction_uploaded,
            cashout_completed, transfer_completed, transfer_in_progress, sender_notified,
            experience_started, experience_completed,
            connect_onboarding_completed, gift_refunded,
            stripe_session_id, stripe_payment_status, stripe_payment_intent_id, stripe_connected_account_id, stripe_transfer_id, stripe_gift_refund_id,
            recipient_token, sender_token,
            reaction_video_local, reaction_video_public_url, experience_video_url,
            gift_refund_deadline_at,
            recipient_sms_sent_at, sender_sms_sent_at, recipient_sms_sid, sender_sms_sid,
            recipient_sms_attempts, sender_sms_attempts, recipient_sms_error, sender_sms_error,
            reaction_upload_pending, reaction_upload_error, eterna_completed,
            created_at, updated_at
        )
        VALUES ({placeholders})
    """, (
        order_id, sender_id, recipient_id,
        message_type, phrase_mode,
        phrase_1, phrase_2, phrase_3,
        fees["gift_amount"], fees["fixed_fee"], fees["variable_fee"], fees["total_fee"], fees["total_amount"],
        0, 0, 0,
        0, 0, 0, 0,
        0, 0,
        0, 0,
        None, None, None, None, None, None,
        recipient_token, sender_token,
        None, None, None,
        None,
        None, None, None, None,
        0, 0, None, None,
        0, None, 0,
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
        )

        try:
            trigger_video_engine(order_id, [phrase_1, phrase_2, phrase_3])
            print("⏳ Render aceptado por el video engine. Esperando callback.")
        except Exception as e:
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
                                f"comisión {money(fees['total_fee'])}€"
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
    customer_phone: str = Form(...),
    recipient_name: str = Form(...),
    recipient_phone: str = Form(...),
    message_type: str = Form(...),
    phrase_mode: str = Form("auto"),
    phrase_1: str = Form(""),
    phrase_2: str = Form(""),
    phrase_3: str = Form(""),
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
        customer_phone=customer_phone,
        recipient_name=recipient_name,
        recipient_phone=recipient_phone,
        message_type=message_type,
        phrase_mode=phrase_mode,
        phrase_1=phrase_1,
        phrase_2=phrase_2,
        phrase_3=phrase_3,
        gift_amount=gift_amount,
        photo1=photo1,
        photo2=photo2,
        photo3=photo3,
        photo4=photo4,
        photo5=photo5,
        photo6=photo6,
    )


# =========================================================
# RECIPIENT ENTRY
# =========================================================

@app.get("/pedido/{recipient_token}", response_class=HTMLResponse)
def pedido(recipient_token: str):
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
    elif bool(order.get("experience_completed")):
        return RedirectResponse(url=f"/mi-video/{recipient_token}", status_code=303)
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

    return HTMLResponse(f"""
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


# =========================================================
# CHECKOUT / WEBHOOK / CALLBACK
# =========================================================

@app.get("/checkout-exito/{order_id}", response_class=HTMLResponse)
def checkout_exito(order_id: str):
    order = get_order_by_id(order_id)
    is_paid = bool(order["paid"])

    refresh = '<meta http-equiv="refresh" content="6">' if not is_paid else ""
    redirect_script = f"""
        setTimeout(function() {{
            window.location.href = "/post-pago/{safe_attr(order_id)}";
        }}, 5000);
    """ if is_paid else ""

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        {refresh}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ETERNA</title>
    </head>
    <body style="margin:0;min-height:100vh;background:#000;color:white;font-family:Arial;display:flex;align-items:center;justify-content:center;text-align:center;padding:24px;">
        <div style="max-width:680px;">
            <h1 style="font-size:42px;margin-bottom:18px;">Todo ya está en camino</h1>
            <div style="font-size:20px;line-height:1.8;color:rgba(255,255,255,0.85);">
                En unos instantes,<br>
                alguien va a vivir algo que no espera
            </div>
        </div>
        <script>{redirect_script}</script>
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
        )

        order = get_order_by_id(order_id)

        phrases = [
            (order.get("phrase_1") or "").strip(),
            (order.get("phrase_2") or "").strip(),
            (order.get("phrase_3") or "").strip(),
        ]

        try:
            data = trigger_video_engine(order_id, phrases)
            print("✅ Video engine aceptó el trabajo:", data)
        except Exception as e:
            log_error("webhook_video_engine", e)
            raise HTTPException(status_code=500, detail=f"video_engine_error: {e}")

        return {"status": "ok"}

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

        if not existing_video:
            update_order(order_id, experience_video_url=video_url)

        if not asset_exists(order_id, "rendered_video", video_url):
            insert_asset(
                order_id=order_id,
                asset_type="rendered_video",
                file_url=video_url,
                storage_provider="video_engine",
            )

            update_order(order_id, experience_video_url=video_url)

        updated_order = maybe_mark_eterna_completed(order_id)

        print("📲 CALLBACK -> intentando SMS recipient")
        print("📲 paid:", updated_order.get("paid"))
        print("📲 experience_video_url:", updated_order.get("experience_video_url"))
        print("📲 recipient_phone raw:", updated_order.get("recipient_phone"))
        print("📲 recipient_phone e164:", to_e164(updated_order.get("recipient_phone", "")))
        print("📲 twilio_enabled:", twilio_enabled())

        try:
            sms_result = try_send_recipient_sms(updated_order)
            print("📩 Resultado SMS callback:", sms_result)
        except Exception as e:
            log_error("recipient_sms_after_callback", e)

        return JSONResponse({
            "status": "ok",
            "order_id": order_id,
            "video_url": video_url,
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
    sms_sent = bool(order.get("recipient_sms_sent_at"))
    video_ready = original_video_ready(order)

    if sms_sent:
        status_line = "Tu ETERNA ya ha salido"
        sub_line = f"{recipient_name} ya tiene su mensaje."
        soft_line = "Ahora el momento ya está en marcha."
    elif video_ready:
        status_line = "Tu ETERNA está lista"
        sub_line = f"Estamos enviando el mensaje a {recipient_name}."
        soft_line = "El aviso solo sale cuando el vídeo ya existe de verdad."
    else:
        status_line = "Pago confirmado"
        sub_line = "La fábrica de ETERNA ya está haciendo magia."
        soft_line = "Estamos preparando este momento. Cuando esté listo y salga, todo seguirá su curso."

    refresh = '<meta http-equiv="refresh" content="8">' if not sms_sent else ""

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
        <div style="max-width:720px;width:100%;">
            <h1 style="font-size:42px;line-height:1.2;margin:0 0 22px 0;font-weight:700;">
                {status_line}
            </h1>

            <div style="font-size:22px;line-height:1.8;color:rgba(255,255,255,0.86);">
                {sub_line}
            </div>

            <div style="margin-top:28px;font-size:16px;line-height:1.7;color:rgba(255,255,255,0.45);">
                {soft_line}
            </div>
        </div>
    </body>
    </html>
    """)


# =========================================================
# EXPERIENCE LOCK
# =========================================================

@app.post("/start-experience")
def start_experience(recipient_token: str = Form(...)):
    order = get_order_by_recipient_token_or_404(recipient_token)
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
            "redirect_url": f"/mi-video/{recipient_token}",
        })

    return JSONResponse({"status": "ok"})


@app.post("/finalizar-experiencia/{recipient_token}")
def finalizar_experiencia(recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(order.get("paid")):
        raise HTTPException(status_code=403, detail="Pedido no pagado")

    if not bool(order.get("experience_started")):
        raise HTTPException(status_code=403, detail="La experiencia no ha empezado")

    if not original_video_ready(order):
        raise HTTPException(status_code=403, detail="Vídeo original no disponible")

    update_order(
        order["id"],
        experience_completed=1,
        delivered_to_recipient=1,
        gift_refund_deadline_at=order.get("gift_refund_deadline_at") or gift_refund_deadline_iso(),
    )

    return JSONResponse({
        "status": "ok",
        "cashout_url": f"{PUBLIC_BASE_URL}/cobrar/{recipient_token}?force_cashout=1",
    })


@app.get("/reaction-upload-status/{recipient_token}")
def reaction_upload_status(recipient_token: str):
    order = maybe_mark_eterna_completed(get_order_by_recipient_token_or_404(recipient_token)["id"])
    return JSONResponse({
        "status": "ok",
        "reaction_uploaded": bool(order.get("reaction_uploaded")),
        "reaction_exists": reaction_exists(order),
        "reaction_upload_pending": bool(order.get("reaction_upload_pending")),
        "reaction_upload_error": order.get("reaction_upload_error"),
        "eterna_completed": bool(order.get("eterna_completed")),
        "experience_completed": bool(order.get("experience_completed")),
    })


# =========================================================
# EXPERIENCE
# =========================================================

@app.get("/experiencia/{recipient_token}", response_class=HTMLResponse)
def experiencia(recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not original_video_ready(order):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if bool(order.get("experience_completed")):
        return RedirectResponse(url=f"/mi-video/{recipient_token}", status_code=303)

    experience_video_url = (order.get("experience_video_url") or "").strip()

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>ETERNA</title>
<style>
html, body {{
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: black;
    overflow: hidden;
    font-family: Arial, sans-serif;
}}
body {{
    position: fixed;
    inset: 0;
}}
.container {{
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    background: black;
    overflow: hidden;
}}
video {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    background: black;
    pointer-events: none;
}}
.overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(0,0,0,0.30) 0%, rgba(0,0,0,0.72) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
    padding: 24px;
    z-index: 3;
}}
.title {{
    font-size: 34px;
    line-height: 1.2;
    margin-bottom: 18px;
    color: white;
}}
.soft {{
    max-width: 560px;
    font-size: 16px;
    line-height: 1.7;
    color: rgba(255,255,255,0.76);
}}
.btn {{
    margin-top: 28px;
    padding: 16px 28px;
    border: none;
    border-radius: 999px;
    font-size: 16px;
    font-weight: bold;
    background: white;
    color: black;
    cursor: pointer;
}}
.hidden {{
    display: none;
}}
.blackout {{
    position: absolute;
    inset: 0;
    background: black;
    opacity: 0;
    pointer-events: none;
    z-index: 4;
    transition: opacity 0.25s ease;
}}
.blackout.show {{
    opacity: 1;
}}
.final-overlay {{
    position: absolute;
    inset: 0;
    background: black;
    display: none;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
    padding: 24px;
    z-index: 6;
}}
.final-overlay.show {{
    display: flex;
}}
.final-title {{
    font-size: 30px;
    line-height: 1.25;
    color: white;
    margin-bottom: 14px;
}}
.final-soft {{
    font-size: 16px;
    line-height: 1.7;
    color: rgba(255,255,255,0.68);
    max-width: 560px;
}}
</style>
</head>
<body>
<div class="container" id="experienceContainer">
    <video
        id="video"
        playsinline
        preload="auto"
        webkit-playsinline
        disablepictureinpicture
        controlslist="nodownload noplaybackrate noremoteplayback nofullscreen"
    >
        <source src="{safe_attr(experience_video_url)}" type="{safe_attr(guess_media_type_from_url(experience_video_url))}">
    </video>

    <div class="overlay" id="overlay">
        <div class="title">Hay algo para ti</div>
        <div class="soft">
            Cuando pulses empezar, se abrirá la experiencia completa
            y comenzará la grabación de tu reacción.
        </div>
        <button id="startBtn" class="btn">Empezar</button>
    </div>

    <div class="blackout" id="blackout"></div>

    <div class="final-overlay" id="finalOverlay">
        <div class="final-title">Un instante…</div>
        <div class="final-soft">
            Estamos cerrando este momento.
        </div>
    </div>
</div>

<script>
const video = document.getElementById("video");
const overlay = document.getElementById("overlay");
const startBtn = document.getElementById("startBtn");
const blackout = document.getElementById("blackout");
const finalOverlay = document.getElementById("finalOverlay");

const recipientToken = "{safe_attr(recipient_token)}";

let mediaRecorder = null;
let recordedChunks = [];
let stream = null;
let finished = false;

function cashoutUrl() {{
    return "/cobrar/" + recipientToken + "?force_cashout=1";
}}

function safeRedirectToCashout() {{
    if (finished) return;
    finished = true;
    window.location.replace(cashoutUrl());
}}

async function markExperienceFinished() {{
    try {{
        await fetch("/finalizar-experiencia/" + recipientToken, {{
            method: "POST"
        }});
    }} catch (e) {{
        console.error("finalizar-experiencia error", e);
    }}
}}

function openReactionDB() {{
    return new Promise((resolve, reject) => {{
        const request = indexedDB.open("eternaReactionDB", 1);
        request.onupgradeneeded = function(event) {{
            const db = event.target.result;
            if (!db.objectStoreNames.contains("reactions")) {{
                db.createObjectStore("reactions");
            }}
        }};
        request.onsuccess = function() {{
            resolve(request.result);
        }};
        request.onerror = function() {{
            reject(request.error || new Error("indexeddb_open_error"));
        }};
    }});
}}

async function savePendingReaction(blob) {{
    const db = await openReactionDB();
    await new Promise((resolve, reject) => {{
        const tx = db.transaction("reactions", "readwrite");
        tx.objectStore("reactions").put(blob, recipientToken);
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error || new Error("indexeddb_put_error"));
    }});
    db.close();
}}

async function loadPendingReaction() {{
    const db = await openReactionDB();
    const blob = await new Promise((resolve, reject) => {{
        const tx = db.transaction("reactions", "readonly");
        const req = tx.objectStore("reactions").get(recipientToken);
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => reject(req.error || new Error("indexeddb_get_error"));
    }});
    db.close();
    return blob;
}}

async function deletePendingReaction() {{
    const db = await openReactionDB();
    await new Promise((resolve, reject) => {{
        const tx = db.transaction("reactions", "readwrite");
        tx.objectStore("reactions").delete(recipientToken);
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error || new Error("indexeddb_delete_error"));
    }});
    db.close();
}}

async function fetchReactionStatus() {{
    try {{
        const res = await fetch("/reaction-upload-status/" + recipientToken, {{
            cache: "no-store"
        }});
        if (!res.ok) return null;
        return await res.json();
    }} catch (e) {{
        console.error("reaction status error", e);
        return null;
    }}
}}

async function uploadReactionBlob(blob) {{
    const formData = new FormData();
    formData.append("file", blob, "reaction.webm");

    const res = await fetch("/upload-reaction/" + recipientToken, {{
        method: "POST",
        body: formData
    }});

    let data = null;
    try {{
        data = await res.json();
    }} catch (_) {{
        data = null;
    }}

    if (!res.ok) {{
        throw new Error((data && data.detail) || "upload_reaction_error");
    }}

    return data;
}}

async function retryReactionUpload(maxAttempts = 8) {{
    const existingStatus = await fetchReactionStatus();
    if (existingStatus && existingStatus.reaction_uploaded && existingStatus.reaction_exists) {{
        await deletePendingReaction().catch(() => null);
        return true;
    }}

    const blob = await loadPendingReaction();
    if (!blob || !blob.size) {{
        return false;
    }}

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {{
        try {{
            await uploadReactionBlob(blob);
            const status = await fetchReactionStatus();
            if (status && status.reaction_uploaded && status.reaction_exists) {{
                await deletePendingReaction().catch(() => null);
                return true;
            }}
        }} catch (e) {{
            console.error("retryReactionUpload attempt error", attempt, e);
        }}

        await new Promise(resolve => setTimeout(resolve, 1200 * attempt));
    }}

    return false;
}}

async function stopRecorderSafely() {{
    try {{
        if (mediaRecorder && mediaRecorder.state !== "inactive") {{
            await new Promise((resolve) => {{
                const timeout = setTimeout(resolve, 3000);

                const oldOnStop = mediaRecorder.onstop;
                mediaRecorder.onstop = function(event) {{
                    clearTimeout(timeout);
                    if (typeof oldOnStop === "function") {{
                        try {{
                            oldOnStop.call(mediaRecorder, event);
                        }} catch (_) {{}}
                    }}
                    resolve();
                }};

                try {{
                    mediaRecorder.stop();
                }} catch (_) {{
                    clearTimeout(timeout);
                    resolve();
                }}
            }});
        }}
    }} catch (e) {{
        console.error("stopRecorderSafely error", e);
    }}

    try {{
        if (stream) {{
            stream.getTracks().forEach(t => t.stop());
        }}
    }} catch (e) {{
        console.error("stream stop error", e);
    }}
}}

async function finishExperience() {{
    blackout.classList.add("show");
    finalOverlay.classList.add("show");

    try {{
        video.pause();
    }} catch (e) {{
        console.error(e);
    }}

    await stopRecorderSafely();

    const blob = new Blob(recordedChunks, {{ type: "video/webm" }});

    if (blob && blob.size > 0) {{
        try {{
            await savePendingReaction(blob);
        }} catch (e) {{
            console.error("savePendingReaction error", e);
        }}
    }}

    setTimeout(() => {{
        safeRedirectToCashout();
    }}, 350);

    setTimeout(() => {{
        markExperienceFinished();
    }}, 450);

    setTimeout(() => {{
        retryReactionUpload().catch((e) => console.error("retryReactionUpload error", e));
    }}, 600);
}}

startBtn.addEventListener("click", async () => {{
    startBtn.disabled = true;

    try {{
        const formData = new FormData();
        formData.append("recipient_token", recipientToken);

        const response = await fetch("/start-experience", {{
            method: "POST",
            body: formData
        }});

        const data = await response.json();

        if (!response.ok) {{
            throw new Error(data.detail || "start_experience_error");
        }}

        if (data.status === "already_completed" && data.redirect_url) {{
            window.location.replace(data.redirect_url);
            return;
        }}

        if (data.status === "video_not_ready" && data.redirect_url) {{
            window.location.replace(data.redirect_url);
            return;
        }}

        stream = await navigator.mediaDevices.getUserMedia({{
            video: true,
            audio: true
        }});

        mediaRecorder = new MediaRecorder(stream);
        recordedChunks = [];

        mediaRecorder.ondataavailable = (e) => {{
            if (e.data && e.data.size > 0) {{
                recordedChunks.push(e.data);
            }}
        }};

        mediaRecorder.start(250);
        overlay.classList.add("hidden");
        await video.play();

    }} catch (e) {{
        console.error(e);
        startBtn.disabled = false;
    }}
}});

video.addEventListener("ended", finishExperience);
</script>
</body>
</html>
""")

# =========================================================
# UPLOAD REACTION VIDEO
# =========================================================

@app.post("/upload-reaction/{recipient_token}")
async def upload_reaction(recipient_token: str, file: UploadFile = File(...)):
    try:
        order = get_order_by_recipient_token_or_404(recipient_token)

        if not bool(order.get("paid")):
            raise HTTPException(status_code=403, detail="Pedido no pagado")

        if not bool(order.get("experience_started")):
            raise HTTPException(status_code=403, detail="La experiencia no ha empezado")

        if not original_video_ready(order):
            raise HTTPException(status_code=403, detail="Vídeo original no disponible")

        if bool(order.get("reaction_uploaded")) and reaction_exists(order):
            updated_order = maybe_mark_eterna_completed(order["id"])
            return JSONResponse({
                "status": "already_uploaded",
                "cashout_url": f"{PUBLIC_BASE_URL}/cobrar/{order['recipient_token']}?force_cashout=1",
                "eterna_completed": bool(updated_order.get("eterna_completed")),
            })

        update_order(
            order["id"],
            reaction_upload_pending=1,
            reaction_upload_error=None,
        )

        ext = Path(file.filename or "reaction.webm").suffix.lower() or ".webm"
        if ext not in {".webm", ".mp4"}:
            ext = ".webm"

        content_type = (file.content_type or "").lower().strip()
        if content_type and content_type not in ALLOWED_VIDEO_TYPES:
            update_order(
                order["id"],
                reaction_upload_pending=0,
                reaction_upload_error="Formato de vídeo no permitido",
                eterna_completed=0,
            )
            raise HTTPException(status_code=400, detail="Formato de vídeo no permitido")

        extension = ext.replace(".", "")
        save_path = reaction_video_path(order["id"], extension)

        total_size = 0
        with open(save_path, "wb") as f:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break

                total_size += len(chunk)
                if total_size > MAX_VIDEO_SIZE:
                    try:
                        f.close()
                    except Exception:
                        pass
                    if os.path.exists(save_path):
                        os.remove(save_path)

                    update_order(
                        order["id"],
                        reaction_upload_pending=0,
                        reaction_upload_error="Vídeo demasiado grande",
                        eterna_completed=0,
                    )
                    raise HTTPException(status_code=400, detail="Vídeo demasiado grande")

                f.write(chunk)

        if not os.path.exists(save_path) or os.path.getsize(save_path) == 0:
            update_order(
                order["id"],
                reaction_upload_pending=0,
                reaction_upload_error="Archivo vacío",
                eterna_completed=0,
            )
            raise HTTPException(status_code=400, detail="Archivo vacío")

        public_url = None
        final_content_type = "video/mp4" if extension == "mp4" else "video/webm"

        try:
            public_url = upload_video_to_r2(
                save_path,
                os.path.basename(save_path),
                final_content_type,
            )
        except Exception as e:
            log_error("upload_reaction_r2", e)

        if not public_url:
            public_url = f"{PUBLIC_BASE_URL}/video/sender/{order['sender_token']}"

        update_order(
            order["id"],
            reaction_video_local=save_path,
            reaction_video_public_url=public_url,
            reaction_uploaded=1,
            reaction_upload_pending=0,
            reaction_upload_error=None,
            experience_completed=1,
            delivered_to_recipient=1,
            gift_refund_deadline_at=order.get("gift_refund_deadline_at") or gift_refund_deadline_iso(),
        )

        if not asset_exists(order["id"], "reaction_video", public_url):
            insert_asset(
                order["id"],
                "reaction_video",
                public_url,
                "r2" if R2_PUBLIC_URL and public_url.startswith(R2_PUBLIC_URL) else "local",
            )

        updated_order = maybe_mark_eterna_completed(order["id"])

        try:
            sender_sms_result = try_send_sender_sms(updated_order)
            print("📩 Resultado SMS sender:", sender_sms_result)
        except Exception as e:
            log_error("upload_reaction_sender_sms", e)

        return JSONResponse({
            "status": "ok",
            "url": public_url,
            "cashout_url": f"{PUBLIC_BASE_URL}/cobrar/{recipient_token}?force_cashout=1",
            "reaction_uploaded": bool(updated_order.get("reaction_uploaded")),
            "reaction_exists": reaction_exists(updated_order),
            "eterna_completed": bool(updated_order.get("eterna_completed")),
        })

    except HTTPException:
        raise
    except Exception as e:
        log_error("upload_reaction", e)
        try:
            order = get_order_by_recipient_token_or_404(recipient_token)
            update_order(
                order["id"],
                reaction_upload_pending=0,
                reaction_upload_error=str(e),
                eterna_completed=0,
            )
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            await file.close()
        except Exception:
            pass


# =========================================================
# CASHOUT / CONNECT
# =========================================================

def maybe_finalize_cashout(order: dict) -> dict:
    order = get_order_by_id(order["id"])

    gift_amount = float(order.get("gift_amount") or 0)

    if gift_amount <= 0:
        update_order(
            order["id"],
            connect_onboarding_completed=1,
            transfer_completed=1,
            cashout_completed=1,
            transfer_in_progress=0,
        )
        return {"status": "completed"}

    if bool(order.get("cashout_completed")) or bool(order.get("transfer_completed")):
        return {"status": "completed"}

    if bool(order.get("transfer_in_progress")):
        return {"status": "processing"}

    if bool(order.get("connect_onboarding_completed")):
        result = process_gift_transfer_for_order(order)
        normalized_status = result.get("status")

        if normalized_status in {"ok", "already_transferred", "no_gift", "stripe_disabled_test_mode"}:
            return {"status": "completed", "transfer_result": result}

        if normalized_status == "transfer_in_progress":
            return {"status": "processing", "transfer_result": result}

        if normalized_status == "onboarding_not_ready":
            return {"status": "pending_onboarding", "transfer_result": result}

        return {"status": normalized_status or "pending_onboarding", "transfer_result": result}

    return {"status": "pending_onboarding"}


@app.get("/cobrar/{recipient_token}", response_class=HTMLResponse)
def cobrar(recipient_token: str, force_cashout: int = 0):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not bool(order.get("experience_started")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if int(force_cashout or 0) == 1 and not bool(order.get("experience_completed")):
        update_order(
            order["id"],
            experience_completed=1,
            delivered_to_recipient=1,
            gift_refund_deadline_at=order.get("gift_refund_deadline_at") or gift_refund_deadline_iso(),
        )
        order = get_order_by_id(order["id"])

    cashout_result = maybe_finalize_cashout(order)
    order = maybe_mark_eterna_completed(order["id"])

    if not bool(order.get("experience_completed")):
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="refresh" content="4">
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
                h1 {{
                    margin: 0 0 18px 0;
                    font-size: 42px;
                    line-height: 1.2;
                }}
                .soft {{
                    font-size: 18px;
                    line-height: 1.8;
                    color: rgba(255,255,255,0.62);
                }}
            </style>
        </head>
        <body>
            <div class="wrap">
                <h1>Un instante…</h1>
                <div class="soft">
                    Estamos cerrando este momento.
                </div>
            </div>
        </body>
        </html>
        """)

    cashout_status = compute_cashout_status(order)
    maybe_status = (cashout_result or {}).get("status")

    if maybe_status == "processing":
        cashout_status = "processing"
    elif maybe_status == "completed":
        cashout_status = "completed"
    elif maybe_status == "pending_onboarding" and cashout_status not in {"completed", "processing"}:
        cashout_status = "pending"

    gift_amount_display = format_amount_display(order.get("gift_amount") or 0)
    original_video_url = safe_attr(order.get("experience_video_url") or "")
    gift_amount_value = float(order.get("gift_amount") or 0)

    reaction_uploaded = bool(order.get("reaction_uploaded"))
    reaction_ok = reaction_exists(order)
    reaction_pending = bool(order.get("reaction_upload_pending"))
    reaction_error = safe_text(order.get("reaction_upload_error") or "")
    eterna_completed = bool(order.get("eterna_completed"))

    if eterna_completed:
        eterna_state_title = "ETERNA está completa"
        eterna_state_text = "Tu vídeo y tu emoción han quedado guardados correctamente."
    elif reaction_pending:
        eterna_state_title = "Estamos guardando tu emoción"
        eterna_state_text = "Tu ETERNA aún no está completa. El sistema seguirá intentando guardar la reacción."
    elif reaction_uploaded and not reaction_ok:
        eterna_state_title = "Estamos recuperando tu emoción"
        eterna_state_text = "La reacción figura subida, pero aún no está disponible correctamente. Seguiremos insistiendo."
    elif reaction_error:
        eterna_state_title = "La emoción sigue pendiente"
        eterna_state_text = "Tu ETERNA todavía no está completa. Seguiremos intentando guardar la reacción."
    else:
        eterna_state_title = "Tu emoción sigue en proceso"
        eterna_state_text = "Hasta que la reacción quede guardada bien, ETERNA no se considera completa."

    retry_note = ""
    if reaction_error:
        retry_note = f"""
        <div class="alert">
            Último estado de reacción: {reaction_error}
        </div>
        """

    if gift_amount_value <= 0:
        title = "Todo ha quedado guardado"
        subtitle = "Este momento ya forma parte de ETERNA."
        action_html = f'''
            <a class="btn" href="/mi-video/{safe_attr(recipient_token)}">Ver mi vídeo</a>
        '''
        share_html = f'''
            <button class="btn ghost" onclick="navigator.share ? navigator.share({{title:'ETERNA', url:window.location.origin + '/mi-video/{safe_attr(recipient_token)}'}}) : alert('Comparte este enlace desde tu navegador: ' + window.location.origin + '/mi-video/{safe_attr(recipient_token)}')">Compartir</button>
        '''
    else:
        if cashout_status == "completed":
            title = "Tu regalo ya está en camino"
            subtitle = f"Importe: {gift_amount_display}"
            action_html = f'''
                <a class="btn" href="/mi-video/{safe_attr(recipient_token)}">Ver mi vídeo</a>
            '''
        elif cashout_status == "processing":
            title = "Estamos enviando tu regalo"
            subtitle = f"Importe: {gift_amount_display}"
            action_html = f'''
                <a class="btn" href="/mi-video/{safe_attr(recipient_token)}">Ver mi vídeo</a>
            '''
        else:
            title = "Tu regalo te espera"
            subtitle = f"Puedes recibir {gift_amount_display}"
            action_html = f'''
                <a class="btn" href="/connect/onboarding/{safe_attr(recipient_token)}">Cobrar ahora</a>
            '''

        share_html = f'''
            <button class="btn ghost" onclick="navigator.share ? navigator.share({{title:'ETERNA', url:window.location.origin + '/mi-video/{safe_attr(recipient_token)}'}}) : alert('Comparte este enlace desde tu navegador: ' + window.location.origin + '/mi-video/{safe_attr(recipient_token)}')">Compartir</button>
        '''

    original_block = ""
    if original_video_url:
        original_block = f"""
        <div class="video-card">
            <div class="video-title">Tu ETERNA</div>
            <video controls playsinline preload="metadata" src="{original_video_url}"></video>
        </div>
        """

    refresh = '<meta http-equiv="refresh" content="6">' if not eterna_completed or cashout_status in {"pending", "processing", "ready_to_send"} else ""

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        {refresh}
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
                padding: 24px;
            }}
            .wrap {{ width: 100%; max-width: 860px; margin: 0 auto; }}
            .hero {{
                text-align: center;
                margin-bottom: 28px;
            }}
            h1 {{
                font-size: 42px;
                line-height: 1.2;
                margin: 0 0 16px 0;
            }}
            .sub {{
                font-size: 20px;
                line-height: 1.7;
                color: rgba(255,255,255,0.82);
            }}
            .status-card {{
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 24px;
                padding: 18px;
                margin: 0 auto 24px auto;
            }}
            .status-title {{
                font-size: 18px;
                line-height: 1.5;
                color: white;
                margin-bottom: 8px;
            }}
            .status-text {{
                font-size: 15px;
                line-height: 1.8;
                color: rgba(255,255,255,0.68);
            }}
            .alert {{
                margin-top: 12px;
                padding: 12px 14px;
                border-radius: 16px;
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.10);
                color: rgba(255,255,255,0.74);
                font-size: 14px;
                line-height: 1.6;
            }}
            .actions {{
                display: grid;
                gap: 12px;
                margin: 30px auto 26px auto;
                max-width: 420px;
            }}
            .btn {{
                display: block;
                width: 100%;
                padding: 17px 22px;
                border-radius: 999px;
                border: 0;
                text-decoration: none;
                text-align: center;
                font-weight: bold;
                font-size: 15px;
                background: white;
                color: black;
                cursor: pointer;
            }}
            .btn.ghost {{
                background: rgba(255,255,255,0.10);
                color: white;
                border: 1px solid rgba(255,255,255,0.12);
            }}
            .grid {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 20px;
                margin-top: 26px;
            }}
            .video-card {{
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 24px;
                padding: 18px;
            }}
            .video-title {{
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1.3px;
                color: rgba(255,255,255,0.46);
                margin-bottom: 12px;
            }}
            video {{
                width: 100%;
                border-radius: 18px;
                background: black;
            }}
            .soft {{
                margin-top: 20px;
                text-align: center;
                font-size: 14px;
                line-height: 1.7;
                color: rgba(255,255,255,0.42);
            }}
        </style>
    </head>
    <body>
        <div class="wrap">
            <div class="hero">
                <h1>{safe_text(title)}</h1>
                <div class="sub">{safe_text(subtitle)}</div>
            </div>

            <div class="status-card">
                <div class="status-title">{safe_text(eterna_state_title)}</div>
                <div class="status-text">{safe_text(eterna_state_text)}</div>
                {retry_note}
            </div>

            <div class="actions">
                {action_html}
                <a class="btn ghost" href="/mi-video/{safe_attr(recipient_token)}">Volver a verlo</a>
                {share_html}
            </div>

            <div class="grid">
                {original_block}
            </div>

            <div class="soft">
                Lo importante ya pasó.<br>
                ETERNA solo queda completa cuando existen el vídeo y la emoción.
            </div>
        </div>

<script>
const recipientToken = "{safe_attr(recipient_token)}";

function openReactionDB() {{
    return new Promise((resolve, reject) => {{
        const request = indexedDB.open("eternaReactionDB", 1);
        request.onupgradeneeded = function(event) {{
            const db = event.target.result;
            if (!db.objectStoreNames.contains("reactions")) {{
                db.createObjectStore("reactions");
            }}
        }};
        request.onsuccess = function() {{
            resolve(request.result);
        }};
        request.onerror = function() {{
            reject(request.error || new Error("indexeddb_open_error"));
        }};
    }});
}}

async function loadPendingReaction() {{
    const db = await openReactionDB();
    const blob = await new Promise((resolve, reject) => {{
        const tx = db.transaction("reactions", "readonly");
        const req = tx.objectStore("reactions").get(recipientToken);
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => reject(req.error || new Error("indexeddb_get_error"));
    }});
    db.close();
    return blob;
}}

async function deletePendingReaction() {{
    const db = await openReactionDB();
    await new Promise((resolve, reject) => {{
        const tx = db.transaction("reactions", "readwrite");
        tx.objectStore("reactions").delete(recipientToken);
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error || new Error("indexeddb_delete_error"));
    }});
    db.close();
}}

async function fetchReactionStatus() {{
    try {{
        const res = await fetch("/reaction-upload-status/" + recipientToken, {{
            cache: "no-store"
        }});
        if (!res.ok) return null;
        return await res.json();
    }} catch (e) {{
        console.error("reaction status error", e);
        return null;
    }}
}}

async function uploadReactionBlob(blob) {{
    const formData = new FormData();
    formData.append("file", blob, "reaction.webm");

    const res = await fetch("/upload-reaction/" + recipientToken, {{
        method: "POST",
        body: formData
    }});

    let data = null;
    try {{
        data = await res.json();
    }} catch (_) {{
        data = null;
    }}

    if (!res.ok) {{
        throw new Error((data && data.detail) || "upload_reaction_error");
    }}

    return data;
}}

async function retryReactionUpload(maxAttempts = 8) {{
    const existingStatus = await fetchReactionStatus();
    if (existingStatus && existingStatus.reaction_uploaded && existingStatus.reaction_exists) {{
        await deletePendingReaction().catch(() => null);
        return true;
    }}

    const blob = await loadPendingReaction();
    if (!blob || !blob.size) {{
        return false;
    }}

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {{
        try {{
            await uploadReactionBlob(blob);
            const status = await fetchReactionStatus();
            if (status && status.reaction_uploaded && status.reaction_exists) {{
                await deletePendingReaction().catch(() => null);
                return true;
            }}
        }} catch (e) {{
            console.error("retryReactionUpload attempt error", attempt, e);
        }}

        await new Promise(resolve => setTimeout(resolve, 1200 * attempt));
    }}

    return false;
}}

window.addEventListener("load", () => {{
    retryReactionUpload().catch((e) => console.error("retryReactionUpload load error", e));
}});

document.addEventListener("visibilitychange", () => {{
    if (document.visibilityState === "visible") {{
        retryReactionUpload().catch((e) => console.error("retryReactionUpload visible error", e));
    }}
}});
</script>
    </body>
    </html>
    """)

@app.get("/connect/onboarding/{recipient_token}")
def connect_onboarding(recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    cashout_result = maybe_finalize_cashout(order)
    order = maybe_mark_eterna_completed(order["id"])

    if not bool(order.get("experience_completed")):
        return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)

    if float(order.get("gift_amount") or 0) <= 0:
        update_order(
            order["id"],
            connect_onboarding_completed=1,
            transfer_completed=1,
            cashout_completed=1,
            transfer_in_progress=0,
        )
        return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)

    if (cashout_result or {}).get("status") == "completed":
        return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)

    try:
        url = create_connect_onboarding_link(order)
        return RedirectResponse(url=url, status_code=303)
    except Exception as e:
        log_error("connect_onboarding", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/connect/refresh/{recipient_token}")
def connect_refresh(recipient_token: str):
    return RedirectResponse(url=f"/connect/onboarding/{recipient_token}", status_code=303)


@app.get("/connect/return/{recipient_token}")
def connect_return(recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    try:
        ready = refresh_connect_status(order)
        order = get_order_by_id(order["id"])

        if ready:
            process_gift_transfer_for_order(order)

    except Exception as e:
        log_error("connect_return", e)

    return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)


# =========================================================
# FINAL PAGES
# =========================================================

@app.get("/mi-video/{recipient_token}", response_class=HTMLResponse)
def mi_video(recipient_token: str):
    order = maybe_mark_eterna_completed(get_order_by_recipient_token_or_404(recipient_token)["id"])

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not original_video_ready(order):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    original_video_url = safe_attr(order.get("experience_video_url") or "")
    cashout_status = compute_cashout_status(order)
    cashout_cta = "Cobrar regalo" if cashout_status not in {"completed", "processing"} else "Ver regalo"

    eterna_completed = bool(order.get("eterna_completed"))
    reaction_pending = bool(order.get("reaction_upload_pending"))
    reaction_error = safe_text(order.get("reaction_upload_error") or "")

    reaction_state = ""
    if eterna_completed:
        reaction_state = """
        <div class="info-box">
            ETERNA está completa: vídeo y emoción guardados correctamente.
        </div>
        """
    elif reaction_pending:
        reaction_state = """
        <div class="info-box">
            La emoción sigue guardándose. ETERNA todavía no está completa.
        </div>
        """
    elif reaction_error:
        reaction_state = f"""
        <div class="info-box">
            La emoción sigue pendiente. Último estado: {reaction_error}
        </div>
        """
    else:
        reaction_state = """
        <div class="info-box">
            La emoción aún no está lista. ETERNA no está completa todavía.
        </div>
        """

    refresh = '<meta http-equiv="refresh" content="6">' if not eterna_completed else ""

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        {refresh}
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
                padding: 24px;
            }}
            .wrap {{ width: 100%; max-width: 860px; margin: 0 auto; }}
            h1 {{
                text-align: center;
                font-size: 42px;
                margin: 0 0 26px 0;
            }}
            .info-box {{
                max-width: 720px;
                margin: 0 auto 22px auto;
                padding: 16px 18px;
                border-radius: 20px;
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.08);
                color: rgba(255,255,255,0.72);
                line-height: 1.7;
                text-align: center;
                font-size: 15px;
            }}
            .grid {{
                display: grid;
                gap: 22px;
            }}
            .card {{
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 24px;
                padding: 18px;
            }}
            .card-title {{
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1.3px;
                color: rgba(255,255,255,0.46);
                margin-bottom: 12px;
            }}
            video {{
                width: 100%;
                border-radius: 18px;
                background: black;
            }}
            .actions {{
                display: grid;
                gap: 12px;
                max-width: 420px;
                margin: 28px auto 0 auto;
            }}
            .btn {{
                display: block;
                width: 100%;
                padding: 17px 22px;
                border-radius: 999px;
                border: 0;
                text-decoration: none;
                text-align: center;
                font-weight: bold;
                font-size: 15px;
                background: white;
                color: black;
            }}
            .btn.ghost {{
                background: rgba(255,255,255,0.10);
                color: white;
                border: 1px solid rgba(255,255,255,0.12);
            }}
        </style>
    </head>
    <body>
        <div class="wrap">
            <h1>Tu momento</h1>

            {reaction_state}

            <div class="grid">
                <div class="card">
                    <div class="card-title">Tu ETERNA</div>
                    <video controls playsinline preload="metadata" src="{original_video_url}"></video>
                </div>
            </div>

            <div class="actions">
                <a class="btn" href="/cobrar/{safe_attr(recipient_token)}">{safe_text(cashout_cta)}</a>
                <button class="btn ghost" onclick="navigator.share ? navigator.share({{title:'ETERNA', url:window.location.href}}) : alert(window.location.href)">Compartir</button>
            </div>
        </div>

<script>
const recipientToken = "{safe_attr(recipient_token)}";

function openReactionDB() {{
    return new Promise((resolve, reject) => {{
        const request = indexedDB.open("eternaReactionDB", 1);
        request.onupgradeneeded = function(event) {{
            const db = event.target.result;
            if (!db.objectStoreNames.contains("reactions")) {{
                db.createObjectStore("reactions");
            }}
        }};
        request.onsuccess = function() {{
            resolve(request.result);
        }};
        request.onerror = function() {{
            reject(request.error || new Error("indexeddb_open_error"));
        }};
    }});
}}

async function loadPendingReaction() {{
    const db = await openReactionDB();
    const blob = await new Promise((resolve, reject) => {{
        const tx = db.transaction("reactions", "readonly");
        const req = tx.objectStore("reactions").get(recipientToken);
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => reject(req.error || new Error("indexeddb_get_error"));
    }});
    db.close();
    return blob;
}}

async function deletePendingReaction() {{
    const db = await openReactionDB();
    await new Promise((resolve, reject) => {{
        const tx = db.transaction("reactions", "readwrite");
        tx.objectStore("reactions").delete(recipientToken);
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error || new Error("indexeddb_delete_error"));
    }});
    db.close();
}}

async function fetchReactionStatus() {{
    try {{
        const res = await fetch("/reaction-upload-status/" + recipientToken, {{
            cache: "no-store"
        }});
        if (!res.ok) return null;
        return await res.json();
    }} catch (e) {{
        console.error("reaction status error", e);
        return null;
    }}
}}

async function uploadReactionBlob(blob) {{
    const formData = new FormData();
    formData.append("file", blob, "reaction.webm");

    const res = await fetch("/upload-reaction/" + recipientToken, {{
        method: "POST",
        body: formData
    }});

    let data = null;
    try {{
        data = await res.json();
    }} catch (_) {{
        data = null;
    }}

    if (!res.ok) {{
        throw new Error((data && data.detail) || "upload_reaction_error");
    }}

    return data;
}}

async function retryReactionUpload(maxAttempts = 8) {{
    const existingStatus = await fetchReactionStatus();
    if (existingStatus && existingStatus.reaction_uploaded && existingStatus.reaction_exists) {{
        await deletePendingReaction().catch(() => null);
        return true;
    }}

    const blob = await loadPendingReaction();
    if (!blob || !blob.size) {{
        return false;
    }}

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {{
        try {{
            await uploadReactionBlob(blob);
            const status = await fetchReactionStatus();
            if (status && status.reaction_uploaded && status.reaction_exists) {{
                await deletePendingReaction().catch(() => null);
                return true;
            }}
        }} catch (e) {{
            console.error("retryReactionUpload attempt error", attempt, e);
        }}

        await new Promise(resolve => setTimeout(resolve, 1200 * attempt));
    }}

    return false;
}}

window.addEventListener("load", () => {{
    retryReactionUpload().catch((e) => console.error("retryReactionUpload load error", e));
}});

document.addEventListener("visibilitychange", () => {{
    if (document.visibilityState === "visible") {{
        retryReactionUpload().catch((e) => console.error("retryReactionUpload visible error", e));
    }}
}});
</script>
    </body>
    </html>
    """)


@app.get("/sender/{sender_token}", response_class=HTMLResponse)
def sender_pack(sender_token: str):
    order = maybe_mark_eterna_completed(get_order_by_sender_token_or_404(sender_token)["id"])

    if not bool(order.get("paid")):
        raise HTTPException(status_code=403, detail="Pedido no pagado")

    original_video_url = safe_attr(order.get("experience_video_url") or "")
    reaction_url = safe_attr(order.get("reaction_video_public_url") or "")
    recipient_name = safe_text(order.get("recipient_name") or "esa persona")
    gift_amount = format_amount_display(order.get("gift_amount") or 0)
    eterna_completed = bool(order.get("eterna_completed"))
    reaction_pending = bool(order.get("reaction_upload_pending"))
    reaction_error = safe_text(order.get("reaction_upload_error") or "")

    state_html = ""
    if eterna_completed:
        state_html = """
        <div class="state-box">
            ETERNA completa: el vídeo y la emoción ya están guardados.
        </div>
        """
    elif reaction_pending:
        state_html = """
        <div class="state-box">
            La emoción sigue guardándose. El sender pack todavía no está completo del todo.
        </div>
        """
    elif reaction_error:
        state_html = f"""
        <div class="state-box">
            La emoción sigue pendiente. Último estado: {reaction_error}
        </div>
        """
    else:
        state_html = """
        <div class="state-box">
            La emoción aún no está lista. Este sender pack todavía no está completo.
        </div>
        """

    reaction_block = ""
    if reaction_url:
        reaction_block = f"""
        <div class="card">
            <div class="card-title">Su emoción</div>
            <video controls playsinline preload="metadata" src="{reaction_url}"></video>
        </div>
        """

    refresh = '<meta http-equiv="refresh" content="6">' if not eterna_completed else ""

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        {refresh}
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
                padding: 24px;
            }}
            .wrap {{ width: 100%; max-width: 920px; margin: 0 auto; }}
            .hero {{
                text-align: center;
                margin-bottom: 26px;
            }}
            h1 {{
                font-size: 42px;
                margin: 0 0 14px 0;
            }}
            .sub {{
                font-size: 20px;
                line-height: 1.7;
                color: rgba(255,255,255,0.82);
            }}
            .state-box {{
                max-width: 760px;
                margin: 0 auto 24px auto;
                padding: 16px 18px;
                border-radius: 20px;
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.08);
                color: rgba(255,255,255,0.72);
                line-height: 1.7;
                text-align: center;
                font-size: 15px;
            }}
            .grid {{
                display: grid;
                gap: 22px;
            }}
            .card {{
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 24px;
                padding: 18px;
            }}
            .card-title {{
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1.3px;
                color: rgba(255,255,255,0.46);
                margin-bottom: 12px;
            }}
            video {{
                width: 100%;
                border-radius: 18px;
                background: black;
            }}
            .meta {{
                margin-top: 24px;
                text-align: center;
                color: rgba(255,255,255,0.46);
                line-height: 1.8;
                font-size: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="wrap">
            <div class="hero">
                <h1>Tu ETERNA ha vuelto</h1>
                <div class="sub">
                    {recipient_name} ya ha vivido su momento.<br>
                    Regalo: {gift_amount}
                </div>
            </div>

            {state_html}

            <div class="grid">
                <div class="card">
                    <div class="card-title">El vídeo que enviaste</div>
                    <video controls playsinline preload="metadata" src="{original_video_url}"></video>
                </div>
                {reaction_block}
            </div>

            <div class="meta">
                ETERNA solo está completa cuando existen las dos partes:<br>
                el vídeo original y la emoción guardada.
            </div>
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


@app.get("/video/sender/{sender_token}")
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
    }


@app.get("/admin/retry-recipient-message/{order_id}")
def admin_retry_recipient_message(order_id: str, token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    order = get_order_by_id(order_id)
    result = try_send_recipient_sms(order)
    updated = get_order_by_id(order_id)

    return JSONResponse({
        "ok": result.get("ok", False),
        "result": result,
        "recipient_sms_sent_at": updated.get("recipient_sms_sent_at"),
        "recipient_sms_sid": updated.get("recipient_sms_sid"),
        "recipient_sms_attempts": updated.get("recipient_sms_attempts"),
        "recipient_sms_error": updated.get("recipient_sms_error"),
    })


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


# =========================================================
# MAIN
# =========================================================

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )