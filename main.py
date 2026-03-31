import html
import mimetypes
import os
import secrets
import sqlite3
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import stripe
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

try:
    from twilio.rest import Client as TwilioClient
except ImportError:
    TwilioClient = None


app = FastAPI(title="ETERNA MAIN")


# =========================================================
# CONFIG
# =========================================================

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "").strip()
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "").strip()

PUBLIC_BASE_URL = os.getenv(
    "PUBLIC_BASE_URL",
    "https://eterna-final.onrender.com",
).strip().rstrip("/")

ETERNA_BASE_PRICE = float(os.getenv("ETERNA_BASE_PRICE", "29"))
ETERNA_CURRENCY = os.getenv("ETERNA_CURRENCY", "eur").strip().lower()
GIFT_COMMISSION_RATE = float(os.getenv("GIFT_COMMISSION_RATE", "0.05"))

DEFAULT_EXPERIENCE_VIDEO_URL = os.getenv(
    "DEFAULT_EXPERIENCE_VIDEO_URL",
    "",
).strip()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
TWILIO_FROM_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "").strip()

MAX_VIDEO_SIZE = 30 * 1024 * 1024
ALLOWED_VIDEO_TYPES = {
    "video/webm",
    "video/mp4",
    "application/octet-stream",
}

BASE_DIR = Path(".")
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = BASE_DIR / "uploads"
VIDEOS_DIR = BASE_DIR / "videos"
STATIC_DIR = BASE_DIR / "static"

DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "eterna.db"

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# =========================================================
# LOG
# =========================================================

def log_info(message: str):
    print(f"[INFO] {message}")


def log_error(message: str, error: Exception | None = None):
    if error is None:
        print(f"[ERROR] {message}")
    else:
        print(f"[ERROR] {message}: {error}")


# =========================================================
# DB
# =========================================================

