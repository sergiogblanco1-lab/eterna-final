# =========================================================
# RC82_PREEXPERIENCIA_CLEAN_SAFE
# Base: RC81.
# Limpia preexperiencia:
# - rescate oculto en flujo normal
# - rescate solo emergencia real
# - cámara/colocación 4 segundos
# - reduce Yul explicativa
# - mantiene SMS salvavidas + sender_pack_master_v1
# =========================================================

print("🔥 ETERNA MAIN DEFINITIVO BLINDADO 🔥")
print("🔥 WEBHOOK + CALLBACK + EXPERIENCE LOCK + REACTION SAVE 🔥")
print("🔥 FINAL UX LOCKED + CASHOUT HARDENED + SENDER PACK READY 🔥")
print("🔥 REACTION RETRY + ETERNA COMPLETE SAFE VERSION 🔥")
print("🔥 SCHEDULED DELIVERY LOCKED VERSION 🔥")
print("🔥 DELIVERY WORKER REAL VERSION 🔥")
print("🔥 GLOBAL PHONE READY VERSION 🔥")
print("🔥 DELIVERY FEE +2€ ONLY IF SCHEDULED VERSION 🔥")
print("🔥 NO SHARE ORIGINAL VIDEO VERSION 🔥")
print("🔥 VIRAL BLOCK + CALLBACK IDEMPOTENT + SMS/WHATSAPP HARDENED VERSION 🔥")
print("✨ VISUAL ETERNA UNIFIED SCREENS VERSION ✨")
print("🛡️ WORKER SENDER SMS EXHAUSTED FILTER VERSION 🛡️")
print("🏛️ HOME PREMIUM + PAGO CONFIRMADO ÚNICO VERSION 🏛️")
print("🎬 ETERNA CINEMATIC FILM UI + STABLE BASE + SENDER AUDIO ENGINE ONLY 🎬")
print("🛟 RC82 PREEXPERIENCIA CLEAN SAFE — MAIN COMPLETO + EL UMBRAL 🛟")

print("🛟 RC82 PREEXPERIENCIA CLEAN SAFE — MAIN COMPLETO + ALMA YUL 🛟")
print("🛟 RC82 PREEXPERIENCIA CLEAN SAFE — CARPETAS BLINDADAS 🛟")
print("🛟 RC82 PREEXPERIENCIA CLEAN SAFE — /CREAR OK 🛟")
print("🛟 RC82 PREEXPERIENCIA CLEAN SAFE — TODO METIDO PARA REVISAR 🛟")
print("🛟 RC82 PREEXPERIENCIA CLEAN SAFE — YUL CUENTA LO QUE ESCRIBES 🛟")
print("🛟 RC82 PREEXPERIENCIA CLEAN SAFE — FORMULARIO SIMPLE + MAGIA 🛟")
print("🛟 RC82 PREEXPERIENCIA CLEAN SAFE — SOLO UN LUGAR 🛟")
print("🛟 RC82 PREEXPERIENCIA CLEAN SAFE — FORMULARIO LIMPIO 🛟")
print("🛟 RC82 PREEXPERIENCIA CLEAN SAFE — YUL NO BLOQUEA ETERNA 🛟")
print("🛟 RC82 PREEXPERIENCIA CLEAN SAFE — SMS + MASTER V1 🛟")
import html
import json
import mimetypes
import os
import secrets
import sqlite3
import traceback
import uuid
import hashlib
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from urllib.parse import quote

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
ADMIN_ALERT_PHONE = os.getenv("ADMIN_ALERT_PHONE", "").strip()

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

# RC60: controles seguros de estabilización.
# Por defecto NO caducamos enlaces para no romper pruebas actuales.
# Cuando lancemos público, poner ETERNA_LINK_EXPIRY_DAYS=30 y ETERNA_ENFORCE_LINK_EXPIRY=1.
ETERNA_LINK_EXPIRY_DAYS = int(os.getenv("ETERNA_LINK_EXPIRY_DAYS", "30"))
ETERNA_ENFORCE_LINK_EXPIRY = os.getenv("ETERNA_ENFORCE_LINK_EXPIRY", "0").strip().lower() in {"1", "true", "yes", "on"}

# RC60: sweep de rescate al arrancar Render. Seguro porque respeta locks, delivered y máximos de intentos.
ETERNA_STARTUP_SWEEP_ENABLED = os.getenv("ETERNA_STARTUP_SWEEP_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}


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
WHATSAPP_ENABLED = os.getenv("WHATSAPP_ENABLED", "1").strip() == "1"
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "").strip()

# Reacción móvil blindada:
# antes estaba limitado a 15MB y en móvil/Safari una emoción real puede superar ese tamaño.
# ETERNA_PRODUCCION_V1_RC1
# Base: MAIN SALVAVIDAS validado con SMS. Mejoras: pantallas cinematicas, CTA viral, rutas PNG blindadas.
# Si supera el límite, no se marca reaction_uploaded y por tanto NO vuelve el sender pack.
MAX_VIDEO_SIZE_MB = int(os.getenv("MAX_REACTION_VIDEO_MB", "100"))
MAX_VIDEO_SIZE = MAX_VIDEO_SIZE_MB * 1024 * 1024
ALLOWED_VIDEO_TYPES = {
    "video/webm",
    "video/mp4",
    "application/octet-stream",
}


# =========================================================
# RC75F — RUNTIME FOLDER RESCUE
# Si /data no existe o no tiene permisos, ETERNA no debe caerse al arrancar.
# Cae a ./data/<fallback> y deja log claro.
# =========================================================

def ensure_runtime_folder(path_value: str, fallback_name: str) -> Path:
    requested = Path(str(path_value or "").strip() or str(DATA_FOLDER / fallback_name))
    try:
        requested.mkdir(parents=True, exist_ok=True)
        return requested
    except Exception as e:
        fallback = DATA_FOLDER / fallback_name
        fallback.mkdir(parents=True, exist_ok=True)
        print(f"[WARN] Runtime folder fallback: {requested} -> {fallback} ({e})")
        return fallback

DATA_FOLDER = Path("data")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

VIDEO_FOLDER = Path("videos")
VIDEO_FOLDER.mkdir(parents=True, exist_ok=True)

REACTIONS_FOLDER = ensure_runtime_folder(os.getenv("REACTIONS_FOLDER", "/data/reactions"), "reactions")
REACTION_CHUNKS_FOLDER = ensure_runtime_folder(os.getenv("REACTION_CHUNKS_FOLDER", "/data/reaction_chunks"), "reaction_chunks")

STATIC_FOLDER = Path("static")
STATIC_FOLDER.mkdir(parents=True, exist_ok=True)

PHOTO_FOLDER = Path("uploads")
PHOTO_FOLDER.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_FOLDER / "eterna.db"

DELIVERY_WORKER_INTERVAL_SECONDS = int(os.getenv("DELIVERY_WORKER_INTERVAL_SECONDS", "15"))
DELIVERY_WORKER_ENABLED = os.getenv("DELIVERY_WORKER_ENABLED", "1").strip() != "0"
DELIVERY_WORKER_STARTED = False
DELIVERY_WORKER_LOCK = threading.Lock()

# =========================================================
# RC74 FULL — AUTONOMÍA OPERATIVA
# =========================================================
ETERNA_APP_VERSION = os.getenv("ETERNA_APP_VERSION", "RC82_PREEXPERIENCIA_CLEAN_SAFE").strip()
ETERNA_SAFE_MODE = os.getenv("ETERNA_SAFE_MODE", "0").strip().lower() in {"1", "true", "yes", "on"}
ETERNA_RECOVERY_WORKER_ENABLED = os.getenv("ETERNA_RECOVERY_WORKER_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
ETERNA_RENDER_QUEUE_ENABLED = os.getenv("ETERNA_RENDER_QUEUE_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
ETERNA_RENDER_STUCK_MINUTES = int(os.getenv("ETERNA_RENDER_STUCK_MINUTES", "25"))
ETERNA_RENDER_MAX_ATTEMPTS = int(os.getenv("ETERNA_RENDER_MAX_ATTEMPTS", "3"))
ETERNA_RENDER_QUEUE_BATCH_SIZE = int(os.getenv("ETERNA_RENDER_QUEUE_BATCH_SIZE", "1"))

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
# ETERNA VISUAL V1 — PANTALLAS CANÓNICAS
# =========================================================

ETERNA_VISUAL_VERSION = "eterna-visual-v74a-observability-plus-safe"
ETERNA_BG_BASE = "/static/eterna-cinematic/backgrounds"
ETERNA_BG_FOLDER = STATIC_FOLDER / "eterna-cinematic" / "backgrounds"

# Pantallas canónicas aprobadas.
# Las claves que no tienen PNG definitivo se redirigen a una pantalla buena para evitar 404.
ETERNA_SCREEN_ASSETS = {
    "landing": "home-mobile-v1.png",
    "home_mobile": "home-mobile-v1.png",
    "checkout_loading": "uploading-reaction-v1.png",
    "payment_success": "payment-success-v1.png",
    "intro_shhh": "ETERNA_INTRO_SHHH_PROD.png",
    "intro_shhh_legacy": "intro-shhh-v1.png",
    "sound_check": "sound-check-v1.png",
    "quiet_place": "eterna_lugar_tranquilo_final.png",
    "terms_acceptance": "terms-acceptance-v1.png",
    "consent_recording": "recording-consent-v1.png",
    "recording_consent": "recording-consent-v1.png",
    "uploading_reaction": "uploading-reaction-v1.png",
    "experience_complete": "experience-complete-v1.png",
    "gift_ready": "uploading-reaction-v1.png",
    "sender_pack_entry": "sender-pack-entry-v1.png",
    "recipient_gift": "recipient-gift-screen-v3.png",
    "sender_pack": "sender_pack_master_v1.png",
    "viral_cta": "viral-cta-v1.png",
    "error": "error-v1.png",
    "guide_butterfly": "ETERNA_GUIDE_BUTTERFLY_V1.png",
}

def _eterna_asset_key(value: str) -> str:
    raw = str(value or "").strip().replace("\\", "/").split("/")[-1].split("?")[0].strip().lower()
    raw = raw.replace("%20", " ")
    raw = raw.replace(".png.png", ".png")
    raw = raw.replace(".jpg.jpg", ".jpg")
    raw = raw.replace(".jpeg.jpeg", ".jpeg")
    raw = raw.replace(".webp.webp", ".webp")
    for suffix in [" (copy)", " copy", " copia", " - copia"]:
        raw = raw.replace(suffix, "")
    for n in range(1, 20):
        raw = raw.replace(f" ({n})", "")
        raw = raw.replace(f"({n})", "")
        raw = raw.replace(f"_{n}", "") if raw.endswith(f"_{n}") else raw
    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
        while raw.endswith(ext):
            raw = raw[:-len(ext)]
    return raw.strip(" ._- ")

def resolve_eterna_asset_filename(name: str, fallback: str = "error-v1.png") -> str:
    """
    Resuelve assets aunque Windows haya dejado nombres tipo:
    payment-success-v1.png (2).png, payment-success-v1.png.png o home-mobile-v1.png (2).
    Así evitamos pantallas negras e iconos rotos en producción.
    """
    requested = str(name or "").strip() or fallback
    if requested in ETERNA_SCREEN_ASSETS:
        requested = ETERNA_SCREEN_ASSETS[requested]

    direct_candidates = [requested]
    if not requested.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        direct_candidates.append(requested + ".png")

    # variantes típicas de Windows / copias / doble extensión
    expanded = []
    for c in direct_candidates:
        expanded.extend([
            c,
            c.replace(".png", ".png.png"),
            c.replace(".png", "(1).png"),
            c.replace(".png", "(2).png"),
            c.replace(".png", " (1).png"),
            c.replace(".png", " (2).png"),
            c + "(1)",
            c + " (1)",
            c + " (2)",
            c + ".png" if not c.endswith(".png") else c,
        ])

    for candidate in expanded:
        p = ETERNA_BG_FOLDER / candidate
        if p.exists() and p.is_file():
            return p.name

    requested_key = _eterna_asset_key(requested)
    try:
        if ETERNA_BG_FOLDER.exists():
            for p in ETERNA_BG_FOLDER.iterdir():
                if p.is_file() and _eterna_asset_key(p.name) == requested_key:
                    return p.name
    except Exception as e:
        print("⚠️ No pude resolver asset ETERNA:", requested, e)

    return requested

def eterna_asset(name: str) -> str:
    clean = resolve_eterna_asset_filename(name)
    return f"/eterna-assets/{quote(clean)}?v={quote(ETERNA_VISUAL_VERSION)}"

@app.get("/eterna-assets/{asset_name}")
def eterna_asset_file(asset_name: str):
    filename = resolve_eterna_asset_filename(asset_name)
    path = ETERNA_BG_FOLDER / filename
    if not path.exists() or not path.is_file():
        fallback = ETERNA_BG_FOLDER / resolve_eterna_asset_filename("error-v1.png")
        if fallback.exists() and fallback.is_file():
            return FileResponse(str(fallback), media_type="image/png")
        raise HTTPException(status_code=404, detail=f"Asset no encontrado: {asset_name}")
    return FileResponse(str(path), media_type=guess_media_type_from_path(str(path)))



@app.get("/favicon.ico")
def favicon_file():
    fallback = ETERNA_BG_FOLDER / resolve_eterna_asset_filename("home-mobile-v1.png")
    if fallback.exists() and fallback.is_file():
        return FileResponse(str(fallback), media_type="image/png")
    raise HTTPException(status_code=404, detail="favicon no disponible")

@app.get("/apple-touch-icon.png")
def apple_touch_icon_file():
    fallback = ETERNA_BG_FOLDER / resolve_eterna_asset_filename("home-mobile-v1.png")
    if fallback.exists() and fallback.is_file():
        return FileResponse(str(fallback), media_type="image/png")
    raise HTTPException(status_code=404, detail="apple touch icon no disponible")

# =========================================================
# ETERNA VISUAL V1 — RENDER ÚNICO LIMPIO Y BLINDADO
# =========================================================

def render_eterna_image_screen(
    image_name: str,
    fallback_image_name: str = "error-v1.png",
    overlay_kind: str = "soft",
    redirect_url: str = "",
    redirect_delay_ms: int = 0,
    button_url: str = "",
    button_label: str = "",
    extra_note: str = "",
    form_action: str = "",
    form_method: str = "post",
    hidden_fields: Optional[dict] = None,
    button_id: str = "",
    extra_script: str = "",
) -> HTMLResponse:
    """
    Renderizador único para pantallas V1 de ETERNA.
    Solo cambia capa visual. No toca Stripe, Twilio, SMS, webhook, DB, Video Engine,
    reacción, workers ni sender pack dinámico.
    """
    clean_image = str(image_name or "").strip() or "error-v1.png"
    clean_fallback = str(fallback_image_name or "error-v1.png").strip() or "error-v1.png"

    # Permite usar clave lógica (intro_shhh) o nombre real (intro-shhh-v1.png).
    if clean_image in ETERNA_SCREEN_ASSETS:
        clean_image = ETERNA_SCREEN_ASSETS[clean_image]
    if clean_fallback in ETERNA_SCREEN_ASSETS:
        clean_fallback = ETERNA_SCREEN_ASSETS[clean_fallback]

    image_src = safe_attr(eterna_asset(clean_image))
    fallback_src = safe_attr(eterna_asset(clean_fallback))
    yul_src = safe_attr(eterna_asset("guide_butterfly"))

    is_terms_screen = _eterna_asset_key(clean_image) == _eterna_asset_key("terms-acceptance-v1.png")
    is_payment_success_screen = _eterna_asset_key(clean_image) == _eterna_asset_key("payment-success-v1.png")
    is_quiet_screen = _eterna_asset_key(clean_image) in {_eterna_asset_key("quiet-place-v1.png"), _eterna_asset_key("eterna_lugar_tranquilo_final.png"), _eterna_asset_key("quiet-place-v2.png")}
    is_intro_screen = _eterna_asset_key(clean_image) in {_eterna_asset_key("intro-shhh-v1.png"), _eterna_asset_key("ETERNA_INTRO_SHHH_PROD.png")}
    is_recording_consent_screen = _eterna_asset_key(clean_image) == _eterna_asset_key("recording-consent-v1.png")
    is_sound_screen = _eterna_asset_key(clean_image) == _eterna_asset_key("sound-check-v1.png")
    is_uploading_screen = _eterna_asset_key(clean_image) == _eterna_asset_key("uploading-reaction-v1.png")
    is_complete_screen = _eterna_asset_key(clean_image) == _eterna_asset_key("experience-complete-v1.png")
    is_sender_entry_screen = _eterna_asset_key(clean_image) == _eterna_asset_key("sender-pack-entry-v1.png")
    is_sender_pack_screen = _eterna_asset_key(clean_image) in {_eterna_asset_key("sender-pack-v1.png"), _eterna_asset_key("sender-pack-v2.png"), _eterna_asset_key("sender_pack_master_v1.png")}
    is_viral_screen = _eterna_asset_key(clean_image) == _eterna_asset_key("viral-cta-v1.png")

    note_html = ""
    if extra_note:
        note_html = f'<div class="extra-note">{safe_text(extra_note)}</div>'

    redirect_script = ""
    if redirect_url and int(redirect_delay_ms or 0) > 0:
        redirect_script = f"""
        <script>
        window.setTimeout(function() {{ window.location.replace({json.dumps(str(redirect_url))}); }}, {int(redirect_delay_ms)});
        </script>
        """

    action_html = ""
    if form_action:
        hidden_html = ""
        for k, v in (hidden_fields or {}).items():
            hidden_html += f'<input type="hidden" name="{safe_attr(k)}" value="{safe_attr(v)}">'
        btn_id = f' id="{safe_attr(button_id)}"' if button_id else ""
        action_html = f"""
        <form class="visual-action-form" method="{safe_attr(form_method or 'post')}" action="{safe_attr(form_action)}">
            {hidden_html}
            <button class="real-button"{btn_id} type="submit">{safe_text(button_label or 'Continuar')}</button>
        </form>
        """
    elif button_url and button_label:
        if is_terms_screen or is_recording_consent_screen:
            check_id = "recordingConsentCheck" if is_recording_consent_screen else "termsRealCheck"
            btn_id = "recordingConsentContinueButton" if is_recording_consent_screen else "termsContinueButton"
            wrapper_class = "recording-consent-real-check" if is_recording_consent_screen else "terms-real-check"
            disabled_class = "recording-consent-continue" if is_recording_consent_screen else "terms-continue"
            aria_label = "Acepto la grabación de mi reacción" if is_recording_consent_screen else "He leído y acepto los términos"
            action_html = f"""
            <div class="{wrapper_class}">
                <input id="{check_id}" type="checkbox" aria-label="{aria_label}">
                <label for="{check_id}"><span></span></label>
            </div>
            <a class="real-button {disabled_class} is-disabled" id="{btn_id}" href="{safe_attr(button_url)}" aria-label="{safe_attr(button_label)}">{safe_text(button_label)}</a>
            <script>
            (function() {{
                const check = document.getElementById('{check_id}');
                const btn = document.getElementById('{btn_id}');
                if (!check || !btn) return;
                function sync() {{
                    if (check.checked) {{
                        btn.classList.remove('is-disabled');
                        btn.classList.add('is-ready');
                    }} else {{
                        btn.classList.add('is-disabled');
                        btn.classList.remove('is-ready');
                    }}
                }}
                btn.addEventListener('click', function(e) {{
                    if (!check.checked) {{
                        e.preventDefault();
                        const box = document.querySelector('.{wrapper_class}');
                        if (box) {{
                            box.classList.remove('needs-attention');
                            void box.offsetWidth;
                            box.classList.add('needs-attention');
                        }}
                    }}
                }});
                check.addEventListener('change', sync);
                sync();
            }})();
            </script>
            """
        else:
            action_html = f'<a class="real-button" href="{safe_attr(button_url)}" aria-label="{safe_attr(button_label)}">{safe_text(button_label)}</a>'

    loading_layers = ""
    screen_mode_class = " loading-mode" if overlay_kind == "loading" else ""
    if is_terms_screen:
        screen_mode_class += " terms-mode"
    if is_recording_consent_screen:
        screen_mode_class += " consent-mode"
    if is_payment_success_screen:
        screen_mode_class += " payment-success-mode"
    if is_quiet_screen:
        screen_mode_class += " quiet-mode"
    if is_intro_screen:
        screen_mode_class += " intro-mode"
    if is_sound_screen:
        screen_mode_class += " sound-mode"
    if is_uploading_screen:
        screen_mode_class += " uploading-mode"
    if is_complete_screen:
        screen_mode_class += " complete-mode"
    if is_sender_entry_screen:
        screen_mode_class += " sender-entry-mode"
    if is_sender_pack_screen:
        screen_mode_class += " sender-pack-bg-mode"
    if is_viral_screen:
        screen_mode_class += " viral-mode"
    if overlay_kind == "loading":
        loading_layers = """
        <div class="magic-line" aria-hidden="true"><span></span><b></b></div>
        <div class="line-spark-runner" aria-hidden="true"></div>
        <div class="blue-orb" aria-hidden="true"></div>
        <div class="water-shimmer" aria-hidden="true"></div>
        <div class="sun-glow" aria-hidden="true"></div>
        <div class="eterna-ring" aria-hidden="true"><span></span></div>
        <i class="loading-spark ls1" aria-hidden="true"></i>
        <i class="loading-spark ls2" aria-hidden="true"></i>
        <i class="loading-spark ls3" aria-hidden="true"></i>
        <i class="loading-spark ls4" aria-hidden="true"></i>
        <i class="loading-spark ls5" aria-hidden="true"></i>
        """

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>ETERNA</title>
<meta name="theme-color" content="#02050a">
<style>
    * {{ box-sizing:border-box; -webkit-tap-highlight-color:transparent; }}
    html, body {{ margin:0; width:100%; min-height:100%; background:#02050a; }}
    body {{ min-height:100svh; overflow-x:hidden; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif; background:#02050a; }}
    .screen {{ position:relative; width:100vw; min-height:100svh; min-height:100dvh; display:flex; align-items:stretch; justify-content:center; background:#02050a; overflow:hidden; }}
    .phone {{ position:relative; width:100vw; max-width:none; min-height:100svh; min-height:100dvh; overflow:hidden; background:#02050a; }}
    .img {{ position:absolute; inset:0; width:100%; height:100%; min-height:100svh; min-height:100dvh; display:block; object-fit:cover; object-position:center center; background:#02050a; }}
    @media (min-width: 760px) {{ .phone {{ width:min(100vw,520px); }} .img {{ object-fit:cover; }} }}
    .soft-halo {{ position:absolute; left:67%; top:22%; width:240px; height:240px; border-radius:999px; transform:translate(-50%,-50%); background:radial-gradient(circle, rgba(34,178,255,.26), rgba(34,178,255,.07) 42%, transparent 70%); filter:blur(16px); opacity:.56; mix-blend-mode:screen; animation:haloBreath 5.6s ease-in-out infinite; pointer-events:none; }}
    .particle {{ position:absolute; width:5px; height:5px; border-radius:50%; background:#62d3ff; box-shadow:0 0 16px #62d3ff, 0 0 34px rgba(98,211,255,.55); opacity:0; animation:floatUp 9s linear infinite; pointer-events:none; }}
    .particle.gold {{ background:#ffd98b; box-shadow:0 0 16px #ffd98b,0 0 34px rgba(255,217,139,.48); }}
    .p1 {{ left:18%; bottom:16%; animation-delay:.4s; }} .p2 {{ left:78%; bottom:18%; animation-delay:1.6s; transform:scale(.72); }} .p3 {{ left:54%; bottom:9%; animation-delay:3.8s; transform:scale(.55); }} .p4 {{ left:38%; bottom:36%; animation-delay:5.2s; transform:scale(.6); }}
    @keyframes haloBreath {{ 0%,100% {{ transform:translate(-50%,-50%) scale(.94); opacity:.34; }} 50% {{ transform:translate(-50%,-50%) scale(1.10); opacity:.72; }} }}
    @keyframes floatUp {{ 0% {{ transform:translateY(0) scale(.6); opacity:0; }} 14% {{ opacity:.95; }} 72% {{ opacity:.36; }} 100% {{ transform:translateY(-150px) scale(1.1); opacity:0; }} }}
    .magic-line {{ position:absolute; left:8%; right:8%; top:56.8%; height:16px; border-radius:999px; pointer-events:none; overflow:hidden; mix-blend-mode:screen; }}
    .magic-line span {{ position:absolute; left:0; top:6px; height:4px; width:100%; border-radius:999px; background:linear-gradient(90deg, rgba(47,195,255,.08), rgba(52,204,255,.95), rgba(255,216,132,.32), rgba(255,216,132,.08)); box-shadow:0 0 18px rgba(45,195,255,.78),0 0 42px rgba(45,195,255,.42); animation:linePulse 1.7s ease-in-out infinite; }}
    .magic-line b {{ position:absolute; top:1px; left:-12%; width:66px; height:14px; border-radius:999px; background:radial-gradient(circle, #fff, #5cd6ff 33%, transparent 70%); filter:blur(1px); box-shadow:0 0 24px #5cd6ff; animation:runner 2.2s cubic-bezier(.42,0,.24,1) infinite; }}
    .line-spark-runner {{ position:absolute; left:8%; top:55.9%; width:76px; height:2px; border-radius:999px; background:linear-gradient(90deg, transparent, rgba(255,255,255,.95), rgba(67,211,255,.88), transparent); box-shadow:0 0 18px rgba(75,210,255,.95),0 0 42px rgba(255,212,120,.42); animation:lightRunner 2.2s cubic-bezier(.42,0,.24,1) infinite; pointer-events:none; mix-blend-mode:screen; }}
    .blue-orb {{ position:absolute; left:50%; top:56.8%; width:58px; height:58px; border-radius:999px; transform:translate(-50%,-50%); background:radial-gradient(circle, rgba(255,255,255,.95), rgba(56,205,255,.62) 24%, transparent 72%); filter:blur(2px); opacity:.88; mix-blend-mode:screen; animation:orbBeat 1.6s ease-in-out infinite; pointer-events:none; }}
    @keyframes linePulse {{ 0%,100% {{ opacity:.70; filter:brightness(1); }} 50% {{ opacity:1; filter:brightness(1.55); }} }}
    @keyframes runner {{ 0% {{ left:-12%; opacity:0; }} 10% {{ opacity:1; }} 82% {{ opacity:1; }} 100% {{ left:104%; opacity:0; }} }}
    @keyframes butterflyRun {{ 0% {{ left:8%; transform:translateY(2px) scale(.82); opacity:.2; }} 12% {{ opacity:1; }} 50% {{ transform:translateY(-10px) scale(1.02); }} 88% {{ opacity:1; }} 100% {{ left:86%; transform:translateY(3px) scale(.9); opacity:0; }} }}

    .edge-glow {{ position:absolute; pointer-events:none; mix-blend-mode:screen; opacity:.0; }}
    .eg1 {{ left:-18%; top:18%; width:72%; height:42%; border-radius:999px; border:1px solid rgba(58,201,255,.16); box-shadow:0 0 24px rgba(58,201,255,.22), inset 0 0 28px rgba(58,201,255,.10); transform:rotate(-18deg); animation:edgeGlowOne 7.4s ease-in-out infinite; }}
    .eg2 {{ right:-24%; bottom:12%; width:78%; height:46%; border-radius:999px; border:1px solid rgba(255,207,113,.13); box-shadow:0 0 28px rgba(255,194,90,.18), inset 0 0 28px rgba(255,194,90,.08); transform:rotate(21deg); animation:edgeGlowTwo 8.2s ease-in-out infinite; }}
    .star-run {{ position:absolute; width:110px; height:2px; border-radius:999px; background:linear-gradient(90deg, transparent, rgba(255,255,255,.94), rgba(255,213,121,.88), transparent); box-shadow:0 0 18px rgba(255,221,143,.72),0 0 36px rgba(74,204,255,.28); opacity:0; pointer-events:none; mix-blend-mode:screen; }}
    .sr1 {{ left:10%; top:30%; animation:starRunOne 5.8s ease-in-out infinite; }}
    .sr2 {{ right:7%; bottom:23%; animation:starRunTwo 6.6s ease-in-out infinite 1.4s; }}
    @keyframes edgeGlowOne {{ 0%,100% {{ opacity:.02; transform:rotate(-18deg) scale(.96); }} 48% {{ opacity:.26; transform:rotate(-14deg) scale(1.04); }} }}
    @keyframes edgeGlowTwo {{ 0%,100% {{ opacity:.02; transform:rotate(21deg) scale(.96); }} 52% {{ opacity:.22; transform:rotate(17deg) scale(1.06); }} }}
    @keyframes starRunOne {{ 0% {{ transform:translateX(-80px) scaleX(.65); opacity:0; }} 14% {{ opacity:.76; }} 48% {{ opacity:.42; }} 100% {{ transform:translateX(360px) scaleX(1.25); opacity:0; }} }}
    @keyframes starRunTwo {{ 0% {{ transform:translateX(100px) scaleX(.65); opacity:0; }} 14% {{ opacity:.62; }} 48% {{ opacity:.34; }} 100% {{ transform:translateX(-360px) scaleX(1.2); opacity:0; }} }}
    @keyframes lightRunner {{ 0% {{ left:8%; opacity:0; transform:translateY(1px) scaleX(.55); }} 10% {{ opacity:1; }} 55% {{ opacity:.98; transform:translateY(-6px) scaleX(1); }} 100% {{ left:86%; opacity:0; transform:translateY(2px) scaleX(.45); }} }}

    @keyframes orbBeat {{ 0%,100% {{ transform:translate(-50%,-50%) scale(.92); opacity:.48; }} 50% {{ transform:translate(-50%,-50%) scale(1.16); opacity:.95; }} }}
    .real-button {{ position:absolute; left:7.5%; right:7.5%; bottom:calc(env(safe-area-inset-bottom) + 54px); min-height:76px; border:0; border-radius:22px; display:block; z-index:8; color:transparent; text-indent:-9999px; overflow:hidden; background:rgba(255,255,255,.001); cursor:pointer; touch-action:manipulation; }}
    .real-button::after {{ content:""; position:absolute; inset:0; border-radius:inherit; background:linear-gradient(90deg,rgba(255,242,186,.10),rgba(255,179,55,.16)); box-shadow:0 0 30px rgba(255,189,75,.22); opacity:.0; animation:ctaBreath 2.8s ease-in-out infinite; }}
    @keyframes ctaBreath {{ 0%,100% {{ opacity:.04; transform:scale(.985); }} 50% {{ opacity:.22; transform:scale(1.01); }} }}
    .visual-action-form {{ position:absolute; left:0; right:0; bottom:0; z-index:8; }}
    .extra-note {{ position:absolute; left:8%; right:8%; bottom:calc(env(safe-area-inset-bottom) + 18px); z-index:7; text-align:center; color:rgba(255,245,220,.72); font-size:12px; line-height:1.35; text-shadow:0 0 14px rgba(0,0,0,.9); }}

    /* RC19 — pantalla transición post-formulario: foto completa y línea azul alineada */
    .screen.loading-mode .phone {{ max-width:520px; }}
    .screen.loading-mode .img {{ object-fit:contain; object-position:center center; background:radial-gradient(circle at 50% 62%, rgba(26,117,219,.22), transparent 36%), #02050a; }}
    .screen.loading-mode .soft-halo {{ left:50%; top:54%; width:320px; height:320px; opacity:.42; }}
    .screen.loading-mode .magic-line {{ left:18.2%; right:18.2%; top:64.15%; height:18px; border-radius:999px; }}
    .screen.loading-mode .magic-line span {{ top:7px; height:3px; background:linear-gradient(90deg, rgba(37,122,255,.15), rgba(51,196,255,.96), rgba(255,220,139,.44), rgba(51,196,255,.30)); box-shadow:0 0 22px rgba(53,203,255,.88),0 0 46px rgba(43,149,255,.45); }}
    .screen.loading-mode .magic-line b {{ top:1px; width:74px; height:16px; }}
    .screen.loading-mode .line-spark-runner {{ left:18.2%; top:64.75%; width:90px; height:2px; }}
    .screen.loading-mode .blue-orb {{ left:50%; top:64.85%; width:52px; height:52px; opacity:.72; }}
    .screen.loading-mode .sr1, .screen.loading-mode .sr2 {{ display:none; }}
    .screen.loading-mode .edge-glow.eg1 {{ left:-20%; top:28%; opacity:.10; }}
    .screen.loading-mode .edge-glow.eg2 {{ right:-28%; bottom:16%; opacity:.10; }}


    /* RC22 — POST FORMULARIO: energía cinematográfica exagerada, no técnica */
    /* Objetivo: primero aparece la escena; después despierta la magia. */
    .screen.loading-mode .img {{
        opacity:0;
        animation:loadingImageReveal 1.05s ease-out forwards;
        filter:contrast(1.05) saturate(1.08) brightness(1.04);
    }}

    .screen.loading-mode .phone::before {{
        content:"";
        position:absolute;
        inset:-12%;
        pointer-events:none;
        z-index:3;
        opacity:0;
        mix-blend-mode:screen;
        background:
            radial-gradient(circle at 50% 39%, rgba(118,222,255,.42), transparent 10%),
            radial-gradient(circle at 38% 43%, rgba(255,226,148,.30), transparent 12%),
            radial-gradient(circle at 62% 42%, rgba(255,226,148,.28), transparent 12%),
            radial-gradient(circle at 50% 66%, rgba(61,207,255,.22), transparent 22%),
            radial-gradient(circle at 50% 78%, rgba(255,205,105,.20), transparent 18%);
        filter:blur(10px);
        animation:energyWake 5.8s ease-in-out 1.0s infinite;
    }}

    .screen.loading-mode .phone::after {{
        content:"";
        position:absolute;
        inset:0;
        pointer-events:none;
        z-index:7;
        opacity:0;
        mix-blend-mode:screen;
        background:
            linear-gradient(115deg, transparent 0%, transparent 34%, rgba(255,255,255,.60) 38%, rgba(98,218,255,.34) 41%, transparent 47%, transparent 100%),
            linear-gradient(65deg, transparent 0%, transparent 56%, rgba(255,222,135,.48) 59%, rgba(255,255,255,.42) 61%, transparent 66%, transparent 100%);
        transform:translateX(-70%) skewX(-10deg);
        animation:bigCinematicFlares 4.9s cubic-bezier(.2,.7,.15,1) 1.65s infinite;
    }}

    .screen.loading-mode .soft-halo {{
        left:50%; top:43.5%; width:410px; height:410px;
        opacity:0;
        background:radial-gradient(circle, rgba(80,216,255,.42), rgba(42,153,255,.16) 40%, transparent 72%);
        filter:blur(18px);
        animation:butterflyHaloPower 3.8s ease-in-out 1.0s infinite;
        z-index:2;
    }}

    /* Línea energética: retrasada, más lenta y más baja para cruzar el eje de la mariposa */
    .screen.loading-mode .magic-line {{
        left:16.2%; right:16.2%; top:66.35%; height:22px;
        opacity:0;
        z-index:6;
        animation:lineWakeDelay .45s ease-out 1.05s forwards;
    }}
    .screen.loading-mode .magic-line span {{
        top:9px; height:4px;
        background:linear-gradient(90deg, rgba(37,122,255,.04), rgba(58,212,255,1), rgba(255,255,255,.96), rgba(255,218,129,.78), rgba(58,212,255,.40), rgba(37,122,255,.04));
        box-shadow:0 0 26px rgba(53,203,255,1),0 0 58px rgba(43,149,255,.62),0 0 34px rgba(255,213,126,.44);
        animation:linePulsePower 2.7s ease-in-out 1.05s infinite;
    }}
    .screen.loading-mode .magic-line b {{
        top:0px; width:98px; height:20px;
        background:radial-gradient(circle, #fff, #75e5ff 28%, rgba(255,218,126,.78) 47%, transparent 74%);
        filter:blur(1px);
        box-shadow:0 0 32px #75e5ff,0 0 68px rgba(255,211,118,.58);
        animation:runnerPower 3.65s cubic-bezier(.23,.72,.18,1) 1.10s infinite;
    }}
    .screen.loading-mode .line-spark-runner {{
        left:16.2%; top:67.05%; width:116px; height:3px;
        opacity:0;
        z-index:7;
        background:linear-gradient(90deg, transparent, rgba(255,255,255,1), rgba(73,219,255,1), rgba(255,218,125,.88), transparent);
        box-shadow:0 0 26px rgba(75,210,255,1),0 0 60px rgba(255,212,120,.62);
        animation:lightRunnerPower 3.65s cubic-bezier(.23,.72,.18,1) 1.10s infinite;
    }}
    .screen.loading-mode .blue-orb {{
        left:50%; top:67.0%; width:76px; height:76px;
        opacity:0;
        z-index:5;
        background:radial-gradient(circle, rgba(255,255,255,1), rgba(82,219,255,.78) 24%, rgba(255,218,126,.30) 46%, transparent 74%);
        filter:blur(2px);
        animation:orbBeatPower 2.35s ease-in-out 1.05s infinite;
    }}

    .screen.loading-mode .water-shimmer {{
        position:absolute; left:5%; right:5%; bottom:11.7%; height:22%;
        border-radius:999px;
        background:linear-gradient(90deg, transparent, rgba(86,207,255,.18), rgba(255,214,126,.22), rgba(86,207,255,.16), transparent);
        filter:blur(12px);
        opacity:0;
        mix-blend-mode:screen;
        animation:waterMovePower 5.9s ease-in-out 1.15s infinite;
        pointer-events:none;
        z-index:2;
    }}
    .screen.loading-mode .sun-glow {{
        position:absolute; left:50%; bottom:17.2%; width:280px; height:155px;
        transform:translateX(-50%);
        border-radius:999px;
        background:radial-gradient(circle, rgba(255,238,174,.58), rgba(255,168,58,.25) 42%, transparent 74%);
        filter:blur(14px);
        opacity:0;
        mix-blend-mode:screen;
        animation:sunBreathPower 4.4s ease-in-out 1.0s infinite;
        pointer-events:none;
        z-index:2;
    }}
    .screen.loading-mode .eterna-ring {{
        position:absolute; left:50%; top:39.9%; width:126px; height:126px;
        transform:translate(-50%,-50%);
        border-radius:999px;
        border:1px solid rgba(255,230,159,.58);
        box-shadow:0 0 36px rgba(255,203,102,.54), inset 0 0 28px rgba(77,204,255,.26), 0 0 74px rgba(65,210,255,.25);
        opacity:0;
        animation:ringRotatePower 7.8s linear 1.0s infinite, ringWake .5s ease-out 1.0s forwards;
        pointer-events:none;
        z-index:5;
        mix-blend-mode:screen;
    }}
    .screen.loading-mode .eterna-ring span {{
        position:absolute; right:-5px; top:52px; width:13px; height:13px;
        border-radius:999px;
        background:#fff7d0;
        box-shadow:0 0 22px #fff7d0, 0 0 46px rgba(255,207,98,1);
    }}

    /* Destellos exagerados alrededor de alas y línea */
    .screen.loading-mode .loading-spark {{
        position:absolute; width:5px; height:5px; border-radius:999px;
        background:#ffd98a;
        box-shadow:0 0 18px #ffd98a,0 0 38px rgba(255,217,138,.72);
        opacity:0;
        pointer-events:none;
        z-index:8;
        animation:loadingSparkFloatPower 4.8s linear 1.1s infinite;
    }}
    .screen.loading-mode .ls1 {{ left:23%; top:37%; animation-delay:1.10s; }}
    .screen.loading-mode .ls2 {{ left:73%; top:39%; animation-delay:1.36s; background:#70dcff; box-shadow:0 0 18px #70dcff,0 0 38px rgba(112,220,255,.76); }}
    .screen.loading-mode .ls3 {{ left:61%; top:52%; animation-delay:1.72s; }}
    .screen.loading-mode .ls4 {{ left:32%; top:54%; animation-delay:2.08s; background:#74dfff; box-shadow:0 0 18px #74dfff,0 0 38px rgba(116,223,255,.76); }}
    .screen.loading-mode .ls5 {{ left:78%; top:65%; animation-delay:2.44s; }}

    .screen.loading-mode .edge-glow.eg1 {{
        left:-16%; top:28%; width:82%; height:45%;
        border-color:rgba(69,213,255,.28);
        box-shadow:0 0 36px rgba(58,201,255,.42), inset 0 0 44px rgba(58,201,255,.18);
        opacity:0;
        animation:edgeGlowOnePower 5.8s ease-in-out 1.2s infinite;
        z-index:4;
    }}
    .screen.loading-mode .edge-glow.eg2 {{
        right:-18%; bottom:12%; width:86%; height:48%;
        border-color:rgba(255,213,126,.24);
        box-shadow:0 0 42px rgba(255,194,90,.36), inset 0 0 42px rgba(255,194,90,.16);
        opacity:0;
        animation:edgeGlowTwoPower 6.1s ease-in-out 1.45s infinite;
        z-index:4;
    }}
    .screen.loading-mode .star-run.sr1 {{
        display:block; left:2%; top:36%; width:150px; height:3px;
        opacity:0; z-index:9;
        animation:starRunOnePower 4.6s ease-in-out 1.75s infinite;
    }}
    .screen.loading-mode .star-run.sr2 {{
        display:block; right:0%; bottom:31%; width:150px; height:3px;
        opacity:0; z-index:9;
        animation:starRunTwoPower 5.0s ease-in-out 2.35s infinite;
    }}

    @keyframes loadingImageReveal {{ 0% {{ opacity:0; transform:scale(1.012); filter:brightness(.42) blur(2px); }} 100% {{ opacity:1; transform:scale(1); filter:contrast(1.05) saturate(1.08) brightness(1.04) blur(0); }} }}
    @keyframes lineWakeDelay {{ from {{ opacity:0; transform:translateY(8px); }} to {{ opacity:1; transform:translateY(0); }} }}
    @keyframes energyWake {{ 0%,100% {{ opacity:.44; transform:scale(.95); }} 45% {{ opacity:1; transform:scale(1.06); }} 70% {{ opacity:.72; transform:scale(1.01); }} }}
    @keyframes bigCinematicFlares {{ 0% {{ opacity:0; transform:translateX(-78%) skewX(-10deg); }} 13% {{ opacity:.0; }} 24% {{ opacity:.85; }} 48% {{ opacity:.42; }} 100% {{ opacity:0; transform:translateX(72%) skewX(-10deg); }} }}
    @keyframes butterflyHaloPower {{ 0%,100% {{ transform:translate(-50%,-50%) scale(.84); opacity:.34; }} 42% {{ transform:translate(-50%,-50%) scale(1.16); opacity:.96; }} 70% {{ opacity:.58; }} }}
    @keyframes linePulsePower {{ 0%,100% {{ opacity:.76; filter:brightness(1); }} 35% {{ opacity:1; filter:brightness(2.25); }} 68% {{ opacity:.92; filter:brightness(1.45); }} }}
    @keyframes runnerPower {{ 0% {{ left:-20%; opacity:0; transform:scaleX(.55); }} 12% {{ opacity:1; }} 76% {{ opacity:1; }} 100% {{ left:110%; opacity:0; transform:scaleX(.72); }} }}
    @keyframes lightRunnerPower {{ 0% {{ left:16.2%; opacity:0; transform:translateY(1px) scaleX(.55); }} 12% {{ opacity:1; }} 52% {{ opacity:1; transform:translateY(-8px) scaleX(1.10); }} 100% {{ left:84%; opacity:0; transform:translateY(2px) scaleX(.50); }} }}
    @keyframes orbBeatPower {{ 0%,100% {{ transform:translate(-50%,-50%) scale(.78); opacity:.30; }} 36% {{ transform:translate(-50%,-50%) scale(1.25); opacity:1; }} 68% {{ opacity:.58; }} }}
    @keyframes waterMovePower {{ 0%,100% {{ transform:translateX(-16px) scaleX(.94); opacity:.34; }} 45% {{ transform:translateX(18px) scaleX(1.08); opacity:.86; }} 72% {{ opacity:.58; }} }}
    @keyframes sunBreathPower {{ 0%,100% {{ transform:translateX(-50%) scale(.82); opacity:.30; }} 42% {{ transform:translateX(-50%) scale(1.18); opacity:.90; }} }}
    @keyframes ringWake {{ from {{ opacity:0; }} to {{ opacity:.92; }} }}
    @keyframes ringRotatePower {{ from {{ transform:translate(-50%,-50%) rotate(0deg); }} to {{ transform:translate(-50%,-50%) rotate(360deg); }} }}
    @keyframes loadingSparkFloatPower {{ 0% {{ opacity:0; transform:translateY(0) translateX(0) scale(.45); }} 12% {{ opacity:1; }} 36% {{ opacity:.94; transform:translateY(-32px) translateX(12px) scale(1.18); }} 72% {{ opacity:.52; }} 100% {{ opacity:0; transform:translateY(-118px) translateX(30px) scale(1.42); }} }}
    @keyframes edgeGlowOnePower {{ 0%,100% {{ opacity:.06; transform:rotate(-18deg) scale(.94); }} 46% {{ opacity:.56; transform:rotate(-13deg) scale(1.08); }} }}
    @keyframes edgeGlowTwoPower {{ 0%,100% {{ opacity:.05; transform:rotate(21deg) scale(.94); }} 52% {{ opacity:.48; transform:rotate(16deg) scale(1.09); }} }}
    @keyframes starRunOnePower {{ 0% {{ transform:translateX(-120px) translateY(12px) scaleX(.55); opacity:0; }} 14% {{ opacity:.95; }} 42% {{ opacity:.68; }} 100% {{ transform:translateX(430px) translateY(-18px) scaleX(1.32); opacity:0; }} }}
    @keyframes starRunTwoPower {{ 0% {{ transform:translateX(130px) translateY(-8px) scaleX(.55); opacity:0; }} 14% {{ opacity:.90; }} 42% {{ opacity:.58; }} 100% {{ transform:translateX(-430px) translateY(18px) scaleX(1.28); opacity:0; }} }}



    /* RC23 — VIDA PREMIUM GENERAL: más cine sin tocar lógica */
    .screen.payment-success-mode .phone::before {{
        content:"";
        position:absolute;
        left:50%; top:61%; width:360px; height:360px;
        transform:translate(-50%,-50%);
        border-radius:999px;
        pointer-events:none;
        z-index:3;
        opacity:.88;
        mix-blend-mode:screen;
        background:
            radial-gradient(circle, rgba(255,255,255,.95) 0%, rgba(255,230,150,.78) 5%, rgba(255,183,52,.55) 14%, rgba(255,183,52,.22) 30%, transparent 58%),
            conic-gradient(from 0deg, transparent, rgba(255,219,130,.50), transparent, rgba(255,244,190,.72), transparent);
        filter:blur(8px);
        animation:paymentHeartMegaPulse 1.55s ease-in-out infinite;
    }}
    .screen.payment-success-mode .phone::after {{
        content:"";
        position:absolute;
        left:50%; top:61%; width:410px; height:410px;
        transform:translate(-50%,-50%);
        pointer-events:none;
        z-index:4;
        opacity:.80;
        mix-blend-mode:screen;
        background:
            repeating-conic-gradient(from 8deg, rgba(255,224,137,.0) 0deg, rgba(255,224,137,.0) 9deg, rgba(255,237,178,.48) 10deg, rgba(255,174,41,.0) 12deg),
            radial-gradient(circle, transparent 0 18%, rgba(255,210,92,.38) 19%, transparent 21%, transparent 31%, rgba(255,221,132,.30) 32%, transparent 35%, transparent 47%, rgba(255,244,186,.22) 48%, transparent 50%);
        filter:drop-shadow(0 0 24px rgba(255,198,68,.78));
        animation:paymentGoldenExplosion 4.2s ease-in-out infinite;
    }}
    .screen.payment-success-mode .soft-halo {{
        left:50%; top:61%; width:430px; height:430px;
        background:radial-gradient(circle, rgba(255,210,92,.50), rgba(255,162,31,.20) 34%, rgba(54,195,255,.15) 52%, transparent 75%);
        filter:blur(20px);
        opacity:.88;
        animation:paymentHaloBreathe 2.0s ease-in-out infinite;
        z-index:2;
    }}
    .screen.payment-success-mode .edge-glow.eg1 {{
        left:-22%; top:22%; width:94%; height:52%;
        border-color:rgba(255,219,126,.26);
        box-shadow:0 0 42px rgba(255,199,76,.36), inset 0 0 44px rgba(255,199,76,.14);
        animation:paymentSideGlow 4.8s ease-in-out infinite;
        opacity:.32;
    }}
    .screen.payment-success-mode .edge-glow.eg2 {{
        right:-24%; bottom:9%; width:96%; height:52%;
        border-color:rgba(61,203,255,.24);
        box-shadow:0 0 42px rgba(61,203,255,.34), inset 0 0 44px rgba(61,203,255,.12);
        animation:paymentSideGlowTwo 5.4s ease-in-out .6s infinite;
        opacity:.28;
    }}
    .screen.payment-success-mode .star-run.sr1 {{
        left:0%; top:54%; width:190px; height:3px; z-index:8;
        animation:paymentStarSweep 3.4s ease-in-out .25s infinite;
    }}
    .screen.payment-success-mode .star-run.sr2 {{
        right:0%; bottom:28%; width:180px; height:3px; z-index:8;
        animation:paymentStarSweepBack 3.8s ease-in-out 1.0s infinite;
    }}
    .screen.payment-success-mode .particle {{ width:7px; height:7px; animation-duration:6.8s; }}
    .screen.payment-success-mode .particle.gold {{ width:8px; height:8px; }}

    @keyframes paymentHeartMegaPulse {{
        0%,100% {{ transform:translate(-50%,-50%) scale(.86); opacity:.52; filter:blur(10px) brightness(1); }}
        28% {{ transform:translate(-50%,-50%) scale(1.16); opacity:1; filter:blur(6px) brightness(1.85); }}
        42% {{ transform:translate(-50%,-50%) scale(.98); opacity:.76; }}
        62% {{ transform:translate(-50%,-50%) scale(1.08); opacity:.94; filter:blur(7px) brightness(1.55); }}
    }}
    @keyframes paymentGoldenExplosion {{
        0%,100% {{ transform:translate(-50%,-50%) rotate(0deg) scale(.88); opacity:.26; }}
        30% {{ opacity:.96; transform:translate(-50%,-50%) rotate(20deg) scale(1.08); }}
        62% {{ opacity:.50; transform:translate(-50%,-50%) rotate(38deg) scale(1.0); }}
    }}
    @keyframes paymentHaloBreathe {{
        0%,100% {{ transform:translate(-50%,-50%) scale(.90); opacity:.45; }}
        38% {{ transform:translate(-50%,-50%) scale(1.16); opacity:1; }}
        62% {{ transform:translate(-50%,-50%) scale(1.02); opacity:.72; }}
    }}
    @keyframes paymentSideGlow {{ 0%,100% {{ opacity:.16; transform:rotate(-18deg) scale(.96); }} 50% {{ opacity:.58; transform:rotate(-13deg) scale(1.07); }} }}
    @keyframes paymentSideGlowTwo {{ 0%,100% {{ opacity:.12; transform:rotate(21deg) scale(.96); }} 50% {{ opacity:.50; transform:rotate(16deg) scale(1.08); }} }}
    @keyframes paymentStarSweep {{ 0% {{ transform:translateX(-140px) translateY(20px); opacity:0; }} 18% {{ opacity:1; }} 100% {{ transform:translateX(520px) translateY(-46px); opacity:0; }} }}
    @keyframes paymentStarSweepBack {{ 0% {{ transform:translateX(140px) translateY(-18px); opacity:0; }} 18% {{ opacity:.9; }} 100% {{ transform:translateX(-520px) translateY(42px); opacity:0; }} }}

    /* RC23 — términos: zonas vivas al pasar cursor y checkbox real */
    .screen.terms-mode .real-button {{
        bottom:calc(env(safe-area-inset-bottom) + 82px);
        min-height:86px;
        transition:filter .22s ease, transform .22s ease;
    }}
    .screen.terms-mode .real-button::after {{
        opacity:.10;
        background:linear-gradient(90deg, rgba(255,230,155,.22), rgba(255,174,42,.34), rgba(255,244,190,.22));
        box-shadow:0 0 22px rgba(255,190,72,.24);
    }}
    .screen.terms-mode .real-button.is-disabled {{
        cursor:not-allowed;
        filter:saturate(.65) brightness(.74);
    }}
    .screen.terms-mode .real-button.is-disabled::after {{
        opacity:.04;
        animation:none;
    }}
    .screen.terms-mode .real-button.is-ready::after,
    .screen.terms-mode .real-button:hover::after,
    .screen.terms-mode .real-button:active::after {{
        opacity:.46;
        box-shadow:0 0 46px rgba(255,191,66,.72), 0 0 86px rgba(255,216,132,.42), inset 0 0 26px rgba(255,255,255,.18);
        animation:termsButtonReady 1.35s ease-in-out infinite;
    }}
    .terms-hover-layer {{ position:absolute; inset:0; z-index:6; pointer-events:auto; }}
    .terms-hover-zone {{
        position:absolute;
        left:18.8%; right:18.6%; height:8.2%;
        border-radius:18px;
        opacity:0;
        border:1px solid rgba(255,222,142,.0);
        background:linear-gradient(90deg, rgba(255,218,126,.02), rgba(255,218,126,.13), rgba(92,216,255,.08), rgba(255,218,126,.02));
        box-shadow:0 0 0 rgba(255,210,95,0);
        transition:opacity .2s ease, box-shadow .2s ease, border-color .2s ease, transform .2s ease;
    }}
    .terms-hover-zone:hover,
    .terms-hover-zone:active {{
        opacity:1;
        border-color:rgba(255,222,142,.82);
        box-shadow:0 0 26px rgba(255,202,82,.55), inset 0 0 22px rgba(255,221,142,.12), 0 0 44px rgba(65,204,255,.22);
        transform:scale(1.015);
    }}
    .thz1 {{ top:46.9%; }}
    .thz2 {{ top:55.0%; }}
    .thz3 {{ top:63.1%; }}
    .thz4 {{ top:71.2%; }}

    .terms-real-check {{
        position:absolute;
        left:17.2%; top:80.7%;
        width:44px; height:44px;
        z-index:12;
        pointer-events:auto;
    }}
    .terms-real-check input {{
        position:absolute;
        inset:0;
        opacity:0;
        cursor:pointer;
        z-index:2;
    }}
    .terms-real-check label {{
        position:absolute;
        inset:0;
        border-radius:8px;
        display:block;
        background:rgba(2,5,10,.78);
        border:2px solid rgba(255,247,218,.95);
        box-shadow:0 0 18px rgba(255,239,196,.42), inset 0 0 12px rgba(0,0,0,.68);
        transition:all .18s ease;
    }}
    .terms-real-check label span {{
        position:absolute;
        left:10px; top:3px;
        width:14px; height:24px;
        border:solid #111;
        border-width:0 4px 4px 0;
        transform:rotate(45deg) scale(.2);
        opacity:0;
        transition:all .18s ease;
    }}
    .terms-real-check input:checked + label {{
        background:linear-gradient(135deg,#fff7d5,#ffbe45 45%,#9b5b06);
        border-color:#fff0bd;
        box-shadow:0 0 28px rgba(255,195,74,.95),0 0 58px rgba(255,220,134,.42), inset 0 0 14px rgba(255,255,255,.28);
    }}
    .terms-real-check input:checked + label span {{ opacity:1; transform:rotate(45deg) scale(1); }}
    .terms-real-check.needs-attention {{ animation:termsCheckShake .35s ease-in-out 1; }}
    @keyframes termsButtonReady {{ 0%,100% {{ filter:brightness(1); transform:scale(.996); }} 50% {{ filter:brightness(1.42); transform:scale(1.012); }} }}
    @keyframes termsCheckShake {{ 0%,100% {{ transform:translateX(0); }} 25% {{ transform:translateX(-6px); }} 50% {{ transform:translateX(5px); }} 75% {{ transform:translateX(-3px); }} }}



    /* RC62 — consentimiento de grabación: checkbox y botón reales alineados al PNG canónico */
    .recording-consent-real-check {{
        position:absolute;
        left:16.6%;
        top:76.3%;
        width:62px;
        height:58px;
        z-index:120;
        pointer-events:auto;
        cursor:pointer;
    }}
    .recording-consent-real-check input {{
        position:absolute !important;
        inset:0 !important;
        width:100% !important;
        height:100% !important;
        opacity:0 !important;
        cursor:pointer !important;
        z-index:5 !important;
    }}
    .recording-consent-real-check label {{
        position:absolute;
        inset:0;
        opacity:0;
        pointer-events:none !important;
        background:transparent;
        border:0;
        box-shadow:none;
    }}
    .recording-consent-real-check::after {{
        content:"";
        position:absolute;
        inset:5px;
        border-radius:12px;
        pointer-events:none;
        opacity:.0;
        border:1px solid rgba(255,235,176,.0);
        box-shadow:0 0 0 rgba(255,205,100,0);
        transition:opacity .18s ease, box-shadow .18s ease, border-color .18s ease;
    }}
    .recording-consent-real-check:has(input:checked)::after {{
        opacity:.62;
        border-color:rgba(255,232,169,.78);
        box-shadow:0 0 24px rgba(255,203,94,.58), inset 0 0 10px rgba(255,221,145,.20);
    }}
    .recording-consent-real-check.needs-attention {{ animation:termsCheckShake .35s ease-in-out 1; }}
    .recording-consent-real-check.needs-attention::after {{
        opacity:.85;
        border-color:rgba(255,255,255,.96);
        box-shadow:0 0 28px rgba(255,255,255,.78),0 0 48px rgba(255,191,66,.42);
    }}
    .screen.consent-mode .real-button.recording-consent-continue {{
        left:11% !important;
        right:11% !important;
        bottom:calc(env(safe-area-inset-bottom) + 76px) !important;
        min-height:92px !important;
        border-radius:30px !important;
        z-index:130 !important;
        pointer-events:auto !important;
        touch-action:manipulation !important;
    }}
    .screen.consent-mode .real-button.is-disabled {{ pointer-events:auto !important; }}
    .screen.consent-mode .real-button.is-ready::after,
    .screen.consent-mode .real-button:hover::after,
    .screen.consent-mode .real-button:active::after {{
        opacity:.42;
        box-shadow:0 0 46px rgba(255,191,66,.72), 0 0 86px rgba(255,216,132,.40), inset 0 0 26px rgba(255,255,255,.16);
        animation:termsButtonReady 1.5s ease-in-out infinite;
    }}
    .screen.consent-mode .soft-halo {{
        left:50%; top:26%; width:420px; height:420px;
        background:radial-gradient(circle, rgba(67,213,255,.32), rgba(29,123,255,.13) 45%, transparent 74%);
        filter:blur(18px);
        animation:rc26BlueWingBreath 4.6s ease-in-out infinite;
        z-index:2;
    }}
    @media (max-height: 740px) {{
        .screen.consent-mode .real-button.recording-consent-continue {{
            bottom:calc(env(safe-area-inset-bottom) + 52px) !important;
            min-height:82px !important;
        }}
        .recording-consent-real-check {{
            top:75.4%;
            height:54px;
        }}
    }}

    /* RC23 — quiet-place: microvida premium también antes de empezar */
    .screen.quiet-mode .soft-halo {{
        left:50%; top:33%; width:390px; height:390px;
        background:radial-gradient(circle, rgba(54,205,255,.36), rgba(255,213,126,.12) 42%, transparent 72%);
        animation:quietButterflyBreathe 4.2s ease-in-out infinite;
    }}
    .screen.quiet-mode .edge-glow.eg1 {{ opacity:.24; animation:edgeGlowOnePower 6.4s ease-in-out infinite; }}
    .screen.quiet-mode .edge-glow.eg2 {{ opacity:.20; animation:edgeGlowTwoPower 6.8s ease-in-out .8s infinite; }}
    .screen.quiet-mode .star-run.sr1 {{ left:6%; top:36%; animation:starRunOnePower 6s ease-in-out .8s infinite; }}
    .screen.quiet-mode .star-run.sr2 {{ right:4%; bottom:23%; animation:starRunTwoPower 6.5s ease-in-out 1.6s infinite; }}
    .screen.quiet-mode .real-button::after {{
        opacity:.30;
        box-shadow:0 0 42px rgba(255,190,66,.58),0 0 80px rgba(255,220,132,.26);
        animation:termsButtonReady 1.8s ease-in-out infinite;
    }}
    @keyframes quietButterflyBreathe {{ 0%,100% {{ transform:translate(-50%,-50%) scale(.88); opacity:.30; }} 50% {{ transform:translate(-50%,-50%) scale(1.08); opacity:.78; }} }}
    .fallback {{ display:none; min-height:100vh; padding:42px 24px; color:#f6f1e8; text-align:center; flex-direction:column; justify-content:center; gap:18px; background:#02050a; }}


    /* RC25 — CHECKOUT ESTABLE: una sola pantalla entre formulario y Stripe */
    .screen.loading-mode .magic-line {{ top:67.20%; }}
    .screen.loading-mode .line-spark-runner {{ top:67.90%; }}
    .screen.loading-mode .blue-orb {{ top:67.85%; }}
    .screen.loading-mode .magic-line,
    .screen.loading-mode .line-spark-runner,
    .screen.loading-mode .blue-orb {{
        animation-delay:1.45s !important;
    }}
    .screen.loading-mode .magic-line span {{
        animation-delay:1.45s !important;
    }}
    .screen.loading-mode .magic-line b {{
        animation-delay:1.50s !important;
    }}

    /* RC25 — pago realizado: corazón vivo pero NO explosión brutal al cargar */
    .screen.payment-success-mode .phone::before {{
        width:270px;
        height:270px;
        top:60.8%;
        opacity:.38;
        filter:blur(12px);
        background:
            radial-gradient(circle, rgba(255,255,255,.62) 0%, rgba(255,230,150,.42) 6%, rgba(255,183,52,.30) 16%, rgba(255,183,52,.13) 32%, transparent 62%),
            conic-gradient(from 0deg, transparent, rgba(255,219,130,.18), transparent, rgba(255,244,190,.26), transparent);
        animation:paymentHeartSoftPulse 2.55s ease-in-out 1.15s infinite both;
    }}
    .screen.payment-success-mode .phone::after {{
        width:305px;
        height:305px;
        top:60.8%;
        opacity:.24;
        filter:drop-shadow(0 0 16px rgba(255,198,68,.42));
        animation:paymentGoldenSoft 5.8s ease-in-out 1.35s infinite both;
    }}
    .screen.payment-success-mode .soft-halo {{
        top:60.8%;
        width:330px;
        height:330px;
        opacity:.36;
        filter:blur(22px);
        animation:paymentHaloSoft 3.4s ease-in-out 1.2s infinite both;
    }}
    @keyframes paymentHeartSoftPulse {{
        0% {{ transform:translate(-50%,-50%) scale(.82); opacity:0; filter:blur(14px) brightness(.85); }}
        22% {{ opacity:.28; }}
        42% {{ transform:translate(-50%,-50%) scale(1.02); opacity:.46; filter:blur(10px) brightness(1.32); }}
        62% {{ transform:translate(-50%,-50%) scale(.94); opacity:.34; }}
        100% {{ transform:translate(-50%,-50%) scale(.88); opacity:.22; filter:blur(13px) brightness(1); }}
    }}
    @keyframes paymentGoldenSoft {{
        0% {{ transform:translate(-50%,-50%) rotate(0deg) scale(.86); opacity:0; }}
        25% {{ opacity:.18; }}
        52% {{ opacity:.34; transform:translate(-50%,-50%) rotate(18deg) scale(1.02); }}
        100% {{ opacity:.10; transform:translate(-50%,-50%) rotate(34deg) scale(.94); }}
    }}
    @keyframes paymentHaloSoft {{
        0% {{ opacity:0; transform:translate(-50%,-50%) scale(.86); }}
        36% {{ opacity:.38; transform:translate(-50%,-50%) scale(1.03); }}
        100% {{ opacity:.25; transform:translate(-50%,-50%) scale(.92); }}
    }}



    /* RC26 — términos estable: checkbox real invisible alineado con la casilla dibujada, sin cuadrado gigante flotante */
    .screen.terms-mode .terms-real-check {{
        left:19.0%;
        top:80.8%;
        width:56px;
        height:48px;
        z-index:12;
    }}
    .screen.terms-mode .terms-real-check label {{
        opacity:0;
        background:transparent;
        border:0;
        box-shadow:none;
    }}
    .screen.terms-mode .terms-real-check label span {{ display:none; }}
    .screen.terms-mode .terms-real-check input {{ opacity:0; }}
    .screen.terms-mode .terms-real-check::after {{
        content:"";
        position:absolute;
        inset:5px;
        border-radius:10px;
        pointer-events:none;
        opacity:.0;
        border:1px solid rgba(255,235,176,.0);
        box-shadow:0 0 0 rgba(255,205,100,0);
        transition:opacity .18s ease, box-shadow .18s ease, border-color .18s ease;
    }}
    .screen.terms-mode .terms-real-check:has(input:checked)::after {{
        opacity:.55;
        border-color:rgba(255,232,169,.75);
        box-shadow:0 0 22px rgba(255,203,94,.55), inset 0 0 10px rgba(255,221,145,.18);
    }}
    .screen.terms-mode .terms-real-check.needs-attention::after {{
        opacity:.80;
        border-color:rgba(255,255,255,.95);
        box-shadow:0 0 26px rgba(255,255,255,.75),0 0 46px rgba(255,191,66,.40);
    }}

    /* RC26 — pantallas reales con vida: luz, agua, alas y botones sin cambiar lógica */
    .screen.intro-mode .soft-halo,
    .screen.sound-mode .soft-halo,
    .screen.complete-mode .soft-halo,
    .screen.sender-entry-mode .soft-halo,
    .screen.viral-mode .soft-halo {{
        left:62%; top:25%; width:380px; height:380px;
        background:radial-gradient(circle, rgba(67,213,255,.36), rgba(29,123,255,.13) 45%, transparent 74%);
        filter:blur(18px);
        animation:rc26BlueWingBreath 4.6s ease-in-out infinite;
        z-index:2;
    }}
    .screen.intro-mode .edge-glow.eg1,
    .screen.sound-mode .edge-glow.eg1,
    .screen.quiet-mode .edge-glow.eg1,
    .screen.complete-mode .edge-glow.eg1,
    .screen.sender-entry-mode .edge-glow.eg1,
    .screen.viral-mode .edge-glow.eg1 {{
        opacity:.28;
        border-color:rgba(56,202,255,.26);
        box-shadow:0 0 38px rgba(56,202,255,.40), inset 0 0 40px rgba(56,202,255,.14);
        animation:rc26LeftAurora 6.2s ease-in-out infinite;
    }}
    .screen.intro-mode .edge-glow.eg2,
    .screen.sound-mode .edge-glow.eg2,
    .screen.quiet-mode .edge-glow.eg2,
    .screen.complete-mode .edge-glow.eg2,
    .screen.sender-entry-mode .edge-glow.eg2,
    .screen.viral-mode .edge-glow.eg2 {{
        opacity:.24;
        border-color:rgba(255,214,126,.22);
        box-shadow:0 0 38px rgba(255,196,82,.34), inset 0 0 40px rgba(255,196,82,.12);
        animation:rc26RightGoldAurora 6.8s ease-in-out .7s infinite;
    }}
    .screen.intro-mode .star-run.sr1,
    .screen.sound-mode .star-run.sr1,
    .screen.quiet-mode .star-run.sr1,
    .screen.complete-mode .star-run.sr1,
    .screen.sender-entry-mode .star-run.sr1,
    .screen.viral-mode .star-run.sr1 {{
        display:block; width:145px; height:3px; top:34%; left:3%; z-index:9;
        animation:rc26StarTravelOne 5.7s ease-in-out .9s infinite;
    }}
    .screen.intro-mode .star-run.sr2,
    .screen.sound-mode .star-run.sr2,
    .screen.quiet-mode .star-run.sr2,
    .screen.complete-mode .star-run.sr2,
    .screen.sender-entry-mode .star-run.sr2,
    .screen.viral-mode .star-run.sr2 {{
        display:block; width:145px; height:3px; bottom:24%; right:3%; z-index:9;
        animation:rc26StarTravelTwo 6.1s ease-in-out 1.6s infinite;
    }}
    .screen.sound-mode .phone::before,
    .screen.quiet-mode .phone::before,
    .screen.complete-mode .phone::before,
    .screen.sender-entry-mode .phone::before,
    .screen.viral-mode .phone::before {{
        content:"";
        position:absolute;
        left:8%; right:8%; bottom:5%; height:22%;
        border-radius:999px;
        background:linear-gradient(90deg, transparent, rgba(66,205,255,.12), rgba(255,214,126,.16), rgba(66,205,255,.10), transparent);
        filter:blur(12px);
        opacity:.50;
        mix-blend-mode:screen;
        pointer-events:none;
        z-index:2;
        animation:rc26WaterGlow 6.4s ease-in-out infinite;
    }}
    .screen.sound-mode .phone::after,
    .screen.quiet-mode .phone::after,
    .screen.complete-mode .phone::after,
    .screen.sender-entry-mode .phone::after,
    .screen.viral-mode .phone::after {{
        content:"";
        position:absolute;
        inset:0;
        pointer-events:none;
        z-index:7;
        opacity:0;
        mix-blend-mode:screen;
        background:linear-gradient(115deg, transparent 0%, transparent 38%, rgba(255,244,198,.42) 41%, rgba(71,211,255,.22) 44%, transparent 50%, transparent 100%);
        transform:translateX(-74%) skewX(-10deg);
        animation:rc26SoftSweep 7.2s cubic-bezier(.2,.7,.15,1) 1.2s infinite;
    }}
    .screen.complete-mode .real-button::after,
    .screen.sound-mode .real-button::after,
    .screen.quiet-mode .real-button::after,
    .screen.viral-mode .real-button::after,
    .screen.sender-entry-mode .real-button::after {{
        opacity:.28;
        box-shadow:0 0 42px rgba(255,190,66,.54),0 0 80px rgba(255,220,132,.24);
        animation:rc26ButtonBreath 1.95s ease-in-out infinite;
    }}
    .screen.uploading-mode .soft-halo {{
        left:50%; top:55%; width:360px; height:360px;
        background:radial-gradient(circle, rgba(59,211,255,.42), rgba(255,211,121,.12) 46%, transparent 76%);
        animation:rc26SavingPulse 2.8s ease-in-out infinite;
    }}
    .screen.uploading-mode .edge-glow.eg1,
    .screen.uploading-mode .edge-glow.eg2 {{ opacity:.20; }}
    .screen.payment-success-mode .phone::before,
    .screen.payment-success-mode .phone::after,
    .screen.payment-success-mode .soft-halo {{
        animation-delay:1.55s !important;
    }}
    .screen.payment-success-mode .phone::before {{ opacity:.30; }}
    .screen.payment-success-mode .phone::after {{ opacity:.16; }}

    @keyframes rc26BlueWingBreath {{ 0%,100% {{ transform:translate(-50%,-50%) scale(.88); opacity:.26; }} 50% {{ transform:translate(-50%,-50%) scale(1.10); opacity:.76; }} }}
    @keyframes rc26LeftAurora {{ 0%,100% {{ opacity:.06; transform:rotate(-18deg) scale(.94); }} 50% {{ opacity:.36; transform:rotate(-13deg) scale(1.06); }} }}
    @keyframes rc26RightGoldAurora {{ 0%,100% {{ opacity:.05; transform:rotate(21deg) scale(.94); }} 50% {{ opacity:.30; transform:rotate(16deg) scale(1.06); }} }}
    @keyframes rc26StarTravelOne {{ 0% {{ transform:translateX(-120px) translateY(12px); opacity:0; }} 18% {{ opacity:.86; }} 100% {{ transform:translateX(430px) translateY(-26px); opacity:0; }} }}
    @keyframes rc26StarTravelTwo {{ 0% {{ transform:translateX(140px) translateY(-12px); opacity:0; }} 18% {{ opacity:.72; }} 100% {{ transform:translateX(-430px) translateY(26px); opacity:0; }} }}
    @keyframes rc26WaterGlow {{ 0%,100% {{ transform:translateX(-12px) scaleX(.94); opacity:.26; }} 50% {{ transform:translateX(14px) scaleX(1.06); opacity:.64; }} }}
    @keyframes rc26SoftSweep {{ 0%,70% {{ opacity:0; transform:translateX(-74%) skewX(-10deg); }} 80% {{ opacity:.48; }} 100% {{ opacity:0; transform:translateX(74%) skewX(-10deg); }} }}
    @keyframes rc26ButtonBreath {{ 0%,100% {{ opacity:.16; transform:scale(.99); filter:brightness(1); }} 50% {{ opacity:.44; transform:scale(1.012); filter:brightness(1.34); }} }}
    @keyframes rc26SavingPulse {{ 0%,100% {{ transform:translate(-50%,-50%) scale(.86); opacity:.28; }} 50% {{ transform:translate(-50%,-50%) scale(1.10); opacity:.70; }} }}

/* RC15 SENDER PACK — encaje fino y vida visual */
.sender-pack-stage, .sender-pack-wrap, .sender-pack-card {{ position:relative; }}
.sender-pack-video, video.sender-pack-video {{
    object-fit:cover !important;
    border-radius:22px !important;
    filter:contrast(1.08) saturate(1.10) brightness(1.04);
}}
.sender-reaction, video.sender-reaction, .reaction-video {{
    object-fit:cover !important;
    filter:contrast(1.12) saturate(1.08) brightness(1.08);
    box-shadow:0 0 0 2px rgba(255,208,108,.82), 0 0 28px rgba(255,190,82,.46) !important;
}}
video::-webkit-media-controls-panel {{ opacity:0; transition:opacity .22s ease; }}
video:hover::-webkit-media-controls-panel, video:focus::-webkit-media-controls-panel {{ opacity:1; }}
.sender-pack-stage::before {{
    content:"";
    position:absolute;
    left:5%;
    right:5%;
    top:19%;
    height:2px;
    border-radius:999px;
    background:linear-gradient(90deg, transparent, rgba(76,209,255,.92), rgba(255,215,125,.78), transparent);
    box-shadow:0 0 22px rgba(76,209,255,.72),0 0 38px rgba(255,208,112,.30);
    animation:senderLineLife 3.1s ease-in-out infinite;
    pointer-events:none;
    z-index:6;
}}
.sender-pack-stage::after {{
    content:"";
    position:absolute;
    width:72px;
    height:72px;
    right:10%;
    top:24%;
    border-radius:999px;
    background:radial-gradient(circle, rgba(255,255,255,.92), rgba(255,210,110,.35) 28%, transparent 72%);
    filter:blur(3px);
    animation:senderGlowBreath 3.8s ease-in-out infinite;
    pointer-events:none;
    z-index:6;
}}
@keyframes senderLineLife {{ 0%,100%{{opacity:.45; filter:brightness(1);}} 50%{{opacity:1; filter:brightness(1.8);}} }}
@keyframes senderGlowBreath {{ 0%,100%{{opacity:.16; transform:scale(.82);}} 50%{{opacity:.48; transform:scale(1.08);}} }}



    /* RC43 — GUÍA LIMPIA SOBRE BASE RC27B
       Regla: las imágenes y efectos nunca capturan clics.
       Solo son interactivos el botón real y el checkbox real. */
    .screen.intro-mode .img,
    .screen.terms-mode .img,
    .screen.quiet-mode .img,
    .screen.intro-mode .soft-halo,
    .screen.terms-mode .soft-halo,
    .screen.quiet-mode .soft-halo,
    .screen.intro-mode .particle,
    .screen.terms-mode .particle,
    .screen.quiet-mode .particle,
    .screen.intro-mode .edge-glow,
    .screen.terms-mode .edge-glow,
    .screen.quiet-mode .edge-glow,
    .screen.intro-mode .star-run,
    .screen.terms-mode .star-run,
    .screen.quiet-mode .star-run,
    .screen.intro-mode .magic-line,
    .screen.terms-mode .magic-line,
    .screen.quiet-mode .magic-line,
    .screen.intro-mode .line-spark-runner,
    .screen.terms-mode .line-spark-runner,
    .screen.quiet-mode .line-spark-runner,
    .screen.intro-mode .blue-orb,
    .screen.terms-mode .blue-orb,
    .screen.quiet-mode .blue-orb {{
        pointer-events:none !important;
    }}

    .screen.intro-mode .terms-hover-layer,
    .screen.terms-mode .terms-hover-layer,
    .screen.quiet-mode .terms-hover-layer,
    .screen.intro-mode .terms-hover-zone,
    .screen.terms-mode .terms-hover-zone,
    .screen.quiet-mode .terms-hover-zone {{
        display:none !important;
        pointer-events:none !important;
        visibility:hidden !important;
        opacity:0 !important;
    }}

    .screen.intro-mode .real-button,
    .screen.consent-mode .real-button,
    .screen.quiet-mode .real-button,
    .screen.terms-mode .terms-continue {{
        pointer-events:auto !important;
        z-index:100 !important;
        touch-action:manipulation !important;
    }}

    /* RC51 — quiet-place final: zona real del botón grande, centrada y sin capas encima */
    .screen.quiet-mode .real-button {{
        left:15% !important;
        right:15% !important;
        bottom:calc(env(safe-area-inset-bottom) + 112px) !important;
        min-height:108px !important;
        border-radius:30px !important;
        z-index:140 !important;
        pointer-events:auto !important;
        touch-action:manipulation !important;
    }}

    .screen.quiet-mode .visual-action-form {{
        position:static !important;
        z-index:140 !important;
    }}

    .screen.quiet-mode .extra-note {{
        display:none !important;
    }}

    @media (max-height: 740px) {{
        .screen.quiet-mode .real-button {{
            bottom:calc(env(safe-area-inset-bottom) + 76px) !important;
            min-height:96px !important;
        }}
    }}

    .screen.terms-mode .terms-real-check {{
        pointer-events:auto !important;
        z-index:110 !important;
        cursor:pointer !important;
    }}

    .screen.terms-mode .terms-real-check input {{
        position:absolute !important;
        inset:0 !important;
        width:100% !important;
        height:100% !important;
        opacity:0 !important;
        cursor:pointer !important;
        z-index:5 !important;
    }}

    .screen.terms-mode .terms-real-check label {{
        pointer-events:none !important;
    }}


    /* =========================================================
       RC71 PRE-EXPERIENCE MAGIC SAFE
       Solo atmósfera viva para: intro, sonido, lugar tranquilo y consentimiento.
       No cambia rutas, botones, formularios, Stripe, Twilio, DB, reacción ni sender pack.
       ========================================================= */
    .pre-magic {{
        position:absolute;
        inset:0;
        z-index:4;
        pointer-events:none;
        display:none;
        overflow:hidden;
        opacity:1;
        contain:paint;
    }}
    .screen.intro-mode .pre-magic,
    .screen.sound-mode .pre-magic,
    .screen.quiet-mode .pre-magic,
    .screen.consent-mode .pre-magic {{
        display:block;
    }}
    .pre-depth {{
        position:absolute;
        inset:-8%;
        opacity:.62;
        mix-blend-mode:screen;
        background:
            radial-gradient(circle at 18% 18%, rgba(55,207,255,.16), transparent 24%),
            radial-gradient(circle at 80% 26%, rgba(255,211,121,.12), transparent 25%),
            radial-gradient(circle at 51% 72%, rgba(72,198,255,.10), transparent 31%),
            linear-gradient(180deg, rgba(2,5,10,.08), transparent 38%, rgba(2,5,10,.20));
        filter:blur(1px);
        animation:rc71DepthBreath 9.8s ease-in-out infinite;
    }}
    .pre-fog {{
        position:absolute;
        left:-32%;
        right:-32%;
        height:44%;
        border-radius:999px;
        opacity:.0;
        filter:blur(23px);
        mix-blend-mode:screen;
        background:linear-gradient(90deg, transparent, rgba(93,211,255,.12), rgba(255,221,144,.08), rgba(93,211,255,.11), transparent);
        animation:rc71FogDrift 18s ease-in-out infinite;
    }}
    .pre-fog.fog-a {{ top:15%; animation-delay:.2s; }}
    .pre-fog.fog-b {{ bottom:8%; opacity:.0; animation-duration:22s; animation-delay:4.2s; transform:scaleY(.72); }}
    .pre-spark {{
        position:absolute;
        width:4px;
        height:4px;
        border-radius:999px;
        opacity:0;
        background:rgba(117,221,255,.96);
        box-shadow:0 0 13px rgba(117,221,255,.95), 0 0 28px rgba(117,221,255,.36);
        animation:rc71SparkRise 10.5s linear infinite;
    }}
    .pre-spark.gold {{
        background:rgba(255,221,145,.95);
        box-shadow:0 0 13px rgba(255,221,145,.90), 0 0 28px rgba(255,196,74,.34);
    }}
    .ps1 {{ left:13%; bottom:11%; animation-delay:.1s; animation-duration:11.8s; transform:scale(.75); }}
    .ps2 {{ left:28%; bottom:25%; animation-delay:2.8s; animation-duration:13.2s; transform:scale(.55); }}
    .ps3 {{ left:47%; bottom:10%; animation-delay:1.4s; animation-duration:12.6s; transform:scale(.68); }}
    .ps4 {{ left:69%; bottom:19%; animation-delay:4.1s; animation-duration:14.4s; transform:scale(.5); }}
    .ps5 {{ left:83%; bottom:33%; animation-delay:6.0s; animation-duration:12.8s; transform:scale(.62); }}
    .ps6 {{ left:56%; bottom:46%; animation-delay:7.2s; animation-duration:15.2s; transform:scale(.45); }}
    .pre-glint {{
        position:absolute;
        width:92px;
        height:2px;
        border-radius:999px;
        opacity:0;
        mix-blend-mode:screen;
        background:linear-gradient(90deg, transparent, rgba(255,255,255,.88), rgba(255,220,135,.70), transparent);
        box-shadow:0 0 18px rgba(255,227,155,.52), 0 0 35px rgba(84,211,255,.20);
        animation:rc71GlintCross 7.6s ease-in-out infinite;
    }}
    .glint-a {{ left:4%; top:31%; animation-delay:2.1s; }}
    .glint-b {{ right:-2%; bottom:27%; animation-delay:5.4s; animation-direction:reverse; }}
    .yul-live {{
        position:absolute;
        width:74px;
        height:auto;
        left:66%;
        top:22%;
        opacity:0;
        z-index:5;
        pointer-events:none;
        transform-origin:center center;
        filter:drop-shadow(0 0 14px rgba(92,216,255,.65)) drop-shadow(0 0 22px rgba(255,214,124,.30));
        mix-blend-mode:screen;
        animation:rc71YulAlive 13.5s cubic-bezier(.45,0,.25,1) infinite;
    }}
    .yul-trail {{
        position:absolute;
        left:66%;
        top:22%;
        width:120px;
        height:32px;
        border-radius:999px;
        z-index:4;
        opacity:0;
        pointer-events:none;
        mix-blend-mode:screen;
        background:radial-gradient(circle at 20% 50%, rgba(255,222,142,.38), transparent 18%), radial-gradient(circle at 48% 48%, rgba(99,219,255,.28), transparent 21%), linear-gradient(90deg, rgba(255,219,130,.00), rgba(255,219,130,.20), rgba(83,211,255,.14), transparent);
        filter:blur(7px);
        animation:rc71YulTrail 13.5s cubic-bezier(.45,0,.25,1) infinite;
    }}
    .screen.sound-mode .yul-live,
    .screen.sound-mode .yul-trail {{ top:19%; left:71%; animation-delay:1.6s; animation-duration:15s; }}
    .screen.quiet-mode .yul-live,
    .screen.quiet-mode .yul-trail {{ top:24%; left:18%; animation-delay:2.4s; animation-duration:16.5s; }}
    .screen.consent-mode .yul-live,
    .screen.consent-mode .yul-trail {{ top:18%; left:70%; animation-delay:3.2s; animation-duration:17s; opacity:0; }}
    .screen.consent-mode .pre-magic {{ opacity:.72; }}
    .screen.consent-mode .pre-spark {{ animation-duration:14.8s; }}
    .screen.quiet-mode .pre-fog {{ opacity:.0; filter:blur(27px); }}
    .screen.quiet-mode .pre-depth {{ opacity:.75; }}

    @keyframes rc71DepthBreath {{
        0%,100% {{ transform:scale(1) translate3d(0,0,0); opacity:.42; }}
        45% {{ transform:scale(1.045) translate3d(-1.8%,1.2%,0); opacity:.74; }}
        72% {{ opacity:.55; }}
    }}
    @keyframes rc71FogDrift {{
        0% {{ transform:translateX(-14%) translateY(10px) scaleX(.92); opacity:0; }}
        18% {{ opacity:.40; }}
        54% {{ opacity:.30; }}
        100% {{ transform:translateX(14%) translateY(-12px) scaleX(1.08); opacity:0; }}
    }}
    @keyframes rc71SparkRise {{
        0% {{ opacity:0; transform:translate3d(0,0,0) scale(.42); }}
        12% {{ opacity:.78; }}
        58% {{ opacity:.42; transform:translate3d(18px,-88px,0) scale(.82); }}
        100% {{ opacity:0; transform:translate3d(34px,-178px,0) scale(1.05); }}
    }}
    @keyframes rc71GlintCross {{
        0%,68% {{ opacity:0; transform:translateX(-80px) translateY(14px) rotate(-9deg) scaleX(.45); }}
        75% {{ opacity:.76; }}
        100% {{ opacity:0; transform:translateX(330px) translateY(-24px) rotate(-9deg) scaleX(1.15); }}
    }}
    @keyframes rc71YulAlive {{
        0% {{ opacity:0; transform:translate3d(-18px,12px,0) rotate(-7deg) scale(.78) skewX(0deg); }}
        10% {{ opacity:.0; }}
        18% {{ opacity:.82; transform:translate3d(0,0,0) rotate(-2deg) scale(.92) skewX(2deg); }}
        30% {{ transform:translate3d(-9px,-12px,0) rotate(4deg) scale(.98) skewX(-3deg); }}
        42% {{ transform:translate3d(7px,-4px,0) rotate(-3deg) scale(.94) skewX(3deg); }}
        55% {{ opacity:.76; transform:translate3d(-4px,10px,0) rotate(3deg) scale(.99) skewX(-2deg); }}
        68% {{ transform:translate3d(12px,-8px,0) rotate(-4deg) scale(.93) skewX(2deg); }}
        80% {{ opacity:.58; transform:translate3d(22px,4px,0) rotate(2deg) scale(.86) skewX(-1deg); }}
        100% {{ opacity:0; transform:translate3d(44px,-18px,0) rotate(8deg) scale(.72) skewX(0deg); }}
    }}
    @keyframes rc71YulTrail {{
        0%,12% {{ opacity:0; transform:translate3d(-40px,20px,0) rotate(-8deg) scale(.72); }}
        24% {{ opacity:.34; }}
        52% {{ opacity:.22; transform:translate3d(-28px,2px,0) rotate(-4deg) scale(.95); }}
        78% {{ opacity:.14; }}
        100% {{ opacity:0; transform:translate3d(14px,-12px,0) rotate(7deg) scale(.82); }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        .screen.intro-mode .pre-magic,
        .screen.sound-mode .pre-magic,
        .screen.quiet-mode .pre-magic,
        .screen.consent-mode .pre-magic {{
            opacity:.42;
        }}
        .pre-depth,
        .pre-fog,
        .pre-spark,
        .pre-glint,
        .yul-live,
        .yul-trail {{
            animation:none !important;
        }}
        .yul-live {{ opacity:.32; }}
    }}

</style>
</head>
<body>
<main class="screen{screen_mode_class}">
    <section class="phone">
        <img class="img" src="{image_src}" alt="ETERNA" onerror="this.onerror=null; this.src='{fallback_src}';">
        <div class="pre-magic" aria-hidden="true">
            <div class="pre-depth"></div>
            <div class="pre-fog fog-a"></div>
            <div class="pre-fog fog-b"></div>
            <i class="pre-spark ps1"></i>
            <i class="pre-spark gold ps2"></i>
            <i class="pre-spark ps3"></i>
            <i class="pre-spark gold ps4"></i>
            <i class="pre-spark ps5"></i>
            <i class="pre-spark gold ps6"></i>
            <span class="pre-glint glint-a"></span>
            <span class="pre-glint glint-b"></span>
            <span class="yul-trail"></span>
            <img class="yul-live" src="{yul_src}" alt="" loading="eager">
        </div>
        <i class="particle p1" aria-hidden="true"></i>
        <i class="particle p2" aria-hidden="true"></i>
        <i class="particle p3" aria-hidden="true"></i>
        <i class="particle gold p4" aria-hidden="true"></i>
        <div class="soft-halo" aria-hidden="true"></div>
        <div class="edge-glow eg1" aria-hidden="true"></div>
        <div class="edge-glow eg2" aria-hidden="true"></div>
        <div class="star-run sr1" aria-hidden="true"></div>
        <div class="star-run sr2" aria-hidden="true"></div>
        {loading_layers}
        {action_html}
        {note_html}
        <section id="fallback-visual" class="fallback"><h1>ETERNA</h1><p>Estamos preparando tu momento.</p></section>
    </section>
</main>
{redirect_script}
{extra_script or ''}
</body>
</html>
""")

# =========================================================
# LOG HUMANO ETERNA (ESPAÑOL)
# =========================================================

LOG_TRANSLATIONS = {
    "ORDER_CREATED": "Pedido creado",
    "PAYMENT_COMPLETED": "Pago recibido",
    "VIDEO_REQUESTED": "Vídeo solicitado al motor",
    "VIDEO_READY": "Vídeo terminado",
    "RECIPIENT_SENT": "Mensaje enviado al destinatario",
    "EXPERIENCE_STARTED": "Experiencia iniciada",
    "REACTION_UPLOADED": "Reacción recibida",
    "PAYOUT_COMPLETED": "Regalo entregado",
    "SENDER_NOTIFIED": "Regalante avisado",
    "ETERNA_COMPLETED": "ETERNA completada",

    "order_created": "Pedido creado",
    "payment_completed": "Pago recibido",
    "checkout_completed": "Pago recibido",
    "video_requested": "Vídeo solicitado al motor",
    "video_ready": "Vídeo terminado",
    "recipient_sms_sent": "Mensaje enviado al destinatario",
    "recipient_sms_failed": "No se pudo enviar el mensaje al destinatario",
    "sender_sms_attempt": "Aviso al regalante",
    "sender_sms_error": "Error avisando al regalante",
    "reaction_saved_local": "Reacción guardada en local",
    "reaction_r2_uploaded": "Reacción subida a la nube",
    "reaction_r2_skipped": "Reacción guardada solo en local",
    "reaction_r2_pending": "Reacción pendiente de subir a la nube",
    "payout_attempt": "Intento de entrega del regalo",
    "payout_error": "Error en la entrega del regalo",
    "eterna_completed": "ETERNA completada",
    "video_engine_requested": "Vídeo enviado al motor",
    "video_engine_error": "Error del motor de vídeo",
    "video_callback_received": "Callback recibido del motor",
    "admin_retry": "Reintento manual desde admin",

    "ok": "correcto",
    "warning": "aviso",
    "error": "error",
    "pending": "pendiente",
}

STATUS_ICONS = {
    "ok": "✅",
    "warning": "⚠️",
    "error": "🚨",
    "pending": "⏳",
}

STEP_ICONS = {
    "order": "🧾",
    "payment": "💳",
    "checkout": "💳",
    "video": "🎬",
    "recipient": "📩",
    "sender": "📱",
    "reaction": "🎥",
    "payout": "💸",
    "transfer": "💸",
    "eterna": "✨",
    "admin": "🛠️",
}


def human_label(value: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return "Paso sin nombre"
    if raw in LOG_TRANSLATIONS:
        return LOG_TRANSLATIONS[raw]
    lowered = raw.lower()
    if lowered in LOG_TRANSLATIONS:
        return LOG_TRANSLATIONS[lowered]
    return lowered.replace("_", " ").replace("-", " ").strip().capitalize()


def icon_for_step(step: str, status: str = "ok") -> str:
    status = str(status or "ok").strip().lower()
    if status == "error":
        return "🚨"
    step_raw = str(step or "").strip().lower()
    for key, icon in STEP_ICONS.items():
        if key in step_raw:
            return icon
    return STATUS_ICONS.get(status, "ℹ️")


def log_info(label: str, value=None):
    title = human_label(label)
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"ℹ️ INFO ETERNA: {title}")
    if value is not None and str(value).strip():
        print(f"📌 Detalle: {value}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


def log_error(label: str, error: Exception):
    title = human_label(label)
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🚨 ERROR ETERNA: {title}")
    print(f"❌ Qué ha pasado: {error}")
    print("🔎 Detalle técnico debajo para poder arreglarlo:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    traceback.print_exc()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


def mask_email(email: str) -> str:
    email = str(email or "").strip()
    if "@" not in email:
        return email or "sin email"
    name, domain = email.split("@", 1)
    masked = (name[:3] if len(name) > 3 else name[:1]) + "***"
    return f"{masked}@{domain}"


def mask_phone(phone: str) -> str:
    phone = str(phone or "").strip()
    if len(phone) <= 6:
        return phone or "sin teléfono"
    return phone[:5] + "****" + phone[-2:]


def log_human(title: str, *lines):
    readable_title = human_label(title)
    icon = icon_for_step(title)
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{icon} {readable_title.upper()}")
    for line in lines:
        if line is not None and str(line).strip():
            print(str(line))
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


def safe_slug(value: str, fallback: str = "persona") -> str:
    raw = str(value or "").strip().lower()
    for a, b in {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ü":"u","ñ":"n"}.items():
        raw = raw.replace(a, b)
    out = []
    for ch in raw:
        if ch.isalnum():
            out.append(ch)
        elif ch in {" ", "-", "_"}:
            out.append("_")
    slug = "".join(out).strip("_")
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug[:60] or fallback


def r2_order_key(order: dict, kind: str, filename: str) -> str:
    order_id = str(order.get("id") or "unknown")
    recipient = safe_slug(order.get("recipient_name") or "destinatario", "destinatario")
    sender = safe_slug(order.get("sender_name") or "regalante", "regalante")
    return f"orders/{order_id}/{recipient}_{sender}/{kind}/{filename}"


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
        transfer_started_at TEXT,
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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS order_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT NOT NULL,
        step TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'ok',
        message TEXT,
        meta_json TEXT,
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
    add_column_if_missing("orders", "transfer_started_at", "ALTER TABLE orders ADD COLUMN transfer_started_at TEXT")
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
    # RC53 — BLINDAJE PRELANZAMIENTO: estados, locks, idempotencia y recuperación
    add_column_if_missing("orders", "order_state", "ALTER TABLE orders ADD COLUMN order_state TEXT NOT NULL DEFAULT 'CREATED'")
    add_column_if_missing("orders", "stripe_event_id", "ALTER TABLE orders ADD COLUMN stripe_event_id TEXT")
    add_column_if_missing("orders", "stripe_event_processed_at", "ALTER TABLE orders ADD COLUMN stripe_event_processed_at TEXT")
    add_column_if_missing("orders", "delivery_processing_lock", "ALTER TABLE orders ADD COLUMN delivery_processing_lock INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "delivery_processing_lock_at", "ALTER TABLE orders ADD COLUMN delivery_processing_lock_at TEXT")
    add_column_if_missing("orders", "sender_sms_processing_lock", "ALTER TABLE orders ADD COLUMN sender_sms_processing_lock INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "sender_sms_processing_lock_at", "ALTER TABLE orders ADD COLUMN sender_sms_processing_lock_at TEXT")
    add_column_if_missing("orders", "last_recovery_at", "ALTER TABLE orders ADD COLUMN last_recovery_at TEXT")
    add_column_if_missing("orders", "last_recovery_reason", "ALTER TABLE orders ADD COLUMN last_recovery_reason TEXT")
    add_column_if_missing("orders", "recipient_session_token", "ALTER TABLE orders ADD COLUMN recipient_session_token TEXT")
    add_column_if_missing("orders", "recipient_session_claimed_at", "ALTER TABLE orders ADD COLUMN recipient_session_claimed_at TEXT")

    # RC74 FULL — columnas de supervivencia / cola / recuperación.
    add_column_if_missing("orders", "order_version", "ALTER TABLE orders ADD COLUMN order_version TEXT")
    add_column_if_missing("orders", "render_status", "ALTER TABLE orders ADD COLUMN render_status TEXT NOT NULL DEFAULT 'PENDING_RENDER'")
    add_column_if_missing("orders", "render_attempts", "ALTER TABLE orders ADD COLUMN render_attempts INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "render_started_at", "ALTER TABLE orders ADD COLUMN render_started_at TEXT")
    add_column_if_missing("orders", "render_last_error", "ALTER TABLE orders ADD COLUMN render_last_error TEXT")
    add_column_if_missing("orders", "recovery_last_checked_at", "ALTER TABLE orders ADD COLUMN recovery_last_checked_at TEXT")
    add_column_if_missing("orders", "recovery_notes", "ALTER TABLE orders ADD COLUMN recovery_notes TEXT")
init_db()



# =========================================================
# RC75 — COLUMNAS FORMULARIO EMOCIONAL YUL
# No son obligatorias. No rompen pedidos antiguos.
# =========================================================
try:
    add_column_if_missing("orders", "yul_memory_place", "ALTER TABLE orders ADD COLUMN yul_memory_place TEXT")
    add_column_if_missing("orders", "yul_memory_detail", "ALTER TABLE orders ADD COLUMN yul_memory_detail TEXT")
    add_column_if_missing("orders", "yul_emotion_tone", "ALTER TABLE orders ADD COLUMN yul_emotion_tone TEXT")
    add_column_if_missing("orders", "yul_magic_hint", "ALTER TABLE orders ADD COLUMN yul_magic_hint TEXT")
except Exception as e:
    print("[WARN] RC75 yul emotional columns skipped:", e)

# =========================================================
# HELPERS BASE
# =========================================================

def now_dt() -> datetime:
    return datetime.now(timezone.utc)


def now_iso() -> str:
    return now_dt().isoformat()


def gift_refund_deadline_iso() -> str:
    return (now_dt() + timedelta(days=GIFT_REFUND_DAYS)).isoformat()


def order_age_days(order: dict) -> Optional[float]:
    """RC60: edad del pedido para auditoría/caducidad futura sin romper pruebas actuales."""
    try:
        created = (order.get("created_at") or "").strip()
        if not created:
            return None
        dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return max(0.0, (now_dt() - dt).total_seconds() / 86400.0)
    except Exception:
        return None


def order_link_expired(order: dict) -> bool:
    """RC60: expiración opcional. Por defecto está apagada para no romper el circuito probado."""
    if not ETERNA_ENFORCE_LINK_EXPIRY:
        return False
    age = order_age_days(order)
    return bool(age is not None and age > ETERNA_LINK_EXPIRY_DAYS)


def safe_bool(value) -> bool:
    return bool(int(value or 0)) if str(value or "").strip().isdigit() else bool(value)


def safe_text(v: str) -> str:
    return html.escape(str(v or "").strip())


def safe_attr(v: str) -> str:
    return html.escape(str(v or "").strip(), quote=True)



# =========================================================
# RC75 — HELPERS YUL EMOCIONAL
# =========================================================

def rc75_clean_emotional_text(value: str, max_len: int = 220) -> str:
    raw = str(value or "").strip()
    raw = " ".join(raw.split())
    return raw[:max_len]

def rc75_yul_context_from_order(order: dict) -> dict:
    return {
        "memory_place": rc75_clean_emotional_text(order.get("yul_memory_place") or "", 140),
        "memory_detail": rc75_clean_emotional_text(order.get("yul_memory_detail") or "", 220),
        "emotion_tone": rc75_clean_emotional_text(order.get("yul_emotion_tone") or "", 80),
        "magic_hint": rc75_clean_emotional_text(order.get("yul_magic_hint") or "", 160),
    }

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
    if filename.endswith(".heic") or content_type in {"image/heic", "image/heif"}:
        return "heic"
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



async def save_upload_original_robust(order_id: str, slot_name: str, upload: UploadFile) -> str:
    """
    RC16 — guardado robusto de foto ORIGINAL.

    Objetivo:
    - No recortar.
    - No reescalar.
    - No comprimir.
    - No tocar orientación.
    - Guardar exactamente los bytes que llegan del navegador.
    - Ser más tolerante con iPhone / Instagram in-app browser.

    El video engine debe recibir estas fotos originales por /video/input.
    """
    if not upload:
        raise HTTPException(status_code=400, detail=f"{slot_name} no ha llegado")

    original_filename = (upload.filename or "").strip()
    content_type = (upload.content_type or "").lower().strip()

    if not original_filename:
        raise HTTPException(status_code=400, detail=f"{slot_name} no tiene nombre de archivo")

    filepath = build_photo_path(order_id, slot_name, upload)
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    # Muy importante en móviles/in-app browsers: asegurar puntero al inicio.
    try:
        await upload.seek(0)
    except Exception:
        try:
            upload.file.seek(0)
        except Exception:
            pass

    total = 0
    chunks = 0

    try:
        with open(filepath, "wb") as f:
            while True:
                chunk = await upload.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                total += len(chunk)
                chunks += 1
            try:
                f.flush()
                os.fsync(f.fileno())
            except Exception:
                pass
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{slot_name} no se pudo escribir en disco: {e}")

    # Fallback extra: algunos UploadFile quedan con stream raro; probamos lectura directa.
    if total <= 0:
        try:
            with open(filepath, "wb") as f:
                try:
                    upload.file.seek(0)
                except Exception:
                    pass
                data = upload.file.read()
                if data:
                    f.write(data)
                    total = len(data)
                    chunks = 1
                    try:
                        f.flush()
                        os.fsync(f.fileno())
                    except Exception:
                        pass
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"{slot_name} llegó vacío y falló el reintento: {e}")

    if not os.path.exists(filepath):
        raise HTTPException(status_code=400, detail=f"{slot_name} no se ha creado en disco")

    size = os.path.getsize(filepath)
    if size <= 0:
        try:
            os.remove(filepath)
        except Exception:
            pass
        raise HTTPException(status_code=400, detail=f"{slot_name} ha llegado vacío desde el navegador")

    # Validación mínima por firma de archivo. No transforma la imagen.
    with open(filepath, "rb") as f:
        head = f.read(32)

    looks_like_image = (
        head.startswith(b"\xff\xd8\xff") or     # jpg/jpeg
        head.startswith(b"\x89PNG\r\n\x1a\n") or # png
        head.startswith(b"RIFF") or              # webp
        b"ftypheic" in head or b"ftypheif" in head or b"ftypmif1" in head
    )

    if not looks_like_image:
        try:
            os.remove(filepath)
        except Exception:
            pass
        raise HTTPException(status_code=400, detail=f"{slot_name} no parece una imagen válida al guardarse")

    log_human(
        "FOTO ORIGINAL GUARDADA",
        f"🆔 Pedido: {order_id}",
        f"🖼️ Slot: {slot_name}",
        f"📄 Archivo: {original_filename}",
        f"📦 Tamaño: {size} bytes",
        f"🧩 Tipo: {content_type or 'desconocido'}",
        f"📍 Ruta original para engine: {filepath}",
    )

    return filepath



def reaction_video_path(order_id: str, extension: str = "webm") -> str:
    extension = (extension or "webm").lower().strip()
    if extension not in {"webm", "mp4"}:
        extension = "webm"
    REACTIONS_FOLDER.mkdir(parents=True, exist_ok=True)
    return str(REACTIONS_FOLDER / f"reaction_{order_id}.{extension}")


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


def upload_bytes_to_r2(data: bytes, remote_name: str, content_type: str = "application/octet-stream") -> Optional[str]:
    client = get_r2_client()
    if not client:
        return None
    client.put_object(Bucket=R2_BUCKET, Key=remote_name, Body=data, ContentType=content_type)
    return f"{R2_PUBLIC_URL}/{remote_name}"


def preserve_remote_video_to_r2(order: dict, video_url: str, kind: str = "original") -> Optional[str]:
    if not r2_enabled():
        log_human("ARCHIVO PERMANENTE R2", "ℹ️ R2 no está configurado. Uso la URL actual del vídeo.")
        return None

    url = (video_url or "").strip()
    if not url:
        return None

    try:
        log_human("GUARDANDO VÍDEO EN R2", f"🆔 Pedido: {order.get('id')}", f"🎞️ Tipo: {kind}")
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        content_type = response.headers.get("content-type") or guess_media_type_from_url(url)
        ext = "mp4" if "mp4" in content_type or url.split("?")[0].lower().endswith(".mp4") else "webm"
        digest = hashlib.sha256(response.content).hexdigest()[:16]
        filename = f"{kind}_{digest}.{ext}"
        key = r2_order_key(order, kind, filename)
        public_url = upload_bytes_to_r2(response.content, key, content_type=content_type)
        if public_url:
            insert_asset(order.get("id"), f"{kind}_r2", public_url, "r2")
            log_human("VÍDEO GUARDADO EN R2", "✅ Archivo permanente creado", f"🔗 {public_url}")
        return public_url
    except Exception as e:
        log_error(f"preserve_{kind}_to_r2", e)
        log_human("AVISO R2", "⚠️ No he podido copiar el vídeo a R2.", "✅ La experiencia sigue con la URL original.")
        return None


def insert_asset(order_id: str, asset_type: str, file_url: str, storage_provider: str):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO assets (order_id, asset_type, file_url, storage_provider, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (order_id, asset_type, file_url, storage_provider, now_iso()))
    conn.commit()
    conn.close()


def insert_order_event(order_id: str, step: str, status: str = "ok", message: str = "", meta: Optional[dict] = None):
    """Log humano por pedido: permite saber exactamente dónde se queda ETERNA."""
    try:
        readable_step = human_label(step)
        readable_status = human_label(status)
        icon = icon_for_step(step, status)
        clean_message = str(message or "").strip()

        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{icon} PASO ETERNA: {readable_step}")
        print(f"🆔 Pedido: {order_id or 'sin pedido'}")
        print(f"📍 Estado: {readable_status}")
        if clean_message:
            print(f"📝 Detalle: {clean_message}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        conn = db_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS order_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                step TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ok',
                message TEXT,
                meta_json TEXT,
                created_at TEXT NOT NULL
            )
        """)
        cur.execute("""
            INSERT INTO order_events (order_id, step, status, message, meta_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(order_id or ""),
            str(step or "unknown"),
            str(status or "ok"),
            str(message or ""),
            json.dumps(meta or {}, ensure_ascii=False),
            now_iso(),
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("⚠️ AVISO ETERNA: no pude guardar un evento del pedido")
        print(f"🧩 Paso: {step}")
        print(f"❌ Error: {e}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


def list_order_events(order_id: str, limit: int = 80):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS order_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                step TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ok',
                message TEXT,
                meta_json TEXT,
                created_at TEXT NOT NULL
            )
        """)
        cur.execute("""
            SELECT id, order_id, step, status, message, meta_json, created_at
            FROM order_events
            WHERE order_id = ?
            ORDER BY id DESC
            LIMIT ?
        """, (order_id, int(limit or 80)))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in reversed(rows)]
    except Exception as e:
        print("[WARN] list_order_events failed:", e)
        return []


def complete_reaction_from_local_file(order: dict, local_path: str, extension: str = "webm", source: str = "single_upload") -> dict:
    """Regla de oro: local primero, R2 después. Si local existe, ETERNA no se pierde."""
    if not local_path or not os.path.exists(local_path):
        raise Exception("reaction_local_file_missing")

    saved_size = os.path.getsize(local_path)
    if saved_size <= 0:
        raise Exception("reaction_local_file_empty")

    extension = (extension or "webm").lower().strip()
    if extension not in {"webm", "mp4"}:
        extension = "webm"

    insert_order_event(
        order["id"],
        "reaction_saved_local",
        "ok",
        "Reacción guardada localmente en el servidor",
        {"bytes": saved_size, "source": source, "path": local_path},
    )

    public_url = None
    r2_error = None
    try:
        content_type = guess_media_type_from_path(local_path)
        remote_name = r2_order_key(order, "reaction", f"reaction.{extension}")
        public_url = upload_video_to_r2(local_path, remote_name, content_type=content_type)
        insert_order_event(
            order["id"],
            "reaction_r2_uploaded" if public_url else "reaction_r2_skipped",
            "ok" if public_url else "pending",
            "Reacción subida a R2" if public_url else "R2 no configurado; se conserva local",
            {"public_url": public_url, "content_type": content_type},
        )
    except Exception as e:
        r2_error = str(e)
        insert_order_event(order["id"], "reaction_r2_pending", "warning", "R2 falló; la reacción queda segura localmente", {"error": r2_error})
        log_error("complete_reaction_r2_best_effort", e)

    update_order(
        order["id"],
        reaction_video_local=local_path,
        reaction_video_public_url=public_url,
        reaction_uploaded=1,
        experience_started=1,
        experience_completed=1,
        delivered_to_recipient=1,
        reaction_upload_pending=0,
        reaction_upload_error=r2_error,
        gift_refund_deadline_at=order.get("gift_refund_deadline_at") or gift_refund_deadline_iso(),
    )

    updated_order = maybe_mark_eterna_completed(order["id"])
    insert_order_event(updated_order["id"], "eterna_completed", "ok", "ETERNA completada: reacción segura y pack desbloqueado")

    try:
        print("📩 RC46: control SMS regalante; si la reacción aún no está estable, queda para worker")
        result = try_send_sender_sms(updated_order)
        print("📩 RESULTADO CONTROLADO REGALANTE:", result)
        insert_order_event(updated_order["id"], "sender_sms_attempt", "ok" if result.get("ok") else "pending", str(result), result)
    except Exception as e:
        insert_order_event(updated_order["id"], "sender_sms_error", "error", str(e))
        log_error("complete_reaction_try_send_sender_sms", e)

    try:
        payout_result = process_gift_transfer_for_order(updated_order)
        print("💸 PAYOUT DESDE REACTION COMPLETE:", payout_result)
        insert_order_event(updated_order["id"], "payout_attempt", "ok", str(payout_result), payout_result)
    except Exception as e:
        insert_order_event(updated_order["id"], "payout_error", "error", str(e))
        log_error("complete_reaction_payout", e)

    return updated_order


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


def reaction_file_ready_for_sender(order: dict, min_age_seconds: int = 30, min_size_bytes: int = 4096) -> tuple[bool, str]:
    """
    RC46: evita mandar el SMS de vuelta demasiado pronto.
    El SMS al regalante solo sale cuando la reacción local existe, pesa algo razonable
    y lleva unos segundos estable en disco. Si aún no está listo, NO consume intento SMS.
    """
    local_path = (order.get("reaction_video_local") or "").strip()
    if not local_path:
        if order.get("reaction_video_public_url"):
            return True, "public_url_available"
        return False, "reaction_local_path_missing"

    if not os.path.exists(local_path):
        return False, "reaction_local_file_missing"

    try:
        size_1 = os.path.getsize(local_path)
    except Exception:
        return False, "reaction_size_unreadable"

    if size_1 < int(min_size_bytes or 0):
        return False, "reaction_file_too_small"

    try:
        age = time.time() - os.path.getmtime(local_path)
    except Exception:
        age = 0

    if age < int(min_age_seconds or 0):
        return False, f"reaction_file_too_recent_{int(age)}s"

    try:
        time.sleep(1)
        size_2 = os.path.getsize(local_path)
        if size_2 != size_1:
            return False, "reaction_file_size_still_changing"
    except Exception:
        return False, "reaction_stability_check_failed"

    return True, "reaction_file_stable"


def reaction_is_safe(order: dict) -> bool:
    return bool(order.get("reaction_uploaded")) and reaction_exists(order)


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
            order["id"],
            eterna_completed=1,
            experience_started=1,
            experience_completed=1,
            delivered_to_recipient=1,
            reaction_upload_pending=0,
            reaction_upload_error=None,
            gift_refund_deadline_at=order.get("gift_refund_deadline_at") or gift_refund_deadline_iso(),
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

    log_human("PREPARANDO VÍDEO", f"🆔 Pedido: {order_id}", "🎬 Enviando fotos y frases al motor de vídeo")
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



# =========================================================
# RC53 — BLINDAJE PRELANZAMIENTO
# Estados únicos, locks anti-bucle y recuperación tras reinicio.
# No cambia Stripe/Twilio/video engine; solo añade cinturón de seguridad.
# =========================================================

ORDER_STATES = {
    "CREATED",
    "PAID",
    "RENDERING",
    "VIDEO_READY",
    "DELIVERED_TO_RECIPIENT",
    "EXPERIENCE_STARTED",
    "REACTION_UPLOADED",
    "SENDER_PACK_READY",
    "COMPLETED",
    "FAILED",
}

def set_order_state(order_id: str, state: str, reason: str = ""):
    state = (state or "").strip().upper()
    if state not in ORDER_STATES:
        state = "FAILED"
    try:
        update_order(order_id, order_state=state)
        insert_order_event(order_id, "state_change", "ok", state, {"reason": reason})
    except Exception as e:
        print("⚠️ No pude marcar estado:", order_id, state, e)

def acquire_order_processing_lock(order_id: str, field: str, at_field: str, max_age_seconds: int = 600) -> bool:
    """
    Lock SQLite atómico:
    - evita dos SMS duplicados
    - evita dos workers pisándose
    - libera locks viejos tras reinicio/caída
    """
    now = now_iso()
    cutoff = (now_dt() - timedelta(seconds=max_age_seconds)).isoformat()
    conn = db_conn()
    cur = conn.cursor()
    try:
        cur.execute(f"""
            UPDATE orders
            SET {field}=1, {at_field}=?, updated_at=?
            WHERE id=?
              AND (
                    COALESCE({field},0)=0
                    OR {at_field} IS NULL
                    OR {at_field} < ?
              )
        """, (now, now, order_id, cutoff))
        conn.commit()
        return cur.rowcount == 1
    finally:
        conn.close()

def release_order_processing_lock(order_id: str, field: str, at_field: str):
    try:
        update_order(order_id, **{field: 0, at_field: None})
    except Exception as e:
        print("⚠️ No pude liberar lock:", order_id, field, e)

def recover_stale_processing_locks(max_age_minutes: int = 15):
    """
    Al arrancar Render, limpia locks antiguos para que un deploy no deje pedidos muertos.
    """
    cutoff = (now_dt() - timedelta(minutes=max_age_minutes)).isoformat()
    conn = db_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE orders
            SET delivery_processing_lock=0,
                delivery_processing_lock_at=NULL,
                sender_sms_processing_lock=0,
                sender_sms_processing_lock_at=NULL,
                last_recovery_at=?,
                last_recovery_reason='stale_processing_lock_released',
                updated_at=?
            WHERE
                (COALESCE(delivery_processing_lock,0)=1 AND delivery_processing_lock_at IS NOT NULL AND delivery_processing_lock_at < ?)
                OR
                (COALESCE(sender_sms_processing_lock,0)=1 AND sender_sms_processing_lock_at IS NOT NULL AND sender_sms_processing_lock_at < ?)
        """, (now_iso(), now_iso(), cutoff, cutoff))
        changed = cur.rowcount
        conn.commit()
        if changed:
            print(f"🛡️ RC53 recuperación: locks antiguos liberados: {changed}")
    except Exception as e:
        print("⚠️ RC53 recuperación locks falló:", e)
    finally:
        conn.close()

def normalize_order_state_from_flags(order: dict) -> str:
    if bool(order.get("eterna_completed")):
        return "COMPLETED"
    if bool(order.get("reaction_uploaded")) and reaction_exists(order):
        return "SENDER_PACK_READY"
    if bool(order.get("experience_started")):
        return "EXPERIENCE_STARTED"
    if bool(order.get("delivery_sent")) or bool(order.get("delivered_to_recipient")):
        return "DELIVERED_TO_RECIPIENT"
    if original_video_ready(order):
        return "VIDEO_READY"
    if bool(order.get("video_render_requested")):
        return "RENDERING"
    if bool(order.get("paid")):
        return "PAID"
    return "CREATED"

def recover_order_states_from_flags():
    """
    No cambia negocio: solo rellena order_state para trazabilidad y rescate.
    """
    conn = db_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM orders")
        ids = [r["id"] for r in cur.fetchall()]
    finally:
        conn.close()
    for oid in ids:
        try:
            order = get_order_by_id(oid)
            state = normalize_order_state_from_flags(order)
            if (order.get("order_state") or "") != state:
                update_order(oid, order_state=state)
        except Exception as e:
            print("⚠️ No pude normalizar estado:", oid, e)

def sender_pack_url_from_order(order: dict) -> str:
    return f"{PUBLIC_BASE_URL}/sender/{order['sender_token']}"


def recipient_experience_url_from_order(order: dict) -> str:
    return f"{PUBLIC_BASE_URL}/pedido/{order['recipient_token']}"


def build_recipient_message(order: dict) -> str:
    recipient_name = (order.get("recipient_name") or "").strip()
    url = (recipient_experience_url_from_order(order) or "").strip()
    greeting = f"{recipient_name}," if recipient_name else ""
    message = ""
    if greeting:
        message += f"Shhh…\n\n{greeting}\n\n"
    else:
        message += "Shhh…\n\n"
    message += (
        "Esto no es un vídeo.\n\n"
        "No es solo un momento.\n\n"
        "Es algo que alguien ha creado para ti.\n\n"
        "Pero hay algo más…\n\n"
        "Dentro hay algo que también es tuyo.\n\n"
        "Ábrelo cuando estés tranquilo:\n\n"
        f"{url}"
    )
    return message.strip()


def build_sender_ready_message(order: dict) -> str:
    sender_name = (order.get("sender_name") or "").strip()
    url = (sender_pack_url_from_order(order) or "").strip()
    greeting = f"{sender_name}," if sender_name else ""
    message = ""
    if greeting:
        message += f"{greeting}\n\n"
    message += (
        "Ya ha pasado.\n\n"
        "Tu ETERNA ha vuelto.\n\n"
        "Lo que diste…\n"
        "ya ha encontrado el camino de vuelta.\n\n"
        "Ahora puedes verlo aquí:\n\n"
        f"{url}"
    )
    return message.strip()


def try_send_sender_sms(order: dict) -> dict:
    order = get_order_by_id(order["id"])

    if not bool(order.get("paid")):
        return {"ok": False, "reason": "order_not_paid"}

    if not bool(order.get("reaction_uploaded")):
        return {"ok": False, "reason": "reaction_not_uploaded"}

    if not reaction_exists(order):
        return {"ok": False, "reason": "reaction_not_found"}

    ready_for_sender, ready_reason = reaction_file_ready_for_sender(order, min_age_seconds=30)
    if not ready_for_sender:
        print("⏳ SMS regalante retenido hasta reacción estable:", ready_reason)
        return {"ok": False, "reason": ready_reason, "retry": True, "no_attempt_increment": True}

    attempts = int(order.get("sender_sms_attempts") or 0)

    if bool(order.get("sender_sms_sent_at")):
        set_order_state(order["id"], "SENDER_PACK_READY", "sender_sms_already_sent")
        return {
            "ok": True,
            "reason": "already_sent",
            "sid": order.get("sender_sms_sid"),
            "sender_sms_sent_at": order.get("sender_sms_sent_at"),
            "sender_sms_attempts": attempts,
            "sender_sms_error": order.get("sender_sms_error"),
        }

    if attempts >= 3:
        insert_order_event(order["id"], "sender_sms_error", "warning", "Máximo de intentos de SMS al regalante alcanzado", {"attempts": attempts})
        return {
            "ok": False,
            "reason": "max_attempts_reached",
            "sender_sms_sent_at": order.get("sender_sms_sent_at"),
            "sender_sms_attempts": attempts,
            "sender_sms_error": order.get("sender_sms_error"),
        }

    locked = acquire_order_processing_lock(
        order["id"],
        "sender_sms_processing_lock",
        "sender_sms_processing_lock_at",
        max_age_seconds=600,
    )
    if not locked:
        return {"ok": False, "reason": "sender_sms_locked", "retry": True, "no_attempt_increment": True}

    try:
        order = get_order_by_id(order["id"])
        attempts = int(order.get("sender_sms_attempts") or 0)

        if bool(order.get("sender_sms_sent_at")):
            return {
                "ok": True,
                "reason": "already_sent_after_lock",
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
        print("📩 RC53 ENVIANDO MENSAJE REGALANTE A:", order.get("sender_phone", ""))
        result = send_message_best_effort(order.get("sender_phone", ""), message)

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
            set_order_state(order["id"], "SENDER_PACK_READY", "sender_sms_sent")

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
    finally:
        release_order_processing_lock(order["id"], "sender_sms_processing_lock", "sender_sms_processing_lock_at")

def calculate_fees(gift_amount: float, delivery_mode: str) -> dict:
    gift_amount = max(0.0, round(float(gift_amount or 0), 2))

    # Regla clara de precios ETERNA:
    # - Si NO hay regalo económico: solo BASE_PRICE.
    # - Si hay regalo económico: +2€ gestión segura + 5% del importe regalado.
    # - Si entrega programada: +2€ SOLO por programación.
    has_gift = gift_amount > 0
    fixed_fee = round(FIXED_PLATFORM_FEE if has_gift else 0.0, 2)
    variable_fee = round(gift_amount * GIFT_COMMISSION_RATE if has_gift else 0.0, 2)

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
        "amistad": [
            "Hay personas que aparecen",
            "y se quedan para siempre.",
            "Gracias por estar.",
        ],
        "madre": [
            "Nunca podré devolverte todo.",
            "Pero sí recordarte lo importante que eres.",
            "Gracias por ser hogar.",
        ],
        "padre": [
            "Aunque no siempre lo diga,",
            "muchas cosas que soy empezaron contigo.",
            "Gracias por todo.",
        ],
        "distancia": [
            "Aunque hoy no estés cerca,",
            "hay algo de ti que sigue aquí.",
            "Y eso no se va.",
        ],
        "perdon": [
            "A veces cuesta decirlo.",
            "Pero hay cosas que merecen sanar.",
            "Ojalá esto llegue donde mis palabras no llegaron.",
        ],
        "reencuentro": [
            "Hay caminos que se separan,",
            "pero hay recuerdos que vuelven.",
            "Y este vuelve para ti.",
        ],
        "gratitud": [
            "A veces no sabemos cómo decirlo.",
            "Pero hay personas que cambian la vida.",
            "Y tú eres una de ellas.",
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
        "no_se_decirlo": [
            "No siempre encuentro las palabras.",
            "Pero sí sé lo que siento.",
            "Y quería que lo vivieras así.",
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
        log_human("SMS APAGADO", f"📱 Destino: {mask_phone(to_phone)}", "ℹ️ No envío nada porque SMS_ENABLED=0")
        print("🚫 SMS DESACTIVADO POR CONFIG")
        print("🚫 Destino:", to_phone)
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


def whatsapp_from_number() -> str:
    raw = (TWILIO_WHATSAPP_FROM or "").strip()
    if not raw:
        return ""
    if raw.startswith("whatsapp:"):
        return raw
    return f"whatsapp:{raw}"


def send_whatsapp(phone: str, message: str) -> dict:
    to_phone = to_e164(phone)
    wa_from = whatsapp_from_number()
    if not to_phone:
        return {"ok": False, "channel": "whatsapp", "sid": None, "error": "invalid_phone"}
    if not WHATSAPP_ENABLED:
        return {"ok": False, "channel": "whatsapp", "sid": None, "error": "whatsapp_disabled"}
    if not wa_from:
        return {"ok": False, "channel": "whatsapp", "sid": None, "error": "missing_twilio_whatsapp_from"}
    if not twilio_enabled():
        return {"ok": False, "channel": "whatsapp", "sid": None, "error": "twilio_not_configured"}
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(body=message, from_=wa_from, to=f"whatsapp:{to_phone}")
        return {"ok": True, "channel": "whatsapp", "sid": msg.sid, "error": None}
    except Exception as e:
        return {"ok": False, "channel": "whatsapp", "sid": None, "error": str(e)}


def send_message_best_effort(phone: str, message: str) -> dict:
    whatsapp_result = send_whatsapp(phone, message)
    if whatsapp_result.get("ok"):
        return whatsapp_result
    sms_result = send_sms(phone, message)
    if sms_result.get("ok"):
        sms_result["fallback_from"] = "whatsapp"
        sms_result["whatsapp_error"] = whatsapp_result.get("error")
        return sms_result
    return {
        "ok": False,
        "channel": "none",
        "sid": None,
        "error": "whatsapp_error=" + str(whatsapp_result.get("error")) + " | sms_error=" + str(sms_result.get("error")),
        "whatsapp_error": whatsapp_result.get("error"),
        "sms_error": sms_result.get("error"),
    }

def send_admin_alert(message: str):
    try:
        if not ADMIN_ALERT_PHONE:
            return
        send_sms(ADMIN_ALERT_PHONE, message)
    except Exception as e:
        log_error("admin_alert_sms", e)


def build_admin_eterna_completed_message(order: dict) -> str:
    sender = order.get("sender_name") or ""
    recipient = order.get("recipient_name") or ""

    ida = order.get("experience_video_url") or ""
    vuelta = sender_pack_url_from_order(order)

    return (
        "✨ Tu ETERNA completada\n\n"
        f"{sender} → {recipient}\n\n"
        "IDA:\n"
        f"{ida}\n\n"
        "VUELTA:\n"
        f"{vuelta}"
    )


def send_admin_eterna_completed(order: dict):
    try:
        msg = build_admin_eterna_completed_message(order)
        send_admin_alert(msg)
    except Exception as e:
        log_error("admin_eterna_completed", e)

def process_scheduled_recipient_delivery(order_id: str) -> dict:
    order = get_order_by_id(order_id)

    log_human("ENTREGA AL DESTINATARIO", f"🆔 Pedido: {order_id}", "📩 Voy a preparar el envío del enlace")
    print("📦 PROCESS RECIPIENT DELIVERY START")
    print("➡️ order_id:", order_id)

    if bool(order.get("delivery_sent")) or bool(order.get("delivery_sent_at")):
        set_order_state(order_id, "DELIVERED_TO_RECIPIENT", "recipient_delivery_already_sent")
        return {
            "ok": True,
            "reason": "already_sent",
            "delivery_sent": True,
            "delivery_sent_at": order.get("delivery_sent_at"),
            "recipient_sms_sent_at": order.get("recipient_sms_sent_at"),
            "recipient_sms_attempts": int(order.get("recipient_sms_attempts") or 0),
            "recipient_sms_error": order.get("recipient_sms_error"),
        }

    locked = acquire_order_processing_lock(
        order_id,
        "delivery_processing_lock",
        "delivery_processing_lock_at",
        max_age_seconds=600,
    )
    if not locked:
        return {
            "ok": False,
            "reason": "delivery_processing_locked",
            "delivery_sent": False,
            "retry": True,
            "no_attempt_increment": True,
        }

    try:
        order = get_order_by_id(order_id)

        if bool(order.get("delivery_sent")) or bool(order.get("delivery_sent_at")):
            set_order_state(order_id, "DELIVERED_TO_RECIPIENT", "recipient_delivery_already_sent_after_lock")
            return {
                "ok": True,
                "reason": "already_sent_after_lock",
                "delivery_sent": True,
                "delivery_sent_at": order.get("delivery_sent_at"),
                "recipient_sms_sent_at": order.get("recipient_sms_sent_at"),
                "recipient_sms_attempts": int(order.get("recipient_sms_attempts") or 0),
                "recipient_sms_error": order.get("recipient_sms_error"),
            }

        attempts = int(order.get("recipient_sms_attempts") or 0)

        if attempts >= 3:
            insert_order_event(order_id, "recipient_sms_failed", "warning", "Máximo de intentos al destinatario alcanzado", {"attempts": attempts})
            return {
                "ok": False,
                "reason": "max_attempts_reached",
                "delivery_sent": False,
                "delivery_sent_at": order.get("delivery_sent_at"),
                "recipient_sms_sent_at": order.get("recipient_sms_sent_at"),
                "recipient_sms_attempts": attempts,
                "recipient_sms_error": order.get("recipient_sms_error"),
            }

        if not bool(order.get("paid")):
            return {"ok": False, "reason": "order_not_paid", "delivery_sent": False}

        if not original_video_ready(order):
            set_order_state(order_id, "RENDERING" if bool(order.get("video_render_requested")) else "PAID", "original_video_not_ready")
            return {"ok": False, "reason": "original_video_not_ready", "delivery_sent": False}

        if not delivery_is_unlocked(order):
            return {
                "ok": False,
                "reason": "scheduled_delivery_not_ready",
                "delivery_sent": False,
                "scheduled_delivery_at": order.get("scheduled_delivery_at"),
                "scheduled_delivery_display": scheduled_delivery_display(order),
            }

        message = build_recipient_message(order)
        print("📩 RC53 ENVIANDO MENSAJE DESTINATARIO A:", order.get("recipient_phone", ""))
        result = send_message_best_effort(order.get("recipient_phone", ""), message)

        print("📩 RECIPIENT SMS RESULT:", result)

        attempts = attempts + 1

        sms_ok = bool(result.get("ok"))
        sms_sid = (result.get("sid") or "").strip() or None
        sms_error = (result.get("error") or "").strip() or None
        sms_reason = (result.get("reason") or "").strip().lower()

        success = bool(sms_ok or sms_sid or sms_reason in {"accepted", "queued", "sent"})

        if success:
            sent_at = now_iso()

            update_order(
                order_id,
                recipient_sms_attempts=attempts,
                recipient_sms_error=None,
                recipient_sms_sid=sms_sid,
                recipient_sms_sent_at=sent_at,
                delivery_sent=1,
                delivery_sent_at=sent_at,
                delivered_to_recipient=1,
            )
            set_order_state(order_id, "DELIVERED_TO_RECIPIENT", "recipient_sms_sent")

            updated = get_order_by_id(order_id)
            insert_order_event(order_id, "recipient_sms_sent", "ok", "SMS/enlace enviado al destinatario", {"sid": updated.get("recipient_sms_sid"), "attempts": int(updated.get("recipient_sms_attempts") or 0)})

            return {
                "ok": True,
                "reason": "sent",
                "delivery_sent": True,
                "delivery_sent_at": updated.get("delivery_sent_at"),
                "recipient_sms_sent_at": updated.get("recipient_sms_sent_at"),
                "recipient_sms_sid": updated.get("recipient_sms_sid"),
                "recipient_sms_attempts": int(updated.get("recipient_sms_attempts") or 0),
                "recipient_sms_error": updated.get("recipient_sms_error"),
            }

        final_error = sms_error or sms_reason or "sms_error"

        update_order(
            order_id,
            recipient_sms_attempts=attempts,
            recipient_sms_error=final_error,
        )

        updated = get_order_by_id(order_id)
        insert_order_event(order_id, "recipient_sms_failed", "error", final_error, {"attempts": int(updated.get("recipient_sms_attempts") or 0)})

        return {
            "ok": False,
            "reason": final_error,
            "delivery_sent": bool(updated.get("delivery_sent")),
            "delivery_sent_at": updated.get("delivery_sent_at"),
            "recipient_sms_sent_at": updated.get("recipient_sms_sent_at"),
            "recipient_sms_sid": updated.get("recipient_sms_sid"),
            "recipient_sms_attempts": int(updated.get("recipient_sms_attempts") or 0),
            "recipient_sms_error": updated.get("recipient_sms_error"),
        }
    finally:
        release_order_processing_lock(order_id, "delivery_processing_lock", "delivery_processing_lock_at")

# =========================================================
# RESCATE AUTOMÁTICO DE REACCIÓN POR CHUNKS
# =========================================================

def _chunk_session_info(session_folder: Path) -> dict:
    chunk_files = sorted(session_folder.glob("chunk_*.part"))
    manifest_path = session_folder / "manifest.json"
    extension = "webm"
    mode = "unknown"
    updated_ts = 0.0

    try:
        updated_ts = max([p.stat().st_mtime for p in chunk_files] + ([manifest_path.stat().st_mtime] if manifest_path.exists() else [session_folder.stat().st_mtime]))
    except Exception:
        updated_ts = 0.0

    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            extension = (manifest.get("extension") or "webm").lower().strip()
            mode = (manifest.get("mode") or "unknown").strip()
        except Exception:
            pass

    if extension not in {"webm", "mp4"}:
        extension = "webm"

    size = 0
    for part in chunk_files:
        try:
            size += part.stat().st_size
        except Exception:
            pass

    return {
        "folder": session_folder,
        "chunk_files": chunk_files,
        "chunks": len(chunk_files),
        "extension": extension,
        "mode": mode,
        "updated_ts": updated_ts,
        "size": size,
    }


def find_latest_reaction_chunk_session(order_id: str) -> Optional[dict]:
    base = REACTION_CHUNKS_FOLDER / str(order_id)
    if not base.exists():
        return None

    sessions = []
    try:
        for session_folder in base.iterdir():
            if not session_folder.is_dir():
                continue
            info = _chunk_session_info(session_folder)
            if info.get("chunks", 0) > 0 and info.get("size", 0) > 0:
                sessions.append(info)
    except Exception as e:
        log_error("find_latest_reaction_chunk_session", e)
        return None

    if not sessions:
        return None

    sessions.sort(key=lambda item: item.get("updated_ts", 0), reverse=True)
    return sessions[0]


def recover_reaction_from_chunks_if_possible(order_or_id, min_idle_seconds: int = 0, source: str = "auto_recovery") -> dict:
    """
    Rescate final ETERNA:
    Si el destinatario corta justo al final y no llega a ejecutar /finish-reaction-upload,
    pero ya hay chunks progresivos en /data/reaction_chunks, ensamblamos lo recibido,
    marcamos reaction_uploaded=1 y disparamos el SMS del sender pack.
    """
    order = get_order_by_id(order_or_id) if isinstance(order_or_id, str) else dict(order_or_id)

    if reaction_is_safe(order):
        return {"ok": True, "reason": "already_safe", "order_id": order.get("id")}

    if not bool(order.get("paid")):
        return {"ok": False, "reason": "order_not_paid", "order_id": order.get("id")}

    if not original_video_ready(order):
        return {"ok": False, "reason": "original_video_not_ready", "order_id": order.get("id")}

    session = find_latest_reaction_chunk_session(order["id"])
    if not session:
        return {"ok": False, "reason": "no_chunks_found", "order_id": order.get("id")}

    if int(min_idle_seconds or 0) > 0:
        age = max(0.0, time.time() - float(session.get("updated_ts") or 0))
        if age < int(min_idle_seconds):
            return {
                "ok": False,
                "reason": "chunks_still_active",
                "order_id": order.get("id"),
                "seconds_since_last_chunk": round(age, 2),
                "required_idle_seconds": int(min_idle_seconds),
            }

    chunk_files = session.get("chunk_files") or []
    if not chunk_files:
        return {"ok": False, "reason": "no_chunk_files", "order_id": order.get("id")}

    extension = session.get("extension") or "webm"
    local_path = reaction_video_path(order["id"], extension)

    try:
        insert_order_event(
            order["id"],
            "reaction_auto_recovery_started",
            "warning",
            "Rescate automático: había trozos de grabación pero no se había cerrado la reacción",
            {
                "source": source,
                "session_folder": str(session.get("folder")),
                "chunks": len(chunk_files),
                "bytes": session.get("size"),
                "extension": extension,
            },
        )

        with open(local_path, "wb") as out:
            for part_path in chunk_files:
                with open(part_path, "rb") as part:
                    out.write(part.read())

        saved_size = os.path.getsize(local_path) if os.path.exists(local_path) else 0
        if saved_size <= 0:
            raise Exception("auto_recovery_empty_file")

        if saved_size > MAX_VIDEO_SIZE:
            update_order(order["id"], reaction_upload_pending=1, reaction_upload_error="auto_recovery_video_too_large")
            insert_order_event(order["id"], "reaction_auto_recovery_too_large", "error", "El rescate ensamblado pesa demasiado", {"bytes": saved_size, "max_bytes": MAX_VIDEO_SIZE})
            return {"ok": False, "reason": "video_too_large", "order_id": order.get("id"), "bytes": saved_size}

        updated_order = complete_reaction_from_local_file(order, local_path, extension=extension, source=source)

        insert_order_event(
            order["id"],
            "reaction_auto_recovery_completed",
            "ok",
            "Reacción rescatada automáticamente y sender pack desbloqueado",
            {"bytes": saved_size, "chunks": len(chunk_files), "source": source},
        )

        return {
            "ok": True,
            "reason": "recovered",
            "order_id": order.get("id"),
            "bytes": saved_size,
            "chunks": len(chunk_files),
            "sender_sms_sent_at": updated_order.get("sender_sms_sent_at"),
            "sender_sms_attempts": int(updated_order.get("sender_sms_attempts") or 0),
            "sender_sms_error": updated_order.get("sender_sms_error"),
        }

    except Exception as e:
        update_order(order["id"], reaction_upload_pending=1, reaction_upload_error=str(e))
        insert_order_event(order["id"], "reaction_auto_recovery_failed", "error", str(e), {"source": source})
        log_error("recover_reaction_from_chunks_if_possible", e)
        return {"ok": False, "reason": str(e), "order_id": order.get("id")}


def list_pending_reaction_recovery_orders(limit: int = 25) -> list[str]:
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id
        FROM orders
        WHERE COALESCE(paid, 0) = 1
          AND COALESCE(reaction_uploaded, 0) = 0
          AND COALESCE(experience_started, 0) = 1
          AND COALESCE(reaction_upload_pending, 0) = 1
          AND experience_video_url IS NOT NULL
          AND TRIM(experience_video_url) != ''
        ORDER BY updated_at ASC
        LIMIT ?
    """, (int(limit or 25),))
    rows = cur.fetchall()
    conn.close()
    return [str(r["id"]) for r in rows]


def process_all_pending_reaction_recoveries() -> list[dict]:
    results = []
    for order_id in list_pending_reaction_recovery_orders():
        try:
            result = recover_reaction_from_chunks_if_possible(order_id, min_idle_seconds=20, source="worker_auto_recovery")
            if result.get("ok"):
                print("🎥 Worker reaction recovery:", order_id, result)
            results.append({"order_id": order_id, "result": result})
        except Exception as e:
            log_error("reaction_recovery_worker_process", e)
            results.append({"order_id": order_id, "result": {"ok": False, "reason": str(e)}})
    return results


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
            transfer_started_at = ?,
            updated_at = ?
        WHERE id = ?
          AND COALESCE(transfer_in_progress, 0) = 0
          AND COALESCE(transfer_completed, 0) = 0
        """,
        (now_iso(), now_iso(), order_id),
    )
    conn.commit()
    acquired = cur.rowcount == 1
    conn.close()
    return acquired


def release_transfer_lock(order_id: str):
    update_order(order_id, transfer_in_progress=0, transfer_started_at=None)


def recover_stuck_transfer_if_needed(order: dict, max_age_seconds: int = 600) -> dict:
    if not bool(order.get("transfer_in_progress")):
        return order

    started_at = parse_iso_dt(order.get("transfer_started_at") or "")
    if started_at and (now_dt() - started_at).total_seconds() < max_age_seconds:
        return order

    print("⚠️ PAYOUT LOCK RECOVERY:", order.get("id"))
    update_order(order["id"], transfer_in_progress=0, transfer_started_at=None)
    return get_order_by_id(order["id"])


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
    """
    RC74 FULL: marca render en curso con estado visible.
    No cambia el video engine. Solo hace trazable la cola.
    """
    now = now_iso()
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE orders
        SET
            video_render_requested = 1,
            video_render_requested_at = ?,
            render_status = 'RENDERING',
            render_started_at = ?,
            render_attempts = COALESCE(render_attempts, 0) + 1,
            render_last_error = NULL,
            order_state = 'RENDERING',
            order_version = COALESCE(order_version, ?),
            updated_at = ?
        WHERE id = ?
    """, (now, now, ETERNA_APP_VERSION, now, order_id))
    conn.commit()
    conn.close()
    insert_order_event(order_id, "RENDER_STARTED", "ok", "Render marcado como iniciado", {"version": ETERNA_APP_VERSION})


def clear_video_render_requested(order_id: str, error: str = ""):
    """
    RC74 FULL: devuelve pedido a cola si el render no pudo arrancar.
    Nunca borra pedido. Nunca pierde estado.
    """
    update_order(
        order_id,
        video_render_requested=0,
        video_render_requested_at=None,
        render_status="PENDING_RENDER",
        render_started_at=None,
        render_last_error=str(error or "")[:1000],
        order_state="PENDING_RENDER",
        recovery_notes=str(error or "")[:1000],
    )
    insert_order_event(order_id, "RENDER_REQUEUED", "warning", "Render devuelto a cola", {"error": str(error or "")[:1000]})


def recipient_cookie_name(recipient_token: str) -> str:
    return f"eterna_recipient_session_{recipient_token}"


def get_recipient_cookie_value(request: Request, recipient_token: str) -> str:
    return (request.cookies.get(recipient_cookie_name(recipient_token)) or "").strip()


def has_valid_recipient_session(order: dict, request: Request) -> bool:
    cookie_key = recipient_cookie_name(order["recipient_token"])
    expected = (order.get("recipient_session_token") or "").strip()
    got = (request.cookies.get(cookie_key) or "").strip()
    experience_started = bool(order.get("experience_started"))
    experience_completed = bool(order.get("experience_completed"))
    reaction_uploaded = bool(order.get("reaction_uploaded"))
    if not experience_started:
        return True
    if experience_completed or reaction_uploaded:
        if not expected:
            return True
        try:
            if got and secrets.compare_digest(expected, got):
                return True
        except Exception:
            pass
        return False
    return True


def attach_recipient_session_if_needed(order: dict, request: Request, response) -> bool:
    cookie_key = recipient_cookie_name(order["recipient_token"])
    expected = (order.get("recipient_session_token") or "").strip()
    got = (request.cookies.get(cookie_key) or "").strip()
    experience_completed = bool(order.get("experience_completed"))
    reaction_uploaded = bool(order.get("reaction_uploaded"))
    if expected and got:
        try:
            if secrets.compare_digest(expected, got):
                return True
        except Exception:
            pass
    if not expected:
        new_session = new_token()
        update_order(order["id"], recipient_session_token=new_session, recipient_session_claimed_at=now_iso())
        response.set_cookie(key=cookie_key, value=new_session, max_age=60 * 60 * 24 * 365 * 5, httponly=True, secure=COOKIE_SECURE, samesite="lax", path="/")
        return True
    if not experience_completed and not reaction_uploaded:
        response.set_cookie(key=cookie_key, value=expected, max_age=60 * 60 * 24 * 365 * 5, httponly=True, secure=COOKIE_SECURE, samesite="lax", path="/")
        return True
    return False


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
                    radial-gradient(circle at top, rgba(218,178,92,0.16), transparent 34%),
                    linear-gradient(180deg, #020817 0%, #000000 58%, #020817 100%);
                color: #fff7e6;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
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
                background: linear-gradient(135deg, #fff0bd 0%, #e4bd69 45%, #b9822f 100%);
                color: #120b02;
                text-decoration: none;
                font-weight: bold;
                font-size: 15px;
            }
            .ghost {
                background: rgba(218,178,92,0.10);
                color: #fff7e6;
                border: 1px solid rgba(218,178,92,0.22);
            }
        </style>
    </head>
    <body>


<div aria-hidden="true" data-eterna-cinematic-scene="1" style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:1;mix-blend-mode:screen;">
    <div style="position:absolute;inset:-18%;background:radial-gradient(circle at 76% 18%,rgba(92,191,255,.28),transparent 24%),radial-gradient(circle at 63% 52%,rgba(23,82,190,.24),transparent 30%),radial-gradient(circle at 18% 82%,rgba(218,178,92,.12),transparent 28%);filter:blur(2px);opacity:.95;"></div>
    <svg viewBox="0 0 900 900" preserveAspectRatio="xMidYMid slice" style="position:absolute;inset:-7%;width:114%;height:114%;opacity:.98;filter:drop-shadow(0 0 26px rgba(125,210,255,.72)) drop-shadow(0 0 82px rgba(37,99,235,.42));" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="cinema_core" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
                <stop offset="20%" stop-color="#dff6ff" stop-opacity=".92"/>
                <stop offset="58%" stop-color="#69bfff" stop-opacity=".46"/>
                <stop offset="100%" stop-color="#061428" stop-opacity="0"/>
            </radialGradient>
            <linearGradient id="cinema_wing" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#ffffff" stop-opacity=".96"/>
                <stop offset="22%" stop-color="#c7eeff" stop-opacity=".88"/>
                <stop offset="58%" stop-color="#4aa4ff" stop-opacity=".56"/>
                <stop offset="100%" stop-color="#071c4b" stop-opacity=".08"/>
            </linearGradient>
            <filter id="wingTexture" x="-30%" y="-30%" width="160%" height="160%">
                <feTurbulence type="fractalNoise" baseFrequency="0.012 0.032" numOctaves="4" seed="8" result="noise"/>
                <feDisplacementMap in="SourceGraphic" in2="noise" scale="10" xChannelSelector="R" yChannelSelector="G"/>
                <feGaussianBlur stdDeviation="0.25"/>
            </filter>
            <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
                <feGaussianBlur stdDeviation="14" result="blur"/>
                <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
        </defs>
        <g opacity=".95">
            <path d="M836 83 C724 138 657 212 597 300 C538 388 476 430 403 461 C310 500 202 506 83 606" fill="none" stroke="#72d8ff" stroke-width="3" stroke-linecap="round" opacity=".28"/>
            <path d="M812 128 C706 169 638 237 585 318 C532 399 458 460 375 492 C284 528 186 536 91 626" fill="none" stroke="#f6c56f" stroke-width="2" stroke-linecap="round" opacity=".18"/>
            <path d="M850 178 C743 199 660 259 595 351 C530 443 451 507 360 544" fill="none" stroke="#b6ecff" stroke-width="1.4" stroke-linecap="round" opacity=".20"/>
        </g>
        <g opacity=".96">
            <animateTransform attributeName="transform" type="translate" values="0 0;-14 -20;0 0" dur="12s" repeatCount="indefinite"/>
            <circle cx="640" cy="222" r="250" fill="url(#cinema_core)" opacity=".28" filter="url(#softGlow)"/>
            <g filter="url(#wingTexture)" opacity=".96">
                <path d="M626 226 C535 85 523 12 592 8 C681 2 694 140 642 229 Z" fill="url(#cinema_wing)" opacity=".92"/>
                <path d="M655 226 C703 80 810 8 866 57 C928 112 794 211 669 244 Z" fill="url(#cinema_wing)" opacity=".92"/>
                <path d="M622 244 C508 233 451 278 485 332 C526 398 599 324 637 254 Z" fill="url(#cinema_wing)" opacity=".70"/>
                <path d="M667 250 C772 233 849 276 814 337 C776 402 699 326 655 256 Z" fill="url(#cinema_wing)" opacity=".70"/>
                <path d="M646 168 C655 201 655 242 646 315" stroke="#f9feff" stroke-width="10" stroke-linecap="round" opacity=".72"/>
                <path d="M590 50 C620 92 632 139 642 199 M735 62 C700 105 675 155 657 205 M515 278 C561 263 600 255 634 251 M791 282 C744 266 704 257 666 252" stroke="#ffffff" stroke-width="2.2" stroke-opacity=".32" fill="none"/>
            </g>
        </g>
        <g opacity=".86">
            <animate attributeName="opacity" values=".55;.95;.55" dur="5.5s" repeatCount="indefinite"/>
            <circle cx="796" cy="149" r="2.8" fill="#e8fbff"/><circle cx="752" cy="176" r="1.8" fill="#74d7ff"/><circle cx="706" cy="210" r="2.1" fill="#f7ca78"/><circle cx="650" cy="253" r="1.6" fill="#c8f2ff"/><circle cx="594" cy="300" r="1.7" fill="#82d8ff"/><circle cx="528" cy="359" r="1.9" fill="#f4c771"/><circle cx="456" cy="421" r="1.4" fill="#b8eeff"/><circle cx="375" cy="488" r="1.6" fill="#81d9ff"/><circle cx="284" cy="529" r="1.2" fill="#f7cf83"/>
        </g>
        <g opacity=".62" filter="url(#softGlow)">
            <animateTransform attributeName="transform" type="translate" values="0 0;16 -18;0 0" dur="14s" repeatCount="indefinite"/>
            <path d="M198 562 C155 492 154 446 190 441 C237 434 242 518 207 565 Z" fill="#dff7ff" opacity=".46"/>
            <path d="M215 562 C244 494 297 449 326 473 C360 501 292 551 222 573 Z" fill="#7fcfff" opacity=".42"/>
            <path d="M206 549 C211 570 210 594 204 625" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".52"/>
        </g>
    </svg>
    <div style="position:absolute;right:0;top:0;width:70vw;height:70vh;background:radial-gradient(ellipse at 70% 28%,rgba(185,237,255,.18),transparent 38%);filter:blur(24px);opacity:.88;"></div>
</div>


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
    order = recover_stuck_transfer_if_needed(order)
    gift_amount = float(order.get("gift_amount") or 0)

    

    if bool(order.get("gift_refunded")):
        return {"status": "gift_already_refunded"}

    if gift_amount <= 0:
        update_order(
            order["id"],
            transfer_completed=1,
            cashout_completed=1,
            transfer_in_progress=0,
            transfer_started_at=None,
            connect_onboarding_completed=1,
        )
        return {"status": "no_gift"}

    if not STRIPE_SECRET_KEY:
        update_order(
            order["id"],
            transfer_completed=1,
            cashout_completed=1,
            transfer_in_progress=0,
            transfer_started_at=None,
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
            transfer_started_at=None,
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
            transfer_started_at=None,
        )
        return {"status": "ok", "transfer_id": transfer.id}

    except Exception as e:
        log_error("Transfer error", e)
        update_order(order["id"], transfer_in_progress=0, transfer_started_at=None)
        return {
            "status": "error",
            "error": str(e),
            "retry": True,
        }


# =========================================================
# LEGAL
# =========================================================

from fastapi.responses import HTMLResponse

@app.get("/condiciones", response_class=HTMLResponse)
def condiciones():
    return HTMLResponse("""<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Condiciones de uso - Tu ETERNA</title><style>body{margin:0;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;line-height:1.72;padding:26px;max-width:860px;margin:auto;background-image:radial-gradient(circle at 80% 10%,rgba(32,164,255,.16),transparent 28%),radial-gradient(circle at 10% 90%,rgba(255,194,74,.10),transparent 30%)}h1{font-family:Georgia,'Times New Roman',serif;font-size:34px;margin:0 0 8px;color:#f5d28b}h2{font-size:19px;margin-top:28px;color:#f5d28b}p,li{opacity:.88}.box{border:1px solid rgba(255,207,112,.22);border-radius:18px;padding:18px;background:rgba(255,255,255,.045);margin:20px 0}.small{opacity:.62;font-size:13px}</style></head><body><h1>Condiciones de uso - Tu ETERNA</h1><p class='small'>Version inicial para fase de lanzamiento. Este texto no sustituye la revision de un profesional legal cuando el servicio escale.</p><div class='box'><p><b>Resumen:</b> ETERNA es una experiencia emocional privada. Quien crea una ETERNA declara tener permiso para usar las fotos, frases y datos introducidos. Quien la vive acepta participar voluntariamente y autoriza que su reaccion pueda ser grabada y enviada de forma privada a la persona que creo la experiencia.</p></div><h2>1. Objeto del servicio</h2><p>Tu ETERNA permite crear una experiencia audiovisual personalizada a partir de fotografias, frases, mensajes y, en su caso, un regalo economico asociado. El destinatario accede mediante un enlace unico y puede vivir una experiencia privada preparada para el o ella.</p><h2>2. Uso responsable</h2><p>El servicio debe usarse de forma respetuosa, privada y licita. Queda prohibido utilizar ETERNA para acosar, presionar, humillar, amenazar, manipular, exponer publicamente, vulnerar derechos de terceros o crear contenido ofensivo, discriminatorio, intimo no consentido, ilicito o contrario a la dignidad de cualquier persona.</p><h2>3. Contenido aportado por quien crea la ETERNA</h2><p>La persona creadora declara que dispone de derechos, autorizacion o legitimacion suficiente para usar las fotografias, frases, nombres, telefonos, mensajes y cualquier otro contenido que introduce.</p><h2>4. Consentimiento del destinatario</h2><p>Antes de acceder a la experiencia, el destinatario debe aceptar estos terminos y la politica de privacidad. Al continuar, acepta participar voluntariamente y entiende que el navegador puede solicitar acceso a camara y microfono para registrar su reaccion durante la experiencia.</p><h2>5. Grabacion de reaccion</h2><p>Si el destinatario concede permisos de camara y microfono, su reaccion podra ser grabada y enviada de forma privada a la persona que creo la ETERNA.</p><h2>6. Uso del recuerdo recibido</h2><p>La persona que recibe el sender pack se compromete a tratarlo como contenido privado. No debe publicarlo, reenviarlo, editarlo, comercializarlo o utilizarlo fuera del contexto emocional sin consentimiento adicional de la persona afectada.</p><h2>7. Pagos y regalo economico</h2><p>Cuando exista regalo economico, ETERNA actua como plataforma tecnica de experiencia y gestion del flujo definido.</p><h2>8. Disponibilidad tecnica</h2><p>Pueden existir fallos derivados del dispositivo, navegador, permisos, conexion, servicios externos, pagos, mensajeria, almacenamiento o mantenimiento tecnico.</p><h2>9. Limitacion de responsabilidad</h2><p>ETERNA no verifica individualmente la titularidad de cada imagen, mensaje o dato introducido por los usuarios. La responsabilidad sobre el contenido aportado y el uso posterior del recuerdo corresponde a quien lo aporta o lo utiliza. Nada excluye responsabilidades que legalmente no puedan excluirse.</p><h2>10. Eliminacion de contenido</h2><p>Los usuarios podran solicitar la eliminacion de contenidos o datos escribiendo al correo de contacto indicado en privacidad.</p><h2>11. Aceptacion</h2><p>El uso del servicio implica la aceptacion de estas condiciones y de la politica de privacidad.</p></body></html>""")


@app.get("/privacidad", response_class=HTMLResponse)
def privacidad(request: Request):
    return HTMLResponse("""<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Privacidad - Tu ETERNA</title><style>body{margin:0;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;line-height:1.72;padding:26px;max-width:860px;margin:auto;background-image:radial-gradient(circle at 80% 10%,rgba(32,164,255,.16),transparent 28%),radial-gradient(circle at 10% 90%,rgba(255,194,74,.10),transparent 30%)}h1{font-family:Georgia,'Times New Roman',serif;font-size:34px;margin:0 0 8px;color:#f5d28b}h2{font-size:19px;margin-top:28px;color:#f5d28b}p,li{opacity:.88}.box{border:1px solid rgba(255,207,112,.22);border-radius:18px;padding:18px;background:rgba(255,255,255,.045);margin:20px 0}.small{opacity:.62;font-size:13px}</style></head><body><h1>Politica de privacidad - Tu ETERNA</h1><p class='small'>Version inicial para fase de lanzamiento. Recomendable revision legal antes de abrir a gran escala.</p><div class='box'><p><b>Resumen:</b> usamos los datos minimos necesarios para crear, entregar y conservar temporalmente la experiencia ETERNA.</p></div><h2>1. Datos tratados</h2><ul><li>Nombre, telefono y correo si se facilita.</li><li>Fotografias, frases y datos introducidos.</li><li>Video generado y reaccion grabada si se aceptan permisos.</li><li>Datos tecnicos minimos: fecha, navegador, estado de entrega, logs de errores y eventos necesarios para seguridad y soporte.</li></ul><h2>2. Finalidad</h2><p>Crear la experiencia, procesar el pago, entregar el enlace, permitir la visualizacion, guardar la reaccion, enviar el sender pack, resolver incidencias y mejorar la seguridad del sistema.</p><h2>3. Legitimacion</h2><p>Ejecucion del servicio solicitado, consentimiento cuando se aceptan permisos de camara y microfono, e interes legitimo para seguridad y soporte.</p><h2>4. Proveedores</h2><p>Podemos utilizar proveedores de alojamiento, almacenamiento, pagos, SMS/WhatsApp, correo y analitica tecnica minima. No vendemos datos personales.</p><h2>5. Conservacion</h2><p>Los datos se conservaran el tiempo necesario para prestar el servicio, permitir acceso al recuerdo y atender incidencias. Puede solicitarse eliminacion.</p><h2>6. Grabacion de reaccion</h2><p>La reaccion solo se graba si el destinatario concede permisos. Puede enviarse de forma privada a la persona que creo la ETERNA.</p><h2>7. Derechos</h2><p>Puedes solicitar acceso, rectificacion, eliminacion, oposicion o limitacion escribiendo al correo de contacto.</p><h2>8. Seguridad</h2><p>Aplicamos medidas razonables, pero ningun sistema conectado a internet garantiza riesgo cero.</p><h2>9. Contacto</h2><p>Para privacidad o eliminacion: <b>contacto@tueterna.com</b>. Sustituir por el correo definitivo antes del lanzamiento publico.</p></body></html>""")

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
    responsible_use_accepted: str = "",
    yul_memory_place: str = "",
    yul_memory_detail: str = "",
    yul_emotion_tone: str = "",
    yul_magic_hint: str = "",
):
    customer_name = (customer_name or "").strip()
    customer_email = (customer_email or "").strip()
    customer_country_code = (customer_country_code or "").strip()
    customer_phone = (customer_phone or "").strip()

    recipient_name = (recipient_name or "").strip()
    recipient_country_code = (recipient_country_code or "").strip()
    recipient_phone = (recipient_phone or "").strip()

    message_type = (message_type or "").strip()
    phrase_mode = (phrase_mode or "auto").strip().lower()

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

    responsible_use_accepted = (responsible_use_accepted or "").strip().lower()
    if responsible_use_accepted not in {"1", "true", "yes", "on", "accepted"}:
        raise HTTPException(
            status_code=400,
            detail="Debes aceptar el uso responsable de ETERNA antes de continuar",
        )

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

    sender_phone = build_global_phone(customer_country_code, customer_phone)
    recipient_phone_global = build_global_phone(recipient_country_code, recipient_phone)

    sender_phone_e164 = to_e164(sender_phone)
    recipient_phone_e164 = to_e164(recipient_phone_global)

    if not sender_phone_e164:
        raise HTTPException(status_code=400, detail="Tu teléfono no es válido")

    if not recipient_phone_e164:
        raise HTTPException(status_code=400, detail="El teléfono del destinatario no es válido")

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

        is_valid_type = content_type in {"image/jpeg", "image/jpg", "image/png", "image/webp", "image/heic", "image/heif", "application/octet-stream"}
        is_valid_name = (
            filename.endswith(".jpg")
            or filename.endswith(".jpeg")
            or filename.endswith(".png")
            or filename.endswith(".webp")
            or filename.endswith(".heic")
            or filename.endswith(".heif")
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

    try:
        cur.execute(
            """
            INSERT INTO senders (name, email, phone, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (customer_name, customer_email, sender_phone_e164, created_at),
        )
        sender_id = cur.lastrowid

        cur.execute(
            """
            INSERT INTO recipients (name, phone, created_at)
            VALUES (?, ?, ?)
            """,
            (recipient_name, recipient_phone_e164, created_at),
        )
        recipient_id = cur.lastrowid

        placeholders = ", ".join(["?"] * 60)

        cur.execute(
            f"""
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
            """,
            (
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
                created_at, created_at,
            ),
        )

        conn.commit()
        insert_order_event(order_id, "order_created", "ok", "Pedido creado y pendiente de pago")

        try:
            update_order(
                order_id,
                yul_memory_place=rc75_clean_emotional_text(yul_memory_place, 140),
                yul_memory_detail=rc75_clean_emotional_text(yul_memory_detail, 220),
                yul_emotion_tone=rc75_clean_emotional_text(yul_emotion_tone, 80),
                yul_magic_hint=rc75_clean_emotional_text(yul_magic_hint, 160),
            )
            insert_order_event(
                order_id,
                "rc78_yul_place_saved",
                "ok",
                "Lugar emocional Yul guardado",
                {
                    "has_place": bool(rc75_clean_emotional_text(yul_memory_place, 140)),
                    "has_memory": bool(rc75_clean_emotional_text(yul_memory_detail, 220)),
                    "emotion": rc75_clean_emotional_text(yul_emotion_tone, 80),
                    "has_hint": bool(rc75_clean_emotional_text(yul_magic_hint, 160)),
                },
            )
        except Exception as e:
            print("[WARN] RC75 yul emotional form save skipped:", e)


        log_human(
            "NUEVA ETERNA CREADA",
            f"👤 La crea: {customer_name}",
            f"📩 Email: {mask_email(customer_email)}",
            f"📱 Teléfono: {mask_phone(sender_phone_e164)}",
            f"🎯 Va para: {recipient_name}",
            f"📱 Teléfono destinatario: {mask_phone(recipient_phone_e164)}",
            f"💸 Total: {fees['total_amount']}€",
            f"🎁 Dinero regalo: {fees['gift_amount']}€",
            f"🕒 Entrega: {'programada' if delivery_mode == 'scheduled' else 'inmediata'}",
            f"🆔 Pedido: {order_id}",
            "✅ Uso responsable aceptado"
        )
        log_info("🔗 Link destinatario", f"{PUBLIC_BASE_URL}/pedido/{recipient_token}")
        log_info("🔗 Link regalante", f"{PUBLIC_BASE_URL}/sender/{sender_token}")

    except Exception:
        conn.rollback()
        conn.close()
        raise
    finally:
        try:
            conn.close()
        except Exception:
            pass

    try:
        for slot_name, upload in photos.items():
            filepath = await save_upload_original_robust(order_id, slot_name, upload)

            insert_asset(
                order_id=order_id,
                asset_type=slot_name,
                file_url=filepath,
                storage_provider="local_original",
            )

        insert_order_event(
            order_id,
            "photos_saved",
            "ok",
            "Las 6 fotos originales se han guardado correctamente para el video engine",
        )

    except HTTPException as e:
        insert_order_event(
            order_id,
            "photos_saved",
            "error",
            str(e.detail),
        )
        raise e

    except Exception as e:
        insert_order_event(
            order_id,
            "photos_saved",
            "error",
            str(e),
        )
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
                                f"gestión regalo {money(fees['total_fee'])}€ + "
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

        update_order(
            order_id,
            stripe_session_id=session.id,
            stripe_payment_status="created",
        )

        return RedirectResponse(url=f"/checkout-loading?order_id={order_id}", status_code=303)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando checkout Stripe: {e}")

    

# =========================================================
# CHECKOUT VISUAL V1 — RUTAS PUENTE BLINDADAS
# =========================================================

@app.get("/checkout-loading", response_class=HTMLResponse)
def checkout_loading(order_id: Optional[str] = None):
    """
    Pantalla visual intermedia antes de Stripe.
    No toca pago, webhook, SMS, video engine ni DB salvo leer el pedido.
    Si falta order_id, vuelve a /crear para evitar error 422/500.
    """
    if not order_id:
        return RedirectResponse(url="/crear", status_code=303)

    try:
        order = get_order_by_id(order_id)
    except Exception:
        return render_eterna_image_screen(
            image_name="error-v1.png",
            fallback_image_name="error-v1.png",
            overlay_kind="soft",
            button_url="/crear",
            button_label="Volver a crear",
            extra_note="No hemos podido encontrar este pedido.",
        )

    target_url = f"/checkout-exito/{order_id}"

    if STRIPE_SECRET_KEY and (order.get("stripe_session_id") or "").strip():
        try:
            session = stripe.checkout.Session.retrieve(order.get("stripe_session_id"))
            session_url = ""
            try:
                session_url = session.get("url") or ""
            except Exception:
                session_url = getattr(session, "url", "") or ""
            if session_url:
                target_url = session_url
        except Exception as e:
            log_error("checkout_loading_retrieve_stripe_session", e)

    # RC19:
    # Pantalla correcta después del formulario: "creando / guardando tu ETERNA"
    # con mariposa y línea azul. No repetimos la pantalla de pago realizado.
    # Se mantiene visible hasta el último instante antes de saltar a Stripe.
    return render_eterna_image_screen(
        image_name="checkout_loading",
        fallback_image_name="checkout_loading",
        overlay_kind="loading",
        redirect_url=target_url,
        redirect_delay_ms=6000,
        extra_note="Tu ETERNA está cobrando vida...",
    )


def render_checkout_success_visual(order: dict) -> HTMLResponse:
    """
    Pantalla de pago realizado. Visual únicamente.
    No fuerza envío, no toca webhook y no modifica el estado del pedido.
    """
    return render_eterna_image_screen(
        image_name="payment-success-v1.png",
        fallback_image_name="payment-success-v1.png",
        overlay_kind="soft",
        button_url="/crear",
        button_label="Crear otra ETERNA",
        extra_note="Tu ETERNA ya está en marcha.",
    )


@app.get("/checkout-exito/{order_id}", response_class=HTMLResponse)
def checkout_exito(order_id: str):
    """
    Landing posterior al pago. Stripe vuelve aquí tras pago correcto.
    El webhook sigue siendo quien marca paid/render/SMS; esta ruta solo muestra pantalla.
    """
    try:
        order = get_order_by_id(order_id)
    except Exception:
        return render_eterna_image_screen(
            image_name="error-v1.png",
            fallback_image_name="error-v1.png",
            overlay_kind="soft",
            button_url="/crear",
            button_label="Volver a crear",
            extra_note="No hemos podido encontrar este pedido.",
        )
    return render_checkout_success_visual(order)


@app.get("/post-pago/{order_id}", response_class=HTMLResponse)
def post_pago(order_id: str):
    """
    Compatibilidad para flujos antiguos o modo sin Stripe.
    Centraliza la salida visual en checkout-exito para no duplicar pantallas.
    """
    try:
        get_order_by_id(order_id)
    except Exception:
        return render_eterna_image_screen(
            image_name="error-v1.png",
            fallback_image_name="error-v1.png",
            overlay_kind="soft",
            button_url="/crear",
            button_label="Volver a crear",
            extra_note="No hemos podido encontrar este pedido.",
        )
    return RedirectResponse(url=f"/checkout-exito/{order_id}", status_code=303)


@app.get("/viral-final/{recipient_token}", response_class=HTMLResponse)
def viral_final_cta(recipient_token: str):
    """CTA viral RC8: no depende de imagen PNG para evitar 404/pantalla rota."""
    try:
        get_order_by_recipient_token_or_404(recipient_token)
    except Exception:
        return render_eterna_image_screen(
            image_name="error-v1.png",
            fallback_image_name="error-v1.png",
            overlay_kind="soft",
            button_url="/crear",
            button_label="Crear una ETERNA",
            extra_note="Esta experiencia ya no está disponible.",
        )
    return HTMLResponse('''
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"><title>ETERNA</title><meta name="theme-color" content="#02050a"><style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}html,body{margin:0;width:100%;min-height:100%;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}body{min-height:100svh;min-height:100dvh;display:flex;align-items:center;justify-content:center;overflow:hidden;background:radial-gradient(circle at 76% 18%,rgba(72,185,255,.26),transparent 30%),radial-gradient(circle at 18% 84%,rgba(255,205,112,.12),transparent 32%),#02050a}.card{width:min(92vw,440px);text-align:center;border:1px solid rgba(255,213,130,.24);border-radius:30px;background:rgba(255,255,255,.055);padding:34px 22px;box-shadow:0 28px 90px rgba(0,0,0,.68)}.logo{letter-spacing:.42em;color:#d8b76d;font-weight:900;font-size:12px;margin-bottom:22px}.heart{font-size:44px;color:#ffd37b;text-shadow:0 0 34px rgba(255,200,90,.54);animation:pulse 2.8s ease-in-out infinite}@keyframes pulse{0%,100%{transform:scale(.96);opacity:.82}50%{transform:scale(1.06);opacity:1}}h1{font-size:clamp(34px,9vw,52px);line-height:1.02;margin:14px 0 12px;letter-spacing:-.06em}.gold{color:#f5c46e}p{margin:0 auto 24px;color:rgba(255,245,229,.75);font-size:17px;line-height:1.5;max-width:330px}.btn{min-height:60px;border-radius:19px;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:900;font-size:16px;padding:12px 16px;background:linear-gradient(135deg,#fff0b9,#d79a35);color:#171007;text-decoration:none;box-shadow:0 0 34px rgba(255,190,72,.28)}.small{margin-top:18px;color:rgba(255,245,229,.52);font-size:13px}
</style></head><body><main class="card"><div class="logo">ETERNA</div><div class="heart">♡</div><h1>¿Quieres provocar <span class="gold">algo así?</span></h1><p>Haz que alguien viva un momento que no se olvida.</p><a class="btn" href="/crear">Crear mi ETERNA</a><div class="small">Privado. Seguro. Emocional.</div></main></body></html>
''')


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
            html, body {{ margin: 0; min-height: 100%; background: #020202; }}
            body {{
                min-height: 100vh;
                background:
                    radial-gradient(circle at 50% -12%, rgba(225,180,92,0.24), transparent 34%),
                    radial-gradient(circle at 12% 18%, rgba(255,230,170,0.08), transparent 26%),
                    radial-gradient(circle at 90% 78%, rgba(204,140,44,0.10), transparent 34%),
                    linear-gradient(180deg, #020817 0%, #000000 48%, #020817 100%);
                color: #fff7e6;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
                padding: 24px;
                overflow-x: hidden;
            }}
            body::before {{
                content: "";
                position: fixed;
                inset: 0;
                pointer-events: none;
                background:
                    radial-gradient(circle at 50% 32%, rgba(255,213,130,0.12), transparent 18%),
                    linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
                background-size: auto, 92px 92px;
                opacity: .72;
            }}
            body::after {{
                content: "";
                position: fixed;
                inset: 0;
                pointer-events: none;
                background: radial-gradient(circle at center, transparent 42%, rgba(0,0,0,.72) 100%);
            }}
            .wrap {{ width: 100%; max-width: 900px; margin: 0 auto; position: relative; z-index: 2; }}
            .card {{
                background:
                    linear-gradient(180deg, rgba(18,15,10,0.92), rgba(4,4,4,0.96)),
                    radial-gradient(circle at 50% 0%, rgba(225,180,92,.14), transparent 42%);
                border: 1px solid rgba(225,180,92,0.18);
                border-radius: 32px;
                padding: 30px;
                overflow: hidden;
                box-shadow: 0 30px 120px rgba(0,0,0,.75), 0 0 80px rgba(225,180,92,.08);
                backdrop-filter: blur(18px);
            }}
            h1 {{
                margin: 0 0 12px 0;
                font-size: clamp(34px, 6vw, 62px);
                text-align: center;
                letter-spacing: 8px;
                color: #f7dfaa;
                text-shadow: 0 0 24px rgba(225,180,92,.40);
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
                border: 1px solid rgba(218,178,92,0.22);
                background: rgba(255,255,255,0.05);
                color: #fff7e6;
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
            .photo-picker-main {{
                margin: 14px 0 18px;
                border-radius: 26px;
                padding: 18px;
                background: linear-gradient(180deg, rgba(218,178,92,0.11), rgba(255,255,255,0.035));
                border: 1px solid rgba(218,178,92,0.20);
                text-align: center;
            }}
            .photo-picker-title {{
                font-size: 18px;
                font-weight: 700;
                margin-bottom: 8px;
            }}
            .photo-picker-sub {{
                color: rgba(255,255,255,0.54);
                font-size: 13px;
                line-height: 1.7;
                margin-bottom: 14px;
            }}
            .photo-picker-btn {{
                display: block;
                width: 100%;
                padding: 16px 18px;
                border-radius: 999px;
                background: rgba(255,255,255,0.92);
                color: #050505;
                font-weight: 800;
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }}
            .photo-picker-btn input {{
                position:absolute;
                inset:0;
                opacity:0;
                cursor:pointer;
            }}
            .photo-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 12px;
                margin-top: 12px;
            }}
            .photo-card {{
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 22px;
                padding: 10px;
            }}
            .photo-label {{
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 1.2px;
                color: rgba(218,178,92,0.82);
                margin-bottom: 8px;
                text-align: center;
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
                aspect-ratio: 9 / 16;
                min-height: 0;
                overflow: hidden;
                background: rgba(255,255,255,0.03);
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 10px;
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
                color: rgba(255,255,255,0.50);
                line-height: 1.45;
                font-size: 12px;
                position: relative;
                z-index: 1;
                pointer-events: none;
                max-width: 110px;
            }}
            .photo-preview {{
                position: absolute;
                inset: 0;
                width: 100%;
                height: 100%;
                object-fit: contain;
                object-position: center center;
                display: none;
                z-index: 2;
                border-radius: 18px;
                background: rgba(0,0,0,0.28);
            }}
            .photo-status {{
                margin-top: 8px;
                color: rgba(255,255,255,0.48);
                font-size: 11px;
                line-height: 1.45;
                min-height: 16px;
                text-align: center;
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
                gap: 12px;
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
            textarea {{
                width: 100%;
                min-height: 96px;
                resize: none;
                overflow: hidden;
                line-height: 1.55;
                font-family: inherit;
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
                background: linear-gradient(135deg, #fff0bd 0%, #e4bd69 45%, #b9822f 100%);
                color: #120b02;
            }}
            button:disabled {{
                opacity: 0.7;
                cursor: default;
            }}
            .ghost {{
                display: inline-block;
                background: rgba(218,178,92,0.10);
                color: #fff7e6;
                border: 1px solid rgba(218,178,92,0.22);
            }}
            .error-box {{
                display: none;
                margin-top: 14px;
                padding: 14px 16px;
                border-radius: 16px;
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(218,178,92,0.22);
                color: rgba(255,255,255,0.82);
                font-size: 14px;
                line-height: 1.7;
            }}
            @media (max-width: 760px) {{
                .emotion-grid,
                .delivery-grid {{
                    grid-template-columns: 1fr;
                }}
                .photo-grid {{
                    grid-template-columns: repeat(3, 1fr);
                    gap: 10px;
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
        
            /* =========================================================
               ETERNA LUXURY CINEMATIC UI — ONE PAGE FLOW
               Solo capa visual: no toca backend, pagos ni rutas.
            ========================================================= */
            body {{
                padding: clamp(14px, 3vw, 28px);
                background:
                    radial-gradient(circle at 50% 0%, rgba(255, 211, 125, 0.20), transparent 28%),
                    radial-gradient(circle at 8% 22%, rgba(189, 133, 47, 0.13), transparent 28%),
                    radial-gradient(circle at 88% 58%, rgba(255, 222, 159, 0.08), transparent 34%),
                    radial-gradient(circle at 50% 115%, rgba(189, 133, 47, 0.12), transparent 34%),
                    linear-gradient(180deg, #020202 0%, #080603 46%, #000 100%);
            }}
            body::before {{
                background:
                    radial-gradient(circle at 50% 28%, rgba(246, 204, 120, 0.11), transparent 22%),
                    radial-gradient(circle at 35% 82%, rgba(246, 204, 120, 0.055), transparent 24%),
                    linear-gradient(90deg, rgba(255,255,255,0.012) 1px, transparent 1px),
                    linear-gradient(0deg, rgba(255,255,255,0.008) 1px, transparent 1px);
                background-size: auto, auto, 96px 96px, 96px 96px;
                opacity: .9;
                animation: eternaAura 12s ease-in-out infinite;
            }}
            body::after {{
                background:
                    radial-gradient(circle at center, transparent 38%, rgba(0,0,0,.82) 100%),
                    linear-gradient(180deg, rgba(0,0,0,.12), rgba(0,0,0,.42));
            }}
            @keyframes eternaAura {{
                0%,100% {{ opacity: .58; transform: scale(1); }}
                50% {{ opacity: 1; transform: scale(1.035); }}
            }}
            .wrap {{ max-width: 980px; }}
            .card {{
                position: relative;
                border-radius: 36px;
                padding: clamp(22px, 4vw, 44px);
                background:
                    radial-gradient(circle at 50% -8%, rgba(255, 218, 146, .17), transparent 34%),
                    radial-gradient(circle at 4% 36%, rgba(220, 164, 74, .07), transparent 26%),
                    radial-gradient(circle at 96% 72%, rgba(220, 164, 74, .06), transparent 30%),
                    linear-gradient(180deg, rgba(18,15,9,.82), rgba(3,3,3,.92));
                border: 1px solid rgba(231, 183, 92, .24);
                box-shadow:
                    0 38px 140px rgba(0,0,0,.86),
                    0 0 90px rgba(221, 169, 72,.12),
                    inset 0 0 0 1px rgba(255,255,255,.035);
            }}
            .card::before {{
                content:"";
                position:absolute;
                inset:0;
                border-radius:inherit;
                pointer-events:none;
                background:
                    linear-gradient(135deg, rgba(255,255,255,.12), transparent 28%, transparent 70%, rgba(255,214,134,.08)),
                    radial-gradient(circle at 50% 0%, rgba(255,226,166,.18), transparent 38%);
                opacity:.55;
            }}
            .card > * {{ position: relative; z-index: 2; }}
            h1 {{
                font-size: clamp(36px, 7vw, 68px);
                letter-spacing: clamp(4px, 1.4vw, 10px);
                color: #ffe2a3;
                text-shadow:
                    0 0 18px rgba(255,226,163,.42),
                    0 0 54px rgba(212,160,68,.30);
                margin-top: 4px;
            }}
            .subtitle {{
                font-size: clamp(15px, 2.4vw, 19px);
                color: rgba(255,245,222,.78);
                text-shadow: 0 0 24px rgba(255,224,158,.14);
            }}
            .intro {{
                min-height: unset;
                margin-bottom: 26px;
                padding: 20px 16px 4px;
            }}
            .intro-line {{
                font-family: Georgia, "Times New Roman", serif;
                font-size: clamp(20px, 3vw, 28px);
                color: rgba(255,255,255,.92);
                text-shadow: 0 0 26px rgba(255,217,140,.12);
            }}
            .intro-line.l4 {{
                color: #ffd985;
                text-shadow: 0 0 30px rgba(255,202,98,.35);
            }}
            .form-progress,
            .step-actions,
            #backStep1,
            .atmosphere-title {{ display: none !important; }}
            .form-step {{ display: block !important; opacity: 1 !important; }}
            .section {{
                margin-top: 26px;
                padding: clamp(16px, 2.6vw, 24px);
                border-radius: 28px;
                background:
                    linear-gradient(180deg, rgba(255,255,255,.045), rgba(255,255,255,.018)),
                    radial-gradient(circle at 50% 0%, rgba(230,176,83,.08), transparent 56%);
                border: 1px solid rgba(231,183,92,.13);
                box-shadow:
                    0 18px 50px rgba(0,0,0,.26),
                    inset 0 0 0 1px rgba(255,255,255,.025);
            }}
            .section-title {{
                color: #e9c06f;
                letter-spacing: 1.8px;
                font-size: 12px;
                margin: 0 0 14px 0;
                text-shadow: 0 0 18px rgba(233,192,111,.18);
            }}
            input, select, textarea {{
                border-radius: 18px;
                border: 1px solid rgba(233,192,111,.16);
                background: rgba(255,255,255,.055);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,.018);
                transition: border-color .25s ease, box-shadow .25s ease, background .25s ease, transform .25s ease;
            }}
            input:focus, select:focus, textarea:focus {{
                border-color: rgba(255,218,143,.56);
                box-shadow: 0 0 0 4px rgba(233,192,111,.08), 0 0 28px rgba(233,192,111,.12);
                background: rgba(255,255,255,.075);
            }}
            .photo-picker-main {{
                border-radius: 30px;
                background:
                    radial-gradient(circle at 50% 0%, rgba(255,218,143,.18), transparent 48%),
                    linear-gradient(180deg, rgba(233,192,111,.10), rgba(255,255,255,.030));
                border: 1px solid rgba(233,192,111,.28);
                box-shadow: 0 18px 55px rgba(0,0,0,.34), 0 0 38px rgba(233,192,111,.08);
            }}
            .photo-picker-title {{ color: #ffe3a3; text-shadow: 0 0 18px rgba(233,192,111,.20); }}
            .photo-picker-btn, button {{
                background: linear-gradient(135deg, #fff0bd 0%, #e6bb62 46%, #b77d2d 100%);
                color: #130d05;
                box-shadow:
                    0 14px 36px rgba(212,157,63,.25),
                    inset 0 1px 0 rgba(255,255,255,.35);
                transition: transform .22s ease, box-shadow .22s ease, filter .22s ease;
            }}
            .photo-picker-btn:hover, button:hover {{
                transform: translateY(-1px);
                box-shadow:
                    0 20px 46px rgba(212,157,63,.34),
                    inset 0 1px 0 rgba(255,255,255,.42);
                filter: brightness(1.03);
            }}
            .photo-grid {{ gap: clamp(10px, 2vw, 16px); }}
            .photo-card {{
                position: relative;
                border-radius: 26px;
                background: linear-gradient(180deg, rgba(255,255,255,.052), rgba(255,255,255,.022));
                border: 1px solid rgba(233,192,111,.14);
                box-shadow: 0 16px 42px rgba(0,0,0,.28);
                overflow: hidden;
            }}
            .photo-card::before {{
                content:"";
                position:absolute;
                inset:0;
                pointer-events:none;
                background: radial-gradient(circle at 50% 0%, rgba(233,192,111,.12), transparent 46%);
                opacity:.6;
            }}
            .photo-label {{ color:#f4c975; text-shadow: 0 0 18px rgba(244,201,117,.18); }}
            .photo-box {{
                border: 1px dashed rgba(233,192,111,.30);
                background:
                    radial-gradient(circle at 50% 30%, rgba(233,192,111,.08), transparent 48%),
                    rgba(255,255,255,.025);
            }}
            .photo-preview {{ filter: saturate(1.08) contrast(1.03); }}
            .emotion-grid {{ gap: clamp(12px, 2vw, 18px); }}
            .emotion-card {{
                position: relative;
                min-height: 104px;
                padding: 20px 19px;
                border-radius: 26px;
                border: 1px solid rgba(233,192,111,.14);
                background:
                    radial-gradient(circle at 20% 0%, rgba(233,192,111,.10), transparent 44%),
                    linear-gradient(180deg, rgba(255,255,255,.052), rgba(255,255,255,.022));
                box-shadow: 0 18px 48px rgba(0,0,0,.24);
                overflow: hidden;
            }}
            .emotion-card::before {{
                content:"";
                position:absolute;
                inset:0;
                opacity:0;
                background:
                    radial-gradient(circle at 50% 0%, rgba(255,221,151,.25), transparent 48%),
                    linear-gradient(135deg, rgba(255,255,255,.09), transparent 42%);
                transition: opacity .28s ease;
                pointer-events:none;
            }}
            .emotion-card::after {{
                content:"";
                position:absolute;
                right:18px;
                top:18px;
                width:8px;
                height:8px;
                border-radius:999px;
                background: rgba(233,192,111,.38);
                box-shadow: 0 0 18px rgba(233,192,111,.26);
                transition: transform .28s ease, opacity .28s ease;
            }}
            .emotion-card:hover {{
                transform: translateY(-2px);
                border-color: rgba(233,192,111,.34);
                box-shadow: 0 24px 60px rgba(0,0,0,.32), 0 0 34px rgba(233,192,111,.09);
            }}
            .emotion-card:hover::before,
            .emotion-card.selected::before {{ opacity:1; }}
            .emotion-card.selected {{
                border-color: rgba(255,219,146,.72);
                background:
                    radial-gradient(circle at 50% 0%, rgba(255,219,146,.22), transparent 52%),
                    linear-gradient(180deg, rgba(233,192,111,.13), rgba(255,255,255,.045));
                box-shadow:
                    0 26px 70px rgba(0,0,0,.38),
                    0 0 38px rgba(233,192,111,.20),
                    inset 0 0 0 1px rgba(255,255,255,.05);
            }}
            .emotion-card.selected::after {{
                transform: scale(1.65);
                opacity:1;
                background:#ffe3a3;
                box-shadow: 0 0 28px rgba(255,227,163,.62);
            }}
            .emotion-title {{
                position:relative;
                z-index:2;
                color: rgba(255,247,230,.96);
                font-size: 18px;
                font-weight: 800;
                letter-spacing: -.2px;
            }}
            .emotion-sub {{
                position:relative;
                z-index:2;
                color: rgba(255,255,255,.58);
                font-size: 13px;
            }}
            .mode-box, .delivery-box, .delivery-option, .price-box {{
                border-color: rgba(233,192,111,.15);
                background:
                    radial-gradient(circle at 50% 0%, rgba(233,192,111,.075), transparent 56%),
                    rgba(255,255,255,.04);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,.018);
            }}
            .delivery-option {{ transition: border-color .22s ease, box-shadow .22s ease, background .22s ease; }}
            .delivery-option:has(input:checked) {{
                border-color: rgba(255,219,146,.58);
                background:
                    radial-gradient(circle at 50% 0%, rgba(255,219,146,.16), transparent 56%),
                    rgba(255,255,255,.055);
                box-shadow: 0 0 30px rgba(233,192,111,.10);
            }}
            .price-box {{ color: rgba(255,244,220,.82); }}
            .buttons {{ margin-top: 28px; }}
            #submitBtn {{ font-size: 16px; padding: 19px 22px; }}
            .ghost {{ display:none !important; }}
            .error-box {{
                border-color: rgba(255,210,130,.20);
                background: rgba(233,192,111,.07);
            }}
            a {{ color:#ffe3a3 !important; }}
            /* ETERNA POLISH SAFE: capa visual sin tocar lógica */
            .payment-overlay {{
                position: fixed;
                inset: 0;
                z-index: 99999;
                display: none;
                align-items: center;
                justify-content: center;
                padding: 24px;
                background:
                    radial-gradient(circle at 50% 35%, rgba(232,186,94,.22), transparent 34%),
                    radial-gradient(circle at 50% 80%, rgba(255,232,178,.08), transparent 36%),
                    rgba(0,0,0,.84);
                backdrop-filter: blur(18px);
                -webkit-backdrop-filter: blur(18px);
            }}
            .payment-overlay.show {{ display: flex; }}
            .payment-card {{
                width: min(430px, 92vw);
                border-radius: 34px;
                padding: 34px 24px;
                text-align: center;
                border: 1px solid rgba(239,197,112,.30);
                background:
                    radial-gradient(circle at 50% 0%, rgba(239,197,112,.18), transparent 54%),
                    linear-gradient(180deg, rgba(255,255,255,.065), rgba(255,255,255,.024));
                box-shadow:
                    0 30px 90px rgba(0,0,0,.64),
                    0 0 70px rgba(219,169,75,.16),
                    inset 0 0 0 1px rgba(255,255,255,.045);
            }}
            .payment-mark {{
                width: 76px;
                height: 76px;
                margin: 0 auto 22px;
                border-radius: 999px;
                border: 1px solid rgba(255,222,150,.55);
                display: grid;
                place-items: center;
                color: #ffe3a3;
                font-size: 34px;
                letter-spacing: -8px;
                padding-right: 8px;
                text-shadow: 0 0 24px rgba(255,219,146,.55);
                box-shadow: 0 0 46px rgba(233,192,111,.22), inset 0 0 28px rgba(233,192,111,.08);
                animation: eternaPulse 1.9s ease-in-out infinite;
            }}
            .payment-title {{
                font-family: Georgia, "Times New Roman", serif;
                font-size: clamp(26px, 7vw, 40px);
                margin: 0 0 10px;
                color: rgba(255,248,232,.96);
                text-shadow: 0 0 30px rgba(255,223,158,.20);
            }}
            .payment-sub {{
                font-size: 15px;
                line-height: 1.75;
                color: rgba(255,255,255,.66);
                margin: 0 auto;
                max-width: 330px;
            }}
            .payment-loader {{
                width: 190px;
                height: 4px;
                border-radius: 999px;
                overflow: hidden;
                margin: 26px auto 0;
                background: rgba(255,255,255,.08);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,.04);
            }}
            .payment-loader::before {{
                content: "";
                display: block;
                height: 100%;
                width: 42%;
                border-radius: inherit;
                background: linear-gradient(90deg, transparent, #ffe3a3, #c58a35, transparent);
                animation: eternaLoad 1.25s ease-in-out infinite;
            }}
            @keyframes eternaPulse {{
                0%,100% {{ transform: scale(1); opacity: .88; }}
                50% {{ transform: scale(1.045); opacity: 1; }}
            }}
            @keyframes eternaLoad {{
                0% {{ transform: translateX(-120%); }}
                100% {{ transform: translateX(260%); }}
            }}
            #submitBtn.is-loading {{
                pointer-events: none;
                opacity: .92;
                filter: saturate(.94) brightness(.98);
            }}

            @media (max-width: 760px) {{
                .card {{ border-radius: 30px; }}
                h1 {{ letter-spacing: 5px; }}
                .emotion-grid {{ grid-template-columns: 1fr; }}
                .emotion-card {{ min-height: 96px; }}
                .section {{ padding: 16px; border-radius: 24px; }}
                .photo-grid {{ grid-template-columns: repeat(2, 1fr); }}
            }}
            @media (max-width: 430px) {{
                body {{ padding: 10px; }}
                .card {{ padding: 18px; }}
                .photo-grid {{ grid-template-columns: repeat(2, 1fr); }}
                .phone-row {{ gap: 8px; }}
                .phone-code {{ min-width: 96px; flex-basis: 96px; }}
                .intro-line {{ font-size: 18px; }}
            }}

        .payment-overlay.show .payment-cinematic {{ animation: cinematicIn .35s ease-out both; }}
        .payment-cinematic {{ position:relative; width:100vw; height:100svh; height:100dvh; max-width:520px; overflow:hidden; background:#02050a; }}
        .payment-cinematic img {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:center center; }}
        .payment-cinematic-glow {{ position:absolute; inset:-10%; background:radial-gradient(circle at 50% 54%,rgba(68,199,255,.26),transparent 25%),radial-gradient(circle at 62% 70%,rgba(255,201,98,.18),transparent 24%); mix-blend-mode:screen; animation: cinematicBreath 4.8s ease-in-out infinite; pointer-events:none; }}
        @keyframes cinematicIn {{ from {{ opacity:0; transform:scale(1.02); }} to {{ opacity:1; transform:scale(1); }} }}
        @keyframes cinematicBreath {{ 0%,100% {{ opacity:.42; transform:scale(1); }} 50% {{ opacity:.85; transform:scale(1.045); }} }}

            .s-yul {{
                border: 1px solid rgba(112, 219, 255, 0.18);
                background:
                    radial-gradient(circle at top left, rgba(69, 211, 255, 0.10), transparent 34%),
                    radial-gradient(circle at bottom right, rgba(255, 206, 116, 0.09), transparent 38%),
                    rgba(255,255,255,0.035);
                box-shadow: 0 0 34px rgba(64, 202, 255, 0.08);
            }}
            .yul-emotional-grid {{
                display: grid;
                gap: 16px;
                margin-top: 16px;
            }}
            .field-label {{
                display: grid;
                gap: 8px;
                color: rgba(255,255,255,0.82);
                font-size: 14px;
                line-height: 1.45;
            }}
            .text-input {{
                width: 100%;
                border: 1px solid rgba(255,255,255,0.14);
                border-radius: 18px;
                padding: 15px 16px;
                background: rgba(0,0,0,0.34);
                color: white;
                font: inherit;
                outline: none;
            }}
            .text-input:focus {{
                border-color: rgba(108, 215, 255, 0.68);
                box-shadow: 0 0 0 4px rgba(108, 215, 255, 0.10);
            }}
            textarea.text-input {{
                resize: vertical;
                min-height: 92px;
            }}
</style>
    </head>
    <body>


<div aria-hidden="true" data-eterna-cinematic-scene="1" style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:1;mix-blend-mode:screen;">
    <div style="position:absolute;inset:-18%;background:radial-gradient(circle at 76% 18%,rgba(92,191,255,.28),transparent 24%),radial-gradient(circle at 63% 52%,rgba(23,82,190,.24),transparent 30%),radial-gradient(circle at 18% 82%,rgba(218,178,92,.12),transparent 28%);filter:blur(2px);opacity:.95;"></div>
    <svg viewBox="0 0 900 900" preserveAspectRatio="xMidYMid slice" style="position:absolute;inset:-7%;width:114%;height:114%;opacity:.98;filter:drop-shadow(0 0 26px rgba(125,210,255,.72)) drop-shadow(0 0 82px rgba(37,99,235,.42));" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="cinema_core" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
                <stop offset="20%" stop-color="#dff6ff" stop-opacity=".92"/>
                <stop offset="58%" stop-color="#69bfff" stop-opacity=".46"/>
                <stop offset="100%" stop-color="#061428" stop-opacity="0"/>
            </radialGradient>
            <linearGradient id="cinema_wing" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#ffffff" stop-opacity=".96"/>
                <stop offset="22%" stop-color="#c7eeff" stop-opacity=".88"/>
                <stop offset="58%" stop-color="#4aa4ff" stop-opacity=".56"/>
                <stop offset="100%" stop-color="#071c4b" stop-opacity=".08"/>
            </linearGradient>
            <filter id="wingTexture" x="-30%" y="-30%" width="160%" height="160%">
                <feTurbulence type="fractalNoise" baseFrequency="0.012 0.032" numOctaves="4" seed="8" result="noise"/>
                <feDisplacementMap in="SourceGraphic" in2="noise" scale="10" xChannelSelector="R" yChannelSelector="G"/>
                <feGaussianBlur stdDeviation="0.25"/>
            </filter>
            <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
                <feGaussianBlur stdDeviation="14" result="blur"/>
                <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
        </defs>
        <g opacity=".95">
            <path d="M836 83 C724 138 657 212 597 300 C538 388 476 430 403 461 C310 500 202 506 83 606" fill="none" stroke="#72d8ff" stroke-width="3" stroke-linecap="round" opacity=".28"/>
            <path d="M812 128 C706 169 638 237 585 318 C532 399 458 460 375 492 C284 528 186 536 91 626" fill="none" stroke="#f6c56f" stroke-width="2" stroke-linecap="round" opacity=".18"/>
            <path d="M850 178 C743 199 660 259 595 351 C530 443 451 507 360 544" fill="none" stroke="#b6ecff" stroke-width="1.4" stroke-linecap="round" opacity=".20"/>
        </g>
        <g opacity=".96">
            <animateTransform attributeName="transform" type="translate" values="0 0;-14 -20;0 0" dur="12s" repeatCount="indefinite"/>
            <circle cx="640" cy="222" r="250" fill="url(#cinema_core)" opacity=".28" filter="url(#softGlow)"/>
            <g filter="url(#wingTexture)" opacity=".96">
                <path d="M626 226 C535 85 523 12 592 8 C681 2 694 140 642 229 Z" fill="url(#cinema_wing)" opacity=".92"/>
                <path d="M655 226 C703 80 810 8 866 57 C928 112 794 211 669 244 Z" fill="url(#cinema_wing)" opacity=".92"/>
                <path d="M622 244 C508 233 451 278 485 332 C526 398 599 324 637 254 Z" fill="url(#cinema_wing)" opacity=".70"/>
                <path d="M667 250 C772 233 849 276 814 337 C776 402 699 326 655 256 Z" fill="url(#cinema_wing)" opacity=".70"/>
                <path d="M646 168 C655 201 655 242 646 315" stroke="#f9feff" stroke-width="10" stroke-linecap="round" opacity=".72"/>
                <path d="M590 50 C620 92 632 139 642 199 M735 62 C700 105 675 155 657 205 M515 278 C561 263 600 255 634 251 M791 282 C744 266 704 257 666 252" stroke="#ffffff" stroke-width="2.2" stroke-opacity=".32" fill="none"/>
            </g>
        </g>
        <g opacity=".86">
            <animate attributeName="opacity" values=".55;.95;.55" dur="5.5s" repeatCount="indefinite"/>
            <circle cx="796" cy="149" r="2.8" fill="#e8fbff"/><circle cx="752" cy="176" r="1.8" fill="#74d7ff"/><circle cx="706" cy="210" r="2.1" fill="#f7ca78"/><circle cx="650" cy="253" r="1.6" fill="#c8f2ff"/><circle cx="594" cy="300" r="1.7" fill="#82d8ff"/><circle cx="528" cy="359" r="1.9" fill="#f4c771"/><circle cx="456" cy="421" r="1.4" fill="#b8eeff"/><circle cx="375" cy="488" r="1.6" fill="#81d9ff"/><circle cx="284" cy="529" r="1.2" fill="#f7cf83"/>
        </g>
        <g opacity=".62" filter="url(#softGlow)">
            <animateTransform attributeName="transform" type="translate" values="0 0;16 -18;0 0" dur="14s" repeatCount="indefinite"/>
            <path d="M198 562 C155 492 154 446 190 441 C237 434 242 518 207 565 Z" fill="#dff7ff" opacity=".46"/>
            <path d="M215 562 C244 494 297 449 326 473 C360 501 292 551 222 573 Z" fill="#7fcfff" opacity=".42"/>
            <path d="M206 549 C211 570 210 594 204 625" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".52"/>
        </g>
    </svg>
    <div style="position:absolute;right:0;top:0;width:70vw;height:70vh;background:radial-gradient(ellipse at 70% 28%,rgba(185,237,255,.18),transparent 38%);filter:blur(24px);opacity:.88;"></div>
</div>


        <div class="wrap">
            <div class="card" style="position:relative;z-index:2;">
                <h1>ETERNA</h1>
                <div class="subtitle">Crea algo que no se abra. Se viva.</div>

                <div class="intro">
                    <p class="intro-line l1">No todo lo importante</p>
                    <p class="intro-line l2">debería desaparecer.</p>
                    <p class="intro-line l3">Haz que vuelva convertido</p>
                    <p class="intro-line l4">en emoción real.</p>
                </div>

                <form action="/crear" method="post" enctype="multipart/form-data" id="createForm">
                    <div class="form-step active" id="formStep1">
                        <div class="atmosphere-title">Primero construimos el recuerdo. Luego decidimos cómo vuelve.</div>

                    <div class="section s1">
                        <div class="section-title">Quién lo crea</div>
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
                        <div class="section-title">Quién lo va a vivir</div>
                        <input name="recipient_name" id="recipient_name" placeholder="Su nombre" required>

                        <div class="phone-row" style="align-items: stretch;">
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

                            <div style="flex:1; display:flex; flex-direction:column; gap:10px;">
                                <input
                                    type="tel"
                                    name="recipient_phone"
                                    id="recipient_phone"
                                    class="phone-input"
                                    placeholder="Su teléfono"
                                    autocomplete="tel"
                                    inputmode="tel"
                                    required
                                >

                                <div
                                    id="phone-help"
                                    style="
                                        margin-top:-2px;
                                        color: rgba(255,255,255,0.48);
                                        font-size: 12px;
                                        line-height: 1.6;
                                    "
                                >
                                    Escríbelo como lo tengas guardado 💛<br>
                                    No hace falta poner el prefijo.
                                </div>
                            </div>
                        </div>
                    </div>

                    
                    
                    
                    <div class="section s-yul">
                        <div class="section-title">El alma de Yul</div>
                        <div class="soft-copy">
                            Una sola pista. Un lugar. Yul no necesita saber más para encontrar una puerta.
                        </div>

                        <div class="yul-emotional-grid">
                            <label class="field-label">
                                ¿Hay algún lugar que forme parte de vuestra historia?
                                <input
                                    type="text"
                                    name="yul_memory_place"
                                    id="yul_memory_place"
                                    class="text-input"
                                    maxlength="140"
                                    placeholder="Ej: Cádiz, la montaña, la casa de la abuela, un banco, París..."
                                    autocomplete="off"
                                >
                            </label>

                            <div class="soft-copy yul-one-place-note">
                                No expliques el recuerdo. Solo escribe el lugar. Yul hará el resto.
                            </div>
                        </div>
                    </div>

<div class="section s3">
                        <div class="section-title">Los recuerdos</div>
                        <div class="soft-copy">
                            Elige 6 fotos directamente desde tu galería. ETERNA las colocará como Foto 1, Foto 2, Foto 3...
                        </div>

                        <div class="photo-picker-main">
                            <div class="photo-picker-title">Seleccionar 6 recuerdos</div>
                            <div class="photo-picker-sub">
                                Puedes elegir las 6 fotos de una vez. Después podrás cambiar cualquiera individualmente.
                            </div>
                            <label class="photo-picker-btn">
                                Abrir galería
                                <input type="file" id="multi_photo_picker" accept="image/*" multiple data-max-files="6">
                            </label>
                        </div>

                        <div class="photo-grid">
                            <div class="photo-card">
                                <div class="photo-label">Foto 1</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo1">
                                    <div class="photo-placeholder" id="placeholder_photo1">Cambiar</div>
                                    <input type="file" name="photo1" id="photo1" accept="image/*" required>
                                </label>
                                <div class="photo-status" id="status_photo1">Pendiente</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 2</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo2">
                                    <div class="photo-placeholder" id="placeholder_photo2">Cambiar</div>
                                    <input type="file" name="photo2" id="photo2" accept="image/*" required>
                                </label>
                                <div class="photo-status" id="status_photo2">Pendiente</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 3</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo3">
                                    <div class="photo-placeholder" id="placeholder_photo3">Cambiar</div>
                                    <input type="file" name="photo3" id="photo3" accept="image/*" required>
                                </label>
                                <div class="photo-status" id="status_photo3">Pendiente</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 4</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo4">
                                    <div class="photo-placeholder" id="placeholder_photo4">Cambiar</div>
                                    <input type="file" name="photo4" id="photo4" accept="image/*" required>
                                </label>
                                <div class="photo-status" id="status_photo4">Pendiente</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 5</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo5">
                                    <div class="photo-placeholder" id="placeholder_photo5">Cambiar</div>
                                    <input type="file" name="photo5" id="photo5" accept="image/*" required>
                                </label>
                                <div class="photo-status" id="status_photo5">Pendiente</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 6</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo6">
                                    <div class="photo-placeholder" id="placeholder_photo6">Cambiar</div>
                                    <input type="file" name="photo6" id="photo6" accept="image/*" required>
                                </label>
                                <div class="photo-status" id="status_photo6">Pendiente</div>
                            </div>

                        </div>

                        <div class="mini-note">
                            Recomendación: formato vertical. Lo importante es que sean recuerdos que de verdad tengan sentido.
                        </div>
                    </div>

                    <div class="section s4">
                        <div class="section-title">Qué quieres provocar</div>

                        <div class="emotion-grid">
                            <div class="emotion-card" data-type="cumpleanos">
                                <div class="emotion-title">Cumpleaños</div>
                                <div class="emotion-sub">Un día que merece quedarse.</div>
                            </div>
                            <div class="emotion-card" data-type="amor">
                                <div class="emotion-title">Amor</div>
                                <div class="emotion-sub">Cuando lo que sientes ya no cabe dentro.</div>
                            </div>
                            <div class="emotion-card" data-type="madre">
                                <div class="emotion-title">Mamá</div>
                                <div class="emotion-sub">Para quien siempre fue hogar.</div>
                            </div>
                            <div class="emotion-card" data-type="padre">
                                <div class="emotion-title">Papá</div>
                                <div class="emotion-sub">Para quien dejó huella sin hacer ruido.</div>
                            </div>
                            <div class="emotion-card" data-type="familia">
                                <div class="emotion-title">Familia</div>
                                <div class="emotion-sub">Para quienes siempre vuelven a ti.</div>
                            </div>
                            <div class="emotion-card" data-type="amistad">
                                <div class="emotion-title">Amistad</div>
                                <div class="emotion-sub">Para esa persona que se quedó.</div>
                            </div>
                            <div class="emotion-card" data-type="distancia">
                                <div class="emotion-title">Distancia</div>
                                <div class="emotion-sub">Cuando alguien está lejos, pero sigue cerca.</div>
                            </div>
                            <div class="emotion-card" data-type="perdon">
                                <div class="emotion-title">Perdón</div>
                                <div class="emotion-sub">Para decir algo que cuesta decir.</div>
                            </div>
                            <div class="emotion-card" data-type="reencuentro">
                                <div class="emotion-title">Reencuentro</div>
                                <div class="emotion-sub">Cuando algo vuelve después del tiempo.</div>
                            </div>
                            <div class="emotion-card" data-type="gratitud">
                                <div class="emotion-title">Gracias</div>
                                <div class="emotion-sub">Para agradecer de verdad.</div>
                            </div>
                            <div class="emotion-card" data-type="superacion">
                                <div class="emotion-title">Superación</div>
                                <div class="emotion-sub">Para recordarle todo lo que vale.</div>
                            </div>
                            <div class="emotion-card" data-type="sorpresa">
                                <div class="emotion-title">Sorpresa</div>
                                <div class="emotion-sub">Cuando quieres tocar el corazón sin avisar.</div>
                            </div>
                            <div class="emotion-card" data-type="esfuerzo">
                                <div class="emotion-title">Esfuerzo</div>
                                <div class="emotion-sub">Para reconocer lo que a veces no se dice.</div>
                            </div>
                            <div class="emotion-card selected" data-type="no_se_decirlo">
                                <div class="emotion-title">No sé cómo decirlo</div>
                                <div class="emotion-sub">Cuando ETERNA debe decirlo por ti.</div>
                            </div>
                        </div>

                        <input type="hidden" name="message_type" id="messageType" value="no_se_decirlo" required>
                    </div>

                    </div>

                    <div class="form-step active" id="formStep2">
                        <div class="atmosphere-title">Ahora dale intención: palabras, momento de entrega y pago seguro.</div>

                    <div class="section s5">
                        <div class="section-title">Las palabras</div>

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
                            <textarea name="phrase_1" id="phrase_1" placeholder="Lo que nunca quieres que olvide" maxlength="220"></textarea>
                            <textarea name="phrase_2" id="phrase_2" placeholder="Eso que sientes y a veces no dices" maxlength="220"></textarea>
                            <textarea name="phrase_3" id="phrase_3" placeholder="La frase que quieres dejarle para siempre" maxlength="220"></textarea>
                        </div>
                    </div>

                    <div class="section s6">
                        <div class="section-title">El momento exacto</div>

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
                            Si añades regalo económico: +{money(FIXED_PLATFORM_FEE)}€ gestión segura + {(GIFT_COMMISSION_RATE * 100):.0f}% del importe regalado<br>
                            Entrega programada: +{money(SCHEDULED_DELIVERY_FEE)}€ solo si eliges guardarlo y entregarlo en un momento exacto
                        </div>

                        <div class="hint">
                            No solo eliges lo que va a sentir. También eliges cuándo debe ocurrir.
                        </div>

                        <div class="error-box" id="errorBox"></div>

                        <label style="
                            display:flex;
                            gap:12px;
                            align-items:flex-start;
                            margin-top:18px;
                            padding:16px;
                            border-radius:18px;
                            background:rgba(255,255,255,0.055);
                            border:1px solid rgba(218,178,92,0.22);
                            color:rgba(255,255,255,0.78);
                            font-size:13px;
                            line-height:1.65;
                        ">
                            <input
                                type="checkbox"
                                id="responsible_use_accepted"
                                name="responsible_use_accepted"
                                value="1"
                                required
                                style="margin-top:4px; width:18px; height:18px; flex:0 0 auto;"
                            >
                            <span>
                                Acepto crear esta ETERNA de forma responsable. Entiendo que, si la persona destinataria vive la experiencia, podré recibir un recuerdo privado de ese momento. Me comprometo a tratar ese contenido con respeto, a no utilizarlo de forma ofensiva, invasiva o pública, y a compartirlo solo de manera responsable.
                            </span>
                        </label>

                        <div style="margin-top:14px;font-size:13px;line-height:1.7;color:rgba(255,255,255,0.58);text-align:center;">
                            Al continuar, aceptas las
                            <a href="/condiciones" target="_blank" style="color:#fff7e6;text-decoration:underline;">condiciones</a>
                            y la
                            <a href="/privacidad" target="_blank" style="color:#fff7e6;text-decoration:underline;">política de privacidad</a>.
                        </div>

                        <div class="buttons">
                        <button type="submit" id="submitBtn">Crear y pasar al pago seguro</button>
                        </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>


        <div class="payment-overlay" id="paymentOverlay" aria-hidden="true">
            <div class="payment-cinematic">
                <img src="{safe_attr(eterna_asset('checkout_loading'))}" alt="Abriendo pago seguro ETERNA">
                <div class="payment-cinematic-glow" aria-hidden="true"></div>
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

    const recipientCountryCode = document.getElementById("recipient_country_code");
    const recipientPhoneInput = document.getElementById("recipient_phone");
    const formStep1 = document.getElementById("formStep1");
    const formStep2 = document.getElementById("formStep2");
    const progressStep1 = document.getElementById("progressStep1");
    const progressStep2 = document.getElementById("progressStep2");
    const goStep2 = document.getElementById("goStep2");
    const backStep1 = document.getElementById("backStep1");

    function setCreateStep(step) {{
        const first = step === 1;
        if (formStep1) formStep1.classList.toggle("active", first);
        if (formStep2) formStep2.classList.toggle("active", !first);
        if (progressStep1) progressStep1.classList.toggle("active", first);
        if (progressStep2) progressStep2.classList.toggle("active", !first);
        window.scrollTo({{ top: 0, behavior: "smooth" }});
    }}

    function validateFirstStep() {{
        const requiredIds = ["customer_name", "customer_phone", "recipient_name", "recipient_phone"];
        for (const id of requiredIds) {{
            const el = document.getElementById(id);
            if (el && !String(el.value || "").trim()) {{
                showError("Falta completar los datos principales antes de continuar.");
                try {{ el.focus(); }} catch (e) {{}}
                return false;
            }}
        }}
        const messageType = messageTypeInput ? messageTypeInput.value.trim() : "";
        if (!messageType) {{
            showError("Selecciona una emoción para continuar.");
            scrollToEmotionChoice();
            return false;
        }}
        if (!allPhotosPresent()) {{
            showError("Necesitas elegir las 6 fotos antes de continuar.");
            return false;
        }}
        clearError();
        return true;
    }}

    // Flujo one-page: sin botón intermedio ni saltos arriba.

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

    function applyDefaultEmotionIfNeeded() {{
        if (!messageTypeInput) return;
        const current = String(messageTypeInput.value || "").trim();
        if (current) return;

        const defaultType = "no_se_decirlo";
        messageTypeInput.value = defaultType;

        cards.forEach((card) => {{
            const isDefault = (card.dataset.type || "") === defaultType;
            card.classList.toggle("selected", isDefault);
        }});

        saveFormState();
    }}

    function scrollToEmotionChoice() {{
        try {{
            const selected = document.querySelector('.emotion-card.selected') || document.querySelector('.emotion-card');
            if (selected) selected.scrollIntoView({{ behavior: "smooth", block: "center" }});
        }} catch (e) {{}}
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

    function cleanPhoneValue(value) {{
        return (value || "").replace(/[^\\d+]/g, "").trim();
    }}

    function getRecipientCountryCodes() {{
        if (!recipientCountryCode) return [];
        return Array.from(recipientCountryCode.options)
            .map((opt) => opt.value)
            .filter(Boolean)
            .sort((a, b) => b.length - a.length);
    }}

    function splitPhoneForRecipient(rawValue) {{
        const currentCode = recipientCountryCode?.value || "+34";
        const availableCodes = getRecipientCountryCodes();

        let value = cleanPhoneValue(rawValue);

        if (!value) {{
            return {{
                code: currentCode,
                local: ""
            }};
        }}

        if (value.startsWith("00")) {{
            value = "+" + value.slice(2);
        }}

        if (value.startsWith("+")) {{
            const matchedCode = availableCodes.find((code) => value.startsWith(code));

            if (matchedCode) {{
                return {{
                    code: matchedCode,
                    local: value.slice(matchedCode.length).replace(/\\D/g, "")
                }};
            }}

            return {{
                code: currentCode,
                local: value.replace(/\\D/g, "")
            }};
        }}

        const digits = value.replace(/\\D/g, "");
        const currentDigits = currentCode.replace(/\\D/g, "");

        if (digits.startsWith(currentDigits) && digits.length > currentDigits.length + 5) {{
            return {{
                code: currentCode,
                local: digits.slice(currentDigits.length)
            }};
        }}

        return {{
            code: currentCode,
            local: digits
        }};
    }}

    function applyRecipientPhoneValue(rawValue) {{
        if (!recipientPhoneInput || !recipientCountryCode) return;

        const result = splitPhoneForRecipient(rawValue);

        if (result.code) {{
            recipientCountryCode.value = result.code;
        }}

        recipientPhoneInput.value = result.local || "";
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

    if (recipientPhoneInput) {{
        recipientPhoneInput.addEventListener("blur", function () {{
            if (!recipientPhoneInput.value) return;
            applyRecipientPhoneValue(recipientPhoneInput.value);
        }});
    }}

    if (recipientCountryCode) {{
        recipientCountryCode.addEventListener("change", saveFormState);
    }}

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


    function setInputFile(input, file) {{
        if (!input || !file) return false;
        try {{
            const dt = new DataTransfer();
            dt.items.add(file);
            input.files = dt.files;
            input.dispatchEvent(new Event("change", {{ bubbles: true }}));
            return true;
        }} catch (e) {{
            console.error("No se pudo asignar la foto", e);
            return false;
        }}
    }}

    const multiPhotoPicker = document.getElementById("multi_photo_picker");
    if (multiPhotoPicker) {{
        multiPhotoPicker.addEventListener("change", function () {{
            clearError();
            const rawFiles = Array.from(multiPhotoPicker.files || []);
            const files = rawFiles.filter((file) => (file.type || "").startsWith("image/"));

            if (!rawFiles.length) return;

            // RC44: ETERNA trabaja con EXACTAMENTE 6 fotos.
            // No usamos silenciosamente "las 6 primeras", porque eso confundía al usuario
            // y podía dejar el formulario en un estado raro después de seleccionar 7/8 fotos en ordenador.
            if (rawFiles.length > 6 || files.length > 6) {{
                multiPhotoPicker.value = "";
                showError("Has elegido más de 6 fotos. Para crear tu ETERNA selecciona exactamente 6 recuerdos.");
                return;
            }}

            if (files.length < 6) {{
                showError("Elige exactamente 6 fotos para crear ETERNA.");
                return;
            }}

            for (const file of files) {{
                if (!(file.type || "").startsWith("image/")) {{
                    multiPhotoPicker.value = "";
                    showError("Una de las fotos no parece una imagen válida.");
                    return;
                }}
            }}

            files.forEach((file, index) => {{
                const input = document.getElementById("photo" + (index + 1));
                setInputFile(input, file);
            }});

            saveFormState();
        }});
    }}

    function autoGrowTextarea(el) {{
        if (!el) return;
        el.style.height = "auto";
        el.style.height = Math.max(96, el.scrollHeight) + "px";
    }}

    ["phrase_1", "phrase_2", "phrase_3"].forEach((id) => {{
        const el = document.getElementById(id);
        if (!el) return;
        el.addEventListener("input", function () {{ autoGrowTextarea(el); saveFormState(); }});
        autoGrowTextarea(el);
    }});

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

        const responsibleUse = document.getElementById("responsible_use_accepted");
        if (responsibleUse && !responsibleUse.checked) {{
            showError("Antes de continuar debes aceptar el uso responsable de ETERNA.");
            try {{ responsibleUse.focus(); }} catch (e) {{}}
            return false;
        }}

        if (!form.checkValidity()) {{
            showError("Revisa los campos. Falta información.");
            return false;
        }}

        const messageType = messageTypeInput ? messageTypeInput.value.trim() : "";
        if (!messageType) {{
            showError("Selecciona una emoción para continuar.");
            scrollToEmotionChoice();
            return false;
        }}

        if (!allPhotosPresent()) {{
            showError("Necesitas elegir exactamente 6 fotos.");
            return false;
        }}

        // RC44: defensa final antes de enviar. Cada slot debe llevar solo una foto.
        for (const id of ["photo1", "photo2", "photo3", "photo4", "photo5", "photo6"]) {{
            const input = document.getElementById(id);
            if (!input || !input.files || input.files.length !== 1) {{
                showError("ETERNA necesita exactamente 6 fotos: una en cada hueco.");
                return false;
            }}
        }}

        if (manualRadio && manualRadio.checked) {{
            const phrase1 = form.querySelector('[name="phrase_1"]')?.value.trim();
            const phrase2 = form.querySelector('[name="phrase_2"]')?.value.trim();
            const phrase3 = form.querySelector('[name="phrase_3"]')?.value.trim();

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
    applyDefaultEmotionIfNeeded();
    bindAutosave();
    updatePhraseMode();
    updateDeliveryMode();

    let eternaSubmitting = false;

    function showPaymentLoadingNow() {{
        if (button) {{
            button.disabled = true;
            button.classList.add("is-loading");
            button.innerText = "Abriendo pago seguro...";
        }}

        // RC25: NO mostramos overlay intermedio dentro del formulario.
        // Solo debe existir UNA pantalla entre formulario y Stripe: /checkout-loading.
        // Esto elimina la pantalla negra y la doble/triple transición.
        const paymentOverlay = document.getElementById("paymentOverlay");
        if (paymentOverlay) {{
            paymentOverlay.classList.remove("show");
            paymentOverlay.setAttribute("aria-hidden", "true");
        }}
    }}

    form.addEventListener("submit", function (e) {{
        if (eternaSubmitting) {{
            return;
        }}

        if (recipientPhoneInput && recipientPhoneInput.value) {{
            applyRecipientPhoneValue(recipientPhoneInput.value);
        }}

        if (!validateBeforeSubmit()) {{
            e.preventDefault();
            return;
        }}

        e.preventDefault();
        eternaSubmitting = true;
        clearError();
        showPaymentLoadingNow();

        try {{
            localStorage.removeItem(STORAGE_KEY);
        }} catch (err) {{
            console.error("localStorage remove error", err);
        }}

        // Importante en móvil: dejamos que el navegador pinte la pantalla
        // Pantalla cinematográfica antes de empezar la subida pesada de las 6 fotos.
        window.requestAnimationFrame(function () {{
            window.setTimeout(function () {{
                form.submit();
            }}, 140);
        }});
    }});

}});
</script>
    </body>
    </html>
    """

# =========================================================
# HOME / CREATE
# =========================================================


def render_create_intro() -> HTMLResponse:
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
        <title>Crear ETERNA</title>
        <style>
            * {{ box-sizing: border-box; }}
            html, body {{ margin:0; min-height:100%; background:#020817; }}
            body {{
                min-height:100vh;
                color:#fff7e6;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                overflow-x:hidden;
                background:
                    radial-gradient(circle at 50% -10%, rgba(218,178,92,.22), transparent 36%),
                    radial-gradient(circle at 20% 90%, rgba(64,156,255,.12), transparent 30%),
                    linear-gradient(180deg,#020817,#000 58%,#020817);
            }}
            .stage {{
                min-height:100vh;
                display:flex;
                align-items:center;
                justify-content:center;
                padding: max(22px, env(safe-area-inset-top)) 18px max(28px, env(safe-area-inset-bottom));
            }}
            .phone {{
                width:100%;
                max-width:430px;
                min-height: min(820px, 94vh);
                border-radius:38px;
                padding:26px 22px;
                position:relative;
                overflow:hidden;
                border:1px solid rgba(218,178,92,.20);
                background:
                    linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.018)),
                    rgba(0,0,0,.68);
                box-shadow:0 30px 90px rgba(0,0,0,.72), inset 0 0 0 1px rgba(255,255,255,.035);
            }}
            .phone:before {{
                content:"";
                position:absolute;
                inset:-30%;
                background: radial-gradient(circle, rgba(64,156,255,.10), transparent 28%);
                animation: breathe 9s ease-in-out infinite;
                pointer-events:none;
            }}
            @keyframes breathe {{ 0%,100% {{ transform:scale(1); opacity:.55; }} 50% {{ transform:scale(1.12); opacity:1; }} }}
            .content {{ position:relative; z-index:2; min-height: calc(min(820px, 94vh) - 52px); display:flex; flex-direction:column; }}
            .brand {{
                letter-spacing:5px;
                font-size:13px;
                color:rgba(218,178,92,.92);
                text-align:center;
                margin-top:8px;
            }}
            .orb {{
                width:86px;
                height:86px;
                margin:42px auto 34px;
                border-radius:999px;
                border:1px solid rgba(218,178,92,.35);
                box-shadow:0 0 44px rgba(218,178,92,.22), inset 0 0 28px rgba(218,178,92,.10);
                display:flex;
                align-items:center;
                justify-content:center;
                color:rgba(218,178,92,.92);
                font-size:34px;
                animation: pulse 4.8s ease-in-out infinite;
            }}
            @keyframes pulse {{ 0%,100% {{ transform:scale(1); }} 50% {{ transform:scale(1.045); }} }}
            .line {{
                font-family: Georgia, "Times New Roman", serif;
                font-size: clamp(31px, 8vw, 43px);
                line-height:1.08;
                text-align:center;
                letter-spacing:-.7px;
                margin:0;
                opacity:0;
                transform:translateY(18px);
                animation: reveal 1.6s ease forwards;
            }}
            .line.two {{ animation-delay:1.25s; color:rgba(255,255,255,.88); }}
            .line.three {{ animation-delay:2.65s; color:rgba(218,178,92,.95); }}
            @keyframes reveal {{ to {{ opacity:1; transform:translateY(0); }} }}
            .copy {{
                margin:30px auto 0;
                max-width:330px;
                text-align:center;
                color:rgba(255,255,255,.58);
                line-height:1.8;
                font-size:15px;
                opacity:0;
                animation: reveal 1.4s ease forwards;
                animation-delay:4.1s;
            }}
            .mock {{
                margin:34px auto 0;
                width:76%;
                max-width:250px;
                aspect-ratio:9/16;
                border-radius:30px;
                border:1px solid rgba(218,178,92,.26);
                background:
                    radial-gradient(circle at 50% 25%, rgba(255,255,255,.16), transparent 34%),
                    linear-gradient(180deg, rgba(218,178,92,.10), rgba(0,0,0,.55));
                box-shadow:0 22px 60px rgba(0,0,0,.58);
                position:relative;
                overflow:hidden;
                opacity:0;
                transform:translateY(20px) scale(.98);
                animation: revealMock 1.7s ease forwards;
                animation-delay:5.2s;
            }}
            @keyframes revealMock {{ to {{ opacity:1; transform:translateY(0) scale(1); }} }}
            .mock:after {{
                content:"Tu ETERNA ha vuelto";
                position:absolute;
                left:18px;
                right:18px;
                bottom:22px;
                text-align:center;
                font-family:Georgia,"Times New Roman",serif;
                font-size:20px;
                color:rgba(255,255,255,.9);
            }}
            .actions {{ margin-top:auto; padding-top:30px; display:grid; gap:12px; }}
            .btn {{
                display:block;
                width:100%;
                padding:18px 22px;
                border-radius:999px;
                text-align:center;
                text-decoration:none;
                font-weight:800;
                letter-spacing:.3px;
                background:linear-gradient(135deg,#f6e1a8,#c89d45);
                color:#120d05;
                box-shadow:0 14px 34px rgba(218,178,92,.22);
            }}
            .ghost {{
                background:rgba(255,255,255,.055);
                color:rgba(255,255,255,.78);
                border:1px solid rgba(255,255,255,.08);
                box-shadow:none;
            }}
            .tiny {{
                text-align:center;
                margin-top:12px;
                color:rgba(255,255,255,.35);
                font-size:12px;
                line-height:1.5;
            }}
        </style>
    </head>
    <body>


<div aria-hidden="true" data-eterna-cinematic-scene="1" style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:1;mix-blend-mode:screen;">
    <div style="position:absolute;inset:-18%;background:radial-gradient(circle at 76% 18%,rgba(92,191,255,.28),transparent 24%),radial-gradient(circle at 63% 52%,rgba(23,82,190,.24),transparent 30%),radial-gradient(circle at 18% 82%,rgba(218,178,92,.12),transparent 28%);filter:blur(2px);opacity:.95;"></div>
    <svg viewBox="0 0 900 900" preserveAspectRatio="xMidYMid slice" style="position:absolute;inset:-7%;width:114%;height:114%;opacity:.98;filter:drop-shadow(0 0 26px rgba(125,210,255,.72)) drop-shadow(0 0 82px rgba(37,99,235,.42));" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="cinema_core" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
                <stop offset="20%" stop-color="#dff6ff" stop-opacity=".92"/>
                <stop offset="58%" stop-color="#69bfff" stop-opacity=".46"/>
                <stop offset="100%" stop-color="#061428" stop-opacity="0"/>
            </radialGradient>
            <linearGradient id="cinema_wing" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#ffffff" stop-opacity=".96"/>
                <stop offset="22%" stop-color="#c7eeff" stop-opacity=".88"/>
                <stop offset="58%" stop-color="#4aa4ff" stop-opacity=".56"/>
                <stop offset="100%" stop-color="#071c4b" stop-opacity=".08"/>
            </linearGradient>
            <filter id="wingTexture" x="-30%" y="-30%" width="160%" height="160%">
                <feTurbulence type="fractalNoise" baseFrequency="0.012 0.032" numOctaves="4" seed="8" result="noise"/>
                <feDisplacementMap in="SourceGraphic" in2="noise" scale="10" xChannelSelector="R" yChannelSelector="G"/>
                <feGaussianBlur stdDeviation="0.25"/>
            </filter>
            <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
                <feGaussianBlur stdDeviation="14" result="blur"/>
                <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
        </defs>
        <g opacity=".95">
            <path d="M836 83 C724 138 657 212 597 300 C538 388 476 430 403 461 C310 500 202 506 83 606" fill="none" stroke="#72d8ff" stroke-width="3" stroke-linecap="round" opacity=".28"/>
            <path d="M812 128 C706 169 638 237 585 318 C532 399 458 460 375 492 C284 528 186 536 91 626" fill="none" stroke="#f6c56f" stroke-width="2" stroke-linecap="round" opacity=".18"/>
            <path d="M850 178 C743 199 660 259 595 351 C530 443 451 507 360 544" fill="none" stroke="#b6ecff" stroke-width="1.4" stroke-linecap="round" opacity=".20"/>
        </g>
        <g opacity=".96">
            <animateTransform attributeName="transform" type="translate" values="0 0;-14 -20;0 0" dur="12s" repeatCount="indefinite"/>
            <circle cx="640" cy="222" r="250" fill="url(#cinema_core)" opacity=".28" filter="url(#softGlow)"/>
            <g filter="url(#wingTexture)" opacity=".96">
                <path d="M626 226 C535 85 523 12 592 8 C681 2 694 140 642 229 Z" fill="url(#cinema_wing)" opacity=".92"/>
                <path d="M655 226 C703 80 810 8 866 57 C928 112 794 211 669 244 Z" fill="url(#cinema_wing)" opacity=".92"/>
                <path d="M622 244 C508 233 451 278 485 332 C526 398 599 324 637 254 Z" fill="url(#cinema_wing)" opacity=".70"/>
                <path d="M667 250 C772 233 849 276 814 337 C776 402 699 326 655 256 Z" fill="url(#cinema_wing)" opacity=".70"/>
                <path d="M646 168 C655 201 655 242 646 315" stroke="#f9feff" stroke-width="10" stroke-linecap="round" opacity=".72"/>
                <path d="M590 50 C620 92 632 139 642 199 M735 62 C700 105 675 155 657 205 M515 278 C561 263 600 255 634 251 M791 282 C744 266 704 257 666 252" stroke="#ffffff" stroke-width="2.2" stroke-opacity=".32" fill="none"/>
            </g>
        </g>
        <g opacity=".86">
            <animate attributeName="opacity" values=".55;.95;.55" dur="5.5s" repeatCount="indefinite"/>
            <circle cx="796" cy="149" r="2.8" fill="#e8fbff"/><circle cx="752" cy="176" r="1.8" fill="#74d7ff"/><circle cx="706" cy="210" r="2.1" fill="#f7ca78"/><circle cx="650" cy="253" r="1.6" fill="#c8f2ff"/><circle cx="594" cy="300" r="1.7" fill="#82d8ff"/><circle cx="528" cy="359" r="1.9" fill="#f4c771"/><circle cx="456" cy="421" r="1.4" fill="#b8eeff"/><circle cx="375" cy="488" r="1.6" fill="#81d9ff"/><circle cx="284" cy="529" r="1.2" fill="#f7cf83"/>
        </g>
        <g opacity=".62" filter="url(#softGlow)">
            <animateTransform attributeName="transform" type="translate" values="0 0;16 -18;0 0" dur="14s" repeatCount="indefinite"/>
            <path d="M198 562 C155 492 154 446 190 441 C237 434 242 518 207 565 Z" fill="#dff7ff" opacity=".46"/>
            <path d="M215 562 C244 494 297 449 326 473 C360 501 292 551 222 573 Z" fill="#7fcfff" opacity=".42"/>
            <path d="M206 549 C211 570 210 594 204 625" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".52"/>
        </g>
    </svg>
    <div style="position:absolute;right:0;top:0;width:70vw;height:70vh;background:radial-gradient(ellipse at 70% 28%,rgba(185,237,255,.18),transparent 38%);filter:blur(24px);opacity:.88;"></div>
</div>


        <main class="stage" style="position:relative;z-index:2;">
            <section class="phone">
                <div class="content">
                    <div class="brand">ETERNA</div>
                    <div class="orb">♥</div>
                    <h1 class="line">No todo lo importante</h1>
                    <h2 class="line two">debería desaparecer.</h2>
                    <h2 class="line three">Haz que vuelva.</h2>
                    <p class="copy">
                        Crea una experiencia íntima con fotos, palabras y un momento que volverá a ti convertido en emoción real.
                    </p>
                    
                    <div class="actions">
                        <a class="btn" href="/crear">Crear mi ETERNA</a>
                        
                    </div>
                    <div class="tiny">6 fotos. 3 frases. Un recuerdo que vuelve.</div>
                </div>
            </section>
        </main>
    </body>
    </html>
    """)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>ETERNA</title>
    <meta name="theme-color" content="#02050a">
    <style>
        * { box-sizing: border-box; }
        html, body { margin:0; width:100%; min-height:100%; background:#02050a; }
        body {
            min-height:100vh;
            overflow-x:hidden;
            font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
            background:
                radial-gradient(circle at 50% 12%, rgba(57,166,255,.20), transparent 36%),
                radial-gradient(circle at 50% 92%, rgba(212,175,55,.14), transparent 42%),
                #02050a;
        }
        .screen {
            position:relative;
            width:100%;
            min-height:100vh;
            display:flex;
            justify-content:center;
            background:#02050a;
            overflow:hidden;
        }
        .phone {
            position:relative;
            width:100%;
            max-width:430px;
            min-height:100vh;
            overflow:hidden;
            background:#02050a;
        }
        .hero-img {
            width:100%;
            max-width:430px;
            min-height:100vh;
            height:auto;
            display:block;
            object-fit:cover;
            object-position:top center;
            background:#02050a;
            filter: drop-shadow(0 0 34px rgba(44,169,255,.12));
        }
        .butterfly-halo {
            position:absolute;
            left:50%;
            top:42%;
            width:64vw;
            max-width:310px;
            aspect-ratio:1;
            transform:translate(-50%,-50%);
            border-radius:999px;
            pointer-events:none;
            background:radial-gradient(circle, rgba(37,181,255,.26), rgba(37,181,255,.08) 33%, transparent 68%);
            filter:blur(16px);
            opacity:.62;
            animation:eternaHalo 5.8s ease-in-out infinite;
            mix-blend-mode:screen;
        }
        .water-shine {
            position:absolute;
            left:-30%;
            right:-30%;
            bottom:10%;
            height:20%;
            pointer-events:none;
            background:linear-gradient(105deg, transparent 0%, rgba(69,198,255,.00) 28%, rgba(69,198,255,.18) 48%, rgba(255,210,121,.12) 54%, transparent 72%);
            filter:blur(18px);
            opacity:.44;
            animation:eternaWater 9s ease-in-out infinite;
            mix-blend-mode:screen;
        }
        .sparkle {
            position:absolute;
            width:5px;
            height:5px;
            border-radius:50%;
            pointer-events:none;
            background:#6fd7ff;
            box-shadow:0 0 14px #56cfff,0 0 28px rgba(86,207,255,.68);
            opacity:.0;
            animation:eternaFloat 8s linear infinite;
        }
        .sparkle.gold { background:#ffd98b; box-shadow:0 0 14px #ffd98b,0 0 28px rgba(255,217,139,.62); }
        .s1 { left:22%; bottom:18%; animation-delay:.2s; }
        .s2 { left:72%; bottom:24%; animation-delay:1.8s; transform:scale(.72); }
        .s3 { left:48%; bottom:12%; animation-delay:3.2s; transform:scale(.58); }
        .s4 { left:63%; bottom:42%; animation-delay:4.7s; transform:scale(.50); }
        @keyframes eternaHalo { 0%,100% { transform:translate(-50%,-50%) scale(.96); opacity:.38; } 50% { transform:translate(-50%,-50%) scale(1.08); opacity:.78; } }
        @keyframes eternaWater { 0%,100% { transform:translateX(-9%); opacity:.24; } 50% { transform:translateX(9%); opacity:.58; } }
        @keyframes eternaFloat { 0% { transform:translateY(0) scale(.6); opacity:0; } 16% { opacity:.9; } 78% { opacity:.38; } 100% { transform:translateY(-150px) scale(1.1); opacity:0; } }
        .real-cta {
            position:absolute;
            left:10.8%;
            right:10.8%;
            bottom:calc(env(safe-area-inset-bottom) + 70px);
            min-height:62px;
            border-radius:18px;
            display:block;
            z-index:5;
            text-indent:-9999px;
            overflow:hidden;
            background:rgba(255,255,255,.001);
            box-shadow:0 0 0 rgba(255,255,255,0);
        }
        .real-cta::after {
            content:"";
            position:absolute;
            inset:-4px;
            border-radius:22px;
            pointer-events:none;
            background:linear-gradient(90deg, transparent, rgba(255,255,255,.32), transparent);
            opacity:0;
            animation:buttonShine 7.5s ease-in-out infinite;
        }
        @keyframes buttonShine { 0%,72%,100% { transform:translateX(-120%); opacity:0; } 78% { opacity:.75; } 90% { transform:translateX(120%); opacity:0; } }
        .fallback {
            display:none;
            width:100%;
            max-width:430px;
            min-height:100vh;
            padding:42px 24px;
            color:#f6f1e8;
            text-align:center;
            flex-direction:column;
            justify-content:center;
            gap:18px;
            background:radial-gradient(circle at 50% 22%, rgba(59,167,255,.18), transparent 32%), #02050a;
        }
        .fallback .mark { width:58px;height:58px;border:1px solid rgba(212,175,55,.75);border-radius:50%;display:grid;place-items:center;margin:0 auto;color:#d4af37;font-family:Georgia,serif;font-size:30px; }
        .fallback h1 { margin:0;color:#f3d98b;font-size:48px;letter-spacing:.18em; }
        .fallback a { display:inline-flex;align-items:center;justify-content:center;margin:10px auto 0;min-height:56px;padding:0 26px;border-radius:18px;color:#120b02;background:linear-gradient(135deg,#fff0bd,#e7bd61,#b87927);font-weight:900;font-size:13px;letter-spacing:.12em;text-transform:uppercase;text-decoration:none; }
    </style>
</head>
<body>
    <main class="screen">
        <section class="phone" aria-label="ETERNA">
            <img class="hero-img" src="/eterna-assets/home_mobile?v=eterna-home-rc12" alt="ETERNA" onerror="this.style.display='none'; document.getElementById('fallback-home').style.display='flex';">
            <div class="butterfly-halo" aria-hidden="true"></div>
            <div class="water-shine" aria-hidden="true"></div>
            <i class="sparkle s1" aria-hidden="true"></i>
            <i class="sparkle gold s2" aria-hidden="true"></i>
            <i class="sparkle s3" aria-hidden="true"></i>
            <i class="sparkle gold s4" aria-hidden="true"></i>
            <a class="real-cta" href="/crear" aria-label="Crear mi ETERNA">Crear mi ETERNA</a>
            <section id="fallback-home" class="fallback">
                <div class="mark">E</div>
                <h1>ETERNA</h1>
                <p>Hay momentos que merecen quedarse para siempre.</p>
                <a href="/crear">Crear mi ETERNA</a>
            </section>
        </section>
    </main>
</body>
</html>
    """)


@app.get("/crear", response_class=HTMLResponse)
def crear_get():
    return render_create_form()


@app.get("/crear/entrada", response_class=HTMLResponse)
def crear_entrada_get():
    return RedirectResponse(url="/crear", status_code=303)


@app.get("/crear/formulario", response_class=HTMLResponse)
def crear_formulario_get():
    return RedirectResponse(url="/crear", status_code=303)


# =========================================================
# CREAR PEDIDO
# =========================================================

@app.post("/crear")
async def crear_post(
    customer_name: str = Form(...),
    customer_email: str = Form(""),
    customer_country_code: str = Form(...),
    customer_phone: str = Form(...),
    recipient_name: str = Form(...),
    recipient_country_code: str = Form(...),
    recipient_phone: str = Form(...),
    message_type: str = Form(...),
    phrase_mode: str = Form(...),
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
    responsible_use_accepted: str = Form(""),
    responsible_use: str = Form(""),
    yul_memory_place: str = Form(""),
    yul_memory_detail: str = Form(""),
    yul_emotion_tone: str = Form(""),
    yul_magic_hint: str = Form(""),
):
    try:
        return await create_order_and_redirect(
            customer_name,
            customer_email,
            customer_country_code,
            customer_phone,
            recipient_name,
            recipient_country_code,
            recipient_phone,
            message_type,
            phrase_mode,
            phrase_1,
            phrase_2,
            phrase_3,
            delivery_mode,
            delivery_date,
            delivery_time,
            gift_amount,
            photo1,
            photo2,
            photo3,
            photo4,
            photo5,
            photo6,
            responsible_use_accepted or responsible_use,
            yul_memory_place,
            yul_memory_detail,
            yul_emotion_tone,
            yul_magic_hint,
        )

    except HTTPException as e:
        print("🔥 ERROR CONTROLADO EN /crear:", e.detail)
        raise e

    except Exception as e:
        print("🔥 ERROR EN /crear:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error creando el pedido")


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
    """
    Worker blindado para avisar al regalante.

    Regla importante:
    después de un deploy NO debe volver a procesar pedidos antiguos agotados.
    Solo trae pedidos realmente pendientes:
    - pagados
    - con reacción recibida
    - sin SMS/WhatsApp enviado al regalante
    - sin sender_notified
    - con menos de 3 intentos

    Esto evita el ruido infinito tipo:
    max_attempts_reached / sms_disabled_by_config / whatsapp_disabled
    en cada arranque o ciclo del worker.
    """
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id
        FROM orders
        WHERE
            COALESCE(paid, 0) = 1
            AND COALESCE(reaction_uploaded, 0) = 1
            AND COALESCE(sender_sms_sent_at, '') = ''
            AND COALESCE(sender_notified, 0) = 0
            AND COALESCE(sender_sms_attempts, 0) < 3
        ORDER BY created_at ASC
    """)
    rows = cur.fetchall()
    conn.close()
    return [r["id"] for r in rows]

def list_pending_payout_orders():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id
        FROM orders
        WHERE
            COALESCE(paid, 0) = 1
            AND COALESCE(gift_amount, 0) > 0
            AND COALESCE(reaction_uploaded, 0) = 1
            AND COALESCE(experience_completed, 0) = 1
            AND COALESCE(connect_onboarding_completed, 0) = 1
            AND COALESCE(transfer_completed, 0) = 0
            AND COALESCE(cashout_completed, 0) = 0
            AND COALESCE(gift_refunded, 0) = 0
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

def process_all_due_payouts() -> list[dict]:
    results = []

    for order_id in list_pending_payout_orders():
        try:
            order = get_order_by_id(order_id)

            try:
                if order.get("stripe_connected_account_id"):
                    refresh_connect_status(order)
                    order = get_order_by_id(order_id)
            except Exception as e:
                log_error("payout_worker_refresh_connect_status", e)

            if not bool(order.get("connect_onboarding_completed")):
                results.append({
                    "order_id": order_id,
                    "result": {
                        "status": "onboarding_not_ready",
                        "retry": True,
                    },
                })
                continue

            result = process_gift_transfer_for_order(order)
            print("💸 Worker payout:", order_id, result)

            results.append({
                "order_id": order_id,
                "result": result,
            })

        except Exception as e:
            log_error("payout_worker_process", e)
            results.append({
                "order_id": order_id,
                "result": {
                    "status": "error",
                    "error": str(e),
                    "retry": True,
                },
            })

    return results


# =========================================================
# RC74 FULL — COLA, RECOVERY Y AUTOGESTIÓN
# =========================================================

def rc74_admin_guard(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")


def rc74_parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return None


def rc74_minutes_since(value):
    dt = rc74_parse_dt(value)
    if not dt:
        return None
    try:
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
        return int((now - dt).total_seconds() // 60)
    except Exception:
        return None


def rc74_computed_order_state(order: dict) -> str:
    if not order:
        return "UNKNOWN"
    if not bool(order.get("paid")):
        return "CREATED"
    if bool(order.get("reaction_uploaded")) and bool(order.get("sender_notified")):
        return "SENDER_PACK_SENT"
    if bool(order.get("reaction_uploaded")):
        return "REACTION_UPLOADED"
    if bool(order.get("experience_completed")):
        return "COMPLETED"
    if bool(order.get("experience_started")):
        return "STARTED"
    if bool(order.get("delivered_to_recipient")) or bool(order.get("delivery_sent")):
        return "DELIVERED"
    if order.get("experience_video_url"):
        return "RENDERED"
    if bool(order.get("video_render_requested")):
        return "RENDERING"
    return "PENDING_RENDER"


def rc74_count(where_sql: str, params=()):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) AS c FROM orders WHERE {where_sql}", tuple(params))
    row = cur.fetchone()
    conn.close()
    return int(row["c"] if row else 0)


def rc74_list_orders(where_sql: str, params=(), limit: int = 50):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT
            id, paid, order_state, order_version, render_status, render_attempts,
            video_render_requested, video_render_requested_at, render_started_at, render_last_error,
            experience_video_url, delivered_to_recipient, delivery_sent, delivery_sent_at,
            experience_started, experience_completed, reaction_uploaded, sender_notified,
            recipient_sms_attempts, sender_sms_attempts, recipient_sms_error, sender_sms_error,
            created_at, updated_at
        FROM orders
        WHERE {where_sql}
        ORDER BY created_at ASC
        LIMIT ?
    """, tuple(params) + (int(limit),))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    for r in rows:
        r["computed_state"] = rc74_computed_order_state(r)
        r["minutes_since_created"] = rc74_minutes_since(r.get("created_at"))
        r["minutes_since_render_started"] = rc74_minutes_since(r.get("render_started_at") or r.get("video_render_requested_at"))
    return rows


def rc74_queue_snapshot():
    return {
        "pending_render": rc74_count(
            "paid = 1 AND COALESCE(video_render_requested,0) = 0 AND (experience_video_url IS NULL OR experience_video_url = '') AND COALESCE(render_attempts,0) < ?",
            (ETERNA_RENDER_MAX_ATTEMPTS,),
        ),
        "rendering_waiting_callback": rc74_count(
            "paid = 1 AND COALESCE(video_render_requested,0) = 1 AND (experience_video_url IS NULL OR experience_video_url = '')"
        ),
        "failed_render": rc74_count(
            "paid = 1 AND COALESCE(render_attempts,0) >= ? AND (experience_video_url IS NULL OR experience_video_url = '')",
            (ETERNA_RENDER_MAX_ATTEMPTS,),
        ),
        "rendered_not_delivered": rc74_count(
            "paid = 1 AND experience_video_url IS NOT NULL AND experience_video_url != '' AND COALESCE(delivered_to_recipient,0) = 0 AND COALESCE(delivery_sent,0) = 0"
        ),
        "completed_no_reaction": rc74_count(
            "paid = 1 AND COALESCE(experience_completed,0) = 1 AND COALESCE(reaction_uploaded,0) = 0"
        ),
        "reaction_sender_pending": rc74_count(
            "paid = 1 AND COALESCE(reaction_uploaded,0) = 1 AND COALESCE(sender_notified,0) = 0"
        ),
        "recipient_sms_errors": rc74_count("recipient_sms_error IS NOT NULL AND recipient_sms_error != ''"),
        "sender_sms_errors": rc74_count("sender_sms_error IS NOT NULL AND sender_sms_error != ''"),
    }


def rc74_process_render_queue(max_jobs: int = 1):
    """
    Cola persistente: procesa pedidos pagados pendientes de render.
    Batch bajo por seguridad.
    """
    if ETERNA_SAFE_MODE or not ETERNA_RENDER_QUEUE_ENABLED:
        return {"ok": True, "skipped": True, "reason": "safe_mode_or_queue_disabled", "processed": []}

    jobs = rc74_list_orders(
        "paid = 1 AND COALESCE(video_render_requested,0) = 0 AND (experience_video_url IS NULL OR experience_video_url = '') AND COALESCE(render_attempts,0) < ?",
        (ETERNA_RENDER_MAX_ATTEMPTS,),
        limit=max(1, int(max_jobs or 1)),
    )

    processed = []
    for job in jobs:
        order_id = job["id"]
        try:
            order = get_order_by_id(order_id)
            if original_video_ready(order):
                update_order(order_id, render_status="RENDERED", order_state="RENDERED", recovery_last_checked_at=now_iso())
                insert_order_event(order_id, "RENDER_ALREADY_READY", "ok", "La cola detectó que el vídeo ya estaba listo")
                processed.append({"order_id": order_id, "ok": True, "reason": "already_rendered"})
                continue

            phrases = [
                (order.get("phrase_1") or "").strip(),
                (order.get("phrase_2") or "").strip(),
                (order.get("phrase_3") or "").strip(),
            ]

            mark_video_render_requested(order_id)
            data = trigger_video_engine(order_id, phrases)
            insert_order_event(order_id, "RENDER_QUEUE_SENT", "ok", "Pedido enviado al motor desde cola", {"data": data})
            processed.append({"order_id": order_id, "ok": True, "reason": "sent_to_video_engine"})
        except Exception as e:
            clear_video_render_requested(order_id, error=str(e))
            insert_order_event(order_id, "RENDER_QUEUE_ERROR", "error", "La cola no pudo enviar el pedido al motor", {"error": str(e)[:1000]})
            processed.append({"order_id": order_id, "ok": False, "reason": str(e)})
    return {"ok": True, "processed": processed}


def rc74_recover_stuck_renders():
    """
    Recupera renders marcados como RENDERING que llevan demasiado sin callback.
    No pierde pedidos: los devuelve a cola hasta máximo de intentos.
    """
    if ETERNA_SAFE_MODE or not ETERNA_RECOVERY_WORKER_ENABLED:
        return {"ok": True, "skipped": True, "reason": "safe_mode_or_recovery_disabled", "recovered": []}

    stuck = rc74_list_orders(
        "paid = 1 AND COALESCE(video_render_requested,0) = 1 AND (experience_video_url IS NULL OR experience_video_url = '')",
        limit=50,
    )
    recovered = []
    for order in stuck:
        order_id = order["id"]
        minutes = rc74_minutes_since(order.get("render_started_at") or order.get("video_render_requested_at"))
        attempts = int(order.get("render_attempts") or 0)
        if minutes is None or minutes < ETERNA_RENDER_STUCK_MINUTES:
            continue
        if attempts >= ETERNA_RENDER_MAX_ATTEMPTS:
            update_order(
                order_id,
                render_status="FAILED_RENDER",
                order_state="ERROR_NEEDS_REVIEW",
                recovery_last_checked_at=now_iso(),
                recovery_notes=f"Render atascado {minutes} min y máximo de intentos alcanzado",
            )
            insert_order_event(order_id, "RENDER_FAILED_MAX_ATTEMPTS", "error", "Render agotó intentos y requiere revisión", {"minutes": minutes, "attempts": attempts})
            recovered.append({"order_id": order_id, "action": "failed_needs_review", "minutes": minutes, "attempts": attempts})
            continue

        clear_video_render_requested(order_id, error=f"Render atascado {minutes} min; devuelto a cola")
        update_order(order_id, recovery_last_checked_at=now_iso())
        recovered.append({"order_id": order_id, "action": "requeued", "minutes": minutes, "attempts": attempts})

    return {"ok": True, "recovered": recovered}


def rc74_recovery_cycle():
    """
    Ciclo de autocuidado: recupera atascados y procesa cola.
    """
    return {
        "recover_stuck_renders": rc74_recover_stuck_renders(),
        "process_render_queue": rc74_process_render_queue(max_jobs=ETERNA_RENDER_QUEUE_BATCH_SIZE),
    }


@app.get("/admin/health")
def admin_health(token: str = ""):
    rc74_admin_guard(token)
    checks = {}
    try:
        conn = db_conn()
        conn.execute("SELECT 1")
        conn.close()
        checks["db"] = "ok"
    except Exception as e:
        checks["db"] = f"error: {e}"

    checks["stripe_secret"] = "ok" if STRIPE_SECRET_KEY else "missing"
    checks["stripe_webhook"] = "ok" if STRIPE_WEBHOOK_SECRET else "missing"
    checks["twilio_sms"] = "ok" if twilio_enabled() else "missing_or_disabled"
    checks["sms_enabled"] = bool(SMS_ENABLED)
    checks["whatsapp_enabled"] = bool(WHATSAPP_ENABLED)
    checks["video_engine_url"] = VIDEO_ENGINE_URL or "missing"
    checks["r2"] = "ok" if r2_enabled() else "local_fallback"
    checks["delivery_worker_enabled"] = bool(DELIVERY_WORKER_ENABLED)
    checks["recovery_worker_enabled"] = bool(ETERNA_RECOVERY_WORKER_ENABLED)
    checks["safe_mode"] = bool(ETERNA_SAFE_MODE)
    checks["app_version"] = ETERNA_APP_VERSION
    checks["queue"] = rc74_queue_snapshot()
    return {"ok": checks.get("db") == "ok", "checks": checks, "timestamp": now_iso()}


@app.get("/admin/orphans")
def admin_orphans(token: str = ""):
    rc74_admin_guard(token)
    groups = {
        "paid_pending_render": rc74_list_orders("paid = 1 AND COALESCE(video_render_requested,0) = 0 AND (experience_video_url IS NULL OR experience_video_url = '')", limit=50),
        "rendering_waiting_callback": rc74_list_orders("paid = 1 AND COALESCE(video_render_requested,0) = 1 AND (experience_video_url IS NULL OR experience_video_url = '')", limit=50),
        "rendered_not_delivered": rc74_list_orders("paid = 1 AND experience_video_url IS NOT NULL AND experience_video_url != '' AND COALESCE(delivered_to_recipient,0) = 0 AND COALESCE(delivery_sent,0) = 0", limit=50),
        "completed_without_reaction": rc74_list_orders("paid = 1 AND COALESCE(experience_completed,0) = 1 AND COALESCE(reaction_uploaded,0) = 0", limit=50),
        "reaction_without_sender_pack": rc74_list_orders("paid = 1 AND COALESCE(reaction_uploaded,0) = 1 AND COALESCE(sender_notified,0) = 0", limit=50),
    }
    return {"version": ETERNA_APP_VERSION, "groups": groups, "timestamp": now_iso()}


@app.get("/admin/confidence")
def admin_confidence(token: str = ""):
    rc74_admin_guard(token)
    score = 100
    reasons = []
    health = admin_health(token=token)
    checks = health.get("checks", {})
    if checks.get("db") != "ok":
        score -= 35
        reasons.append("DB no está OK")
    if checks.get("stripe_secret") != "ok":
        score -= 15
        reasons.append("Stripe secret ausente")
    if checks.get("stripe_webhook") != "ok":
        score -= 10
        reasons.append("Stripe webhook ausente")
    if not VIDEO_ENGINE_URL:
        score -= 20
        reasons.append("Video Engine URL ausente")
    if checks.get("twilio_sms") != "ok":
        score -= 10
        reasons.append("Twilio/SMS no configurado completo")
    if ETERNA_SAFE_MODE:
        score -= 25
        reasons.append("SAFE MODE activo")

    q = rc74_queue_snapshot()
    risk = (
        q.get("failed_render", 0) * 10
        + q.get("rendering_waiting_callback", 0) * 3
        + q.get("completed_no_reaction", 0) * 5
        + q.get("reaction_sender_pending", 0) * 4
        + q.get("recipient_sms_errors", 0) * 2
        + q.get("sender_sms_errors", 0) * 2
    )
    if risk:
        score -= min(35, risk)
        reasons.append("Hay señales de cola/pedidos/errores que revisar")

    score = max(0, min(100, int(score)))
    status = "LISTA_PARA_PRUEBA_CONTROLADA" if score >= 85 else "REVISAR_ANTES_DE_LANZAR" if score >= 65 else "NO_LANZAR"
    return {"confidence": score, "status": status, "reasons": reasons, "queue": q, "timestamp": now_iso()}


@app.get("/admin/go-live")
def admin_go_live(token: str = ""):
    rc74_admin_guard(token)
    health = admin_health(token=token)
    confidence = admin_confidence(token=token)
    blocking = []
    if health["checks"].get("db") != "ok":
        blocking.append("DB no accesible")
    if not STRIPE_SECRET_KEY:
        blocking.append("Falta STRIPE_SECRET_KEY")
    if not STRIPE_WEBHOOK_SECRET:
        blocking.append("Falta STRIPE_WEBHOOK_SECRET")
    if not VIDEO_ENGINE_URL:
        blocking.append("Falta VIDEO_ENGINE_URL")
    if confidence["confidence"] < 85:
        blocking.append("Confianza menor de 85")
    if ETERNA_SAFE_MODE:
        blocking.append("SAFE MODE activo")

    decision = "APTA_PARA_PRUEBA_CONTROLADA" if not blocking else "NO_LANZAR_AUN"
    return {
        "version": ETERNA_APP_VERSION,
        "decision": decision,
        "blocking": blocking,
        "health": health,
        "confidence": confidence,
        "principle": "Todo puede fallar. Ningún pedido puede perderse jamás.",
        "timestamp": now_iso(),
    }


@app.post("/admin/recovery-cycle")
def admin_recovery_cycle(request: Request):
    admin_token = (request.query_params.get("token") or request.headers.get("x-admin-token") or "").strip()
    rc74_admin_guard(admin_token)
    return rc74_recovery_cycle()


def delivery_worker_loop():
    print("🚀 DELIVERY WORKER STARTED")
    while True:
        try:
            if ETERNA_SAFE_MODE:
                print("🛟 ETERNA_SAFE_MODE activo: no se procesan entregas, SMS, sender packs ni payouts automáticos.")
            else:
                rc74_recovery_cycle()
                process_all_due_scheduled_deliveries()
                process_all_pending_reaction_recoveries()
                process_all_due_sender_notifications()
                process_all_due_payouts()
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
    # RC60 — recuperación tras reinicio/deploy de Render.
    try:
        recover_stale_processing_locks()
        recover_order_states_from_flags()
    except Exception as e:
        log_error("startup_recovery_rc60", e)

    ensure_delivery_worker_started()

    # RC60: barrido único de rescate. No cambia negocio: solo procesa pendientes reales.
    if ETERNA_STARTUP_SWEEP_ENABLED:
        def _startup_safe_sweep():
            try:
                time.sleep(3)
                log_human("RC60 SWEEP ARRANQUE", "Buscando entregas y avisos pendientes tras deploy/reinicio")
                delivery_results = process_all_due_scheduled_deliveries()
                sender_results = process_all_due_sender_notifications()
                log_human(
                    "RC60 SWEEP COMPLETADO",
                    f"📦 Entregas revisadas: {len(delivery_results)}",
                    f"📩 Avisos regalante revisados: {len(sender_results)}",
                )
            except Exception as e:
                log_error("startup_safe_sweep_rc60", e)

        threading.Thread(target=_startup_safe_sweep, daemon=True, name="eterna-rc60-startup-sweep").start()


# =========================================================
# PEDIDO / ENTRADA REGALADO (BLINDADO)
# =========================================================

@app.get("/pedido/{recipient_token}", response_class=HTMLResponse)
def pedido(request: Request, recipient_token: str):
    # Entrada del destinatario con pantallas visuales V1.
    try:
        order = get_order_by_recipient_token_or_404(recipient_token)
        if order_link_expired(order):
            insert_order_event(order["id"], "recipient_link_expired", "warning", "Enlace de destinatario caducado por configuración RC60")
            return render_eterna_image_screen(
                image_name="error-v1.png",
                title="Este momento no está disponible",
                subtitle="Puede que el enlace haya expirado o que haya ocurrido un problema temporal.",
                button_text="Volver al inicio",
                button_href="/",
            )
        insert_order_event(order["id"], "recipient_opened", "ok", "El destinatario abrió el enlace recibido")
    except Exception:
        log_info("🚪 ENTRADA ETERNA CON TOKEN INVÁLIDO", recipient_token)
        return render_eterna_image_screen(
            image_name="error-v1.png",
            fallback_image_name="error-v1.png",
            button_url="/",
            button_label="Volver al inicio",
        )

    if not bool(order.get("paid")):
        return render_eterna_image_screen(
            image_name="error-v1.png",
            fallback_image_name="error-v1.png",
            extra_note="Este acceso aún no está activo.",
        )

    if not original_video_ready(order):
        return render_eterna_image_screen(
            image_name="gift-ready-v1.png",
            fallback_image_name="error-v1.png",
            redirect_url=f"/pedido/{recipient_token}",
            redirect_delay_ms=8000,
            extra_note="Tu ETERNA está tomando forma. No cierres esta pantalla.",
        )

    if not delivery_is_unlocked(order):
        return render_eterna_image_screen(
            image_name="gift-ready-v1.png",
            fallback_image_name="error-v1.png",
            extra_note=f"Esta ETERNA se abrirá en el momento elegido: {scheduled_delivery_display(order)}.",
        )

    if bool(order.get("experience_completed")):
        return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)

    response = RedirectResponse(url=f"/guia/0/{recipient_token}", status_code=303)
    attach_recipient_session_if_needed(order, request, response)
    return response



@app.get("/admin/yul-version")
def admin_yul_version(token: str = ""):
    if ADMIN_TOKEN and token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC82_PREEXPERIENCIA_CLEAN_SAFE",
        "base": "RC75_MAGIA_YUL_FORMULARIO_DEPLOY_SAFE",
        "yul": "particula_estela_indigo",
        "umbral": "trovador_cinematografico",
        "formulario_emocional": True,
        "consent_delay_ms": 55000,
        "touches_core": False,
    }



@app.get("/admin/rc76-version")
def admin_rc76_version(token: str = ""):
    if ADMIN_TOKEN and token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC82_PREEXPERIENCIA_CLEAN_SAFE",
        "golden_master_preserved": True,
        "contains_rc74_core": True,
        "contains_yul_umbral": True,
        "contains_yul_emotional_form": True,
        "contains_runtime_folder_rescue": True,
        "contains_crear_css_fix": True,
        "review_candidate": True,
        "touches_critical_core": False,
    }


@app.get("/admin/rc77-version")
def admin_rc77_version(token: str = ""):
    if ADMIN_TOKEN and token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {"version":"RC82_PREEXPERIENCIA_CLEAN_SAFE","yul_uses_form_values":True,"post_consent_story_bridge":True,"auto_opens_after_camera_ready":True,"touches_critical_core":False}



@app.get("/admin/rc78-version")
def admin_rc78_version(token: str = ""):
    if ADMIN_TOKEN and token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC82_PREEXPERIENCIA_CLEAN_SAFE",
        "formulario_yul": "solo_lugar",
        "uses_real_place": True,
        "generic_romantic_responses": True,
        "does_not_invent_memory": True,
        "touches_critical_core": False,
    }



@app.get("/admin/rc78b-version")
def admin_rc78b_version(token: str = ""):
    if ADMIN_TOKEN and token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC82_PREEXPERIENCIA_CLEAN_SAFE",
        "formulario_yul": "solo_lugar",
        "lugar_real_en_historia": True,
        "no_inventa_recuerdos": True,
        "compatible_db_columns": True,
        "touches_critical_core": False,
    }



@app.get("/admin/rc78c-version")
def admin_rc78c_version(token: str = ""):
    if ADMIN_TOKEN and token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC82_PREEXPERIENCIA_CLEAN_SAFE",
        "formulario_yul": "solo_lugar_visible",
        "lugar_real_en_historia": True,
        "no_inventa_recuerdos": True,
        "compatible_db_columns": True,
        "touches_critical_core": False,
    }



@app.post("/internal/yul-event/{recipient_token}")
async def internal_yul_event(recipient_token: str, request: Request):
    """
    RC79: log ligero de recuperación Yul. Nunca bloquea experiencia.
    """
    try:
        order = get_order_by_recipient_token_or_404(recipient_token)
        payload = await request.json()
        event_name = str(payload.get("event") or "yul_event")[:80]
        meta = payload.get("meta") or {}
        insert_order_event(
            order["id"],
            event_name,
            "ok",
            "Evento de preexperiencia Yul",
            {
                "scene": payload.get("scene"),
                "meta": meta,
                "at": payload.get("at"),
            },
        )
    except Exception as e:
        print("[WARN] yul event ignored:", e)
    return {"ok": True}



@app.get("/admin/rc79-version")
def admin_rc79_version(token: str = ""):
    if ADMIN_TOKEN and token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC82_PREEXPERIENCIA_CLEAN_SAFE",
        "watchdog_global": True,
        "watchdog_scene": True,
        "tap_recovery": True,
        "multi_tap_rescue": True,
        "local_storage_resume": True,
        "visibility_focus_recovery": True,
        "direct_experience_fallback": True,
        "low_power_mode": True,
        "rescue_button": "Abrir mi ETERNA",
        "rule": "Yul es opcional. La ETERNA no.",
        "touches_critical_core": False,
    }



# =========================================================
# RC81 — ADMIN SMS DELIVERY RESCUE
# Solo diagnóstico y reintento controlado. No cambia lógica base de Twilio.
# =========================================================

@app.get("/admin/sms-delivery-check/{order_id}")
def admin_sms_delivery_check(order_id: str, token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    order = get_order_by_id(order_id)
    return {
        "ok": True,
        "order_id": order_id,
        "app_version": ETERNA_APP_VERSION,
        "sms_enabled": SMS_ENABLED,
        "whatsapp_enabled": WHATSAPP_ENABLED,
        "twilio_enabled": twilio_enabled(),
        "twilio_from_number_present": bool(TWILIO_FROM_NUMBER),
        "twilio_whatsapp_from_present": bool(TWILIO_WHATSAPP_FROM),
        "recipient_phone_present": bool(order.get("recipient_phone")),
        "sender_phone_present": bool(order.get("sender_phone")),
        "delivery_mode": order.get("delivery_mode"),
        "scheduled_delivery_at": order.get("scheduled_delivery_at"),
        "delivery_locked": bool(order.get("delivery_locked")),
        "delivery_sent": bool(order.get("delivery_sent")),
        "delivery_sent_at": order.get("delivery_sent_at"),
        "recipient_sms_sent_at": order.get("recipient_sms_sent_at"),
        "recipient_sms_attempts": int(order.get("recipient_sms_attempts") or 0),
        "recipient_sms_error": order.get("recipient_sms_error"),
        "sender_sms_sent_at": order.get("sender_sms_sent_at"),
        "sender_sms_attempts": int(order.get("sender_sms_attempts") or 0),
        "sender_sms_error": order.get("sender_sms_error"),
        "experience_video_url": bool(order.get("experience_video_url")),
        "reaction_uploaded": bool(order.get("reaction_uploaded")),
        "sender_notified": bool(order.get("sender_notified")),
    }


@app.get("/admin/force-recipient-sms/{order_id}")
def admin_force_recipient_sms(order_id: str, token: str = "", reset: int = 0):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    if int(reset or 0) == 1:
        update_order(
            order_id,
            recipient_sms_attempts=0,
            recipient_sms_error=None,
            recipient_sms_sent_at=None,
            recipient_sms_sid=None,
            delivery_sent=0,
            delivery_sent_at=None,
        )
        insert_order_event(order_id, "admin_recipient_sms_reset", "warning", "Intentos SMS destinatario reseteados por admin")
    order = get_order_by_id(order_id)
    result = process_scheduled_recipient_delivery(order_id)
    updated = get_order_by_id(order_id)
    return {
        "ok": bool(result.get("ok")),
        "result": result,
        "recipient_sms_attempts": updated.get("recipient_sms_attempts"),
        "recipient_sms_error": updated.get("recipient_sms_error"),
        "recipient_sms_sent_at": updated.get("recipient_sms_sent_at"),
        "delivery_sent": bool(updated.get("delivery_sent")),
        "delivery_sent_at": updated.get("delivery_sent_at"),
    }


@app.get("/admin/force-sender-sms/{order_id}")
def admin_force_sender_sms(order_id: str, token: str = "", reset: int = 0):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    if int(reset or 0) == 1:
        update_order(
            order_id,
            sender_sms_attempts=0,
            sender_sms_error=None,
            sender_sms_sent_at=None,
            sender_sms_sid=None,
            sender_notified=0,
        )
        insert_order_event(order_id, "admin_sender_sms_reset", "warning", "Intentos SMS regalante reseteados por admin")
    try:
        recover_reaction_from_chunks_if_possible(order_id, min_idle_seconds=0, source="admin_force_sender_sms")
    except Exception as e:
        print("[WARN] RC81 sender recovery before SMS skipped:", e)
    order = maybe_mark_eterna_completed(order_id)
    result = try_send_sender_sms(order)
    updated = get_order_by_id(order_id)
    return {
        "ok": bool(result.get("ok")),
        "result": result,
        "sender_sms_attempts": updated.get("sender_sms_attempts"),
        "sender_sms_error": updated.get("sender_sms_error"),
        "sender_sms_sent_at": updated.get("sender_sms_sent_at"),
        "sender_notified": bool(updated.get("sender_notified")),
    }



@app.get("/admin/rc81-version")
def admin_rc81_version(token: str = ""):
    if ADMIN_TOKEN and token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC82_PREEXPERIENCIA_CLEAN_SAFE",
        "sms_base_checked_against_salvavidas": True,
        "sms_core_changed": False,
        "admin_sms_delivery_check": True,
        "force_recipient_sms": True,
        "force_sender_sms": True,
        "sender_pack_asset": "sender_pack_master_v1.png",
        "sender_buttons": ["CREAR OTRA ETERNA", "COMPARTIR", "DESCARGAR"],
        "touches_critical_core": False,
    }



@app.get("/admin/rc82-version")
def admin_rc82_version(token: str = ""):
    if ADMIN_TOKEN and token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC82_PREEXPERIENCIA_CLEAN_SAFE",
        "rescue_hidden_normal_flow": True,
        "rescue_emergency_after_ms": 60000,
        "camera_guide_auto_continue_ms": 4000,
        "sms_core_kept": True,
        "sender_pack_master_v1": "sender_pack_master_v1.png",
        "touches_critical_core": False,
    }


# =========================================================
# START EXPERIENCE (FIX CRÍTICO)
# =========================================================



# =========================================================
# RUTAS CRÍTICAS RECUPERADAS DEL SALVAVIDAS
# Stripe webhook + callback video engine + resumen
# =========================================================

@app.post("/stripe/webhook")
@app.post("/stripe/webhook/")
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

    stripe_event_id = (event.get("id") or "").strip()
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

        # RC53 — idempotencia webhook Stripe: si Stripe reenvía el mismo evento, no relanzamos motor ni SMS.
        if stripe_event_id and (order.get("stripe_event_id") or "") == stripe_event_id and order.get("stripe_event_processed_at"):
            return {"status": "ok", "reason": "stripe_event_already_processed", "order_id": order_id}

        log_info("💳 PAGO RECIBIDO EN STRIPE")
        log_info("🆔 Order ID", order_id)
        log_info("👤 Regalante", f"{order.get('sender_name')} | {order.get('sender_email') or 'sin email'} | {order.get('sender_phone')}")
        log_info("🎯 Destinatario", f"{order.get('recipient_name')} | {order.get('recipient_phone')}")
        log_info("🎬 Estado", "voy a preparar el vídeo")
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
            stripe_event_id=stripe_event_id or order.get("stripe_event_id"),
            stripe_event_processed_at=now_iso() if stripe_event_id else order.get("stripe_event_processed_at"),
            order_state="PAID",
        )

        order = get_order_by_id(order_id)

        if original_video_ready(order):
            set_order_state(order_id, "VIDEO_READY", "stripe_webhook_video_already_ready")
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
            set_order_state(order_id, "RENDERING", "stripe_webhook_render_requested")
            data = trigger_video_engine(order_id, phrases)
            print("✅ Video engine aceptó el trabajo:", data)
        except Exception as e:
            clear_video_render_requested(order_id, error=str(e))
            log_error("webhook_video_engine_queued_for_recovery", e)
            return {
                "status": "ok",
                "reason": "video_engine_error_queued_for_recovery",
                "order_id": order_id,
                "error": str(e),
            }

        return {"status": "ok", "reason": "render_requested"}

    except Exception as e:
        log_error("webhook", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/internal/video-ready")
@app.post("/internal/video-ready/")
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
        insert_order_event(order_id, "video_ready", "ok", "El motor de vídeo avisó de que el vídeo está listo", {"video_url": video_url})

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

        permanent_video_url = preserve_remote_video_to_r2(order, video_url, kind="original")
        final_video_url = permanent_video_url or video_url

        update_order(
            order_id,
            experience_video_url=final_video_url,
            video_render_requested=0,
            render_status="RENDERED",
            order_state="RENDERED",
            render_last_error=None,
            recovery_last_checked_at=now_iso(),
        )
        insert_order_event(
            order_id,
            "RENDER_FINISHED",
            "ok",
            "Callback recibido y vídeo guardado como listo",
            {"video_url": final_video_url, "version": ETERNA_APP_VERSION},
        )

        video_url = final_video_url

        log_human("VÍDEO LISTO", f"🆔 Pedido: {order_id}", "✅ El vídeo ya está preparado", f"🔗 Link experiencia: {recipient_experience_url_from_order(order)}")
        log_info("✅ VÍDEO LISTO")
        log_info("🆔 Order ID", order_id)
        log_info("🎯 Destinatario", f"{order.get('recipient_name')} | {order.get('recipient_phone')}")
        log_info("🔗 Link experiencia", recipient_experience_url_from_order(order))
        log_info("🔗 Link regalante", sender_pack_url_from_order(order))

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

@app.get("/resumen/{order_id}", response_class=HTMLResponse)
def resumen(order_id: str):
    """Compatibilidad: se elimina la pantalla antigua de progreso post-pago."""
    try:
        get_order_by_id(order_id)
    except Exception:
        return render_eterna_image_screen(
            image_name="error-v1.png",
            fallback_image_name="error-v1.png",
            button_url="/crear",
            button_label="Volver a crear",
        )
    return RedirectResponse(url=f"/checkout-exito/{order_id}", status_code=303)


# =========================================================
# START EXPERIENCE (FIX CRÍTICO)
# =========================================================

@app.post("/start-experience")
async def start_experience(request: Request, recipient_token: str = Form(...)):
    try:
        order = get_order_by_recipient_token_or_404(recipient_token)
        insert_order_event(order["id"], "experience_started", "ok", "El destinatario ha pulsado empezar y se inicia cámara/vídeo")

        log_human("EXPERIENCIA INICIADA", f"🎭 {order.get('recipient_name')} ha pulsado Empezar", f"🆔 Pedido: {order.get('id')}")
        print("🎬 START EXPERIENCE:", order["id"])
        log_info("▶️ HA PULSADO EMPEZAR")
        log_info("🆔 Order ID", order["id"])
        log_info("🎯 Destinatario", f"{order.get('recipient_name')} | {order.get('recipient_phone')}")

        if not bool(order.get("paid")):
            raise HTTPException(status_code=403, detail="not_paid")

        if not original_video_ready(order):
            raise HTTPException(status_code=403, detail="video_not_ready")

        if not delivery_is_unlocked(order):
            raise HTTPException(status_code=403, detail="delivery_locked")

        update_order(
            order["id"],
            experience_started=1,
            order_state="EXPERIENCE_STARTED",
        )

        redirect_url = f"/experiencia/{recipient_token}"

        # Si Safari envía el formulario de forma normal porque algún JS falla,
        # NO debe quedarse en una página blanca con {"ok":true}.
        # En navegación HTML redirigimos directamente a la experiencia.
        ajax_header = (request.headers.get("x-eterna-ajax") or "").strip()
        # RC26: por defecto redirigimos. Solo devolvemos JSON si el JS lo pide explícitamente.
        # Así evitamos Safari en blanco con {"ok":true}.
        if ajax_header != "1":
            return RedirectResponse(url=redirect_url, status_code=303)

        return JSONResponse({
            "ok": True,
            "redirect_url": redirect_url
        })

    except Exception as e:
        log_error("START EXPERIENCE ERROR", e)
        raise HTTPException(status_code=500, detail="start_experience_failed")






# =========================================================
# RC48 — PANTALLAS POR CÓDIGO: TÉRMINOS + REGALO
# Objetivo:
# - Evitar zonas fantasma de PNG en aceptación de términos.
# - Crear pantalla de regalo/cobro con HTML/CSS real, sin depender de imagen.
# - NO toca Stripe, Twilio, webhooks, DB, video engine, reacción ni sender pack.
# =========================================================

def render_terms_code_screen(recipient_token: str) -> HTMLResponse:
    # RC50 - Terminos por codigo, legal ampliado y boton siempre visible.
    # No toca Stripe, Twilio, webhook, DB, video engine, reaccion, pagos ni sender pack.
    next_url = f"/guia/2/{safe_attr(recipient_token)}"
    return HTMLResponse(f'''
<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"><title>ETERNA - Terminos</title><meta name="theme-color" content="#02050a"><style>
*{{box-sizing:border-box;-webkit-tap-highlight-color:transparent}}html,body{{margin:0;width:100%;min-height:100%;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}}body{{min-height:100svh;min-height:100dvh;background:radial-gradient(circle at 78% 16%,rgba(26,159,255,.28),transparent 25%),radial-gradient(circle at 12% 82%,rgba(255,194,74,.16),transparent 28%),linear-gradient(180deg,#02050a 0%,#030914 54%,#02050a 100%);overflow:hidden}}.screen{{position:relative;width:100%;max-width:520px;height:100svh;height:100dvh;margin:0 auto;padding:calc(env(safe-area-inset-top) + 20px) 20px calc(env(safe-area-inset-bottom) + 18px);display:flex;flex-direction:column;overflow:hidden}}.scene{{position:absolute;inset:-18%;pointer-events:none;overflow:hidden;opacity:.96}}.scene:before{{content:"";position:absolute;inset:0;background:conic-gradient(from 218deg at 50% 49%,transparent,rgba(38,169,255,.18),transparent,rgba(255,201,90,.16),transparent);filter:blur(18px);animation:breath 8s ease-in-out infinite}}.scene:after{{content:"";position:absolute;right:-8%;top:8%;width:72%;height:58%;background:radial-gradient(ellipse at center,rgba(64,192,255,.22),transparent 58%);filter:blur(18px);animation:halo 5.8s ease-in-out infinite}}@keyframes breath{{0%,100%{{transform:scale(1);opacity:.55}}50%{{transform:scale(1.08);opacity:1}}}}@keyframes halo{{0%,100%{{opacity:.38;transform:scale(.96)}}50%{{opacity:.78;transform:scale(1.08)}}}}.spark{{position:absolute;border-radius:50%;background:#6bd7ff;box-shadow:0 0 18px #6bd7ff,0 0 34px rgba(66,189,255,.42);opacity:.82;animation:float 7.5s linear infinite;pointer-events:none}}.s1{{width:5px;height:5px;left:13%;top:17%}}.s2{{width:4px;height:4px;right:16%;top:31%;background:#ffd98b;box-shadow:0 0 18px #ffd98b;animation-delay:1.2s}}.s3{{width:6px;height:6px;left:18%;bottom:17%;animation-delay:2.1s}}.s4{{width:4px;height:4px;right:19%;bottom:23%;background:#ffd98b;box-shadow:0 0 18px #ffd98b;animation-delay:3.1s}}@keyframes float{{0%,100%{{transform:translateY(0);opacity:.30}}50%{{transform:translateY(-30px);opacity:1}}}}.logo{{position:relative;z-index:1;text-align:center;letter-spacing:.42em;color:#d8b76d;font-size:16px;font-weight:900;text-shadow:0 0 28px rgba(255,197,87,.35);margin:2px 0 10px}}.logo:after{{content:"♡";display:block;letter-spacing:0;font-size:18px;margin-top:8px;color:#f4c76e;text-shadow:0 0 22px rgba(255,193,76,.55)}}.content{{position:relative;z-index:1;display:flex;flex-direction:column;min-height:0;flex:1;text-align:center;gap:12px}}h1{{font-family:Georgia,"Times New Roman",serif;font-weight:500;font-size:clamp(34px,8.5vw,52px);line-height:1.04;margin:0;text-shadow:0 0 26px rgba(255,255,255,.15)}}h1 span{{color:#f4c76e;text-shadow:0 0 28px rgba(244,199,110,.28)}}.lead{{margin:0 auto;color:rgba(255,246,232,.78);font-size:15.5px;line-height:1.48;max-width:460px}}.legal-card{{margin-top:2px;border:1px solid rgba(255,207,112,.28);border-radius:24px;background:linear-gradient(180deg,rgba(255,255,255,.065),rgba(255,255,255,.025));box-shadow:0 22px 70px rgba(0,0,0,.42),inset 0 0 30px rgba(48,165,255,.06);overflow:hidden;text-align:left;flex:1;min-height:0}}.legal-scroll{{height:100%;overflow:auto;padding:2px 0;-webkit-overflow-scrolling:touch}}.row{{display:flex;align-items:center;gap:14px;padding:14px 16px;border-bottom:1px solid rgba(255,255,255,.075);text-decoration:none;color:#fff}}.row:last-child{{border-bottom:0}}.ico{{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1px solid rgba(255,205,110,.50);color:#f4c76e;font-size:20px;box-shadow:0 0 22px rgba(255,196,82,.12);flex:0 0 auto}}.row strong{{display:block;font-family:Georgia,"Times New Roman",serif;font-weight:500;font-size:19px;margin-bottom:3px}}.row small{{display:block;color:rgba(255,246,232,.62);font-size:13px;line-height:1.34}}.chev{{margin-left:auto;color:#f4c76e;font-size:26px}}.mini-legal{{padding:12px 16px 14px;color:rgba(255,246,232,.70);font-size:12.6px;line-height:1.45;border-top:1px solid rgba(255,255,255,.06)}}.mini-legal b{{color:#f4c76e;font-weight:800}}.actions{{position:relative;z-index:2;display:grid;gap:10px;padding-top:4px;flex:0 0 auto}}.accept{{display:flex;align-items:center;gap:12px;padding:13px 14px;border-radius:20px;border:1px solid rgba(255,207,112,.34);background:rgba(0,0,0,.46);box-shadow:inset 0 0 24px rgba(255,201,99,.05);text-align:left;cursor:pointer;min-height:62px}}.accept input{{position:absolute;opacity:0;pointer-events:none}}.box{{width:34px;height:34px;border-radius:10px;border:2px solid rgba(255,223,151,.86);display:flex;align-items:center;justify-content:center;color:#080603;font-weight:950;flex:0 0 auto;box-shadow:0 0 18px rgba(255,202,91,.24)}}.accept input:checked + .box{{background:linear-gradient(135deg,#fff2bf,#d5942e);box-shadow:0 0 28px rgba(255,198,77,.72)}}.accept input:checked + .box:before{{content:"✓"}}.accept span:last-child{{font-size:15px;color:rgba(255,246,232,.84);line-height:1.32}}.btn{{width:100%;min-height:62px;border:0;border-radius:22px;background:linear-gradient(135deg,#fff0bb,#e4a23d 52%,#9b5e08);color:#120c04;font-family:Georgia,"Times New Roman",serif;font-size:25px;box-shadow:0 0 34px rgba(255,190,72,.34),inset 0 0 24px rgba(255,255,255,.20);opacity:.42;transform:scale(.992);transition:all .18s ease;cursor:not-allowed}}.btn.ready{{opacity:1;transform:scale(1);cursor:pointer}}.warn{{display:none;color:#ffd98b;font-size:12px;line-height:1.35;text-align:center;margin-top:-2px}}.warn.on{{display:block}}.note{{color:rgba(255,246,232,.42);font-size:11.4px;line-height:1.35;text-align:center;margin-top:-2px}}@media (max-height:760px){{.screen{{padding-top:12px;padding-bottom:10px}}.logo{{font-size:13px;margin-bottom:5px}}.logo:after{{font-size:15px;margin-top:5px}}h1{{font-size:34px}}.lead{{font-size:13.5px;line-height:1.35}}.row{{padding:10px 14px}}.ico{{width:36px;height:36px;font-size:17px}}.row strong{{font-size:17px}}.row small{{font-size:12px}}.mini-legal{{font-size:11.2px;line-height:1.35;padding:9px 14px}}.accept{{min-height:54px;padding:10px 12px}}.btn{{min-height:56px;font-size:22px}}}}
</style></head><body><main class="screen"><div class="scene" aria-hidden="true"></div><i class="spark s1"></i><i class="spark s2"></i><i class="spark s3"></i><i class="spark s4"></i><div class="logo">ETERNA</div><section class="content"><h1>Acepta los <span>términos</span></h1><p class="lead">Antes de continuar, lee y acepta las condiciones para vivir esta experiencia de forma privada, respetuosa y segura.</p><div class="legal-card"><div class="legal-scroll"><a class="row" href="/condiciones" target="_blank" rel="noopener"><div class="ico">▤</div><div><strong>Términos y condiciones</strong><small>Lo esencial para vivir la experiencia con respeto.</small></div><div class="chev">›</div></a><a class="row" href="/privacidad" target="_blank" rel="noopener"><div class="ico">◈</div><div><strong>Privacidad</strong><small>Tu experiencia es personal y privada.</small></div><div class="chev">›</div></a><div class="mini-legal">Al continuar aceptas vivir esta experiencia de forma privada y respetuosa. El navegador podrá pedir cámara y micrófono para que el momento pueda conservarse y enviarse de forma privada a quien lo creó.<br><br><b>Uso responsable:</b> este recuerdo es personal. Trátalo con respeto y no lo compartas públicamente sin consentimiento.</div></div></div><div class="actions"><label class="accept"><input id="termsCheck" type="checkbox"><span class="box"></span><span>He leído y acepto los términos y la política de privacidad.</span></label><div id="termsWarn" class="warn">Marca la casilla para continuar.</div><button id="continueBtn" class="btn" type="button">Aceptar y continuar</button><div class="note"></div></div></section></main><script>(function(){{const check=document.getElementById('termsCheck');const btn=document.getElementById('continueBtn');const warn=document.getElementById('termsWarn');function sync(){{btn.classList.toggle('ready',check.checked);if(check.checked&&warn)warn.classList.remove('on');}}check.addEventListener('change',sync);btn.addEventListener('click',function(){{if(!check.checked){{if(warn)warn.classList.add('on');return;}}window.location.href={json.dumps(next_url)};}});sync();}})();</script></body></html>
''')

def render_gift_code_screen(recipient_token: str, amount_text: str, cta_html: str) -> HTMLResponse:
    """
    RC53 — pantalla recipient-gift-screen-v3 como fondo definitivo.
    Los botones y el importe siguen siendo HTML real encima: no dependen del PNG.
    """
    bg = eterna_asset("recipient_gift")
    return HTMLResponse(f'''
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>ETERNA</title>
<meta name="theme-color" content="#02050a">
<style>
*{{box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
html,body{{margin:0;width:100%;min-height:100%;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}}
body{{min-height:100svh;min-height:100dvh;overflow:hidden;display:flex;align-items:center;justify-content:center;background:#02050a}}
.shell{{position:relative;width:100vw;max-width:520px;height:100svh;height:100dvh;overflow:hidden;background:#02050a}}
.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center top;z-index:0;user-select:none;pointer-events:none}}
.amount{{position:absolute;z-index:3;left:18%;right:18%;top:45.8%;min-height:9.4%;border-radius:22px;display:flex;align-items:center;justify-content:center;text-align:center;padding:10px 14px;color:#ffe0a0;font-size:clamp(20px,6vw,33px);font-weight:950;line-height:1.15;text-shadow:0 0 18px rgba(255,196,72,.58);background:rgba(0,0,0,.18);border:1px solid rgba(255,212,126,.22);box-shadow:0 0 28px rgba(255,190,72,.18),inset 0 0 20px rgba(0,0,0,.28)}}
.actions{{position:absolute;z-index:4;left:8.2%;right:8.2%;bottom:calc(env(safe-area-inset-bottom) + 7.0%);display:grid;gap:1.15vh}}
.actions form{{margin:0}}
.btn,.actions form button{{width:100%;min-height:6.9svh;border-radius:18px;display:flex;align-items:center;justify-content:center;text-align:center;text-decoration:none;text-transform:uppercase;letter-spacing:.06em;font-weight:950;font-size:clamp(13px,3.6vw,18px);border:1px solid rgba(255,213,130,.42);background:rgba(0,7,15,.64);color:#fff2d6;box-shadow:0 14px 34px rgba(0,0,0,.34),0 0 22px rgba(255,189,75,.12);backdrop-filter:blur(6px)}}
.btn.primary,.actions form button{{background:linear-gradient(135deg,#fff1bb,#e6a43c 52%,#9c5d08);color:#120a02;border:0;box-shadow:0 0 34px rgba(255,190,72,.42),inset 0 0 18px rgba(255,255,255,.22)}}
.blue{{border-color:rgba(49,185,255,.45);box-shadow:0 0 28px rgba(43,175,255,.25),0 14px 34px rgba(0,0,0,.34)}}
.small{{position:absolute;z-index:3;left:7%;right:7%;bottom:calc(env(safe-area-inset-bottom) + 1.8%);text-align:center;color:rgba(255,246,232,.58);font-size:12px;line-height:1.35;text-shadow:0 0 14px rgba(0,0,0,.9)}}
.glow{{position:absolute;z-index:1;inset:-10%;pointer-events:none;mix-blend-mode:screen;background:radial-gradient(circle at 50% 37%,rgba(51,196,255,.18),transparent 24%),radial-gradient(circle at 50% 58%,rgba(255,196,73,.17),transparent 20%);animation:breath 5.6s ease-in-out infinite}}
@keyframes breath{{0%,100%{{opacity:.45;transform:scale(1)}}50%{{opacity:.92;transform:scale(1.04)}}}}
@media (min-width:760px){{.shell{{width:min(100vw,520px)}}}}

    /* =========================================================
       RC71 PRE-EXPERIENCE MAGIC SAFE
       Solo atmósfera viva para: intro, sonido, lugar tranquilo y consentimiento.
       No cambia rutas, botones, formularios, Stripe, Twilio, DB, reacción ni sender pack.
       ========================================================= */
    .pre-magic {{
        position:absolute;
        inset:0;
        z-index:4;
        pointer-events:none;
        display:none;
        overflow:hidden;
        opacity:1;
        contain:paint;
    }}
    .screen.intro-mode .pre-magic,
    .screen.sound-mode .pre-magic,
    .screen.quiet-mode .pre-magic,
    .screen.consent-mode .pre-magic {{
        display:block;
    }}
    .pre-depth {{
        position:absolute;
        inset:-8%;
        opacity:.62;
        mix-blend-mode:screen;
        background:
            radial-gradient(circle at 18% 18%, rgba(55,207,255,.16), transparent 24%),
            radial-gradient(circle at 80% 26%, rgba(255,211,121,.12), transparent 25%),
            radial-gradient(circle at 51% 72%, rgba(72,198,255,.10), transparent 31%),
            linear-gradient(180deg, rgba(2,5,10,.08), transparent 38%, rgba(2,5,10,.20));
        filter:blur(1px);
        animation:rc71DepthBreath 9.8s ease-in-out infinite;
    }}
    .pre-fog {{
        position:absolute;
        left:-32%;
        right:-32%;
        height:44%;
        border-radius:999px;
        opacity:.0;
        filter:blur(23px);
        mix-blend-mode:screen;
        background:linear-gradient(90deg, transparent, rgba(93,211,255,.12), rgba(255,221,144,.08), rgba(93,211,255,.11), transparent);
        animation:rc71FogDrift 18s ease-in-out infinite;
    }}
    .pre-fog.fog-a {{ top:15%; animation-delay:.2s; }}
    .pre-fog.fog-b {{ bottom:8%; opacity:.0; animation-duration:22s; animation-delay:4.2s; transform:scaleY(.72); }}
    .pre-spark {{
        position:absolute;
        width:4px;
        height:4px;
        border-radius:999px;
        opacity:0;
        background:rgba(117,221,255,.96);
        box-shadow:0 0 13px rgba(117,221,255,.95), 0 0 28px rgba(117,221,255,.36);
        animation:rc71SparkRise 10.5s linear infinite;
    }}
    .pre-spark.gold {{
        background:rgba(255,221,145,.95);
        box-shadow:0 0 13px rgba(255,221,145,.90), 0 0 28px rgba(255,196,74,.34);
    }}
    .ps1 {{ left:13%; bottom:11%; animation-delay:.1s; animation-duration:11.8s; transform:scale(.75); }}
    .ps2 {{ left:28%; bottom:25%; animation-delay:2.8s; animation-duration:13.2s; transform:scale(.55); }}
    .ps3 {{ left:47%; bottom:10%; animation-delay:1.4s; animation-duration:12.6s; transform:scale(.68); }}
    .ps4 {{ left:69%; bottom:19%; animation-delay:4.1s; animation-duration:14.4s; transform:scale(.5); }}
    .ps5 {{ left:83%; bottom:33%; animation-delay:6.0s; animation-duration:12.8s; transform:scale(.62); }}
    .ps6 {{ left:56%; bottom:46%; animation-delay:7.2s; animation-duration:15.2s; transform:scale(.45); }}
    .pre-glint {{
        position:absolute;
        width:92px;
        height:2px;
        border-radius:999px;
        opacity:0;
        mix-blend-mode:screen;
        background:linear-gradient(90deg, transparent, rgba(255,255,255,.88), rgba(255,220,135,.70), transparent);
        box-shadow:0 0 18px rgba(255,227,155,.52), 0 0 35px rgba(84,211,255,.20);
        animation:rc71GlintCross 7.6s ease-in-out infinite;
    }}
    .glint-a {{ left:4%; top:31%; animation-delay:2.1s; }}
    .glint-b {{ right:-2%; bottom:27%; animation-delay:5.4s; animation-direction:reverse; }}
    .yul-live {{
        position:absolute;
        width:74px;
        height:auto;
        left:66%;
        top:22%;
        opacity:0;
        z-index:5;
        pointer-events:none;
        transform-origin:center center;
        filter:drop-shadow(0 0 14px rgba(92,216,255,.65)) drop-shadow(0 0 22px rgba(255,214,124,.30));
        mix-blend-mode:screen;
        animation:rc71YulAlive 13.5s cubic-bezier(.45,0,.25,1) infinite;
    }}
    .yul-trail {{
        position:absolute;
        left:66%;
        top:22%;
        width:120px;
        height:32px;
        border-radius:999px;
        z-index:4;
        opacity:0;
        pointer-events:none;
        mix-blend-mode:screen;
        background:radial-gradient(circle at 20% 50%, rgba(255,222,142,.38), transparent 18%), radial-gradient(circle at 48% 48%, rgba(99,219,255,.28), transparent 21%), linear-gradient(90deg, rgba(255,219,130,.00), rgba(255,219,130,.20), rgba(83,211,255,.14), transparent);
        filter:blur(7px);
        animation:rc71YulTrail 13.5s cubic-bezier(.45,0,.25,1) infinite;
    }}
    .screen.sound-mode .yul-live,
    .screen.sound-mode .yul-trail {{ top:19%; left:71%; animation-delay:1.6s; animation-duration:15s; }}
    .screen.quiet-mode .yul-live,
    .screen.quiet-mode .yul-trail {{ top:24%; left:18%; animation-delay:2.4s; animation-duration:16.5s; }}
    .screen.consent-mode .yul-live,
    .screen.consent-mode .yul-trail {{ top:18%; left:70%; animation-delay:3.2s; animation-duration:17s; opacity:0; }}
    .screen.consent-mode .pre-magic {{ opacity:.72; }}
    .screen.consent-mode .pre-spark {{ animation-duration:14.8s; }}
    .screen.quiet-mode .pre-fog {{ opacity:.0; filter:blur(27px); }}
    .screen.quiet-mode .pre-depth {{ opacity:.75; }}

    @keyframes rc71DepthBreath {{
        0%,100% {{ transform:scale(1) translate3d(0,0,0); opacity:.42; }}
        45% {{ transform:scale(1.045) translate3d(-1.8%,1.2%,0); opacity:.74; }}
        72% {{ opacity:.55; }}
    }}
    @keyframes rc71FogDrift {{
        0% {{ transform:translateX(-14%) translateY(10px) scaleX(.92); opacity:0; }}
        18% {{ opacity:.40; }}
        54% {{ opacity:.30; }}
        100% {{ transform:translateX(14%) translateY(-12px) scaleX(1.08); opacity:0; }}
    }}
    @keyframes rc71SparkRise {{
        0% {{ opacity:0; transform:translate3d(0,0,0) scale(.42); }}
        12% {{ opacity:.78; }}
        58% {{ opacity:.42; transform:translate3d(18px,-88px,0) scale(.82); }}
        100% {{ opacity:0; transform:translate3d(34px,-178px,0) scale(1.05); }}
    }}
    @keyframes rc71GlintCross {{
        0%,68% {{ opacity:0; transform:translateX(-80px) translateY(14px) rotate(-9deg) scaleX(.45); }}
        75% {{ opacity:.76; }}
        100% {{ opacity:0; transform:translateX(330px) translateY(-24px) rotate(-9deg) scaleX(1.15); }}
    }}
    @keyframes rc71YulAlive {{
        0% {{ opacity:0; transform:translate3d(-18px,12px,0) rotate(-7deg) scale(.78) skewX(0deg); }}
        10% {{ opacity:.0; }}
        18% {{ opacity:.82; transform:translate3d(0,0,0) rotate(-2deg) scale(.92) skewX(2deg); }}
        30% {{ transform:translate3d(-9px,-12px,0) rotate(4deg) scale(.98) skewX(-3deg); }}
        42% {{ transform:translate3d(7px,-4px,0) rotate(-3deg) scale(.94) skewX(3deg); }}
        55% {{ opacity:.76; transform:translate3d(-4px,10px,0) rotate(3deg) scale(.99) skewX(-2deg); }}
        68% {{ transform:translate3d(12px,-8px,0) rotate(-4deg) scale(.93) skewX(2deg); }}
        80% {{ opacity:.58; transform:translate3d(22px,4px,0) rotate(2deg) scale(.86) skewX(-1deg); }}
        100% {{ opacity:0; transform:translate3d(44px,-18px,0) rotate(8deg) scale(.72) skewX(0deg); }}
    }}
    @keyframes rc71YulTrail {{
        0%,12% {{ opacity:0; transform:translate3d(-40px,20px,0) rotate(-8deg) scale(.72); }}
        24% {{ opacity:.34; }}
        52% {{ opacity:.22; transform:translate3d(-28px,2px,0) rotate(-4deg) scale(.95); }}
        78% {{ opacity:.14; }}
        100% {{ opacity:0; transform:translate3d(14px,-12px,0) rotate(7deg) scale(.82); }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        .screen.intro-mode .pre-magic,
        .screen.sound-mode .pre-magic,
        .screen.quiet-mode .pre-magic,
        .screen.consent-mode .pre-magic {{
            opacity:.42;
        }}
        .pre-depth,
        .pre-fog,
        .pre-spark,
        .pre-glint,
        .yul-live,
        .yul-trail {{
            animation:none !important;
        }}
        .yul-live {{ opacity:.32; }}
    }}

</style>
</head>
<body>
<main class="shell">
  <img class="bg" src="{safe_attr(bg)}" alt="Tu ETERNA aún no ha terminado">
  <div class="glow" aria-hidden="true"></div>
  <div class="amount">{safe_text(amount_text)}</div>
  <nav class="actions">
    {cta_html}
    <a class="btn blue" href="/mi-video/{safe_attr(recipient_token)}">Volver a ver mi ETERNA</a>
    <a class="btn" href="/crear">Crear mi ETERNA</a>
  </nav>
  <div class="small">Privado y seguro · Un gesto que permanece</div>
</main>
</body>
</html>
''')


# =========================================================
# RC63 — PRÓLOGO CINEMATOGRÁFICO ETERNA
# Sustituye las pantallas frías previas al vídeo por una sola experiencia narrativa.
# NO toca Stripe, Twilio, webhooks, DB, Video Engine, reacción, cobros ni sender pack.
# =========================================================


# =========================================================
# RC78 — YUL LUGAR ÚNICO / FRASES GENÉRICAS ROMÁNTICAS
# =========================================================

def rc78_yul_place_lines(place: str) -> str:
    clean_place = rc75_clean_emotional_text(place, 140) if "rc75_clean_emotional_text" in globals() else str(place or "").strip()[:140]
    if not clean_place:
        return ""

    safe_place = safe_text(clean_place)
    lines = [
        f'<div class="line small l-place-found">Espera...<br><span class="gold">creo que he encontrado algo.</span></div>',
        f'<div class="line big l-place-name"><span class="gold">{safe_place}</span></div>',
        '<div class="line small l-place-meaning">No sé qué ocurrió allí.<br><span class="gold">Pero alguien decidió guardar este lugar.</span></div>',
        '<div class="line small l-place-heart">Y eso suele significar algo.</div>',
    ]
    return "".join(lines)



# =========================================================
# RC82 — PREEXPERIENCIA CLEAN PATCH
# =========================================================

def rc82_preexperience_clean_patch(html_doc: str) -> str:
    try:
        css = """
<style id="rc82-preexperience-clean">
#yulRescuePanel,#yulSafeNote{display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important}
#yulRescuePanel.is-emergency{display:flex!important;visibility:visible!important;opacity:1!important;pointer-events:auto!important}
#yulSafeNote.is-emergency{display:block!important;visibility:visible!important;opacity:1!important}
.yul-line,.yul-text,.yul-story-line,.scene-text,.magic-text{text-wrap:balance}
</style>
"""
        js = """
<script id="rc82-preexperience-clean-js">
(function(){
  function hideRescue(){
    var p=document.getElementById("yulRescuePanel");
    var n=document.getElementById("yulSafeNote");
    if(p){p.classList.remove("is-visible");p.classList.remove("is-emergency");p.style.display="none";p.style.visibility="hidden";p.style.opacity="0";}
    if(n){n.classList.remove("is-visible");n.classList.remove("is-emergency");n.style.display="none";n.style.visibility="hidden";n.style.opacity="0";}
  }
  function emergencyRescue(){
    var p=document.getElementById("yulRescuePanel");
    var n=document.getElementById("yulSafeNote");
    if(p){p.classList.add("is-emergency");p.style.display="flex";p.style.visibility="visible";p.style.opacity="1";}
    if(n){n.classList.add("is-emergency");n.style.display="block";n.style.visibility="visible";n.style.opacity="1";}
  }
  window.__YUL_SHOW_RESCUE__=emergencyRescue;
  window.__YUL_HIDE_RESCUE__=hideRescue;
  if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded", hideRescue);} else {hideRescue();}
  setTimeout(hideRescue,250);setTimeout(hideRescue,1000);setTimeout(hideRescue,2500);
  setTimeout(function(){ if(location.pathname.indexOf("/guia/")>=0){ emergencyRescue(); } },60000);

  // Cámara / colocación: 4 segundos y avanza.
  setTimeout(function(){
    try{
      var body=(document.body&&document.body.innerText||"").toLowerCase();
      var hasCamera=document.querySelector("video,#cameraPreview,.camera-preview,.guide-camera,.webcam-preview");
      if(location.pathname.indexOf("/guia/")>=0 && (hasCamera || body.includes("rostro") || body.includes("así te verá"))){
        if(typeof window.__YUL_SOFT_ADVANCE__==="function"){window.__YUL_SOFT_ADVANCE__("camera_4s");return;}
        if(typeof window.nextYulScene==="function"){window.nextYulScene("camera_4s");return;}
        if(typeof window.advanceScene==="function"){window.advanceScene("camera_4s");return;}
        var btn=Array.from(document.querySelectorAll("button,a")).find(function(el){
          var t=(el.textContent||"").toLowerCase();
          return t.includes("continuar")||t.includes("listo");
        });
        if(btn) btn.click();
      }
    }catch(e){}
  },4000);
})();
</script>
"""
        if "rc82-preexperience-clean" not in html_doc:
            html_doc = html_doc.replace("</head>", css + "</head>", 1) if "</head>" in html_doc else css + html_doc
        if "rc82-preexperience-clean-js" not in html_doc:
            html_doc = html_doc.replace("</body>", js + "</body>", 1) if "</body>" in html_doc else html_doc + js
    except Exception as e:
        print("[WARN] RC82 preexperience clean patch skipped:", e)
    return html_doc


def render_eterna_prologo_experience(recipient_token: str) -> HTMLResponse:
    """
    RC82_PREEXPERIENCIA_CLEAN_SAFE.
    Sustituye únicamente la pre-experiencia /guia por EL UMBRAL.
    No toca Stripe, Twilio, webhooks, DB crítica, video engine, reaction upload,
    sender pack, cola RC74 ni recovery worker.
    """
    recipient_token_safe = safe_attr(recipient_token)
    recipient_token_json = json.dumps(str(recipient_token))

    try:
        order = get_order_by_recipient_token_or_404(recipient_token)
        yul_context = rc75_yul_context_from_order(order)
        yul_place_story_line = rc78_yul_place_lines(yul_context.get("memory_place", ""))
    except Exception:
        yul_context = {"memory_place": "", "memory_detail": "", "emotion_tone": "", "magic_hint": ""}
        yul_place_story_line = ""

    yul_place_line = ""
    yul_detail_line = ""
    yul_emotion_line = ""
    yul_hint_line = ""
    bridge_memory_line = ""
    bridge_hint_line = ""

    if yul_context.get("memory_place"):
        place = safe_text(yul_context.get("memory_place"))
        yul_place_line = f'<div class="line small l-extra-place">Antes de llegar a ti, Yul encontró un lugar:<br><span class="gold">{place}</span></div>'
        bridge_memory_line = f'<p>Hay una pista escondida: <span>{place}</span>.</p>'

    if yul_context.get("memory_detail"):
        detail = safe_text(yul_context.get("memory_detail"))
        yul_detail_line = f'<div class="line small l-extra-detail">Hay un recuerdo pequeño intentando volver:<br><span class="gold">{detail}</span></div>'

    if yul_context.get("emotion_tone"):
        tone = safe_text(yul_context.get("emotion_tone"))
        yul_emotion_line = f'<div class="line small l-extra-emotion">Esta historia viene buscando una emoción:<br><span class="gold">{tone}</span></div>'

    if yul_context.get("magic_hint"):
        hint_txt = safe_text(yul_context.get("magic_hint"))
        yul_hint_line = f'<div class="line small l-extra-hint">Yul encontró una pista secreta:<br><span class="gold">{hint_txt}</span></div>'
        bridge_hint_line = f'<p class="bridge-secret">Y antes de cruzar, Yul susurra: <span>{hint_txt}</span></p>'

    html_doc = '\n<!DOCTYPE html>\n<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"><title>ETERNA - El Umbral</title><meta name="theme-color" content="#02050a"><style>\n*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}html,body{margin:0;width:100%;min-height:100%;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}body{min-height:100svh;min-height:100dvh;overflow:hidden;background:#02050a}.umbral{position:relative;width:100vw;height:100svh;height:100dvh;overflow:hidden;background:#02050a;display:flex;align-items:center;justify-content:center}.stage{position:relative;width:100vw;height:100svh;height:100dvh;max-width:520px;overflow:hidden;background:radial-gradient(circle at 50% 78%,rgba(5,56,92,.60),transparent 31%),radial-gradient(circle at 16% 16%,rgba(44,180,255,.10),transparent 24%),linear-gradient(180deg,#000 0%,#020713 46%,#030d18 100%)}.stage:before{content:"";position:absolute;inset:-18%;background:conic-gradient(from 220deg at 50% 50%,transparent,rgba(48,179,255,.16),transparent,rgba(255,197,96,.10),transparent);filter:blur(18px);opacity:.64;animation:breathWorld 16s ease-in-out infinite;pointer-events:none}.stage:after{content:"";position:absolute;inset:0;background-image:radial-gradient(circle,rgba(255,255,255,.44) 0 1px,transparent 1.4px),radial-gradient(circle,rgba(66,213,255,.70) 0 1px,transparent 1.5px),radial-gradient(circle,rgba(255,211,123,.48) 0 1px,transparent 1.5px);background-size:97px 131px,137px 191px,191px 251px;opacity:.46;animation:starDrift 42s linear infinite;pointer-events:none}.brand{position:absolute;z-index:20;top:calc(env(safe-area-inset-top) + 22px);left:0;right:0;text-align:center;letter-spacing:.46em;font-family:Georgia,"Times New Roman",serif;font-size:clamp(17px,5.3vw,28px);color:#eec36a;text-shadow:0 0 22px rgba(255,200,93,.52);opacity:.80}.brand:after{content:"♡";display:block;letter-spacing:0;margin-top:7px;font-size:19px;color:#ffd477;text-shadow:0 0 22px rgba(255,204,90,.72)}.yul{position:absolute;z-index:18;left:50%;top:50%;width:18px;height:18px;border-radius:999px;background:radial-gradient(circle,#fff 0 16%,#9ee9ff 18% 32%,#265cff 36% 54%,rgba(76,0,255,.32) 65%,transparent 76%);box-shadow:0 0 18px rgba(255,255,255,.95),0 0 42px rgba(81,214,255,.86),0 0 82px rgba(40,86,255,.54),0 0 118px rgba(89,0,255,.32);filter:saturate(1.25);opacity:0;transform:translate(-50%,-50%);animation:yulLife 88s cubic-bezier(.18,.76,.15,1) forwards;pointer-events:none}.yul:before{content:"";position:absolute;left:-118px;top:7px;width:135px;height:4px;border-radius:999px;background:linear-gradient(90deg,transparent,rgba(76,0,255,.05),rgba(60,192,255,.60),rgba(255,255,255,.92));filter:blur(.4px);transform-origin:100% 50%;opacity:.74;animation:yulTail 88s cubic-bezier(.18,.76,.15,1) forwards}.yul:after{content:"";position:absolute;inset:-26px;border-radius:999px;background:radial-gradient(circle,rgba(87,214,255,.30),rgba(58,97,255,.14) 40%,transparent 68%);filter:blur(8px);animation:yulAura 2.1s ease-in-out infinite;opacity:.9}.spark{position:absolute;z-index:13;width:4px;height:4px;border-radius:999px;background:#69d9ff;box-shadow:0 0 14px #69d9ff,0 0 28px rgba(105,217,255,.42);opacity:0;animation:sparkRise 9s linear infinite;pointer-events:none}.spark.gold{background:#ffd782;box-shadow:0 0 14px #ffd782,0 0 28px rgba(255,215,130,.42)}.s1{left:14%;bottom:16%;animation-delay:2s}.s2{right:18%;bottom:21%;animation-delay:4s}.s3{left:26%;top:28%;animation-delay:7s}.s4{right:27%;top:35%;animation-delay:11s}.s5{left:48%;bottom:10%;animation-delay:15s}.s6{right:10%;top:16%;animation-delay:19s}.copy{position:absolute;z-index:22;left:7%;right:7%;top:49%;transform:translateY(-50%);text-align:center;pointer-events:none}.line{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);opacity:0;font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:clamp(27px,8.2vw,46px);line-height:1.12;letter-spacing:.005em;color:#fff6e8;text-shadow:0 0 20px rgba(255,255,255,.22),0 0 44px rgba(57,194,255,.22);animation:lineReveal 5.4s ease-in-out forwards}.line.small{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;font-size:clamp(17px,4.9vw,25px);line-height:1.42;color:#f8ebd8}.line.gold,.gold{color:#f4c46c;text-shadow:0 0 24px rgba(255,199,92,.56),0 0 54px rgba(255,166,41,.20)}.line.whisper{font-size:clamp(38px,14vw,76px);letter-spacing:.03em}.l1{animation-delay:3s}.l2{animation-delay:8.8s}.l3{animation-delay:14.5s}.l4{animation-delay:20.2s}.l5{animation-delay:26.2s}.l6{animation-delay:32.4s}.l7{animation-delay:38.5s}.l8{animation-delay:44.6s}.l9{animation-delay:50.5s}.l10{animation-delay:56.2s}.l11{animation-delay:62.2s}.l12{animation-delay:68.4s}.l13{animation-delay:74s}.l14{animation-delay:80s}.l15{animation-delay:86s}.consent-card,.camera-card,.bridge-card{position:absolute;z-index:40;left:6.3%;right:6.3%;top:50%;transform:translateY(-50%) scale(.96);opacity:0;pointer-events:none;padding:25px 20px 22px;border:1px solid rgba(255,215,136,.44);border-radius:28px;background:linear-gradient(180deg,rgba(2,9,20,.88),rgba(1,4,11,.78));box-shadow:0 0 46px rgba(36,171,255,.20),0 0 78px rgba(255,191,83,.13),inset 0 0 28px rgba(255,255,255,.045);backdrop-filter:blur(12px);transition:opacity .9s ease,transform .9s ease}.umbral.consent-phase .consent-card{opacity:1;transform:translateY(-50%) scale(1);pointer-events:auto}.umbral.camera-phase .camera-card{opacity:1;transform:translateY(-50%) scale(1);pointer-events:auto}.umbral.bridge-phase .bridge-card{opacity:1;transform:translateY(-50%) scale(1);pointer-events:auto}.consent-card h1,.camera-card h1,.bridge-card h1{font-family:Georgia,"Times New Roman",serif;margin:0 0 14px;text-align:center;font-size:clamp(29px,8.2vw,44px);font-weight:400;color:#fff5e5;line-height:1.05}.consent-card h1 span,.camera-card h1 span,.bridge-card h1 span{color:#f4c46c}.consent-card p,.camera-card p,.bridge-card p{margin:11px 0;font-size:clamp(15px,4.15vw,19px);line-height:1.42;text-align:center;color:#f6ead6;text-shadow:0 0 16px rgba(0,0,0,.8)}.bridge-card span{color:#f4c46c;text-shadow:0 0 22px rgba(255,199,92,.42)}.bridge-secret{margin-top:16px;padding:13px;border-radius:18px;border:1px solid rgba(255,215,136,.22);background:rgba(0,0,0,.24)}.legal-box{margin:15px 0;padding:14px 13px;border-radius:18px;border:1px solid rgba(255,215,136,.26);background:rgba(0,0,0,.24);font-weight:600}.check-row{margin-top:16px;display:flex;align-items:center;gap:12px;padding:14px;border-radius:18px;border:1px solid rgba(255,218,143,.36);background:rgba(0,0,0,.24);text-align:left;color:#fff7e9;font-size:clamp(14px,3.9vw,17px);line-height:1.25}.check-row input{appearance:none;width:33px;height:33px;min-width:33px;border-radius:9px;border:2px solid rgba(255,235,184,.88);background:rgba(0,0,0,.4);box-shadow:0 0 18px rgba(255,213,118,.20);position:relative}.check-row input:checked{background:linear-gradient(135deg,#fff1bb,#e6a43c 58%,#8e5307);box-shadow:0 0 26px rgba(255,196,79,.72)}.check-row input:checked:after{content:"";position:absolute;left:9px;top:3px;width:10px;height:19px;border:solid #120900;border-width:0 4px 4px 0;transform:rotate(45deg)}.consent-btn,.camera-btn,.final-btn{width:100%;border:0;border-radius:24px;margin-top:18px;min-height:66px;background:linear-gradient(135deg,#fff1bb,#e6a43c 54%,#9c5d08);color:#150b02;font-family:Georgia,"Times New Roman",serif;font-size:clamp(21px,6.2vw,31px);box-shadow:0 0 34px rgba(255,190,72,.43),inset 0 0 18px rgba(255,255,255,.22);cursor:pointer}.consent-btn:disabled,.camera-btn:disabled,.final-btn:disabled{filter:saturate(.45) brightness(.65);cursor:not-allowed}.preview-wrap{position:relative;width:100%;aspect-ratio:9/13;border-radius:24px;overflow:hidden;background:#03070e;border:1px solid rgba(255,215,136,.30);box-shadow:0 0 34px rgba(54,199,255,.18),inset 0 0 28px rgba(255,255,255,.04);margin:14px 0}.preview-wrap video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scaleX(-1);filter:saturate(1.04) contrast(1.03) brightness(1.03)}.face-guide{position:absolute;left:50%;top:42%;width:54%;height:37%;transform:translate(-50%,-50%);border-radius:45% 45% 42% 42%;border:1px solid rgba(255,220,143,.48);box-shadow:0 0 24px rgba(255,210,104,.22),inset 0 0 18px rgba(74,210,255,.10);opacity:.76;pointer-events:none}.horizon{position:absolute;left:16%;right:16%;top:42%;height:1px;background:linear-gradient(90deg,transparent,rgba(255,230,171,.66),transparent);box-shadow:0 0 14px rgba(255,219,142,.45);pointer-events:none}.camera-hint{position:absolute;left:8%;right:8%;bottom:10px;text-align:center;padding:10px 12px;border-radius:16px;background:rgba(0,0,0,.46);font-size:13px;color:#fff0d1;line-height:1.25;backdrop-filter:blur(8px)}.final-gate{position:absolute;z-index:45;left:7%;right:7%;bottom:calc(env(safe-area-inset-bottom) + 7%);opacity:0;transform:translateY(24px);pointer-events:none;transition:opacity 1.1s ease,transform 1.1s ease}.umbral.ready-phase .final-gate{opacity:1;transform:translateY(0);pointer-events:auto}.final-btn{min-height:78px;text-transform:uppercase;letter-spacing:.055em;font-weight:900}.final-note{margin-top:13px;text-align:center;color:rgba(255,243,220,.72);font-size:13px;line-height:1.35}.safe-note{position:absolute;z-index:55;left:0;right:0;bottom:calc(env(safe-area-inset-bottom) + 10px);text-align:center;color:rgba(255,255,255,.31);font-size:11px;pointer-events:none}.umbral.consent-phase .copy,.umbral.bridge-phase .copy,.umbral.camera-phase .copy,.umbral.ready-phase .copy{opacity:0;transition:opacity .7s ease}.umbral.consent-phase .yul{animation:yulHoldConsent 2.8s ease-in-out infinite;opacity:1}.umbral.bridge-phase .yul{animation:yulHoldConsent 2.8s ease-in-out infinite;opacity:1}.umbral.camera-phase .yul{animation:yulCamera 4.1s ease-in-out infinite;opacity:1}.umbral.ready-phase .yul{animation:yulFarewell 9s ease-in-out forwards;opacity:1}@keyframes breathWorld{0%,100%{transform:scale(.98) rotate(0deg);opacity:.42}50%{transform:scale(1.08) rotate(9deg);opacity:.86}}@keyframes starDrift{from{background-position:0 0,0 0,0 0}to{background-position:130px -310px,-190px -360px,240px -460px}}@keyframes sparkRise{0%{opacity:0;transform:translateY(0) scale(.55)}15%{opacity:.9}75%{opacity:.38}100%{opacity:0;transform:translateY(-160px) translateX(25px) scale(1.12)}}@keyframes lineReveal{0%{opacity:0;filter:blur(14px);transform:translateY(22px) scale(.97)}18%{opacity:1;filter:blur(0);transform:translateY(0) scale(1)}76%{opacity:1;filter:blur(0);transform:translateY(0) scale(1)}100%{opacity:0;filter:blur(14px);transform:translateY(-20px) scale(1.02)}}@keyframes yulAura{0%,100%{transform:scale(.82);opacity:.46}50%{transform:scale(1.28);opacity:.92}}@keyframes yulTail{0%,7%{opacity:0;transform:rotate(15deg) scaleX(.25)}9%,18%{opacity:.92;transform:rotate(15deg) scaleX(1.2)}19%,27%{opacity:.18;transform:rotate(-30deg) scaleX(.6)}28%,38%{opacity:.86;transform:rotate(8deg) scaleX(1)}39%,49%{opacity:.22;transform:rotate(-20deg) scaleX(.55)}50%,62%{opacity:.92;transform:rotate(22deg) scaleX(1.18)}63%,75%{opacity:.18;transform:rotate(-14deg) scaleX(.55)}76%,88%{opacity:.88;transform:rotate(4deg) scaleX(1.08)}100%{opacity:.14;transform:rotate(0) scaleX(.3)}}@keyframes yulLife{0%{left:-10%;top:76%;opacity:0;transform:translate(-50%,-50%) scale(.50)}3%{opacity:1}7%{left:112%;top:22%;transform:translate(-50%,-50%) scale(1.18)}8%{opacity:0}10%{left:85%;top:78%;opacity:0;transform:translate(-50%,-50%) scale(.58)}12%{opacity:1}17%{left:17%;top:30%;transform:translate(-50%,-50%) scale(1.02)}18%{opacity:0}21%{left:8%;top:55%;opacity:0;transform:translate(-50%,-50%) scale(.7)}23%{opacity:1}29%{left:82%;top:46%;transform:translate(-50%,-50%) scale(1.08)}31%{left:53%;top:40%;opacity:.82;transform:translate(-50%,-50%) scale(.92)}34%{opacity:0}38%{left:70%;top:18%;opacity:0;transform:translate(-50%,-50%) scale(.58)}40%{opacity:1}47%{left:22%;top:74%;transform:translate(-50%,-50%) scale(1.15)}48%{opacity:0}52%{left:104%;top:58%;opacity:0;transform:translate(-50%,-50%) scale(.7)}54%{opacity:1}61%{left:18%;top:42%;transform:translate(-50%,-50%) scale(1.04)}64%{left:50%;top:39%;opacity:.88;transform:translate(-50%,-50%) scale(.92)}67%{opacity:0}72%{left:12%;top:22%;opacity:0;transform:translate(-50%,-50%) scale(.62)}74%{opacity:1}83%{left:88%;top:62%;transform:translate(-50%,-50%) scale(1.22)}85%{opacity:0}89%{left:50%;top:38%;opacity:0;transform:translate(-50%,-50%) scale(.86)}91%{opacity:1}100%{left:50%;top:38%;opacity:.86;transform:translate(-50%,-50%) scale(.96)}}@keyframes yulHoldConsent{0%,100%{left:50%;top:22%;transform:translate(-50%,-50%) scale(.86);box-shadow:0 0 18px rgba(255,255,255,.95),0 0 42px rgba(81,214,255,.76),0 0 82px rgba(40,86,255,.44)}50%{left:50%;top:22%;transform:translate(-50%,-50%) scale(1.08);box-shadow:0 0 24px #fff,0 0 62px rgba(81,214,255,.98),0 0 118px rgba(89,0,255,.48)}}@keyframes yulCamera{0%,100%{left:18%;top:18%;transform:translate(-50%,-50%) scale(.78);opacity:.68}25%{left:82%;top:20%;transform:translate(-50%,-50%) scale(1.05);opacity:1}50%{left:80%;top:78%;transform:translate(-50%,-50%) scale(.82);opacity:.78}75%{left:20%;top:75%;transform:translate(-50%,-50%) scale(1.04);opacity:1}}@keyframes yulFarewell{0%{left:50%;top:42%;opacity:1;transform:translate(-50%,-50%) scale(1.18)}42%{left:50%;top:34%;opacity:.9;transform:translate(-50%,-50%) scale(.82)}78%{left:50%;top:21%;opacity:.55;transform:translate(-50%,-50%) scale(.42)}100%{left:50%;top:10%;opacity:0;transform:translate(-50%,-50%) scale(.16)}}@media(max-height:740px){.line{font-size:clamp(23px,7.4vw,39px)}.line.small{font-size:clamp(15px,4.2vw,21px)}.consent-card,.camera-card{padding:17px 16px 16px}.consent-card p,.camera-card p{margin:8px 0}.preview-wrap{aspect-ratio:9/11}.brand{top:calc(env(safe-area-inset-top) + 12px)}}@media(prefers-reduced-motion:reduce){.yul,.yul:before,.yul:after,.stage:before,.stage:after,.spark{animation:none!important}.yul{opacity:.72;left:50%;top:35%}.line{animation:none!important;opacity:1;position:relative;margin-top:18px}.copy{top:37%;transform:none}.line:not(.l1){display:none}}\n</style></head><body><main id="umbral" class="umbral" aria-label="El Umbral de ETERNA"><section class="stage"><div class="brand">ETERNA</div><div class="yul" aria-hidden="true"></div><i class="spark s1"></i><i class="spark gold s2"></i><i class="spark s3"></i><i class="spark gold s4"></i><i class="spark s5"></i><i class="spark gold s6"></i><div class="copy" aria-hidden="true"><div class="line whisper l1 gold">Shhh...</div><div class="line small l2">Escucha...</div><div class="line l3">No todas las historias<br>empiezan cuando creemos.</div><div class="line small l4">Algunas comenzaron<br>mucho antes de que llegaras aquí.</div><div class="line l5">Y sin embargo...</div><div class="line small l6">de alguna manera...<br>te estaban esperando.</div><div class="line small l7">Hay rincones donde los minutos<br>pasan sin hacer ruido.</div><div class="line small l8">Si conoces uno...<br><span class="gold">quédate allí un instante.</span></div>__RC78_YUL_PLACE_STORY____RC75_YUL_EXTRA_LINES__<div class="line small l9">Los viejos contadores de historias<br>decían que los recuerdos no desaparecen.</div><div class="line small l10">Solo aprenden a esconderse.<br>Y esperan.</div><div class="line small l11">Algunas cosas necesitan reposar<br>para ser vistas.</div><div class="line gold l12">Déjalo descansar.</div><div class="line small l13">Hay quienes buscan la magia toda su vida.</div><div class="line small l14">Y hay quienes la encuentran<br>sin darse cuenta.</div><div class="line l15 gold">Déjame verte.</div></div><div class="consent-card" id="consentCard" role="dialog" aria-modal="true" aria-labelledby="consentTitle"><h1 id="consentTitle">Antes de seguir...<br><span>debo confiarte algo.</span></h1><p>Este momento será grabado.</p><p class="legal-box">Y cuando termine, viajará únicamente hacia la persona que hizo posible que existiera.</p><p>Si decides continuar, aceptas formar parte de esta historia.</p><label class="check-row"><input id="acceptRecording" type="checkbox"><span>He leído y acepto que mi reacción sea grabada y enviada únicamente a la persona que preparó esta ETERNA.</span></label><button id="acceptConsent" class="consent-btn" disabled>Acepto y continuar</button></div><div class="bridge-card" id="bridgeCard" role="dialog" aria-modal="true" aria-labelledby="bridgeTitle"><h1 id="bridgeTitle">Bien.<br><span>Ahora sí.</span></h1><p>No todos llegan hasta aquí.</p><p>Algunos regalos solo se abren con los ojos. Este no.</p>__RC77_BRIDGE_MEMORY____RC77_BRIDGE_HINT__<p>Respira. Lo que viene no es una pantalla más. Es una puerta.</p></div><div class="camera-card" id="cameraCard" role="dialog" aria-modal="true" aria-labelledby="cameraTitle"><h1 id="cameraTitle">Déjame verte.</h1><p>Algunas historias merecen encontrar un rostro.</p><div class="preview-wrap"><video id="cameraPreview" autoplay muted playsinline></video><div class="face-guide"></div><div class="horizon"></div><div class="camera-hint" id="cameraHint">Déjalo descansar a la altura de tus ojos. Que la luz te encuentre de frente.</div></div><button id="cameraReady" class="camera-btn" disabled>Abrir mi ETERNA</button></div><form id="startForm" class="final-gate" method="post" action="/start-experience"><input type="hidden" name="recipient_token" value="__RECIPIENT_TOKEN_SAFE__"><button id="startExperienceNow" class="final-btn" type="submit">Abriendo...</button><div class="final-note">Yul abre la puerta. Nos vemos al otro lado.</div></form><div class="safe-note">No cierres esta página. Yul está abriendo el camino.</div></section></main><script>\n(function(){const root=document.getElementById(\'umbral\');const check=document.getElementById(\'acceptRecording\');const accept=document.getElementById(\'acceptConsent\');const cameraReady=document.getElementById(\'cameraReady\');const preview=document.getElementById(\'cameraPreview\');const hint=document.getElementById(\'cameraHint\');const form=document.getElementById(\'startForm\');const btn=document.getElementById(\'startExperienceNow\');const token=__RECIPIENT_TOKEN_JSON__;let stream=null;function showConsent(){if(!root.classList.contains(\'consent-done\'))root.classList.add(\'consent-phase\')}setTimeout(showConsent,55000);check.addEventListener(\'change\',function(){accept.disabled=!check.checked});async function openCameraPreview(){try{stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:\'user\',width:{ideal:720},height:{ideal:1280}},audio:true});preview.srcObject=stream;cameraReady.disabled=false;hint.textContent=\'Sube un poco el móvil. Que tus ojos encuentren la luz.\';setTimeout(function(){hint.textContent=\'Así. Sin mirar hacia abajo. Yul ya puede verte.\'},5200);setTimeout(function(){hint.textContent=\'Perfecto. Quédate ahí.\'},9400)}catch(err){cameraReady.disabled=false;hint.textContent=\'ETERNA necesita cámara y micrófono para continuar. Permítelo cuando el móvil te lo pida.\'}}accept.addEventListener(\'click\',async function(){if(!check.checked)return;root.classList.remove(\'consent-phase\');root.classList.add(\'consent-done\');root.classList.add(\'bridge-phase\');setTimeout(async function(){root.classList.remove(\'bridge-phase\');root.classList.add(\'camera-phase\');await openCameraPreview()},6200)});cameraReady.addEventListener(\'click\',function(){cameraReady.disabled=true;root.classList.remove(\'camera-phase\');root.classList.add(\'ready-phase\');try{if(stream)stream.getTracks().forEach(function(track){track.stop()})}catch(_){}setTimeout(function(){try{if(form.requestSubmit){form.requestSubmit()}else{form.dispatchEvent(new Event(\'submit\',{cancelable:true}))}}catch(e){form.dispatchEvent(new Event(\'submit\',{cancelable:true}))}},2100)});form.addEventListener(\'submit\',async function(e){e.preventDefault();btn.disabled=true;try{const fd=new FormData(form);const res=await fetch(\'/start-experience\',{method:\'POST\',body:fd,headers:{\'X-ETERNA-AJAX\':\'1\'}});if(!res.ok)throw new Error(\'start_experience_failed\');let data={};try{data=await res.json()}catch(_){}window.location.replace(data.redirect_url||(\'/experiencia/\'+encodeURIComponent(token)))}catch(err){btn.disabled=false;alert(\'No hemos podido abrir ETERNA todavía. Revisa la conexión y vuelve a intentarlo.\')}})})();\n</script></body></html>\n'
    html_doc = html_doc.replace("__RC75_YUL_EXTRA_LINES__", yul_place_line + yul_detail_line + yul_emotion_line + yul_hint_line)
    html_doc = html_doc.replace("__RC77_BRIDGE_MEMORY__", bridge_memory_line)
    html_doc = html_doc.replace("__RC77_BRIDGE_HINT__", bridge_hint_line)

    # RC79 — inyección segura anti-freeze sobre HTML ya construido.
    try:
        rc79_css = "\n/* RC79 YUL ANTI-FREEZE FULL */\n.yul-rescue-panel{position:fixed;left:18px;right:18px;bottom:calc(env(safe-area-inset-bottom) + 22px);z-index:99999;display:none;align-items:center;justify-content:center;gap:10px;pointer-events:auto}\n.yul-rescue-panel.is-visible{display:flex}\n.yul-rescue-button{border:1px solid rgba(255,220,145,.38);border-radius:999px;padding:15px 22px;min-height:52px;background:radial-gradient(circle at top left,rgba(112,220,255,.16),transparent 34%),linear-gradient(135deg,rgba(255,213,122,.18),rgba(255,255,255,.06));color:rgba(255,248,224,.96);font-size:13px;letter-spacing:.18em;text-transform:uppercase;text-decoration:none;text-align:center;box-shadow:0 0 26px rgba(82,207,255,.18),0 0 34px rgba(255,205,110,.10);backdrop-filter:blur(10px)}\n.yul-progress{position:fixed;left:20px;right:20px;bottom:calc(env(safe-area-inset-bottom) + 8px);height:2px;border-radius:999px;z-index:99998;overflow:hidden;background:rgba(255,255,255,.08);pointer-events:none}\n.yul-progress span{display:block;width:0%;height:100%;border-radius:inherit;background:linear-gradient(90deg,rgba(85,218,255,.95),rgba(255,218,132,.95));box-shadow:0 0 18px rgba(95,220,255,.65);transition:width .35s ease}\n.yul-safe-note{position:fixed;left:18px;right:18px;bottom:calc(env(safe-area-inset-bottom) + 86px);z-index:99999;display:none;color:rgba(255,255,255,.62);font-size:12px;line-height:1.35;text-align:center;text-shadow:0 0 18px rgba(0,0,0,.85);pointer-events:none}\n.yul-safe-note.is-visible{display:block}\n.yul-low-power *{animation-duration:.001s!important;animation-iteration-count:1!important;transition-duration:.001s!important}\n.yul-low-power .spark,.yul-low-power .trail,.yul-low-power .particle,.yul-low-power .yul-particle,.yul-low-power .floating-particle{display:none!important}\n"
        rc79_html = "\n<div id=\"yulRescuePanel\" class=\"yul-rescue-panel\" aria-live=\"polite\">\n    <button id=\"yulRescueButton\" class=\"yul-rescue-button\" type=\"button\">\u2728 Abrir mi ETERNA \u2728</button>\n</div>\n<div id=\"yulSafeNote\" class=\"yul-safe-note\"></div>\n<div id=\"yulProgress\" class=\"yul-progress\" aria-hidden=\"true\"><span></span></div>\n"
        rc79_js = "\n/* RC79 YUL ANTI-FREEZE FULL */\n(function(){\n    const token = (window.__RECIPIENT_TOKEN__ || \"\").toString();\n    const storageKey = \"eterna_yul_scene_\" + token;\n    const maxSceneMs = 30000;\n    const rescueMs = 45000;\n    const globalFallbackMs = 60000;\n    const tapThreshold = 5;\n    const lowFpsLimit = 18;\n    const rescuePanel = document.getElementById(\"yulRescuePanel\");\n    const rescueButton = document.getElementById(\"yulRescueButton\");\n    const safeNote = document.getElementById(\"yulSafeNote\");\n    const progressBar = document.querySelector(\"#yulProgress span\");\n    let currentScene = 0;\n    let lastProgressAt = Date.now();\n    let sceneStartedAt = Date.now();\n    let taps = 0;\n    let fallbackUsed = false;\n    let lastFrame = performance.now();\n    let lowFpsHits = 0;\n\n    function logYul(eventName, meta){\n        try{\n            const payload = {event:eventName, meta:meta||{}, at:new Date().toISOString(), scene:currentScene};\n            if(navigator.sendBeacon){\n                navigator.sendBeacon(\"/internal/yul-event/\" + encodeURIComponent(token), new Blob([JSON.stringify(payload)], {type:\"application/json\"}));\n            }\n        }catch(e){}\n        try{ console.log(\"[YUL]\", eventName, meta||{}); }catch(e){}\n    }\n    function saveScene(){\n        try{ localStorage.setItem(storageKey, JSON.stringify({scene:currentScene, at:Date.now(), path:location.pathname})); }catch(e){}\n    }\n    function restoreScene(){\n        try{\n            const raw = localStorage.getItem(storageKey);\n            if(!raw) return;\n            const data = JSON.parse(raw);\n            if(!data || typeof data.scene !== \"number\") return;\n            if(Date.now() - (data.at || 0) > 1000*60*60*6) return;\n            currentScene = Math.max(0, data.scene);\n            logYul(\"yul_scene_restored\", {scene:currentScene});\n        }catch(e){}\n    }\n    function updateProgress(){\n        try{\n            const total = Math.max(1, (window.__YUL_TOTAL_SCENES__ || 9));\n            const pct = Math.min(100, Math.max(4, Math.round((currentScene / total) * 100)));\n            if(progressBar) progressBar.style.width = pct + \"%\";\n        }catch(e){}\n    }\n    function showRescue(label){\n        if(rescueButton && label) rescueButton.textContent = label;\n        if(rescuePanel) rescuePanel.classList.add(\"is-visible\");\n        if(safeNote) safeNote.classList.add(\"is-visible\");\n    }\n    function openExperience(reason){\n        if(fallbackUsed) return;\n        fallbackUsed = true;\n        saveScene();\n        logYul(\"yul_fallback_open_experience\", {reason:reason});\n        try{\n            if(typeof window.startExperience === \"function\"){ window.startExperience(); return; }\n        }catch(e){}\n        try{\n            fetch(\"/start-experience/\" + encodeURIComponent(token), {method:\"POST\", credentials:\"same-origin\"})\n            .then(r => r.json())\n            .then(data => {\n                const url = (data && data.redirect_url) ? data.redirect_url : (\"/experiencia/\" + encodeURIComponent(token));\n                window.location.href = url;\n            })\n            .catch(() => { window.location.href = \"/experiencia/\" + encodeURIComponent(token); });\n        }catch(e){\n            window.location.href = \"/experiencia/\" + encodeURIComponent(token);\n        }\n    }\n    function markProgress(){\n        lastProgressAt = Date.now();\n        sceneStartedAt = Date.now();\n        saveScene();\n        updateProgress();\n    }\n    function softAdvance(reason){\n        markProgress();\n        currentScene += 1;\n        saveScene();\n        updateProgress();\n        logYul(\"yul_scene_advanced\", {reason:reason, scene:currentScene});\n        try{\n            if(typeof window.nextYulScene === \"function\"){ window.nextYulScene(reason || \"rc79\"); return; }\n            if(typeof window.advanceScene === \"function\"){ window.advanceScene(reason || \"rc79\"); return; }\n            if(typeof window.nextScene === \"function\"){ window.nextScene(reason || \"rc79\"); return; }\n        }catch(e){}\n        showRescue(\"\u2728 Abrir mi ETERNA \u2728\");\n    }\n    function watchdog(){\n        const now = Date.now();\n        if(now - sceneStartedAt > rescueMs) showRescue(\"\u2728 Abrir mi ETERNA \u2728\");\n        if(now - sceneStartedAt > maxSceneMs){\n            logYul(\"yul_watchdog_scene_recovered\", {elapsed:now - sceneStartedAt});\n            softAdvance(\"scene_watchdog\");\n        }\n        if(now - lastProgressAt > globalFallbackMs){\n            logYul(\"yul_watchdog_global_fallback\", {elapsed:now - lastProgressAt});\n            showRescue(\"\u2728 Abrir mi ETERNA \u2728\");\n        }\n    }\n    function detectLowFps(now){\n        const delta = now - lastFrame;\n        lastFrame = now;\n        if(delta > (1000 / lowFpsLimit)) lowFpsHits += 1;\n        else lowFpsHits = Math.max(0, lowFpsHits - 1);\n        if(lowFpsHits > 24){\n            document.documentElement.classList.add(\"yul-low-power\");\n            logYul(\"yul_low_power_mode_enabled\", {delta:delta});\n            return;\n        }\n        try{ requestAnimationFrame(detectLowFps); }catch(e){}\n    }\n    function bind(){\n        restoreScene();\n        updateProgress();\n        logYul(\"yul_started\", {ua:navigator.userAgent || \"\"});\n        if(rescueButton) rescueButton.addEventListener(\"click\", function(ev){ ev.preventDefault(); openExperience(\"rescue_button\"); });\n        [\"click\",\"touchstart\",\"pointerdown\"].forEach(evt => {\n            document.addEventListener(evt, function(){\n                taps += 1;\n                markProgress();\n                if(taps >= tapThreshold){\n                    showRescue(\"\u2728 Abrir mi ETERNA \u2728\");\n                    logYul(\"yul_multi_tap_rescue_visible\", {taps:taps});\n                }else if(Date.now() - sceneStartedAt > 3500){\n                    softAdvance(\"tap_recovery\");\n                }\n            }, {passive:true});\n        });\n        document.addEventListener(\"visibilitychange\", function(){\n            if(document.hidden){ saveScene(); logYul(\"yul_visibility_hidden\", {}); }\n            else{ markProgress(); showRescue(\"\u2728 Abrir mi ETERNA \u2728\"); logYul(\"yul_visibility_returned\", {}); }\n        });\n        window.addEventListener(\"focus\", function(){ markProgress(); logYul(\"yul_window_focus\", {}); });\n        window.addEventListener(\"pageshow\", function(){ markProgress(); logYul(\"yul_pageshow\", {}); });\n        window.addEventListener(\"pagehide\", function(){ saveScene(); logYul(\"yul_pagehide\", {}); });\n        window.__YUL_MARK_PROGRESS__ = markProgress;\n        window.__YUL_OPEN_EXPERIENCE__ = openExperience;\n        window.__YUL_SHOW_RESCUE__ = showRescue;\n        window.__YUL_SOFT_ADVANCE__ = softAdvance;\n        setInterval(watchdog, 1000);\n        setTimeout(() => showRescue(\"\u2728 Abrir mi ETERNA \u2728\"), globalFallbackMs);\n        try{ requestAnimationFrame(detectLowFps); }catch(e){}\n    }\n    if(document.readyState === \"loading\") document.addEventListener(\"DOMContentLoaded\", bind);\n    else bind();\n})();\n"
        html_doc = html_doc.replace("</style>", rc79_css + "</style>", 1)
        html_doc = html_doc.replace("<body>", "<body>" + rc79_html, 1)
        html_doc = html_doc.replace("<script>", "<script>\nwindow.__RECIPIENT_TOKEN__ = " + json.dumps(str(recipient_token)) + ";\nwindow.__YUL_TOTAL_SCENES__ = 9;\n", 1)
        html_doc = html_doc.replace("</script>", rc79_js + "</script>", 1)
    except Exception as e:
        print("[WARN] RC79 yul antifreeze injection skipped:", e)

    html_doc = html_doc.replace("__RC78_YUL_PLACE_STORY__", yul_place_story_line)
    html_doc = html_doc.replace("__RECIPIENT_TOKEN_SAFE__", recipient_token_safe)
    html_doc = html_doc.replace("__RECIPIENT_TOKEN_JSON__", recipient_token_json)
    html_doc = rc82_preexperience_clean_patch(html_doc)
    return HTMLResponse(html_doc)

# =========================================================
# GUÍA PREVIA A LA EXPERIENCIA — CAPA DELANTE, SIN TOCAR /experiencia
# =========================================================

@app.get("/guia/{step}/{recipient_token}", response_class=HTMLResponse)
def guia_previa_experiencia(request: Request, step: int, recipient_token: str):
    """
    RC63 — PRÓLOGO CINEMATOGRÁFICO ETERNA.
    Sustituye las pantallas frías previas al vídeo por una sola entrada narrativa:
      - silencio visual
      - mariposa guía
      - historia del tiempo
      - consentimiento claro de grabación
      - umbral "Estoy preparado"
      - entrada a /experiencia

    NO toca MediaRecorder, chunks, subida, Stripe, SMS, webhooks, cobros ni video engine.
    """
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)
    if not original_video_ready(order):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)
    if not delivery_is_unlocked(order):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)
    if bool(order.get("experience_completed")):
        return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)

    insert_order_event(order["id"], "guide_prologue_opened", "ok", "Prólogo cinematográfico ETERNA antes de iniciar experiencia")
    response = render_eterna_prologo_experience(recipient_token)
    attach_recipient_session_if_needed(order, request, response)
    return response


# =========================================================
# EXPERIENCE (VERSIÓN ESTABLE LIMPIA)
# =========================================================

@app.post("/experience-event/{recipient_token}")
async def experience_event(recipient_token: str, request: Request):
    """Eventos humanos desde Safari: permite saber si aceptó cámara, empezó grabación, terminó vídeo, etc."""
    order = get_order_by_recipient_token_or_404(recipient_token)
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    step = str(payload.get("step") or "client_event")[:80]
    status = str(payload.get("status") or "ok")[:30]
    message = str(payload.get("message") or "")[:300]
    meta = payload.get("meta") or {}
    if not isinstance(meta, dict):
        meta = {"value": str(meta)[:300]}

    insert_order_event(order["id"], step, status, message, meta)
    return JSONResponse({"ok": True})


@app.get("/experiencia/{recipient_token}", response_class=HTMLResponse)
def experiencia(request: Request, recipient_token: str, ritual_step: int = 0):
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

    try:
        ritual_step = int(ritual_step or 0)
    except Exception:
        ritual_step = 0
    ritual_step = max(0, min(ritual_step, 7))
    next_ritual_step = min(ritual_step + 1, 7)

    if gift_amount > 0:
        payoff_title = "Espere un momento…"
        payoff_text = "Estamos generando su regalo."
    else:
        payoff_title = "Espere un momento…"
        payoff_text = "Estamos guardando este vídeo para que pueda volver a verlo."

    # =========================================================
    # EXPERIENCIA FUNCIONAL RECUPERADA DEL MAIN ESTABLE
    # Bloque único activo: cámara + MediaRecorder + vídeo + subida segura.
    # =========================================================
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
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
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
    z-index: 5;
}

body.video-clean-mode [data-eterna-cinematic-scene] {
    display: none !important;
}

body.video-clean-mode video {
    z-index: 5;
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
    color: #fff7e6;
}

.text {
    font-size: 24px;
    line-height: 1.7;
    color: rgba(255,255,255,0.86);
    margin: 0 auto 14px auto;
    max-width: 520px;
}

.soft {
    font-size: 16px;
    line-height: 1.8;
    color: rgba(255,255,255,0.46);
    margin: 0 auto 0 auto;
    max-width: 460px;
}

.btn {
    display: inline-block;
    min-width: 220px;
    padding: 18px 26px;
    border-radius: 999px;
    border: 0;
    background: linear-gradient(135deg, #fff0bd 0%, #e4bd69 45%, #b9822f 100%);
    color: #120b02;
    font-weight: 700;
    font-size: 17px;
    cursor: pointer;
}

.btn:disabled {
    opacity: 0.7;
    cursor: default;
}

.error-note {
    margin-top: 18px;
    font-size: 14px;
    line-height: 1.7;
    color: rgba(255,255,255,0.62);
    max-width: 460px;
    margin-left: auto;
    margin-right: auto;
    display: none;
}

.error-note.show {
    display: block;
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
        linear-gradient(180deg, rgba(0,0,0,0.10) 0%, rgba(0,0,0,0.40) 100%),
        url("__PAYOFF_BG__") center center / cover no-repeat,
        #02050a;
}

.payoff.show {
    display: flex;
}

.payoff-card {
    width: 100%;
    max-width: 560px;
    margin: 0 auto;
    padding-top: 38vh;
    text-shadow: 0 0 18px rgba(0,0,0,.92), 0 0 34px rgba(0,0,0,.76);
}

.payoff-mark {
    width: 64px;
    height: 64px;
    margin: 0 auto 24px auto;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #f2c878;
    font-size: 34px;
    background: rgba(242,200,120,0.08);
    border: 1px solid rgba(242,200,120,0.30);
    box-shadow: 0 0 42px rgba(242,200,120,0.18);
}

.eterna-progress {
    position: relative;
    overflow: hidden;
    width: min(280px, 70vw);
    height: 2px;
    margin: 28px auto 0 auto;
    border-radius: 999px;
    background: rgba(242,200,120,0.16);
}

.eterna-progress::before {
    content: "";
    position: absolute;
    top: 0;
    left: -45%;
    width: 45%;
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, transparent, #f2c878, transparent);
    animation: eternaLine 1.8s ease-in-out infinite;
}

@keyframes eternaLine {
    0% { left: -45%; }
    100% { left: 100%; }
}

.payoff-title {
    font-size: 46px;
    line-height: 1.12;
    font-weight: 700;
    margin: 0 0 18px 0;
    color: #fff7e6;
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

.retry-actions {
    margin-top: 24px;
    display: none;
    gap: 12px;
    max-width: 320px;
    margin-left: auto;
    margin-right: auto;
}

.retry-actions.show {
    display: grid;
}

.retry-btn {
    width: 100%;
    padding: 16px 22px;
    border-radius: 999px;
    border: 0;
    background: linear-gradient(135deg, #fff0bd 0%, #e4bd69 45%, #b9822f 100%);
    color: #120b02;
    font-weight: 700;
    font-size: 15px;
    cursor: pointer;
}

.retry-btn.secondary {
    background: rgba(255,255,255,0.10);
    color: #fff7e6;
    border: 1px solid rgba(218,178,92,0.22);
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

    /* =========================================================
       RC71 PRE-EXPERIENCE MAGIC SAFE
       Solo atmósfera viva para: intro, sonido, lugar tranquilo y consentimiento.
       No cambia rutas, botones, formularios, Stripe, Twilio, DB, reacción ni sender pack.
       ========================================================= */
    .pre-magic {{
        position:absolute;
        inset:0;
        z-index:4;
        pointer-events:none;
        display:none;
        overflow:hidden;
        opacity:1;
        contain:paint;
    }}
    .screen.intro-mode .pre-magic,
    .screen.sound-mode .pre-magic,
    .screen.quiet-mode .pre-magic,
    .screen.consent-mode .pre-magic {{
        display:block;
    }}
    .pre-depth {{
        position:absolute;
        inset:-8%;
        opacity:.62;
        mix-blend-mode:screen;
        background:
            radial-gradient(circle at 18% 18%, rgba(55,207,255,.16), transparent 24%),
            radial-gradient(circle at 80% 26%, rgba(255,211,121,.12), transparent 25%),
            radial-gradient(circle at 51% 72%, rgba(72,198,255,.10), transparent 31%),
            linear-gradient(180deg, rgba(2,5,10,.08), transparent 38%, rgba(2,5,10,.20));
        filter:blur(1px);
        animation:rc71DepthBreath 9.8s ease-in-out infinite;
    }}
    .pre-fog {{
        position:absolute;
        left:-32%;
        right:-32%;
        height:44%;
        border-radius:999px;
        opacity:.0;
        filter:blur(23px);
        mix-blend-mode:screen;
        background:linear-gradient(90deg, transparent, rgba(93,211,255,.12), rgba(255,221,144,.08), rgba(93,211,255,.11), transparent);
        animation:rc71FogDrift 18s ease-in-out infinite;
    }}
    .pre-fog.fog-a {{ top:15%; animation-delay:.2s; }}
    .pre-fog.fog-b {{ bottom:8%; opacity:.0; animation-duration:22s; animation-delay:4.2s; transform:scaleY(.72); }}
    .pre-spark {{
        position:absolute;
        width:4px;
        height:4px;
        border-radius:999px;
        opacity:0;
        background:rgba(117,221,255,.96);
        box-shadow:0 0 13px rgba(117,221,255,.95), 0 0 28px rgba(117,221,255,.36);
        animation:rc71SparkRise 10.5s linear infinite;
    }}
    .pre-spark.gold {{
        background:rgba(255,221,145,.95);
        box-shadow:0 0 13px rgba(255,221,145,.90), 0 0 28px rgba(255,196,74,.34);
    }}
    .ps1 {{ left:13%; bottom:11%; animation-delay:.1s; animation-duration:11.8s; transform:scale(.75); }}
    .ps2 {{ left:28%; bottom:25%; animation-delay:2.8s; animation-duration:13.2s; transform:scale(.55); }}
    .ps3 {{ left:47%; bottom:10%; animation-delay:1.4s; animation-duration:12.6s; transform:scale(.68); }}
    .ps4 {{ left:69%; bottom:19%; animation-delay:4.1s; animation-duration:14.4s; transform:scale(.5); }}
    .ps5 {{ left:83%; bottom:33%; animation-delay:6.0s; animation-duration:12.8s; transform:scale(.62); }}
    .ps6 {{ left:56%; bottom:46%; animation-delay:7.2s; animation-duration:15.2s; transform:scale(.45); }}
    .pre-glint {{
        position:absolute;
        width:92px;
        height:2px;
        border-radius:999px;
        opacity:0;
        mix-blend-mode:screen;
        background:linear-gradient(90deg, transparent, rgba(255,255,255,.88), rgba(255,220,135,.70), transparent);
        box-shadow:0 0 18px rgba(255,227,155,.52), 0 0 35px rgba(84,211,255,.20);
        animation:rc71GlintCross 7.6s ease-in-out infinite;
    }}
    .glint-a {{ left:4%; top:31%; animation-delay:2.1s; }}
    .glint-b {{ right:-2%; bottom:27%; animation-delay:5.4s; animation-direction:reverse; }}
    .yul-live {{
        position:absolute;
        width:74px;
        height:auto;
        left:66%;
        top:22%;
        opacity:0;
        z-index:5;
        pointer-events:none;
        transform-origin:center center;
        filter:drop-shadow(0 0 14px rgba(92,216,255,.65)) drop-shadow(0 0 22px rgba(255,214,124,.30));
        mix-blend-mode:screen;
        animation:rc71YulAlive 13.5s cubic-bezier(.45,0,.25,1) infinite;
    }}
    .yul-trail {{
        position:absolute;
        left:66%;
        top:22%;
        width:120px;
        height:32px;
        border-radius:999px;
        z-index:4;
        opacity:0;
        pointer-events:none;
        mix-blend-mode:screen;
        background:radial-gradient(circle at 20% 50%, rgba(255,222,142,.38), transparent 18%), radial-gradient(circle at 48% 48%, rgba(99,219,255,.28), transparent 21%), linear-gradient(90deg, rgba(255,219,130,.00), rgba(255,219,130,.20), rgba(83,211,255,.14), transparent);
        filter:blur(7px);
        animation:rc71YulTrail 13.5s cubic-bezier(.45,0,.25,1) infinite;
    }}
    .screen.sound-mode .yul-live,
    .screen.sound-mode .yul-trail {{ top:19%; left:71%; animation-delay:1.6s; animation-duration:15s; }}
    .screen.quiet-mode .yul-live,
    .screen.quiet-mode .yul-trail {{ top:24%; left:18%; animation-delay:2.4s; animation-duration:16.5s; }}
    .screen.consent-mode .yul-live,
    .screen.consent-mode .yul-trail {{ top:18%; left:70%; animation-delay:3.2s; animation-duration:17s; opacity:0; }}
    .screen.consent-mode .pre-magic {{ opacity:.72; }}
    .screen.consent-mode .pre-spark {{ animation-duration:14.8s; }}
    .screen.quiet-mode .pre-fog {{ opacity:.0; filter:blur(27px); }}
    .screen.quiet-mode .pre-depth {{ opacity:.75; }}

    @keyframes rc71DepthBreath {{
        0%,100% {{ transform:scale(1) translate3d(0,0,0); opacity:.42; }}
        45% {{ transform:scale(1.045) translate3d(-1.8%,1.2%,0); opacity:.74; }}
        72% {{ opacity:.55; }}
    }}
    @keyframes rc71FogDrift {{
        0% {{ transform:translateX(-14%) translateY(10px) scaleX(.92); opacity:0; }}
        18% {{ opacity:.40; }}
        54% {{ opacity:.30; }}
        100% {{ transform:translateX(14%) translateY(-12px) scaleX(1.08); opacity:0; }}
    }}
    @keyframes rc71SparkRise {{
        0% {{ opacity:0; transform:translate3d(0,0,0) scale(.42); }}
        12% {{ opacity:.78; }}
        58% {{ opacity:.42; transform:translate3d(18px,-88px,0) scale(.82); }}
        100% {{ opacity:0; transform:translate3d(34px,-178px,0) scale(1.05); }}
    }}
    @keyframes rc71GlintCross {{
        0%,68% {{ opacity:0; transform:translateX(-80px) translateY(14px) rotate(-9deg) scaleX(.45); }}
        75% {{ opacity:.76; }}
        100% {{ opacity:0; transform:translateX(330px) translateY(-24px) rotate(-9deg) scaleX(1.15); }}
    }}
    @keyframes rc71YulAlive {{
        0% {{ opacity:0; transform:translate3d(-18px,12px,0) rotate(-7deg) scale(.78) skewX(0deg); }}
        10% {{ opacity:.0; }}
        18% {{ opacity:.82; transform:translate3d(0,0,0) rotate(-2deg) scale(.92) skewX(2deg); }}
        30% {{ transform:translate3d(-9px,-12px,0) rotate(4deg) scale(.98) skewX(-3deg); }}
        42% {{ transform:translate3d(7px,-4px,0) rotate(-3deg) scale(.94) skewX(3deg); }}
        55% {{ opacity:.76; transform:translate3d(-4px,10px,0) rotate(3deg) scale(.99) skewX(-2deg); }}
        68% {{ transform:translate3d(12px,-8px,0) rotate(-4deg) scale(.93) skewX(2deg); }}
        80% {{ opacity:.58; transform:translate3d(22px,4px,0) rotate(2deg) scale(.86) skewX(-1deg); }}
        100% {{ opacity:0; transform:translate3d(44px,-18px,0) rotate(8deg) scale(.72) skewX(0deg); }}
    }}
    @keyframes rc71YulTrail {{
        0%,12% {{ opacity:0; transform:translate3d(-40px,20px,0) rotate(-8deg) scale(.72); }}
        24% {{ opacity:.34; }}
        52% {{ opacity:.22; transform:translate3d(-28px,2px,0) rotate(-4deg) scale(.95); }}
        78% {{ opacity:.14; }}
        100% {{ opacity:0; transform:translate3d(14px,-12px,0) rotate(7deg) scale(.82); }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        .screen.intro-mode .pre-magic,
        .screen.sound-mode .pre-magic,
        .screen.quiet-mode .pre-magic,
        .screen.consent-mode .pre-magic {{
            opacity:.42;
        }}
        .pre-depth,
        .pre-fog,
        .pre-spark,
        .pre-glint,
        .yul-live,
        .yul-trail {{
            animation:none !important;
        }}
        .yul-live {{ opacity:.32; }}
    }}

</style>
</head>
<body>


<div aria-hidden="true" data-eterna-cinematic-scene="1" style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:1;mix-blend-mode:screen;">
    <div style="position:absolute;inset:-18%;background:radial-gradient(circle at 76% 18%,rgba(92,191,255,.28),transparent 24%),radial-gradient(circle at 63% 52%,rgba(23,82,190,.24),transparent 30%),radial-gradient(circle at 18% 82%,rgba(218,178,92,.12),transparent 28%);filter:blur(2px);opacity:.95;"></div>
    <svg viewBox="0 0 900 900" preserveAspectRatio="xMidYMid slice" style="position:absolute;inset:-7%;width:114%;height:114%;opacity:.98;filter:drop-shadow(0 0 26px rgba(125,210,255,.72)) drop-shadow(0 0 82px rgba(37,99,235,.42));" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="cinema_core" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
                <stop offset="20%" stop-color="#dff6ff" stop-opacity=".92"/>
                <stop offset="58%" stop-color="#69bfff" stop-opacity=".46"/>
                <stop offset="100%" stop-color="#061428" stop-opacity="0"/>
            </radialGradient>
            <linearGradient id="cinema_wing" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#ffffff" stop-opacity=".96"/>
                <stop offset="22%" stop-color="#c7eeff" stop-opacity=".88"/>
                <stop offset="58%" stop-color="#4aa4ff" stop-opacity=".56"/>
                <stop offset="100%" stop-color="#071c4b" stop-opacity=".08"/>
            </linearGradient>
            <filter id="wingTexture" x="-30%" y="-30%" width="160%" height="160%">
                <feTurbulence type="fractalNoise" baseFrequency="0.012 0.032" numOctaves="4" seed="8" result="noise"/>
                <feDisplacementMap in="SourceGraphic" in2="noise" scale="10" xChannelSelector="R" yChannelSelector="G"/>
                <feGaussianBlur stdDeviation="0.25"/>
            </filter>
            <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
                <feGaussianBlur stdDeviation="14" result="blur"/>
                <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
        </defs>
        <g opacity=".95">
            <path d="M836 83 C724 138 657 212 597 300 C538 388 476 430 403 461 C310 500 202 506 83 606" fill="none" stroke="#72d8ff" stroke-width="3" stroke-linecap="round" opacity=".28"/>
            <path d="M812 128 C706 169 638 237 585 318 C532 399 458 460 375 492 C284 528 186 536 91 626" fill="none" stroke="#f6c56f" stroke-width="2" stroke-linecap="round" opacity=".18"/>
            <path d="M850 178 C743 199 660 259 595 351 C530 443 451 507 360 544" fill="none" stroke="#b6ecff" stroke-width="1.4" stroke-linecap="round" opacity=".20"/>
        </g>
        <g opacity=".96">
            <animateTransform attributeName="transform" type="translate" values="0 0;-14 -20;0 0" dur="12s" repeatCount="indefinite"/>
            <circle cx="640" cy="222" r="250" fill="url(#cinema_core)" opacity=".28" filter="url(#softGlow)"/>
            <g filter="url(#wingTexture)" opacity=".96">
                <path d="M626 226 C535 85 523 12 592 8 C681 2 694 140 642 229 Z" fill="url(#cinema_wing)" opacity=".92"/>
                <path d="M655 226 C703 80 810 8 866 57 C928 112 794 211 669 244 Z" fill="url(#cinema_wing)" opacity=".92"/>
                <path d="M622 244 C508 233 451 278 485 332 C526 398 599 324 637 254 Z" fill="url(#cinema_wing)" opacity=".70"/>
                <path d="M667 250 C772 233 849 276 814 337 C776 402 699 326 655 256 Z" fill="url(#cinema_wing)" opacity=".70"/>
                <path d="M646 168 C655 201 655 242 646 315" stroke="#f9feff" stroke-width="10" stroke-linecap="round" opacity=".72"/>
                <path d="M590 50 C620 92 632 139 642 199 M735 62 C700 105 675 155 657 205 M515 278 C561 263 600 255 634 251 M791 282 C744 266 704 257 666 252" stroke="#ffffff" stroke-width="2.2" stroke-opacity=".32" fill="none"/>
            </g>
        </g>
        <g opacity=".86">
            <animate attributeName="opacity" values=".55;.95;.55" dur="5.5s" repeatCount="indefinite"/>
            <circle cx="796" cy="149" r="2.8" fill="#e8fbff"/><circle cx="752" cy="176" r="1.8" fill="#74d7ff"/><circle cx="706" cy="210" r="2.1" fill="#f7ca78"/><circle cx="650" cy="253" r="1.6" fill="#c8f2ff"/><circle cx="594" cy="300" r="1.7" fill="#82d8ff"/><circle cx="528" cy="359" r="1.9" fill="#f4c771"/><circle cx="456" cy="421" r="1.4" fill="#b8eeff"/><circle cx="375" cy="488" r="1.6" fill="#81d9ff"/><circle cx="284" cy="529" r="1.2" fill="#f7cf83"/>
        </g>
        <g opacity=".62" filter="url(#softGlow)">
            <animateTransform attributeName="transform" type="translate" values="0 0;16 -18;0 0" dur="14s" repeatCount="indefinite"/>
            <path d="M198 562 C155 492 154 446 190 441 C237 434 242 518 207 565 Z" fill="#dff7ff" opacity=".46"/>
            <path d="M215 562 C244 494 297 449 326 473 C360 501 292 551 222 573 Z" fill="#7fcfff" opacity=".42"/>
            <path d="M206 549 C211 570 210 594 204 625" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".52"/>
        </g>
    </svg>
    <div style="position:absolute;right:0;top:0;width:70vw;height:70vh;background:radial-gradient(ellipse at 70% 28%,rgba(185,237,255,.18),transparent 38%);filter:blur(24px);opacity:.88;"></div>
</div>


<div class="wrap">
    <video
    id="video"
    playsinline
    webkit-playsinline
    preload="auto"
    style="
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        transform: scale(1.15);
        transform-origin: center;
        background: black;
    "
>
        <source src="__VIDEO_URL__" type="__VIDEO_TYPE__">
    </video>

    <div class="overlay" id="overlay">
        <div class="overlay-card">
            <div class="eyebrow">ETERNA</div>

            <h1 class="title">Shhh…</h1>

            <div class="text">
                Esto no es un vídeo.<br>
                Es un momento.
            </div>

            <div class="soft">
                No pienses.<br>
                Solo deja que ocurra.
            </div>

            <button class="btn" id="startBtn" style="margin-top:28px;">
                Estoy listo
            </button>

            <div class="error-note" id="errorNote"></div>
        </div>
    </div>

    <div class="payoff" id="payoff">
        <div class="payoff-card">
            <div class="payoff-mark">♥</div>
            <div class="payoff-title" id="payoffTitle">__PAYOFF_TITLE__</div>
            <div class="payoff-text" id="payoffText">__PAYOFF_TEXT__</div>
            <div class="eterna-progress" aria-hidden="true"></div>
            <div class="loader" id="payoffLoader"></div>

            <div class="retry-actions" id="retryActions">
                <button class="retry-btn" id="retryExperienceBtn">Volver a intentarlo</button>
                <button class="retry-btn secondary" id="backToStartBtn">Volver al inicio</button>
            </div>
        </div>
    </div>
</div>

<script>
const startBtn = document.getElementById("startBtn");
const overlay = document.getElementById("overlay");
const video = document.getElementById("video");
const payoff = document.getElementById("payoff");
const payoffLoader = document.getElementById("payoffLoader");
const retryActions = document.getElementById("retryActions");
const retryExperienceBtn = document.getElementById("retryExperienceBtn");
const backToStartBtn = document.getElementById("backToStartBtn");
const errorNote = document.getElementById("errorNote");
const cinematicLayers = Array.from(document.querySelectorAll("[data-eterna-cinematic-scene]"));

function hideCinematicLayersForVideo() {
    try {
        document.body.classList.add("video-clean-mode");
        cinematicLayers.forEach((el) => { el.style.display = "none"; });
    } catch (_) {}
}

function showCinematicLayersAfterVideo() {
    try {
        cinematicLayers.forEach((el) => { el.style.display = ""; });
        document.body.classList.remove("video-clean-mode");
    } catch (_) {}
}

const recipientToken = "__RECIPIENT_TOKEN__";
const hasGift = __HAS_GIFT__;
const finalWaitingTitle = "Espere un momento…";
const finalWaitingText = hasGift
    ? "Estamos generando su regalo."
    : "Estamos guardando este vídeo para que pueda volver a verlo.";

let stream = null;
let mediaRecorder = null;
let recordedChunks = [];
let finishing = false;
let recordingMimeType = "";
let recordingExtension = "webm";
let experienceStarted = false;
let finishTimeout = null;

// Blindaje industrial Safari:
// además de guardar chunks en memoria, subimos trozos en paralelo mientras se vive la experiencia.
let liveUploadSessionId = "";
let liveChunkIndex = 0;
let liveUploadedChunks = 0;
let liveUploadChain = Promise.resolve();
let liveUploadFailed = false;
let liveLastError = null;

function showStartError(message) {
    if (!errorNote) return;
    errorNote.textContent = message || "No hemos podido preparar la grabación.";
    errorNote.classList.add("show");
}

function clearStartError() {
    if (!errorNote) return;
    errorNote.textContent = "";
    errorNote.classList.remove("show");
}

function logClientStep(step, status, message, meta) {
    try {
        fetch("/experience-event/" + recipientToken, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                step: step || "client_event",
                status: status || "ok",
                message: message || "",
                meta: meta || {}
            }),
            keepalive: true
        }).catch(() => {});
    } catch (_) {}
}

function newLiveUploadSession() {
    return String(Date.now()) + "_" + Math.random().toString(16).slice(2);
}

async function uploadLiveChunk(part, index) {
    const formData = new FormData();
    formData.append("session_id", liveUploadSessionId);
    formData.append("chunk_index", String(index));
    formData.append("extension", recordingExtension || "webm");
    formData.append("chunk", part, "live_chunk_" + index + ".part");

    let lastError = null;
    for (let attempt = 1; attempt <= 3; attempt++) {
        try {
            const response = await fetch("/upload-reaction-live-chunk/" + recipientToken, {
                method: "POST",
                body: formData
            });
            const data = await response.json().catch(() => ({}));
            if (!response.ok) {
                throw new Error(data.detail || "live_chunk_upload_failed");
            }
            liveUploadedChunks += 1;
            return data;
        } catch (e) {
            lastError = e;
            await new Promise((resolve) => setTimeout(resolve, 600 * attempt));
        }
    }
    throw lastError || new Error("live_chunk_upload_failed");
}

function queueLiveChunkUpload(part) {
    if (!part || part.size <= 0 || !liveUploadSessionId || liveUploadFailed) return;

    const index = liveChunkIndex;
    liveChunkIndex += 1;

    liveUploadChain = liveUploadChain.then(async () => {
        if (liveUploadFailed) return;
        try {
            await uploadLiveChunk(part, index);
        } catch (e) {
            liveUploadFailed = true;
            liveLastError = e;
            logClientStep("reaction_live_chunk_failed", "warning", String(e && e.message ? e.message : e), { index });
        }
    });
}

function showRetryActions() {
    if (retryActions) {
        retryActions.classList.add("show");
    }
}

function hideRetryActions() {
    if (retryActions) {
        retryActions.classList.remove("show");
    }
}

function showFinalWaitingScreen() {
    showCinematicLayersAfterVideo();
    const titleEl = document.getElementById("payoffTitle");
    const textEl = document.getElementById("payoffText");
    if (titleEl) titleEl.innerText = finalWaitingTitle;
    if (textEl) textEl.innerText = finalWaitingText;
    if (payoffLoader) payoffLoader.innerText = "";
    payoff.classList.add("show");
    hideRetryActions();
}

function buildFriendlyUploadMessage(errorCode) {
    const code = String(errorCode || "").toLowerCase();

    if (code.includes("empty_video")) {
        return "No se ha detectado ninguna grabación. Vamos a intentarlo de nuevo.";
    }

    if (code.includes("video_too_large")) {
        return "No se ha podido guardar porque el vídeo ocupa demasiado. Inténtalo otra vez.";
    }

    if (code.includes("notallowederror") || code.includes("permission") || code.includes("camera") || code.includes("microphone")) {
        return "No se ha podido grabar la reacción porque faltan permisos de cámara o micrófono.";
    }

    if (code.includes("network") || code.includes("failed to fetch") || code.includes("fetch")) {
        return "No se ha podido subir la reacción por un problema de conexión. Revisa internet e inténtalo de nuevo.";
    }

    return "No se ha podido guardar este momento. Puede faltar espacio, conexión o permisos. Vamos a intentarlo otra vez.";
}

function resetRecordingState() {
    try {
        if (finishTimeout) {
            clearTimeout(finishTimeout);
            finishTimeout = null;
        }
    } catch (_) {}

    try {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
        }
    } catch (_) {}

    try {
        if (stream) {
            stream.getTracks().forEach((t) => t.stop());
        }
    } catch (_) {}

    stream = null;
    mediaRecorder = null;
    recordedChunks = [];
    recordingMimeType = "";
    recordingExtension = "webm";
    finishing = false;
    experienceStarted = false;
    liveUploadSessionId = "";
    liveChunkIndex = 0;
    liveUploadedChunks = 0;
    liveUploadChain = Promise.resolve();
    liveUploadFailed = false;
    liveLastError = null;

    try {
        video.pause();
    } catch (_) {}

    try {
        video.currentTime = 0;
    } catch (_) {}

    overlay.classList.remove("hidden");
    payoff.classList.remove("show");
    startBtn.disabled = false;
    clearStartError();
    hideRetryActions();
}

function waitForVideoReady() {
    return new Promise((resolve) => {
        const isReady =
            Number.isFinite(video.duration) &&
            video.duration > 0 &&
            video.readyState >= 1;

        if (isReady) {
            resolve();
            return;
        }

        let resolved = false;

        const done = () => {
            if (resolved) return;
            resolved = true;
            video.removeEventListener("loadedmetadata", onReady);
            video.removeEventListener("loadeddata", onReady);
            video.removeEventListener("canplay", onReady);
            clearTimeout(timeoutId);
            resolve();
        };

        const onReady = () => {
            const readyNow =
                Number.isFinite(video.duration) &&
                video.duration > 0 &&
                video.readyState >= 1;

            if (readyNow) {
                done();
            }
        };

        const timeoutId = setTimeout(done, 4000);

        video.addEventListener("loadedmetadata", onReady);
        video.addEventListener("loadeddata", onReady);
        video.addEventListener("canplay", onReady);
    });
}

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

async function tryStartRecordingStrict() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: "user",
                width: { ideal: 360, max: 480 },
                height: { ideal: 640, max: 854 },
                frameRate: { ideal: 12, max: 15 }
            },
            audio: true
        });

        const format = detectRecordingFormat();
        recordingMimeType = format.mimeType;
        recordingExtension = format.extension;
        recordedChunks = [];
        liveUploadSessionId = newLiveUploadSession();
        liveChunkIndex = 0;
        liveUploadedChunks = 0;
        liveUploadChain = Promise.resolve();
        liveUploadFailed = false;
        liveLastError = null;

        const recorderOptions = {
            videoBitsPerSecond: 260000,
            audioBitsPerSecond: 32000
        };

        if (recordingMimeType) {
            recorderOptions.mimeType = recordingMimeType;
        }

        mediaRecorder = new MediaRecorder(stream, recorderOptions);

        mediaRecorder.ondataavailable = (e) => {
            if (e.data && e.data.size > 0) {
                recordedChunks.push(e.data);
                queueLiveChunkUpload(e.data);
            }
        };

        mediaRecorder.onerror = (e) => {
            console.error("mediaRecorder error", e);
            logClientStep("recording_error", "error", "MediaRecorder lanzó un error", { error: String(e && e.message ? e.message : e) });
        };

        // Menos trozos = menos lentitud y menos riesgo en Render/Safari.
        // Cada 8s seguimos teniendo rescate progresivo, pero sin saturar backend.
        mediaRecorder.start(8000);
        logClientStep("recording_started", "ok", "Cámara y grabación iniciadas");

        await new Promise((resolve, reject) => {
            const timer = setTimeout(() => {
                if (mediaRecorder && mediaRecorder.state === "recording") {
                    resolve();
                } else {
                    reject(new Error("recorder_not_running"));
                }
            }, 700);

            try {
                mediaRecorder.addEventListener("start", () => {
                    clearTimeout(timer);
                    resolve();
                }, { once: true });
            } catch (_) {}
        });

        console.log("🎥 grabación iniciada");
        return true;

    } catch (recordingError) {
        console.error("recording init error", recordingError);

        try {
            if (stream) {
                stream.getTracks().forEach((t) => t.stop());
            }
        } catch (_) {}

        stream = null;
        mediaRecorder = null;
        recordedChunks = [];
        recordingMimeType = "";
        recordingExtension = "webm";

        return false;
    }
}

async function uploadReactionSingle(blob) {
    const filename = "reaction." + recordingExtension;
    const formData = new FormData();
    formData.append("video", blob, filename);

    const uploadResponse = await fetch("/upload-reaction/" + recipientToken, {
        method: "POST",
        body: formData
    });

    const uploadData = await uploadResponse.json().catch(() => ({}));

    if (!uploadResponse.ok) {
        throw new Error(uploadData.detail || "upload_reaction_failed");
    }

    return uploadData;
}

async function finishLiveUploadIfPossible() {
    if (!liveUploadSessionId || liveChunkIndex <= 0 || liveUploadFailed) {
        return null;
    }

    if (payoffLoader) payoffLoader.innerText = "";
    await liveUploadChain;

    if (liveUploadFailed) {
        throw liveLastError || new Error("live_chunk_upload_failed");
    }

    const finishData = new FormData();
    finishData.append("session_id", liveUploadSessionId);
    finishData.append("total_chunks", String(liveChunkIndex));
    finishData.append("extension", recordingExtension || "webm");

    const finishResponse = await fetch("/finish-reaction-upload/" + recipientToken, {
        method: "POST",
        body: finishData
    });

    const finishJson = await finishResponse.json().catch(() => ({}));
    if (!finishResponse.ok) {
        throw new Error(finishJson.detail || "finish_live_upload_failed");
    }

    if (payoffLoader) payoffLoader.innerText = "";
    logClientStep("reaction_live_upload_finished", "ok", "Reacción ensamblada desde subida progresiva", { chunks: liveChunkIndex });
    return finishJson;
}

async function uploadReactionChunked(blob) {
    const chunkSize = 4 * 1024 * 1024; // 4 MB: menos llamadas, más rápido, sigue siendo seguro para Safari.
    const totalChunks = Math.max(1, Math.ceil(blob.size / chunkSize));
    const sessionId = String(Date.now()) + "_" + Math.random().toString(16).slice(2);

    if (payoffLoader) payoffLoader.innerText = "";

    for (let index = 0; index < totalChunks; index++) {
        const start = index * chunkSize;
        const end = Math.min(blob.size, start + chunkSize);
        const slice = blob.slice(start, end, recordingMimeType || "video/webm");

        const formData = new FormData();
        formData.append("session_id", sessionId);
        formData.append("chunk_index", String(index));
        formData.append("total_chunks", String(totalChunks));
        formData.append("extension", recordingExtension || "webm");
        formData.append("chunk", slice, "chunk_" + index + ".part");

        let uploaded = false;
        let lastError = null;

        for (let attempt = 1; attempt <= 3; attempt++) {
            try {
                const response = await fetch("/upload-reaction-chunk/" + recipientToken, {
                    method: "POST",
                    body: formData
                });
                const data = await response.json().catch(() => ({}));
                if (!response.ok) {
                    throw new Error(data.detail || "chunk_upload_failed");
                }
                uploaded = true;
                break;
            } catch (e) {
                lastError = e;
                await new Promise((resolve) => setTimeout(resolve, 700 * attempt));
            }
        }

        if (!uploaded) {
            throw lastError || new Error("chunk_upload_failed");
        }

        const pct = Math.min(99, Math.round(((index + 1) / totalChunks) * 100));
        if (payoffLoader) payoffLoader.innerText = "";
    }

    const finishData = new FormData();
    finishData.append("session_id", sessionId);
    finishData.append("total_chunks", String(totalChunks));
    finishData.append("extension", recordingExtension || "webm");

    const finishResponse = await fetch("/finish-reaction-upload/" + recipientToken, {
        method: "POST",
        body: finishData
    });

    const finishJson = await finishResponse.json().catch(() => ({}));
    if (!finishResponse.ok) {
        throw new Error(finishJson.detail || "finish_chunk_upload_failed");
    }

    if (payoffLoader) payoffLoader.innerText = "";
    return finishJson;
}

async function uploadReactionSafely(blob) {
    // Pequeños: subida clásica. Grandes: trozos. Si la clásica falla, fallback a trozos.
    const singleLimit = 4 * 1024 * 1024;
    if (blob.size <= singleLimit) {
        try {
            return await uploadReactionSingle(blob);
        } catch (e) {
            console.warn("single upload failed, trying chunked", e);
            return await uploadReactionChunked(blob);
        }
    }
    return await uploadReactionChunked(blob);
}

async function finalizeExperienceFlow() {
    if (finishing) return;
    finishing = true;

    payoff.classList.add("show");
    showFinalWaitingScreen();

    try {
        if (finishTimeout) {
            clearTimeout(finishTimeout);
            finishTimeout = null;
        }
    } catch (_) {}

    try {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            try {
                mediaRecorder.requestData();
            } catch (_) {}

            await new Promise((resolve) => {
                let done = false;

                const finish = () => {
                    if (done) return;
                    done = true;
                    clearTimeout(timeoutId);
                    resolve();
                };

                const timeoutId = setTimeout(finish, 2500);

                mediaRecorder.addEventListener("stop", finish, { once: true });

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
    } catch (e) {
        console.error("stream stop error", e);
    }

    let blob = null;
    try {
        blob = new Blob(recordedChunks, {
            type: recordingMimeType || "video/webm"
        });

        console.log("chunks:", recordedChunks.length);
        console.log("blob size:", blob.size);
    } catch (e) {
        console.error("blob error", e);
    }

    try {
        // Prioridad 1: usar lo que ya se fue subiendo mientras la persona veía el vídeo.
        // Si esto falla, todavía tenemos el blob local en memoria como rescate.
        try {
            const liveResult = await finishLiveUploadIfPossible();
            if (liveResult) {
                console.log("✅ reacción subida progresivamente");
                window.location.replace("/finalizar-experiencia/" + recipientToken);
                return;
            }
        } catch (liveError) {
            console.warn("live upload failed, using blob fallback", liveError);
            logClientStep("reaction_live_upload_fallback", "warning", "Fallo subida progresiva; intento subida de rescate", { error: String(liveError && liveError.message ? liveError.message : liveError) });
        }

        // Rescate: si la subida progresiva no terminó, subimos el blob completo o por chunks al final.
        if (blob && blob.size > 0) {
            await uploadReactionSafely(blob);
            console.log("✅ reacción subida por rescate");
        } else {
            throw new Error("empty_blob");
        }
    } catch (e) {
        console.error("upload error", e);

        let humanMessage = buildFriendlyUploadMessage(
            e?.message || e?.detail || ""
        );

        payoffLoader.innerText = humanMessage;
        showRetryActions();

        finishing = false;
        return;
    }

    window.location.replace("/finalizar-experiencia/" + recipientToken);
}

function armFinishFallbacks() {
    video.addEventListener("ended", () => {
        logClientStep("experience_video_ended", "ok", "El vídeo terminó en Safari");
        finalizeExperienceFlow();
    }, { once: true });

    let fallbackMs = 120000;

    if (Number.isFinite(video.duration) && video.duration > 0) {
        fallbackMs = Math.max(15000, Math.floor(video.duration * 1000) + 2500);
    }

    finishTimeout = setTimeout(() => {
        finalizeExperienceFlow();
    }, fallbackMs);
}

async function safeResumePlayback() {
    try {
        if (!experienceStarted || finishing) return;

        if (video.ended) {
            finalizeExperienceFlow();
            return;
        }

        if (video.paused) {
            await video.play();
        }
    } catch (e) {
        console.error("resume playback error", e);
    }
}

startBtn.addEventListener("click", async () => {
    if (experienceStarted) return;

    startBtn.disabled = true;
    clearStartError();

    try {
        try {
            video.pause();
        } catch (_) {}

        try {
            video.currentTime = 0;
        } catch (_) {}

        const recordingStarted = await tryStartRecordingStrict();

        if (!recordingStarted) {
            showStartError("No hemos podido activar cámara y micrófono. Permítelos y vuelve a pulsar.");
            startBtn.disabled = false;
            return;
        }

        const formData = new FormData();
        formData.append("recipient_token", recipientToken);

        const response = await fetch("/start-experience", {
            method: "POST",
            body: formData,
            headers: { "X-ETERNA-AJAX": "1" }
        });

        let data = {};
        try {
            data = await response.json();
        } catch (_) {}

        if (!response.ok) {
            throw new Error(data.detail || "start_experience_error");
        }

        // RC27 FIX CRÍTICO:
        // /start-experience confirma en backend que la experiencia empezó.
        // En RC26 devolvía redirect_url y este botón volvía a cargar /experiencia,
        // dejando al usuario otra vez en la pantalla Shhh sin arrancar el vídeo.
        // Aquí NO redirigimos: seguimos en la misma página, con el gesto del usuario vivo,
        // cámara ya iniciada y el vídeo listo para reproducirse.
        if (data.redirect_url) {
            console.log("RC27 start-experience confirmado; no redirijo para evitar bucle", data.redirect_url);
        }

        if (!video || !video.querySelector('source') || !video.querySelector('source').src) {
            throw new Error('experience_video_url_missing');
        }

        video.load();
        await waitForVideoReady();

        hideCinematicLayersForVideo();
        overlay.classList.add("hidden");
        experienceStarted = true;
        logClientStep("experience_started_client", "ok", "La persona empezó a vivir la experiencia");

        armFinishFallbacks();

        try {
            await video.play();
        } catch (e) {
            console.error("video play error", e);

            showStartError("No hemos podido iniciar el vídeo. Vuelve a intentarlo.");
            experienceStarted = false;
            showCinematicLayersAfterVideo();
            overlay.classList.remove("hidden");
            startBtn.disabled = false;

            try {
                if (mediaRecorder && mediaRecorder.state === "recording") {
                    mediaRecorder.stop();
                }
            } catch (_) {}

            try {
                if (stream) {
                    stream.getTracks().forEach((t) => t.stop());
                }
            } catch (_) {}

            stream = null;
            mediaRecorder = null;
            recordedChunks = [];
            recordingMimeType = "";
            recordingExtension = "webm";

            return;
        }

    } catch (e) {
        console.error("experience start error", e);
        logClientStep("experience_start_error_client", "error", String(e && e.message ? e.message : e));

        startBtn.disabled = false;
        experienceStarted = false;
        payoff.classList.remove("show");

        try {
            if (mediaRecorder && mediaRecorder.state === "recording") {
                mediaRecorder.stop();
            }
        } catch (_) {}

        try {
            if (stream) {
                stream.getTracks().forEach((t) => t.stop());
            }
        } catch (_) {}

        stream = null;
        mediaRecorder = null;
        recordedChunks = [];
        recordingMimeType = "";
        recordingExtension = "webm";

        showStartError("No hemos podido preparar este momento. Vuelve a intentarlo.");
    }
});

document.addEventListener("visibilitychange", async () => {
    if (!experienceStarted || finishing) return;

    if (document.visibilityState === "visible") {
        await safeResumePlayback();
    }
});

window.addEventListener("focus", async () => {
    if (!experienceStarted || finishing) return;
    await safeResumePlayback();
});

window.addEventListener("pagehide", () => {
    if (!experienceStarted || finishing) return;

    try {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.requestData();
        }
    } catch (_) {}
});

window.addEventListener("beforeunload", () => {
    if (!experienceStarted || finishing) return;

    try {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.requestData();
        }
    } catch (_) {}
});

if (retryExperienceBtn) {
    retryExperienceBtn.addEventListener("click", () => {
        resetRecordingState();
        clearStartError();
    });
}

if (backToStartBtn) {
    backToStartBtn.addEventListener("click", () => {
        window.location.replace("/pedido/" + recipientToken);
    });
}
</script>
</body>
</html>
    """

    html_page = html_page.replace("__VIDEO_URL__", safe_attr(experience_video_url))
    html_page = html_page.replace("__VIDEO_TYPE__", safe_attr(guess_media_type_from_url(experience_video_url)))
    html_page = html_page.replace("__RECIPIENT_TOKEN__", safe_attr(recipient_token))
    html_page = html_page.replace("__HAS_GIFT__", "true" if gift_amount > 0 else "false")
    html_page = html_page.replace("__PAYOFF_TITLE__", safe_text(payoff_title))
    html_page = html_page.replace("__PAYOFF_TEXT__", safe_text(payoff_text))
    html_page = html_page.replace("__PAYOFF_BG__", safe_attr(eterna_asset("uploading_reaction")))

    return HTMLResponse(html_page)


# =========================================================
# UPLOAD REACTION POR TROZOS (BLINDAJE SAFARI/IPHONE)
# =========================================================

@app.post("/upload-reaction-live-chunk/{recipient_token}")
async def upload_reaction_live_chunk(
    recipient_token: str,
    session_id: str = Form(...),
    chunk_index: int = Form(...),
    extension: str = Form("webm"),
    chunk: UploadFile = File(...),
):
    """Subida progresiva: Safari va mandando trozos mientras la experiencia ocurre."""
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(order.get("paid")):
        raise HTTPException(status_code=403, detail="not_paid")

    if not original_video_ready(order):
        raise HTTPException(status_code=403, detail="video_not_ready")

    if reaction_is_safe(order):
        return JSONResponse({"ok": True, "already_uploaded": True})

    session_id = safe_slug(session_id, "live_session")
    extension = (extension or "webm").lower().strip()
    if extension not in {"webm", "mp4"}:
        extension = "webm"

    try:
        chunk_index = int(chunk_index)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid_chunk_index")

    if chunk_index < 0 or chunk_index > 1000:
        raise HTTPException(status_code=400, detail="invalid_chunk_index")

    session_folder = REACTION_CHUNKS_FOLDER / order["id"] / session_id
    session_folder.mkdir(parents=True, exist_ok=True)

    data = await chunk.read()
    if not data:
        raise HTTPException(status_code=400, detail="empty_chunk")

    if len(data) > 8 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="chunk_too_large")

    chunk_path = session_folder / f"chunk_{chunk_index:05d}.part"
    with open(chunk_path, "wb") as f:
        f.write(data)

    manifest_path = session_folder / "manifest.json"
    manifest = {
        "order_id": order["id"],
        "session_id": session_id,
        "extension": extension,
        "mode": "live",
        "updated_at": now_iso(),
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    received = len(list(session_folder.glob("chunk_*.part")))
    update_order(order["id"], reaction_upload_pending=1, reaction_upload_error=None)

    # Para no llenar logs, guardamos eventos clave: primer chunk y cada 5 chunks.
    if chunk_index == 0 or (chunk_index + 1) % 5 == 0:
        insert_order_event(
            order["id"],
            "reaction_live_chunk_received",
            "ok",
            f"Grabación progresiva recibida: {received} trozos",
            {"session_id": session_id, "chunk_index": chunk_index, "bytes": len(data), "received": received},
        )

    return JSONResponse({"ok": True, "received": received, "chunk_index": chunk_index})


@app.post("/upload-reaction-chunk/{recipient_token}")
async def upload_reaction_chunk(
    recipient_token: str,
    session_id: str = Form(...),
    chunk_index: int = Form(...),
    total_chunks: int = Form(...),
    extension: str = Form("webm"),
    chunk: UploadFile = File(...),
):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(order.get("paid")):
        raise HTTPException(status_code=403, detail="not_paid")

    if not original_video_ready(order):
        raise HTTPException(status_code=403, detail="video_not_ready")

    if reaction_is_safe(order):
        return JSONResponse({"ok": True, "already_uploaded": True})

    session_id = safe_slug(session_id, "session")
    extension = (extension or "webm").lower().strip()
    if extension not in {"webm", "mp4"}:
        extension = "webm"

    try:
        chunk_index = int(chunk_index)
        total_chunks = int(total_chunks)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid_chunk_numbers")

    if total_chunks <= 0 or total_chunks > 300:
        raise HTTPException(status_code=400, detail="invalid_total_chunks")

    if chunk_index < 0 or chunk_index >= total_chunks:
        raise HTTPException(status_code=400, detail="invalid_chunk_index")

    session_folder = REACTION_CHUNKS_FOLDER / order["id"] / session_id
    session_folder.mkdir(parents=True, exist_ok=True)

    data = await chunk.read()
    if not data:
        raise HTTPException(status_code=400, detail="empty_chunk")

    if len(data) > 8 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="chunk_too_large")

    chunk_path = session_folder / f"chunk_{chunk_index:05d}.part"
    with open(chunk_path, "wb") as f:
        f.write(data)

    manifest_path = session_folder / "manifest.json"
    manifest = {
        "order_id": order["id"],
        "session_id": session_id,
        "total_chunks": total_chunks,
        "extension": extension,
        "updated_at": now_iso(),
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    received = len(list(session_folder.glob("chunk_*.part")))
    update_order(order["id"], reaction_upload_pending=1, reaction_upload_error=None)
    insert_order_event(
        order["id"],
        "reaction_chunk_received",
        "ok",
        f"Chunk {chunk_index + 1}/{total_chunks} recibido",
        {"session_id": session_id, "chunk_index": chunk_index, "total_chunks": total_chunks, "bytes": len(data), "received": received},
    )

    return JSONResponse({"ok": True, "received": received, "total_chunks": total_chunks})


@app.post("/finish-reaction-upload/{recipient_token}")
async def finish_reaction_upload(
    recipient_token: str,
    session_id: str = Form(...),
    total_chunks: int = Form(0),
    extension: str = Form("webm"),
):
    """
    🔧 FINISH FLEXIBLE / MODO MÁQUINA
    Antes fallaba con 400 si faltaba 1 chunk o Safari mandaba un contador raro.
    Ahora NO mata la experiencia por eso:
    - busca todos los chunks reales guardados
    - los ordena
    - ensambla lo recibido
    - guarda local primero
    - R2 después
    """
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(order.get("paid")):
        raise HTTPException(status_code=403, detail="not_paid")

    if not original_video_ready(order):
        raise HTTPException(status_code=403, detail="video_not_ready")

    if reaction_is_safe(order):
        maybe_mark_eterna_completed(order["id"])
        return JSONResponse({"ok": True, "already_uploaded": True, "redirect": f"/cobrar/{recipient_token}"})

    session_id = safe_slug(session_id, "session")
    extension = (extension or "webm").lower().strip()
    if extension not in {"webm", "mp4"}:
        extension = "webm"

    try:
        total_chunks = int(total_chunks or 0)
    except Exception:
        total_chunks = 0

    session_folder = REACTION_CHUNKS_FOLDER / order["id"] / session_id
    if not session_folder.exists():
        insert_order_event(order["id"], "🧩 finish_no_session", "error", "No existe carpeta de chunks", {"session_id": session_id})
        raise HTTPException(status_code=400, detail="chunk_session_not_found")

    chunk_files = sorted(session_folder.glob("chunk_*.part"))
    received = len(chunk_files)

    if received <= 0:
        insert_order_event(order["id"], "🧩 finish_no_chunks", "error", "No hay chunks recibidos", {"session_id": session_id})
        raise HTTPException(status_code=400, detail="no_chunks_received")

    # Informe humano: si Safari dijo 80 y llegaron 78, no rompemos; ensamblamos los 78.
    if total_chunks and received < total_chunks:
        insert_order_event(
            order["id"],
            "⚠️ reaction_finish_flexible",
            "warning",
            f"Safari anunció {total_chunks} chunks, llegaron {received}. Ensamblo lo recibido para no perder la reacción.",
            {"session_id": session_id, "declared": total_chunks, "received": received},
        )
    else:
        insert_order_event(
            order["id"],
            "🧩 reaction_finish_start",
            "ok",
            f"Ensamblando reacción con {received} chunks",
            {"session_id": session_id, "declared": total_chunks, "received": received},
        )

    local_path = reaction_video_path(order["id"], extension)
    try:
        with open(local_path, "wb") as out:
            for part_path in chunk_files:
                with open(part_path, "rb") as part:
                    out.write(part.read())

        saved_size = os.path.getsize(local_path) if os.path.exists(local_path) else 0
        if saved_size <= 0:
            raise Exception("assembled_file_empty")

        if saved_size > MAX_VIDEO_SIZE:
            # Último blindaje: no borramos nada; dejamos pendiente y visible.
            update_order(order["id"], reaction_upload_pending=1, reaction_upload_error="video_too_large_after_assembly")
            insert_order_event(order["id"], "🚫 reaction_too_large", "error", "La reacción ensamblada pesa demasiado", {"bytes": saved_size, "max_bytes": MAX_VIDEO_SIZE, "max_mb": MAX_VIDEO_SIZE_MB})
            raise HTTPException(status_code=400, detail="video_too_large")

        insert_order_event(
            order["id"],
            "💾 reaction_local_saved",
            "ok",
            "Reacción guardada localmente antes de R2",
            {"session_id": session_id, "bytes": saved_size, "chunks": received},
        )

        updated_order = complete_reaction_from_local_file(order, local_path, extension=extension, source="chunked_upload_flexible")

        insert_order_event(
            order["id"],
            "✅ reaction_completed",
            "ok",
            "La reacción quedó salvada y ETERNA puede continuar",
            {"bytes": saved_size, "chunks": received, "r2": bool(updated_order.get("reaction_video_public_url"))},
        )

        return JSONResponse({
            "ok": True,
            "redirect": f"/cobrar/{recipient_token}",
            "bytes": saved_size,
            "chunks_received": received,
            "chunks_declared": total_chunks,
            "finish_mode": "flexible",
        })

    except HTTPException:
        raise
    except Exception as e:
        update_order(order["id"], reaction_upload_pending=0, reaction_upload_error="chunk_assembly_failed")
        insert_order_event(order["id"], "❌ reaction_chunk_finish_failed", "error", str(e), {"session_id": session_id, "received": received})
        log_error("finish_reaction_upload", e)
        raise HTTPException(status_code=500, detail="chunk_assembly_failed")


@app.post("/upload-reaction/{recipient_token}")
async def upload_reaction(recipient_token: str, video: UploadFile = File(...)):
    order = get_order_by_recipient_token_or_404(recipient_token)

    print("🎥 UPLOAD REACTION START")
    print("➡️ order_id:", order["id"])
    print("➡️ content_type:", video.content_type)
    print("➡️ filename:", video.filename)
    log_info("❤️ RECIBIENDO REACCIÓN")
    log_info("🆔 Order ID", order["id"])
    log_info("🎯 Destinatario", f"{order.get('recipient_name')} | {order.get('recipient_phone')}")
    log_info("👤 Regalante", f"{order.get('sender_name')} | {order.get('sender_email') or 'sin email'} | {order.get('sender_phone')}")

    if not bool(order.get("paid")):
        raise HTTPException(status_code=403, detail="not_paid")

    if not original_video_ready(order):
        raise HTTPException(status_code=403, detail="video_not_ready")

    if reaction_is_safe(order):
        print("✅ Reacción ya estaba guardada. Anti doble subida activado.")
        maybe_mark_eterna_completed(order["id"])
        return JSONResponse({"ok": True, "already_uploaded": True, "redirect": f"/cobrar/{recipient_token}"})

    try:
        update_order(
            order["id"],
            reaction_upload_pending=1,
            reaction_upload_error=None,
        )

        data = await video.read()
        size = len(data)

        print("📦 reaction_size:", size)
        log_human("REACCIÓN RECIBIDA", "❤️ Está llegando la emoción", f"📦 Tamaño: {round(size / (1024 * 1024), 2)} MB", f"🆔 Pedido: {order['id']}")

        if size <= 0:
            raise HTTPException(status_code=400, detail="empty_video")

        if size > MAX_VIDEO_SIZE:
            raise HTTPException(status_code=400, detail="video_too_large")

        extension = detect_video_extension(video)
        local_path = reaction_video_path(order["id"], extension)

        with open(local_path, "wb") as f:
            f.write(data)

        saved_size = os.path.getsize(local_path) if os.path.exists(local_path) else 0
        if saved_size <= 0:
            raise Exception("local_file_empty_after_write")

        print("💾 Reacción guardada local OK:", local_path)
        print("💾 reaction_saved_size:", saved_size)
        log_human("EMOCIÓN GUARDADA EN SERVIDOR", "💾 Guardada localmente", f"📦 Tamaño: {round(saved_size / (1024 * 1024), 2)} MB")

        updated_order = complete_reaction_from_local_file(order, local_path, extension=extension, source="single_upload")

        print("✅ DB ACTUALIZADA: reacción segura")
        log_human("ETERNA COMPLETADA", "✅ La emoción se ha guardado", f"🎁 Pack listo para {order.get('sender_name')}", "💸 Siguiente paso: cobros")
        log_info("✅ REACCIÓN GUARDADA Y ETERNA COMPLETADA")
        log_info("🆔 Order ID", order["id"])
        log_info("💾 Reacción local", local_path)
        log_info("🎁 Pack regalante", sender_pack_url_from_order(updated_order))
        log_info("💸 Siguiente paso", f"/cobrar/{recipient_token}")

        return JSONResponse({
            "ok": True,
            "redirect": f"/cobrar/{recipient_token}",
        })

    except HTTPException as e:
        update_order(
            order["id"],
            reaction_upload_pending=0,
            reaction_upload_error=str(e.detail),
        )
        insert_order_event(order["id"], "reaction_upload_failed", "error", str(e.detail))
        raise

    except Exception as e:
        log_error("upload_reaction_save_error", e)

        update_order(
            order["id"],
            reaction_upload_pending=0,
            reaction_upload_error="local_save_failed",
        )
        insert_order_event(order["id"], "reaction_upload_failed", "error", "local_save_failed")

        raise HTTPException(status_code=500, detail="local_save_failed")


# =========================================================
# MI VIDEO (POST EXPERIENCIA)
# =========================================================

@app.get("/mi-video/{recipient_token}", response_class=HTMLResponse)
def mi_video(request: Request, recipient_token: str):
    """
    MI VIDEO RC8 — elimina la pantalla negra rota.
    Pantalla mobile-first con vídeo ocupando el centro y CTA claro.
    """
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not has_valid_recipient_session(order, request) and not reaction_is_safe(order):
        return render_viral_block_page()

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not original_video_ready(order):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    video_url = (order.get("experience_video_url") or "").strip()

    if not video_url:
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    media_type = guess_media_type_from_url(video_url)
    return HTMLResponse(f'''
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>ETERNA</title>
<meta name="theme-color" content="#02050a">
<style>
*{{box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
html,body{{margin:0;width:100%;min-height:100%;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}}
body{{min-height:100svh;min-height:100dvh;overflow:hidden;background:radial-gradient(circle at 80% 12%,rgba(78,190,255,.24),transparent 28%),radial-gradient(circle at 18% 88%,rgba(255,199,102,.10),transparent 32%),#02050a}}
.scene{{position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:0}}
.scene:before{{content:"";position:absolute;inset:-20%;background:radial-gradient(circle at 72% 26%,rgba(65,185,255,.22),transparent 26%),radial-gradient(circle at 48% 72%,rgba(255,205,112,.10),transparent 28%);filter:blur(18px);animation:breath 7s ease-in-out infinite}}
@keyframes breath{{0%,100%{{transform:scale(1);opacity:.55}}50%{{transform:scale(1.08);opacity:.95}}}}
.wrap{{position:relative;z-index:1;min-height:100svh;min-height:100dvh;width:100%;max-width:560px;margin:0 auto;padding:calc(env(safe-area-inset-top) + 18px) 12px calc(env(safe-area-inset-bottom) + 16px);display:flex;flex-direction:column;gap:12px}}
.logo{{letter-spacing:.42em;color:#d8b76d;font-weight:900;font-size:12px;text-align:center;text-shadow:0 0 20px rgba(255,196,92,.34)}}
h1{{margin:0;text-align:center;font-size:clamp(28px,7vw,42px);line-height:1.05;letter-spacing:-.05em;text-shadow:0 0 26px rgba(255,255,255,.16)}}
.video-shell{{position:relative;flex:1;min-height:0;border-radius:28px;overflow:hidden;background:#000;border:1px solid rgba(255,214,139,.22);box-shadow:0 0 0 1px rgba(88,205,255,.14),0 28px 90px rgba(0,0,0,.72),0 0 34px rgba(0,153,255,.18)}}
video{{width:100%;height:100%;display:block;object-fit:contain;background:#000}}
.actions{{display:grid;gap:10px}}
.btn{{min-height:56px;border-radius:18px;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:900;font-size:15px;padding:12px 16px;border:1px solid rgba(255,213,130,.22);background:rgba(255,255,255,.06);color:#fff;text-decoration:none;box-shadow:0 14px 42px rgba(0,0,0,.28)}}
.btn.primary{{background:linear-gradient(135deg,#fff0b9,#d79a35);color:#171007;border:0;box-shadow:0 0 34px rgba(255,190,72,.28)}}
@media (orientation:landscape){{body{{overflow:auto}}.wrap{{max-width:980px;display:grid;grid-template-columns:.58fr 1.42fr;grid-template-areas:"logo video" "title video" "actions video";align-items:center}}.logo{{grid-area:logo}}h1{{grid-area:title;text-align:left}}.video-shell{{grid-area:video;height:82vh;flex:none}}.actions{{grid-area:actions}}}}

    /* =========================================================
       RC71 PRE-EXPERIENCE MAGIC SAFE
       Solo atmósfera viva para: intro, sonido, lugar tranquilo y consentimiento.
       No cambia rutas, botones, formularios, Stripe, Twilio, DB, reacción ni sender pack.
       ========================================================= */
    .pre-magic {{
        position:absolute;
        inset:0;
        z-index:4;
        pointer-events:none;
        display:none;
        overflow:hidden;
        opacity:1;
        contain:paint;
    }}
    .screen.intro-mode .pre-magic,
    .screen.sound-mode .pre-magic,
    .screen.quiet-mode .pre-magic,
    .screen.consent-mode .pre-magic {{
        display:block;
    }}
    .pre-depth {{
        position:absolute;
        inset:-8%;
        opacity:.62;
        mix-blend-mode:screen;
        background:
            radial-gradient(circle at 18% 18%, rgba(55,207,255,.16), transparent 24%),
            radial-gradient(circle at 80% 26%, rgba(255,211,121,.12), transparent 25%),
            radial-gradient(circle at 51% 72%, rgba(72,198,255,.10), transparent 31%),
            linear-gradient(180deg, rgba(2,5,10,.08), transparent 38%, rgba(2,5,10,.20));
        filter:blur(1px);
        animation:rc71DepthBreath 9.8s ease-in-out infinite;
    }}
    .pre-fog {{
        position:absolute;
        left:-32%;
        right:-32%;
        height:44%;
        border-radius:999px;
        opacity:.0;
        filter:blur(23px);
        mix-blend-mode:screen;
        background:linear-gradient(90deg, transparent, rgba(93,211,255,.12), rgba(255,221,144,.08), rgba(93,211,255,.11), transparent);
        animation:rc71FogDrift 18s ease-in-out infinite;
    }}
    .pre-fog.fog-a {{ top:15%; animation-delay:.2s; }}
    .pre-fog.fog-b {{ bottom:8%; opacity:.0; animation-duration:22s; animation-delay:4.2s; transform:scaleY(.72); }}
    .pre-spark {{
        position:absolute;
        width:4px;
        height:4px;
        border-radius:999px;
        opacity:0;
        background:rgba(117,221,255,.96);
        box-shadow:0 0 13px rgba(117,221,255,.95), 0 0 28px rgba(117,221,255,.36);
        animation:rc71SparkRise 10.5s linear infinite;
    }}
    .pre-spark.gold {{
        background:rgba(255,221,145,.95);
        box-shadow:0 0 13px rgba(255,221,145,.90), 0 0 28px rgba(255,196,74,.34);
    }}
    .ps1 {{ left:13%; bottom:11%; animation-delay:.1s; animation-duration:11.8s; transform:scale(.75); }}
    .ps2 {{ left:28%; bottom:25%; animation-delay:2.8s; animation-duration:13.2s; transform:scale(.55); }}
    .ps3 {{ left:47%; bottom:10%; animation-delay:1.4s; animation-duration:12.6s; transform:scale(.68); }}
    .ps4 {{ left:69%; bottom:19%; animation-delay:4.1s; animation-duration:14.4s; transform:scale(.5); }}
    .ps5 {{ left:83%; bottom:33%; animation-delay:6.0s; animation-duration:12.8s; transform:scale(.62); }}
    .ps6 {{ left:56%; bottom:46%; animation-delay:7.2s; animation-duration:15.2s; transform:scale(.45); }}
    .pre-glint {{
        position:absolute;
        width:92px;
        height:2px;
        border-radius:999px;
        opacity:0;
        mix-blend-mode:screen;
        background:linear-gradient(90deg, transparent, rgba(255,255,255,.88), rgba(255,220,135,.70), transparent);
        box-shadow:0 0 18px rgba(255,227,155,.52), 0 0 35px rgba(84,211,255,.20);
        animation:rc71GlintCross 7.6s ease-in-out infinite;
    }}
    .glint-a {{ left:4%; top:31%; animation-delay:2.1s; }}
    .glint-b {{ right:-2%; bottom:27%; animation-delay:5.4s; animation-direction:reverse; }}
    .yul-live {{
        position:absolute;
        width:74px;
        height:auto;
        left:66%;
        top:22%;
        opacity:0;
        z-index:5;
        pointer-events:none;
        transform-origin:center center;
        filter:drop-shadow(0 0 14px rgba(92,216,255,.65)) drop-shadow(0 0 22px rgba(255,214,124,.30));
        mix-blend-mode:screen;
        animation:rc71YulAlive 13.5s cubic-bezier(.45,0,.25,1) infinite;
    }}
    .yul-trail {{
        position:absolute;
        left:66%;
        top:22%;
        width:120px;
        height:32px;
        border-radius:999px;
        z-index:4;
        opacity:0;
        pointer-events:none;
        mix-blend-mode:screen;
        background:radial-gradient(circle at 20% 50%, rgba(255,222,142,.38), transparent 18%), radial-gradient(circle at 48% 48%, rgba(99,219,255,.28), transparent 21%), linear-gradient(90deg, rgba(255,219,130,.00), rgba(255,219,130,.20), rgba(83,211,255,.14), transparent);
        filter:blur(7px);
        animation:rc71YulTrail 13.5s cubic-bezier(.45,0,.25,1) infinite;
    }}
    .screen.sound-mode .yul-live,
    .screen.sound-mode .yul-trail {{ top:19%; left:71%; animation-delay:1.6s; animation-duration:15s; }}
    .screen.quiet-mode .yul-live,
    .screen.quiet-mode .yul-trail {{ top:24%; left:18%; animation-delay:2.4s; animation-duration:16.5s; }}
    .screen.consent-mode .yul-live,
    .screen.consent-mode .yul-trail {{ top:18%; left:70%; animation-delay:3.2s; animation-duration:17s; opacity:0; }}
    .screen.consent-mode .pre-magic {{ opacity:.72; }}
    .screen.consent-mode .pre-spark {{ animation-duration:14.8s; }}
    .screen.quiet-mode .pre-fog {{ opacity:.0; filter:blur(27px); }}
    .screen.quiet-mode .pre-depth {{ opacity:.75; }}

    @keyframes rc71DepthBreath {{
        0%,100% {{ transform:scale(1) translate3d(0,0,0); opacity:.42; }}
        45% {{ transform:scale(1.045) translate3d(-1.8%,1.2%,0); opacity:.74; }}
        72% {{ opacity:.55; }}
    }}
    @keyframes rc71FogDrift {{
        0% {{ transform:translateX(-14%) translateY(10px) scaleX(.92); opacity:0; }}
        18% {{ opacity:.40; }}
        54% {{ opacity:.30; }}
        100% {{ transform:translateX(14%) translateY(-12px) scaleX(1.08); opacity:0; }}
    }}
    @keyframes rc71SparkRise {{
        0% {{ opacity:0; transform:translate3d(0,0,0) scale(.42); }}
        12% {{ opacity:.78; }}
        58% {{ opacity:.42; transform:translate3d(18px,-88px,0) scale(.82); }}
        100% {{ opacity:0; transform:translate3d(34px,-178px,0) scale(1.05); }}
    }}
    @keyframes rc71GlintCross {{
        0%,68% {{ opacity:0; transform:translateX(-80px) translateY(14px) rotate(-9deg) scaleX(.45); }}
        75% {{ opacity:.76; }}
        100% {{ opacity:0; transform:translateX(330px) translateY(-24px) rotate(-9deg) scaleX(1.15); }}
    }}
    @keyframes rc71YulAlive {{
        0% {{ opacity:0; transform:translate3d(-18px,12px,0) rotate(-7deg) scale(.78) skewX(0deg); }}
        10% {{ opacity:.0; }}
        18% {{ opacity:.82; transform:translate3d(0,0,0) rotate(-2deg) scale(.92) skewX(2deg); }}
        30% {{ transform:translate3d(-9px,-12px,0) rotate(4deg) scale(.98) skewX(-3deg); }}
        42% {{ transform:translate3d(7px,-4px,0) rotate(-3deg) scale(.94) skewX(3deg); }}
        55% {{ opacity:.76; transform:translate3d(-4px,10px,0) rotate(3deg) scale(.99) skewX(-2deg); }}
        68% {{ transform:translate3d(12px,-8px,0) rotate(-4deg) scale(.93) skewX(2deg); }}
        80% {{ opacity:.58; transform:translate3d(22px,4px,0) rotate(2deg) scale(.86) skewX(-1deg); }}
        100% {{ opacity:0; transform:translate3d(44px,-18px,0) rotate(8deg) scale(.72) skewX(0deg); }}
    }}
    @keyframes rc71YulTrail {{
        0%,12% {{ opacity:0; transform:translate3d(-40px,20px,0) rotate(-8deg) scale(.72); }}
        24% {{ opacity:.34; }}
        52% {{ opacity:.22; transform:translate3d(-28px,2px,0) rotate(-4deg) scale(.95); }}
        78% {{ opacity:.14; }}
        100% {{ opacity:0; transform:translate3d(14px,-12px,0) rotate(7deg) scale(.82); }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        .screen.intro-mode .pre-magic,
        .screen.sound-mode .pre-magic,
        .screen.quiet-mode .pre-magic,
        .screen.consent-mode .pre-magic {{
            opacity:.42;
        }}
        .pre-depth,
        .pre-fog,
        .pre-spark,
        .pre-glint,
        .yul-live,
        .yul-trail {{
            animation:none !important;
        }}
        .yul-live {{ opacity:.32; }}
    }}

</style>
</head>
<body>
<div class="scene"></div>
<main class="wrap">
  <div class="logo">ETERNA</div>
  <h1>Esto ya es tuyo.</h1>
  <section class="video-shell">
    <video controls playsinline preload="metadata">
      <source src="{safe_attr(video_url)}" type="{safe_attr(media_type)}">
    </video>
  </section>
  <nav class="actions">
    <a class="btn primary" href="/pedido/{safe_attr(recipient_token)}">Volver al inicio</a>
    <a class="btn" href="/crear">Crear una ETERNA</a>
  </nav>
</main>
</body>
</html>
''')


# =========================================================
# COBRAR / CONNECT / PAYOUT (UNA SOLA PANTALLA)
# =========================================================

@app.get("/cobrar/{recipient_token}", response_class=HTMLResponse)
def cobrar(request: Request, recipient_token: str):
    """COBRAR RC48 — pantalla de regalo por código, sin PNG ni overlays."""
    order = get_order_by_recipient_token_or_404(recipient_token)
    log_info("💸 DESTINATARIO ENTRA EN COBROS")
    log_info("🆔 Order ID", order.get("id"))
    log_info("🎯 Destinatario", f"{order.get('recipient_name')} | {order.get('recipient_phone')}")
    log_info("🎁 Regalo", f"{order.get('gift_amount') or 0}€")

    if not has_valid_recipient_session(order, request) and not reaction_is_safe(order):
        return render_viral_block_page()
    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)
    if not original_video_ready(order):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)
    if not reaction_is_safe(order):
        return RedirectResponse(url=f"/experiencia/{recipient_token}", status_code=303)

    try:
        if order.get("stripe_connected_account_id"):
            refresh_connect_status(order)
            order = get_order_by_recipient_token_or_404(recipient_token)
    except Exception as e:
        log_error("refresh_connect_status_en_cobrar", e)

    gift_amount = float(order.get("gift_amount") or 0)
    cashout_status = compute_cashout_status(order)

    if gift_amount <= 0:
        amount_text = "Este regalo no incluía dinero."
        cta_html = f'<a href="/mi-video/{safe_attr(recipient_token)}" class="btn primary">Volver a ver mi ETERNA</a>'
    elif cashout_status == "completed":
        amount_text = f"Tu regalo de {format_amount_display(gift_amount)} ya ha sido enviado."
        cta_html = f'<a href="/mi-video/{safe_attr(recipient_token)}" class="btn primary">Volver a ver mi ETERNA</a>'
    elif cashout_status == "processing":
        amount_text = f"Estamos procesando tu regalo de {format_amount_display(gift_amount)}."
        cta_html = f'<a href="/mi-video/{safe_attr(recipient_token)}" class="btn primary">Volver a ver mi ETERNA</a>'
    elif cashout_status == "ready_to_send":
        amount_text = f"Has recibido {format_amount_display(gift_amount)}."
        cta_html = f'<form action="/connect/payout/{safe_attr(recipient_token)}" method="post"><button type="submit" class="btn primary">Recibir mi regalo</button></form>'
    else:
        amount_text = f"Has recibido {format_amount_display(gift_amount)}."
        connect_url = None
        try:
            connect_url = create_connect_onboarding_link(order)
        except Exception as e:
            log_error("create_connect_onboarding_link_en_cobrar", e)
        if connect_url:
            cta_html = f'<a href="{safe_attr(connect_url)}" class="btn primary">Recibir mi regalo</a>'
        else:
            cta_html = '<a href="" class="btn primary">Intentar recibir mi regalo</a>'

    return render_gift_code_screen(recipient_token, amount_text, cta_html)



@app.get("/recibir-regalo/{recipient_token}", response_class=HTMLResponse)
def recibir_regalo(request: Request, recipient_token: str):
    return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)


@app.get("/connect/refresh/{recipient_token}")
def connect_refresh(recipient_token: str):
    return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)


@app.get("/connect/return/{recipient_token}")
def connect_return(recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    try:
        refresh_connect_status(order)
    except Exception as e:
        log_error("refresh_connect_status", e)

    return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)


@app.post("/connect/payout/{recipient_token}")
def connect_payout(request: Request, recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    if not has_valid_recipient_session(order, request) and not reaction_is_safe(order):
        return render_viral_block_page()

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not original_video_ready(order):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    if not reaction_is_safe(order):
        return RedirectResponse(url=f"/experiencia/{recipient_token}", status_code=303)

    try:
        refresh_connect_status(order)
    except Exception as e:
        log_error("refresh_connect_status", e)

    refreshed = get_order_by_recipient_token_or_404(recipient_token)

    if not bool(refreshed.get("connect_onboarding_completed")):
        return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)

    try:
        process_gift_transfer_for_order(refreshed)
    except Exception as e:
        log_error("process_gift_transfer_for_order", e)

    return RedirectResponse(url=f"/cobrar/{recipient_token}", status_code=303)




# =========================================================
# RC81 — SENDER PACK MASTER V1 BUTTONS / LAYOUT HELPER
# =========================================================

def rc81_polish_sender_pack_html(html_doc: str) -> str:
    try:
        rc81_css = """
<style id="rc81-sender-pack-master">
.rc81-sender-actions{display:flex;flex-direction:column;gap:12px;width:min(92%,430px);margin:18px auto 24px;position:relative;z-index:60}
.rc81-sender-btn{min-height:58px;border-radius:18px;border:1px solid rgba(255,215,136,.42);background:rgba(0,0,0,.34);color:#fff4dc;display:flex;align-items:center;justify-content:center;gap:10px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;text-decoration:none;box-shadow:0 0 18px rgba(255,205,92,.12),inset 0 0 18px rgba(255,255,255,.035);backdrop-filter:blur(10px)}
.rc81-sender-btn.primary{background:linear-gradient(135deg,#fff1bb,#e6a43c 56%,#9c5d08);color:#170b02;box-shadow:0 0 30px rgba(255,190,72,.38),inset 0 0 18px rgba(255,255,255,.22)}
.rc81-sender-btn.secondary{background:rgba(0,0,0,.40)}
.rc81-sender-btn.download{background:rgba(0,0,0,.28)}
.sender-actions,.sender-buttons,.actions,.pack-actions,.cta-stack{display:flex!important;flex-direction:column!important;gap:12px!important;width:min(92%,430px)!important;margin:18px auto 22px!important;position:relative!important;z-index:30!important}
.sender-actions a,.sender-actions button,.sender-buttons a,.sender-buttons button,.actions a,.actions button,.pack-actions a,.pack-actions button,.cta-stack a,.cta-stack button{width:100%!important;min-height:56px!important;border-radius:18px!important;text-align:center!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:10px!important;font-weight:800!important;letter-spacing:.08em!important;text-transform:uppercase!important;text-decoration:none!important;box-sizing:border-box!important}
.reaction-video,.reaction-box,.reaction-window,.reaction-preview,.sender-reaction{right:10px!important;bottom:10px!important;left:auto!important;top:auto!important;transform:none!important;width:clamp(74px,23%,112px)!important;aspect-ratio:9/16!important;border-radius:16px!important;overflow:hidden!important;z-index:20!important}
.reaction-video video,.reaction-box video,.reaction-window video,.reaction-preview video,.sender-reaction video{width:100%!important;height:100%!important;object-fit:cover!important}
.rc81-hidden-old{display:none!important}
@media(max-width:420px){.rc81-sender-actions{width:min(92%,360px);gap:10px;margin-top:14px}.rc81-sender-btn{min-height:54px;border-radius:16px;font-size:13px}}
</style>
"""
        if "rc81-sender-pack-master" not in html_doc:
            if "</head>" in html_doc:
                html_doc = html_doc.replace("</head>", rc81_css + "</head>", 1)
            elif "</style>" in html_doc:
                html_doc = html_doc.replace("</style>", rc81_css + "</style>", 1)
            else:
                html_doc = rc81_css + html_doc

        rc81_js = """
<script id="rc81-sender-buttons-js">
(function(){
  function byText(txt){
    txt=(txt||"").toLowerCase();
    return Array.from(document.querySelectorAll("a,button")).find(function(el){return (el.textContent||"").toLowerCase().includes(txt);});
  }
  function hrefOf(el,fallback){return el&&el.tagName==="A"?el.getAttribute("href"):fallback;}
  var createOld=byText("crear")||document.querySelector('a[href*="/crear"]');
  var shareOld=byText("compartir");
  var downloadOld=byText("descargar");
  var createHref=hrefOf(createOld,"/crear");
  var shareHref=hrefOf(shareOld,"#");
  var downloadHref=hrefOf(downloadOld,"#");
  var host=document.querySelector(".rc81-sender-actions");
  if(!host){
    host=document.createElement("div");
    host.className="rc81-sender-actions";
    host.innerHTML='<a class="rc81-sender-btn primary" href="'+createHref+'">♡ Crear otra ETERNA</a><a class="rc81-sender-btn secondary" href="'+shareHref+'" id="rc81ShareBtn">↗ Compartir</a><a class="rc81-sender-btn download" href="'+downloadHref+'" id="rc81DownloadBtn">↓ Descargar</a>';
    var video=document.querySelector("video");
    var insertAfter=video?(video.closest("section,div,main")||video.parentElement):null;
    if(insertAfter&&insertAfter.parentNode){insertAfter.parentNode.insertBefore(host,insertAfter.nextSibling);}
    else{document.body.appendChild(host);}
  }
  Array.from(document.querySelectorAll("a,button")).forEach(function(el){
    if(host.contains(el))return;
    var t=(el.textContent||"").toLowerCase();
    if(t.includes("descargar reacción")||t.includes("compartir experiencia"))el.classList.add("rc81-hidden-old");
  });
  var shareBtn=document.getElementById("rc81ShareBtn");
  if(shareBtn){
    shareBtn.addEventListener("click",function(e){
      if(shareHref==="#"&&navigator.share){e.preventDefault();navigator.share({title:"Aquí vuelve lo que provocaste",url:location.href}).catch(function(){});}
    });
  }
})();
</script>
"""
        if "rc81-sender-buttons-js" not in html_doc:
            html_doc = html_doc.replace("</body>", rc81_js + "</body>", 1) if "</body>" in html_doc else html_doc + rc81_js
    except Exception as e:
        print("[WARN] RC81 sender polish skipped:", e)
    return html_doc


@app.get("/sender/{sender_token}", response_class=HTMLResponse)
def sender_pack(sender_token: str, view: str = ""):
    """
    SENDER PACK FINAL — flujo directo y limpio.

    Decisión RC49:
      1) Se elimina la entrada obligatoria sender-pack-entry-v1.png.
      2) Si la reacción existe, el regalante entra directo al pack principal.
      3) Si la reacción todavía no existe, se muestra una espera segura.

    No toca Stripe, Twilio, webhooks, pagos, video engine ni DB.
    """
    order = get_order_by_sender_token_or_404(sender_token)
    log_human("REGALANTE HA ABIERTO EL PACK", "🎁 El creador ha abierto el recuerdo", f"🆔 Pedido: {order.get('id')}")
    log_info("🎁 REGALANTE HA ABIERTO EL PACK")
    log_info("🆔 Order ID", order.get("id"))
    log_info("👤 Regalante", f"{order.get('sender_name')} | {order.get('sender_email') or 'sin email'} | {order.get('sender_phone')}")
    log_info("❤️ Reacción disponible", "sí" if reaction_is_safe(order) else "no")

    original_video_url = (order.get("experience_video_url") or "").strip()
    reaction_url = (order.get("reaction_video_public_url") or "").strip()
    reaction_video_type = guess_media_type_from_url(reaction_url) if reaction_url else "video/mp4"

    if not reaction_url:
        local_path = (order.get("reaction_video_local") or "").strip()
        if local_path and os.path.exists(local_path):
            reaction_url = f"{PUBLIC_BASE_URL}/video/sender-reaction/{sender_token}"
            reaction_video_type = guess_media_type_from_path(local_path)

    if not reaction_url:
        return render_eterna_image_screen(
            image_name="uploading_reaction",
            fallback_image_name="uploading_reaction",
            button_url=f"/sender/{sender_token}",
            button_label="Volver a comprobar",
            extra_note="Tu ETERNA todavía está volviendo. La reacción se está guardando.",
        )

    # RC49: sin pantalla sender-pack-entry.
    # Si la reacción está disponible, entramos directamente al pack principal.
    share_url = sender_pack_url_from_order(order)
    recipient_name = safe_text(order.get("recipient_name") or "esa persona")

    original_source_html = ""
    if original_video_url:
        original_source_html = f'<source src="{safe_attr(original_video_url)}" type="video/mp4">'

    reaction_source_html = f'<source src="{safe_attr(reaction_url)}" type="{safe_attr(reaction_video_type)}">'
    sender_bg = eterna_asset("sender_pack")

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Aquí vuelve lo que provocaste</title>
<meta name="theme-color" content="#02050a">
<style>
*{{box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
html,body{{margin:0;width:100%;min-height:100%;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif}}
body{{min-height:100svh;min-height:100dvh;overflow-x:hidden;overflow-y:auto;background:#02050a;display:flex;align-items:flex-start;justify-content:center}}
.shell{{position:relative;width:100vw;height:100svh;height:100dvh;max-width:520px;overflow:hidden;background:#02050a;box-shadow:0 0 80px rgba(0,0,0,.72)}}
.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center top;z-index:0;user-select:none;pointer-events:none}}
.glow{{position:absolute;inset:-10%;z-index:1;pointer-events:none;background:radial-gradient(circle at 50% 32%,rgba(50,190,255,.20),transparent 25%),radial-gradient(circle at 74% 45%,rgba(255,174,56,.18),transparent 18%);mix-blend-mode:screen;animation:breath 6s ease-in-out infinite}}
@keyframes breath{{0%,100%{{opacity:.45;transform:scale(1)}}50%{{opacity:.9;transform:scale(1.045)}}}}
  .main-video{{position:absolute;z-index:3;left:6.2%;right:6.2%;top:25.8%;height:43.0%;border-radius:25px;overflow:hidden;background:#000;border:1px solid rgba(71,192,255,.82);box-shadow:0 0 32px rgba(34,174,255,.54), inset 0 0 20px rgba(60,190,255,.18)}}
 .main-video video{{width:100%;height:100%;object-fit:contain;object-position:center center;display:block;background:#000;filter:contrast(1.06) saturate(1.06) brightness(1.03)}}
  .reaction-video{{position:absolute;z-index:5;right:7.2%;top:45.6%;width:30.0%;height:24.0%;border-radius:20px;overflow:hidden;background:#000;border:2px solid rgba(255,204,104,.98);box-shadow:0 0 0 1px rgba(255,245,207,.22),0 0 30px rgba(255,183,70,.72), inset 0 0 16px rgba(255,218,137,.22)}}
.reaction-video video{{width:100%;height:100%;object-fit:cover;object-position:center center;display:block;background:#000;filter:contrast(1.12) saturate(1.10) brightness(1.08)}}
.real-hit{{position:absolute;z-index:8;border:0;background:rgba(255,255,255,.001);cursor:pointer;text-indent:-9999px;overflow:hidden;border-radius:999px}}
 .hit-replay{{left:8.6%;right:8.6%;bottom:25.0%;height:7.5%}}
.hit-save{{left:8.6%;right:8.6%;bottom:16.8%;height:7.5%}}
.hit-share{{left:8.6%;right:8.6%;bottom:8.6%;height:7.5%}}
.hit-back{{right:5.8%;top:4.8%;width:36%;height:6.8%}}
 .pulse{{position:absolute;z-index:2;left:11%;right:11%;bottom:11.8%;height:7%;border-radius:999px;pointer-events:none;box-shadow:0 0 28px rgba(255,196,78,.28);animation:btnPulse 3.2s ease-in-out infinite}}
@keyframes btnPulse{{0%,100%{{opacity:.10;transform:scale(.99)}}50%{{opacity:.36;transform:scale(1.01)}}}}
.floating{{position:absolute;z-index:2;width:5px;height:5px;border-radius:999px;background:#5bd9ff;box-shadow:0 0 16px #5bd9ff;animation:floatUp 7.5s linear infinite;opacity:0;pointer-events:none}}
.f1{{left:17%;bottom:13%;animation-delay:.2s}}.f2{{left:83%;bottom:22%;animation-delay:1.5s;background:#ffd98c;box-shadow:0 0 16px #ffd98c}}.f3{{left:47%;bottom:7%;animation-delay:3.1s}}.f4{{left:70%;bottom:58%;animation-delay:4.6s}}
@keyframes floatUp{{0%{{transform:translateY(0) scale(.6);opacity:0}}15%{{opacity:.95}}100%{{transform:translateY(-180px) scale(1.1);opacity:0}}}}

 .life-line{{position:absolute;z-index:2;left:7%;right:7%;top:26.2%;height:2px;border-radius:999px;background:linear-gradient(90deg,transparent,rgba(70,210,255,.95),rgba(255,215,126,.85),transparent);box-shadow:0 0 24px rgba(70,210,255,.78),0 0 46px rgba(255,208,105,.34);animation:lifeLine 3.4s ease-in-out infinite;pointer-events:none;mix-blend-mode:screen}}
.life-line::after{{content:"";position:absolute;top:-5px;left:-12%;width:70px;height:12px;border-radius:999px;background:radial-gradient(circle,#fff,rgba(79,211,255,.86) 34%,transparent 72%);filter:blur(1px);box-shadow:0 0 26px rgba(87,215,255,.94);animation:lineStar 4.8s cubic-bezier(.42,0,.24,1) infinite}}
.alive-heart{{position:absolute;z-index:4;left:50%;bottom:18.9%;width:92px;height:92px;transform:translateX(-50%);border-radius:999px;pointer-events:none;display:flex;align-items:center;justify-content:center;color:#ffd98a;font-size:36px;text-shadow:0 0 20px rgba(255,212,126,.9),0 0 44px rgba(255,166,54,.5);animation:heartBeat 2.4s ease-in-out infinite}}
.alive-heart::before{{content:"";position:absolute;inset:2px;border-radius:999px;background:radial-gradient(circle,rgba(255,255,255,.20),rgba(255,198,84,.18) 38%,transparent 70%);filter:blur(3px);animation:heartHalo 3.1s ease-in-out infinite}}
.alive-heart::after{{content:"";position:absolute;inset:18px;border-radius:999px;border:1px solid rgba(255,213,128,.42);box-shadow:0 0 22px rgba(255,197,82,.38);animation:heartRing 3.7s ease-in-out infinite}}
.spark{{position:absolute;z-index:4;width:4px;height:4px;border-radius:999px;background:#ffd98a;box-shadow:0 0 14px #ffd98a,0 0 28px rgba(255,217,138,.48);opacity:0;pointer-events:none;animation:sparkFloat 5.2s linear infinite}}
.s1{{right:22%;top:38%;animation-delay:.1s}}.s2{{right:34%;top:44%;animation-delay:1.1s;background:#69d8ff;box-shadow:0 0 14px #69d8ff,0 0 28px rgba(105,216,255,.46)}}.s3{{right:11%;top:52%;animation-delay:2.0s}}.s4{{left:18%;top:26%;animation-delay:2.8s;background:#7ddfff;box-shadow:0 0 14px #7ddfff,0 0 28px rgba(125,223,255,.46)}}.s5{{left:68%;bottom:30%;animation-delay:3.6s}}
@keyframes lifeLine{{0%,100%{{opacity:.36;filter:brightness(1)}}50%{{opacity:1;filter:brightness(1.85)}}}}
@keyframes lineStar{{0%{{left:-14%;opacity:0;transform:scaleX(.62)}}12%{{opacity:1}}82%{{opacity:1}}100%{{left:104%;opacity:0;transform:scaleX(1.18)}}}}
@keyframes heartBeat{{0%,100%{{transform:translateX(-50%) scale(.96);opacity:.72}}14%{{transform:translateX(-50%) scale(1.08);opacity:1}}28%{{transform:translateX(-50%) scale(.98);opacity:.86}}44%{{transform:translateX(-50%) scale(1.04);opacity:1}}}}
@keyframes heartHalo{{0%,100%{{opacity:.18;transform:scale(.86)}}50%{{opacity:.46;transform:scale(1.12)}}}}
@keyframes heartRing{{0%{{opacity:.18;transform:scale(.72)}}55%{{opacity:.56;transform:scale(1.18)}}100%{{opacity:0;transform:scale(1.42)}}}}
@keyframes sparkFloat{{0%{{opacity:0;transform:translateY(0) scale(.55)}}16%{{opacity:.96}}72%{{opacity:.42}}100%{{opacity:0;transform:translateY(-105px) translateX(24px) scale(1.1)}}}}
  .video-shine{{position:absolute;z-index:6;left:6.2%;right:6.2%;top:25.8%;height:43.0%;border-radius:25px;pointer-events:none;overflow:hidden}}
.video-shine::before{{content:"";position:absolute;top:-35%;left:-45%;width:28%;height:170%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.18),transparent);transform:rotate(18deg);animation:videoShine 7.8s ease-in-out infinite;mix-blend-mode:screen}}
@keyframes videoShine{{0%,62%{{left:-45%;opacity:0}}70%{{opacity:.7}}100%{{left:118%;opacity:0}}}}


/* RC46 — botones reales grandes y visibles en sender pack */
.hit-save, .hit-share{{
    text-indent:0!important;
    display:flex!important;
    align-items:center!important;
    justify-content:center!important;
    left:8.6%!important;
    right:8.6%!important;
    width:auto!important;
    height:6.3%!important;
    border-radius:18px!important;
    font-size:clamp(14px,3.7vw,18px)!important;
    letter-spacing:.08em!important;
    font-weight:900!important;
    text-transform:uppercase!important;
    text-decoration:none!important;
    color:#110900!important;
    background:linear-gradient(135deg,#fff4c7 0%,#f6bd48 42%,#9c640c 100%)!important;
    border:1px solid rgba(255,238,181,.88)!important;
    box-shadow:0 0 24px rgba(255,187,65,.62), inset 0 0 18px rgba(255,255,255,.22)!important;
}}
 .hit-save{{bottom:12.4%!important;}}
.hit-share{{bottom:5.2%!important;}}
.hit-save::before{{content:"⬇ ";font-size:1.08em;margin-right:.45em;}}
.hit-share::before{{content:"↗ ";font-size:1.08em;margin-right:.45em;}}
.hit-save:active, .hit-share:active{{transform:scale(.985);filter:brightness(1.08);}}

/* RC60 — encuadre sender pack más grande y estable para vídeo real + reacción vertical. */
.main-video video:fullscreen, .reaction-video video:fullscreen{{object-fit:contain!important}}

.toast{{position:absolute;z-index:12;left:50%;bottom:calc(env(safe-area-inset-bottom) + 18px);transform:translateX(-50%) translateY(16px);max-width:86%;padding:11px 15px;border-radius:999px;background:rgba(0,0,0,.72);border:1px solid rgba(255,214,134,.28);color:#fff7df;font-size:13px;font-weight:800;opacity:0;transition:.25s ease;pointer-events:none;text-align:center}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
@media (min-width:760px){{body{{overflow:auto}}.shell{{width:min(100vw,520px);height:100svh;height:100dvh}}}}
@media (max-width:420px){{.main-video{{border-radius:20px}}.reaction-video{{border-radius:15px}}}}

    /* =========================================================
       RC71 PRE-EXPERIENCE MAGIC SAFE
       Solo atmósfera viva para: intro, sonido, lugar tranquilo y consentimiento.
       No cambia rutas, botones, formularios, Stripe, Twilio, DB, reacción ni sender pack.
       ========================================================= */
    .pre-magic {{
        position:absolute;
        inset:0;
        z-index:4;
        pointer-events:none;
        display:none;
        overflow:hidden;
        opacity:1;
        contain:paint;
    }}
    .screen.intro-mode .pre-magic,
    .screen.sound-mode .pre-magic,
    .screen.quiet-mode .pre-magic,
    .screen.consent-mode .pre-magic {{
        display:block;
    }}
    .pre-depth {{
        position:absolute;
        inset:-8%;
        opacity:.62;
        mix-blend-mode:screen;
        background:
            radial-gradient(circle at 18% 18%, rgba(55,207,255,.16), transparent 24%),
            radial-gradient(circle at 80% 26%, rgba(255,211,121,.12), transparent 25%),
            radial-gradient(circle at 51% 72%, rgba(72,198,255,.10), transparent 31%),
            linear-gradient(180deg, rgba(2,5,10,.08), transparent 38%, rgba(2,5,10,.20));
        filter:blur(1px);
        animation:rc71DepthBreath 9.8s ease-in-out infinite;
    }}
    .pre-fog {{
        position:absolute;
        left:-32%;
        right:-32%;
        height:44%;
        border-radius:999px;
        opacity:.0;
        filter:blur(23px);
        mix-blend-mode:screen;
        background:linear-gradient(90deg, transparent, rgba(93,211,255,.12), rgba(255,221,144,.08), rgba(93,211,255,.11), transparent);
        animation:rc71FogDrift 18s ease-in-out infinite;
    }}
    .pre-fog.fog-a {{ top:15%; animation-delay:.2s; }}
    .pre-fog.fog-b {{ bottom:8%; opacity:.0; animation-duration:22s; animation-delay:4.2s; transform:scaleY(.72); }}
    .pre-spark {{
        position:absolute;
        width:4px;
        height:4px;
        border-radius:999px;
        opacity:0;
        background:rgba(117,221,255,.96);
        box-shadow:0 0 13px rgba(117,221,255,.95), 0 0 28px rgba(117,221,255,.36);
        animation:rc71SparkRise 10.5s linear infinite;
    }}
    .pre-spark.gold {{
        background:rgba(255,221,145,.95);
        box-shadow:0 0 13px rgba(255,221,145,.90), 0 0 28px rgba(255,196,74,.34);
    }}
    .ps1 {{ left:13%; bottom:11%; animation-delay:.1s; animation-duration:11.8s; transform:scale(.75); }}
    .ps2 {{ left:28%; bottom:25%; animation-delay:2.8s; animation-duration:13.2s; transform:scale(.55); }}
    .ps3 {{ left:47%; bottom:10%; animation-delay:1.4s; animation-duration:12.6s; transform:scale(.68); }}
    .ps4 {{ left:69%; bottom:19%; animation-delay:4.1s; animation-duration:14.4s; transform:scale(.5); }}
    .ps5 {{ left:83%; bottom:33%; animation-delay:6.0s; animation-duration:12.8s; transform:scale(.62); }}
    .ps6 {{ left:56%; bottom:46%; animation-delay:7.2s; animation-duration:15.2s; transform:scale(.45); }}
    .pre-glint {{
        position:absolute;
        width:92px;
        height:2px;
        border-radius:999px;
        opacity:0;
        mix-blend-mode:screen;
        background:linear-gradient(90deg, transparent, rgba(255,255,255,.88), rgba(255,220,135,.70), transparent);
        box-shadow:0 0 18px rgba(255,227,155,.52), 0 0 35px rgba(84,211,255,.20);
        animation:rc71GlintCross 7.6s ease-in-out infinite;
    }}
    .glint-a {{ left:4%; top:31%; animation-delay:2.1s; }}
    .glint-b {{ right:-2%; bottom:27%; animation-delay:5.4s; animation-direction:reverse; }}
    .yul-live {{
        position:absolute;
        width:74px;
        height:auto;
        left:66%;
        top:22%;
        opacity:0;
        z-index:5;
        pointer-events:none;
        transform-origin:center center;
        filter:drop-shadow(0 0 14px rgba(92,216,255,.65)) drop-shadow(0 0 22px rgba(255,214,124,.30));
        mix-blend-mode:screen;
        animation:rc71YulAlive 13.5s cubic-bezier(.45,0,.25,1) infinite;
    }}
    .yul-trail {{
        position:absolute;
        left:66%;
        top:22%;
        width:120px;
        height:32px;
        border-radius:999px;
        z-index:4;
        opacity:0;
        pointer-events:none;
        mix-blend-mode:screen;
        background:radial-gradient(circle at 20% 50%, rgba(255,222,142,.38), transparent 18%), radial-gradient(circle at 48% 48%, rgba(99,219,255,.28), transparent 21%), linear-gradient(90deg, rgba(255,219,130,.00), rgba(255,219,130,.20), rgba(83,211,255,.14), transparent);
        filter:blur(7px);
        animation:rc71YulTrail 13.5s cubic-bezier(.45,0,.25,1) infinite;
    }}
    .screen.sound-mode .yul-live,
    .screen.sound-mode .yul-trail {{ top:19%; left:71%; animation-delay:1.6s; animation-duration:15s; }}
    .screen.quiet-mode .yul-live,
    .screen.quiet-mode .yul-trail {{ top:24%; left:18%; animation-delay:2.4s; animation-duration:16.5s; }}
    .screen.consent-mode .yul-live,
    .screen.consent-mode .yul-trail {{ top:18%; left:70%; animation-delay:3.2s; animation-duration:17s; opacity:0; }}
    .screen.consent-mode .pre-magic {{ opacity:.72; }}
    .screen.consent-mode .pre-spark {{ animation-duration:14.8s; }}
    .screen.quiet-mode .pre-fog {{ opacity:.0; filter:blur(27px); }}
    .screen.quiet-mode .pre-depth {{ opacity:.75; }}

    @keyframes rc71DepthBreath {{
        0%,100% {{ transform:scale(1) translate3d(0,0,0); opacity:.42; }}
        45% {{ transform:scale(1.045) translate3d(-1.8%,1.2%,0); opacity:.74; }}
        72% {{ opacity:.55; }}
    }}
    @keyframes rc71FogDrift {{
        0% {{ transform:translateX(-14%) translateY(10px) scaleX(.92); opacity:0; }}
        18% {{ opacity:.40; }}
        54% {{ opacity:.30; }}
        100% {{ transform:translateX(14%) translateY(-12px) scaleX(1.08); opacity:0; }}
    }}
    @keyframes rc71SparkRise {{
        0% {{ opacity:0; transform:translate3d(0,0,0) scale(.42); }}
        12% {{ opacity:.78; }}
        58% {{ opacity:.42; transform:translate3d(18px,-88px,0) scale(.82); }}
        100% {{ opacity:0; transform:translate3d(34px,-178px,0) scale(1.05); }}
    }}
    @keyframes rc71GlintCross {{
        0%,68% {{ opacity:0; transform:translateX(-80px) translateY(14px) rotate(-9deg) scaleX(.45); }}
        75% {{ opacity:.76; }}
        100% {{ opacity:0; transform:translateX(330px) translateY(-24px) rotate(-9deg) scaleX(1.15); }}
    }}
    @keyframes rc71YulAlive {{
        0% {{ opacity:0; transform:translate3d(-18px,12px,0) rotate(-7deg) scale(.78) skewX(0deg); }}
        10% {{ opacity:.0; }}
        18% {{ opacity:.82; transform:translate3d(0,0,0) rotate(-2deg) scale(.92) skewX(2deg); }}
        30% {{ transform:translate3d(-9px,-12px,0) rotate(4deg) scale(.98) skewX(-3deg); }}
        42% {{ transform:translate3d(7px,-4px,0) rotate(-3deg) scale(.94) skewX(3deg); }}
        55% {{ opacity:.76; transform:translate3d(-4px,10px,0) rotate(3deg) scale(.99) skewX(-2deg); }}
        68% {{ transform:translate3d(12px,-8px,0) rotate(-4deg) scale(.93) skewX(2deg); }}
        80% {{ opacity:.58; transform:translate3d(22px,4px,0) rotate(2deg) scale(.86) skewX(-1deg); }}
        100% {{ opacity:0; transform:translate3d(44px,-18px,0) rotate(8deg) scale(.72) skewX(0deg); }}
    }}
    @keyframes rc71YulTrail {{
        0%,12% {{ opacity:0; transform:translate3d(-40px,20px,0) rotate(-8deg) scale(.72); }}
        24% {{ opacity:.34; }}
        52% {{ opacity:.22; transform:translate3d(-28px,2px,0) rotate(-4deg) scale(.95); }}
        78% {{ opacity:.14; }}
        100% {{ opacity:0; transform:translate3d(14px,-12px,0) rotate(7deg) scale(.82); }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        .screen.intro-mode .pre-magic,
        .screen.sound-mode .pre-magic,
        .screen.quiet-mode .pre-magic,
        .screen.consent-mode .pre-magic {{
            opacity:.42;
        }}
        .pre-depth,
        .pre-fog,
        .pre-spark,
        .pre-glint,
        .yul-live,
        .yul-trail {{
            animation:none !important;
        }}
        .yul-live {{ opacity:.32; }}
    }}

</style>
</head>
<body>
<main class="shell" aria-label="Sender Pack ETERNA">
    <img class="bg" src="{safe_attr(sender_bg)}" alt="Aquí vuelve lo que provocaste">
    <div class="glow" aria-hidden="true"></div>
    <div class="life-line" aria-hidden="true"></div>
    <i class="floating f1"></i><i class="floating f2"></i><i class="floating f3"></i><i class="floating f4"></i>
    <i class="spark s1"></i><i class="spark s2"></i><i class="spark s3"></i><i class="spark s4"></i><i class="spark s5"></i>
    <section class="main-video" aria-label="Lo que enviaste">
        <video id="originalVideo" controls playsinline preload="metadata">
            {original_source_html}
        </video>
    </section>
    <div class="video-shine" aria-hidden="true"></div>
    <section class="reaction-video" aria-label="Su reacción">
        <video id="reactionVideo" muted playsinline preload="metadata">
            {reaction_source_html}
        </video>
    </section>
    <div class="alive-heart" aria-hidden="true">♡</div>
    <div class="pulse" aria-hidden="true"></div>
    <button class="real-hit hit-replay" id="replayBtn" type="button">Volver a ver esta emoción</button>
    <a class="real-hit hit-save" id="saveBtn" href="{safe_attr(reaction_url)}" download>Descargar reacción</a>
    <button class="real-hit hit-share" id="shareBtn" type="button">Compartir experiencia</button>
    <a class="real-hit hit-back" href="/sender/{safe_attr(sender_token)}">Volver a sentirlo</a>
    <div class="toast" id="toast">Listo</div>
</main>
<script>
(function(){{
  const original = document.getElementById('originalVideo');
  const reaction = document.getElementById('reactionVideo');
  const replay = document.getElementById('replayBtn');
  const share = document.getElementById('shareBtn');
  const toast = document.getElementById('toast');
  function showToast(msg){{
    if(!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 1800);
  }}
  function restartBoth(){{
    try{{ original.currentTime = 0; }}catch(e){{}}
    try{{ reaction.currentTime = 0; }}catch(e){{}}
    try{{ original.play(); }}catch(e){{}}
    try{{ reaction.play(); }}catch(e){{}}
  }}
  replay && replay.addEventListener('click', restartBoth);
  original && original.addEventListener('play', function(){{ try{{ reaction.play(); }}catch(e){{}} }});
  original && original.addEventListener('pause', function(){{ try{{ reaction.pause(); }}catch(e){{}} }});
  original && original.addEventListener('ended', function(){{ try{{ reaction.pause(); }}catch(e){{}} }});
  share && share.addEventListener('click', async function(){{
    const data = {{title:'ETERNA', text:'Aquí vuelve lo que provocaste.', url:{json.dumps(share_url)}}};
    try {{
      if (navigator.share) {{ await navigator.share(data); }}
      else {{ await navigator.clipboard.writeText(data.url); showToast('Enlace copiado'); }}
    }} catch(e) {{}}
  }});
}})();
</script>
</body>
</html>
""")



def prepare_photo_for_video_engine(original_path: str, order_id: str, slot_name: str) -> str:
    """
    RC21 MAIN PATCH — prepara la foto para el video engine SIN tocar el video engine.

    Objetivo:
    - Mantener el original intacto.
    - Crear una copia vertical 360x640 ya lista para el engine.
    - No recortar la foto principal.
    - No deformar.
    - No mandar la foto principal ampliada.
    - Rellenar con fondo blur cinematográfico.
    - Evitar que fotos horizontales/cuadradas lleguen ampliadas o raras al render.

    Importante:
    - save_upload_original_robust() sigue guardando el archivo original.
    - Esta función solo crea una copia técnica para /video/input.
    """
    TARGET_W = 360
    TARGET_H = 640

    original_path = str(original_path or "").strip()
    if not original_path or not os.path.exists(original_path):
        raise ValueError(f"Original no encontrado: {original_path}")

    safe_slot = safe_slug(slot_name, "photo")
    prepared_dir = PHOTO_FOLDER / str(order_id) / "engine_prepared"
    prepared_dir.mkdir(parents=True, exist_ok=True)

    prepared_path = prepared_dir / f"{safe_slot}_engine_360x640.jpg"

    original_mtime = os.path.getmtime(original_path)
    if prepared_path.exists() and os.path.getsize(prepared_path) > 0:
        prepared_mtime = os.path.getmtime(prepared_path)
        if prepared_mtime >= original_mtime:
            return str(prepared_path)

    with Image.open(original_path) as img:
        # Respeta orientación EXIF de iPhone/Instagram sin tocar el archivo original.
        img = ImageOps.exif_transpose(img)

        if img.mode != "RGB":
            img = img.convert("RGB")

        original_w, original_h = img.size
        if original_w <= 0 or original_h <= 0:
            raise ValueError(f"Imagen inválida: {original_path}")

        # 1) Fondo cinematográfico: cubre 360x640 con la misma foto ampliada + blur.
        bg_ratio = max(TARGET_W / original_w, TARGET_H / original_h)
        bg_w = max(int(original_w * bg_ratio), TARGET_W)
        bg_h = max(int(original_h * bg_ratio), TARGET_H)

        bg = img.resize((bg_w, bg_h), Image.LANCZOS)

        left = max((bg_w - TARGET_W) // 2, 0)
        top = max((bg_h - TARGET_H) // 2, 0)
        bg = bg.crop((left, top, left + TARGET_W, top + TARGET_H))

        bg = bg.filter(ImageFilter.GaussianBlur(radius=18))
        bg = ImageEnhance.Brightness(bg).enhance(0.42)
        bg = ImageEnhance.Contrast(bg).enhance(1.16)
        bg = ImageEnhance.Color(bg).enhance(1.08)

        # 2) Foto principal: entra COMPLETA dentro del lienzo sin recorte ni deformación.
        fg_ratio = min(TARGET_W / original_w, TARGET_H / original_h)
        fg_w = max(int(original_w * fg_ratio), 1)
        fg_h = max(int(original_h * fg_ratio), 1)

        fg = img.resize((fg_w, fg_h), Image.LANCZOS)

        x = (TARGET_W - fg_w) // 2
        y = (TARGET_H - fg_h) // 2

        bg.paste(fg, (x, y))
        bg.save(str(prepared_path), "JPEG", quality=94, optimize=True)

    if not prepared_path.exists() or os.path.getsize(prepared_path) <= 0:
        raise ValueError(f"No se pudo preparar imagen para engine: {prepared_path}")

    return str(prepared_path)


@app.get("/video/input/{order_id}/{slot_name}")
def get_video_input(order_id: str, slot_name: str):
    """
    RC21 MAIN PATCH.
    Ruta crítica para que el video engine pueda descargar las 6 fotos.

    Decisión técnica:
    - NO tocamos video engine.
    - NO tocamos zoompan.
    - NO tocamos Stripe/webhook/SMS/workers/DB.
    - El main conserva el original y entrega al engine una copia recalculada 360x640.

    Si la preparación falla, entregamos el original como fallback para no romper el render.
    """
    path = get_photo_asset_path(order_id, slot_name)
    if not path:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    try:
        prepared_path = prepare_photo_for_video_engine(path, order_id, slot_name)
        print(
            f"🖼️ RC21 /video/input preparado -> "
            f"order={order_id} slot={slot_name} "
            f"original={path} prepared={prepared_path} "
            f"size={os.path.getsize(prepared_path)}"
        )
        return FileResponse(
            prepared_path,
            media_type="image/jpeg",
            filename=os.path.basename(prepared_path),
        )

    except Exception as e:
        # Fallback salvavidas: jamás bloqueamos el render si PIL falla por una imagen rara.
        print(
            f"⚠️ RC21 prepare_photo_for_video_engine falló. "
            f"Entrego original para no romper render. "
            f"order={order_id} slot={slot_name} error={e}"
        )
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

@app.get("/admin/order-status/{order_id}", response_class=HTMLResponse)
def admin_order_status(order_id: str, token: str):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="unauthorized")

    order = get_order_by_id(order_id)
    events = list_order_events(order_id, limit=120)

    steps = [
        ("order_created", "Pedido creado"),
        ("payment_received", "Pago recibido"),
        ("render_requested", "Vídeo enviado al motor"),
        ("video_ready", "Vídeo generado"),
        ("recipient_sms_sent", "SMS enviado"),
        ("recipient_opened", "Destinatario abrió enlace"),
        ("experience_started", "Experiencia iniciada"),
        ("reaction_chunk_received", "Chunks recibidos"),
        ("reaction_assembled", "Reacción recompuesta"),
        ("reaction_saved_local", "Reacción guardada local"),
        ("reaction_r2_uploaded", "Reacción subida a R2"),
        ("eterna_completed", "ETERNA completada"),
        ("sender_sms_attempt", "SMS al regalante"),
    ]

    latest_by_step = {}
    for ev in events:
        latest_by_step[ev.get("step")] = ev

    rows = ""
    for step, label in steps:
        ev = latest_by_step.get(step)
        if ev:
            status = ev.get("status") or "ok"
            icon = "✅" if status == "ok" else ("⚠️" if status in {"warning", "pending"} else "❌")
            msg = safe_text(ev.get("message") or "")
            created = safe_text(ev.get("created_at") or "")
        else:
            icon = "⏳"
            msg = "Pendiente"
            created = ""
        rows += f"<tr><td>{icon}</td><td>{safe_text(label)}</td><td>{msg}</td><td>{created}</td></tr>"

    raw_rows = ""
    for ev in events:
        raw_rows += f"<tr><td>{safe_text(ev.get('created_at'))}</td><td>{safe_text(ev.get('step'))}</td><td>{safe_text(ev.get('status'))}</td><td>{safe_text(ev.get('message'))}</td></tr>"

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Estado ETERNA</title>
<style>
body {{ background:#050505; color:#fff; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif; padding:22px; }}
h1 {{ margin:0 0 10px; }}
.card {{ background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.08); border-radius:18px; padding:18px; margin:16px 0; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
td, th {{ border-bottom:1px solid rgba(255,255,255,.10); padding:10px; text-align:left; vertical-align:top; }}
.small {{ color:rgba(255,255,255,.62); line-height:1.6; }}
</style></head><body>


<div aria-hidden="true" data-eterna-cinematic-scene="1" style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:1;mix-blend-mode:screen;">
    <div style="position:absolute;inset:-18%;background:radial-gradient(circle at 76% 18%,rgba(92,191,255,.28),transparent 24%),radial-gradient(circle at 63% 52%,rgba(23,82,190,.24),transparent 30%),radial-gradient(circle at 18% 82%,rgba(218,178,92,.12),transparent 28%);filter:blur(2px);opacity:.95;"></div>
    <svg viewBox="0 0 900 900" preserveAspectRatio="xMidYMid slice" style="position:absolute;inset:-7%;width:114%;height:114%;opacity:.98;filter:drop-shadow(0 0 26px rgba(125,210,255,.72)) drop-shadow(0 0 82px rgba(37,99,235,.42));" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="cinema_core" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
                <stop offset="20%" stop-color="#dff6ff" stop-opacity=".92"/>
                <stop offset="58%" stop-color="#69bfff" stop-opacity=".46"/>
                <stop offset="100%" stop-color="#061428" stop-opacity="0"/>
            </radialGradient>
            <linearGradient id="cinema_wing" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#ffffff" stop-opacity=".96"/>
                <stop offset="22%" stop-color="#c7eeff" stop-opacity=".88"/>
                <stop offset="58%" stop-color="#4aa4ff" stop-opacity=".56"/>
                <stop offset="100%" stop-color="#071c4b" stop-opacity=".08"/>
            </linearGradient>
            <filter id="wingTexture" x="-30%" y="-30%" width="160%" height="160%">
                <feTurbulence type="fractalNoise" baseFrequency="0.012 0.032" numOctaves="4" seed="8" result="noise"/>
                <feDisplacementMap in="SourceGraphic" in2="noise" scale="10" xChannelSelector="R" yChannelSelector="G"/>
                <feGaussianBlur stdDeviation="0.25"/>
            </filter>
            <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
                <feGaussianBlur stdDeviation="14" result="blur"/>
                <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
        </defs>
        <g opacity=".95">
            <path d="M836 83 C724 138 657 212 597 300 C538 388 476 430 403 461 C310 500 202 506 83 606" fill="none" stroke="#72d8ff" stroke-width="3" stroke-linecap="round" opacity=".28"/>
            <path d="M812 128 C706 169 638 237 585 318 C532 399 458 460 375 492 C284 528 186 536 91 626" fill="none" stroke="#f6c56f" stroke-width="2" stroke-linecap="round" opacity=".18"/>
            <path d="M850 178 C743 199 660 259 595 351 C530 443 451 507 360 544" fill="none" stroke="#b6ecff" stroke-width="1.4" stroke-linecap="round" opacity=".20"/>
        </g>
        <g opacity=".96">
            <animateTransform attributeName="transform" type="translate" values="0 0;-14 -20;0 0" dur="12s" repeatCount="indefinite"/>
            <circle cx="640" cy="222" r="250" fill="url(#cinema_core)" opacity=".28" filter="url(#softGlow)"/>
            <g filter="url(#wingTexture)" opacity=".96">
                <path d="M626 226 C535 85 523 12 592 8 C681 2 694 140 642 229 Z" fill="url(#cinema_wing)" opacity=".92"/>
                <path d="M655 226 C703 80 810 8 866 57 C928 112 794 211 669 244 Z" fill="url(#cinema_wing)" opacity=".92"/>
                <path d="M622 244 C508 233 451 278 485 332 C526 398 599 324 637 254 Z" fill="url(#cinema_wing)" opacity=".70"/>
                <path d="M667 250 C772 233 849 276 814 337 C776 402 699 326 655 256 Z" fill="url(#cinema_wing)" opacity=".70"/>
                <path d="M646 168 C655 201 655 242 646 315" stroke="#f9feff" stroke-width="10" stroke-linecap="round" opacity=".72"/>
                <path d="M590 50 C620 92 632 139 642 199 M735 62 C700 105 675 155 657 205 M515 278 C561 263 600 255 634 251 M791 282 C744 266 704 257 666 252" stroke="#ffffff" stroke-width="2.2" stroke-opacity=".32" fill="none"/>
            </g>
        </g>
        <g opacity=".86">
            <animate attributeName="opacity" values=".55;.95;.55" dur="5.5s" repeatCount="indefinite"/>
            <circle cx="796" cy="149" r="2.8" fill="#e8fbff"/><circle cx="752" cy="176" r="1.8" fill="#74d7ff"/><circle cx="706" cy="210" r="2.1" fill="#f7ca78"/><circle cx="650" cy="253" r="1.6" fill="#c8f2ff"/><circle cx="594" cy="300" r="1.7" fill="#82d8ff"/><circle cx="528" cy="359" r="1.9" fill="#f4c771"/><circle cx="456" cy="421" r="1.4" fill="#b8eeff"/><circle cx="375" cy="488" r="1.6" fill="#81d9ff"/><circle cx="284" cy="529" r="1.2" fill="#f7cf83"/>
        </g>
        <g opacity=".62" filter="url(#softGlow)">
            <animateTransform attributeName="transform" type="translate" values="0 0;16 -18;0 0" dur="14s" repeatCount="indefinite"/>
            <path d="M198 562 C155 492 154 446 190 441 C237 434 242 518 207 565 Z" fill="#dff7ff" opacity=".46"/>
            <path d="M215 562 C244 494 297 449 326 473 C360 501 292 551 222 573 Z" fill="#7fcfff" opacity=".42"/>
            <path d="M206 549 C211 570 210 594 204 625" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".52"/>
        </g>
    </svg>
    <div style="position:absolute;right:0;top:0;width:70vw;height:70vh;background:radial-gradient(ellipse at 70% 28%,rgba(185,237,255,.18),transparent 38%);filter:blur(24px);opacity:.88;"></div>
</div>


<h1>Estado ETERNA</h1>
<div class="small">Pedido: {safe_text(order_id)} · Destinatario: {safe_text(order.get('recipient_name'))} · Regalante: {safe_text(order.get('sender_name'))}</div>
<div class="card" style="position:relative;z-index:2;"><h2>Proceso sencillo</h2><table><tbody>{rows}</tbody></table></div>
<div class="card" style="position:relative;z-index:2;"><h2>Eventos técnicos</h2><table><thead><tr><th>Hora</th><th>Paso</th><th>Estado</th><th>Mensaje</th></tr></thead><tbody>{raw_rows}</tbody></table></div>
</body></html>
    """)


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


@app.get("/admin/recover-reaction/{order_id}")
def admin_recover_reaction(order_id: str, token: str = "", force: int = 0):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    result = recover_reaction_from_chunks_if_possible(
        order_id,
        min_idle_seconds=0 if int(force or 0) == 1 else 20,
        source="admin_manual_recovery",
    )
    updated = get_order_by_id(order_id)

    return JSONResponse({
        "ok": result.get("ok", False),
        "result": result,
        "order_id": order_id,
        "reaction_uploaded": bool(updated.get("reaction_uploaded")),
        "reaction_upload_pending": bool(updated.get("reaction_upload_pending")),
        "reaction_upload_error": updated.get("reaction_upload_error"),
        "reaction_video_local": updated.get("reaction_video_local"),
        "reaction_video_public_url": updated.get("reaction_video_public_url"),
        "sender_sms_sent_at": updated.get("sender_sms_sent_at"),
        "sender_sms_attempts": int(updated.get("sender_sms_attempts") or 0),
        "sender_sms_error": updated.get("sender_sms_error"),
        "eterna_completed": bool(updated.get("eterna_completed")),
    })


@app.get("/admin/retry-sender-message/{order_id}")
def admin_retry_sender_message(order_id: str, token: str = "", force: int = 0):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    # Modo rescate: si un pedido agotó 3 intentos cuando SMS/WhatsApp estaba sin saldo
    # o mal configurado, permitimos resetear SOLO desde admin y SOLO bajo petición explícita.
    # Uso:
    # /admin/retry-sender-message/ORDER_ID?token=ADMIN_TOKEN&force=1
    if int(force or 0) == 1:
        update_order(
            order_id,
            sender_sms_attempts=0,
            sender_sms_error=None,
            sender_sms_sent_at=None,
            sender_sms_sid=None,
            sender_notified=0,
        )
        insert_order_event(order_id, "admin_sender_retry_forced", "warning", "Reintento forzado del aviso al regalante: intentos reseteados por admin")

    # Si el problema real fue que el destinatario cortó justo al final, antes de reenviar
    # intentamos convertir los chunks pendientes en reacción final.
    recover_reaction_from_chunks_if_possible(order_id, min_idle_seconds=0, source="admin_retry_sender_recovery")

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
        "force_used": bool(int(force or 0) == 1),
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
        "pending_reaction_recovery_ids": list_pending_reaction_recovery_orders(),
        "pending_sender_notification_ids": list_pending_sender_notifications(),
        "pending_payout_order_ids": list_pending_payout_orders(),
    })


@app.get("/admin/process-all-due-deliveries")
def admin_process_all_due_deliveries(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    delivery_results = process_all_due_scheduled_deliveries()
    recovery_results = process_all_pending_reaction_recoveries()
    sender_results = process_all_due_sender_notifications()
    payout_results = process_all_due_payouts()

    return JSONResponse({
        "ok": True,
        "delivery_count": len(delivery_results),
        "recovery_count": len(recovery_results),
        "sender_count": len(sender_results),
        "payout_count": len(payout_results),
        "delivery_results": delivery_results,
        "recovery_results": recovery_results,
        "sender_results": sender_results,
        "payout_results": payout_results,
    })


# =========================================================
# ADMIN R2 RETRY (REACTION)
# =========================================================

@app.post("/admin/retry-r2-reaction/{order_id}")
def admin_retry_r2_reaction(order_id: str, token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    order = get_order_by_id(order_id)
    local_path = (order.get("reaction_video_local") or "").strip()

    if not local_path or not os.path.exists(local_path):
        return JSONResponse({"ok": False, "reason": "local_reaction_not_found", "local_path": local_path})

    try:
        extension = Path(local_path).suffix.lower().replace(".", "") or "webm"
        content_type = guess_media_type_from_path(local_path)
        remote_name = f"reactions/{order_id}.{extension}"
        public_url = upload_video_to_r2(local_path, remote_name, content_type=content_type)

        if public_url:
            update_order(order_id, reaction_video_public_url=public_url, reaction_upload_error=None)
            return JSONResponse({"ok": True, "public_url": public_url})

        return JSONResponse({"ok": False, "reason": "r2_not_configured"})

    except Exception as e:
        log_error("admin_retry_r2_reaction", e)
        update_order(order_id, reaction_upload_error=str(e))
        return JSONResponse({"ok": False, "reason": str(e)})


# =========================================================
# FINALIZAR EXPERIENCIA (DEFINITIVO)
# =========================================================

@app.get("/finalizar-experiencia/{recipient_token}")
def finalizar_experiencia(request: Request, recipient_token: str):
    order = get_order_by_recipient_token_or_404(recipient_token)

    print("🏁 FINALIZANDO EXPERIENCE:", order["id"])

    if not has_valid_recipient_session(order, request) and not reaction_is_safe(order):
        return render_viral_block_page()

    if not bool(order.get("paid")):
        return RedirectResponse(url=f"/pedido/{recipient_token}", status_code=303)

    try:
        # Si el destinatario llegó aquí justo después del vídeo pero el JS no alcanzó a cerrar
        # /finish-reaction-upload, intentamos rescatar los chunks ya subidos antes de continuar.
        if not reaction_is_safe(order):
            recover_reaction_from_chunks_if_possible(order, min_idle_seconds=0, source="finalizar_experiencia_recovery")
            order = get_order_by_id(order["id"])

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
@app.get("/admin/reset-recipient-session/{order_id}")
def admin_reset_recipient_session(order_id: str, token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    order = get_order_by_id(order_id)

    update_order(
        order_id,
        recipient_session_token=None,
        recipient_session_claimed_at=None,
        experience_started=0,
    )

    refreshed = get_order_by_id(order_id)

    return JSONResponse({
        "ok": True,
        "order_id": order_id,
        "recipient_token": refreshed.get("recipient_token"),
        "experience_started": bool(refreshed.get("experience_started")),
        "experience_completed": bool(refreshed.get("experience_completed")),
        "recipient_session_token": refreshed.get("recipient_session_token"),
        "recipient_session_claimed_at": refreshed.get("recipient_session_claimed_at"),
        "recipient_url": recipient_experience_url_from_order(refreshed),
    })



# =========================================================
# ADMIN — RC60 AUDITORÍA PRELANZAMIENTO
# =========================================================

def rc60_order_flags(order: dict) -> dict:
    return {
        "id": order.get("id"),
        "state": order.get("order_state"),
        "paid": bool(order.get("paid")),
        "video_ready": original_video_ready(order),
        "delivery_sent": bool(order.get("delivery_sent")),
        "delivered_to_recipient": bool(order.get("delivered_to_recipient")),
        "recipient_sms_attempts": int(order.get("recipient_sms_attempts") or 0),
        "recipient_sms_sent_at": order.get("recipient_sms_sent_at"),
        "experience_started": bool(order.get("experience_started")),
        "experience_completed": bool(order.get("experience_completed")),
        "reaction_uploaded": bool(order.get("reaction_uploaded")),
        "reaction_exists": reaction_exists(order),
        "sender_notified": bool(order.get("sender_notified")),
        "sender_sms_attempts": int(order.get("sender_sms_attempts") or 0),
        "sender_sms_sent_at": order.get("sender_sms_sent_at"),
        "age_days": order_age_days(order),
        "link_expired_now": order_link_expired(order),
        "updated_at": order.get("updated_at"),
        "created_at": order.get("created_at"),
    }


def rc60_audit_snapshot(limit: int = 80) -> dict:
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id
        FROM orders
        ORDER BY created_at DESC
        LIMIT ?
    """, (int(limit or 80),))
    ids = [r["id"] for r in cur.fetchall()]
    conn.close()

    orders = []
    counters = {
        "total_sample": 0,
        "paid_not_video_ready": 0,
        "video_ready_not_delivered": 0,
        "delivered_without_reaction": 0,
        "reaction_without_sender_notice": 0,
        "recipient_sms_maxed": 0,
        "sender_sms_maxed": 0,
        "completed": 0,
    }

    for oid in ids:
        try:
            order = get_order_by_id(oid)
            flags = rc60_order_flags(order)
            orders.append(flags)
            counters["total_sample"] += 1
            if flags["paid"] and not flags["video_ready"]:
                counters["paid_not_video_ready"] += 1
            if flags["paid"] and flags["video_ready"] and not flags["delivery_sent"]:
                counters["video_ready_not_delivered"] += 1
            if flags["delivered_to_recipient"] and not flags["reaction_uploaded"]:
                counters["delivered_without_reaction"] += 1
            if flags["reaction_uploaded"] and not flags["sender_notified"]:
                counters["reaction_without_sender_notice"] += 1
            if flags["recipient_sms_attempts"] >= 3 and not flags["delivery_sent"]:
                counters["recipient_sms_maxed"] += 1
            if flags["sender_sms_attempts"] >= 3 and not flags["sender_notified"]:
                counters["sender_sms_maxed"] += 1
            if flags["reaction_uploaded"] and flags["sender_notified"]:
                counters["completed"] += 1
        except Exception as e:
            orders.append({"id": oid, "error": str(e)})

    recommendations = []
    if counters["video_ready_not_delivered"]:
        recommendations.append("Hay vídeos listos sin entrega: revisar worker/SMS y usar /admin/process-all-due-deliveries.")
    if counters["reaction_without_sender_notice"]:
        recommendations.append("Hay reacciones sin aviso al regalante: revisar Twilio/WhatsApp y worker de sender.")
    if counters["recipient_sms_maxed"] or counters["sender_sms_maxed"]:
        recommendations.append("Hay pedidos con máximo de intentos: revisar configuración SMS/WhatsApp antes de reenviar manualmente.")
    if not recommendations:
        recommendations.append("Muestra reciente sin bloqueos críticos detectados por RC60.")

    return {
        "ok": True,
        "rc": "RC61_BLINDAJE_VISUAL_FINAL_SAFE",
        "generated_at": now_iso(),
        "public_base_url": PUBLIC_BASE_URL,
        "startup_sweep_enabled": ETERNA_STARTUP_SWEEP_ENABLED,
        "link_expiry_enforced": ETERNA_ENFORCE_LINK_EXPIRY,
        "link_expiry_days": ETERNA_LINK_EXPIRY_DAYS,
        "messaging": messaging_config_status() if "messaging_config_status" in globals() else {},
        "counters": counters,
        "recommendations": recommendations,
        "orders": orders,
    }


@app.get("/admin/rc60-audit")
def admin_rc60_audit(token: str = "", limit: int = 80):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return JSONResponse(rc60_audit_snapshot(limit=limit))


@app.get("/admin/rc61-audit")
def admin_rc61_audit(token: str = "", limit: int = 80):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return JSONResponse(rc60_audit_snapshot(limit=limit))


@app.get("/admin/audit")
def admin_audit_alias(token: str = "", limit: int = 80):
    # Alias limpio para producción: evita tener que recordar el número de RC.
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return JSONResponse(rc60_audit_snapshot(limit=limit))


def rc61_assets_audit_snapshot() -> dict:
    items = []
    missing = []
    for logical_name, configured_name in ETERNA_SCREEN_ASSETS.items():
        resolved = resolve_eterna_asset_filename(configured_name)
        exists = bool((ETERNA_BG_FOLDER / resolved).exists())
        row = {
            "logical_name": logical_name,
            "configured_name": configured_name,
            "resolved_name": resolved,
            "exists": exists,
        }
        items.append(row)
        if not exists:
            missing.append(row)
    return {
        "ok": len(missing) == 0,
        "rc": "RC61_BLINDAJE_VISUAL_FINAL_SAFE",
        "generated_at": now_iso(),
        "asset_folder": str(ETERNA_BG_FOLDER),
        "missing_count": len(missing),
        "missing": missing,
        "assets": items,
    }


@app.get("/admin/assets-audit")
def admin_assets_audit(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return JSONResponse(rc61_assets_audit_snapshot())


@app.get("/admin/go-live-checklist", response_class=HTMLResponse)
def admin_go_live_checklist(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    audit = rc60_audit_snapshot(limit=60)
    c = audit.get("counters", {})
    items = [
        ("Circuito completo probado", "Hacer 1 pedido real completo en móvil antes de vender."),
        ("SMS anti-bucle", "Confirmar que no hay pedidos con recipient_sms_attempts/sender_sms_attempts creciendo sin control."),
        ("Sender Pack", "Verificar encuadre del vídeo principal y reacción en móvil real."),
        ("Render recovery", "Reiniciar servicio y comprobar que RC61 sweep no duplica SMS."),
        ("WhatsApp", "Pendiente hasta aprobación Meta/Twilio; SMS queda como fallback."),
        ("Legal básico", "Mantener términos/privacidad activos y revisar con profesional antes de escalar."),
    ]
    rows = "".join(f"<tr><td>✅</td><td>{safe_text(a)}</td><td>{safe_text(b)}</td></tr>" for a,b in items)
    recs = "".join(f"<li>{safe_text(r)}</li>" for r in audit.get("recommendations", []))

    return HTMLResponse(f"""
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RC61 Go Live</title>
<style>body{{margin:0;background:#05070d;color:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;padding:24px;line-height:1.55}}.card{{max-width:980px;margin:0 auto 18px;padding:18px;border:1px solid rgba(255,209,118,.22);border-radius:20px;background:rgba(255,255,255,.055)}}h1{{font-family:Georgia,serif;color:#f4ce83}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border-bottom:1px solid rgba(255,255,255,.10);text-align:left;vertical-align:top}}code{{color:#7ed7ff}}</style></head>
<body><section class="card"><h1>ETERNA RC61 — Checklist Go Live</h1><p>Estado generado: <code>{safe_text(audit.get('generated_at'))}</code></p><p>Muestra revisada: <b>{int(c.get('total_sample') or 0)}</b> pedidos recientes.</p></section>
<section class="card"><h2>Contadores críticos</h2><table><tr><th>Métrica</th><th>Valor</th></tr>{''.join(f'<tr><td>{safe_text(k)}</td><td>{safe_text(v)}</td></tr>' for k,v in c.items())}</table></section>
<section class="card"><h2>Checklist</h2><table>{rows}</table></section>
<section class="card"><h2>Recomendaciones RC61</h2><ul>{recs}</ul></section>
</body></html>""")


# =========================================================
# ADMIN — SMS / WHATSAPP DIAGNÓSTICO Y TEST REAL
# =========================================================

def messaging_config_status() -> dict:
    return {
        "sms_enabled": SMS_ENABLED,
        "whatsapp_enabled": WHATSAPP_ENABLED,
        "twilio_library_loaded": bool(Client),
        "twilio_account_sid_configured": bool(TWILIO_ACCOUNT_SID),
        "twilio_auth_token_configured": bool(TWILIO_AUTH_TOKEN),
        "twilio_sms_from_configured": bool(TWILIO_FROM_NUMBER),
        "twilio_whatsapp_from_configured": bool(TWILIO_WHATSAPP_FROM),
        "twilio_sms_ready": bool(Client and TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER and SMS_ENABLED),
        "twilio_whatsapp_ready": bool(Client and TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_WHATSAPP_FROM and WHATSAPP_ENABLED),
        "best_effort_ready": bool(
            Client
            and TWILIO_ACCOUNT_SID
            and TWILIO_AUTH_TOKEN
            and (
                (TWILIO_WHATSAPP_FROM and WHATSAPP_ENABLED)
                or (TWILIO_FROM_NUMBER and SMS_ENABLED)
            )
        ),
    }


@app.get("/admin/messaging-status")
def admin_messaging_status(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    return JSONResponse({
        "ok": True,
        "public_base_url": PUBLIC_BASE_URL,
        "messaging": messaging_config_status(),
        "notes": {
            "sms": "Requiere TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER y SMS_ENABLED=1.",
            "whatsapp": "Requiere TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM y WHATSAPP_ENABLED=1.",
            "fallback": "send_message_best_effort intenta WhatsApp primero y, si falla, SMS.",
        },
    })


@app.get("/admin/test-message")
def admin_test_message(
    token: str = "",
    phone: str = "",
    channel: str = "best_effort",
    send: int = 0,
    message: str = "",
):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    phone = (phone or "").strip()
    channel = (channel or "best_effort").strip().lower()
    message = (message or "").strip()

    if channel not in {"best_effort", "sms", "whatsapp"}:
        raise HTTPException(status_code=400, detail="channel debe ser best_effort, sms o whatsapp")

    to_phone = to_e164(phone)
    config = messaging_config_status()

    if not to_phone:
        return JSONResponse({
            "ok": False,
            "sent": False,
            "reason": "invalid_phone",
            "input_phone": phone,
            "normalized_phone": to_phone,
            "channel": channel,
            "messaging": config,
        })

    if not message:
        message = (
            "Shhh…\n\n"
            "Esto es una prueba real de ETERNA.\n\n"
            "Si recibes este mensaje, el canal de entrega está vivo."
        )

    if not bool(send):
        return JSONResponse({
            "ok": True,
            "sent": False,
            "dry_run": True,
            "reason": "dry_run_no_send",
            "input_phone": phone,
            "normalized_phone": to_phone,
            "channel": channel,
            "message_preview": message,
            "messaging": config,
            "how_to_send": "Añade &send=1 para enviar de verdad.",
        })

    print("📨 ADMIN TEST MESSAGE")
    print("➡️ channel:", channel)
    print("➡️ to:", to_phone)
    print("➡️ message:", message)

    if channel == "sms":
        result = send_sms(to_phone, message)
    elif channel == "whatsapp":
        result = send_whatsapp(to_phone, message)
    else:
        result = send_message_best_effort(to_phone, message)

    print("📨 ADMIN TEST MESSAGE RESULT:", result)

    return JSONResponse({
        "ok": bool(result.get("ok")),
        "sent": bool(result.get("ok")),
        "channel_requested": channel,
        "channel_used": result.get("channel") or ("sms" if channel == "sms" else channel),
        "sid": result.get("sid"),
        "error": result.get("error"),
        "whatsapp_error": result.get("whatsapp_error"),
        "sms_error": result.get("sms_error"),
        "input_phone": phone,
        "normalized_phone": to_phone,
        "messaging": config,
    })


@app.get("/admin/test-order-message/{order_id}")
def admin_test_order_message(
    order_id: str,
    token: str = "",
    target: str = "recipient",
    channel: str = "best_effort",
    send: int = 0,
):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    order = get_order_by_id(order_id)
    target = (target or "recipient").strip().lower()
    channel = (channel or "best_effort").strip().lower()

    if target not in {"recipient", "sender"}:
        raise HTTPException(status_code=400, detail="target debe ser recipient o sender")

    if channel not in {"best_effort", "sms", "whatsapp"}:
        raise HTTPException(status_code=400, detail="channel debe ser best_effort, sms o whatsapp")

    if target == "recipient":
        phone = order.get("recipient_phone", "")
        message = build_recipient_message(order)
    else:
        phone = order.get("sender_phone", "")
        message = build_sender_ready_message(order)

    to_phone = to_e164(phone)
    config = messaging_config_status()

    if not bool(send):
        return JSONResponse({
            "ok": True,
            "sent": False,
            "dry_run": True,
            "reason": "dry_run_no_send",
            "order_id": order_id,
            "target": target,
            "channel": channel,
            "input_phone": phone,
            "normalized_phone": to_phone,
            "message_preview": message,
            "order_flags": {
                "paid": bool(order.get("paid")),
                "video_ready": original_video_ready(order),
                "delivery_unlocked": delivery_is_unlocked(order),
                "delivery_sent": bool(order.get("delivery_sent")),
                "reaction_uploaded": bool(order.get("reaction_uploaded")),
                "reaction_exists": reaction_exists(order),
                "experience_completed": bool(order.get("experience_completed")),
            },
            "messaging": config,
            "how_to_send": "Añade &send=1 para enviar de verdad.",
        })

    if channel == "sms":
        result = send_sms(phone, message)
    elif channel == "whatsapp":
        result = send_whatsapp(phone, message)
    else:
        result = send_message_best_effort(phone, message)

    return JSONResponse({
        "ok": bool(result.get("ok")),
        "sent": bool(result.get("ok")),
        "order_id": order_id,
        "target": target,
        "channel_requested": channel,
        "channel_used": result.get("channel") or ("sms" if channel == "sms" else channel),
        "sid": result.get("sid"),
        "error": result.get("error"),
        "whatsapp_error": result.get("whatsapp_error"),
        "sms_error": result.get("sms_error"),
        "input_phone": phone,
        "normalized_phone": to_phone,
        "messaging": config,
    })




# =========================================================
# ETERNA CINEMATIC SAFE TEST ROUTES
# =========================================================

@app.get("/home-v2", response_class=HTMLResponse)
def home_v2_safe_preview(request: Request):
    """Alias seguro: muestra exactamente la misma Home azul nueva."""
    return home(request)

@app.get("/admin/debug-photos/{order_id}", response_class=HTMLResponse)
def admin_debug_photos(order_id: str, token: str = ""):
    """Muestra exactamente las 6 URLs/fotos que el main entrega al video engine. No modifica nada."""
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    order = get_order_by_id(order_id)
    cards = []
    for idx in range(1, 7):
        slot = f"photo{idx}"
        path = get_photo_asset_path(order_id, slot)
        exists = bool(path and os.path.exists(path))
        size = os.path.getsize(path) if exists else 0
        media_type = guess_media_type_from_path(path) if exists else "desconocido"
        src = f"/video/input/{order_id}/{slot}"
        absolute_src = f"{PUBLIC_BASE_URL}{src}"
        cards.append(f"""
        <article class="card">
            <div class="slot">{slot}</div>
            <img src="{src}" alt="{slot}" loading="lazy">
            <div class="meta"><strong>Existe:</strong> {'sí' if exists else 'no'}</div>
            <div class="meta"><strong>Tamaño:</strong> {size} bytes</div>
            <div class="meta"><strong>Tipo:</strong> {safe_text(media_type)}</div>
            <div class="meta"><strong>Archivo:</strong> {safe_text(os.path.basename(path or 'sin archivo'))}</div>
            <a href="{src}" target="_blank">Abrir esta foto como la recibe el motor</a>
            <textarea readonly>{safe_text(absolute_src)}</textarea>
        </article>
        """)

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Debug fotos ETERNA</title>
        <style>
            * {{ box-sizing: border-box; }}
            body {{ margin:0; background:#05070b; color:#fff7e6; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; padding:24px; }}
            h1 {{ margin:0 0 8px; font-size:30px; }}
            .sub {{ color:rgba(255,255,255,.66); margin-bottom:24px; line-height:1.6; }}
            .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:18px; }}
            .card {{ border:1px solid rgba(212,175,55,.25); background:rgba(255,255,255,.05); border-radius:22px; padding:14px; overflow:hidden; }}
            .slot {{ color:#d4af37; font-weight:800; letter-spacing:.08em; margin-bottom:10px; text-transform:uppercase; }}
            img {{ width:100%; max-height:420px; object-fit:contain; background:#000; border-radius:16px; display:block; }}
            .meta {{ font-size:13px; color:rgba(255,255,255,.72); margin-top:8px; word-break:break-word; }}
            a {{ display:block; margin-top:12px; color:#7bd6ff; }}
            textarea {{ width:100%; min-height:72px; margin-top:10px; border-radius:12px; border:1px solid rgba(255,255,255,.12); background:#02050a; color:#fff7e6; padding:10px; }}
        </style>
    </head>
    <body>
        <h1>Debug fotos ETERNA</h1>
        <div class="sub">
            Pedido: <strong>{safe_text(order_id)}</strong><br>
            Esta pantalla muestra exactamente lo que sirve <code>/video/input/order/photoX</code>, es decir, lo que descarga el video engine.
        </div>
        <div class="grid">{''.join(cards)}</div>
    </body>
    </html>
    """



# =========================================================
# RC74A — OBSERVABILITY PLUS SAFE
# Solo lectura. No cambia estados. No reintenta. No envía mensajes.
# =========================================================

def rc74a_admin_guard(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")


def rc74a_parse_dt(value):
    if not value:
        return None
    try:
        raw = str(value).replace("Z", "+00:00")
        return datetime.fromisoformat(raw)
    except Exception:
        return None


def rc74a_minutes_since(value):
    dt = rc74a_parse_dt(value)
    if not dt:
        return None
    try:
        if dt.tzinfo is None:
            now = datetime.now()
        else:
            now = datetime.now(dt.tzinfo)
        return int((now - dt).total_seconds() // 60)
    except Exception:
        return None


def rc74a_count_where(where_sql: str, params=()):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) AS c FROM orders WHERE {where_sql}", params)
    row = cur.fetchone()
    conn.close()
    return int(row["c"] if row else 0)


def rc74a_list_orders(where_sql: str, params=(), limit: int = 30):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT
            id,
            paid,
            delivered_to_recipient,
            delivery_sent,
            video_render_requested,
            video_render_requested_at,
            experience_video_url,
            experience_started,
            experience_completed,
            reaction_uploaded,
            sender_notified,
            recipient_sms_attempts,
            sender_sms_attempts,
            recipient_sms_error,
            sender_sms_error,
            created_at,
            updated_at
        FROM orders
        WHERE {where_sql}
        ORDER BY created_at DESC
        LIMIT ?
    """, tuple(params) + (int(limit),))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def rc74a_order_public_state(order: dict) -> str:
    if not order.get("paid"):
        return "CREATED_NOT_PAID"
    if not order.get("video_render_requested"):
        return "PAID_PENDING_RENDER_REQUEST"
    if order.get("video_render_requested") and not order.get("experience_video_url"):
        return "RENDERING_OR_WAITING_CALLBACK"
    if order.get("experience_video_url") and not (order.get("delivered_to_recipient") or order.get("delivery_sent")):
        return "RENDERED_NOT_DELIVERED"
    if (order.get("delivered_to_recipient") or order.get("delivery_sent")) and not order.get("experience_started"):
        return "DELIVERED_NOT_STARTED"
    if order.get("experience_started") and not order.get("experience_completed"):
        return "STARTED_NOT_COMPLETED"
    if order.get("experience_completed") and not order.get("reaction_uploaded"):
        return "COMPLETED_NO_REACTION"
    if order.get("reaction_uploaded") and not order.get("sender_notified"):
        return "REACTION_UPLOADED_SENDER_PENDING"
    if order.get("sender_notified"):
        return "SENDER_PACK_SENT"
    return "UNKNOWN"


def rc74a_queue_snapshot():
    paid_pending_render = rc74a_count_where("paid = 1 AND COALESCE(video_render_requested,0) = 0")
    rendering_waiting_callback = rc74a_count_where(
        "paid = 1 AND COALESCE(video_render_requested,0) = 1 AND (experience_video_url IS NULL OR experience_video_url = '')"
    )
    rendered_not_delivered = rc74a_count_where(
        "paid = 1 AND experience_video_url IS NOT NULL AND experience_video_url != '' AND COALESCE(delivered_to_recipient,0) = 0 AND COALESCE(delivery_sent,0) = 0"
    )
    delivered_not_started = rc74a_count_where(
        "paid = 1 AND (COALESCE(delivered_to_recipient,0) = 1 OR COALESCE(delivery_sent,0) = 1) AND COALESCE(experience_started,0) = 0"
    )
    completed_no_reaction = rc74a_count_where(
        "paid = 1 AND COALESCE(experience_completed,0) = 1 AND COALESCE(reaction_uploaded,0) = 0"
    )
    reaction_sender_pending = rc74a_count_where(
        "paid = 1 AND COALESCE(reaction_uploaded,0) = 1 AND COALESCE(sender_notified,0) = 0"
    )
    sms_errors = rc74a_count_where(
        "(recipient_sms_error IS NOT NULL AND recipient_sms_error != '') OR (sender_sms_error IS NOT NULL AND sender_sms_error != '')"
    )
    return {
        "paid_pending_render": paid_pending_render,
        "rendering_waiting_callback": rendering_waiting_callback,
        "rendered_not_delivered": rendered_not_delivered,
        "delivered_not_started": delivered_not_started,
        "completed_no_reaction": completed_no_reaction,
        "reaction_uploaded_sender_pending": reaction_sender_pending,
        "sms_errors": sms_errors,
        "total_visible_risk": (
            paid_pending_render
            + rendering_waiting_callback
            + rendered_not_delivered
            + completed_no_reaction
            + reaction_sender_pending
            + sms_errors
        ),
    }


@app.get("/admin/rc74a-queue-status")
def admin_rc74a_queue_status(token: str = ""):
    """
    Cola de pedidos en modo lectura.
    No reintenta, no envía, no cambia DB.
    Sirve para ver si hay pedidos atascados antes de automatizar nada.
    """
    rc74a_admin_guard(token)
    snapshot = rc74a_queue_snapshot()
    sample_pending = rc74a_list_orders("paid = 1 AND COALESCE(video_render_requested,0) = 0", limit=15)
    sample_rendering = rc74a_list_orders(
        "paid = 1 AND COALESCE(video_render_requested,0) = 1 AND (experience_video_url IS NULL OR experience_video_url = '')",
        limit=15,
    )

    for item in sample_pending + sample_rendering:
        item["state"] = rc74a_order_public_state(item)
        item["minutes_since_render_requested"] = rc74a_minutes_since(item.get("video_render_requested_at"))
        item["minutes_since_created"] = rc74a_minutes_since(item.get("created_at"))

    return {
        "version": "RC82_PREEXPERIENCIA_CLEAN_SAFE",
        "mode": "read_only",
        "auto_retry": False,
        "sends_messages": False,
        "queue": snapshot,
        "pending_render_sample": sample_pending,
        "rendering_waiting_callback_sample": sample_rendering,
        "principle": "Todo puede fallar. Ningún pedido puede perderse jamás.",
        "timestamp": now_iso(),
    }


@app.get("/admin/rc74a-orphans")
def admin_rc74a_orphans(token: str = ""):
    """
    Detección de pedidos huérfanos en modo lectura.
    No arregla todavía. Solo encuentra.
    """
    rc74a_admin_guard(token)

    groups = {
        "paid_without_render_request": rc74a_list_orders(
            "paid = 1 AND COALESCE(video_render_requested,0) = 0",
            limit=25,
        ),
        "render_requested_without_video": rc74a_list_orders(
            "paid = 1 AND COALESCE(video_render_requested,0) = 1 AND (experience_video_url IS NULL OR experience_video_url = '')",
            limit=25,
        ),
        "rendered_not_delivered": rc74a_list_orders(
            "paid = 1 AND experience_video_url IS NOT NULL AND experience_video_url != '' AND COALESCE(delivered_to_recipient,0) = 0 AND COALESCE(delivery_sent,0) = 0",
            limit=25,
        ),
        "completed_without_reaction": rc74a_list_orders(
            "paid = 1 AND COALESCE(experience_completed,0) = 1 AND COALESCE(reaction_uploaded,0) = 0",
            limit=25,
        ),
        "reaction_without_sender_notification": rc74a_list_orders(
            "paid = 1 AND COALESCE(reaction_uploaded,0) = 1 AND COALESCE(sender_notified,0) = 0",
            limit=25,
        ),
    }

    total = 0
    for rows in groups.values():
        total += len(rows)
        for item in rows:
            item["state"] = rc74a_order_public_state(item)
            item["minutes_since_created"] = rc74a_minutes_since(item.get("created_at"))
            item["minutes_since_render_requested"] = rc74a_minutes_since(item.get("video_render_requested_at"))

    return {
        "version": "RC82_PREEXPERIENCIA_CLEAN_SAFE",
        "mode": "read_only",
        "total_orphan_samples": total,
        "groups": groups,
        "timestamp": now_iso(),
    }


@app.get("/admin/rc74a-confidence")
def admin_rc74a_confidence(token: str = ""):
    """
    Índice simple de confianza ETERNA.
    No es perfecto: sirve para decidir si podemos lanzar o no con calma.
    """
    rc74a_admin_guard(token)

    score = 100
    reasons = []

    try:
        conn = db_conn()
        conn.execute("SELECT 1")
        conn.close()
    except Exception as e:
        score -= 30
        reasons.append(f"DB no accesible: {e}")

    if not STRIPE_SECRET_KEY:
        score -= 15
        reasons.append("Stripe secret no configurado")

    if not STRIPE_WEBHOOK_SECRET:
        score -= 10
        reasons.append("Stripe webhook secret no configurado")

    if not VIDEO_ENGINE_URL:
        score -= 20
        reasons.append("Video engine URL no configurada")

    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and (TWILIO_FROM_NUMBER or TWILIO_WHATSAPP_FROM)):
        score -= 10
        reasons.append("Twilio/SMS/WhatsApp incompleto")

    snapshot = rc74a_queue_snapshot()
    risk = int(snapshot.get("total_visible_risk", 0))
    if risk > 0:
        penalty = min(25, risk * 5)
        score -= penalty
        reasons.append(f"Hay {risk} señales de pedidos pendientes/huérfanos/errores SMS")

    missing_assets = []
    try:
        for key, filename in ETERNA_SCREEN_ASSETS.items():
            resolved = resolve_eterna_asset_filename(filename)
            path = ETERNA_BG_FOLDER / resolved
            if not path.exists():
                missing_assets.append(key)
    except Exception as e:
        score -= 10
        reasons.append(f"No se pudo auditar assets: {e}")

    if missing_assets:
        penalty = min(20, len(missing_assets) * 2)
        score -= penalty
        reasons.append(f"Assets faltantes: {', '.join(missing_assets[:8])}")

    score = max(0, min(100, int(score)))

    if score >= 90:
        status = "LISTA_PARA_PROBAR_LANZAMIENTO"
    elif score >= 75:
        status = "CASI_LISTA_REVISAR_AVISOS"
    elif score >= 50:
        status = "NO_LANZAR_AUN"
    else:
        status = "RIESGO_ALTO"

    return {
        "version": "RC82_PREEXPERIENCIA_CLEAN_SAFE",
        "confidence_score": score,
        "status": status,
        "reasons": reasons,
        "queue": snapshot,
        "missing_assets": missing_assets,
        "auto_actions_enabled": False,
        "timestamp": now_iso(),
    }


@app.get("/admin/rc74a-production-validator")
def admin_rc74a_production_validator(token: str = ""):
    """
    Página de decisión rápida: ¿está ETERNA lista hoy?
    Modo lectura. No toca flujo.
    """
    rc74a_admin_guard(token)

    confidence = admin_rc74a_confidence(token=token)
    checks = {
        "db": True,
        "stripe_secret": bool(STRIPE_SECRET_KEY),
        "stripe_webhook": bool(STRIPE_WEBHOOK_SECRET),
        "video_engine_url": bool(VIDEO_ENGINE_URL),
        "twilio_available": bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and (TWILIO_FROM_NUMBER or TWILIO_WHATSAPP_FROM)),
        "sms_enabled": bool(SMS_ENABLED),
        "whatsapp_enabled": bool(WHATSAPP_ENABLED),
        "r2_configured": bool(r2_enabled()),
        "worker_enabled": bool(DELIVERY_WORKER_ENABLED),
        "public_base_url": bool(PUBLIC_BASE_URL),
    }

    try:
        conn = db_conn()
        conn.execute("SELECT 1")
        conn.close()
    except Exception:
        checks["db"] = False

    blocking = []
    if not checks["db"]:
        blocking.append("DB no accesible")
    if not checks["stripe_secret"]:
        blocking.append("Stripe secret ausente")
    if not checks["stripe_webhook"]:
        blocking.append("Stripe webhook secret ausente")
    if not checks["video_engine_url"]:
        blocking.append("Video engine URL ausente")
    if confidence["confidence_score"] < 75:
        blocking.append("Confianza ETERNA por debajo de 75")

    decision = "NO_LANZAR_AUN" if blocking else "APTA_PARA_PRUEBA_CONTROLADA"

    return {
        "version": "RC82_PREEXPERIENCIA_CLEAN_SAFE",
        "decision": decision,
        "blocking": blocking,
        "checks": checks,
        "confidence": confidence,
        "next_safe_step": "Si todo está verde, hacer prueba completa controlada antes de abrir público.",
        "timestamp": now_iso(),
    }



# =========================================================
# MAIN
# =========================================================

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/full")
def health_full():
    result = {
        "status": "ok",
        "db": False,
        "stripe_configured": bool(STRIPE_SECRET_KEY),
        "twilio_configured": bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and (TWILIO_FROM_NUMBER or TWILIO_WHATSAPP_FROM)),
        "r2_configured": r2_enabled(),
        "video_engine_configured": bool(VIDEO_ENGINE_URL),
        "video_engine_ok": False,
        "messaging": messaging_config_status(),
        "public_base_url": PUBLIC_BASE_URL,
        "timestamp": now_iso(),
    }

    try:
        conn = db_conn()
        conn.execute("SELECT 1")
        conn.close()
        result["db"] = True
    except Exception as e:
        result["status"] = "degraded"
        result["db_error"] = str(e)

    try:
        if VIDEO_ENGINE_URL:
            response = requests.get(f"{VIDEO_ENGINE_URL}/health", timeout=2)
            result["video_engine_ok"] = bool(response.ok)
    except Exception as e:
        result["video_engine_error"] = str(e)

    critical_ok = bool(result["db"] and result["stripe_configured"] and result["video_engine_configured"])
    if not critical_ok:
        result["status"] = "degraded"

    return result


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port
    )