def db_conn():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_db():
    conn = db_conn()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS senders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS recipients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
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
            gift_commission REAL NOT NULL DEFAULT 0,
            total_amount REAL NOT NULL DEFAULT 0,

            paid INTEGER NOT NULL DEFAULT 0,
            delivered_to_recipient INTEGER NOT NULL DEFAULT 0,
            experience_started INTEGER NOT NULL DEFAULT 0,
            experience_completed INTEGER NOT NULL DEFAULT 0,
            reaction_uploaded INTEGER NOT NULL DEFAULT 0,
            sender_notified INTEGER NOT NULL DEFAULT 0,

            stripe_session_id TEXT,
            stripe_payment_status TEXT,
            stripe_payment_intent_id TEXT,

            recipient_token TEXT NOT NULL UNIQUE,
            sender_token TEXT NOT NULL UNIQUE,

            reaction_video_local TEXT,
            reaction_video_public_url TEXT,
            experience_video_url TEXT,

            recipient_sms_sent_at TEXT,
            sender_sms_sent_at TEXT,
            recipient_sms_sid TEXT,
            sender_sms_sid TEXT,
            recipient_sms_error TEXT,
            sender_sms_error TEXT,

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,

            FOREIGN KEY(sender_id) REFERENCES senders(id),
            FOREIGN KEY(recipient_id) REFERENCES recipients(id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            file_url TEXT NOT NULL,
            storage_provider TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
        """
    )

    conn.commit()
    conn.close()


init_db()


# =========================================================
# HELPERS
# =========================================================

def now_dt() -> datetime:
    return datetime.now(timezone.utc)


def now_iso() -> str:
    return now_dt().isoformat()


def safe_text(value: str) -> str:
    return html.escape(str(value or "").strip())


def safe_attr(value: str) -> str:
    return html.escape(str(value or "").strip(), quote=True)


def money(value: float) -> str:
    return f"{float(value):.2f}"


def format_amount_display(value: float) -> str:
    return f"{float(value):.2f} €".replace(".", ",")


def normalize_phone(phone: str) -> str:
    raw = str(phone or "").strip()
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


def calculate_totals(gift_amount: float) -> dict:
    gift_amount = max(0.0, round(float(gift_amount or 0), 2))
    commission = round(gift_amount * GIFT_COMMISSION_RATE, 2)
    total_amount = round(ETERNA_BASE_PRICE + gift_amount + commission, 2)
    return {
        "gift_amount": gift_amount,
        "gift_commission": commission,
        "total_amount": total_amount,
    }


def get_phrases_by_type(message_type: str):
    templates = {
        "cumpleanos": [
            "Hoy no es un día cualquiera.",
            "Es tu historia celebrándose.",
            "Y lo mejor aún está por venir.",
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
            "Y vale más de lo que imaginas.",
        ],
        "sorpresa": [
            "Pensabas que hoy era un día normal…",
            "Pero alguien ha estado pensando en ti.",
            "Mucho más de lo que imaginas.",
        ],
    }
    return templates.get(message_type, templates["sorpresa"])


def detect_image_extension(upload: UploadFile) -> str:
    filename = (upload.filename or "").lower().strip()
    content_type = (upload.content_type or "").lower().strip()
    if filename.endswith(".png") or content_type == "image/png":
        return "png"
    if filename.endswith(".webp") or content_type == "image/webp":
        return "webp"
    return "jpg"


def detect_video_extension(upload: UploadFile) -> str:
    filename = (upload.filename or "").lower().strip()
    content_type = (upload.content_type or "").lower().strip()
    if filename.endswith(".mp4") or content_type == "video/mp4":
        return "mp4"
    return "webm"


def build_photo_path(order_id: str, slot_name: str, upload: UploadFile) -> Path:
    folder = UPLOADS_DIR / order_id
    folder.mkdir(parents=True, exist_ok=True)
    ext = detect_image_extension(upload)
    return folder / f"{slot_name}.{ext}"


def reaction_video_path(order_id: str, extension: str = "webm") -> Path:
    extension = extension if extension in {"webm", "mp4"} else "webm"
    return VIDEOS_DIR / f"{order_id}.{extension}"


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


def insert_asset(order_id: str, asset_type: str, file_url: str, storage_provider: str = "local"):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO assets (order_id, asset_type, file_url, storage_provider, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (order_id, asset_type, file_url, storage_provider, now_iso()),
    )
    conn.commit()
    conn.close()


def get_order_by_id(order_id: str) -> dict:
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(
        """
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
        LIMIT 1
        """,
        (order_id,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return dict(row)


def get_order_by_recipient_token_or_404(token: str) -> dict:
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(
        """
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
        LIMIT 1
        """,
        (token,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Experiencia no encontrada")
    return dict(row)


def get_order_by_sender_token_or_404(token: str) -> dict:
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(
        """
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
        LIMIT 1
        """,
        (token,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Sender pack no encontrado")
    return dict(row)


def update_order(order_id: str, **fields):
    if not fields:
        return
    fields["updated_at"] = now_iso()
    columns = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values()) + [order_id]

    conn = db_conn()
    cur = conn.cursor()
    cur.execute(f"UPDATE orders SET {columns} WHERE id = ?", values)
    conn.commit()
    conn.close()


def reaction_exists(order: dict) -> bool:
    local_path = (order.get("reaction_video_local") or "").strip()
    public_url = (order.get("reaction_video_public_url") or "").strip()
    if public_url:
        return True
    if local_path and os.path.exists(local_path):
        return True
    return False


def recipient_experience_url(order: dict) -> str:
    return f"{PUBLIC_BASE_URL}/pedido/{order['recipient_token']}"


def sender_pack_url(order: dict) -> str:
    return f"{PUBLIC_BASE_URL}/sender/{order['sender_token']}"


def build_recipient_message(order: dict) -> str:
    return (
        "ETERNA\n\n"
        "Tienes algo que ver…\n\n"
        f"{recipient_experience_url(order)}"
    )


def build_sender_ready_message(order: dict) -> str:
    return (
        "Tu ETERNA ha vuelto.\n\n"
        f"{sender_pack_url(order)}"
    )


# =========================================================
# SMS
# =========================================================

def twilio_enabled() -> bool:
    return bool(
        TWILIO_ACCOUNT_SID and
        TWILIO_AUTH_TOKEN and
        TWILIO_FROM_NUMBER and
        TwilioClient is not None
    )


def send_sms(phone: str, message: str) -> dict:
    e164_phone = to_e164(phone)

    if not e164_phone:
        return {"ok": False, "sid": None, "error": "invalid_phone"}

    if not twilio_enabled():
        print("\n================ SMS STUB ================")
        print("TO:", e164_phone)
        print("MESSAGE:")
        print(message)
        print("=========================================\n")
        return {"ok": True, "sid": "stub_sid", "error": None}

    try:
        client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        sms = client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=e164_phone,
        )
        return {"ok": True, "sid": sms.sid, "error": None}
    except Exception as e:
        return {"ok": False, "sid": None, "error": str(e)}


def try_send_recipient_sms(order: dict) -> dict:
    if order.get("recipient_sms_sent_at"):
        return {"ok": True, "sid": order.get("recipient_sms_sid"), "already_sent": True, "error": None}

    result = send_sms(order.get("recipient_phone", ""), build_recipient_message(order))

    if result["ok"]:
        update_order(
            order["id"],
            recipient_sms_sent_at=now_iso(),
            recipient_sms_sid=result["sid"],
            recipient_sms_error=None,
        )
        return {"ok": True, "sid": result["sid"], "already_sent": False, "error": None}

    update_order(
        order["id"],
        recipient_sms_error=result["error"],
    )
    return {"ok": False, "sid": None, "already_sent": False, "error": result["error"]}


def try_send_sender_sms(order: dict) -> dict:
    if order.get("sender_sms_sent_at"):
        return {"ok": True, "sid": order.get("sender_sms_sid"), "already_sent": True, "error": None}

    result = send_sms(order.get("sender_phone", ""), build_sender_ready_message(order))

    if result["ok"]:
        update_order(
            order["id"],
            sender_sms_sent_at=now_iso(),
            sender_sms_sid=result["sid"],
            sender_sms_error=None,
            sender_notified=1,
        )
        return {"ok": True, "sid": result["sid"], "already_sent": False, "error": None}

    update_order(
        order["id"],
        sender_sms_error=result["error"],
    )
    return {"ok": False, "sid": None, "already_sent": False, "error": result["error"]}


# =========================================================
# VIDEO ENGINE BRIDGE
# =========================================================

def trigger_video_engine(order_id: str) -> str:
    order = get_order_by_id(order_id)

    conn = db_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT asset_type, file_url
        FROM assets
        WHERE order_id = ?
        ORDER BY id ASC
        """,
        (order_id,),
    )
    assets = cur.fetchall()
    conn.close()

    photo_map = {}

    for asset in assets:
        asset_type = (asset["asset_type"] or "").strip().lower()
        file_url = (asset["file_url"] or "").strip()

        if asset_type in {"photo1", "foto1"}:
            photo_map[1] = file_url
        elif asset_type in {"photo2", "foto2"}:
            photo_map[2] = file_url
        elif asset_type in {"photo3", "foto3"}:
            photo_map[3] = file_url
        elif asset_type in {"photo4", "foto4"}:
            photo_map[4] = file_url
        elif asset_type in {"photo5", "foto5"}:
            photo_map[5] = file_url
        elif asset_type in {"photo6", "foto6"}:
            photo_map[6] = file_url

    photo_paths = [photo_map[i] for i in range(1, 7) if i in photo_map]

    if len(photo_paths) != 6:
        raise Exception(f"El pedido {order_id} no tiene exactamente 6 fotos válidas")

    for idx, path in enumerate(photo_paths, start=1):
        if not os.path.exists(path):
            raise Exception(f"La foto {idx} no existe en disco: {path}")

    phrase_1 = (order.get("phrase_1") or "").strip()
    phrase_2 = (order.get("phrase_2") or "").strip()
    phrase_3 = (order.get("phrase_3") or "").strip()

    output_path = VIDEOS_DIR / f"{order_id}.mp4"

    from video_engine import render_eterna_video

    final_path = render_eterna_video(
        photo_paths=photo_paths,
        phrase_1=phrase_1,
        phrase_2=phrase_2,
        phrase_3=phrase_3,
        output_path=str(output_path),
    )

    final_path = final_path or str(output_path)

    if not os.path.exists(final_path):
        raise Exception(f"El render terminó pero no existe el archivo final: {final_path}")

    public_video_url = f"{PUBLIC_BASE_URL}/video/generated/{order_id}"

    update_order(
        order_id,
        experience_video_url=public_video_url,
    )

    insert_asset(
        order_id=order_id,
        asset_type="rendered_video",
        file_url=public_video_url,
        storage_provider="local",
    )

    return public_video_url


@app.get("/video/generated/{order_id}")
def generated_video(order_id: str):
    filepath = VIDEOS_DIR / f"{order_id}.mp4"
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Vídeo generado no encontrado")
    return FileResponse(
        str(filepath),
        media_type="video/mp4",
        filename=f"{order_id}.mp4",
    )


# =========================================================
# FORM HTML
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
            }}
            h1 {{ margin: 0 0 12px 0; font-size: 36px; text-align: center; letter-spacing: 2px; }}
            .subtitle {{ text-align: center; color: rgba(255,255,255,0.7); line-height: 1.7; margin-bottom: 10px; }}
            .intro-soft {{
                text-align: center;
                color: rgba(255,255,255,0.48);
                line-height: 1.8;
                margin: 0 auto 26px auto;
                max-width: 620px;
                font-size: 14px;
            }}
            .section-title {{
                margin: 22px 0 10px 0;
                font-size: 13px;
                letter-spacing: 1.4px;
                text-transform: uppercase;
                color: rgba(255,255,255,0.55);
            }}
            input {{
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
            input::placeholder {{ color: rgba(255,255,255,0.4); }}
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
            }}
            .photo-box input[type="file"] {{
                position: absolute;
                inset: 0;
                opacity: 0;
                cursor: pointer;
                margin: 0;
                padding: 0;
            }}
            .photo-placeholder {{
                color: rgba(255,255,255,0.48);
                line-height: 1.7;
                font-size: 14px;
            }}
            .photo-preview {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: none;
                position: absolute;
                inset: 0;
            }}
            .mini-note {{
                margin-top: 10px;
                color: rgba(255,255,255,0.42);
                font-size: 12px;
                line-height: 1.6;
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
            .emotion-title {{ font-size: 16px; font-weight: 600; margin-bottom: 6px; }}
            .emotion-sub {{ font-size: 13px; color: rgba(255,255,255,0.55); line-height: 1.45; }}
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
            .radio-row input {{ width: auto; margin: 0; }}
            .recommended {{ opacity: 0.5; font-size: 12px; margin-left: 4px; }}
            .phrases-manual.hidden {{ display: none; }}
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
                margin-top: 10px;
                font-size: 13px;
                line-height: 1.7;
                color: rgba(255,255,255,0.45);
                text-align: center;
            }}
            .buttons {{ display: grid; gap: 12px; margin-top: 24px; }}
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
            button {{ background: white; color: black; }}
            .ghost {{
                display: inline-block;
                background: rgba(255,255,255,0.10);
                color: white;
                border: 1px solid rgba(255,255,255,0.10);
            }}
            @media (max-width: 760px) {{
                .photo-grid,
                .emotion-grid {{
                    grid-template-columns: 1fr;
                }}
                body {{ padding: 16px; }}
                .card {{ padding: 22px; }}
            }}
        </style>
    </head>
    <body>
        <div class="wrap">
            <div class="card">
                <h1>CREAR ETERNA</h1>
                <div class="subtitle">Hay momentos que merecen quedarse para siempre</div>
                <div class="intro-soft">
                    Shhh…<br>
                    Esto no es un vídeo.<br>
                    Es algo que alguien no va a olvidar.
                </div>

                <form action="/crear" method="post" enctype="multipart/form-data" id="createForm">
                    <div class="section-title">Tus datos</div>
                    <input name="customer_name" placeholder="Tu nombre" required>
                    <input name="customer_email" type="email" placeholder="Tu email">
                    <input name="customer_phone" placeholder="Tu teléfono (ej. 674123456)" required>

                    <div class="section-title">Persona que recibe</div>
                    <input name="recipient_name" placeholder="Nombre de la persona" required>
                    <input name="recipient_phone" placeholder="Teléfono de la persona (ej. 674123456)" required>

                    <div class="section-title">Tus 6 fotos</div>
                    <div class="photo-grid">
                        <div class="photo-card">
                            <div class="photo-label">Foto 1</div>
                            <div class="photo-guide">Una imagen solo suya.</div>
                            <label class="photo-box">
                                <img class="photo-preview" id="preview_photo1">
                                <div class="photo-placeholder" id="placeholder_photo1">Añadir foto</div>
                                <input type="file" name="photo1" id="photo1" accept="image/*" required>
                            </label>
                        </div>

                        <div class="photo-card">
                            <div class="photo-label">Foto 2</div>
                            <div class="photo-guide">Ese momento que lo dice todo.</div>
                            <label class="photo-box">
                                <img class="photo-preview" id="preview_photo2">
                                <div class="photo-placeholder" id="placeholder_photo2">Añadir foto</div>
                                <input type="file" name="photo2" id="photo2" accept="image/*" required>
                            </label>
                        </div>

                        <div class="photo-card">
                            <div class="photo-label">Foto 3</div>
                            <div class="photo-guide">Algo que os una.</div>
                            <label class="photo-box">
                                <img class="photo-preview" id="preview_photo3">
                                <div class="photo-placeholder" id="placeholder_photo3">Añadir foto</div>
                                <input type="file" name="photo3" id="photo3" accept="image/*" required>
                            </label>
                        </div>

                        <div class="photo-card">
                            <div class="photo-label">Foto 4</div>
                            <div class="photo-guide">Un recuerdo que duela bonito.</div>
                            <label class="photo-box">
                                <img class="photo-preview" id="preview_photo4">
                                <div class="photo-placeholder" id="placeholder_photo4">Añadir foto</div>
                                <input type="file" name="photo4" id="photo4" accept="image/*" required>
                            </label>
                        </div>

                        <div class="photo-card">
                            <div class="photo-label">Foto 5</div>
                            <div class="photo-guide">Algo especial, solo vuestro.</div>
                            <label class="photo-box">
                                <img class="photo-preview" id="preview_photo5">
                                <div class="photo-placeholder" id="placeholder_photo5">Añadir foto</div>
                                <input type="file" name="photo5" id="photo5" accept="image/*" required>
                            </label>
                        </div>

                        <div class="photo-card">
                            <div class="photo-label">Foto 6</div>
                            <div class="photo-guide">La que nunca olvidará.</div>
                            <label class="photo-box">
                                <img class="photo-preview" id="preview_photo6">
                                <div class="photo-placeholder" id="placeholder_photo6">Añadir foto</div>
                                <input type="file" name="photo6" id="photo6" accept="image/*" required>
                            </label>
                        </div>
                    </div>

                    <div class="mini-note">
                        Recomendación: mejor verticales. Idealmente 2 fotos suyas, 2 juntos y 2 finales suyas.
                    </div>

                    <div class="section-title">Elige la emoción</div>

                    <div class="emotion-grid">
                        <div class="emotion-card" data-type="cumpleanos">
                            <div class="emotion-title">Cumpleaños</div>
                            <div class="emotion-sub">Un día que merece quedarse</div>
                        </div>
                        <div class="emotion-card" data-type="amor">
                            <div class="emotion-title">Amor</div>
                            <div class="emotion-sub">Cuando lo que sientes ya no cabe dentro</div>
                        </div>
                        <div class="emotion-card" data-type="familia">
                            <div class="emotion-title">Familia</div>
                            <div class="emotion-sub">Para quien siempre ha estado</div>
                        </div>
                        <div class="emotion-card" data-type="superacion">
                            <div class="emotion-title">Superación</div>
                            <div class="emotion-sub">Para recordar todo lo que vale</div>
                        </div>
                        <div class="emotion-card" data-type="esfuerzo">
                            <div class="emotion-title">Esfuerzo</div>
                            <div class="emotion-sub">Para reconocer lo que otros no siempre ven</div>
                        </div>
                        <div class="emotion-card" data-type="sorpresa">
                            <div class="emotion-title">Sorpresa</div>
                            <div class="emotion-sub">Cuando quieres tocar el corazón sin avisar</div>
                        </div>
                    </div>

                    <input type="hidden" name="message_type" id="messageType" required>

                    <div class="mode-box">
                        <div class="radio-row">
                            <input type="radio" id="mode_auto" name="phrase_mode" value="auto" checked>
                            <label for="mode_auto">
                                Que ETERNA lo haga por mí
                                <span class="recommended">(recomendado)</span>
                            </label>
                        </div>

                        <div class="radio-row">
                            <input type="radio" id="mode_manual" name="phrase_mode" value="manual">
                            <label for="mode_manual">Quiero escribir mis frases</label>
                        </div>
                    </div>

                    <div class="phrases-manual hidden" id="manualPhrases">
                        <div class="section-title">Tus 3 frases</div>
                        <input name="phrase_1" placeholder="Frase para foto 2" maxlength="160">
                        <input name="phrase_2" placeholder="Frase para foto 4" maxlength="160">
                        <input name="phrase_3" placeholder="Frase para foto 6" maxlength="160">
                    </div>

                    <div class="section-title">Dinero a regalar</div>
                    <input
                        name="gift_amount"
                        placeholder="Dinero a regalar (€)"
                        type="number"
                        step="0.01"
                        min="0"
                        value="0"
                        required
                    >

                    <div class="price-box">
                        Precio base ETERNA: {money(ETERNA_BASE_PRICE)}€<br>
                        Comisión regalo: {(GIFT_COMMISSION_RATE * 100):.0f}% del importe regalado
                    </div>

                    <div class="hint">No es un vídeo. Es un momento.</div>

                    <div class="buttons">
                        <button type="submit" id="submitBtn">CONTINUAR</button>
                        <a class="btn ghost" href="/">Volver</a>
                    </div>
                </form>
            </div>
        </div>

        <script>
            const cards = document.querySelectorAll(".emotion-card");
            const input = document.getElementById("messageType");
            const autoRadio = document.getElementById("mode_auto");
            const manualRadio = document.getElementById("mode_manual");
            const manualPhrases = document.getElementById("manualPhrases");
            const form = document.getElementById("createForm");
            const button = document.getElementById("submitBtn");

            cards.forEach(card => {{
                card.addEventListener("click", () => {{
                    cards.forEach(c => c.classList.remove("selected"));
                    card.classList.add("selected");
                    input.value = card.dataset.type;
                }});
            }});

            function updatePhraseMode() {{
                if (manualRadio.checked) manualPhrases.classList.remove("hidden");
                else manualPhrases.classList.add("hidden");
            }}

            autoRadio.addEventListener("change", updatePhraseMode);
            manualRadio.addEventListener("change", updatePhraseMode);
            updatePhraseMode();

            function bindPreview(inputId) {{
                const fileInput = document.getElementById(inputId);
                const preview = document.getElementById("preview_" + inputId);
                const placeholder = document.getElementById("placeholder_" + inputId);

                fileInput.addEventListener("change", function() {{
                    const file = this.files && this.files[0];
                    if (!file) return;

                    const url = URL.createObjectURL(file);
                    preview.src = url;
                    preview.style.display = "block";
                    placeholder.style.display = "none";
                }});
            }}

            ["photo1", "photo2", "photo3", "photo4", "photo5", "photo6"].forEach(bindPreview);

            form.addEventListener("submit", function () {{
                button.disabled = true;
                button.textContent = "Procesando...";
            }});
        </script>
    </body>
    </html>
    """


# =========================================================
# HOME
# =========================================================

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ETERNA</title>
        </head>
        <body style="margin:0;min-height:100vh;background:#000;color:white;font-family:Arial,sans-serif;display:flex;align-items:center;justify-content:center;text-align:center;padding:24px;">
            <div style="max-width:760px;">
                <h1 style="font-size:52px;margin:0 0 18px 0;letter-spacing:2px;">ETERNA</h1>
                <div style="font-size:22px;line-height:1.8;color:rgba(255,255,255,0.85);margin-bottom:28px;">
                    Hay momentos que merecen quedarse para siempre
                </div>
                <a href="/crear" style="display:inline-block;padding:16px 28px;border-radius:999px;background:white;color:black;text-decoration:none;font-weight:bold;">
                    CREAR MI ETERNA
                </a>
            </div>
        </body>
        </html>
        """
    )


@app.get("/crear", response_class=HTMLResponse)
def crear_get():
    return render_create_form()


# =========================================================
# CREATE ORDER
# =========================================================

async def save_upload_to_path(upload: UploadFile, path: Path):
    with open(path, "wb") as f:
        while True:
            chunk = await upload.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)


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

    if not sender_phone:
        raise HTTPException(status_code=400, detail="Teléfono del comprador no válido")

    if not recipient_phone_norm:
        raise HTTPException(status_code=400, detail="Teléfono del destinatario no válido")

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

        valid_type = content_type.startswith("image/")
        valid_name = filename.endswith((".jpg", ".jpeg", ".png", ".webp"))

        if not valid_type and not valid_name:
            raise HTTPException(status_code=400, detail=f"{slot_name} no es una imagen válida")

    order_id = new_order_id()
    recipient_token = new_token()
    sender_token = new_token()
    created_at = now_iso()
    totals = calculate_totals(gift_amount)

    conn = db_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO senders (name, email, phone, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (customer_name, customer_email, sender_phone, created_at),
    )
    sender_id = cur.lastrowid

    cur.execute(
        """
        INSERT INTO recipients (name, phone, created_at)
        VALUES (?, ?, ?)
        """,
        (recipient_name, recipient_phone_norm, created_at),
    )
    recipient_id = cur.lastrowid

    cur.execute(
        """
        INSERT INTO orders (
            id, sender_id, recipient_id,
            message_type, phrase_mode,
            phrase_1, phrase_2, phrase_3,
            gift_amount, gift_commission, total_amount,
            paid, delivered_to_recipient, experience_started, experience_completed, reaction_uploaded, sender_notified,
            stripe_session_id, stripe_payment_status, stripe_payment_intent_id,
            recipient_token, sender_token,
            reaction_video_local, reaction_video_public_url, experience_video_url,
            recipient_sms_sent_at, sender_sms_sent_at, recipient_sms_sid, sender_sms_sid,
            recipient_sms_error, sender_sms_error,
            created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            order_id, sender_id, recipient_id,
            message_type, phrase_mode,
            phrase_1, phrase_2, phrase_3,
            totals["gift_amount"], totals["gift_commission"], totals["total_amount"],
            0, 0, 0, 0, 0, 0,
            None, None, None,
            recipient_token, sender_token,
            None, None, None,
            None, None, None, None,
            None, None,
            created_at, created_at,
        ),
    )

    conn.commit()
    conn.close()

    try:
        for slot_name, upload in photos.items():
            photo_path = build_photo_path(order_id, slot_name, upload)
            await save_upload_to_path(upload, photo_path)
            insert_asset(
                order_id=order_id,
                asset_type=slot_name,
                file_url=str(photo_path),
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
        )

        order = get_order_by_id(order_id)

        try:
            try_send_recipient_sms(order)
        except Exception as e:
            log_error("SMS destinatario sin Stripe", e)

        try:
            trigger_video_engine(order_id)
        except Exception as e:
            log_error("Video engine sin Stripe", e)
            traceback.print_exc()

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
                        "currency": ETERNA_CURRENCY,
                        "product_data": {
                            "name": "ETERNA",
                            "description": (
                                f"Base {money(ETERNA_BASE_PRICE)}€ + "
                                f"regalo {money(totals['gift_amount'])}€ + "
                                f"comisión {money(totals['gift_commission'])}€"
                            ),
                        },
                        "unit_amount": int(round(totals["total_amount"] * 100)),
                    },
                    "quantity": 1,
                }
            ],
            success_url=f"{PUBLIC_BASE_URL}/checkout-exito/{order_id}",
            cancel_url=f"{PUBLIC_BASE_URL}/crear",
        )

        update_order(
            order_id,
            stripe_session_id=session.id,
            stripe_payment_status="created",
        )

        return RedirectResponse(url=session.url, status_code=303)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando checkout Stripe: {e}")


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
# CHECKOUT / WEBHOOK
# =========================================================

@app.get("/checkout-exito/{order_id}", response_class=HTMLResponse)
def checkout_exito(order_id: str):
    order = get_order_by_id(order_id)
    is_paid = bool(order["paid"])

    refresh = '<meta http-equiv="refresh" content="5">' if not is_paid else ""
    redirect_script = f"""
        setTimeout(function() {{
            window.location.href = "/post-pago/{safe_attr(order_id)}";
        }}, 3000);
    """ if is_paid else ""

    return f"""
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
    """


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
        return {"status": "ignored", "event_type": event["type"]}

    session = event["data"]["object"]
    session_id = session.get("id")
    order_id = session.get("client_reference_id")

    if not order_id:
        metadata = session.get("metadata", {}) or {}
        order_id = metadata.get("order_id")

    if not order_id and session_id:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT id FROM orders WHERE stripe_session_id = ? LIMIT 1",
            (session_id,),
        )
        row = cur.fetchone()
        conn.close()
        if row:
            order_id = row["id"]

    if not order_id:
        log_error("WEBHOOK sin order_id")
        return {"status": "error", "reason": "order_id_not_found"}

    conn = db_conn()
    cur = conn.cursor()
    cur.execute("SELECT paid FROM orders WHERE id = ? LIMIT 1", (order_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        log_error(f"WEBHOOK pedido no encontrado: {order_id}")
        return {"status": "error", "reason": "order_not_found"}

    already_paid = int(row["paid"] or 0) == 1

    cur.execute(
        """
        UPDATE orders
        SET paid = 1,
            stripe_session_id = COALESCE(?, stripe_session_id),
            stripe_payment_status = ?,
            stripe_payment_intent_id = COALESCE(?, stripe_payment_intent_id),
            updated_at = ?
        WHERE id = ?
        """,
        (
            session_id,
            session.get("payment_status", "paid"),
            session.get("payment_intent"),
            now_iso(),
            order_id,
        ),
    )
    conn.commit()
    conn.close()

    if not already_paid:
        try:
            order = get_order_by_id(order_id)
            try_send_recipient_sms(order)
        except Exception as e:
            log_error("WEBHOOK SMS destinatario", e)

        try:
            trigger_video_engine(order_id)
        except Exception as e:
            log_error("WEBHOOK VIDEO ENGINE", e)
            traceback.print_exc()

    return {"status": "success"}


@app.get("/post-pago/{order_id}")
def post_pago(order_id: str):
    order = get_order_by_id(order_id)
    if not order["paid"]:
        return RedirectResponse(url=f"/checkout-exito/{order_id}", status_code=303)
    return RedirectResponse(url=f"/resumen/{order_id}", status_code=303)


@app.get("/resumen/{order_id}", response_class=HTMLResponse)
def resumen(order_id: str):
    order = get_order_by_id(order_id)

    if not order.get("recipient_sms_sent_at"):
        try:
            try_send_recipient_sms(order)
            order = get_order_by_id(order_id)
        except Exception as e:
            log_error("Resumen SMS destinatario", e)

    recipient_name = safe_text(order.get("recipient_name") or "esa persona")
    sms_sent = bool(order.get("recipient_sms_sent_at"))

    if sms_sent:
        status_line = "Estamos creando tu momento."
        sub_line = f"{recipient_name} ya tiene su mensaje."
        soft_line = "Pronto tendrás noticias."
    else:
        status_line = "Estamos creando tu momento."
        sub_line = f"Estamos intentando enviar el mensaje a {recipient_name}."
        soft_line = "Pronto tendrás noticias."

    return HTMLResponse(
        f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
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
        """
    )


# =========================================================
# PEDIDO / EXPERIENCIA
# =========================================================

@app.get("/pedido/{recipient_token}", response_class=HTMLResponse)
def pedido(recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not order["paid"]:
        return HTMLResponse(
            """
            <!DOCTYPE html>
            <html lang="es">
            <body style="background:#000;color:white;text-align:center;padding-top:100px;font-family:Arial;">
                <h1>Esta ETERNA aún no está disponible</h1>
            </body>
            </html>
            """
        )

    if bool(order.get("experience_completed")):
        return RedirectResponse(url=f"/mi-video/{recipient_token}", status_code=303)

    return HTMLResponse(
        f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ETERNA</title>
            <style>
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
                .card {{
                    width: 100%;
                    max-width: 720px;
                    background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 28px;
                    padding: 40px 28px;
                }}
                h1 {{
                    font-size: 40px;
                    margin: 0 0 18px 0;
                    line-height: 1.25;
                }}
                .line {{
                    font-size: 22px;
                    line-height: 1.8;
                    color: rgba(255,255,255,0.88);
                    margin-top: 8px;
                }}
                .btn {{
                    width: 100%;
                    margin-top: 30px;
                    padding: 17px 22px;
                    border-radius: 999px;
                    border: 0;
                    background: white;
                    color: black;
                    font-weight: bold;
                    font-size: 15px;
                    cursor: pointer;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>Esto es solo para ti</h1>

                <div class="line">Busca un momento a solas</div>
                <div class="line">Sin ruido</div>
                <div class="line">Sin prisa</div>

                <button class="btn" onclick="window.location.href='/experiencia/{safe_attr(recipient_token)}'">Vivirlo</button>
            </div>
        </body>
        </html>
        """
    )


def try_start_experience(order_id: str) -> str:
    order = get_order_by_id(order_id)

    if not bool(order.get("paid")):
        return "not_paid"

    if bool(order.get("experience_completed")):
        return "already_completed"

    update_order(
        order_id,
        experience_started=1,
        delivered_to_recipient=1,
    )

    return "started"


@app.post("/start-experience")
def start_experience(recipient_token: str = Form(...)):
    order = get_order_by_recipient_token_or_404(recipient_token)
    result = try_start_experience(order["id"])

    if result == "not_paid":
        raise HTTPException(status_code=403, detail="Pedido no pagado")

    if result == "already_completed":
        return JSONResponse(
            {
                "status": "already_completed",
                "redirect_url": f"/mi-video/{recipient_token}",
            }
        )

    return JSONResponse({"status": "ok"})


@app.get("/experiencia/{recipient_token}", response_class=HTMLResponse)
def experiencia(recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not order["paid"]:
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if bool(order.get("experience_completed")):
        return RedirectResponse(url=f"/mi-video/{recipient_token}", status_code=303)

    phrase_1 = safe_text(order["phrase_1"])
    phrase_2 = safe_text(order["phrase_2"])
    phrase_3 = safe_text(order["phrase_3"])
    gift_amount = format_amount_display(order["gift_amount"])

    return HTMLResponse(
        f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ETERNA</title>
            <style>
                * {{ box-sizing: border-box; }}
                html, body {{
                    margin: 0;
                    width: 100%;
                    min-height: 100%;
                    background: #000;
                }}
                body {{
                    background: #000;
                    color: white;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }}
                .screen {{
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    padding: 24px;
                }}
                #content {{
                    width: 100%;
                    max-width: 920px;
                    padding: 24px;
                    opacity: 0;
                    transform: translateY(12px);
                    transition: opacity 0.7s ease, transform 0.7s ease;
                }}
                #content.visible {{
                    opacity: 1;
                    transform: translateY(0);
                }}
                #content h2 {{
                    font-size: 42px;
                    line-height: 1.4;
                    margin: 0;
                    font-weight: 500;
                    color: white;
                    white-space: pre-line;
                    opacity: 0.95;
                }}
                #content .amount {{
                    margin-top: 20px;
                    font-size: 54px;
                    font-weight: bold;
                    line-height: 1;
                }}
                #statusMsg {{
                    margin-top: 20px;
                    color: rgba(255,255,255,0.6);
                    font-size: 14px;
                }}
                @media (max-width: 768px) {{
                    #content h2 {{ font-size: 30px; }}
                    #content .amount {{ font-size: 42px; }}
                }}
            </style>
        </head>
        <body>
            <div class="screen">
                <div id="content"></div>
                <div id="statusMsg"></div>
            </div>

            <script>
                let recorder = null;
                let chunks = [];
                let currentStream = null;
                let mediaMimeType = "video/webm";
                let uploadStarted = false;
                let experienceStarted = false;

                function wait(ms) {{
                    return new Promise(resolve => setTimeout(resolve, ms));
                }}

                function setStatus(text) {{
                    const el = document.getElementById("statusMsg");
                    if (el) el.textContent = text || "";
                }}

                async function showScene(scene) {{
                    const content = document.getElementById("content");
                    content.classList.remove("visible");
                    await wait(180);
                    content.innerHTML = scene.html || "";
                    await wait(40);
                    content.classList.add("visible");
                    await wait(scene.duration || 2000);
                }}

                async function lockExperienceStart() {{
                    const formData = new FormData();
                    formData.append("recipient_token", "{safe_attr(order['recipient_token'])}");

                    const response = await fetch("/start-experience", {{
                        method: "POST",
                        body: formData
                    }});

                    const data = await response.json();

                    if (data.status === "already_completed") {{
                        window.location.href = data.redirect_url || "/mi-video/{safe_attr(order['recipient_token'])}";
                        return false;
                    }}

                    return true;
                }}

                async function sendVideo() {{
                    try {{
                        if (!chunks.length) return null;

                        const ext = mediaMimeType.includes("mp4") ? "mp4" : "webm";
                        const blob = new Blob(chunks, {{
                            type: ext === "mp4" ? "video/mp4" : "video/webm"
                        }});

                        if (!blob || blob.size === 0) return null;

                        const formData = new FormData();
                        formData.append("recipient_token", "{safe_attr(order['recipient_token'])}");
                        formData.append("video", blob, "{safe_attr(order['id'])}." + ext);

                        const response = await fetch("/upload-video", {{
                            method: "POST",
                            body: formData
                        }});

                        if (!response.ok) return null;
                        return await response.json();

                    }} catch (err) {{
                        return null;
                    }}
                }}

                async function stopRecordingAndUpload() {{
                    if (uploadStarted) return null;
                    uploadStarted = true;

                    if (recorder && recorder.state !== "inactive") {{
                        await new Promise((resolve) => {{
                            recorder.onstop = () => resolve();
                            try {{
                                recorder.stop();
                            }} catch (e) {{
                                resolve();
                            }}
                        }});
                    }}

                    if (currentStream) {{
                        currentStream.getTracks().forEach(track => track.stop());
                        currentStream = null;
                    }}

                    await wait(500);
                    return await sendVideo();
                }}

                async function finishFlow() {{
                    setStatus("Guardando este momento…");

                    const result = await stopRecordingAndUpload();

                    if (!result || (result.status !== "ok" && result.status !== "already_uploaded")) {{
                        alert("No hemos podido guardar bien la reacción. Inténtalo otra vez.");
                        window.location.href = "/pedido/{safe_attr(order['recipient_token'])}";
                        return;
                    }}

                    window.location.href = result.final_url || "/mi-video/{safe_attr(order['recipient_token'])}";
                }}

                const scenes = [
                    {{ html: "<h2>Esto no es un vídeo.</h2>", duration: 2000 }},
                    {{ html: "<h2>No es solo un momento.</h2>", duration: 2000 }},
                    {{ html: "<h2>Esto es magia.</h2>", duration: 2400 }},
                    {{ html: "<h2>{phrase_1}</h2>", duration: 2200 }},
                    {{ html: "<h2>{phrase_2}</h2>", duration: 2200 }},
                    {{ html: "<h2>{phrase_3}</h2>", duration: 2200 }},
                    {{
                        html: "<h2>Esto es para ti.</h2><div class='amount'>{gift_amount}</div>",
                        duration: 5000
                    }}
                ];

                async function startExperience() {{
                    if (experienceStarted) return;
                    experienceStarted = true;

                    try {{
                        if (!window.MediaRecorder) {{
                            throw new Error("MediaRecorder no soportado");
                        }}

                        const stream = await navigator.mediaDevices.getUserMedia({{
                            video: {{ width: 640, height: 480, facingMode: "user" }},
                            audio: true
                        }});

                        currentStream = stream;
                        chunks = [];
                        uploadStarted = false;

                        let options = null;

                        if (MediaRecorder.isTypeSupported("video/webm;codecs=vp8,opus")) {{
                            mediaMimeType = "video/webm;codecs=vp8,opus";
                            options = {{
                                mimeType: mediaMimeType,
                                videoBitsPerSecond: 900000,
                                audioBitsPerSecond: 64000
                            }};
                        }} else if (MediaRecorder.isTypeSupported("video/webm")) {{
                            mediaMimeType = "video/webm";
                            options = {{
                                mimeType: mediaMimeType,
                                videoBitsPerSecond: 900000,
                                audioBitsPerSecond: 64000
                            }};
                        }} else if (MediaRecorder.isTypeSupported("video/mp4")) {{
                            mediaMimeType = "video/mp4";
                            options = {{
                                mimeType: mediaMimeType,
                                videoBitsPerSecond: 900000,
                                audioBitsPerSecond: 64000
                            }};
                        }} else {{
                            throw new Error("Formato no soportado");
                        }}

                        const lockOk = await lockExperienceStart();
                        if (!lockOk) {{
                            if (currentStream) {{
                                currentStream.getTracks().forEach(track => track.stop());
                                currentStream = null;
                            }}
                            return;
                        }}

                        recorder = new MediaRecorder(stream, options);

                        recorder.ondataavailable = (e) => {{
                            if (e.data && e.data.size > 0) chunks.push(e.data);
                        }};

                        await wait(300);
                        recorder.start(300);

                        for (const scene of scenes) {{
                            await showScene(scene);
                        }}

                        await finishFlow();

                    }} catch (e) {{
                        if (currentStream) {{
                            currentStream.getTracks().forEach(track => track.stop());
                            currentStream = null;
                        }}
                        alert("Necesitamos acceso a cámara y micrófono para continuar.");
                        window.location.href = "/pedido/{safe_attr(order['recipient_token'])}";
                    }}
                }}

                startExperience();
            </script>
        </body>
        </html>
        """
    )


# =========================================================
# UPLOAD VIDEO REACCION
# =========================================================

@app.post("/upload-video")
async def upload_video(
    recipient_token: str = Form(...),
    video: UploadFile = File(...),
):
    order = get_order_by_recipient_token_or_404(recipient_token)
    order_id = order["id"]

    if not order["paid"]:
        raise HTTPException(status_code=403, detail="Pedido no pagado")

    if bool(order.get("reaction_uploaded")) or reaction_exists(order):
        return JSONResponse(
            {
                "status": "already_uploaded",
                "final_url": f"{PUBLIC_BASE_URL}/mi-video/{order['recipient_token']}",
            }
        )

    content_type = (video.content_type or "").lower().strip()
    filename = (video.filename or "").lower().strip()

    valid_type = content_type in ALLOWED_VIDEO_TYPES
    valid_name = filename.endswith(".webm") or filename.endswith(".mp4")

    if not valid_type and not valid_name:
        raise HTTPException(status_code=400, detail="Formato de vídeo no permitido")

    video_extension = detect_video_extension(video)
    filepath = reaction_video_path(order_id, video_extension)

    total_size = 0

    try:
        with open(filepath, "wb") as f:
            while True:
                chunk = await video.read(1024 * 1024)
                if not chunk:
                    break

                total_size += len(chunk)
                if total_size > MAX_VIDEO_SIZE:
                    f.close()
                    if filepath.exists():
                        filepath.unlink()
                    raise HTTPException(status_code=400, detail="Vídeo demasiado grande")

                f.write(chunk)

        if not filepath.exists() or filepath.stat().st_size == 0:
            raise HTTPException(status_code=400, detail="Vídeo vacío")

        public_video_url = f"{PUBLIC_BASE_URL}/video/sender/{order['sender_token']}"

        update_order(
            order_id,
            reaction_uploaded=1,
            experience_completed=1,
            reaction_video_local=str(filepath),
            reaction_video_public_url=public_video_url,
        )

        insert_asset(
            order_id=order_id,
            asset_type="reaction_video",
            file_url=public_video_url,
            storage_provider="local",
        )

        updated_order = get_order_by_id(order_id)

        try:
            try_send_sender_sms(updated_order)
        except Exception as e:
            log_error("SMS regalante tras reacción", e)

        return JSONResponse(
            {
                "status": "ok",
                "final_url": f"{PUBLIC_BASE_URL}/mi-video/{updated_order['recipient_token']}",
            }
        )

    finally:
        try:
            await video.close()
        except Exception:
            pass


# =========================================================
# VIDEOS
# =========================================================

@app.get("/video/sender/{sender_token}")
def get_video_for_sender(sender_token: str):
    order = get_order_by_sender_token_or_404(sender_token)
    filepath = (order.get("reaction_video_local") or "").strip()

    if not filepath or not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Vídeo no encontrado")

    media_type = guess_media_type_from_path(filepath)

    return FileResponse(
        filepath,
        media_type=media_type,
        filename=os.path.basename(filepath),
    )


# =========================================================
# FINAL RECIPIENTE
# =========================================================

@app.get("/mi-video/{recipient_token}", response_class=HTMLResponse)
def mi_video(recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(order.get("experience_started")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not bool(order.get("experience_completed")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    experience_video_url = (order.get("experience_video_url") or DEFAULT_EXPERIENCE_VIDEO_URL or "").strip()

    if not experience_video_url:
        return HTMLResponse(
            """
            <!DOCTYPE html>
            <html lang="es">
            <body style="margin:0;min-height:100vh;background:#000;color:white;font-family:Arial, sans-serif;display:flex;align-items:center;justify-content:center;text-align:center;padding:24px;">
                <div>
                    <h1>Tu momento ya es tuyo.</h1>
                    <p>Falta conectar el vídeo original final de esta ETERNA.</p>
                </div>
            </body>
            </html>
            """
        )

    video_type = guess_media_type_from_url(experience_video_url)

    return HTMLResponse(
        f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mi vídeo</title>
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
                .wrap {{
                    width: 100%;
                    max-width: 720px;
                    margin: 0 auto;
                    text-align: center;
                }}
                h1 {{
                    margin: 0 0 18px 0;
                    font-size: 38px;
                }}
                .sub {{
                    color: rgba(255,255,255,0.72);
                    font-size: 18px;
                    line-height: 1.7;
                    margin-bottom: 24px;
                }}
                video {{
                    width: 100%;
                    border-radius: 22px;
                    background: #000;
                    overflow: hidden;
                }}
            </style>
        </head>
        <body>
            <div class="wrap">
                <h1>Esto ya es tuyo</h1>
                <div class="sub">Tu momento original</div>
                <video controls playsinline preload="metadata">
                    <source src="{safe_attr(experience_video_url)}" type="{safe_attr(video_type)}">
                </video>
            </div>
        </body>
        </html>
        """
    )


# =========================================================
# SENDER PACK
# =========================================================

@app.get("/sender/{sender_token}", response_class=HTMLResponse)
def sender_pack(sender_token: str):
    order = get_order_by_sender_token_or_404(sender_token)

    if not bool(order.get("reaction_uploaded")):
        return HTMLResponse(
            """
            <!DOCTYPE html>
            <html lang="es">
            <body style="margin:0;min-height:100vh;background:#000;color:white;font-family:Arial,sans-serif;display:flex;align-items:center;justify-content:center;text-align:center;padding:24px;">
                <div>
                    <h1>Aún no ha vuelto</h1>
                    <p>La reacción todavía no está disponible.</p>
                </div>
            </body>
            </html>
            """
        )

    reaction_url = f"{PUBLIC_BASE_URL}/video/sender/{order['sender_token']}"
    reaction_type = guess_media_type_from_url(reaction_url)

    return HTMLResponse(
        f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tu ETERNA ha vuelto</title>
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
                .wrap {{
                    width: 100%;
                    max-width: 720px;
                    margin: 0 auto;
                    text-align: center;
                }}
                h1 {{
                    margin: 0 0 18px 0;
                    font-size: 38px;
                }}
                .sub {{
                    color: rgba(255,255,255,0.72);
                    font-size: 18px;
                    line-height: 1.7;
                    margin-bottom: 24px;
                }}
                video {{
                    width: 100%;
                    border-radius: 22px;
                    background: #000;
                    overflow: hidden;
                }}
            </style>
        </head>
        <body>
            <div class="wrap">
                <h1>Tu ETERNA ha vuelto</h1>
                <div class="sub">Esta es su reacción</div>
                <video controls playsinline preload="metadata">
                    <source src="{safe_attr(reaction_url)}" type="{safe_attr(reaction_type)}">
                </video>
            </div>
        </body>
        </html>
        """
    )