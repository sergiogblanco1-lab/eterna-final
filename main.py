
# =========================================================
# RC101B_FORM_POST_NATIVE_SAFE
# Base: RC100 reacción congelada + soporte.
# AÑADE MEJORAS DE CONVERSIÓN/SOPORTE SIN TOCAR EL CORAZÓN DE ETERNA:
# - emails operativos RC95/RC96
# - security headers suaves RC96
# - rate limit ligero RC97, pero más seguro para producción
# - NO limita Stripe webhook para evitar bloquear pagos
# - NO limita chunks de reacción para evitar cortar subidas móviles
# - validación extra de archivos claramente peligrosos
# - bloque de confianza en formulario
# - /health/full ampliado
# - dashboard privado simple
# - teléfono de soporte ETERNA +34 641 63 53 14
# - email opcional del destinatario como plan B de rescate
# - selector de ocasión no invasivo
# - MEMORY ENGINE V1 silencioso: guarda momentos importantes sin enviar recordatorios
# - frases sugeridas en el formulario
# - páginas simples /como-funciona, /faq y /soporte
# - identidad opcional del remitente en llegada
# - foto de llegada opcional reutilizando una de las 6 fotos
# - bloque de confianza reforzado con soporte
# - RC101B: submit nativo multipart para evitar POST vacío en móvil/Instagram
#
# Mantiene intacto:
# Stripe Checkout, webhook de pago, SMS, WhatsApp, video engine,
# grabación, upload reacción, cámara, workers, cobros,
# Sender Pack y arquitectura separada.
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
print("🛟 RC93 SENDER PACK REACTION NO ZOOM SAFE — MAIN COMPLETO + EL UMBRAL 🛟")

print("🛟 RC93 SENDER PACK REACTION NO ZOOM SAFE — MAIN COMPLETO + ALMA YUL 🛟")
print("🛟 RC93 SENDER PACK REACTION NO ZOOM SAFE — CARPETAS BLINDADAS 🛟")
print("🛟 RC93 SENDER PACK REACTION NO ZOOM SAFE — /CREAR OK 🛟")
print("🛟 RC93 SENDER PACK REACTION NO ZOOM SAFE — TODO METIDO PARA REVISAR 🛟")
print("🛟 RC93 SENDER PACK REACTION NO ZOOM SAFE — YUL CUENTA LO QUE ESCRIBES 🛟")
print("🛟 RC93 SENDER PACK REACTION NO ZOOM SAFE — FORMULARIO SIMPLE + MAGIA 🛟")
print("🛟 RC93 SENDER PACK REACTION NO ZOOM SAFE — SOLO UN LUGAR 🛟")
print("🛟 RC93 SENDER PACK REACTION NO ZOOM SAFE — FORMULARIO LIMPIO 🛟")
print("🛟 RC93 SENDER PACK REACTION NO ZOOM SAFE — YUL NO BLOQUEA ETERNA 🛟")
print("🦋 RC101B FORM POST NATIVE SAFE — SENDER IDENTITY + TRUST 🦋")
print("🧠 MEMORY ENGINE V1 SILENT SAFE — GUARDA MOMENTOS SIN ENVIAR NADA 🧠")
print("👁️ VISITOR INTELLIGENCE V1 SAFE — LOGS HUMANOS DE VISITAS 👁️")
print("🧩 RC103 BLACKBOX + SENDER PACK NO ZOOM SAFE 🧩")
print("🦋 RC104 FOUNDER EDITION SAFE — REPORT + HEALTH + BACKUP 🦋")
print("📸 RC106 INSTAGRAM 4-6 PHOTOS SAFE — PAGO BLOQUEADO HASTA FOTOS LISTAS 📸")
print("🛡️ RC107 INSTAGRAM PREFLIGHT UPLOAD SAFE — FOTOS SUBEN ANTES DEL PAGO 🛡️")
print("🌍 RC108B INTERNATIONAL FORM CLEANUP SAFE — FORMULARIO ES/EN LIMPIO 🌍")
print("🌍 RC111 LANGUAGE SWITCH SAFE — BOTÓN ES/EN BLINDADO 🌍")
print("🌍 RC111 LANGUAGE SWITCH HARD FALLBACK — CLICK DIRECTO ES/EN 🌍")
print("🧾 RC113 FORM EN NATIVE GALLERY LOCKED SAFE — FORMULARIO EN REAL + GALERÍA NATIVA 🧾")
print("🚀 RC115 WEBHOOK RECOVERY LAUNCH SAFE — PAGO REAL → VIDEOENGINE 🛟")
print("🛟 RC116 FORM RECOVERY SAFE — VUELTA DE STRIPE SIN PERDER FORMULARIO 🛟")
import html
import json
import mimetypes
import os
import secrets
import sqlite3
import traceback
import uuid
import hashlib
import smtplib
import subprocess
import shutil
from email.message import EmailMessage
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
from fastapi.exceptions import RequestValidationError
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



@app.exception_handler(RequestValidationError)
async def eterna_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    RC101B — evita JSON técnico si /crear recibe un POST vacío o incompleto.
    No arregla datos por arte de magia: protege la experiencia y devuelve al formulario.
    """
    try:
        if request.url.path == "/crear":
            print("⚠️ RC101B /crear recibió formulario incompleto o vacío:", exc.errors())
            return HTMLResponse(
                """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ETERNA</title>
<style>
body{margin:0;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;}
.card{max-width:420px;border:1px solid rgba(245,210,139,.24);border-radius:24px;padding:24px;background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,.03));box-shadow:0 20px 80px rgba(0,0,0,.45);}
h1{font-size:22px;margin:0 0 12px;color:#f5d28b;}
p{line-height:1.55;color:rgba(255,255,255,.78);}
a{display:block;margin-top:18px;text-align:center;text-decoration:none;color:#06111d;background:#f5d28b;border-radius:999px;padding:14px 18px;font-weight:800;}
</style>
</head>
<body>
<div class="card">
<h1>Formulario incompleto / Incomplete form</h1>
<p>Vuelve a intentarlo desde el formulario. / Please try again from the form.</p>
<a href="/crear">Volver / Back to ETERNA</a>
</div>
</body>
</html>
                """,
                status_code=422,
            )
    except Exception as e:
        print("⚠️ RC101B validation handler fallback:", e)
    return JSONResponse({"detail": exc.errors()}, status_code=422)


def _client_ip_from_request(request: Request) -> str:
    forwarded = (request.headers.get("x-forwarded-for") or "").split(",")[0].strip()
    if forwarded:
        return forwarded
    return request.client.host if request.client else "unknown"


def _rate_limit_for_path(path: str) -> int:
    # RC98: conservador para no romper producción.
    # NO aplicamos límite estricto a Stripe webhook ni a chunks de reacción.
    # Stripe debe poder repetir eventos; los chunks móviles pueden venir muy seguidos.
    strict_paths = ("/crear", "/upload-reaction/", "/finish-reaction-upload/")
    if any(path.startswith(p) for p in strict_paths):
        return RATE_LIMIT_STRICT_MAX_REQUESTS
    return RATE_LIMIT_MAX_REQUESTS


# =========================================================
# VISITOR INTELLIGENCE V1 SAFE
# Logs humanos de visitas.
# No identifica personas reales ni números de teléfono.
# Usa IP pública aproximada + navegador + ruta + referrer.
# La geolocalización por IP es aproximada y puede fallar.
# =========================================================
VISITOR_LOG_ENABLED = os.getenv("VISITOR_LOG_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
VISITOR_GEO_ENABLED = os.getenv("VISITOR_GEO_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
VISITOR_GEO_TIMEOUT_SECONDS = float(os.getenv("VISITOR_GEO_TIMEOUT_SECONDS", "0.8"))
VISITOR_GEO_URL_TEMPLATE = os.getenv(
    "VISITOR_GEO_URL_TEMPLATE",
    "https://ipapi.co/{ip}/json/",
).strip()
VISITOR_LOG_FULL_IP = os.getenv("VISITOR_LOG_FULL_IP", "1").strip().lower() in {"1", "true", "yes", "on"}

_visitor_geo_cache = {}
_visitor_geo_cache_lock = threading.Lock()


def _is_private_or_internal_ip(ip: str) -> bool:
    clean = (ip or "").strip().lower()
    if not clean:
        return True
    if clean in {"unknown", "localhost", "::1", "127.0.0.1"}:
        return True
    if clean.startswith("10."):
        return True
    if clean.startswith("192.168."):
        return True
    if clean.startswith("172."):
        try:
            second = int(clean.split(".")[1])
            if 16 <= second <= 31:
                return True
        except Exception:
            pass
    return False


def _visitor_public_ip(request: Request) -> str:
    # Render suele mostrar IP interna 10.x en logs.
    # La IP pública real, cuando existe, viene en X-Forwarded-For.
    forwarded = request.headers.get("x-forwarded-for") or ""
    for item in forwarded.split(","):
        candidate = item.strip()
        if candidate and not _is_private_or_internal_ip(candidate):
            return candidate

    cf_ip = (request.headers.get("cf-connecting-ip") or "").strip()
    if cf_ip and not _is_private_or_internal_ip(cf_ip):
        return cf_ip

    real_ip = (request.headers.get("x-real-ip") or "").strip()
    if real_ip and not _is_private_or_internal_ip(real_ip):
        return real_ip

    return _client_ip_from_request(request)


def _mask_ip_for_log(ip: str) -> str:
    clean = (ip or "").strip()
    if VISITOR_LOG_FULL_IP:
        return clean or "unknown"
    parts = clean.split(".")
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.{parts[2]}.xxx"
    return clean[:10] + "…" if clean else "unknown"


def _safe_visitor_path(path: str) -> str:
    """
    Evita imprimir tokens completos en Render.
    Mantiene la ruta útil pero enmascara segmentos largos.
    """
    raw = str(path or "/").split("?")[0]
    parts = raw.split("/")
    safe_parts = []
    for part in parts:
        if len(part) >= 18:
            safe_parts.append(part[:6] + "…" + part[-4:])
        else:
            safe_parts.append(part)
    return "/".join(safe_parts) or "/"


def _visitor_device_from_user_agent(user_agent: str) -> dict:
    ua = (user_agent or "").lower()

    if "iphone" in ua:
        device = "iPhone"
    elif "ipad" in ua:
        device = "iPad"
    elif "android" in ua:
        device = "Android"
    elif "windows" in ua:
        device = "Windows"
    elif "macintosh" in ua or "mac os" in ua:
        device = "Mac"
    elif "linux" in ua:
        device = "Linux"
    else:
        device = "desconocido"

    if "edg/" in ua:
        browser = "Edge"
    elif "chrome/" in ua and "safari/" in ua:
        browser = "Chrome"
    elif "safari/" in ua and "chrome/" not in ua:
        browser = "Safari"
    elif "firefox/" in ua:
        browser = "Firefox"
    elif "instagram" in ua:
        browser = "Instagram WebView"
    elif "whatsapp" in ua:
        browser = "WhatsApp WebView"
    else:
        browser = "desconocido"

    bot_signals = ["bot", "crawler", "spider", "preview", "facebookexternalhit", "whatsapp", "telegrambot", "slurp"]
    is_bot = any(signal in ua for signal in bot_signals)

    return {
        "device": device,
        "browser": browser,
        "is_bot": is_bot,
    }


def _visitor_geo_lookup(ip: str) -> dict:
    if not VISITOR_GEO_ENABLED:
        return {}
    if not ip or _is_private_or_internal_ip(ip):
        return {"geo_note": "ip_interna_o_privada"}

    with _visitor_geo_cache_lock:
        cached = _visitor_geo_cache.get(ip)
    if cached:
        return cached

    result = {}
    try:
        url = VISITOR_GEO_URL_TEMPLATE.replace("{ip}", ip)
        response = requests.get(url, timeout=VISITOR_GEO_TIMEOUT_SECONDS)
        if response.ok:
            data = response.json()
            result = {
                "country": data.get("country_name") or data.get("country") or "",
                "region": data.get("region") or data.get("region_name") or "",
                "city": data.get("city") or "",
                "postal": data.get("postal") or data.get("zip") or "",
                "org": data.get("org") or data.get("isp") or data.get("as") or "",
                "latitude": data.get("latitude") or data.get("lat") or "",
                "longitude": data.get("longitude") or data.get("lon") or "",
            }
        else:
            result = {"geo_note": f"geo_http_{response.status_code}"}
    except Exception as e:
        result = {"geo_note": f"geo_error: {str(e)[:80]}"}

    with _visitor_geo_cache_lock:
        if len(_visitor_geo_cache) > 1000:
            _visitor_geo_cache.clear()
        _visitor_geo_cache[ip] = result

    return result


def _should_log_visitor_path(path: str) -> bool:
    clean = str(path or "/")
    skip_prefixes = (
        "/static",
        "/eterna-assets",
        "/favicon",
        "/apple-touch-icon",
        "/video/",
        "/upload-reaction-chunk",
        "/upload-reaction-live-chunk",
        "/health",
    )
    return not clean.startswith(skip_prefixes)


def log_visitor_request(request: Request, response_status_code: int = 0):
    """
    Log humano para Render.
    No bloquea ETERNA: si falla, no rompe la petición.
    """
    if not VISITOR_LOG_ENABLED:
        return

    path = request.url.path or "/"
    if not _should_log_visitor_path(path):
        return

    try:
        ip = _visitor_public_ip(request)
        ua = request.headers.get("user-agent") or ""
        referrer = request.headers.get("referer") or request.headers.get("referrer") or ""
        accept_language = request.headers.get("accept-language") or ""
        device = _visitor_device_from_user_agent(ua)
        geo = _visitor_geo_lookup(ip)

        visitor_id = hashlib.sha256(f"{ip}|{ua}".encode("utf-8", errors="ignore")).hexdigest()[:10]
        safe_path = _safe_visitor_path(path)

        country = geo.get("country") or "desconocido"
        region = geo.get("region") or "desconocido"
        city = geo.get("city") or "desconocido"
        postal = geo.get("postal") or ""
        org = geo.get("org") or "desconocido"
        geo_note = geo.get("geo_note") or ""

        print("👁️ VISITA ETERNA")
        print(f"   🕒 Hora servidor: {datetime.now().isoformat(timespec='seconds')}")
        print(f"   🆔 Visitante aprox: {visitor_id}")
        print(f"   🌍 IP pública: {_mask_ip_for_log(ip)}")
        print(f"   📍 Ubicación aprox: {city}, {region}, {country}" + (f" · CP {postal}" if postal else ""))
        print(f"   🏢 Red/operador aprox: {org}")
        print(f"   📱 Dispositivo: {device.get('device')} · Navegador: {device.get('browser')}" + (" · BOT/PREVIEW" if device.get("is_bot") else ""))
        print(f"   🗣️ Idioma navegador: {accept_language[:120] or 'desconocido'}")
        print(f"   ➡️ Ruta: {request.method} {safe_path} → {response_status_code}")
        if referrer:
            print(f"   🔗 Venía de: {referrer[:220]}")
        if geo_note:
            print(f"   📝 Geo nota: {geo_note}")
    except Exception as e:
        print("[WARN] Visitor log no pudo escribirse:", e)


@app.middleware("http")
async def eterna_security_headers_and_light_rate_limit(request: Request, call_next):
    """
    RC99 — seguridad ligera combinada + soporte de lanzamiento.
    No lee ni modifica el body. No toca el flujo de ETERNA.
    """
    path = request.url.path or "/"

    if RATE_LIMIT_ENABLED and not path.startswith((
        "/static",
        "/eterna-assets",
        "/favicon",
        "/apple-touch-icon",
        "/stripe/webhook",              # no bloquear reintentos reales de Stripe
        "/upload-reaction-chunk",       # no cortar subidas por chunks
        "/upload-reaction-live-chunk",  # no cortar subidas móviles en vivo
    )):
        now = int(time.time())
        window = max(10, RATE_LIMIT_WINDOW_SECONDS)
        bucket = now // window
        ip = _client_ip_from_request(request)
        key = (ip, path, bucket)
        max_requests = max(5, _rate_limit_for_path(path))
        try:
            with _rate_limit_lock:
                # Limpieza pequeña para no crecer indefinidamente.
                if len(_rate_limit_bucket) > 8000:
                    old_keys = [k for k in _rate_limit_bucket.keys() if k[2] < bucket - 2]
                    for k in old_keys[:4000]:
                        _rate_limit_bucket.pop(k, None)
                count = _rate_limit_bucket.get(key, 0) + 1
                _rate_limit_bucket[key] = count
            if count > max_requests:
                return JSONResponse({"ok": False, "detail": "too_many_requests"}, status_code=429)
        except Exception as e:
            # Si el rate limit fallase, no rompe ETERNA.
            print("[WARN] Rate limit bypass por error:", e)

    response = await call_next(request)

    try:
        log_visitor_request(request, getattr(response, "status_code", 0))
    except Exception as e:
        print("[WARN] Visitor Intelligence fallback:", e)

    if SECURITY_HEADERS_ENABLED:
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "geolocation=(), payment=(self), camera=(self), microphone=(self)")
        if PUBLIC_BASE_URL.startswith("https://"):
            response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        # CSP suave para no romper inline styles/scripts actuales de ETERNA.
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self' https: data: blob:; "
            "img-src 'self' https: data: blob:; "
            "media-src 'self' https: data: blob:; "
            "script-src 'self' 'unsafe-inline' https:; "
            "style-src 'self' 'unsafe-inline' https:; "
            "connect-src 'self' https: blob:; "
            "frame-ancestors 'self';"
        )

    return response


# =========================================================
# RC115 — SAFE ENV MONEY PARSER
# Acepta 0.50 y 0,50 para evitar caídas de Render por variables españolas.
# =========================================================
def env_float(name: str, default: str = "0") -> float:
    raw = os.getenv(name, str(default))
    try:
        clean = str(raw or default).strip().replace("€", "").replace(" ", "").replace(",", ".")
        return float(clean)
    except Exception as e:
        print(f"[WARN] ENV_FLOAT inválido {name}={raw!r}; usando {default}: {e}")
        return float(str(default).replace(",", "."))

# =========================================================
# CONFIG
# =========================================================

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "").strip()
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "").strip()
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "").strip()
ADMIN_ALERT_PHONE = os.getenv("ADMIN_ALERT_PHONE", "").strip()

# RC111 — Lanzamiento seguro:
# En producción NO permitimos crear pedidos pagados sin Stripe.
# Solo para pruebas locales/controladas se puede activar ETERNA_ALLOW_NO_STRIPE_TEST=1.
ETERNA_ALLOW_NO_STRIPE_TEST = os.getenv("ETERNA_ALLOW_NO_STRIPE_TEST", "0").strip().lower() in {"1", "true", "yes", "on"}

# =========================================================
# RC95 — EMAIL CORPORATIVO / PEDIDOS / ALERTAS
# Config recomendado Namecheap Private Email:
# SMTP_HOST=mail.privateemail.com
# SMTP_PORT=587
# SMTP_USER=hola@tueterna.com
# SMTP_PASSWORD=<contraseña del buzón>
# SMTP_FROM=hola@tueterna.com
# EMAIL_ENABLED=1
# ADMIN_ALERT_EMAIL=sergiog.blanco1@gmail.com
# ETERNA_OPERATIONS_EMAIL=hola@tueterna.com
# =========================================================
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
SMTP_HOST = os.getenv("SMTP_HOST", "mail.privateemail.com").strip()
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "").strip()
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").strip()
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER or "hola@tueterna.com").strip()
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "ETERNA").strip()
ADMIN_ALERT_EMAIL = os.getenv("ADMIN_ALERT_EMAIL", "sergiog.blanco1@gmail.com").strip()
ETERNA_OPERATIONS_EMAIL = os.getenv("ETERNA_OPERATIONS_EMAIL", SMTP_FROM or "hola@tueterna.com").strip()

# =========================================================
# RC99 — SOPORTE / CONFIANZA / CONVERSIÓN
# =========================================================
ETERNA_SUPPORT_EMAIL = os.getenv("ETERNA_SUPPORT_EMAIL", "hola@tueterna.com").strip()
ETERNA_SUPPORT_PHONE = os.getenv("ETERNA_SUPPORT_PHONE", "+34 641 63 53 14").strip()

# =========================================================
# MEMORY ENGINE V1 — MODO SILENCIOSO
# Guarda momentos importantes desde cada pedido.
# No envía recordatorios, no campañas, no SMS, no WhatsApp.
# =========================================================
MEMORY_ENGINE_ENABLED = os.getenv("MEMORY_ENGINE_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
MEMORY_REMINDERS_ENABLED = os.getenv("MEMORY_REMINDERS_ENABLED", "0").strip().lower() in {"1", "true", "yes", "on"}

# =========================================================
# RC101 — IDENTIDAD OPCIONAL DEL REMITENTE
# Mejora de confianza: permite mostrar quién envía la ETERNA
# usando una de las 6 fotos ya subidas. No añade nuevas subidas.
# =========================================================
SENDER_IDENTITY_ENABLED = os.getenv("SENDER_IDENTITY_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
ARRIVAL_PHOTO_DEFAULT_SLOT = os.getenv("ARRIVAL_PHOTO_DEFAULT_SLOT", "photo1").strip() or "photo1"

# =========================================================
# RC98 — SEGURIDAD LIGERA COMBINADA PARA LANZAMIENTO
# No toca lógica de Stripe, Twilio, vídeo, reacción ni Sender Pack.
# =========================================================
SECURITY_HEADERS_ENABLED = os.getenv("SECURITY_HEADERS_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "120"))
RATE_LIMIT_STRICT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_STRICT_MAX_REQUESTS", "30"))
MAX_PHOTO_SIZE_MB = int(os.getenv("MAX_PHOTO_SIZE_MB", "15"))
MAX_PHOTO_SIZE = MAX_PHOTO_SIZE_MB * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "heic", "heif"}
ALLOWED_IMAGE_MIME_PREFIXES = {"image/"}
BLOCKED_UPLOAD_EXTENSIONS = {"exe", "php", "js", "bat", "cmd", "sh", "ps1", "html", "htm", "svg", "zip", "rar", "7z"}
_rate_limit_bucket = {}
_rate_limit_lock = threading.Lock()

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

BASE_PRICE = env_float("ETERNA_BASE_PRICE", "29")
CURRENCY = os.getenv("ETERNA_CURRENCY", "eur").strip().lower()

GIFT_COMMISSION_RATE = env_float("GIFT_COMMISSION_RATE", "0.05")
FIXED_PLATFORM_FEE = env_float("ETERNA_FIXED_FEE", "2")

SCHEDULED_DELIVERY_FEE = env_float("SCHEDULED_DELIVERY_FEE", "2")
GIFT_REFUND_DAYS = int(os.getenv("GIFT_REFUND_DAYS", "20"))

# RC60: controles seguros de estabilización.
# Por defecto NO caducamos enlaces para no romper pruebas actuales.
# Cuando lancemos público, poner ETERNA_LINK_EXPIRY_DAYS=30 y ETERNA_ENFORCE_LINK_EXPIRY=1.
ETERNA_LINK_EXPIRY_DAYS = int(os.getenv("ETERNA_LINK_EXPIRY_DAYS", "30"))
ETERNA_ENFORCE_LINK_EXPIRY = os.getenv("ETERNA_ENFORCE_LINK_EXPIRY", "0").strip().lower() in {"1", "true", "yes", "on"}

# RC60: sweep de rescate al arrancar Render. Seguro porque respeta locks, delivered y máximos de intentos.
ETERNA_STARTUP_SWEEP_ENABLED = os.getenv("ETERNA_STARTUP_SWEEP_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}


# =========================================================
# R2 STORAGE — ALIASES SAFE
# Acepta los nombres clásicos y los nombres habituales de Cloudflare/S3.
# IMPORTANTE: R2_API_TOKEN NO sirve como S3 secret para boto3; se conserva
# solo para diagnóstico. Para subir objetos hacen falta Access Key ID + Secret.
# =========================================================
def _env_first(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return ""

R2_ACCESS_KEY = _env_first(
    "R2_ACCESS_KEY",
    "R2_ACCESS_KEY_ID",
    "R2_ACCESS_KEYID",
    "AWS_ACCESS_KEY_ID",
)
R2_SECRET_KEY = _env_first(
    "R2_SECRET_KEY",
    "R2_SECRET_ACCESS_KEY",
    "R2_SECRET_ACCESSKEY",
    "AWS_SECRET_ACCESS_KEY",
)
R2_API_TOKEN = os.getenv("R2_API_TOKEN", "").strip()
R2_BUCKET = _env_first("R2_BUCKET", "R2_BUCKET_NAME")
R2_ENDPOINT = _env_first("R2_ENDPOINT", "R2_S3_ENDPOINT", "R2_ENDPOINT_URL").rstrip("/")
R2_PUBLIC_URL = _env_first(
    "R2_PUBLIC_URL",
    "R2_PUBLIC_BASE_URL",
    "R2_CUSTOM_DOMAIN",
    "R2_DEV_URL",
).rstrip("/")

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
# RC100 — BLINDAJE REACCIÓN CONGELADA
# Diagnóstico + validación + normalización segura antes del Sender Pack.
# No toca Stripe, webhook, Twilio/SMS, WhatsApp ni video engine principal.
# =========================================================
REACTION_NORMALIZE_ENABLED = os.getenv("REACTION_NORMALIZE_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
REACTION_FFPROBE_ENABLED = os.getenv("REACTION_FFPROBE_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
REACTION_MAX_DURATION_SECONDS = int(os.getenv("REACTION_MAX_DURATION_SECONDS", "180"))
REACTION_NORMALIZED_MAX_WIDTH = int(os.getenv("REACTION_NORMALIZED_MAX_WIDTH", "720"))
REACTION_NORMALIZED_MAX_HEIGHT = int(os.getenv("REACTION_NORMALIZED_MAX_HEIGHT", "1280"))
REACTION_NORMALIZED_FPS = int(os.getenv("REACTION_NORMALIZED_FPS", "25"))
REACTION_MIN_VALID_SECONDS = float(os.getenv("REACTION_MIN_VALID_SECONDS", "1"))
REACTION_MIN_VALID_BYTES = int(os.getenv("REACTION_MIN_VALID_BYTES", "4096"))


# =========================================================
# RC111 — DB PERSISTENT SAFE
# Mantiene RC111 como versión de lanzamiento, pero endurece la persistencia.
# Prioridad en Render: /data/eterna.db o DATABASE_PATH explícito.
# Si /data no existe o no tiene permisos, ETERNA no se cae: vuelve a ./data.
# Además, si existe una DB antigua en ./data/eterna.db y la nueva DB aún no
# existe, la copia una sola vez como rescate seguro.
# =========================================================

def ensure_base_data_folder(path_value: str = "") -> Path:
    requested = Path(str(path_value or "").strip() or "/data")
    try:
        requested.mkdir(parents=True, exist_ok=True)
        test_file = requested / ".eterna_write_test"
        test_file.write_text("ok", encoding="utf-8")
        try:
            test_file.unlink()
        except Exception:
            pass
        print(f"🗄️ DATA_FOLDER activo: {requested}")
        return requested
    except Exception as e:
        fallback = Path("data")
        fallback.mkdir(parents=True, exist_ok=True)
        print(f"[WARN] DATA_FOLDER fallback: {requested} -> {fallback} ({e})")
        return fallback


DATA_FOLDER = ensure_base_data_folder(os.getenv("DATA_FOLDER", "/data"))


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


def resolve_db_path() -> Path:
    configured = os.getenv("DATABASE_PATH", "").strip()
    requested = Path(configured) if configured else (DATA_FOLDER / "eterna.db")
    try:
        requested.parent.mkdir(parents=True, exist_ok=True)
        legacy = Path("data") / "eterna.db"
        if legacy.exists() and legacy.resolve() != requested.resolve() and not requested.exists():
            try:
                shutil.copy2(legacy, requested)
                print(f"🛟 DB rescue: copiada DB antigua {legacy} -> {requested}")
            except Exception as copy_error:
                print(f"[WARN] DB rescue no pudo copiar {legacy} -> {requested}: {copy_error}")
        print(f"🗄️ DB_PATH activo: {requested}")
        return requested
    except Exception as e:
        fallback = Path("data") / "eterna.db"
        fallback.parent.mkdir(parents=True, exist_ok=True)
        print(f"[WARN] DB_PATH fallback: {requested} -> {fallback} ({e})")
        return fallback


VIDEO_FOLDER = Path("videos")
VIDEO_FOLDER.mkdir(parents=True, exist_ok=True)

REACTIONS_FOLDER = ensure_runtime_folder(os.getenv("REACTIONS_FOLDER", str(DATA_FOLDER / "reactions")), "reactions")
REACTION_CHUNKS_FOLDER = ensure_runtime_folder(os.getenv("REACTION_CHUNKS_FOLDER", str(DATA_FOLDER / "reaction_chunks")), "reaction_chunks")
PREUPLOAD_FOLDER = ensure_runtime_folder(os.getenv("PREUPLOAD_FOLDER", str(DATA_FOLDER / "preuploads")), "preuploads")

STATIC_FOLDER = Path("static")
STATIC_FOLDER.mkdir(parents=True, exist_ok=True)

PHOTO_FOLDER = Path("uploads")
PHOTO_FOLDER.mkdir(parents=True, exist_ok=True)

DB_PATH = resolve_db_path()

DELIVERY_WORKER_INTERVAL_SECONDS = int(os.getenv("DELIVERY_WORKER_INTERVAL_SECONDS", "15"))
DELIVERY_WORKER_ENABLED = os.getenv("DELIVERY_WORKER_ENABLED", "1").strip() != "0"
DELIVERY_WORKER_STARTED = False
DELIVERY_WORKER_LOCK = threading.Lock()

# =========================================================
# RC74 FULL — AUTONOMÍA OPERATIVA
# =========================================================
ETERNA_APP_VERSION = os.getenv("ETERNA_APP_VERSION", "RC116_FORM_RECOVERY_SAFE").strip()
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
    object-fit:contain !important;
    object-position:center center !important;
    transform:none !important;
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
    add_column_if_missing("orders", "language", "ALTER TABLE orders ADD COLUMN language TEXT NOT NULL DEFAULT 'es'")

    # RC101 — identidad opcional del remitente para aumentar confianza de apertura.
    add_column_if_missing("orders", "show_sender_identity", "ALTER TABLE orders ADD COLUMN show_sender_identity INTEGER NOT NULL DEFAULT 0")
    add_column_if_missing("orders", "arrival_photo_slot", "ALTER TABLE orders ADD COLUMN arrival_photo_slot TEXT")
    add_column_if_missing("orders", "arrival_photo_url", "ALTER TABLE orders ADD COLUMN arrival_photo_url TEXT")

    # RC100 — diagnóstico y normalización segura de reacciones.
    # Campos añadidos de forma compatible: si ya existen, no hace nada.
    add_column_if_missing("orders", "reaction_video_original_local", "ALTER TABLE orders ADD COLUMN reaction_video_original_local TEXT")
    add_column_if_missing("orders", "reaction_video_normalized_local", "ALTER TABLE orders ADD COLUMN reaction_video_normalized_local TEXT")
    add_column_if_missing("orders", "reaction_validation_status", "ALTER TABLE orders ADD COLUMN reaction_validation_status TEXT")
    add_column_if_missing("orders", "reaction_validation_error", "ALTER TABLE orders ADD COLUMN reaction_validation_error TEXT")
    add_column_if_missing("orders", "reaction_normalized_at", "ALTER TABLE orders ADD COLUMN reaction_normalized_at TEXT")
    add_column_if_missing("orders", "reaction_probe_json", "ALTER TABLE orders ADD COLUMN reaction_probe_json TEXT")

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

    # RC95 — email pedidos + alertas. Idempotente para no duplicar correos en reintentos de Stripe/Render.
    add_column_if_missing("orders", "order_email_customer_sent_at", "ALTER TABLE orders ADD COLUMN order_email_customer_sent_at TEXT")
    add_column_if_missing("orders", "order_email_admin_sent_at", "ALTER TABLE orders ADD COLUMN order_email_admin_sent_at TEXT")
    add_column_if_missing("orders", "order_email_last_error", "ALTER TABLE orders ADD COLUMN order_email_last_error TEXT")
    add_column_if_missing("orders", "admin_alert_last_sent_at", "ALTER TABLE orders ADD COLUMN admin_alert_last_sent_at TEXT")
    add_column_if_missing("orders", "admin_alert_last_reason", "ALTER TABLE orders ADD COLUMN admin_alert_last_reason TEXT")

    # RC99 — conversión/soporte. Campos opcionales; no rompen pedidos antiguos.
    add_column_if_missing("recipients", "email", "ALTER TABLE recipients ADD COLUMN email TEXT")
    add_column_if_missing("orders", "occasion_type", "ALTER TABLE orders ADD COLUMN occasion_type TEXT")
def init_memory_engine():
    """
    MEMORY ENGINE V1 — SILENT SAFE.
    Crea una tabla separada para no contaminar orders ni tocar Stripe/Twilio/vídeo.
    Solo guarda memoria. No envía recordatorios.
    """
    if not MEMORY_ENGINE_ENABLED:
        print("🧠 Memory Engine V1 desactivado por configuración")
        return

    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS memory_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL UNIQUE,
            sender_id INTEGER,
            recipient_id INTEGER,
            sender_name TEXT,
            sender_email TEXT,
            sender_phone TEXT,
            recipient_name TEXT,
            recipient_email TEXT,
            recipient_phone TEXT,
            occasion_type TEXT,
            occasion_date TEXT,
            delivery_mode TEXT,
            scheduled_delivery_at TEXT,
            marketing_opt_in INTEGER NOT NULL DEFAULT 0,
            last_reminder_sent TEXT,
            memory_created_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            meta_json TEXT,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(sender_id) REFERENCES senders(id),
            FOREIGN KEY(recipient_id) REFERENCES recipients(id)
        )
        """)

        cur.execute("CREATE INDEX IF NOT EXISTS idx_memory_events_sender_phone ON memory_events(sender_phone)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_memory_events_sender_email ON memory_events(sender_email)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_memory_events_recipient_name ON memory_events(recipient_name)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_memory_events_occasion_date ON memory_events(occasion_date)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_memory_events_occasion_type ON memory_events(occasion_type)")

        conn.commit()
        conn.close()
        print("🧠 Memory Engine V1 listo: tabla memory_events activa")
    except Exception as e:
        print("[WARN] Memory Engine V1 no pudo inicializarse:", e)


init_db()
init_memory_engine()



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


def upload_extension_from_filename(filename: str) -> str:
    raw = (filename or "").strip().lower().split("?")[0].split("#")[0]
    if "." not in raw:
        return ""
    return raw.rsplit(".", 1)[-1].strip()


def validate_upload_metadata_safe(upload: UploadFile, kind: str, slot_name: str = "archivo") -> None:
    """
    RC98 — filtro ligero previo.
    No transforma archivos. Solo rechaza nombres/tipos claramente peligrosos.
    """
    filename = (upload.filename or "").strip()
    content_type = (upload.content_type or "").lower().strip()
    ext = upload_extension_from_filename(filename)

    if not filename:
        raise HTTPException(status_code=400, detail=f"{slot_name} no tiene nombre de archivo")

    if ext in BLOCKED_UPLOAD_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"{slot_name} tiene un formato no permitido")

    lowered = filename.lower()
    dangerous_fragments = [".php", ".exe", ".js", ".bat", ".cmd", ".sh", ".ps1", "<", ">", ".."]
    if any(fragment in lowered for fragment in dangerous_fragments):
        raise HTTPException(status_code=400, detail=f"{slot_name} tiene un nombre no permitido")

    if kind == "image":
        if ext and ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"{slot_name} debe ser una imagen válida")
        if content_type and not any(content_type.startswith(prefix) for prefix in ALLOWED_IMAGE_MIME_PREFIXES):
            # Algunos navegadores mandan application/octet-stream; lo permitimos y luego validamos firma.
            if content_type != "application/octet-stream":
                raise HTTPException(status_code=400, detail=f"{slot_name} no parece una imagen")
    elif kind == "video":
        if ext and ext not in {"mp4", "webm", "mov"}:
            raise HTTPException(status_code=400, detail=f"{slot_name} debe ser vídeo mp4 o webm")
        if content_type and content_type not in ALLOWED_VIDEO_TYPES and not content_type.startswith("video/"):
            raise HTTPException(status_code=400, detail=f"{slot_name} no parece un vídeo")


def validate_reaction_signature_safe(local_path: str, extension: str) -> bool:
    try:
        with open(local_path, "rb") as f:
            head = f.read(64)
        ext = (extension or "").lower().strip()
        if ext == "mp4":
            return b"ftyp" in head[:32] or head.startswith(b"\x00\x00\x00")
        if ext == "webm":
            return head.startswith(b"\x1a\x45\xdf\xa3") or b"webm" in head.lower()[:64]
        return True
    except Exception:
        return True


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

    validate_upload_metadata_safe(upload, "image", slot_name)

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
    if size > MAX_PHOTO_SIZE:
        try:
            os.remove(filepath)
        except Exception:
            pass
        raise HTTPException(status_code=400, detail=f"{slot_name} supera el tamaño máximo permitido")

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


# =========================================================
# RC107 — INSTAGRAM PREFLIGHT UPLOAD SAFE
# Las fotos se suben antes de abrir Stripe.
# El POST final /crear ya no depende de que Instagram WebView mande 4-6 archivos.
# =========================================================
ALLOWED_CREATE_PHOTO_SLOTS = {"photo1", "photo2", "photo3", "photo4", "photo5", "photo6"}


def _safe_preupload_session(value: str) -> str:
    raw = str(value or "").strip()
    safe = "".join(ch for ch in raw if ch.isalnum() or ch in {"_", "-"})
    return safe[:80] or secrets.token_urlsafe(18)


def preupload_session_folder(session_id: str) -> Path:
    clean = _safe_preupload_session(session_id)
    folder = PREUPLOAD_FOLDER / clean
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def find_preuploaded_photo(session_id: str, slot_name: str) -> Optional[str]:
    if not session_id or slot_name not in ALLOWED_CREATE_PHOTO_SLOTS:
        return None
    folder = preupload_session_folder(session_id)
    for ext in ("jpg", "jpeg", "png", "webp", "heic", "heif"):
        candidate = folder / f"{slot_name}.{ext}"
        if candidate.exists() and candidate.is_file() and candidate.stat().st_size > 0:
            return str(candidate)
    return None


def list_preuploaded_photos(session_id: str) -> dict:
    result = {}
    for slot in sorted(ALLOWED_CREATE_PHOTO_SLOTS):
        found = find_preuploaded_photo(session_id, slot)
        if found:
            result[slot] = found
    return result


async def save_preupload_photo(session_id: str, slot_name: str, upload: UploadFile) -> str:
    if slot_name not in ALLOWED_CREATE_PHOTO_SLOTS:
        raise HTTPException(status_code=400, detail="Slot de foto no válido")
    if not upload or not getattr(upload, "filename", ""):
        raise HTTPException(status_code=400, detail="No ha llegado la foto")

    validate_upload_metadata_safe(upload, "image", slot_name)

    ext = detect_image_extension(upload)
    folder = preupload_session_folder(session_id)
    filepath = folder / f"{slot_name}.{ext}"

    for old_ext in ("jpg", "jpeg", "png", "webp", "heic", "heif"):
        old = folder / f"{slot_name}.{old_ext}"
        if old.exists() and old != filepath:
            try:
                old.unlink()
            except Exception:
                pass

    try:
        await upload.seek(0)
    except Exception:
        try:
            upload.file.seek(0)
        except Exception:
            pass

    total = 0
    with open(filepath, "wb") as f:
        while True:
            chunk = await upload.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
            total += len(chunk)
        try:
            f.flush()
            os.fsync(f.fileno())
        except Exception:
            pass

    if total <= 0 or not filepath.exists() or filepath.stat().st_size <= 0:
        try:
            filepath.unlink()
        except Exception:
            pass
        raise HTTPException(status_code=400, detail=f"{slot_name} llegó vacía desde el navegador")

    if filepath.stat().st_size > MAX_PHOTO_SIZE:
        try:
            filepath.unlink()
        except Exception:
            pass
        raise HTTPException(status_code=400, detail=f"{slot_name} supera el tamaño máximo")

    with open(filepath, "rb") as f:
        head = f.read(32)

    looks_like_image = (
        head.startswith(b"\xff\xd8\xff") or
        head.startswith(b"\x89PNG\r\n\x1a\n") or
        head.startswith(b"RIFF") or
        b"ftypheic" in head or b"ftypheif" in head or b"ftypmif1" in head
    )
    if not looks_like_image:
        try:
            filepath.unlink()
        except Exception:
            pass
        raise HTTPException(status_code=400, detail=f"{slot_name} no parece una imagen válida")

    return str(filepath)


@app.post("/preupload-photo")
async def preupload_photo(
    photo_upload_session: str = Form(""),
    slot: str = Form(...),
    photo: UploadFile = File(...),
):
    session_id = _safe_preupload_session(photo_upload_session)
    slot = (slot or "").strip()
    try:
        filepath = await save_preupload_photo(session_id, slot, photo)
        size = os.path.getsize(filepath)
        print("📸 RC107 preupload OK", {"session": session_id[:10], "slot": slot, "size": size})
        return {"ok": True, "photo_upload_session": session_id, "slot": slot, "size": size}
    except HTTPException:
        raise
    except Exception as e:
        print("❌ RC107 preupload error", slot, e)
        raise HTTPException(status_code=500, detail=f"No se pudo subir {slot}: {e}")
    finally:
        try:
            await photo.close()
        except Exception:
            pass



def reaction_video_path(order_id: str, extension: str = "webm") -> str:
    extension = (extension or "webm").lower().strip()
    if extension not in {"webm", "mp4"}:
        extension = "webm"
    REACTIONS_FOLDER.mkdir(parents=True, exist_ok=True)
    return str(REACTIONS_FOLDER / f"reaction_{order_id}.{extension}")


def reaction_normalized_video_path(order_id: str) -> str:
    REACTIONS_FOLDER.mkdir(parents=True, exist_ok=True)
    return str(REACTIONS_FOLDER / f"reaction_{order_id}_normalized.mp4")


def _safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _fps_from_ffprobe_rate(value: str) -> float:
    raw = str(value or "").strip()
    if not raw or raw == "0/0":
        return 0.0
    if "/" in raw:
        try:
            a, b = raw.split("/", 1)
            b_float = float(b)
            return float(a) / b_float if b_float else 0.0
        except Exception:
            return 0.0
    return _safe_float(raw, 0.0)


def reaction_ffprobe_available() -> bool:
    return bool(REACTION_FFPROBE_ENABLED and shutil.which("ffprobe"))


def reaction_ffmpeg_available() -> bool:
    return bool(shutil.which("ffmpeg"))


def probe_reaction_video(local_path: str, order_id: str = "") -> dict:
    """
    RC100 — lee metadatos reales con ffprobe si está disponible.
    Nunca rompe ETERNA por sí solo: devuelve dict con ok/error.
    """
    info = {
        "ok": False,
        "ffprobe_available": reaction_ffprobe_available(),
        "path": local_path,
        "exists": bool(local_path and os.path.exists(local_path)),
        "bytes": 0,
        "duration": 0.0,
        "width": None,
        "height": None,
        "fps": 0.0,
        "video_codec": None,
        "audio_codec": None,
        "has_video": False,
        "has_audio": False,
        "format_name": None,
        "error": None,
    }

    try:
        if not local_path or not os.path.exists(local_path):
            info["error"] = "reaction_file_missing"
            return info

        info["bytes"] = os.path.getsize(local_path)
        if info["bytes"] <= 0:
            info["error"] = "reaction_file_empty"
            return info

        if not reaction_ffprobe_available():
            info["ok"] = True
            info["error"] = "ffprobe_not_available_basic_size_only"
            return info

        cmd = [
            "ffprobe",
            "-v", "error",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            local_path,
        ]
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
        if completed.returncode != 0:
            info["error"] = (completed.stderr or completed.stdout or "ffprobe_failed").strip()[:2000]
            return info

        raw = json.loads(completed.stdout or "{}")
        fmt = raw.get("format") or {}
        streams = raw.get("streams") or []
        info["format_name"] = fmt.get("format_name")
        info["duration"] = _safe_float(fmt.get("duration"), 0.0)

        for stream in streams:
            codec_type = (stream.get("codec_type") or "").lower()
            if codec_type == "video" and not info["has_video"]:
                info["has_video"] = True
                info["video_codec"] = stream.get("codec_name")
                info["width"] = stream.get("width")
                info["height"] = stream.get("height")
                info["fps"] = _fps_from_ffprobe_rate(stream.get("avg_frame_rate") or stream.get("r_frame_rate"))
                if not info["duration"]:
                    info["duration"] = _safe_float(stream.get("duration"), 0.0)
            elif codec_type == "audio" and not info["has_audio"]:
                info["has_audio"] = True
                info["audio_codec"] = stream.get("codec_name")

        info["raw_stream_count"] = len(streams)
        info["ok"] = True
        return info

    except Exception as e:
        info["error"] = str(e)
        return info


def validate_reaction_video_file(local_path: str, order: dict, mime_type: str = "", source: str = "") -> tuple[bool, dict]:
    """
    RC100 — validación básica real de la reacción antes de marcarla como subida.
    Si ffprobe está disponible exige stream de vídeo y duración válida.
    """
    order_id = (order or {}).get("id") or ""
    probe = probe_reaction_video(local_path, order_id=order_id)
    probe["mime_type"] = mime_type or ""
    probe["source"] = source or ""

    if not probe.get("exists"):
        probe["validation_error"] = "reaction_file_missing"
        return False, probe

    if int(probe.get("bytes") or 0) <= 0:
        probe["validation_error"] = "reaction_file_empty"
        return False, probe

    if int(probe.get("bytes") or 0) < int(REACTION_MIN_VALID_BYTES or 0):
        probe["validation_error"] = "reaction_file_too_small"
        return False, probe

    if int(probe.get("bytes") or 0) > int(MAX_VIDEO_SIZE or 0):
        probe["validation_error"] = "reaction_file_too_large"
        return False, probe

    # Sin ffprobe no inventamos: permitimos pasar con tamaño/firma, pero dejamos log claro.
    if not probe.get("ffprobe_available"):
        probe["validation_warning"] = "ffprobe_not_available"
        return True, probe

    if not probe.get("ok"):
        probe["validation_error"] = probe.get("error") or "ffprobe_failed"
        return False, probe

    if not probe.get("has_video"):
        probe["validation_error"] = "reaction_has_no_video_stream"
        return False, probe

    duration = float(probe.get("duration") or 0.0)
    if duration < float(REACTION_MIN_VALID_SECONDS or 1):
        probe["validation_error"] = "reaction_duration_too_short"
        return False, probe

    if int(REACTION_MAX_DURATION_SECONDS or 0) > 0 and duration > int(REACTION_MAX_DURATION_SECONDS):
        probe["validation_error"] = "reaction_duration_too_long"
        return False, probe

    return True, probe


def build_reaction_invalid_alert_body(order: dict, probe: dict, original_path: str = "", normalized_path: str = "") -> str:
    sender_url = sender_pack_url_from_order(order) if order else ""
    recipient_url = recipient_experience_url_from_order(order) if order else ""
    return f"""🚨 ETERNA — Reacción inválida o no normalizable

Pedido: {order_public_code(order)}
Order ID: {order.get('id') if order else 'sin order_id'}
Hora: {now_iso()}

ARCHIVO
Ruta original: {original_path or probe.get('path') or 'sin ruta'}
Ruta normalizada: {normalized_path or 'no generada'}
URL pública actual: {order.get('reaction_video_public_url') if order else ''}

DIAGNÓSTICO
Estado: {probe.get('validation_error') or probe.get('normalization_error') or probe.get('error') or 'sin detalle'}
Bytes: {probe.get('bytes')}
MIME recibido: {probe.get('mime_type') or 'desconocido'}
Duración: {probe.get('duration')}
Resolución: {probe.get('width')}x{probe.get('height')}
FPS: {probe.get('fps')}
Codec vídeo: {probe.get('video_codec')}
Codec audio: {probe.get('audio_codec')}
Tiene vídeo: {probe.get('has_video')}
Tiene audio: {probe.get('has_audio')}
ffprobe disponible: {probe.get('ffprobe_available')}

ENLACES DE RESCATE
Link regalado: {recipient_url}
Link regalante: {sender_url}

ACCIÓN RECOMENDADA
No se debe enviar un Sender Pack roto.
Permitir repetir reacción o rescatar manualmente con un vídeo alternativo.
""".strip()


def mark_reaction_invalid(order: dict, probe: dict, reason: str, original_path: str = "", normalized_path: str = "") -> None:
    """RC100 — deja el pedido sin Sender Pack roto y avisa a Sergio/operaciones."""
    order_id = order.get("id")
    error_text = str(reason or probe.get("validation_error") or probe.get("error") or "reaction_invalid")[:1000]
    try:
        update_order(
            order_id,
            reaction_uploaded=0,
            experience_completed=0,
            eterna_completed=0,
            reaction_upload_pending=0,
            reaction_upload_error=error_text,
            reaction_video_original_local=original_path or probe.get("path"),
            reaction_video_normalized_local=normalized_path or None,
            reaction_validation_status="invalid",
            reaction_validation_error=error_text,
            reaction_probe_json=json.dumps(probe or {}, ensure_ascii=False)[:12000],
        )
    except Exception as e:
        print("[WARN] RC100 no pudo marcar reaction_invalid:", e)

    try:
        insert_order_event(
            order_id,
            "❌ rc100_reaction_invalid",
            "error",
            error_text,
            {
                "path": original_path or probe.get("path"),
                "normalized_path": normalized_path,
                "probe": probe,
            },
        )
    except Exception as e:
        print("[WARN] RC100 no pudo insertar evento invalid:", e)

    try:
        send_admin_error_email(
            "⚠️ ETERNA — Reacción inválida o no normalizable",
            build_reaction_invalid_alert_body(order, probe, original_path=original_path, normalized_path=normalized_path),
            order_id=order_id,
            reason=error_text,
        )
    except Exception as e:
        print("[WARN] RC100 email alerta reacción falló:", e)


def normalize_reaction_video(input_path: str, order_id: str, probe: Optional[dict] = None) -> tuple[Optional[str], dict]:
    """
    RC100 — normaliza reacción a MP4 H.264/AAC CFR para evitar vídeo congelado por HEVC/H265/VFR/WEBM raro.
    Mantiene proporción. Contain + padding. Nunca crop. Nunca zoom agresivo.
    """
    meta = dict(probe or {})
    meta["normalization_enabled"] = bool(REACTION_NORMALIZE_ENABLED)
    meta["ffmpeg_available"] = reaction_ffmpeg_available()

    if not REACTION_NORMALIZE_ENABLED:
        meta["normalized"] = False
        meta["normalization_error"] = "normalization_disabled"
        return None, meta

    if not input_path or not os.path.exists(input_path):
        meta["normalized"] = False
        meta["normalization_error"] = "input_missing"
        return None, meta

    if not reaction_ffmpeg_available():
        meta["normalized"] = False
        meta["normalization_error"] = "ffmpeg_not_available"
        return None, meta

    width = int(meta.get("width") or 0)
    height = int(meta.get("height") or 0)

    # Si sabemos que es horizontal, canvas horizontal. Si no, vertical por defecto ETERNA.
    if width > height and width > 0 and height > 0:
        canvas_w = max(int(REACTION_NORMALIZED_MAX_HEIGHT or 1280), int(REACTION_NORMALIZED_MAX_WIDTH or 720))
        canvas_h = min(int(REACTION_NORMALIZED_MAX_HEIGHT or 1280), int(REACTION_NORMALIZED_MAX_WIDTH or 720))
    else:
        canvas_w = min(int(REACTION_NORMALIZED_MAX_WIDTH or 720), int(REACTION_NORMALIZED_MAX_HEIGHT or 1280))
        canvas_h = max(int(REACTION_NORMALIZED_MAX_WIDTH or 720), int(REACTION_NORMALIZED_MAX_HEIGHT or 1280))

    fps = max(1, int(REACTION_NORMALIZED_FPS or 25))
    output_path = reaction_normalized_video_path(order_id)

    # contain + padding, sin deformar ni cortar caras.
    vf = (
        f"scale={canvas_w}:{canvas_h}:force_original_aspect_ratio=decrease,"
        f"pad={canvas_w}:{canvas_h}:(ow-iw)/2:(oh-ih)/2,"
        f"setsar=1,fps={fps}"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-map", "0:v:0",
        "-map", "0:a?",
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        output_path,
    ]

    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        meta["ffmpeg_cmd"] = " ".join(cmd)
        if completed.returncode != 0:
            meta["normalized"] = False
            meta["normalization_error"] = (completed.stderr or completed.stdout or "ffmpeg_failed").strip()[-2000:]
            return None, meta

        if not os.path.exists(output_path) or os.path.getsize(output_path) <= 0:
            meta["normalized"] = False
            meta["normalization_error"] = "normalized_output_missing_or_empty"
            return None, meta

        normalized_probe = probe_reaction_video(output_path, order_id=order_id)
        meta["normalized"] = True
        meta["normalized_path"] = output_path
        meta["normalized_bytes"] = os.path.getsize(output_path)
        meta["normalized_probe"] = normalized_probe
        return output_path, meta

    except Exception as e:
        meta["normalized"] = False
        meta["normalization_error"] = str(e)
        return None, meta


def best_reaction_local_path(order: dict) -> str:
    """
    RC100 — ruta preferida para reproducir/servir reacción.
    1) normalizada si existe
    2) original/local clásica si existe
    """
    normalized = (order.get("reaction_video_normalized_local") or "").strip()
    if normalized and os.path.exists(normalized):
        return normalized

    local_path = (order.get("reaction_video_local") or "").strip()
    if local_path and os.path.exists(local_path):
        return local_path

    return ""


def guess_reaction_media_type(order: dict, path: str = "") -> str:
    normalized = (order.get("reaction_video_normalized_local") or "").strip()
    if path and normalized and os.path.abspath(path) == os.path.abspath(normalized):
        return "video/mp4"
    return guess_media_type_from_path(path) if path else "video/mp4"


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


def r2_missing_config() -> list:
    missing = []
    if not R2_ACCESS_KEY:
        missing.append("R2_ACCESS_KEY o R2_ACCESS_KEY_ID")
    if not R2_SECRET_KEY:
        missing.append("R2_SECRET_KEY o R2_SECRET_ACCESS_KEY")
    if not R2_BUCKET:
        missing.append("R2_BUCKET")
    if not R2_ENDPOINT:
        missing.append("R2_ENDPOINT")
    if not R2_PUBLIC_URL:
        missing.append("R2_PUBLIC_URL")
    return missing


def r2_enabled() -> bool:
    return len(r2_missing_config()) == 0


def get_r2_client():
    missing = r2_missing_config()
    if missing:
        try:
            print("🟡 R2 no configurado completo. Falta:", ", ".join(missing))
            if R2_API_TOKEN and (not R2_ACCESS_KEY or not R2_SECRET_KEY):
                print("🟡 R2_API_TOKEN existe, pero boto3 necesita Access Key ID + Secret Access Key de R2, no solo API Token.")
        except Exception:
            pass
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

    remote_name = str(remote_name or "").lstrip("/")
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
    remote_name = str(remote_name or "").lstrip("/")
    client.put_object(Bucket=R2_BUCKET, Key=remote_name, Body=data, ContentType=content_type)
    return f"{R2_PUBLIC_URL}/{remote_name}"


def r2_status_summary() -> dict:
    missing = r2_missing_config()
    return {
        "configured": not missing,
        "missing": missing,
        "bucket": R2_BUCKET or None,
        "endpoint": R2_ENDPOINT or None,
        "public_url": R2_PUBLIC_URL or None,
        "has_access_key": bool(R2_ACCESS_KEY),
        "has_secret_key": bool(R2_SECRET_KEY),
        "has_api_token_note": bool(R2_API_TOKEN),
        "note": "R2_API_TOKEN no sirve para boto3; hacen falta Access Key ID y Secret Access Key." if R2_API_TOKEN and (not R2_ACCESS_KEY or not R2_SECRET_KEY) else None,
    }


def r2_write_probe() -> dict:
    status = r2_status_summary()
    if not status["configured"]:
        return {"ok": False, "stage": "config", "status": status}

    key = f"diagnostics/go-live/r2_probe_{int(time.time())}_{secrets.token_hex(4)}.txt"
    body = f"ETERNA R2 probe {now_iso()} {ETERNA_APP_VERSION}\n".encode("utf-8")
    try:
        public_url = upload_bytes_to_r2(body, key, content_type="text/plain; charset=utf-8")
        if not public_url:
            return {"ok": False, "stage": "upload", "status": status, "key": key}

        public_read_ok = False
        public_status_code = None
        try:
            response = requests.get(public_url, timeout=20)
            public_status_code = response.status_code
            public_read_ok = response.status_code == 200 and body.decode("utf-8").strip() in response.text
        except Exception as public_error:
            return {
                "ok": True,
                "upload_ok": True,
                "public_read_ok": False,
                "stage": "public_read",
                "warning": str(public_error),
                "status": status,
                "key": key,
                "public_url": public_url,
            }

        return {
            "ok": bool(public_read_ok),
            "upload_ok": True,
            "public_read_ok": bool(public_read_ok),
            "public_status_code": public_status_code,
            "stage": "complete" if public_read_ok else "public_read",
            "status": status,
            "key": key,
            "public_url": public_url,
        }
    except Exception as e:
        log_error("r2_write_probe", e)
        return {"ok": False, "stage": "upload", "error": str(e), "status": status, "key": key}


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
    """
    RC100 — Regla de oro:
    1) local primero
    2) validar/probar reacción
    3) normalizar si se puede
    4) R2 después con archivo estable
    5) solo entonces marcar reaction_uploaded y abrir Sender Pack

    No toca Stripe, webhook, Twilio/SMS, WhatsApp ni video engine principal.
    """
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
        "Reacción original guardada localmente en el servidor",
        {"bytes": saved_size, "source": source, "path": local_path},
    )

    validation_ok, probe = validate_reaction_video_file(
        local_path,
        order,
        mime_type=guess_media_type_from_path(local_path),
        source=source,
    )

    insert_order_event(
        order["id"],
        "🔎 rc100_reaction_probe",
        "ok" if validation_ok else "error",
        "Diagnóstico de reacción antes del Sender Pack",
        probe,
    )

    if not validation_ok:
        mark_reaction_invalid(order, probe, probe.get("validation_error") or "reaction_invalid", original_path=local_path)
        raise HTTPException(status_code=400, detail="reaction_invalid_try_again")

    normalized_path, normalization_meta = normalize_reaction_video(local_path, order["id"], probe=probe)

    if normalized_path and os.path.exists(normalized_path):
        sender_safe_path = normalized_path
        sender_safe_extension = "mp4"
        validation_status = "valid_normalized"
        validation_error = None
        insert_order_event(
            order["id"],
            "✅ rc100_reaction_normalized",
            "ok",
            "Reacción normalizada a MP4 H.264/AAC estable para Sender Pack",
            normalization_meta,
        )
    else:
        # Si el original pasó validación pero no se pudo normalizar, no rompemos ETERNA.
        # Se usa original validado y se deja incidencia visible para revisar ffmpeg/config.
        sender_safe_path = local_path
        sender_safe_extension = extension
        validation_status = "valid_original_not_normalized"
        validation_error = normalization_meta.get("normalization_error") or "normalization_skipped"
        insert_order_event(
            order["id"],
            "⚠️ rc100_reaction_not_normalized",
            "warning",
            "La reacción pasó validación, pero no se pudo normalizar; se conserva original validado",
            normalization_meta,
        )

    public_url = None
    r2_error = None
    try:
        content_type = "video/mp4" if sender_safe_extension == "mp4" else guess_media_type_from_path(sender_safe_path)
        remote_name = r2_order_key(order, "reaction", f"reaction.{sender_safe_extension}")
        public_url = upload_video_to_r2(sender_safe_path, remote_name, content_type=content_type)
        insert_order_event(
            order["id"],
            "reaction_r2_uploaded" if public_url else "reaction_r2_skipped",
            "ok" if public_url else "pending",
            "Reacción segura subida a R2" if public_url else "R2 no configurado; se conserva local",
            {
                "public_url": public_url,
                "content_type": content_type,
                "safe_path": sender_safe_path,
                "original_path": local_path,
                "normalized_path": normalized_path,
            },
        )
    except Exception as e:
        r2_error = str(e)
        insert_order_event(order["id"], "reaction_r2_pending", "warning", "R2 falló; la reacción queda segura localmente", {"error": r2_error})
        log_error("complete_reaction_r2_best_effort", e)

    update_order(
        order["id"],
        reaction_video_original_local=local_path,
        reaction_video_local=sender_safe_path,
        reaction_video_normalized_local=normalized_path,
        reaction_video_public_url=public_url,
        reaction_validation_status=validation_status,
        reaction_validation_error=validation_error or r2_error,
        reaction_normalized_at=now_iso() if normalized_path else None,
        reaction_probe_json=json.dumps({**probe, "normalization": normalization_meta}, ensure_ascii=False)[:12000],
        reaction_uploaded=1,
        experience_started=1,
        experience_completed=1,
        delivered_to_recipient=1,
        reaction_upload_pending=0,
        reaction_upload_error=r2_error,
        gift_refund_deadline_at=order.get("gift_refund_deadline_at") or gift_refund_deadline_iso(),
    )

    updated_order = maybe_mark_eterna_completed(order["id"])
    insert_order_event(updated_order["id"], "eterna_completed", "ok", "ETERNA completada: reacción validada/segura y pack desbloqueado")

    try:
        print("📩 RC100: control SMS regalante; solo sale tras validación de reacción")
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
# MEMORY ENGINE V1 — HELPERS SILENCIOSOS
# =========================================================

def memory_truthy(value) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on", "si", "sí", "acepto", "accepted", "checked"}


def clean_memory_text(value: str, max_len: int = 160) -> str:
    return str(value or "").strip()[:max_len]


def normalize_memory_date(value: str) -> str:
    """
    Acepta YYYY-MM-DD. Si viene vacío o raro, devuelve vacío.
    No bloquea el pedido por una fecha mal escrita.
    """
    raw = str(value or "").strip()[:20]
    if not raw:
        return ""
    try:
        candidate = raw[:10]
        datetime.strptime(candidate, "%Y-%m-%d")
        return candidate
    except Exception:
        return ""


def remember_order_moment_silent(
    order_id: str,
    sender_id: int,
    recipient_id: int,
    sender_name: str,
    sender_email: str,
    sender_phone: str,
    recipient_name: str,
    recipient_email: str,
    recipient_phone: str,
    occasion_type: str = "",
    occasion_date: str = "",
    delivery_mode: str = "instant",
    scheduled_delivery_at: str = "",
    marketing_opt_in=False,
) -> bool:
    """
    MEMORY ENGINE V1 — guarda la memoria emocional del pedido.
    - No envía emails.
    - No envía SMS.
    - No envía WhatsApp.
    - No toca Stripe.
    - No toca vídeo.
    - Si falla, NO rompe la compra.
    """
    if not MEMORY_ENGINE_ENABLED:
        return False

    safe_order_id = str(order_id or "").strip()
    if not safe_order_id:
        return False

    now = now_iso()
    safe_occasion_type = clean_memory_text(occasion_type, 60).lower()
    safe_occasion_date = normalize_memory_date(occasion_date)
    safe_delivery_mode = clean_memory_text(delivery_mode or "instant", 30).lower()
    safe_scheduled_delivery_at = clean_memory_text(scheduled_delivery_at, 40)
    opt_in = 1 if memory_truthy(marketing_opt_in) else 0

    meta = {
        "version": "MEMORY_ENGINE_V1_SILENT_SAFE",
        "source": "order_created",
        "reminders_enabled": bool(MEMORY_REMINDERS_ENABLED),
        "note": "Solo guarda memoria. No envía recordatorios todavía.",
    }

    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO memory_events (
                order_id,
                sender_id,
                recipient_id,
                sender_name,
                sender_email,
                sender_phone,
                recipient_name,
                recipient_email,
                recipient_phone,
                occasion_type,
                occasion_date,
                delivery_mode,
                scheduled_delivery_at,
                marketing_opt_in,
                last_reminder_sent,
                memory_created_at,
                created_at,
                updated_at,
                meta_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            safe_order_id,
            sender_id,
            recipient_id,
            clean_memory_text(sender_name, 160),
            clean_memory_text(sender_email, 180),
            clean_memory_text(sender_phone, 60),
            clean_memory_text(recipient_name, 160),
            clean_memory_text(recipient_email, 180),
            clean_memory_text(recipient_phone, 60),
            safe_occasion_type,
            safe_occasion_date,
            safe_delivery_mode,
            safe_scheduled_delivery_at,
            opt_in,
            None,
            now,
            now,
            now,
            json.dumps(meta, ensure_ascii=False),
        ))
        conn.commit()
        conn.close()

        insert_order_event(
            safe_order_id,
            "memory_engine_saved",
            "ok",
            "Memory Engine V1 guardó el momento en modo silencioso",
            {
                "occasion_type": safe_occasion_type,
                "occasion_date": safe_occasion_date,
                "marketing_opt_in": bool(opt_in),
            },
        )
        return True
    except Exception as e:
        print("[WARN] Memory Engine V1 no pudo guardar el momento:", e)
        try:
            insert_order_event(
                safe_order_id,
                "memory_engine_save_failed",
                "warning",
                str(e),
                {"version": "MEMORY_ENGINE_V1_SILENT_SAFE"},
            )
        except Exception:
            pass
        return False


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
            r.phone AS recipient_phone,
            r.email AS recipient_email
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
            r.phone AS recipient_phone,
            r.email AS recipient_email
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
            r.phone AS recipient_phone,
            r.email AS recipient_email
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
            r.phone AS recipient_phone,
            r.email AS recipient_email
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



def rc101_truthy(value) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on", "si", "sí", "mostrar", "show"}


def rc101_clean_photo_slot(slot: str) -> str:
    slot = (slot or ARRIVAL_PHOTO_DEFAULT_SLOT or "photo1").strip().lower()
    slot = slot.replace("_", "").replace("-", "")
    if slot in {"1", "foto1"}:
        return "photo1"
    if slot in {"2", "foto2"}:
        return "photo2"
    if slot in {"3", "foto3"}:
        return "photo3"
    if slot in {"4", "foto4"}:
        return "photo4"
    if slot in {"5", "foto5"}:
        return "photo5"
    if slot in {"6", "foto6"}:
        return "photo6"
    if slot in {"photo1", "photo2", "photo3", "photo4", "photo5", "photo6"}:
        return slot
    return "photo1"


def arrival_photo_url_from_order(order: dict) -> str:
    if not SENDER_IDENTITY_ENABLED:
        return ""
    if not rc101_truthy(order.get("show_sender_identity")):
        return ""
    slot = rc101_clean_photo_slot(order.get("arrival_photo_slot") or ARRIVAL_PHOTO_DEFAULT_SLOT)
    token = (order.get("recipient_token") or "").strip()
    if not token:
        return ""
    return f"{PUBLIC_BASE_URL}/arrival-photo/{token}?slot={quote(slot)}"


def normalize_order_language(value: str) -> str:
    raw = str(value or "").strip().lower()
    if raw in {"en", "english", "gb", "uk", "us"}:
        return "en"
    return "es"


def eterna_ui_text(language: str, key: str) -> str:
    """RC109 INTERNATIONAL UI SAFE — textos backend ES/EN sin tocar imágenes ni assets."""
    lang = normalize_order_language(language or "es")
    texts = {
        "es": {
            "back_create": "Volver a crear",
            "not_found": "No hemos podido encontrar este pedido.",
            "checkout_life": "Tu ETERNA está cobrando vida...",
            "create_another": "Crear otra ETERNA",
            "payment_started": "Tu ETERNA ya está en marcha.",
            "create_one": "Crear una ETERNA",
            "not_available": "Esta experiencia ya no está disponible.",
            "check_again": "Volver a comprobar",
            "still_returning": "Tu ETERNA todavía está volviendo. La reacción se está guardando.",
            "sender_title_html": "Aquí vuelve<br><span>lo que provocaste.</span>",
            "sender_page_title": "Aquí vuelve lo que provocaste",
            "sender_aria": "Sender Pack ETERNA",
            "reaction_aria": "Reacción",
            "share": "↗ Compartir",
            "download": "↓ Descargar",
            "link_copied": "Enlace copiado",
            "share_text": "Aquí vuelve lo que provocaste.",
            "view_again": "Volver a ver mi ETERNA",
            "receive_gift": "Recibir mi regalo",
            "try_receive_gift": "Intentar recibir mi regalo",
            "gift_no_money": "Este regalo no incluía dinero.",
            "gift_sent": "Tu regalo de {amount} ya ha sido enviado.",
            "gift_processing": "Estamos procesando tu regalo de {amount}.",
            "gift_received": "Has recibido {amount}.",
            "mine_title": "Esto ya es tuyo.",
            "back_start": "Volver al inicio",
        },
        "en": {
            "back_create": "Create again",
            "not_found": "We could not find this order.",
            "checkout_life": "Your ETERNA is coming to life...",
            "create_another": "Create another ETERNA",
            "payment_started": "Your ETERNA is already in motion.",
            "create_one": "Create an ETERNA",
            "not_available": "This experience is no longer available.",
            "check_again": "Check again",
            "still_returning": "Your ETERNA is still returning. The reaction is being saved.",
            "sender_title_html": "Here returns<br><span>what you made them feel.</span>",
            "sender_page_title": "Here returns what you made them feel",
            "sender_aria": "ETERNA Sender Pack",
            "reaction_aria": "Reaction",
            "share": "↗ Share",
            "download": "↓ Download",
            "link_copied": "Link copied",
            "share_text": "Here returns what you made them feel.",
            "view_again": "Watch my ETERNA again",
            "receive_gift": "Receive my gift",
            "try_receive_gift": "Try to receive my gift",
            "gift_no_money": "This gift did not include money.",
            "gift_sent": "Your gift of {amount} has already been sent.",
            "gift_processing": "We are processing your gift of {amount}.",
            "gift_received": "You have received {amount}.",
            "mine_title": "This is yours now.",
            "back_start": "Back to the start",
        },
    }
    return texts.get(lang, texts["es"]).get(key, texts["es"].get(key, key))


def build_recipient_arrival_intro(order: dict, language: str = "es") -> str:
    sender_name = (order.get("sender_name") or "").strip()
    lang = normalize_order_language(language or order.get("language") or "es")
    if SENDER_IDENTITY_ENABLED and rc101_truthy(order.get("show_sender_identity")) and sender_name:
        if lang == "en":
            return f"{sender_name} has prepared something for you."
        return f"{sender_name} ha preparado algo para ti."
    if lang == "en":
        return "Someone has prepared something for you."
    return "Alguien ha preparado algo para ti."


def build_recipient_message(order: dict) -> str:
    recipient_name = (order.get("recipient_name") or "").strip()
    url = (recipient_experience_url_from_order(order) or "").strip()
    lang = normalize_order_language(order.get("language") or "es")
    greeting = f"{recipient_name}," if recipient_name else ""
    arrival_intro = build_recipient_arrival_intro(order, lang)
    message = ""

    if lang == "en":
        if greeting:
            message += f"Shhh…\n\n{greeting}\n\n"
        else:
            message += "Shhh…\n\n"
        message += (
            f"{arrival_intro}\n\n"
            "This is not just a video.\n\n"
            "It is not just a moment.\n\n"
            "It is an ETERNA created for you.\n\n"
            "But there is something more…\n\n"
            "Inside, there is something that is also yours.\n\n"
            "Open it when you have a quiet moment:\n\n"
            f"{url}"
        )
        return message.strip()

    if greeting:
        message += f"Shhh…\n\n{greeting}\n\n"
    else:
        message += "Shhh…\n\n"
    message += (
        f"{arrival_intro}\n\n"
        "Esto no es un vídeo.\n\n"
        "No es solo un momento.\n\n"
        "Es una ETERNA creada para ti.\n\n"
        "Pero hay algo más…\n\n"
        "Dentro hay algo que también es tuyo.\n\n"
        "Ábrelo cuando estés tranquilo:\n\n"
        f"{url}"
    )
    return message.strip()


def build_sender_ready_message(order: dict) -> str:
    sender_name = (order.get("sender_name") or "").strip()
    url = (sender_pack_url_from_order(order) or "").strip()
    lang = normalize_order_language(order.get("language") or "es")
    greeting = f"{sender_name}," if sender_name else ""
    message = ""
    if greeting:
        message += f"{greeting}\n\n"

    if lang == "en":
        message += (
            "It has happened.\n\n"
            "Your ETERNA has returned.\n\n"
            "What you gave…\n"
            "has found its way back.\n\n"
            "You can see it here:\n\n"
            f"{url}"
        )
        return message.strip()

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
        try:
            send_admin_error_email(
                f"🚨 ETERNA ERROR sender pack {order_public_code(order)}",
                build_critical_alert_body(order, "Reacción subida pero Sender Pack no enviado al regalante", order.get("sender_sms_error") or "Máximo de intentos alcanzado"),
                order_id=order["id"],
                reason="sender_sms_max_attempts",
            )
        except Exception as email_error:
            log_error("email_alert_sender_sms_max_attempts", email_error)
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

        if attempts >= 3:
            try:
                send_admin_error_email(
                    f"🚨 ETERNA ERROR sender pack {order_public_code(order)}",
                    build_critical_alert_body(order, "No se ha podido enviar el Sender Pack tras varios intentos", result.get("error") or "sms_error"),
                    order_id=order["id"],
                    reason="sender_sms_failed_after_retries",
                )
            except Exception as email_error:
                log_error("email_alert_sender_sms_failed", email_error)

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


def twilio_base_configured() -> bool:
    return bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and Client)


def twilio_sms_enabled() -> bool:
    return bool(twilio_base_configured() and TWILIO_FROM_NUMBER)


def twilio_whatsapp_enabled() -> bool:
    return bool(twilio_base_configured() and whatsapp_from_number())


def twilio_enabled() -> bool:
    # Compatibilidad con código antiguo: significa SMS Twilio configurado.
    return twilio_sms_enabled()


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


def send_whatsapp(phone: str, message: str, media_url: str = "") -> dict:
    to_phone = to_e164(phone)
    wa_from = whatsapp_from_number()
    if not to_phone:
        return {"ok": False, "channel": "whatsapp", "sid": None, "error": "invalid_phone"}
    if not WHATSAPP_ENABLED:
        return {"ok": False, "channel": "whatsapp", "sid": None, "error": "whatsapp_disabled"}
    if not wa_from:
        return {"ok": False, "channel": "whatsapp", "sid": None, "error": "missing_twilio_whatsapp_from"}
    if not twilio_base_configured():
        return {"ok": False, "channel": "whatsapp", "sid": None, "error": "twilio_base_not_configured"}
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        kwargs = {"body": message, "from_": wa_from, "to": f"whatsapp:{to_phone}"}
        if media_url:
            kwargs["media_url"] = [media_url]
        msg = client.messages.create(**kwargs)
        return {"ok": True, "channel": "whatsapp", "sid": msg.sid, "error": None, "media_url": media_url or None}
    except Exception as e:
        return {"ok": False, "channel": "whatsapp", "sid": None, "error": str(e), "media_url": media_url or None}


def send_message_best_effort(phone: str, message: str, media_url: str = "") -> dict:
    whatsapp_result = send_whatsapp(phone, message, media_url=media_url)
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


# =========================================================
# RC95 — EMAIL CORPORATIVO / PEDIDOS / ALERTAS
# No bloquea el flujo: si el email falla, ETERNA sigue y deja evento/log.
# =========================================================

def email_enabled_and_configured() -> bool:
    return bool(EMAIL_ENABLED and SMTP_HOST and SMTP_PORT and SMTP_USER and SMTP_PASSWORD and SMTP_FROM)


def _email_recipients(value: str) -> list[str]:
    recipients = []
    for part in str(value or "").replace(";", ",").split(","):
        item = part.strip()
        if item and "@" in item:
            recipients.append(item)
    return recipients


def send_eterna_email(to_email: str, subject: str, body: str, reply_to: str = "") -> dict:
    """Envía email de texto simple desde el buzón corporativo. Nunca lanza excepción al flujo principal."""
    recipients = _email_recipients(to_email)
    if not recipients:
        return {"ok": False, "error": "missing_recipient"}
    if not email_enabled_and_configured():
        return {"ok": False, "error": "email_not_configured"}

    try:
        msg = EmailMessage()
        msg["Subject"] = str(subject or "ETERNA").strip()[:180]
        msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM}>" if SMTP_FROM_NAME else SMTP_FROM
        msg["To"] = ", ".join(recipients)
        if reply_to and "@" in reply_to:
            msg["Reply-To"] = reply_to.strip()
        msg.set_content(str(body or "").strip() or "ETERNA")

        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20) as smtp:
                smtp.login(SMTP_USER, SMTP_PASSWORD)
                smtp.send_message(msg)
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(SMTP_USER, SMTP_PASSWORD)
                smtp.send_message(msg)
        return {"ok": True, "error": None}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def order_public_code(order: dict) -> str:
    raw = str((order or {}).get("id") or "").strip()
    if not raw:
        return "ET-SIN-ID"
    if raw.upper().startswith("ET-"):
        return raw
    return f"ET-{raw}"


def build_customer_order_email_body(order: dict) -> str:
    sender_name = (order.get("sender_name") or "").strip()
    greeting = f"Hola {sender_name}," if sender_name else "Hola,"
    return f"""{greeting}

Hemos recibido tu ETERNA correctamente.

Número de pedido: {order_public_code(order)}

Pago recibido.
Tu ETERNA se está creando.

Pronto tendrás noticias.

Si necesitas ayuda con tu pedido, puedes contactar con ETERNA:
{ETERNA_SUPPORT_EMAIL}
{ETERNA_SUPPORT_PHONE}

Gracias por formar parte de ETERNA.
""".strip()


def build_admin_order_email_body(order: dict) -> str:
    recipient_url = recipient_experience_url_from_order(order) if order else ""
    sender_url = sender_pack_url_from_order(order) if order else ""
    return f"""🦋 NUEVO PEDIDO ETERNA

Pedido: {order_public_code(order)}
Order ID interno: {order.get('id')}
Fecha: {order.get('created_at')}
Estado: {order.get('order_state') or 'PAID'}

REGALANTE
Nombre: {order.get('sender_name') or 'sin nombre'}
Email: {order.get('sender_email') or 'sin email'}
Teléfono: {order.get('sender_phone') or 'sin teléfono'}

REGALADO
Nombre: {order.get('recipient_name') or 'sin nombre'}
Teléfono: {order.get('recipient_phone') or 'sin teléfono'}
Email rescate: {order.get('recipient_email') or 'no indicado'}

PEDIDO
Ocasión: {order.get('occasion_type') or 'no indicada'}
Tipo emoción: {order.get('message_type') or 'sin tipo'}
Entrega: {order.get('delivery_mode') or 'instant'}
Entrega programada: {order.get('scheduled_delivery_at') or 'no'}
Dinero regalo: {money(order.get('gift_amount') or 0)} €
Total pagado: {money(order.get('total_amount') or 0)} €
Stripe session: {order.get('stripe_session_id') or 'pendiente/no disponible'}
Stripe payment intent: {order.get('stripe_payment_intent_id') or 'pendiente/no disponible'}

FRASES
1. {order.get('phrase_1') or ''}
2. {order.get('phrase_2') or ''}
3. {order.get('phrase_3') or ''}

ENLACES INTERNOS DE RESCATE
Link regalado: {recipient_url}
Link regalante: {sender_url}

CHECK ACTUAL
✅ Pago recibido
⏳ Tu ETERNA se está creando / esperando render

SOPORTE ETERNA
Email: {ETERNA_SUPPORT_EMAIL}
Teléfono/WhatsApp: {ETERNA_SUPPORT_PHONE}
""".strip()


def send_order_received_emails(order_id: str) -> dict:
    """Envía confirmación simple al comprador y correo operativo a ETERNA. Idempotente."""
    result = {"customer": "skipped", "admin": "skipped"}
    try:
        order = get_order_by_id(order_id)
    except Exception as e:
        return {"customer": "error", "admin": "error", "error": str(e)}

    errors = []
    sender_email = (order.get("sender_email") or "").strip()

    if sender_email and not order.get("order_email_customer_sent_at"):
        customer_res = send_eterna_email(
            sender_email,
            "Hemos recibido tu ETERNA",
            build_customer_order_email_body(order),
        )
        if customer_res.get("ok"):
            update_order(order_id, order_email_customer_sent_at=now_iso(), order_email_last_error=None)
            insert_order_event(order_id, "customer_order_email", "ok", "Email simple de pedido enviado al comprador")
            result["customer"] = "sent"
        else:
            err = customer_res.get("error") or "customer_email_error"
            errors.append(f"customer: {err}")
            update_order(order_id, order_email_last_error=err)
            insert_order_event(order_id, "customer_order_email", "error", err)
            result["customer"] = "error"

    admin_targets = ",".join([x for x in [ETERNA_OPERATIONS_EMAIL, ADMIN_ALERT_EMAIL] if x])
    if admin_targets and not order.get("order_email_admin_sent_at"):
        admin_res = send_eterna_email(
            admin_targets,
            f"🦋 Nuevo pedido ETERNA {order_public_code(order)}",
            build_admin_order_email_body(order),
            reply_to=sender_email,
        )
        if admin_res.get("ok"):
            update_order(order_id, order_email_admin_sent_at=now_iso(), order_email_last_error=None)
            insert_order_event(order_id, "admin_order_email", "ok", "Email operativo de pedido enviado a ETERNA/Sergio")
            result["admin"] = "sent"
        else:
            err = admin_res.get("error") or "admin_email_error"
            errors.append(f"admin: {err}")
            update_order(order_id, order_email_last_error=err)
            insert_order_event(order_id, "admin_order_email", "error", err)
            result["admin"] = "error"

    if errors:
        result["error"] = " | ".join(errors)
    return result


def send_admin_error_email(subject: str, body: str, order_id: str = "", reason: str = "") -> dict:
    targets = ",".join([x for x in [ADMIN_ALERT_EMAIL, ETERNA_OPERATIONS_EMAIL] if x])
    if not targets:
        return {"ok": False, "error": "missing_admin_email"}
    res = send_eterna_email(targets, subject, body)
    if order_id:
        try:
            update_order(order_id, admin_alert_last_sent_at=now_iso(), admin_alert_last_reason=reason or subject)
            insert_order_event(order_id, "admin_error_email", "ok" if res.get("ok") else "error", reason or subject, {"email_result": res})
        except Exception:
            pass
    return res


def build_critical_alert_body(order: dict, title: str, detail: str) -> str:
    return f"""🚨 ALERTA ETERNA

{title}

Pedido: {order_public_code(order)}
Order ID: {order.get('id') if order else 'sin pedido'}
Hora: {now_iso()}

Detalle:
{detail}

Regalante: {(order or {}).get('sender_name') or 'sin nombre'} | {(order or {}).get('sender_email') or 'sin email'} | {(order or {}).get('sender_phone') or 'sin teléfono'}
Regalado: {(order or {}).get('recipient_name') or 'sin nombre'} | {(order or {}).get('recipient_phone') or 'sin teléfono'}

Link regalado: {recipient_experience_url_from_order(order) if order else ''}
Link regalante: {sender_pack_url_from_order(order) if order else ''}
""".strip()

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
        arrival_media_url = arrival_photo_url_from_order(order)
        print("📩 RC53 ENVIANDO MENSAJE DESTINATARIO A:", order.get("recipient_phone", ""))
        result = send_message_best_effort(order.get("recipient_phone", ""), message, media_url=arrival_media_url)

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
    <html lang="{initial_language}">
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
    return HTMLResponse("""<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Privacidad - Tu ETERNA</title><style>body{margin:0;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;line-height:1.72;padding:26px;max-width:860px;margin:auto;background-image:radial-gradient(circle at 80% 10%,rgba(32,164,255,.16),transparent 28%),radial-gradient(circle at 10% 90%,rgba(255,194,74,.10),transparent 30%)}h1{font-family:Georgia,'Times New Roman',serif;font-size:34px;margin:0 0 8px;color:#f5d28b}h2{font-size:19px;margin-top:28px;color:#f5d28b}p,li{opacity:.88}.box{border:1px solid rgba(255,207,112,.22);border-radius:18px;padding:18px;background:rgba(255,255,255,.045);margin:20px 0}.small{opacity:.62;font-size:13px}</style></head><body><h1>Politica de privacidad - Tu ETERNA</h1><p class='small'>Version inicial para fase de lanzamiento. Recomendable revision legal antes de abrir a gran escala.</p><div class='box'><p><b>Resumen:</b> usamos los datos minimos necesarios para crear, entregar y conservar temporalmente la experiencia ETERNA.</p></div><h2>1. Datos tratados</h2><ul><li>Nombre, telefono y correo si se facilita.</li><li>Fotografias, frases y datos introducidos.</li><li>Video generado y reaccion grabada si se aceptan permisos.</li><li>Datos tecnicos minimos: fecha, navegador, estado de entrega, logs de errores y eventos necesarios para seguridad y soporte.</li></ul><h2>2. Finalidad</h2><p>Crear la experiencia, procesar el pago, entregar el enlace, permitir la visualizacion, guardar la reaccion, enviar el sender pack, resolver incidencias y mejorar la seguridad del sistema.</p><h2>3. Legitimacion</h2><p>Ejecucion del servicio solicitado, consentimiento cuando se aceptan permisos de camara y microfono, e interes legitimo para seguridad y soporte.</p><h2>4. Proveedores</h2><p>Podemos utilizar proveedores de alojamiento, almacenamiento, pagos, SMS/WhatsApp, correo y analitica tecnica minima. No vendemos datos personales.</p><h2>5. Conservacion</h2><p>Los datos se conservaran el tiempo necesario para prestar el servicio, permitir acceso al recuerdo y atender incidencias. Puede solicitarse eliminacion.</p><h2>6. Grabacion de reaccion</h2><p>La reaccion solo se graba si el destinatario concede permisos. Puede enviarse de forma privada a la persona que creo la ETERNA.</p><h2>7. Derechos</h2><p>Puedes solicitar acceso, rectificacion, eliminacion, oposicion o limitacion escribiendo al correo de contacto.</p><h2>8. Seguridad</h2><p>Aplicamos medidas razonables, pero ningun sistema conectado a internet garantiza riesgo cero.</p><h2>9. Contacto</h2><p>Para privacidad o eliminacion: <b>hola@tueterna.com</b> o WhatsApp +34 641 63 53 14.</p></body></html>""")

@app.get("/soporte", response_class=HTMLResponse)
def soporte_eterna():
    return HTMLResponse(f"""<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Soporte ETERNA</title><style>body{{margin:0;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;line-height:1.7;padding:28px;max-width:760px;margin:auto}}h1{{font-family:Georgia,serif;color:#f5d28b}}.box{{border:1px solid rgba(245,210,139,.25);border-radius:22px;padding:22px;background:rgba(255,255,255,.045)}}a{{color:#f5d28b}}</style></head><body><h1>Soporte ETERNA</h1><div class='box'><p>Si tienes cualquier incidencia con tu ETERNA, escríbenos indicando tu número de pedido.</p><p><b>Email:</b> <a href='mailto:{ETERNA_SUPPORT_EMAIL}'>{ETERNA_SUPPORT_EMAIL}</a></p><p><b>Teléfono / WhatsApp:</b> {ETERNA_SUPPORT_PHONE}</p><p>Tu ETERNA no se pierde. Si algo falla, podremos revisar el pedido y ayudarte.</p></div></body></html>""")


@app.get("/como-funciona", response_class=HTMLResponse)
def como_funciona_eterna():
    return HTMLResponse("""<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Cómo funciona ETERNA</title><style>body{margin:0;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;line-height:1.7;padding:28px;max-width:860px;margin:auto}h1{font-family:Georgia,serif;color:#f5d28b}.step{border:1px solid rgba(245,210,139,.22);border-radius:22px;padding:18px;margin:14px 0;background:rgba(255,255,255,.045)}b{color:#f5d28b}</style></head><body><h1>Cómo funciona ETERNA</h1><div class='step'><b>1. Eliges 6 fotos</b><br>Seleccionas los recuerdos que quieres convertir en una experiencia emocional.</div><div class='step'><b>2. Escribes o eliges frases</b><br>Puedes escribir lo que sientes o dejar que ETERNA encuentre las palabras.</div><div class='step'><b>3. La persona recibe la experiencia</b><br>Le llega un enlace para vivirla con calma, en su móvil.</div><div class='step'><b>4. La emoción vuelve a ti</b><br>Recibes la reacción real de la persona al vivir la experiencia.</div></body></html>""")


@app.get("/faq", response_class=HTMLResponse)
def faq_eterna():
    return HTMLResponse(f"""<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Preguntas frecuentes ETERNA</title><style>body{{margin:0;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;line-height:1.7;padding:28px;max-width:860px;margin:auto}}h1{{font-family:Georgia,serif;color:#f5d28b}}h2{{color:#f5d28b;font-size:18px;margin-top:24px}}.box{{border:1px solid rgba(245,210,139,.22);border-radius:22px;padding:20px;background:rgba(255,255,255,.045)}}a{{color:#f5d28b}}</style></head><body><h1>Preguntas frecuentes</h1><div class='box'><h2>¿Qué es ETERNA?</h2><p>Una experiencia emocional creada con fotos, frases y una reacción real que vuelve a quien la crea.</p><h2>¿Es privado?</h2><p>Sí. Las fotos, el vídeo y la reacción se tratan como contenido privado de la experiencia.</p><h2>¿Se puede enviar dinero?</h2><p>Sí. Puedes añadir un regalo económico que recibirá la persona destinataria.</p><h2>¿Qué recibe la otra persona?</h2><p>Un enlace para vivir la experiencia en su móvil.</p><h2>¿Qué recibo yo?</h2><p>El sender pack con la emoción de vuelta.</p><h2>¿Y si hay una incidencia?</h2><p>Contacta con ETERNA: <a href='mailto:{ETERNA_SUPPORT_EMAIL}'>{ETERNA_SUPPORT_EMAIL}</a> · {ETERNA_SUPPORT_PHONE}</p><h2>¿Dónde está disponible?</h2><p>Disponible en toda España: Madrid, Barcelona, Valencia, Sevilla, Málaga, Bilbao, Zaragoza y el resto del país.</p></div></body></html>""")


async def create_order_and_redirect(
    customer_name: str,
    customer_email: str,
    customer_country_code: str,
    customer_phone: str,
    recipient_name: str,
    recipient_country_code: str,
    recipient_phone: str,
    recipient_email: str,
    occasion_type: str,
    message_type: str,
    phrase_mode: str,
    phrase_1: str,
    phrase_2: str,
    phrase_3: str,
    delivery_mode: str,
    delivery_date: str,
    delivery_time: str,
    gift_amount: float,
    photo1: Optional[UploadFile],
    photo2: Optional[UploadFile],
    photo3: Optional[UploadFile],
    photo4: Optional[UploadFile],
    photo5: Optional[UploadFile],
    photo6: Optional[UploadFile],
    photo_upload_session: str = "",
    show_sender_identity: str = "",
    arrival_photo_slot: str = "photo1",
    responsible_use_accepted: str = "",
    yul_memory_place: str = "",
    yul_memory_detail: str = "",
    yul_emotion_tone: str = "",
    yul_magic_hint: str = "",
    occasion_date: str = "",
    marketing_opt_in: str = "",
    language: str = "es",
):
    customer_name = (customer_name or "").strip()
    customer_email = (customer_email or "").strip()
    customer_country_code = (customer_country_code or "").strip()
    customer_phone = (customer_phone or "").strip()

    recipient_name = (recipient_name or "").strip()
    recipient_country_code = (recipient_country_code or "").strip()
    recipient_phone = (recipient_phone or "").strip()
    recipient_email = (recipient_email or "").strip()
    photo_upload_session = _safe_preupload_session(photo_upload_session) if photo_upload_session else ""

    show_sender_identity_bool = rc101_truthy(show_sender_identity)
    arrival_photo_slot = rc101_clean_photo_slot(arrival_photo_slot)

    occasion_type = (occasion_type or "").strip().lower()[:40]
    occasion_date = normalize_memory_date(occasion_date or delivery_date)
    marketing_opt_in = str(marketing_opt_in or "").strip()
    language = normalize_order_language(language)
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

    if not customer_email or "@" not in customer_email:
        raise HTTPException(status_code=400, detail="Tu email es obligatorio para enviarte el número de pedido")

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

    # RC107 — fuente de fotos:
    # 1) Preferimos preuploads ya guardados por /preupload-photo.
    # 2) Si no hay preupload, mantenemos compatibilidad con multipart normal.
    preuploaded_photos = list_preuploaded_photos(photo_upload_session) if photo_upload_session else {}

    required_first_slots = ["photo1", "photo2", "photo3", "photo4"]
    for slot_name in required_first_slots:
        upload = photos.get(slot_name)
        has_upload = bool(upload and getattr(upload, "filename", ""))
        has_preupload = bool(preuploaded_photos.get(slot_name))
        if not has_upload and not has_preupload:
            raise HTTPException(status_code=400, detail=f"Falta {slot_name}. Sube al menos las primeras 4 fotos.")

    provided_photo_count = 0
    for slot_name in ["photo1", "photo2", "photo3", "photo4", "photo5", "photo6"]:
        upload = photos.get(slot_name)
        if (upload and getattr(upload, "filename", "")) or preuploaded_photos.get(slot_name):
            provided_photo_count += 1

    if provided_photo_count < 4:
        raise HTTPException(status_code=400, detail="Sube al menos 4 fotos para crear tu ETERNA")

    for slot_name, upload in photos.items():
        if not upload or not getattr(upload, "filename", ""):
            continue

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
            INSERT INTO recipients (name, phone, email, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (recipient_name, recipient_phone_e164, recipient_email, created_at),
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
        if occasion_type:
            try:
                update_order(order_id, occasion_type=occasion_type)
            except Exception as e:
                print("[WARN] RC99 occasion_type no guardado:", e)

        try:
            update_order(order_id, language=language)
            insert_order_event(order_id, "rc108_language_saved", "ok", "Idioma del pedido guardado", {"language": language})
        except Exception as e:
            print("[WARN] RC108 language no guardado:", e)

        # =========================================================
        # MEMORY ENGINE V1 — SILENT SAFE
        # Guarda el momento importante sin enviar nada.
        # =========================================================
        try:
            remember_order_moment_silent(
                order_id=order_id,
                sender_id=sender_id,
                recipient_id=recipient_id,
                sender_name=customer_name,
                sender_email=customer_email,
                sender_phone=sender_phone_e164,
                recipient_name=recipient_name,
                recipient_email=recipient_email,
                recipient_phone=recipient_phone_e164,
                occasion_type=occasion_type,
                occasion_date=occasion_date,
                delivery_mode=delivery_mode,
                scheduled_delivery_at=scheduled_delivery_at,
                marketing_opt_in=marketing_opt_in,
            )
        except Exception as e:
            print("[WARN] Memory Engine V1 no bloquea pedido:", e)

        try:
            update_order(
                order_id,
                show_sender_identity=1 if show_sender_identity_bool else 0,
                arrival_photo_slot=arrival_photo_slot if show_sender_identity_bool else None,
                arrival_photo_url=f"{PUBLIC_BASE_URL}/arrival-photo/{recipient_token}?slot={quote(arrival_photo_slot)}" if show_sender_identity_bool else None,
            )
            insert_order_event(
                order_id,
                "rc101_sender_identity_saved",
                "ok",
                "Identidad opcional del remitente guardada",
                {"show_sender_identity": bool(show_sender_identity_bool), "arrival_photo_slot": arrival_photo_slot if show_sender_identity_bool else None},
            )
        except Exception as e:
            print("[WARN] RC101 sender identity no guardada:", e)

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
            f"🌍 Idioma: {language}",
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
        saved_photo_paths = {}

        for slot_name in ["photo1", "photo2", "photo3", "photo4", "photo5", "photo6"]:
            pre_path = preuploaded_photos.get(slot_name)
            if pre_path and os.path.exists(pre_path):
                source = Path(pre_path)
                folder = PHOTO_FOLDER / order_id
                folder.mkdir(parents=True, exist_ok=True)
                target = folder / f"{slot_name}{source.suffix or '.jpg'}"
                shutil.copyfile(str(source), str(target))
                saved_photo_paths[slot_name] = str(target)

                insert_asset(
                    order_id=order_id,
                    asset_type=slot_name,
                    file_url=str(target),
                    storage_provider="local_preupload_rc107",
                )
                continue

            upload = photos.get(slot_name)
            if not upload or not getattr(upload, "filename", ""):
                continue

            filepath = await save_upload_original_robust(order_id, slot_name, upload)
            saved_photo_paths[slot_name] = filepath

            insert_asset(
                order_id=order_id,
                asset_type=slot_name,
                file_url=filepath,
                storage_provider="local_original",
            )

        # RC106/RC107: completar hasta 6 fotos si el usuario sube 4 o 5.
        # 4 fotos -> photo5 = photo1, photo6 = photo2
        # 5 fotos -> photo6 = photo1
        duplicate_plan = {
            "photo5": "photo1",
            "photo6": "photo2" if "photo5" not in saved_photo_paths else "photo1",
        }

        for missing_slot, source_slot in duplicate_plan.items():
            if missing_slot in saved_photo_paths:
                continue

            source_path = saved_photo_paths.get(source_slot) or saved_photo_paths.get("photo1")
            if not source_path or not os.path.exists(source_path):
                raise HTTPException(status_code=400, detail=f"No se pudo completar {missing_slot}")

            source = Path(source_path)
            duplicate_path = source.with_name(f"{missing_slot}{source.suffix or '.jpg'}")
            shutil.copyfile(str(source), str(duplicate_path))
            saved_photo_paths[missing_slot] = str(duplicate_path)

            insert_asset(
                order_id=order_id,
                asset_type=missing_slot,
                file_url=str(duplicate_path),
                storage_provider="local_original_duplicate",
            )

        insert_order_event(
            order_id,
            "photos_saved",
            "ok",
            "Fotos guardadas correctamente. Si faltaban foto5/foto6, ETERNA las completó repitiendo fotos.",
            {"provided_photo_count": provided_photo_count, "completed_to_six": True},
        )
        try:
            if photo_upload_session:
                shutil.rmtree(str(preupload_session_folder(photo_upload_session)), ignore_errors=True)
        except Exception as cleanup_error:
            print("[WARN] RC107 preupload cleanup skipped:", cleanup_error)

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
            if not upload:
                continue
            try:
                await upload.close()
            except Exception:
                pass

    if not STRIPE_SECRET_KEY:
        if not ETERNA_ALLOW_NO_STRIPE_TEST:
            insert_order_event(
                order_id,
                "stripe_missing_blocked",
                "error",
                "Pedido bloqueado: falta STRIPE_SECRET_KEY y ETERNA_ALLOW_NO_STRIPE_TEST no está activo.",
                {"version": ETERNA_APP_VERSION},
            )
            raise HTTPException(
                status_code=503,
                detail="ETERNA no puede aceptar pedidos ahora mismo: Stripe no está configurado en producción.",
            )

        update_order(
            order_id,
            paid=1,
            stripe_payment_status="test_no_stripe",
            gift_refund_deadline_at=gift_refund_deadline_iso(),
            delivery_locked=1 if delivery_mode == "scheduled" else 0,
        )

        try:
            email_result = send_order_received_emails(order_id)
            print("📧 RC95 emails pedido test_no_stripe:", email_result)
        except Exception as e:
            log_error("order_emails_test_no_stripe", e)

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
        extra_note=eterna_ui_text(order.get("language"), "checkout_life"),
    )


def render_checkout_success_visual(order: dict) -> HTMLResponse:
    """
    Pantalla de pago realizado. Visual únicamente.
    RC116: al confirmar pago correcto limpiamos el borrador local del formulario
    y los drafts de fotos del navegador para evitar mezclar Eternas antiguas.
    No fuerza envío, no toca webhook y no modifica el estado del pedido.
    """
    rc116_cleanup_script = """
<script>
(function(){
    try { localStorage.removeItem("eterna_create_form_v4"); } catch(e) {}
    try { localStorage.setItem("eterna_last_paid_order", "%s"); } catch(e) {}
    try {
        if ("indexedDB" in window) {
            var req = indexedDB.deleteDatabase("eterna_photo_draft_v1");
            req.onerror = function(){ console.warn("RC116 photo draft cleanup skipped"); };
        }
    } catch(e) {
        console.warn("RC116 checkout cleanup skipped", e);
    }
})();
</script>
""" % safe_attr(order.get("id") or "")
    return render_eterna_image_screen(
        image_name="payment-success-v1.png",
        fallback_image_name="payment-success-v1.png",
        overlay_kind="soft",
        button_url="/crear",
        button_label=eterna_ui_text(order.get("language"), "create_another"),
        extra_note=eterna_ui_text(order.get("language"), "payment_started"),
        extra_script=rc116_cleanup_script,
    )


@app.get("/checkout-exito/{order_id}", response_class=HTMLResponse)
def checkout_exito(order_id: str):
    """
    Landing posterior al pago. RC115 mantiene el webhook como vía principal,
    pero añade rescate seguro: si el webhook falló, verifica la sesión en Stripe
    y dispara el mismo procesador de pago real.
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

    try:
        if STRIPE_SECRET_KEY and not bool(order.get("paid")):
            stripe_session_id = (order.get("stripe_session_id") or "").strip()
            if stripe_session_id:
                print("🛟 RC115 checkout-exito recovery intentando verificar sesión:", stripe_session_id)
                session = stripe.checkout.Session.retrieve(stripe_session_id)
                result = process_paid_checkout_session(session, source="checkout_exito_recovery")
                print("🛟 RC115 checkout-exito recovery result:", result)
                order = get_order_by_id(order_id)
            else:
                print("⚠️ RC115 checkout-exito sin stripe_session_id para recovery:", order_id)
    except Exception as e:
        # No rompemos la pantalla de éxito al comprador; dejamos log para corregir Stripe/secret.
        log_error("checkout_exito_payment_recovery", e)

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

def render_create_form(initial_language: str = "es") -> str:
    initial_language = "en" if str(initial_language or "").lower().strip() == "en" else "es"
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
            .language-switch {{
                display: flex;
                gap: 10px;
                justify-content: center;
                margin: 8px auto 22px auto;
                flex-wrap: wrap;
            }}
            .language-option {{
                border: 1px solid rgba(245,210,139,.28);
                background: rgba(255,255,255,.045);
                color: rgba(255,247,230,.78);
                padding: 10px 14px;
                border-radius: 999px;
                font-weight: 800;
                cursor: pointer;
            }}
            .language-option.active {{
                background: rgba(245,210,139,.16);
                color: #f5d28b;
                box-shadow: 0 0 22px rgba(245,210,139,.12);
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
            .photo-status.ready {{ color: rgba(245,210,139,0.95); text-shadow:0 0 14px rgba(245,210,139,.28); }}
            .photo-status.loading {{ color: rgba(120,210,255,0.96); text-shadow:0 0 14px rgba(90,200,255,.25); }}
            .photo-status.optional {{ color: rgba(255,255,255,0.38); }}
            .photo-box.ready {{ border-color: rgba(245,210,139,.72); box-shadow:0 0 22px rgba(245,210,139,.16); }}
            .photo-box.loading {{ border-color: rgba(90,200,255,.68); box-shadow:0 0 22px rgba(90,200,255,.16); }}
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
                <div class="subtitle" data-i18n="subtitle">Crea algo que no se abra. Se viva.</div>
                <div class="language-switch" aria-label="Idioma / Language">
                    <a href="/crear?lang=es" role="button" class="language-option {'active' if initial_language == 'es' else ''}" data-lang="es">🇪🇸 Español</a>
                    <a href="/crear?lang=en" role="button" class="language-option {'active' if initial_language == 'en' else ''}" data-lang="en">🇬🇧 English</a>
                </div>
                <script>
                // RC111 LANGUAGE SWITCH HARD FALLBACK
                // Este bloque pequeño vive pegado al botón para que ES/EN funcione aunque el JS grande del formulario falle después.
                (function() {{
                    function setText(selector, value) {{
                        var el = document.querySelector(selector);
                        if (el) el.textContent = value;
                    }}
                    function setPlaceholder(id, value) {{
                        var el = document.getElementById(id);
                        if (el) el.placeholder = value;
                    }}
                    var hardTexts = {{
                        es: {{
                            subtitle: "Crea algo que no se abra. Se viva.",
                            intro1: "No todo lo importante",
                            intro2: "debería desaparecer.",
                            intro3: "Haz que vuelva convertido",
                            intro4: "en emoción real.",
                            creator: "QUIÉN LO CREA",
                            recipient: "QUIÉN LO VA A VIVIR",
                            customerName: "Tu nombre",
                            customerEmail: "Tu email",
                            customerPhone: "Tu teléfono",
                            recipientName: "Su nombre",
                            recipientPhone: "Su teléfono",
                            recipientEmail: "Su email (opcional, por si el SMS falla)",
                            photosCopy: "Elige entre 4 y 6 fotos. Si subes 4, ETERNA completará el vídeo de forma discreta.",
                            pickerTitle: "Seleccionar 6 recuerdos",
                            pickerSub: "Puedes elegir las 6 fotos de una vez. Después podrás cambiar cualquiera individualmente.",
                            openGallery: "Abrir galería",
                            photo: "FOTO",
                            change: "Cambiar",
                            pending: "Pendiente",
                            photoNote: "Sube al menos 4 fotos. Si tienes 6, mejor.",
                            emotionTitle: "TIPO DE EMOCIÓN",
                            wordsTitle: "TUS PALABRAS",
                            giftTitle: "DINERO A REGALAR",
                            submit: "CONTINUAR AL PAGO"
                        }},
                        en: {{
                            subtitle: "Create something they do not just open. They live it.",
                            intro1: "Not everything important",
                            intro2: "should disappear.",
                            intro3: "Make it return as",
                            intro4: "real emotion.",
                            creator: "WHO CREATES IT",
                            recipient: "WHO WILL LIVE IT",
                            customerName: "Your name",
                            customerEmail: "Your email",
                            customerPhone: "Your phone",
                            recipientName: "Their name",
                            recipientPhone: "Their phone",
                            recipientEmail: "Their email (optional, in case SMS fails)",
                            photosCopy: "Choose 4 to 6 photos. If you upload 4, ETERNA will complete the video discreetly.",
                            pickerTitle: "Select 6 memories",
                            pickerSub: "You can choose all 6 photos at once. Afterwards, you can replace any of them individually.",
                            openGallery: "Open gallery",
                            photo: "PHOTO",
                            change: "Change",
                            pending: "Pending",
                            photoNote: "Upload at least 4 photos. 6 is ideal.",
                            emotionTitle: "TYPE OF EMOTION",
                            wordsTitle: "YOUR WORDS",
                            giftTitle: "GIFT AMOUNT",
                            submit: "CONTINUE TO PAYMENT"
                        }}
                    }};
                    window.eternaHardLanguageSwitch = function(lang) {{
                        lang = lang === "en" ? "en" : "es";
                        var t = hardTexts[lang] || hardTexts.es;
                        var input = document.getElementById("language");
                        if (input) input.value = lang;
                        try {{ localStorage.setItem("eterna_language", lang); }} catch(e) {{}}
                        document.documentElement.setAttribute("lang", lang);
                        document.querySelectorAll(".language-option").forEach(function(btn) {{
                            btn.classList.toggle("active", btn.getAttribute("data-lang") === lang);
                        }});
                        setText('[data-i18n="subtitle"]', t.subtitle);
                        setText('.intro-line.l1', t.intro1);
                        setText('.intro-line.l2', t.intro2);
                        setText('.intro-line.l3', t.intro3);
                        setText('.intro-line.l4', t.intro4);
                        var titles = document.querySelectorAll('.section-title');
                        if (titles[0]) titles[0].textContent = t.creator;
                        if (titles[1]) titles[1].textContent = t.recipient;
                        setPlaceholder('customer_name', t.customerName);
                        setPlaceholder('customer_email', t.customerEmail);
                        setPlaceholder('customer_phone', t.customerPhone);
                        setPlaceholder('recipient_name', t.recipientName);
                        setPlaceholder('recipient_phone', t.recipientPhone);
                        setPlaceholder('recipient_email', t.recipientEmail);
                        setText('.s3 .soft-copy', t.photosCopy);
                        setText('.photo-picker-title', t.pickerTitle);
                        setText('.photo-picker-sub', t.pickerSub);
                        var pickerBtn = document.querySelector('.photo-picker-btn');
                        if (pickerBtn && pickerBtn.childNodes && pickerBtn.childNodes.length) pickerBtn.childNodes[0].nodeValue = t.openGallery + ' ';
                        document.querySelectorAll('.photo-label').forEach(function(el, index) {{ el.textContent = t.photo + ' ' + (index + 1); }});
                        document.querySelectorAll('.photo-placeholder').forEach(function(el) {{ el.textContent = t.change; }});
                        document.querySelectorAll('.photo-status').forEach(function(el) {{
                            var raw = (el.textContent || '').trim();
                            if (!raw || raw === 'Pendiente' || raw === 'Pending' || raw.indexOf('Aún no') >= 0 || raw.indexOf('Still missing') >= 0) el.textContent = t.pending;
                        }});
                        setText('.mini-note', t.photoNote);
                        var sectionTitles = document.querySelectorAll('.section-title');
                        if (sectionTitles[5]) sectionTitles[5].textContent = t.emotionTitle;
                        if (sectionTitles[6]) sectionTitles[6].textContent = t.wordsTitle;
                        if (sectionTitles[8]) sectionTitles[8].textContent = t.giftTitle;
                        var submit = document.getElementById('submitBtn');
                        if (submit && !submit.disabled) submit.textContent = t.submit;
                        try {{ if (typeof applyLanguage === 'function') applyLanguage(lang); }} catch(e) {{ console.log('ETERNA language full switch fallback:', e); }}
                    }};
                }})();
                </script>

                <div class="intro">
                    <p class="intro-line l1">No todo lo importante</p>
                    <p class="intro-line l2">debería desaparecer.</p>
                    <p class="intro-line l3">Haz que vuelva convertido</p>
                    <p class="intro-line l4">en emoción real.</p>
                </div>

                <form action="/crear" method="post" enctype="multipart/form-data" id="createForm" novalidate>
                    <input type="hidden" name="language" id="language" value="{initial_language}">
                    <input type="hidden" name="photo_upload_session" id="photo_upload_session" value="">
                    <div class="form-step active" id="formStep1">
                        <div class="atmosphere-title">Primero construimos el recuerdo. Luego decidimos cómo vuelve.</div>

                    <div class="section s1">
                        <div class="section-title">Quién lo crea</div>
                        <input name="customer_name" id="customer_name" placeholder="Tu nombre" required>
                        <input name="customer_email" id="customer_email" type="email" placeholder="Tu email" required>

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

                                <input
                                    type="email"
                                    name="recipient_email"
                                    id="recipient_email"
                                    class="phone-input"
                                    placeholder="Su email (opcional, por si el SMS falla)"
                                    autocomplete="email"
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

                    
                    
                    
                    <div class="section s-occasion">
                        <div class="section-title">¿Para quién es esta ETERNA?</div>
                        <div class="soft-copy">Elige una ocasión. Solo nos ayuda a entender el tono. No complica el proceso.</div>
                        <div class="emotion-grid occasion-grid" id="occasionGrid" style="margin-top:14px;">
                            <div class="emotion-card selected" data-occasion="pareja"><div class="emotion-title">❤️ Pareja</div><div class="emotion-sub">Amor, aniversario o algo que no sabes decir.</div></div>
                            <div class="emotion-card" data-occasion="madre"><div class="emotion-title">👩 Madre</div><div class="emotion-sub">Para agradecer todo lo que siempre estuvo.</div></div>
                            <div class="emotion-card" data-occasion="padre"><div class="emotion-title">👨 Padre</div><div class="emotion-sub">Para reconocer lo que a veces no se dice.</div></div>
                            <div class="emotion-card" data-occasion="cumpleanos"><div class="emotion-title">🎂 Cumpleaños</div><div class="emotion-sub">Una sorpresa que se vive de verdad.</div></div>
                            <div class="emotion-card" data-occasion="amistad"><div class="emotion-title">🤝 Amistad</div><div class="emotion-sub">Para alguien que siempre estuvo cerca.</div></div>
                            <div class="emotion-card" data-occasion="distancia"><div class="emotion-title">🌍 A distancia</div><div class="emotion-sub">Cuando está lejos, pero sigue aquí.</div></div>
                            <div class="emotion-card" data-occasion="otro"><div class="emotion-title">✨ Otro momento</div><div class="emotion-sub">Cuando simplemente quieres emocionar.</div></div>
                        </div>
                        <input type="hidden" name="occasion_type" id="occasionType" value="pareja">
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
                            Elige 6 fotos directamente desde tu galería. Se cargan de forma nativa para que el proceso sea rápido.
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
                                    <input type="file" name="photo1" id="photo1" accept="image/*">
                                </label>
                                <div class="photo-status" id="status_photo1">Pendiente</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 2</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo2">
                                    <div class="photo-placeholder" id="placeholder_photo2">Cambiar</div>
                                    <input type="file" name="photo2" id="photo2" accept="image/*">
                                </label>
                                <div class="photo-status" id="status_photo2">Pendiente</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 3</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo3">
                                    <div class="photo-placeholder" id="placeholder_photo3">Cambiar</div>
                                    <input type="file" name="photo3" id="photo3" accept="image/*">
                                </label>
                                <div class="photo-status" id="status_photo3">Pendiente</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 4</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo4">
                                    <div class="photo-placeholder" id="placeholder_photo4">Cambiar</div>
                                    <input type="file" name="photo4" id="photo4" accept="image/*">
                                </label>
                                <div class="photo-status" id="status_photo4">Pendiente</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 5</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo5">
                                    <div class="photo-placeholder" id="placeholder_photo5">Cambiar</div>
                                    <input type="file" name="photo5" id="photo5" accept="image/*">
                                </label>
                                <div class="photo-status" id="status_photo5">Pendiente</div>
                            </div>

                            <div class="photo-card">
                                <div class="photo-label">Foto 6</div>
                                <label class="photo-box">
                                    <img class="photo-preview" id="preview_photo6">
                                    <div class="photo-placeholder" id="placeholder_photo6">Cambiar</div>
                                    <input type="file" name="photo6" id="photo6" accept="image/*">
                                </label>
                                <div class="photo-status" id="status_photo6">Pendiente</div>
                            </div>

                        </div>

                        <div class="mini-note">
                            Recomendación: formato vertical. Lo importante es que sean recuerdos que de verdad tengan sentido.
                        </div>

                        <div class="trust-box" style="margin-top:14px;padding:14px;border-radius:18px;background:rgba(255,255,255,0.045);border:1px solid rgba(218,178,92,0.20);color:rgba(255,255,255,0.76);font-size:13px;line-height:1.65;">
                            <b style="color:#f5d28b;">¿Quieres que la persona sepa quién le envía esta ETERNA?</b><br>
                            <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;">
                                <label style="display:flex;align-items:center;gap:7px;">
                                    <input type="radio" name="show_sender_identity" value="1" id="show_sender_identity_yes">
                                    Sí, mostrar una foto
                                </label>
                                <label style="display:flex;align-items:center;gap:7px;">
                                    <input type="radio" name="show_sender_identity" value="0" id="show_sender_identity_no" checked>
                                    No, mantener la sorpresa
                                </label>
                            </div>
                            <div id="arrivalPhotoSelector" class="hidden" style="margin-top:12px;">
                                <div style="margin-bottom:8px;color:rgba(255,255,255,.72);">Foto de llegada:</div>
                                <select name="arrival_photo_slot" id="arrival_photo_slot" style="width:100%;padding:12px;border-radius:14px;border:1px solid rgba(245,210,139,.24);background:#07111c;color:#fff;">
                                    <option value="photo1" selected>Foto 1</option>
                                    <option value="photo2">Foto 2</option>
                                    <option value="photo3">Foto 3</option>
                                    <option value="photo4">Foto 4</option>
                                    <option value="photo5">Foto 5</option>
                                    <option value="photo6">Foto 6</option>
                                </select>
                                <div style="margin-top:8px;color:rgba(255,255,255,.58);font-size:12px;">
                                    Esta mini foto puede aparecer como imagen de llegada para dar confianza. No cambia el vídeo.
                                </div>
                            </div>
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

                        <div class="trust-box" style="margin-top:14px;padding:14px;border-radius:18px;background:rgba(255,255,255,0.045);border:1px solid rgba(218,178,92,0.20);color:rgba(255,255,255,0.76);font-size:13px;line-height:1.65;">
                            <b style="color:#f5d28b;">¿Necesitas inspiración?</b><br>
                            <button type="button" id="inspirationBtn" style="margin:10px 0 8px;padding:10px 14px;border-radius:999px;border:1px solid rgba(245,210,139,.32);background:rgba(245,210,139,.08);color:#f5d28b;font-weight:800;">Ver frases sugeridas</button>
                            <div id="inspirationBox" class="hidden" style="margin-top:8px;">
                                <div class="suggested-phrase">Gracias por estar siempre.</div>
                                <div class="suggested-phrase">Hay personas que se quedan para siempre.</div>
                                <div class="suggested-phrase">Hoy quería recordarte algo bonito.</div>
                                <div class="suggested-phrase">Aunque estemos lejos, sigues aquí.</div>
                                <div class="suggested-phrase">Nunca olvides lo importante que eres para mí.</div>
                            </div>
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

                        <div class="trust-box" style="
                            margin-top:16px;
                            padding:16px;
                            border-radius:18px;
                            background:linear-gradient(135deg, rgba(255,215,128,0.10), rgba(80,190,255,0.07));
                            border:1px solid rgba(218,178,92,0.24);
                            color:rgba(255,255,255,0.78);
                            font-size:13px;
                            line-height:1.75;
                        ">
                            <b style="color:#f5d28b;">Privado y seguro</b><br>
                            ✓ Tus fotos son privadas.<br>
                            ✓ El pago se realiza de forma segura con Stripe.<br>
                            ✓ La reacción solo vuelve a quien crea esta ETERNA.<br>
                            ✓ Si añades dinero, lo recibirá la persona destinataria.<br>
                            ✓ Soporte: hola@tueterna.com · +34 641 63 53 14
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

    // RC108 INTERNATIONAL SAFE — solo formulario + mensajes de envío.
    // No toca Stripe, Twilio, WhatsApp, Video Engine, Sender Pack ni reacciones.
    const I18N = {{
        es: {{
            subtitle: "Crea algo que no se abra. Se viva.",
            intro1: "No todo lo importante", intro2: "debería desaparecer.", intro3: "Haz que vuelva convertido", intro4: "en emoción real.",
            atmosphere1: "Primero construimos el recuerdo. Luego decidimos cómo vuelve.",
            atmosphere2: "Ahora dale intención: palabras, momento de entrega y pago seguro.",
            creator: "Quién lo crea", recipient: "Quién lo va a vivir", occasionTitle: "¿Para quién es esta ETERNA?", yulTitle: "El alma de Yul", emotionTitle: "Qué quieres provocar", wordsTitle: "Las palabras", exactMoment: "El momento exacto", giftTitle: "El regalo", photosTitle: "Los recuerdos",
            customerName: "Tu nombre", customerEmail: "Tu email", customerPhone: "Tu teléfono", recipientName: "Su nombre", recipientPhone: "Su teléfono", recipientEmail: "Su email (opcional, por si el SMS falla)",
            phoneHelp: "Escríbelo como lo tengas guardado 💛<br>No hace falta poner el prefijo.",
            occasionCopy: "Elige una ocasión. Solo nos ayuda a entender el tono. No complica el proceso.",
            yulCopy: "Una sola pista. Un lugar. Yul no necesita saber más para encontrar una puerta.",
            yulQuestion: "¿Hay algún lugar que forme parte de vuestra historia?",
            yulPlaceholder: "Ej: Cádiz, la montaña, la casa de la abuela, un banco, París...",
            yulNote: "No expliques el recuerdo. Solo escribe el lugar. Yul hará el resto.",
            photosCopy: "Elige entre 4 y 6 fotos desde tu galería. ETERNA las optimiza automáticamente para que carguen mejor en móvil.",
            pickerTitle: "Seleccionar recuerdos",
            pickerSub: "Puedes elegir varias fotos de una vez. Después podrás cambiar cualquiera individualmente.",
            openGallery: "Abrir galería",
            photo: "Foto",
            change: "Cambiar",
            pending: "Pendiente",
            photoNote: "Recomendación: formato vertical. Lo importante es que sean recuerdos que de verdad tengan sentido.",
            senderIdentityQuestion: "¿Quieres que la persona sepa quién le envía esta ETERNA?",
            senderIdentityYes: "Sí, mostrar una foto",
            senderIdentityNo: "No, mantener la sorpresa",
            arrivalPhoto: "Foto de llegada:",
            arrivalPhotoNote: "Esta mini foto puede aparecer como imagen de llegada para dar confianza. No cambia el vídeo.",
            phrase1: "Lo que nunca quieres que olvide", phrase2: "Eso que sientes y a veces no dices", phrase3: "La frase que quieres dejarle para siempre",
            autoWords: "Quiero que ETERNA encuentre las palabras", manualWords: "Quiero escribir lo que siento", recommended: "(recomendado)",
            inspirationTitle: "¿Necesitas inspiración?", inspirationBtn: "Ver frases sugeridas",
            suggested1: "Gracias por estar siempre.", suggested2: "Hay personas que se quedan para siempre.", suggested3: "Hoy quería recordarte algo bonito.", suggested4: "Aunque estemos lejos, sigues aquí.", suggested5: "Nunca olvides lo importante que eres para mí.",
            deliveryCopy: "Puedes dejar que llegue en cuanto esté lista...<br>o programar ese momento íntimo en el que sabes que podrá vivirla de verdad.",
            deliveryInstant: "Enviarlo en cuanto esté listo", deliveryInstantSub: "Sin coste extra.", deliveryScheduled: "Guardarlo y entregarlo en un momento exacto", deliveryScheduledSub: "+{money(SCHEDULED_DELIVERY_FEE)}€ para guardarlo y hacer que llegue exactamente cuando tú elijas.",
            deliveryHint: "Lo ideal es que pueda vivirlo con calma.<br>Con unos cascos. En silencio. Sin que nadie le moleste.",
            giftAmountTitle: "Dinero a regalar", giftAmountPlaceholder: "Dinero a regalar (€)",
            priceBox: "Precio base ETERNA: {money(BASE_PRICE)}€<br>Si añades regalo económico: +{money(FIXED_PLATFORM_FEE)}€ gestión segura + {(GIFT_COMMISSION_RATE * 100):.0f}% del importe regalado<br>Entrega programada: +{money(SCHEDULED_DELIVERY_FEE)}€ solo si eliges guardarlo y entregarlo en un momento exacto",
            trustTitle: "Privado y seguro", trust1: "✓ Tus fotos son privadas.", trust2: "✓ El pago se realiza de forma segura con Stripe.", trust3: "✓ La reacción solo vuelve a quien crea esta ETERNA.", trust4: "✓ Si añades dinero, lo recibirá la persona destinataria.", trust5: "✓ Soporte: hola@tueterna.com · +34 641 63 53 14",
            finalHint: "No solo eliges lo que va a sentir. También eliges cuándo debe ocurrir.",
            responsibleText: "Acepto crear esta ETERNA de forma responsable. Entiendo que, si la persona destinataria vive la experiencia, podré recibir un recuerdo privado de ese momento. Me comprometo a tratar ese contenido con respeto, a no utilizarlo de forma ofensiva, invasiva o pública, y a compartirlo solo de manera responsable.",
            legalText: "Al continuar, aceptas las <a href=\"/condiciones\" target=\"_blank\" style=\"color:#fff7e6;text-decoration:underline;\">condiciones</a> y la <a href=\"/privacidad\" target=\"_blank\" style=\"color:#fff7e6;text-decoration:underline;\">política de privacidad</a>.",
            submit: "Crear y pasar al pago seguro",
            photosUploading: "Las fotos se están cargando. Espera unos segundos: el pago se desbloqueará automáticamente.",
            photosPreparing: "Estamos preparando tus fotos. El pago se desbloqueará automáticamente cuando estén listas.",
            need4Photos: "Sube al menos 4 fotos. El pago se desbloqueará cuando estén subidas.",
            reviewFields: "Revisa los campos. Falta algún dato.", acceptResponsible: "Antes de continuar debes aceptar el uso responsable de ETERNA.", selectEmotion: "Elige una emoción para continuar.", write3: "Escribe tus 3 frases.", deliveryDate: "Elige la fecha y hora de entrega.", badDate: "La fecha de entrega no es válida.", futureDate: "La fecha de entrega debe ser futura.", badAmount: "El importe no es válido.", openingCheckout: "Abriendo pago seguro...", firstStepMissing: "Falta completar los datos principales antes de continuar.", need6Photos: "Necesitas elegir las 6 fotos antes de continuar.", genericError: "Ha ocurrido un error.",
            photoOptional: "Opcional si ya tienes 4 fotos.", photoOptionalRepeat: "Opcional: ETERNA puede repetir una foto.", photoRequired: "Necesaria para crear tu ETERNA.", photoUploaded: "Foto subida ✓", photoReady: "Foto lista ✓", optimizingPhoto: "Optimizando foto para ETERNA...", photoPreparedUploading: "Foto preparada. Subiendo...", photoPrepareError: "Esta foto no se ha podido preparar. Prueba con otra.", photoTryAnother: "Una foto no se ha podido preparar. Prueba con otra imagen o una captura.", photoRecovered: "Foto recuperada y subida ✓", photoTapAgain: "Toca esta foto otra vez para subirla.", photoLoading: "Subiendo foto...", photosPreparingButton: "PREPARANDO FOTOS...", uploadAtLeast4Button: "SUBE AL MENOS 4 FOTOS", continuePaymentButton: "CONTINUAR AL PAGO", continuePaymentCompleteButton: "CONTINUAR AL PAGO · ETERNA COMPLETARÁ LAS 6", photoPreparingHint: "Preparando tus fotos para que pesen menos. En cuanto haya 4 listas podrás continuar.", photoMinimumHint: "Sube al menos 4 fotos. Si no tienes 6, ETERNA repetirá alguna de forma discreta.", photoSixReadyHint: "6 fotos listas. Puedes continuar al pago.", photoPartialReadyHint: "{{count}} fotos listas. ETERNA completará las 6 repitiendo alguna de forma discreta.", formNativeFallback: "Enviando tus fotos de forma segura...",
            occasions: {{
                pareja: ["❤️ Pareja", "Amor, aniversario o algo que no sabes decir."], madre: ["👩 Madre", "Para agradecer todo lo que siempre estuvo."], padre: ["👨 Padre", "Para reconocer lo que a veces no se dice."], cumpleanos: ["🎂 Cumpleaños", "Una sorpresa que se vive de verdad."], amistad: ["🤝 Amistad", "Para alguien que siempre estuvo cerca."], distancia: ["🌍 A distancia", "Cuando está lejos, pero sigue aquí."], otro: ["✨ Otro momento", "Cuando simplemente quieres emocionar."]
            }},
            emotions: {{
                cumpleanos: ["Cumpleaños", "Un día que merece quedarse."], amor: ["Amor", "Cuando lo que sientes ya no cabe dentro."], madre: ["Mamá", "Para quien siempre fue hogar."], padre: ["Papá", "Para quien dejó huella sin hacer ruido."], familia: ["Familia", "Para quienes siempre vuelven a ti."], amistad: ["Amistad", "Para esa persona que se quedó."], distancia: ["Distancia", "Cuando alguien está lejos, pero sigue cerca."], perdon: ["Perdón", "Para decir algo que cuesta decir."], reencuentro: ["Reencuentro", "Cuando algo vuelve después del tiempo."], gratitud: ["Gracias", "Para agradecer de verdad."], superacion: ["Superación", "Para recordarle todo lo que vale."], sorpresa: ["Sorpresa", "Cuando quieres tocar el corazón sin avisar."], esfuerzo: ["Esfuerzo", "Para reconocer lo que a veces no se dice."], no_se_decirlo: ["No sé cómo decirlo", "Cuando ETERNA debe decirlo por ti."]
            }}
        }},
        en: {{
            subtitle: "Create something that is not opened. It is felt.",
            intro1: "Not everything important", intro2: "should disappear.", intro3: "Make it come back", intro4: "as real emotion.",
            atmosphere1: "First we build the memory. Then we decide how it returns.",
            atmosphere2: "Now give it intention: words, delivery moment and secure payment.",
            creator: "Who creates it", recipient: "Who will experience it", occasionTitle: "Who is this ETERNA for?", yulTitle: "Yul's soul", emotionTitle: "What do you want to awaken?", wordsTitle: "The words", exactMoment: "The exact moment", giftTitle: "The gift", photosTitle: "The memories",
            customerName: "Your name", customerEmail: "Your email", customerPhone: "Your phone", recipientName: "Their name", recipientPhone: "Their phone", recipientEmail: "Their email (optional, in case SMS fails)",
            phoneHelp: "Write it as you have it saved 💛<br>You do not need to add the country code here.",
            occasionCopy: "Choose an occasion. It only helps us understand the tone. It does not complicate the process.",
            yulCopy: "One clue. One place. Yul does not need more to find a door.",
            yulQuestion: "Is there a place that is part of your story?",
            yulPlaceholder: "Example: Paris, the beach, grandma's house, a bench, London...",
            yulNote: "Do not explain the memory. Just write the place. Yul will do the rest.",
            photosCopy: "Choose between 4 and 6 photos from your gallery. ETERNA optimizes them automatically so they load better on mobile.",
            pickerTitle: "Select memories",
            pickerSub: "You can choose several photos at once. Afterwards, you can change any of them individually.",
            openGallery: "Open gallery",
            photo: "Photo",
            change: "Change",
            pending: "Pending",
            photoNote: "Recommendation: vertical format. What matters is that they are memories that truly mean something.",
            senderIdentityQuestion: "Do you want the person to know who sent this ETERNA?",
            senderIdentityYes: "Yes, show a photo",
            senderIdentityNo: "No, keep the surprise",
            arrivalPhoto: "Arrival photo:",
            arrivalPhotoNote: "This small photo can appear as the arrival image to build trust. It does not change the video.",
            phrase1: "What you never want them to forget", phrase2: "What you feel but do not always say", phrase3: "The sentence you want to leave forever",
            autoWords: "I want ETERNA to find the words", manualWords: "I want to write what I feel", recommended: "(recommended)",
            inspirationTitle: "Need inspiration?", inspirationBtn: "See suggested messages",
            suggested1: "Thank you for always being there.", suggested2: "Some people stay forever.", suggested3: "Today I wanted to remind you of something beautiful.", suggested4: "Even if we are far apart, you are still here.", suggested5: "Never forget how important you are to me.",
            deliveryCopy: "You can send it as soon as it is ready...<br>or schedule that intimate moment when you know they will truly be able to experience it.",
            deliveryInstant: "Send it as soon as it is ready", deliveryInstantSub: "No extra cost.", deliveryScheduled: "Save it and deliver it at an exact moment", deliveryScheduledSub: "+{money(SCHEDULED_DELIVERY_FEE)}€ to save it and make it arrive exactly when you choose.",
            deliveryHint: "Ideally, they should experience it calmly.<br>With headphones. In silence. Without anyone disturbing them.",
            giftAmountTitle: "Gift money", giftAmountPlaceholder: "Gift money (€)",
            priceBox: "Base ETERNA price: {money(BASE_PRICE)}€<br>If you add gift money: +{money(FIXED_PLATFORM_FEE)}€ secure handling + {(GIFT_COMMISSION_RATE * 100):.0f}% of the gifted amount<br>Scheduled delivery: +{money(SCHEDULED_DELIVERY_FEE)}€ only if you choose to save it and deliver it at an exact moment",
            trustTitle: "Private and secure", trust1: "✓ Your photos are private.", trust2: "✓ Payment is processed securely with Stripe.", trust3: "✓ The reaction only returns to the person who creates this ETERNA.", trust4: "✓ If you add money, the recipient will receive it.", trust5: "✓ Support: hola@tueterna.com · +34 641 63 53 14",
            finalHint: "You do not only choose what they will feel. You also choose when it should happen.",
            responsibleText: "I accept creating this ETERNA responsibly. I understand that, if the recipient experiences it, I may receive a private memory of that moment. I commit to treating that content with respect, not using it in an offensive, invasive or public way, and sharing it only responsibly.",
            legalText: "By continuing, you accept the <a href=\"/condiciones\" target=\"_blank\" style=\"color:#fff7e6;text-decoration:underline;\">terms</a> and the <a href=\"/privacidad\" target=\"_blank\" style=\"color:#fff7e6;text-decoration:underline;\">privacy policy</a>.",
            submit: "Create and continue to secure payment",
            photosUploading: "Photos are uploading. Please wait a few seconds: payment will unlock automatically.",
            photosPreparing: "We are preparing your photos. Payment will unlock automatically when they are ready.",
            need4Photos: "Upload at least 4 photos. Payment will unlock when they are uploaded.",
            reviewFields: "Please review the fields. Some information is missing.", acceptResponsible: "Before continuing, you must accept ETERNA's responsible use.", selectEmotion: "Select an emotion to continue.", write3: "Write your 3 messages.", deliveryDate: "Choose the delivery date and time.", badDate: "The delivery date is not valid.", futureDate: "The delivery date must be in the future.", badAmount: "The amount is not valid.", openingCheckout: "Opening secure checkout...", firstStepMissing: "Please complete the main details before continuing.", need6Photos: "You need to choose the 6 photos before continuing.", genericError: "Something went wrong.",
            photoOptional: "Optional if you already have 4 photos.", photoOptionalRepeat: "Optional: ETERNA can repeat one photo.", photoRequired: "Required to create your ETERNA.", photoUploaded: "Photo uploaded ✓", photoReady: "Photo ready ✓", optimizingPhoto: "Optimizing photo for ETERNA...", photoPreparedUploading: "Photo prepared. Uploading...", photoPrepareError: "This photo could not be prepared. Try another one.", photoTryAnother: "A photo could not be prepared. Try another image or a screenshot.", photoRecovered: "Photo recovered and uploaded ✓", photoTapAgain: "Tap this photo again to upload it.", photoLoading: "Uploading photo...", photosPreparingButton: "PREPARING PHOTOS...", uploadAtLeast4Button: "UPLOAD AT LEAST 4 PHOTOS", continuePaymentButton: "CONTINUE TO PAYMENT", continuePaymentCompleteButton: "CONTINUE TO PAYMENT · ETERNA WILL COMPLETE THE 6", photoPreparingHint: "Preparing your photos so they load faster. As soon as 4 are ready, you can continue.", photoMinimumHint: "Upload at least 4 photos. If you do not have 6, ETERNA will discreetly repeat one.", photoSixReadyHint: "6 photos ready. You can continue to payment.", photoPartialReadyHint: "{{count}} photos ready. ETERNA will complete the 6 by discreetly repeating one.", formNativeFallback: "Sending your photos securely...",
            occasions: {{
                pareja: ["❤️ Partner", "Love, anniversary or something you do not know how to say."], madre: ["👩 Mother", "To thank everything that was always there."], padre: ["👨 Father", "To recognize what is not always said."], cumpleanos: ["🎂 Birthday", "A surprise that is truly experienced."], amistad: ["🤝 Friendship", "For someone who was always close."], distancia: ["🌍 Long distance", "When they are far away, but still here."], otro: ["✨ Another moment", "When you simply want to move someone."]
            }},
            emotions: {{
                cumpleanos: ["Birthday", "A day that deserves to stay."], amor: ["Love", "When what you feel no longer fits inside."], madre: ["Mother", "For the person who has always felt like home."], padre: ["Father", "For the person who left a mark quietly."], familia: ["Family", "For the people who always come back to you."], amistad: ["Friendship", "For that person who stayed."], distancia: ["Distance", "When someone is far away, but still close."], perdon: ["Apology", "To say something that is hard to say."], reencuentro: ["Reunion", "When something returns after time."], gratitud: ["Thank you", "To truly say thank you."], superacion: ["Encouragement", "To remind them of everything they are worth."], sorpresa: ["Surprise", "When you want to touch their heart without warning."], esfuerzo: ["Effort", "To recognize what is not always said."], no_se_decirlo: ["I do not know how to say it", "When ETERNA should say it for you."]
            }}
        }}
    }};

    function currentLang() {{
        const input = document.getElementById("language");
        const raw = (input && input.value ? input.value : localStorage.getItem("eterna_language") || "es").toLowerCase();
        return raw === "en" ? "en" : "es";
    }}

    function tr(key) {{
        const lang = currentLang();
        return (I18N[lang] && I18N[lang][key]) || (I18N.es && I18N.es[key]) || key;
    }}

    function setTextBySelector(selector, value) {{
        const el = document.querySelector(selector);
        if (el) el.textContent = value;
    }}


    function setHTMLBySelector(selector, value) {{
        const el = document.querySelector(selector);
        if (el) el.innerHTML = value;
    }}

    function setAllTextBySelector(selector, values) {{
        const nodes = Array.from(document.querySelectorAll(selector));
        nodes.forEach(function(el, index) {{
            if (values[index] !== undefined) el.textContent = values[index];
        }});
    }}

    function normalizeTextForI18n(value) {{
        return String(value || "").replace(/\s+/g, " ").trim();
    }}

    function replaceExactTextNodes(map) {{
        try {{
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
            const nodes = [];
            while (walker.nextNode()) nodes.push(walker.currentNode);
            nodes.forEach(function(node) {{
                const raw = node.nodeValue || "";
                const key = normalizeTextForI18n(raw);
                if (!key || !map[key]) return;
                const prefix = (raw.match(/^\s*/) || [""])[0];
                const suffix = (raw.match(/\s*$/) || [""])[0];
                node.nodeValue = prefix + map[key] + suffix;
            }});
        }} catch (e) {{ console.warn("RC112F replaceExactTextNodes skipped", e); }}
    }}

    function translateExactTextNodes(lang) {{
        if (lang !== "en") return;
        replaceExactTextNodes({{
            "Primero construimos el recuerdo. Luego decidimos cómo vuelve.": "First we build the memory. Then we decide how it returns.",
            "Quién lo crea": "Who creates it",
            "Quién lo va a vivir": "Who will live it",
            "Cuándo simplemente quieres emocionar.": "When you simply want to move someone.",
            "El alma de Yul": "Yul's soul",
            "Una sola pista. Un lugar. Yul no necesita saber más para encontrar una puerta.": "One clue. One place. Yul does not need more to find a doorway.",
            "¿Hay algún lugar que forme parte de vuestra historia?": "Is there a place that belongs to your story?",
            "No expliques el recuerdo. Solo escribe el lugar. Yul hará el resto.": "Do not explain the memory. Just write the place. Yul will do the rest.",
            "Los recuerdos": "The memories",
            "Qué quieres provocar": "Type of emotion",
            "Cumpleaños": "Birthday",
            "Un día que merece quedarse.": "A day worth keeping.",
            "Amor": "Love",
            "Cuando lo que sientes ya no cabe dentro.": "When what you feel no longer fits inside.",
            "Mamá": "Mom",
            "Para quien siempre fue hogar.": "For the one who was always home.",
            "Papá": "Dad",
            "Para quien dejó huella sin hacer ruido.": "For the one who left a mark quietly.",
            "Familia": "Family",
            "Para quienes siempre vuelven a ti.": "For those who always come back to you.",
            "Amistad": "Friendship",
            "Para esa persona que se quedó.": "For the person who stayed.",
            "Distancia": "Distance",
            "Cuando alguien está lejos, pero sigue cerca.": "When someone is far away, but still close.",
            "Perdón": "Forgiveness",
            "Para decir algo que cuesta decir.": "To say something hard to say.",
            "Reencuentro": "Reunion",
            "Cuando algo vuelve después del tiempo.": "When something returns after time.",
            "Gracias": "Thank you",
            "Para agradecer de verdad.": "To truly say thank you.",
            "Superación": "Overcoming",
            "Para recordarle todo lo que vale.": "To remind them how much they are worth.",
            "Sorpresa": "Surprise",
            "Cuando quieres tocar el corazón sin avisar.": "When you want to touch their heart without warning.",
            "Esfuerzo": "Effort",
            "Para reconocer lo que a veces no se dice.": "To recognize what is not always said.",
            "No sé cómo decirlo": "I do not know how to say it",
            "Cuando ETERNA debe decirlo por ti.": "When ETERNA should say it for you.",
            "Ahora dale intención: palabras, momento de entrega y pago seguro.": "Now give it intention: words, delivery moment and secure payment.",
            "Las palabras": "Your words",
            "Quiero que ETERNA encuentre las palabras": "I want ETERNA to find the words",
            "(recomendado)": "(recommended)",
            "Quiero escribir lo que siento": "I want to write what I feel",
            "¿Necesitas inspiración?": "Need inspiration?",
            "Ver frases sugeridas": "See suggested phrases",
            "Gracias por estar siempre.": "Thank you for always being there.",
            "Hay personas que se quedan para siempre.": "Some people stay forever.",
            "Hoy quería recordarte algo bonito.": "Today I wanted to remind you of something beautiful.",
            "Aunque estemos lejos, sigues aquí.": "Even if we are far apart, you are still here.",
            "Nunca olvides lo importante que eres para mí.": "Never forget how important you are to me.",
            "El momento exacto": "The exact moment",
            "Puedes dejar que llegue en cuanto esté lista... o programar ese momento íntimo en el que sabes que podrá vivirla de verdad.": "You can let it arrive as soon as it is ready... or schedule that intimate moment when you know they will truly be able to live it.",
            "Enviarlo en cuanto esté listo": "Send it as soon as it is ready",
            "Sin coste extra.": "No extra cost.",
            "Guardarlo y entregarlo en un momento exacto": "Save it and deliver it at an exact moment",
            "Dinero a regalar": "Gift amount",
            "Precio base ETERNA: 1.00€": "Base ETERNA price: €1.00",
            "Privado y seguro": "Private and secure",
            "✓ Tus fotos son privadas.": "✓ Your photos are private.",
            "✓ El pago se realiza de forma segura con Stripe.": "✓ Payment is processed securely with Stripe.",
            "✓ La reacción solo vuelve a quien crea esta ETERNA.": "✓ The reaction only returns to the person who creates this ETERNA.",
            "✓ Si añades dinero, lo recibirá la persona destinataria.": "✓ If you add money, the recipient will receive it.",
            "No solo eliges lo que va a sentir. También eliges cuándo debe ocurrir.": "You do not only choose what they will feel. You also choose when it should happen.",
            "Acepto crear esta ETERNA de forma responsable. Entiendo que, si la persona destinataria vive la experiencia, podré recibir un recuerdo privado de ese momento. Me comprometo a tratar ese contenido con respeto, a no utilizarlo de forma ofensiva, invasiva o pública, y a compartirlo solo de manera responsable.": "I accept creating this ETERNA responsibly. I understand that, if the recipient experiences it, I may receive a private memory of that moment. I commit to treating that content with respect, not using it in an offensive, invasive or public way, and sharing it only responsibly.",
            "Al continuar, aceptas las": "By continuing, you accept the",
            "condiciones": "terms",
            "política de privacidad": "privacy policy"
        }});
    }}

    function translateCards(lang) {{
        const dict = I18N[lang] || I18N.es;
        document.querySelectorAll('[data-occasion]').forEach(function(card) {{
            const key = card.getAttribute('data-occasion');
            const val = dict.occasions && dict.occasions[key];
            if (!val) return;
            const title = card.querySelector('.emotion-title');
            const sub = card.querySelector('.emotion-sub');
            if (title) title.textContent = val[0];
            if (sub) sub.textContent = val[1];
        }});
        document.querySelectorAll('[data-type]').forEach(function(card) {{
            const key = card.getAttribute('data-type');
            const val = dict.emotions && dict.emotions[key];
            if (!val) return;
            const title = card.querySelector('.emotion-title');
            const sub = card.querySelector('.emotion-sub');
            if (title) title.textContent = val[0];
            if (sub) sub.textContent = val[1];
        }});
    }}

    function translateStaticForm(lang) {{
        setHTMLBySelector('#phone-help', tr('phoneHelp'));
        setTextBySelector('.s-occasion .soft-copy', tr('occasionCopy'));
        setTextBySelector('.s-yul .soft-copy', tr('yulCopy'));
        const yulLabel = document.querySelector('.s-yul .field-label');
        if (yulLabel) {{
            const input = yulLabel.querySelector('input');
            yulLabel.childNodes[0].nodeValue = tr('yulQuestion') + ' ';
            if (input) input.placeholder = tr('yulPlaceholder');
        }}
        setTextBySelector('.yul-one-place-note', tr('yulNote'));
        setTextBySelector('.s3 .soft-copy', tr('photosCopy'));
        setTextBySelector('.photo-picker-title', tr('pickerTitle'));
        setTextBySelector('.photo-picker-sub', tr('pickerSub'));
        const pickerBtn = document.querySelector('.photo-picker-btn');
        if (pickerBtn) {{
            const input = pickerBtn.querySelector('input');
            pickerBtn.childNodes[0].nodeValue = tr('openGallery') + ' ';
        }}
        document.querySelectorAll('.photo-label').forEach(function(el, index) {{ el.textContent = tr('photo') + ' ' + (index + 1); }});
        document.querySelectorAll('.photo-placeholder').forEach(function(el) {{ el.textContent = tr('change'); }});
        document.querySelectorAll('.photo-status').forEach(function(el) {{ if ((el.textContent || '').trim() === 'Pendiente' || (el.textContent || '').trim() === 'Pending') el.textContent = tr('pending'); }});
        setTextBySelector('.mini-note', tr('photoNote'));
        const senderTrust = document.querySelector('.s3 .trust-box');
        if (senderTrust) {{
            const b = senderTrust.querySelector('b');
            if (b) b.textContent = tr('senderIdentityQuestion');
            const labels = senderTrust.querySelectorAll('label');
            if (labels[0]) labels[0].lastChild.nodeValue = ' ' + tr('senderIdentityYes');
            if (labels[1]) labels[1].lastChild.nodeValue = ' ' + tr('senderIdentityNo');
            const arrivalTitle = document.querySelector('#arrivalPhotoSelector > div');
            if (arrivalTitle) arrivalTitle.textContent = tr('arrivalPhoto');
            const note = document.querySelector('#arrivalPhotoSelector div[style*="font-size:12px"]');
            if (note) note.textContent = tr('arrivalPhotoNote');
        }}
        const inspirationBox = document.querySelector('.s5 .trust-box');
        if (inspirationBox) {{
            const b = inspirationBox.querySelector('b');
            if (b) b.textContent = tr('inspirationTitle');
            const btn = document.getElementById('inspirationBtn');
            if (btn) btn.textContent = tr('inspirationBtn');
            setAllTextBySelector('.suggested-phrase', [tr('suggested1'), tr('suggested2'), tr('suggested3'), tr('suggested4'), tr('suggested5')]);
        }}
        setHTMLBySelector('.delivery-copy', tr('deliveryCopy'));
        const deliveryTitles = document.querySelectorAll('.delivery-option-title');
        if (deliveryTitles[0]) deliveryTitles[0].textContent = tr('deliveryInstant');
        if (deliveryTitles[1]) deliveryTitles[1].textContent = tr('deliveryScheduled');
        const deliverySubs = document.querySelectorAll('.delivery-option-sub');
        if (deliverySubs[0]) deliverySubs[0].textContent = tr('deliveryInstantSub');
        if (deliverySubs[1]) deliverySubs[1].textContent = tr('deliveryScheduledSub');
        setHTMLBySelector('.delivery-hint', tr('deliveryHint'));
        const giftInput = document.getElementById('gift_amount');
        if (giftInput) giftInput.placeholder = tr('giftAmountPlaceholder');
        setHTMLBySelector('.price-box', tr('priceBox'));
        const trustBoxes = document.querySelectorAll('.s7 .trust-box');
        if (trustBoxes[0]) {{
            trustBoxes[0].innerHTML = '<b style="color:#f5d28b;">' + tr('trustTitle') + '</b><br>' + tr('trust1') + '<br>' + tr('trust2') + '<br>' + tr('trust3') + '<br>' + tr('trust4') + '<br>' + tr('trust5');
        }}
        setTextBySelector('.s7 .hint', tr('finalHint'));
        const resp = document.querySelector('#responsible_use_accepted')?.closest('label')?.querySelector('span');
        if (resp) resp.textContent = tr('responsibleText');
        const legal = document.querySelector('.s7 div[style*="text-align:center"]');
        if (legal) legal.innerHTML = tr('legalText');
        // RC111 LANGUAGE SWITCH SAFE — no usamos la const `button` aquí porque
        // applyLanguage() se ejecuta antes de inicializar algunas constantes del formulario.
        // Si tocamos `button` antes de tiempo, Safari/Chrome pueden romper todo el JS
        // y el selector ES/EN deja de responder.
        translateExactTextNodes(lang);
        const submitButtonSafe = document.getElementById('submitBtn');
        if (submitButtonSafe) submitButtonSafe.textContent = tr('submit');
    }}

    function applyLanguage(lang) {{
        lang = lang === "en" ? "en" : "es";
        const input = document.getElementById("language");
        if (input) input.value = lang;
        try {{ localStorage.setItem("eterna_language", lang); }} catch (e) {{}}
        document.documentElement.setAttribute("lang", lang);

        document.querySelectorAll(".language-option").forEach(function(btn) {{
            btn.classList.toggle("active", btn.getAttribute("data-lang") === lang);
        }});

        setTextBySelector('[data-i18n="subtitle"]', tr("subtitle"));
        setTextBySelector('.intro-line.l1', tr("intro1"));
        setTextBySelector('.intro-line.l2', tr("intro2"));
        setTextBySelector('.intro-line.l3', tr("intro3"));
        setTextBySelector('.intro-line.l4', tr("intro4"));

        const atmospheres = document.querySelectorAll('.atmosphere-title');
        if (atmospheres[0]) atmospheres[0].textContent = tr("atmosphere1");
        if (atmospheres[1]) atmospheres[1].textContent = tr("atmosphere2");

        const titles = Array.from(document.querySelectorAll('.section-title'));
        const titleMap = [tr("creator"), tr("recipient"), tr("occasionTitle"), tr("yulTitle"), tr("photosTitle"), tr("emotionTitle"), tr("wordsTitle"), tr("exactMoment"), tr("giftTitle")];
        titles.forEach(function(el, index) {{ if (titleMap[index]) el.textContent = titleMap[index]; }});

        const setPlaceholder = function(id, value) {{ const el = document.getElementById(id); if (el) el.placeholder = value; }};
        setPlaceholder("customer_name", tr("customerName"));
        setPlaceholder("customer_email", tr("customerEmail"));
        setPlaceholder("customer_phone", tr("customerPhone"));
        setPlaceholder("recipient_name", tr("recipientName"));
        setPlaceholder("recipient_phone", tr("recipientPhone"));
        setPlaceholder("recipient_email", tr("recipientEmail"));
        setPlaceholder("phrase_1", tr("phrase1"));
        setPlaceholder("phrase_2", tr("phrase2"));
        setPlaceholder("phrase_3", tr("phrase3"));

        const autoLabel = document.querySelector('label[for="mode_auto"]');
        if (autoLabel) autoLabel.innerHTML = tr("autoWords") + ' <span class="recommended">' + tr("recommended") + '</span>';
        const manualLabel = document.querySelector('label[for="mode_manual"]');
        if (manualLabel) manualLabel.textContent = tr("manualWords");

        translateCards(lang);
        translateStaticForm(lang);
        try {{ updatePhotoReadiness(); }} catch (e) {{}}
    }}

    document.querySelectorAll(".language-option").forEach(function(btn) {{
        btn.addEventListener("click", function(ev) {{
            const targetLang = btn.getAttribute("data-lang") || "es";
            try {{ localStorage.setItem("eterna_language", targetLang); }} catch (e) {{}}
            try {{ saveFormState(); }} catch (e) {{}}

            // RC112E: los botones de idioma son enlaces reales (/crear?lang=en).
            // No bloqueamos la navegación: si cualquier JS falla, Safari recarga
            // la página en el idioma correcto y no se queda atrapado en español.
            if (btn.tagName && btn.tagName.toLowerCase() === "a" && btn.getAttribute("href")) {{
                return true;
            }}

            try {{ if (ev) {{ ev.preventDefault(); ev.stopPropagation(); }} }} catch (_) {{}}
            try {{
                if (window.eternaHardLanguageSwitch) window.eternaHardLanguageSwitch(targetLang);
                else applyLanguage(targetLang);
            }} catch (e) {{
                console.log("ETERNA language click fallback:", e);
            }}
            return false;
        }});
    }});

    let savedLanguage = "";
    let urlLanguage = "";
    try {{
        const params = new URLSearchParams(window.location.search || "");
        const rawUrlLang = (params.get("lang") || params.get("language") || "").toLowerCase();
        if (rawUrlLang === "en" || rawUrlLang === "es") urlLanguage = rawUrlLang;
    }} catch (e) {{ urlLanguage = ""; }}
    try {{ savedLanguage = localStorage.getItem("eterna_language") || ""; }} catch (e) {{ savedLanguage = ""; }}
    const browserLanguage = (navigator.language || "").toLowerCase().startsWith("en") ? "en" : "es";
    try {{
        const initialLang = urlLanguage || savedLanguage || browserLanguage;
        // RC112F: primero aplicamos el traductor completo. El hard switch queda solo como emergencia.
        if (typeof applyLanguage === "function") applyLanguage(initialLang);
        else if (window.eternaHardLanguageSwitch) window.eternaHardLanguageSwitch(initialLang);
    }} catch (e) {{ console.log("ETERNA initial language fallback:", e); }}

    const STORAGE_KEY = "eterna_create_form_v4";

    function eternaFinalEnglishSweep() {{
        if (currentLang() !== "en") return;
        const map = {{
            "Cumpleaños":"Birthday","Mamá":"Mom","Papá":"Dad","Esfuerzo":"Effort","No sé cómo decirlo":"I do not know how to say it",
            "Quiero que ETERNA encuentre las palabras":"I want ETERNA to find the words","Quiero escribir lo que siento":"I want to write what I feel",
            "Ver frases sugeridas":"See suggested phrases","Precio base ETERNA":"Base ETERNA price","Si añades regalo económico":"If you add a money gift",
            "gestión segura":"secure handling","del importe regalado":"of the gifted amount","Entrega programada":"Scheduled delivery",
            "Privado y seguro":"Private and secure","política de privacidad":"privacy policy","condiciones":"terms",
            "Abrir galería":"Open gallery","Cambiar":"Change","Pendiente":"Pending","Foto":"Photo","Dinero a regalar":"Gift amount",
            "Crear y pasar al pago seguro":"Continue to secure payment","Al continuar, aceptas las":"By continuing, you accept the",
            "y la":"and the","Tus fotos son privadas.":"Your photos are private.","El pago se realiza de forma segura con Stripe.":"Payment is processed securely with Stripe.",
            "La reacción solo vuelve a quien crea esta ETERNA.":"The reaction only returns to the person who created this ETERNA.",
            "Si añades dinero, lo recibirá la persona destinataria.":"If you add money, the recipient will receive it.","Soporte:":"Support:"
        }};
        function replaceInTextNode(node) {{
            let v = node.nodeValue;
            if (!v || !v.trim()) return;
            for (const k in map) v = v.split(k).join(map[k]);
            node.nodeValue = v;
        }}
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {{
            acceptNode: function(node) {{
                const p = node.parentElement;
                if (!p || ["SCRIPT","STYLE"].includes(p.tagName)) return NodeFilter.FILTER_REJECT;
                return NodeFilter.FILTER_ACCEPT;
            }}
        }});
        const nodes = [];
        while (walker.nextNode()) nodes.push(walker.currentNode);
        nodes.forEach(replaceInTextNode);
        document.querySelectorAll("input,textarea").forEach(function(el){{
            if (!el.placeholder) return;
            let p = el.placeholder;
            for (const k in map) p = p.split(k).join(map[k]);
            el.placeholder = p;
        }});
    }}
    try {{ eternaFinalEnglishSweep(); setTimeout(eternaFinalEnglishSweep, 120); setTimeout(eternaFinalEnglishSweep, 800); }} catch(e) {{ console.warn("RC112H english sweep skipped", e); }}

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
                showError(tr("firstStepMissing"));
                try {{ el.focus(); }} catch (e) {{}}
                return false;
            }}
        }}
        const messageType = messageTypeInput ? messageTypeInput.value.trim() : "";
        if (!messageType) {{
            showError(tr("selectEmotion"));
            scrollToEmotionChoice();
            return false;
        }}
        if (!allPhotosPresent()) {{
            showError(tr("need4Photos"));
            return false;
        }}
        clearError();
        return true;
    }}

    // Flujo one-page: sin botón intermedio ni saltos arriba.

    function showError(message) {{
        if (!errorBox) return;
        errorBox.style.display = "block";
        errorBox.innerText = message || tr("genericError");
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

    const occasionCards = document.querySelectorAll("#occasionGrid .emotion-card");
    const occasionInput = document.getElementById("occasionType");
    occasionCards.forEach((card) => {{
        card.addEventListener("click", () => {{
            occasionCards.forEach((c) => c.classList.remove("selected"));
            card.classList.add("selected");
            if (occasionInput) occasionInput.value = card.dataset.occasion || "otro";
            saveFormState();
        }});
    }});

    const inspirationBtn = document.getElementById("inspirationBtn");
    const inspirationBox = document.getElementById("inspirationBox");
    if (inspirationBtn && inspirationBox) {{
        inspirationBtn.addEventListener("click", () => {{
            inspirationBox.classList.toggle("hidden");
        }});
        inspirationBox.querySelectorAll(".suggested-phrase").forEach((el) => {{
            el.style.cursor = "pointer";
            el.style.padding = "8px 0";
            el.addEventListener("click", () => {{
                const manual = document.getElementById("mode_manual");
                if (manual) {{ manual.checked = true; manual.dispatchEvent(new Event("change")); }}
                const targets = ["phrase_1", "phrase_2", "phrase_3"].map(id => document.getElementById(id));
                const empty = targets.find(t => t && !String(t.value || "").trim());
                if (empty) {{ empty.value = el.textContent.trim(); empty.focus(); saveFormState(); }}
            }});
        }});
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
            recipient_email: document.getElementById("recipient_email")?.value || "",
            show_sender_identity: document.querySelector('input[name="show_sender_identity"]:checked')?.value || "0",
            arrival_photo_slot: document.getElementById("arrival_photo_slot")?.value || "photo1",
            occasion_type: document.getElementById("occasionType")?.value || "",
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
            const data = getPersistableData();
            data.__saved_at = Date.now();
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
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
                "recipient_email",
                "arrival_photo_slot",
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
            "#recipient_email",
            "#show_sender_identity_yes",
            "#show_sender_identity_no",
            "#arrival_photo_slot",
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

    // =====================================================
    // RC91 — BLINDAJE FOTOS IPHONE / SAFARI / INSTAGRAM
    // Solo afecta al formulario /crear.
    // Objetivo: nunca mandar fotos gigantes al navegador/backend.
    // =====================================================
    const ETERNA_PHOTO_IDS = ["photo1", "photo2", "photo3", "photo4", "photo5", "photo6"];
    const ETERNA_PHOTO_MAX_SIDE = 1280;
    const ETERNA_PHOTO_QUALITY = 0.72;
    const ETERNA_PHOTO_DB = "eterna_photo_draft_v1";
    const ETERNA_PHOTO_STORE = "photos";
    const ETERNA_OPTIMIZED_PREFIX = "eterna_optimized_";
    const photoObjectUrls = {{}};
    const photoProcessing = {{}};
    const photoUploaded = {{}};
    const photoUploadErrors = {{}};
    // RC112C: memoria segura de fotos por slot.
    // Si Safari/Instagram no permite DataTransfer/input.files, no perdemos la foto:
    // la enviamos por FormData manual solo en ese caso.
    const photoNativeFiles = {{}};
    const photoNativeAssigned = {{}};
    const photoUploadSessionInput = document.getElementById("photo_upload_session");

    function getPhotoUploadSession() {{
        let value = photoUploadSessionInput ? String(photoUploadSessionInput.value || "").trim() : "";
        if (!value) {{
            try {{
                value = (window.crypto && crypto.randomUUID)
                    ? crypto.randomUUID()
                    : ("sess_" + Date.now() + "_" + Math.random().toString(16).slice(2));
            }} catch (e) {{
                value = "sess_" + Date.now() + "_" + Math.random().toString(16).slice(2);
            }}
            if (photoUploadSessionInput) photoUploadSessionInput.value = value;
        }}
        return value;
    }}

    function countPreuploadedPhotos() {{
        let count = 0;
        for (const id of ETERNA_PHOTO_IDS) {{
            if (photoUploaded[id] && photoUploaded[id].ok) count += 1;
        }}
        return count;
    }}

    async function uploadPreparedPhotoToServer(inputId, file) {{
        if (!file) throw new Error(currentLang && currentLang() === "en" ? "Empty photo" : "Foto vacía");
        const sessionId = getPhotoUploadSession();
        const data = new FormData();
        data.append("photo_upload_session", sessionId);
        data.append("slot", inputId);
        data.append("photo", file, file.name || (inputId + ".jpg"));

        setPhotoStatus(inputId, tr("photoLoading"));
        const response = await fetch("/preupload-photo", {{
            method: "POST",
            body: data,
            credentials: "same-origin",
        }});

        let payload = {{}};
        try {{ payload = await response.json(); }} catch (e) {{}}

        if (!response.ok || !payload.ok) {{
            throw new Error(payload.detail || (currentLang && currentLang() === "en" ? "Could not upload the photo" : "No se pudo subir la foto"));
        }}

        photoUploaded[inputId] = payload;
        delete photoUploadErrors[inputId];
        return payload;
    }}

    function preuploadedMinimumReady() {{
        return countPreuploadedPhotos() >= 4 && !photoProcessingActive();
    }}

    function isOptimizedEternaPhoto(file) {{
        return !!(file && String(file.name || "").startsWith(ETERNA_OPTIMIZED_PREFIX));
    }}

    function updatePhotoUI(inputId, file, message) {{
        const preview = document.getElementById("preview_" + inputId);
        const placeholder = document.getElementById("placeholder_" + inputId);
        const status = document.getElementById("status_" + inputId);

        if (!file) {{
            if (photoObjectUrls[inputId]) {{
                try {{ URL.revokeObjectURL(photoObjectUrls[inputId]); }} catch (e) {{}}
                delete photoObjectUrls[inputId];
            }}
            if (preview) {{
                preview.src = "";
                preview.style.display = "none";
            }}
            if (placeholder) {{
                placeholder.style.display = "block";
            }}
            if (status) {{
                status.innerText = message || tr("photoOptional");
                status.classList.remove("ready", "loading");
                status.classList.add("optional");
            }}
            const input = inputId ? document.getElementById(inputId) : null;
            const box = input ? input.closest(".photo-box") : null;
            if (box) box.classList.remove("ready", "loading");
            try {{ updatePhotoReadiness(); }} catch (e) {{}}
            return;
        }}

        if (photoObjectUrls[inputId]) {{
            try {{ URL.revokeObjectURL(photoObjectUrls[inputId]); }} catch (e) {{}}
        }}

        const url = URL.createObjectURL(file);
        photoObjectUrls[inputId] = url;

        if (preview) {{
            preview.src = url;
            preview.style.display = "block";
        }}

        if (placeholder) {{
            placeholder.style.display = "none";
        }}

        if (status) {{
            const kb = Math.max(1, Math.round((file.size || 0) / 1024));
            status.innerText = message || (photoUploaded[inputId] && photoUploaded[inputId].ok ? tr("photoUploaded") : (tr("photoReady") + " · " + kb + " KB"));
            status.classList.remove("loading", "optional");
            status.classList.add("ready");
        }}

        const box = inputId ? document.getElementById(inputId)?.closest(".photo-box") : null;
        if (box) {{
            box.classList.remove("loading");
            box.classList.add("ready");
        }}

        try {{ updatePhotoReadiness(); }} catch (e) {{}}
    }}

    function setPhotoStatus(inputId, message) {{
        const status = document.getElementById("status_" + inputId);
        const input = document.getElementById(inputId);
        const box = input ? input.closest(".photo-box") : null;
        if (status) {{
            status.innerText = message;
            status.classList.remove("ready", "optional");
            status.classList.add("loading");
        }}
        if (box) {{
            box.classList.remove("ready");
            box.classList.add("loading");
        }}
        try {{ updatePhotoReadiness(); }} catch (e) {{}}
    }}

    function openPhotoDraftDB() {{
        return new Promise((resolve, reject) => {{
            if (!("indexedDB" in window)) {{
                reject(new Error("IndexedDB no disponible"));
                return;
            }}

            const request = indexedDB.open(ETERNA_PHOTO_DB, 1);
            request.onupgradeneeded = function () {{
                const db = request.result;
                if (!db.objectStoreNames.contains(ETERNA_PHOTO_STORE)) {{
                    db.createObjectStore(ETERNA_PHOTO_STORE);
                }}
            }};
            request.onsuccess = function () {{ resolve(request.result); }};
            request.onerror = function () {{ reject(request.error || new Error("No se pudo abrir IndexedDB")); }};
        }});
    }}

    async function savePhotoDraft(inputId, file) {{
        try {{
            if (!file || !("indexedDB" in window)) return;
            const db = await openPhotoDraftDB();
            await new Promise((resolve, reject) => {{
                const tx = db.transaction(ETERNA_PHOTO_STORE, "readwrite");
                tx.objectStore(ETERNA_PHOTO_STORE).put(file, inputId);
                tx.oncomplete = resolve;
                tx.onerror = function () {{ reject(tx.error || new Error("No se pudo guardar foto draft")); }};
            }});
            db.close();
        }} catch (e) {{
            console.warn("RC91 photo draft save skipped", inputId, e);
        }}
    }}

    async function loadPhotoDraft(inputId) {{
        try {{
            if (!("indexedDB" in window)) return null;
            const db = await openPhotoDraftDB();
            const file = await new Promise((resolve, reject) => {{
                const tx = db.transaction(ETERNA_PHOTO_STORE, "readonly");
                const req = tx.objectStore(ETERNA_PHOTO_STORE).get(inputId);
                req.onsuccess = function () {{ resolve(req.result || null); }};
                req.onerror = function () {{ reject(req.error || new Error("No se pudo leer foto draft")); }};
            }});
            db.close();
            return file;
        }} catch (e) {{
            console.warn("RC91 photo draft load skipped", inputId, e);
            return null;
        }}
    }}

    async function clearPhotoDrafts() {{
        try {{
            if (!("indexedDB" in window)) return;
            const db = await openPhotoDraftDB();
            await new Promise((resolve, reject) => {{
                const tx = db.transaction(ETERNA_PHOTO_STORE, "readwrite");
                tx.objectStore(ETERNA_PHOTO_STORE).clear();
                tx.oncomplete = resolve;
                tx.onerror = function () {{ reject(tx.error || new Error("No se pudo limpiar draft fotos")); }};
            }});
            db.close();
        }} catch (e) {{
            console.warn("RC91 photo draft clear skipped", e);
        }}
    }}

    function loadImageFromFile(file) {{
        return new Promise((resolve, reject) => {{
            const img = new Image();
            const url = URL.createObjectURL(file);
            img.onload = function () {{
                URL.revokeObjectURL(url);
                resolve(img);
            }};
            img.onerror = function () {{
                URL.revokeObjectURL(url);
                reject(new Error("No se pudo leer la foto"));
            }};
            img.src = url;
        }});
    }}

    function canvasToBlobSafe(canvas, type, quality) {{
        return new Promise((resolve) => {{
            try {{
                canvas.toBlob((blob) => resolve(blob), type, quality);
            }} catch (e) {{
                resolve(null);
            }}
        }});
    }}

    async function optimizeImageFile(file, inputId) {{
        if (!file) throw new Error(currentLang && currentLang() === "en" ? "Empty photo" : "Foto vacía");

        const type = String(file.type || "").toLowerCase();
        const name = String(file.name || "foto.jpg").toLowerCase();

        if (!(type.startsWith("image/") || /\\.(jpg|jpeg|png|webp|heic|heif)$/i.test(name))) {{
            throw new Error("No parece una imagen válida");
        }}

        let img;
        try {{
            img = await loadImageFromFile(file);
        }} catch (e) {{
            console.warn("RC91: no se pudo optimizar, se usará original", inputId, e);
            return file;
        }}

        const originalW = img.naturalWidth || img.width || 0;
        const originalH = img.naturalHeight || img.height || 0;

        if (!originalW || !originalH) {{
            return file;
        }}

        let targetW = originalW;
        let targetH = originalH;
        const maxSide = Math.max(originalW, originalH);

        if (maxSide > ETERNA_PHOTO_MAX_SIDE) {{
            const ratio = ETERNA_PHOTO_MAX_SIDE / maxSide;
            targetW = Math.max(1, Math.round(originalW * ratio));
            targetH = Math.max(1, Math.round(originalH * ratio));
        }}

        const canvas = document.createElement("canvas");
        canvas.width = targetW;
        canvas.height = targetH;

        const ctx = canvas.getContext("2d", {{ alpha: false }});
        if (!ctx) return file;

        ctx.fillStyle = "#000";
        ctx.fillRect(0, 0, targetW, targetH);
        ctx.drawImage(img, 0, 0, targetW, targetH);

        const blob = await canvasToBlobSafe(canvas, "image/jpeg", ETERNA_PHOTO_QUALITY);
        canvas.width = 1;
        canvas.height = 1;

        if (!blob) return file;

        const slotNumber = String(inputId || "photo").replace(/[^0-9]/g, "") || "x";
        const optimized = new File(
            [blob],
            ETERNA_OPTIMIZED_PREFIX + "photo" + slotNumber + ".jpg",
            {{
                type: "image/jpeg",
                lastModified: Date.now()
            }}
        );

        console.log("RC91 foto optimizada", inputId, {{
            before_kb: Math.round((file.size || 0) / 1024),
            after_kb: Math.round((optimized.size || 0) / 1024),
            from: originalW + "x" + originalH,
            to: targetW + "x" + targetH
        }});

        return optimized;
    }}

    function setInputFile(input, file, dispatchChange=true) {{
        if (!input || !file) return false;
        const inputId = input.id || input.name || "photo";
        photoNativeFiles[inputId] = file;
        try {{
            if (typeof DataTransfer === "undefined") {{
                throw new Error("DataTransfer no disponible");
            }}
            const dt = new DataTransfer();
            dt.items.add(file);
            input.files = dt.files;
            photoNativeAssigned[inputId] = !!(input.files && input.files.length > 0);
            if (dispatchChange) {{
                input.dispatchEvent(new Event("change", {{ bubbles: true }}));
            }}
            return photoNativeAssigned[inputId];
        }} catch (e) {{
            // RC112C: esto puede pasar en Safari/Instagram WebView.
            // No borramos la foto ni bloqueamos la venta: la dejamos en memoria
            // para enviarla con FormData manual si el submit nativo no la incluye.
            console.warn("RC112F DataTransfer fallback activo", inputId, e);
            photoNativeAssigned[inputId] = false;
            return false;
        }}
    }}

    async function preparePhotoForSlot(inputId, rawFile, slotIndex) {{
        const input = document.getElementById(inputId);
        if (!input || !rawFile) return false;

        try {{
            // RC112 FAST FORM:
            // La foto queda lista para avanzar en cuanto está colocada en el input.
            // El preupload queda como acelerador en segundo plano, nunca como bloqueo de venta.
            photoProcessing[inputId] = true;
            setPhotoStatus(inputId, tr("optimizingPhoto"));

            // RC112F FAST GALLERY SAFE:
            // No bloqueamos la selección múltiple con canvas/HEIC/optimización en Safari o Instagram.
            // La foto queda lista inmediatamente y se envía como archivo original.
            const optimized = rawFile;

            const ok = setInputFile(input, optimized, false);
            // RC112C:
            // Si ok=false, no significa que la foto sea mala; significa que el navegador
            // no nos deja recolocar input.files. La foto queda en photoNativeFiles
            // y se enviará por fallback FormData en submit.
            if (!ok && !(input.files && input.files.length > 0)) {{
                console.warn("RC112F foto mantenida en memoria para submit seguro", inputId);
            }}

            delete photoUploadErrors[inputId];
            updatePhotoUI(inputId, optimized, tr("photoReady"));
            await savePhotoDraft(inputId, optimized);
            saveFormState();
            clearError();

            // Preupload no bloqueante: si sale bien, el backend usará esa copia.
            // Si falla, /crear recibirá las fotos por multipart normal.
            uploadPreparedPhotoToServer(inputId, optimized)
                .then(function () {{
                    updatePhotoUI(inputId, optimized, tr("photoUploaded"));
                    updatePhotoReadiness();
                    console.log("RC112 PHOTO_PREUPLOAD_OK", inputId);
                }})
                .catch(function (uploadErr) {{
                    console.warn("RC112 PHOTO_PREUPLOAD_FAIL_FALLBACK_MULTIPART", inputId, uploadErr);
                    delete photoUploaded[inputId];
                    photoUploadErrors[inputId] = String(uploadErr && uploadErr.message ? uploadErr.message : uploadErr);
                    updatePhotoUI(inputId, optimized, tr("photoReady"));
                    updatePhotoReadiness();
                }});

            updatePhotoReadiness();
            return true;
        }} catch (e) {{
            console.error("RC112F prepare photo error", inputId, e);
            delete photoUploaded[inputId];
            photoUploadErrors[inputId] = String(e && e.message ? e.message : e);
            // RC112C: si el input original conserva una foto, NO la borramos.
            // Así el submit nativo sigue pudiendo mandarla.
            const existing = input && input.files && input.files[0] ? input.files[0] : rawFile;
            if (existing) {{
                photoNativeFiles[inputId] = existing;
                updatePhotoUI(inputId, existing, tr("photoReady"));
                clearError();
                return true;
            }}
            updatePhotoUI(inputId, null, tr("photoPrepareError"));
            showError(tr("photoTryAnother"));
            return false;
        }} finally {{
            photoProcessing[inputId] = false;
            updatePhotoReadiness();
        }}
    }}

    async function restorePhotoDrafts() {{
        try {{
            let restored = 0;
            for (const inputId of ETERNA_PHOTO_IDS) {{
                const input = document.getElementById(inputId);
                if (!input || (input.files && input.files.length)) continue;

                const file = await loadPhotoDraft(inputId);
                if (file) {{
                    const ok = setInputFile(input, file, false);
                    if (ok) {{
                        updatePhotoUI(inputId, file, tr("photoRecovered"));
                        restored += 1;
                        uploadPreparedPhotoToServer(inputId, file)
                            .then(function () {{
                                updatePhotoUI(inputId, file, tr("photoUploaded"));
                                updatePhotoReadiness();
                            }})
                            .catch(function (uploadErr) {{
                                console.warn("RC112 no pudo pre-subir foto recuperada; seguirá por multipart", inputId, uploadErr);
                                delete photoUploaded[inputId];
                                updatePhotoUI(inputId, file, tr("photoReady"));
                                updatePhotoReadiness();
                            }});
                    }}
                }}
            }}

            if (restored > 0) {{
                console.log("RC91 fotos recuperadas", restored);
                saveFormState();
            }}
        }} catch (e) {{
            console.warn("RC91 restorePhotoDrafts skipped", e);
        }}
    }}

    function findNextEmptyPhotoSlot(startIndex) {{
        for (let i = startIndex || 0; i < ETERNA_PHOTO_IDS.length; i++) {{
            const id = ETERNA_PHOTO_IDS[i];
            const input = document.getElementById(id);
            const nativeHasFile = !!(input && input.files && input.files.length > 0);
            // RC112D: en Safari/Instagram puede fallar DataTransfer y quedarse la foto en memoria.
            // Si no miramos photoNativeFiles, el selector múltiple volvería a pisar photo1/photo2.
            if (!nativeHasFile && !photoNativeFiles[id]) {{
                return i;
            }}
        }}
        return -1;
    }}

    function currentPhotoCount() {{
        let count = 0;
        for (const id of ETERNA_PHOTO_IDS) {{
            const input = document.getElementById(id);
            if ((input && input.files && input.files.length > 0) || photoNativeFiles[id]) count += 1;
        }}
        return count;
    }}

    function photoIsReady(id) {{
        const input = document.getElementById(id);
        return !!((input && input.files && input.files.length > 0) || photoNativeFiles[id]);
    }}

    function firstRequiredPhotoCount() {{
        let count = 0;
        for (const id of ["photo1", "photo2", "photo3", "photo4"]) {{
            if (photoIsReady(id)) count += 1;
        }}
        return count;
    }}

    function firstRequiredPhotosPresent() {{
        return firstRequiredPhotoCount() >= 4;
    }}

    function photoProcessingActive() {{
        return ETERNA_PHOTO_IDS.some((id) => !!photoProcessing[id]);
    }}

    function updatePhotoReadiness() {{
        if (!button) return;

        const count = currentPhotoCount();
        const requiredCount = firstRequiredPhotoCount();
        const processing = photoProcessingActive();
        const minimumReady = firstRequiredPhotosPresent();

        for (const id of ETERNA_PHOTO_IDS) {{
            const input = document.getElementById(id);
            const status = document.getElementById("status_" + id);
            const box = input ? input.closest(".photo-box") : null;
            if (!status) continue;

            if (photoProcessing[id]) {{
                status.innerText = tr("photoLoading");
                status.classList.remove("ready", "optional");
                status.classList.add("loading");
                if (box) {{
                    box.classList.remove("ready");
                    box.classList.add("loading");
                }}
            }} else if (photoIsReady(id)) {{
                status.classList.remove("loading", "optional");
                status.classList.add("ready");
                if (box) {{
                    box.classList.remove("loading");
                    box.classList.add("ready");
                }}
                if (!status.innerText || status.innerText === "Pendiente" || status.innerText.includes("Aún no")) {{
                    status.innerText = tr("photoReady");
                }}
            }} else {{
                status.classList.remove("ready", "loading");
                status.classList.add("optional");
                if (box) box.classList.remove("ready", "loading");
                if (id === "photo5" || id === "photo6") {{
                    status.innerText = minimumReady ? tr("photoOptionalRepeat") : tr("photoOptional");
                }} else {{
                    status.innerText = tr("photoRequired");
                }}
            }}
        }}

        if (processing) {{
            button.disabled = true;
            button.classList.remove("ready");
            button.innerText = tr("photosPreparingButton");
            updateGlobalPhotoHint(tr("photoPreparingHint"));
            return;
        }}

        if (!minimumReady) {{
            button.disabled = true;
            button.classList.remove("ready");
            button.innerText = tr("uploadAtLeast4Button");
            updateGlobalPhotoHint(tr("photoMinimumHint"));
            return;
        }}

        button.disabled = false;
        button.classList.add("ready");
        button.innerText = count >= 6 ? tr("continuePaymentButton") : tr("continuePaymentCompleteButton");
        if (count >= 6) {{
            updateGlobalPhotoHint(tr("photoSixReadyHint"));
        }} else {{
            updateGlobalPhotoHint(tr("photoPartialReadyHint").replace("{{count}}", String(count)).replace("{{required}}", String(requiredCount)));
        }}
    }}

    function updateGlobalPhotoHint(message) {{
        const helper = document.querySelector(".multi-photo-helper");
        if (helper && message) {{
            helper.innerText = message;
        }}
    }}

    const multiPhotoPicker = document.getElementById("multi_photo_picker");
    const multiPhotoButton = document.querySelector(".photo-picker-btn");
    // RC112H GALLERY NATIVE SAFE:
    // NO interceptamos el click del label ni llamamos a input.click() con preventDefault.
    // En iPhone/Safari/Instagram, el gesto nativo sobre <label><input type=file></label>
    // es más fiable que el click programático.
    if (multiPhotoPicker) {{
        multiPhotoPicker.addEventListener("change", async function () {{
            clearError();

            const rawFiles = Array.from(multiPhotoPicker.files || []);
            if (!rawFiles.length) return;

            const validFiles = rawFiles.filter((file) => {{
                const type = String(file.type || "").toLowerCase();
                const name = String(file.name || "").toLowerCase();
                return type.startsWith("image/") || /\\.(jpg|jpeg|png|webp|heic|heif)$/i.test(name);
            }});

            if (!validFiles.length) {{
                multiPhotoPicker.value = "";
                showError(currentLang() === "en" ? "We couldn't find valid images. Choose photos from your gallery." : "No hemos encontrado imágenes válidas. Elige fotos desde tu galería.");
                return;
            }}

            const availableSlots = ETERNA_PHOTO_IDS.length - currentPhotoCount();

            if (availableSlots <= 0) {{
                multiPhotoPicker.value = "";
                showError(currentLang() === "en" ? "You already have 6 photos. To change one, tap the photo you want to replace." : "Ya tienes 6 fotos. Si quieres cambiar una, toca directamente la foto que quieras sustituir.");
                return;
            }}

            const filesToUse = validFiles.slice(0, availableSlots);
            const ignored = validFiles.length - filesToUse.length;

            let slotSearchStart = 0;
            let loaded = 0;

            for (const file of filesToUse) {{
                const slotIndex = findNextEmptyPhotoSlot(slotSearchStart);
                if (slotIndex < 0) break;

                const inputId = ETERNA_PHOTO_IDS[slotIndex];
                const ok = await preparePhotoForSlot(inputId, file, slotIndex);
                if (!ok) {{
                    multiPhotoPicker.value = "";
                    return;
                }}

                loaded += 1;
                slotSearchStart = slotIndex + 1;
            }}

            multiPhotoPicker.value = "";
            saveFormState();
            updatePhotoReadiness();

            const total = currentPhotoCount();
            const missing = Math.max(0, 4 - total);

            if (ignored > 0) {{
                updateGlobalPhotoHint(currentLang() === "en" ? "We placed the available photos. To change one, tap its box." : "Hemos colocado las fotos posibles. Para cambiar una, toca su casilla.");
            }} else if (missing > 0) {{
                updateGlobalPhotoHint(currentLang() === "en" ? ("Photos loaded. You still need " + missing + " to continue. If you have 4, ETERNA will complete the 6.") : ("Fotos cargadas. Te faltan " + missing + " para poder continuar. Si tienes 4, ETERNA completará las 6."));
            }} else {{
                updateGlobalPhotoHint(total >= 6 ? (currentLang() === "en" ? "6 photos ready. You can change any of them by tapping its box." : "6 fotos listas. Puedes cambiar cualquiera tocando su casilla.") : (currentLang() === "en" ? (total + " photos ready. ETERNA will complete the 6.") : (total + " fotos listas. ETERNA completará las 6.")));
            }}

            clearError();
        }});
    }}

    function bindPreview(inputId) {{
        const fileInput = document.getElementById(inputId);
        if (!fileInput) return;

        fileInput.addEventListener("change", async function () {{
            if (photoProcessing[inputId]) return;
            clearError();

            const file = fileInput.files && fileInput.files[0];
            if (!file) {{
                updatePhotoUI(inputId, null);
                updatePhotoReadiness();
                return;
            }}

            const type = String(file.type || "").toLowerCase();
            const name = String(file.name || "").toLowerCase();
            if (!(type.startsWith("image/") || /\\.(jpg|jpeg|png|webp|heic|heif)$/i.test(name))) {{
                fileInput.value = "";
                updatePhotoUI(inputId, null);
                showError(currentLang() === "en" ? "One of the selected files does not look like a valid image." : "Una de las fotos no parece una imagen válida.");
                return;
            }}

            await preparePhotoForSlot(inputId, file, 0);
            updatePhotoReadiness();
        }});
    }}

    ETERNA_PHOTO_IDS.forEach(bindPreview);

    function allPhotosPresent() {{
        // RC112D: el backend exige específicamente photo1-photo4.
        // No vale tener 4 fotos repartidas si falta una de las cuatro primeras.
        return firstRequiredPhotosPresent();
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

    // RC104 PHOTO FIX — se elimina el handler legacy duplicado.
    // Motivo: el handler antiguo rechazaba algunas fotos móviles/HEIC y pisaba la lógica robusta.
    // Se mantiene únicamente el preparador robusto ya definido arriba.

    function validateBeforeSubmit() {{
        if (!form) {{
            showError(tr("reviewFields"));
            return false;
        }}

        const responsibleUse = document.getElementById("responsible_use_accepted");
        if (responsibleUse && !responsibleUse.checked) {{
            showError(tr("acceptResponsible"));
            try {{ responsibleUse.focus(); }} catch (e) {{}}
            return false;
        }}

        // RC112H: no usamos form.checkValidity() global porque en Safari/Instagram
        // DataTransfer puede fallar y los input[type=file] requeridos quedar vacíos
        // aunque tengamos la foto segura en photoNativeFiles. Validamos los campos
        // normales y las fotos por nuestra lógica firstRequiredPhotosPresent().
        const requiredFields = Array.from(form.querySelectorAll("[required]")).filter(function(el) {{
            return !(el && el.type === "file");
        }});
        for (const el of requiredFields) {{
            if (el && typeof el.checkValidity === "function" && !el.checkValidity()) {{
                showError(tr("reviewFields"));
                try {{ el.focus(); }} catch(e) {{}}
                return false;
            }}
        }}

        const messageType = messageTypeInput ? messageTypeInput.value.trim() : "";
        if (!messageType) {{
            showError(tr("selectEmotion"));
            scrollToEmotionChoice();
            return false;
        }}

        if (photoProcessingActive()) {{
            showError(tr("photosPreparing"));
            updatePhotoReadiness();
            return false;
        }}

        if (!allPhotosPresent()) {{
            showError(tr("need4Photos"));
            updatePhotoReadiness();
            return false;
        }}

        // RC112 FAST FORM:
        // No bloqueamos el pago por preupload. Si hay 4 fotos locales, /crear las recibe por multipart.
        // El preupload sigue funcionando como acelerador, pero nunca frena una venta.

        if (manualRadio && manualRadio.checked) {{
            const phrase1 = form.querySelector('[name="phrase_1"]')?.value.trim();
            const phrase2 = form.querySelector('[name="phrase_2"]')?.value.trim();
            const phrase3 = form.querySelector('[name="phrase_3"]')?.value.trim();

            if (!phrase1 || !phrase2 || !phrase3) {{
                showError(tr("write3"));
                return false;
            }}
        }}

        if (deliveryModeScheduled && deliveryModeScheduled.checked) {{
            const deliveryDate = document.getElementById("delivery_date")?.value || "";
            const deliveryTime = document.getElementById("delivery_time")?.value || "";

            if (!deliveryDate || !deliveryTime) {{
                showError(tr("deliveryDate"));
                return false;
            }}

            const deliveryLocal = new Date(deliveryDate + "T" + deliveryTime);
            const now = new Date();

            if (!(deliveryLocal instanceof Date) || isNaN(deliveryLocal.getTime())) {{
                showError(tr("badDate"));
                return false;
            }}

            if (deliveryLocal.getTime() <= now.getTime()) {{
                showError(tr("futureDate"));
                return false;
            }}
        }}

        const giftAmount = parseFloat(document.getElementById("gift_amount")?.value || "0");
        if (Number.isNaN(giftAmount) || giftAmount < 0) {{
            showError(tr("badAmount"));
            return false;
        }}

        clearError();
        return true;
    }}

    if (!form) return;

    // RC105 FORM DRAFT TTL SAFE — lanzamiento Instagram
    // Mantiene el borrador reciente, pero limpia datos antiguos.
    // Si alguien sale a Stripe y vuelve/cancela, recupera.
    // Si vuelve mucho después, entra limpio. Pago correcto limpia todo desde /checkout-exito.
    // No toca Stripe, SMS, WhatsApp, R2, reacción ni Sender Pack.
    const FORM_DRAFT_TTL_MS = 30 * 60 * 1000;

    try {{
        const rawDraft = localStorage.getItem(STORAGE_KEY);
        let draftIsFresh = false;

        if (rawDraft) {{
            try {{
                const parsedDraft = JSON.parse(rawDraft);
                const savedAt = Number(parsedDraft && parsedDraft.__saved_at ? parsedDraft.__saved_at : 0);
                draftIsFresh = savedAt > 0 && (Date.now() - savedAt) <= FORM_DRAFT_TTL_MS;
            }} catch (e) {{
                draftIsFresh = false;
            }}
        }}

        if (draftIsFresh) {{
            restoreFormState();
            restorePhotoDrafts();
        }} else {{
            localStorage.removeItem(STORAGE_KEY);
            try {{
                if (form) form.reset();
            }} catch (e) {{
                console.error("RC105 form reset error", e);
            }}
        }}
    }} catch (e) {{
        console.error("RC105 draft ttl check error", e);
    }}

    applyDefaultEmotionIfNeeded();
    bindAutosave();
    updatePhraseMode();
    updateDeliveryMode();
    updatePhotoReadiness();

    let eternaSubmitting = false;

    function showPaymentLoadingNow() {{
        if (button) {{
            button.disabled = true;
            button.classList.add("is-loading");
            button.innerText = tr("openingCheckout");
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

    function needsManualPhotoSubmit() {{
        for (const id of ETERNA_PHOTO_IDS) {{
            const input = document.getElementById(id);
            const nativeHasFile = !!(input && input.files && input.files.length > 0);
            if (!nativeHasFile && photoNativeFiles[id]) return true;
        }}
        return false;
    }}

    async function submitWithPhotoMemoryFallback() {{
        const fd = new FormData(form);
        for (const id of ETERNA_PHOTO_IDS) {{
            const input = document.getElementById(id);
            const nativeHasFile = !!(input && input.files && input.files.length > 0);
            if (!nativeHasFile && photoNativeFiles[id]) {{
                fd.set(id, photoNativeFiles[id], photoNativeFiles[id].name || (id + ".jpg"));
            }}
        }}
        const response = await fetch(form.action || "/crear", {{
            method: "POST",
            body: fd,
            credentials: "same-origin",
            redirect: "follow"
        }});
        if (response.redirected && response.url) {{
            window.location.href = response.url;
            return;
        }}
        const contentType = response.headers.get("content-type") || "";
        if (contentType.indexOf("text/html") !== -1) {{
            const html = await response.text();
            document.open();
            document.write(html);
            document.close();
            return;
        }}
        if (!response.ok) throw new Error("HTTP " + response.status);
        window.location.href = "/crear";
    }}

    form.addEventListener("submit", function (e) {{
        if (eternaSubmitting) {{
            e.preventDefault();
            return;
        }}

        if (recipientPhoneInput && recipientPhoneInput.value) {{
            applyRecipientPhoneValue(recipientPhoneInput.value);
        }}

        if (!validateBeforeSubmit()) {{
            e.preventDefault();
            return;
        }}

        // RC101B/RC112C:
        // Preferimos submit nativo multipart/form-data.
        // Solo usamos fallback manual cuando Safari/Instagram no ha permitido
        // meter alguna foto en input.files pero sí la tenemos guardada en memoria.
        eternaSubmitting = true;
        clearError();
        showPaymentLoadingNow();

        // RC116 FORM RECOVERY SAFE:
        // NO borramos el borrador al salir hacia Stripe.
        // Si el usuario pulsa atrás/cancela porque Stripe preselecciona una tarjeta,
        // recupera textos y fotos draft/preupload.
        // El borrado definitivo ocurre solo en /checkout-exito/{order_id}, cuando el pago ya es correcto.
        try {{
            saveFormState();
        }} catch (err) {{
            console.error("RC116 save before Stripe error", err);
        }}

        // RC112B FAST PHOTO FALLBACK FIX:
        // NO desactivamos los inputs de fotos antes del submit.
        // Motivo: si el preupload falla o va lento, el backend necesita recibir las fotos
        // por multipart/form-data normal. Desactivar inputs aquí rompería exactamente
        // el fallback rápido que queremos para lanzamiento.
        console.log("RC112D FORM_SUBMIT_NATIVE_MULTIPART_WITH_PHOTO_FALLBACK", {{
            local_photos: currentPhotoCount(),
            preuploaded_photos: countPreuploadedPhotos(),
            preupload_required: false,
            manual_memory_fallback: needsManualPhotoSubmit()
        }});

        if (needsManualPhotoSubmit()) {{
            e.preventDefault();
            if (button) button.innerText = tr("formNativeFallback");
            submitWithPhotoMemoryFallback().catch(function(err) {{
                console.error("RC112D manual photo submit fallback error", err);
                eternaSubmitting = false;
                if (button) {{
                    button.disabled = false;
                    button.classList.remove("is-loading");
                    button.innerText = tr("submit");
                }}
                showError(tr("genericError"));
            }});
            return false;
        }}

        return true;
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
def crear_get(request: Request):
    raw_lang = (request.query_params.get("lang") or request.query_params.get("language") or "").strip().lower()
    return render_create_form("en" if raw_lang == "en" else "es")


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
    language: str = Form("es"),
    customer_country_code: str = Form(...),
    customer_phone: str = Form(...),
    recipient_name: str = Form(...),
    recipient_country_code: str = Form(...),
    recipient_phone: str = Form(...),
    recipient_email: str = Form(""),
    occasion_type: str = Form(""),
    occasion_date: str = Form(""),
    marketing_opt_in: str = Form(""),
    message_type: str = Form(...),
    phrase_mode: str = Form(...),
    phrase_1: str = Form(""),
    phrase_2: str = Form(""),
    phrase_3: str = Form(""),
    delivery_mode: str = Form("instant"),
    delivery_date: str = Form(""),
    delivery_time: str = Form(""),
    gift_amount: float = Form(0),
    photo1: Optional[UploadFile] = File(None),
    photo2: Optional[UploadFile] = File(None),
    photo3: Optional[UploadFile] = File(None),
    photo4: Optional[UploadFile] = File(None),
    photo5: Optional[UploadFile] = File(None),
    photo6: Optional[UploadFile] = File(None),
    photo_upload_session: str = Form(""),
    show_sender_identity: str = Form(""),
    arrival_photo_slot: str = Form("photo1"),
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
            recipient_email,
            occasion_type,
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
            photo_upload_session,
            show_sender_identity,
            arrival_photo_slot,
            responsible_use_accepted or responsible_use,
            yul_memory_place,
            yul_memory_detail,
            yul_emotion_tone,
            yul_magic_hint,
            occasion_date,
            marketing_opt_in,
            language,
        )

    except HTTPException as e:
        print("🔥 ERROR CONTROLADO EN /crear:", e.detail)
        raise e

    except Exception as e:
        print("🔥 ERROR EN /crear:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error creando el pedido")


# =========================================================
# MEMORY ENGINE V1 — ADMIN SOLO LECTURA
# =========================================================

@app.get("/admin/memory")
def admin_memory(token: str = "", limit: int = 50):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")

    safe_limit = max(1, min(int(limit or 50), 200))
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            id,
            order_id,
            sender_name,
            sender_email,
            sender_phone,
            recipient_name,
            recipient_email,
            recipient_phone,
            occasion_type,
            occasion_date,
            delivery_mode,
            scheduled_delivery_at,
            marketing_opt_in,
            last_reminder_sent,
            memory_created_at,
            created_at
        FROM memory_events
        ORDER BY created_at DESC
        LIMIT ?
    """, (safe_limit,))
    rows = [dict(r) for r in cur.fetchall()]

    cur.execute("SELECT COUNT(*) AS total FROM memory_events")
    total = cur.fetchone()["total"]

    cur.execute("""
        SELECT occasion_type, COUNT(*) AS total
        FROM memory_events
        WHERE COALESCE(occasion_type, '') <> ''
        GROUP BY occasion_type
        ORDER BY total DESC
        LIMIT 20
    """)
    by_occasion = [dict(r) for r in cur.fetchall()]
    conn.close()

    return {
        "ok": True,
        "version": "MEMORY_ENGINE_V1_SILENT_SAFE",
        "enabled": bool(MEMORY_ENGINE_ENABLED),
        "reminders_enabled": bool(MEMORY_REMINDERS_ENABLED),
        "total_memory_events": total,
        "by_occasion": by_occasion,
        "items": rows,
    }


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
    checks["r2_status"] = r2_status_summary()
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

    warnings = []
    if not r2_enabled():
        warnings.append("R2 no está completo: ETERNA seguirá con respaldo local, pero conviene validar R2 antes de escalar ventas.")

    decision = "APTA_PARA_PRUEBA_CONTROLADA" if not blocking else "NO_LANZAR_AUN"
    return {
        "version": ETERNA_APP_VERSION,
        "decision": decision,
        "blocking": blocking,
        "warnings": warnings,
        "r2_status": r2_status_summary(),
        "health": health,
        "confidence": confidence,
        "principle": "Todo puede fallar. Ningún pedido puede perderse jamás.",
        "timestamp": now_iso(),
    }


@app.get("/admin/r2-check")
def admin_r2_check(token: str = "", write: int = 0):
    rc74_admin_guard(token)
    if write:
        return r2_write_probe()
    return {
        "ok": r2_enabled(),
        "status": r2_status_summary(),
        "hint": "Usa /admin/r2-check?token=ADMIN_TOKEN&write=1 para probar subida real y lectura pública.",
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
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
        "base": "RC75_MAGIA_YUL_FORMULARIO_DEPLOY_SAFE",
        "yul": "particula_estela_indigo",
        "umbral": "trovador_cinematografico",
        "formulario_emocional": True,
        "consent_delay_ms": 55000,
        "touches_core": False,
    }



@app.get("/admin/rc76-version")
def admin_rc76_version(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
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
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {"version":"RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE","yul_uses_form_values":True,"post_consent_story_bridge":True,"auto_opens_after_camera_ready":True,"touches_critical_core":False}



@app.get("/admin/rc78-version")
def admin_rc78_version(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
        "formulario_yul": "solo_lugar",
        "uses_real_place": True,
        "generic_romantic_responses": True,
        "does_not_invent_memory": True,
        "touches_critical_core": False,
    }



@app.get("/admin/rc78b-version")
def admin_rc78b_version(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
        "formulario_yul": "solo_lugar",
        "lugar_real_en_historia": True,
        "no_inventa_recuerdos": True,
        "compatible_db_columns": True,
        "touches_critical_core": False,
    }



@app.get("/admin/rc78c-version")
def admin_rc78c_version(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
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
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
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
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
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
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
        "rescue_hidden_normal_flow": True,
        "rescue_emergency_after_ms": 60000,
        "camera_guide_auto_continue_ms": 4000,
        "sms_core_kept": True,
        "sender_pack_master_v1": "sender_pack_master_v1.png",
        "touches_critical_core": False,
    }



@app.get("/admin/rc84-version")
def admin_rc84_version(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
        "guia_replaced_from_root": True,
        "one_text_at_a_time": True,
        "skip_button_removed": True,
        "camera_auto_continue_ms": 4000,
        "sender_pack_replaced_from_root": True,
        "sender_buttons": ["CREAR OTRA ETERNA", "COMPARTIR", "DESCARGAR"],
        "sms_core_kept": True,
        "touches_critical_core": False,
    }



@app.get("/admin/rc85-version")
def admin_rc85_version(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
        "fix": "guia_start_button_route",
        "canonical_js_route": "/start-experience",
        "compat_route": "/start-experience/{recipient_token}",
        "guia_replaced_from_root": True,
        "sender_pack_replaced_from_root": True,
        "sms_core_kept": True,
        "touches_critical_core": False,
    }



@app.get("/admin/rc86-version")
def admin_rc86_version(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
        "only_sender_pack_changed": True,
        "vertical_call_layout": True,
        "main_video_format": "9:16",
        "reaction_smaller": True,
        "reaction_position": "top-right-inside",
        "sender_pack_master_v1": "sender_pack_master_v1.png",
        "touches_critical_core": False,
    }



@app.get("/admin/rc89-version")
def admin_rc89_version(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
        "base": "RC86_good_uploaded",
        "only_phrase_timing_changed": True,
        "anti_overlap": True,
        "one_text_box_only": True,
        "button_logic_touched": False,
        "camera_4s_touched": False,
        "sender_pack_touched": False,
        "critical_core_touched": False,
    }






@app.get("/admin/rc93-version")
def admin_rc93_version(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
        "base": "RC92_PHOTO_PICKER_ONLY_SAFE",
        "only_sender_pack_reaction_visual_changed": True,
        "reaction_object_fit": "contain",
        "reaction_transform_scale_removed": True,
        "reaction_window_aspect_ratio": "16/9",
        "critical_core_touched": False,
        "stripe_touched": False,
        "sms_touched": False,
        "camera_capture_touched": False,
        "reaction_upload_touched": False,
        "video_engine_touched": False,
        "db_touched": False,
    }

@app.get("/admin/rc92-version")
def admin_rc92_version(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
        "base": "RC91_photo_optimize_only",
        "only_gallery_picker_changed": True,
        "photo_optimization_kept": True,
        "more_than_six_uses_available_slots": True,
        "less_than_six_keeps_loaded_photos": True,
        "individual_photo_change_kept": True,
        "critical_core_touched": False,
        "stripe_touched": False,
        "sms_touched": False,
        "sender_pack_touched": False,
        "experience_touched": False,
    }


@app.get("/admin/rc91-version")
def admin_rc91_version(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
        "base": "RC90_final_perfect",
        "only_create_photos_changed": True,
        "client_photo_optimization": True,
        "max_side_px": 1600,
        "jpeg_quality": 0.78,
        "indexeddb_photo_draft_restore": True,
        "critical_core_touched": False,
        "stripe_touched": False,
        "sms_touched": False,
        "sender_pack_touched": False,
        "experience_touched": False,
    }


@app.get("/admin/rc90-version")
def admin_rc90_version(token: str = ""):
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
        "base": "RC89_final_candidate",
        "only_sender_pack_visual_changed": True,
        "removed_lo_que_sintio": True,
        "removed_decorative_icons": True,
        "main_video_bigger": True,
        "reaction_bigger": True,
        "buttons_higher_and_tighter": True,
        "background_title_heavy_blur_overlay": True,
        "critical_core_touched": False,
    }


# =========================================================
# START EXPERIENCE (FIX CRÍTICO)
# =========================================================



# =========================================================
# RUTAS CRÍTICAS RECUPERADAS DEL SALVAVIDAS
# Stripe webhook + callback video engine + resumen
# =========================================================


# =========================================================
# RC115 — STRIPE PAID SESSION PROCESSOR + CHECKOUT RECOVERY SAFE
# Unifica pago real -> pedido paid -> VideoEngine.
# Mantiene el webhook como fuente principal, pero si Stripe vuelve a
# /checkout-exito y el webhook ha fallado por firma/secret, verifica la
# sesión con Stripe API y rescata el render sin tocar formulario, fotos ni SMS.
# =========================================================
def process_paid_checkout_session(session, stripe_event_id: str = "", source: str = "stripe") -> dict:
    metadata = session.get("metadata", {}) or {}
    order_id = (session.get("client_reference_id") or metadata.get("order_id") or "").strip()

    if not order_id:
        stripe_session_id_lookup = (session.get("id") or "").strip()
        if stripe_session_id_lookup:
            try:
                order = get_order_by_stripe_session_id(stripe_session_id_lookup)
                order_id = order["id"]
            except Exception:
                order_id = ""

    print(f"📦 RC115 order_id {source}:", order_id)

    if not order_id:
        raise HTTPException(status_code=400, detail="order_id missing")

    try:
        order = get_order_by_id(order_id)
    except Exception:
        raise HTTPException(status_code=404, detail="order_not_found")

    stripe_payment_status = (session.get("payment_status") or "").strip() or "paid"
    if stripe_payment_status != "paid":
        print(f"⚠️ RC115 sesión no pagada todavía: {order_id} status={stripe_payment_status}")
        return {"status": "ignored", "reason": "payment_not_paid", "order_id": order_id, "payment_status": stripe_payment_status}

    # Idempotencia: nunca relanzar motor si el mismo evento ya se procesó.
    if stripe_event_id and (order.get("stripe_event_id") or "") == stripe_event_id and order.get("stripe_event_processed_at"):
        try:
            email_result = send_order_received_emails(order_id)
            print("📧 RC115 emails pedido webhook duplicado:", email_result)
        except Exception as e:
            log_error("order_emails_duplicate_webhook", e)
        return {"status": "ok", "reason": "stripe_event_already_processed", "order_id": order_id}

    log_info("💳 PAGO RECIBIDO EN STRIPE")
    log_info("🆔 Order ID", order_id)
    log_info("👤 Regalante", f"{order.get('sender_name')} | {order.get('sender_email') or 'sin email'} | {order.get('sender_phone')}")
    log_info("🎯 Destinatario", f"{order.get('recipient_name')} | {order.get('recipient_phone')}")
    log_info("🎬 Estado", f"voy a preparar el vídeo · source={source}")

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

    # Email operativo: no bloquea render ni SMS.
    try:
        email_result = send_order_received_emails(order_id)
        print(f"📧 RC115 emails pedido {source}:", email_result)
    except Exception as e:
        log_error(f"order_emails_after_payment_{source}", e)

    if original_video_ready(order):
        set_order_state(order_id, "VIDEO_READY", f"{source}_video_already_ready")
        return {"status": "ok", "reason": "video_already_ready", "order_id": order_id}

    if render_request_already_marked(order):
        return {"status": "ok", "reason": "render_already_requested", "order_id": order_id}

    phrases = [
        (order.get("phrase_1") or "").strip(),
        (order.get("phrase_2") or "").strip(),
        (order.get("phrase_3") or "").strip(),
    ]

    try:
        mark_video_render_requested(order_id)
        set_order_state(order_id, "RENDERING", f"{source}_render_requested")
        data = trigger_video_engine(order_id, phrases)
        print("✅ RC115 Video engine aceptó el trabajo:", data)
    except Exception as e:
        clear_video_render_requested(order_id, error=str(e))
        log_error(f"{source}_video_engine_queued_for_recovery", e)
        try:
            alert_order = get_order_by_id(order_id)
            send_admin_error_email(
                f"🚨 ETERNA ERROR render {order_public_code(alert_order)}",
                build_critical_alert_body(alert_order, "Pago recibido pero el motor de vídeo no ha arrancado correctamente", str(e)),
                order_id=order_id,
                reason=f"video_engine_error_after_payment_{source}",
            )
        except Exception as email_error:
            log_error(f"email_alert_video_engine_error_{source}", email_error)
        return {"status": "ok", "reason": "video_engine_error_queued_for_recovery", "order_id": order_id, "error": str(e)}

    return {"status": "ok", "reason": "render_requested", "order_id": order_id}

@app.post("/stripe/webhook")
@app.post("/stripe/webhook/")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    print("🔔 RC115 STRIPE WEBHOOK RECIBIDO")
    print("🔔 RC115 signature header:", "present" if sig_header else "missing")
    print("🔔 RC115 webhook secret:", "present" if STRIPE_WEBHOOK_SECRET else "missing")

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Falta STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        print("❌ RC115 STRIPE WEBHOOK payload inválido:", str(e))
        raise HTTPException(status_code=400, detail="Payload inválido")
    except stripe.error.SignatureVerificationError as e:
        print("❌ RC115 STRIPE WEBHOOK firma inválida:", str(e))
        # Importante: no procesamos webhooks sin firma válida.
        # Si Stripe devuelve al usuario a /checkout-exito, RC115 intentará rescate
        # verificando la sesión directamente contra Stripe API.
        raise HTTPException(status_code=400, detail="Firma inválida")

    print("🔔 RC115 stripe event:", event.get("type"), event.get("id"))

    if event["type"] != "checkout.session.completed":
        return {"status": "ignored", "event_type": event.get("type")}

    session = event["data"]["object"]
    return process_paid_checkout_session(session, stripe_event_id=(event.get("id") or "").strip(), source="webhook")

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


@app.post("/start-experience/{recipient_token}")
async def start_experience_direct_compat(recipient_token: str, request: Request):
    """
    RC85: compatibilidad con guías que llaman /start-experience/{token}.
    Misma lógica de start_experience, sin tocar SMS/Stripe/video engine.
    """
    try:
        order = get_order_by_recipient_token_or_404(recipient_token)
        insert_order_event(order["id"], "experience_started", "ok", "El destinatario ha pulsado empezar y se inicia cámara/vídeo")

        log_human("EXPERIENCIA INICIADA", f"🎭 {order.get('recipient_name')} ha pulsado Empezar", f"🆔 Pedido: {order.get('id')}")
        print("🎬 START EXPERIENCE DIRECT COMPAT:", order["id"])
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
        ajax_header = (request.headers.get("x-eterna-ajax") or "").strip()
        if ajax_header != "1":
            return RedirectResponse(url=redirect_url, status_code=303)

        return JSONResponse({
            "ok": True,
            "redirect_url": redirect_url
        })

    except HTTPException:
        raise
    except Exception as e:
        log_error("START EXPERIENCE DIRECT COMPAT ERROR", e)
        raise HTTPException(status_code=500, detail="start_experience_direct_failed")


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
    RC84 — GUÍA REAL LIMPIA.
    Una sola línea de texto activa cada vez.
    Sin botón de salto.
    Consentimiento claro.
    Cámara/rostro 4 segundos.
    Luego entrada a /experiencia.
    """
    recipient_token_safe = safe_attr(recipient_token)
    recipient_token_json = json.dumps(str(recipient_token))

    try:
        order = get_order_by_recipient_token_or_404(recipient_token)
        yul_context = rc75_yul_context_from_order(order)
    except Exception:
        yul_context = {"memory_place": "", "memory_detail": "", "emotion_tone": "", "magic_hint": ""}

    place = safe_text(yul_context.get("memory_place") or "")
    place_line = "Hay un lugar escondido dentro de esta historia." if not place else f"Hay un lugar escondido dentro de esta historia:<br><span>{place}</span>."

    html_doc = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>ETERNA - El Umbral</title>
<meta name="theme-color" content="#02050a">
<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;width:100%;min-height:100%;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
body{min-height:100svh;min-height:100dvh;overflow:hidden;background:#02050a}
.stage{position:relative;width:100vw;height:100svh;height:100dvh;max-width:520px;margin:0 auto;overflow:hidden;background:radial-gradient(circle at 50% 75%,rgba(0,75,130,.52),transparent 34%),radial-gradient(circle at 22% 20%,rgba(52,190,255,.13),transparent 26%),linear-gradient(180deg,#000 0%,#020713 52%,#030d18 100%)}
.stage:before{content:"";position:absolute;inset:0;background-image:radial-gradient(circle,rgba(255,255,255,.45) 0 1px,transparent 1.4px),radial-gradient(circle,rgba(73,212,255,.60) 0 1px,transparent 1.4px),radial-gradient(circle,rgba(255,214,126,.46) 0 1px,transparent 1.4px);background-size:95px 130px,137px 190px,190px 250px;opacity:.45;animation:stars 46s linear infinite}
@keyframes stars{from{transform:translateY(0)}to{transform:translateY(-120px)}}
.brand{position:absolute;z-index:5;top:calc(env(safe-area-inset-top) + 22px);left:0;right:0;text-align:center;font-family:Georgia,"Times New Roman",serif;letter-spacing:.46em;font-size:clamp(18px,5.5vw,28px);color:#eec36a;text-shadow:0 0 22px rgba(255,200,93,.54)}
.brand:after{content:"♡";display:block;letter-spacing:0;margin-top:7px;font-size:18px;color:#ffd477}
.yul{position:absolute;z-index:8;left:50%;top:50%;width:20px;height:20px;border-radius:999px;background:radial-gradient(circle,#fff 0 16%,#9ee9ff 18% 32%,#2668ff 36% 56%,rgba(89,0,255,.34) 67%,transparent 78%);box-shadow:0 0 20px rgba(255,255,255,.95),0 0 48px rgba(87,218,255,.90),0 0 92px rgba(46,96,255,.58);transform:translate(-50%,-50%);animation:yulMove 24s ease-in-out infinite;pointer-events:none}
.yul:before{content:"";position:absolute;right:13px;top:9px;width:120px;height:4px;border-radius:999px;background:linear-gradient(90deg,transparent,rgba(64,204,255,.55),rgba(255,255,255,.86));filter:blur(.3px);opacity:.72}
.yul:after{content:"";position:absolute;inset:-28px;border-radius:999px;background:radial-gradient(circle,rgba(87,214,255,.30),rgba(58,97,255,.12) 42%,transparent 70%);filter:blur(8px);animation:pulse 2s ease-in-out infinite}
@keyframes yulMove{0%,100%{left:50%;top:50%}20%{left:42%;top:42%}45%{left:58%;top:47%}70%{left:48%;top:56%}}
@keyframes pulse{0%,100%{opacity:.55;transform:scale(.9)}50%{opacity:1;transform:scale(1.1)}}
.copy{position:absolute;z-index:10;left:7%;right:7%;top:50%;transform:translateY(-50%);text-align:center;min-height:160px;display:flex;align-items:center;justify-content:center}
#yulText{font-size:clamp(24px,7vw,40px);line-height:1.17;font-family:Georgia,"Times New Roman",serif;color:#fff6e8;text-shadow:0 0 22px rgba(255,255,255,.22),0 0 48px rgba(57,194,255,.22);opacity:0;transition:opacity .9s ease,transform .9s ease;transform:translateY(10px)}
#yulText.show{opacity:1;transform:translateY(0)}
#yulText.small{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;font-size:clamp(18px,5vw,25px);line-height:1.42}
#yulText span,.gold{color:#f4c46c;text-shadow:0 0 24px rgba(255,199,92,.56)}
.card{position:absolute;z-index:20;left:6%;right:6%;top:50%;transform:translateY(-50%) scale(.96);opacity:0;pointer-events:none;padding:26px 20px 22px;border:1px solid rgba(255,215,136,.44);border-radius:28px;background:linear-gradient(180deg,rgba(2,9,20,.90),rgba(1,4,11,.82));box-shadow:0 0 46px rgba(36,171,255,.20),0 0 78px rgba(255,191,83,.13),inset 0 0 28px rgba(255,255,255,.045);backdrop-filter:blur(12px);transition:opacity .9s ease,transform .9s ease}
.card.show{opacity:1;transform:translateY(-50%) scale(1);pointer-events:auto}
.card h1{font-family:Georgia,"Times New Roman",serif;margin:0 0 14px;text-align:center;font-size:clamp(29px,8vw,43px);font-weight:400;color:#fff5e5;line-height:1.05}
.card h1 span{color:#f4c46c}
.card p{margin:11px 0;font-size:clamp(15px,4.1vw,19px);line-height:1.42;text-align:center;color:#f6ead6}
.legal{margin:15px 0;padding:14px 13px;border-radius:18px;border:1px solid rgba(255,215,136,.26);background:rgba(0,0,0,.24);font-weight:650}
.check{margin-top:16px;display:flex;align-items:center;gap:12px;padding:14px;border-radius:18px;border:1px solid rgba(255,218,143,.36);background:rgba(0,0,0,.24);text-align:left;color:#fff7e9;font-size:clamp(14px,3.9vw,17px);line-height:1.25}
.check input{appearance:none;width:34px;height:34px;min-width:34px;border-radius:9px;border:2px solid rgba(255,235,184,.88);background:rgba(0,0,0,.4);box-shadow:0 0 18px rgba(255,213,118,.20);position:relative}
.check input:checked{background:linear-gradient(135deg,#fff1bb,#e6a43c 58%,#8e5307);box-shadow:0 0 26px rgba(255,196,79,.72)}
.check input:checked:after{content:"";position:absolute;left:9px;top:3px;width:10px;height:19px;border:solid #120900;border-width:0 4px 4px 0;transform:rotate(45deg)}
.btn{width:100%;border:0;border-radius:24px;margin-top:18px;min-height:66px;background:linear-gradient(135deg,#fff1bb,#e6a43c 54%,#9c5d08);color:#150b02;font-family:Georgia,"Times New Roman",serif;font-size:clamp(21px,6.2vw,31px);box-shadow:0 0 34px rgba(255,190,72,.43),inset 0 0 18px rgba(255,255,255,.22);cursor:pointer}
.btn:disabled{filter:saturate(.45) brightness(.65);cursor:not-allowed}
.preview{position:relative;width:100%;aspect-ratio:9/13;border-radius:24px;overflow:hidden;background:#03070e;border:1px solid rgba(255,215,136,.30);box-shadow:0 0 34px rgba(54,199,255,.18),inset 0 0 28px rgba(255,255,255,.04);margin:14px 0}
.preview video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scaleX(-1);filter:saturate(1.04) contrast(1.03) brightness(1.03)}
.face{position:absolute;left:50%;top:42%;width:54%;height:37%;transform:translate(-50%,-50%);border-radius:45%;border:1px solid rgba(255,220,143,.52);box-shadow:0 0 24px rgba(255,210,104,.22)}
.camera-hint{position:absolute;left:8%;right:8%;bottom:10px;text-align:center;padding:10px 12px;border-radius:16px;background:rgba(0,0,0,.46);font-size:13px;color:#fff0d1;line-height:1.25}
.safe{position:absolute;z-index:30;left:0;right:0;bottom:calc(env(safe-area-inset-bottom) + 12px);text-align:center;color:rgba(255,255,255,.28);font-size:11px;pointer-events:none}
#rescue{display:none!important}
</style>
</head>
<body>
<div class="stage">
  <div class="brand">ETERNA</div>
  <div class="yul"></div>
  <div class="copy"><div id="yulText"></div></div>

  <div class="card" id="consent">
    <h1>Antes de seguir...<br><span>debo confiarte algo.</span></h1>
    <p>Este momento será grabado.</p>
    <div class="legal">Y cuando termine, viajará únicamente hacia la persona que hizo posible que existiera.</div>
    <p>Si decides continuar, aceptas formar parte de esta historia.</p>
    <label class="check"><input id="accept" type="checkbox"><span>He leído y acepto que mi reacción sea grabada y enviada únicamente a la persona que preparó esta ETERNA.</span></label>
    <button class="btn" id="acceptBtn" disabled>Acepto y continúo</button>
  </div>

  <div class="card" id="cameraCard">
    <h1>Algunas historias merecen<br><span>encontrar un rostro.</span></h1>
    <div class="preview">
      <video id="preview" autoplay muted playsinline></video>
      <div class="face"></div>
      <div class="camera-hint">Así te verá este momento.</div>
    </div>
  </div>

  <div class="card" id="ready">
    <h1>Shhh...</h1>
    <p>Esto no es un vídeo.</p>
    <p>Es un momento.</p>
    <p>No pienses. Solo deja que ocurra.</p>
    <button class="btn" id="startBtn">Estoy listo</button>
  </div>

  <button id="rescue" type="button">Abrir mi ETERNA</button>
  <div class="safe">No cierres esta página. ETERNA está abriendo el camino.</div>
</div>

<script>
const token = __RECIPIENT_TOKEN_JSON__;
const placeLine = __PLACE_LINE_JSON__;
const textBox = document.getElementById("yulText");
const consent = document.getElementById("consent");
const cameraCard = document.getElementById("cameraCard");
const ready = document.getElementById("ready");
const accept = document.getElementById("accept");
const acceptBtn = document.getElementById("acceptBtn");
const startBtn = document.getElementById("startBtn");
const preview = document.getElementById("preview");
let stream = null;

function logYul(eventName, meta){
  try{
    const payload = {event:eventName, meta:meta||{}, at:new Date().toISOString()};
    if(navigator.sendBeacon){
      navigator.sendBeacon("/internal/yul-event/" + encodeURIComponent(token), new Blob([JSON.stringify(payload)], {type:"application/json"}));
    }
  }catch(e){}
}

function sleep(ms){ return new Promise(r => setTimeout(r, ms)); }

async function showText(html, small=false, hold=2550){
  // RC89: anti-solape real. Nunca hay dos frases al mismo tiempo.
  textBox.classList.remove("show");
  textBox.className = small ? "small" : "";
  textBox.innerHTML = "";
  await sleep(220);
  textBox.innerHTML = html;
  await sleep(140);
  textBox.classList.add("show");
  await sleep(hold);
  textBox.classList.remove("show");
  await sleep(760);
  textBox.innerHTML = "";
  await sleep(280);
}

async function startCamera(){
  try{
    stream = await navigator.mediaDevices.getUserMedia({video:{facingMode:"user", width:{ideal:640}, height:{ideal:960}}, audio:false});
    preview.srcObject = stream;
  }catch(e){ logYul("camera_preview_error", {error:String(e)}); }
}
function stopCamera(){
  try{ if(stream){ stream.getTracks().forEach(t => t.stop()); stream=null; } }catch(e){}
}

async function openExperience(){
  logYul("guide_start_experience", {});
  try{
    const fd = new FormData();
    fd.append("recipient_token", token);
    const r = await fetch("/start-experience", {
      method:"POST",
      credentials:"same-origin",
      headers: {"x-eterna-ajax":"1"},
      body: fd
    });
    const data = await r.json().catch(()=>({}));
    window.location.href = (data && data.redirect_url) ? data.redirect_url : ("/experiencia/" + encodeURIComponent(token));
  }catch(e){
    window.location.href = "/experiencia/" + encodeURIComponent(token);
  }
}

async function run(){
  logYul("guide_rc89_started", {});
  await sleep(550);
  await showText("Shhh...", false, 2700);
  await showText("Algunas historias comenzaron<br>mucho antes de que llegaras aquí.", true, 3600);
  await showText("Escucha...", false, 2200);
  await showText("Hay rincones donde los minutos<br>pasan sin hacer ruido.", true, 3500);
  await showText("Si conoces uno...<br>quédate allí un instante.", true, 3400);
  await showText(placeLine, true, 3600);
  await showText("Los recuerdos no desaparecen.<br><span>Solo esperan una forma de volver.</span>", true, 3900);

  await sleep(550);
  consent.classList.add("show");
  logYul("guide_consent_visible", {});
}

accept.addEventListener("change", () => { acceptBtn.disabled = !accept.checked; });
acceptBtn.addEventListener("click", async () => {
  if(!accept.checked) return;
  consent.classList.remove("show");
  await sleep(500);
  cameraCard.classList.add("show");
  logYul("guide_camera_visible_4s", {});
  await startCamera();
  await sleep(4000);
  stopCamera();
  cameraCard.classList.remove("show");
  await sleep(500);
  ready.classList.add("show");
  logYul("guide_ready_visible", {});
});
startBtn.addEventListener("click", openExperience);

if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
else run();
</script>
</body>
</html>
"""
    html_doc = html_doc.replace("__RECIPIENT_TOKEN_JSON__", recipient_token_json)
    html_doc = html_doc.replace("__PLACE_LINE_JSON__", json.dumps(place_line))
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
            <div class="payoff-mark" id="payoffMark">♥</div>
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
const recipientName = __RECIPIENT_NAME_JSON__;
const giftAmountDisplay = __GIFT_AMOUNT_DISPLAY_JSON__;
const postGiftHoldMs = hasGift ? 15000 : 3500;
const giftRevealTitle = hasGift
    ? "Has recibido un regalo"
    : "Este momento ya es tuyo";
const giftRevealText = hasGift
    ? giftAmountDisplay
    : "Lo estamos guardando para quien pensó en ti.";
const finalWaitingTitle = "Espere un momento…";
const finalWaitingText = hasGift
    ? "Estamos guardando tu reacción."
    : "Estamos guardando este vídeo para que pueda volver a verlo.";

let stream = null;
let mediaRecorder = null;
let recordedChunks = [];
let finishing = false;
let recordingMimeType = "";
let recordingExtension = "webm";
let experienceStarted = false;
let finishTimeout = null;
let postGiftHoldActive = false;

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
    const markEl = document.getElementById("payoffMark");
    if (markEl) markEl.innerText = "♥";
    if (titleEl) titleEl.innerText = finalWaitingTitle;
    if (textEl) textEl.innerText = finalWaitingText;
    if (payoffLoader) payoffLoader.innerText = "";
    payoff.classList.add("show");
    hideRetryActions();
}

function showGiftRevealScreen() {
    showCinematicLayersAfterVideo();
    const titleEl = document.getElementById("payoffTitle");
    const textEl = document.getElementById("payoffText");
    const markEl = document.getElementById("payoffMark");
    if (markEl) markEl.innerText = hasGift ? "🎁" : "♥";
    if (titleEl) titleEl.innerText = giftRevealTitle;
    if (textEl) textEl.innerText = giftRevealText;
    if (payoffLoader) payoffLoader.innerText = hasGift ? "" : "";
    payoff.classList.add("show");
    hideRetryActions();
}

function startPostVideoGiftHold() {
    if (finishing || postGiftHoldActive) return;
    postGiftHoldActive = true;

    try {
        if (finishTimeout) {
            clearTimeout(finishTimeout);
            finishTimeout = null;
        }
    } catch (_) {}

    showGiftRevealScreen();
    logClientStep("post_video_gift_reveal_started", "ok", "La reacción sigue grabando mientras ve el regalo", { has_gift: hasGift, hold_ms: postGiftHoldMs });

    setTimeout(() => {
        finalizeExperienceFlow();
    }, postGiftHoldMs);
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
    postGiftHoldActive = false;
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
    postGiftHoldActive = false;

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
        startPostVideoGiftHold();
    }, { once: true });

    let fallbackMs = 120000;

    if (Number.isFinite(video.duration) && video.duration > 0) {
        fallbackMs = Math.max(15000, Math.floor(video.duration * 1000) + postGiftHoldMs + 3500);
    }

    finishTimeout = setTimeout(() => {
        startPostVideoGiftHold();
    }, fallbackMs);
}

async function safeResumePlayback() {
    try {
        if (!experienceStarted || finishing) return;

        if (video.ended) {
            startPostVideoGiftHold();
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
    html_page = html_page.replace("__RECIPIENT_NAME_JSON__", json.dumps((order.get("recipient_name") or "").strip() or "esta persona"))
    html_page = html_page.replace("__GIFT_AMOUNT_DISPLAY_JSON__", json.dumps(format_amount_display(gift_amount)))
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

        validate_upload_metadata_safe(video, "video", "reacción")

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

        if not validate_reaction_signature_safe(local_path, extension):
            try:
                os.remove(local_path)
            except Exception:
                pass
            raise HTTPException(status_code=400, detail="invalid_video_signature")

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

    ui_lang = normalize_order_language(order.get("language") or "es")
    if gift_amount <= 0:
        amount_text = eterna_ui_text(ui_lang, "gift_no_money")
        cta_html = f'<a href="/mi-video/{safe_attr(recipient_token)}" class="btn primary">{safe_text(eterna_ui_text(ui_lang, "view_again"))}</a>'
    elif cashout_status == "completed":
        amount_text = eterna_ui_text(ui_lang, "gift_sent").format(amount=format_amount_display(gift_amount))
        cta_html = f'<a href="/mi-video/{safe_attr(recipient_token)}" class="btn primary">{safe_text(eterna_ui_text(ui_lang, "view_again"))}</a>'
    elif cashout_status == "processing":
        amount_text = eterna_ui_text(ui_lang, "gift_processing").format(amount=format_amount_display(gift_amount))
        cta_html = f'<a href="/mi-video/{safe_attr(recipient_token)}" class="btn primary">{safe_text(eterna_ui_text(ui_lang, "view_again"))}</a>'
    elif cashout_status == "ready_to_send":
        amount_text = eterna_ui_text(ui_lang, "gift_received").format(amount=format_amount_display(gift_amount))
        cta_html = f'<form action="/connect/payout/{safe_attr(recipient_token)}" method="post"><button type="submit" class="btn primary">{safe_text(eterna_ui_text(ui_lang, "receive_gift"))}</button></form>'
    else:
        amount_text = eterna_ui_text(ui_lang, "gift_received").format(amount=format_amount_display(gift_amount))
        connect_url = None
        try:
            connect_url = create_connect_onboarding_link(order)
        except Exception as e:
            log_error("create_connect_onboarding_link_en_cobrar", e)
        if connect_url:
            cta_html = f'<a href="{safe_attr(connect_url)}" class="btn primary">{safe_text(eterna_ui_text(ui_lang, "receive_gift"))}</a>'
        else:
            cta_html = f'<a href="" class="btn primary">{safe_text(eterna_ui_text(ui_lang, "try_receive_gift"))}</a>'

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
.reaction-video,.reaction-box,.reaction-window,.reaction-preview,.sender-reaction{right:10px!important;bottom:10px!important;left:auto!important;top:auto!important;transform:none!important;width:clamp(86px,24%,126px)!important;aspect-ratio:9/16!important;border-radius:16px!important;overflow:hidden!important;z-index:20!important;background:#000!important}
.reaction-video video,.reaction-box video,.reaction-window video,.reaction-preview video,.sender-reaction video{width:100%!important;height:100%!important;object-fit:contain!important;object-position:center center!important;transform:none!important;background:#000!important}
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
    RC90 — Sender Pack limpio final.
    Fondo sender_pack_master_v1.png + vídeo 9:16 + reacción más visible + botones.
    Sin "", sin iconos decorativos, sin ruido.
    SOLO layout visual. No toca circuito.
    """
    order = get_order_by_sender_token_or_404(sender_token)
    log_human("REGALANTE HA ABIERTO EL PACK", "🎁 El creador ha abierto el recuerdo", f"🆔 Pedido: {order.get('id')}")
    log_info("🎁 REGALANTE HA ABIERTO EL PACK")
    log_info("🆔 Order ID", order.get("id"))

    original_video_url = (order.get("experience_video_url") or "").strip()
    reaction_url = (order.get("reaction_video_public_url") or "").strip()
    local_reaction_path = best_reaction_local_path(order)
    reaction_video_type = guess_media_type_from_url(reaction_url) if reaction_url else "video/mp4"

    # RC100: si existe reacción normalizada/local estable, el Sender Pack la sirve desde backend.
    # Así evitamos que una URL antigua de R2 apunte a un WEBM/codec problemático.
    if local_reaction_path:
        reaction_url = f"{PUBLIC_BASE_URL}/video/sender-reaction/{sender_token}"
        reaction_video_type = guess_reaction_media_type(order, local_reaction_path)

    if not reaction_url:
        return render_eterna_image_screen(
            image_name="uploading_reaction",
            fallback_image_name="uploading_reaction",
            button_url=f"/sender/{sender_token}",
            button_label=eterna_ui_text(order.get("language"), "check_again"),
            extra_note=eterna_ui_text(order.get("language"), "still_returning"),
        )

    share_url = sender_pack_url_from_order(order)
    sender_bg = eterna_asset("sender_pack")

    original_source_html = ""
    if original_video_url:
        original_source_html = f'<source src="{safe_attr(original_video_url)}" type="video/mp4">'
    reaction_source_html = f'<source src="{safe_attr(reaction_url)}" type="{safe_attr(reaction_video_type)}">'
    ui_lang = normalize_order_language(order.get("language") or "es")
    sender_page_title = eterna_ui_text(ui_lang, "sender_page_title")
    sender_title_html = eterna_ui_text(ui_lang, "sender_title_html")
    sender_aria = eterna_ui_text(ui_lang, "sender_aria")
    reaction_aria = eterna_ui_text(ui_lang, "reaction_aria")
    sender_create_label = "♡ " + eterna_ui_text(ui_lang, "create_another")
    sender_share_label = eterna_ui_text(ui_lang, "share")
    sender_download_label = eterna_ui_text(ui_lang, "download")
    sender_link_copied = eterna_ui_text(ui_lang, "link_copied")
    sender_share_text = eterna_ui_text(ui_lang, "share_text")
    sender_recipient_name = (order.get("recipient_name") or "").strip() or "Esta persona"
    sender_gift_amount = float(order.get("gift_amount") or 0)
    sender_gift_display = format_amount_display(sender_gift_amount)
    if ui_lang == "en":
        sender_gift_card_title = f"{sender_recipient_name} is receiving your gift"
    else:
        sender_gift_card_title = f"{sender_recipient_name} está recibiendo tu regalo"

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="{safe_attr(ui_lang)}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{safe_text(sender_page_title)}</title>
<meta name="theme-color" content="#02050a">
<style>
*{{box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
html,body{{margin:0;width:100%;min-height:100%;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}}
body{{height:100svh;height:100dvh;background:#02050a;overflow:hidden;display:flex;justify-content:center}}
.shell{{position:relative;width:100vw;max-width:520px;height:100svh;height:100dvh;overflow:hidden;background:#02050a}}
.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center top;opacity:.84;z-index:0;pointer-events:none}}
.veil{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.10) 0%,rgba(0,0,0,.16) 28%,rgba(0,0,0,.50) 100%);z-index:1;pointer-events:none}}

/* RC90: desenfoque fuerte del texto integrado en el fondo, sin tocar PNG */
.bg-blur-title{{position:absolute;left:0;right:0;top:calc(env(safe-area-inset-top) + 38px);height:176px;z-index:2;overflow:hidden;pointer-events:none;opacity:.92}}
.bg-blur-title:before{{content:"";position:absolute;left:-18px;right:-18px;top:calc(-1 * (env(safe-area-inset-top) + 38px));height:100svh;background-image:url("{safe_attr(sender_bg)}");background-size:cover;background-position:center top;filter:blur(30px) brightness(.72) saturate(.78);transform:scale(1.08);opacity:.72}}
.bg-blur-title:after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(2,5,10,.30),rgba(2,5,10,.16),rgba(2,5,10,0));backdrop-filter:blur(7px)}}

.header{{position:relative;z-index:4;text-align:center;padding-top:calc(env(safe-area-inset-top) + 10px)}}
.logo{{font-family:Georgia,"Times New Roman",serif;letter-spacing:.42em;color:#eec36a;font-size:clamp(16px,4.5vw,23px);text-shadow:0 0 24px rgba(255,200,93,.66)}}
.logo:after{{content:"♡";display:block;letter-spacing:0;margin-top:4px;font-size:15px;color:#ffd477}}
.title{{margin:8px auto 7px;width:90%;font-family:Georgia,"Times New Roman",serif;font-size:clamp(24px,7vw,38px);line-height:1.04;color:#fff5e8;text-shadow:0 0 24px rgba(0,0,0,.50),0 0 22px rgba(255,255,255,.16)}}
.title span{{color:#f4c46c;text-shadow:0 0 30px rgba(255,199,92,.52),0 0 22px rgba(0,0,0,.50)}}

/* RC90: vídeo un poco más grande y más alto */
.call-frame{{position:relative;z-index:4;width:min(81vw,404px);height:min(68.5svh,682px);margin:4px auto 8px;border-radius:34px;overflow:hidden;background:#000;border:1px solid rgba(255,215,136,.50);box-shadow:0 0 42px rgba(36,171,255,.30),0 0 58px rgba(255,191,83,.18),inset 0 0 26px rgba(255,255,255,.055)}}
.call-frame:before{{content:"";position:absolute;left:50%;top:9px;transform:translateX(-50%);width:72px;height:5px;border-radius:999px;background:rgba(255,236,190,.22);z-index:8;box-shadow:0 0 14px rgba(255,222,150,.18)}}
.main-video{{position:absolute;inset:0;background:#000}}
.main-video video{{width:100%;height:100%;object-fit:cover;object-position:center center;display:block;background:#000}}
.gift-card{{position:absolute;inset:0;z-index:7;display:flex;align-items:center;justify-content:center;text-align:center;padding:28px;background:#02050a;opacity:0;pointer-events:none;transition:opacity .55s ease}}
.gift-card.show{{opacity:1}}
.gift-inner{{width:100%;max-width:300px;margin:0 auto}}
.gift-icon{{width:72px;height:72px;margin:0 auto 22px;border-radius:999px;display:flex;align-items:center;justify-content:center;font-size:36px;color:#f2c878;border:1px solid rgba(242,200,120,.34);background:rgba(242,200,120,.08);box-shadow:0 0 42px rgba(242,200,120,.16)}}
.gift-title{{font-family:Georgia,"Times New Roman",serif;font-size:clamp(22px,6vw,34px);line-height:1.14;color:#fff5e8;text-shadow:0 0 22px rgba(0,0,0,.82);margin:0 0 18px}}
.gift-amount{{font-size:clamp(34px,9vw,58px);font-weight:900;letter-spacing:.02em;color:#f4c46c;text-shadow:0 0 34px rgba(255,199,92,.34)}}

/* RC90: reacción más grande, sin etiqueta */
.reaction-video{{position:absolute;right:10px;top:52px;width:24%;min-width:86px;max-width:126px;aspect-ratio:9/16;border-radius:18px;overflow:hidden;background:#000;border:1.8px solid rgba(255,205,104,.97);box-shadow:0 0 0 1px rgba(255,245,207,.20),0 0 26px rgba(255,183,70,.62),inset 0 0 14px rgba(255,218,137,.20);z-index:9}}
.reaction-video video{{width:100%;height:100%;object-fit:contain;object-position:center center;transform:none;display:block;background:#000}}



/* RC94: SOLO formato del marco PiP de la reacción.
   Objetivo: quitar bandas negras sin tocar cámara, upload, vídeo original ni circuito.
   La clave es que el marco vuelva a ser 9:16 real y el vídeo cubra ese marco. */
.reaction-video,
.reaction-box,
.reaction-window,
.reaction-preview,
.sender-reaction{{
  width:clamp(86px,24%,126px)!important;
  aspect-ratio:9/16!important;
  background:#000!important;
  overflow:hidden!important;
  transform:none!important;
  border-radius:18px!important;
}}
.reaction-video video,
.reaction-box video,
.reaction-window video,
.reaction-preview video,
.sender-reaction video,
video.sender-reaction{{
  width:100%!important;
  height:100%!important;
  object-fit:contain!important;
  object-position:center center!important;
  transform:none!important;
  background:#000!important;
}}
@media(max-width:480px){{
  .reaction-video,.reaction-box,.reaction-window,.reaction-preview,.sender-reaction{{
    width:clamp(82px,24%,118px)!important;
    aspect-ratio:9/16!important;
  }}
}}

/* RC90: botones juntos y más arriba */
.actions{{position:relative;z-index:5;width:min(86vw,420px);margin:-2px auto calc(env(safe-area-inset-bottom) + 12px);display:flex;flex-direction:column;gap:6px}}
.btn{{min-height:47px;border-radius:16px;border:1px solid rgba(255,215,136,.42);display:flex;align-items:center;justify-content:center;gap:9px;text-decoration:none;text-transform:uppercase;letter-spacing:.07em;font-weight:900;color:#fff4dc;background:rgba(0,0,0,.42);box-shadow:0 0 18px rgba(255,205,92,.12),inset 0 0 18px rgba(255,255,255,.035);backdrop-filter:blur(10px);font-size:clamp(12px,3.45vw,15px)}}
.btn.primary{{background:linear-gradient(135deg,#fff1bb,#e6a43c 56%,#9c5d08);color:#170b02;box-shadow:0 0 30px rgba(255,190,72,.38),inset 0 0 18px rgba(255,255,255,.22)}}
.toast{{position:fixed;left:50%;bottom:calc(env(safe-area-inset-bottom) + 18px);transform:translateX(-50%) translateY(16px);padding:10px 14px;border-radius:999px;background:rgba(0,0,0,.72);color:#fff4dc;font-size:13px;opacity:0;transition:all .25s ease;z-index:20}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}

@media(max-height:760px){{
  .header{{padding-top:calc(env(safe-area-inset-top) + 8px)}}
  .title{{font-size:clamp(21px,6.2vw,33px);margin:7px auto 5px}}
  .bg-blur-title{{height:148px}}
  .call-frame{{height:62.5svh;width:min(78vw,382px);border-radius:30px;margin-bottom:6px}}
  .reaction-video{{width:23%;min-width:82px;max-width:118px;top:48px;aspect-ratio:9/16}}
  .btn{{min-height:44px}}
  .actions{{gap:5px;margin-bottom:calc(env(safe-area-inset-bottom) + 9px)}}
}}
@media(max-height:680px){{
  .logo:after{{display:none}}
  .title{{font-size:clamp(19px,5.6vw,30px);margin:4px auto}}
  .bg-blur-title{{height:126px}}
  .call-frame{{height:59svh;width:min(74vw,356px)}}
  .reaction-video{{width:22%;min-width:76px;max-width:108px;top:44px;aspect-ratio:9/16}}
  .btn{{min-height:40px;font-size:12px}}
  .actions{{gap:5px}}
}}
</style>
</head>
<body>
<div class="shell">
  <img class="bg" src="{safe_attr(sender_bg)}" alt="">
  <div class="veil"></div>
  <div class="bg-blur-title" aria-hidden="true"></div>

  <div class="header">
    <div class="logo">ETERNA</div>
    <div class="title">{sender_title_html}</div>
  </div>

  <section class="call-frame" aria-label="{safe_attr(sender_aria)}">
    <div class="main-video">
      <video id="originalVideo" controls playsinline preload="metadata" poster="{safe_attr(sender_bg)}">
        {original_source_html}
      </video>
      <div class="gift-card" id="giftCard" aria-hidden="true">
        <div class="gift-inner">
          <div class="gift-icon">🎁</div>
          <div class="gift-title">{safe_text(sender_gift_card_title)}</div>
          <div class="gift-amount">{safe_text(sender_gift_display)}</div>
        </div>
      </div>
    </div>

    <div class="reaction-video" aria-label="{safe_attr(reaction_aria)}">
      <video id="reactionVideo" muted playsinline preload="metadata">
        {reaction_source_html}
      </video>
    </div>
  </section>

  <nav class="actions">
    <a class="btn primary" href="/crear">{safe_text(sender_create_label)}</a>
    <a class="btn" href="#" id="shareBtn">{safe_text(sender_share_label)}</a>
    <a class="btn" href="{safe_attr(reaction_url)}" download>{safe_text(sender_download_label)}</a>
  </nav>

  <div class="toast" id="toast">{safe_text(sender_link_copied)}</div>
</div>

<script>
(function(){{
  const original = document.getElementById("originalVideo");
  const reaction = document.getElementById("reactionVideo");
  const share = document.getElementById("shareBtn");
  const toast = document.getElementById("toast");
  const giftCard = document.getElementById("giftCard");

  function showToast(msg){{ 
    if(!toast) return; 
    toast.textContent=msg; 
    toast.classList.add("show"); 
    setTimeout(()=>toast.classList.remove("show"),1800); 
  }}

  if(original && reaction){{
    original.addEventListener("play", ()=>{{ 
      try{{ if(giftCard){{ giftCard.classList.remove("show"); giftCard.setAttribute("aria-hidden","true"); }} }}catch(e){{}}
      try{{ reaction.currentTime = original.currentTime || 0; reaction.play().catch(()=>{{}}); }}catch(e){{}} 
    }});
    original.addEventListener("pause", ()=>{{ try{{ reaction.pause(); }}catch(e){{}} }});
    original.addEventListener("seeking", ()=>{{ 
      try{{ if(giftCard){{ giftCard.classList.remove("show"); giftCard.setAttribute("aria-hidden","true"); }} }}catch(e){{}}
      try{{ reaction.currentTime = original.currentTime || 0; }}catch(e){{}} 
    }});
    original.addEventListener("ended", ()=>{{
      try{{ if(giftCard){{ giftCard.classList.add("show"); giftCard.setAttribute("aria-hidden","false"); }} }}catch(e){{}}
      try{{ reaction.play().catch(()=>{{}}); }}catch(e){{}}
      setTimeout(()=>{{ try{{ reaction.pause(); }}catch(e){{}} }}, 15500);
    }});
  }}

  if(share){{
    share.addEventListener("click", async function(e){{
      e.preventDefault();
      const data={{title:"ETERNA", text:{json.dumps(sender_share_text)}, url:{json.dumps(share_url)}}};
      try{{
        if(navigator.share) await navigator.share(data);
        else {{ await navigator.clipboard.writeText(data.url); showToast({json.dumps(sender_link_copied)}); }}
      }}catch(err){{}}
    }});
  }}
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


@app.get("/arrival-photo/{recipient_token}")
def get_arrival_photo(recipient_token: str, slot: str = "photo1"):
    """
    RC101 — mini foto opcional de llegada.
    Solo se sirve si el regalante eligió mostrar identidad.
    Reutiliza una de las 6 fotos; no añade nuevas subidas ni toca el motor.
    """
    order = get_order_by_recipient_token_or_404(recipient_token)
    if not SENDER_IDENTITY_ENABLED or not rc101_truthy(order.get("show_sender_identity")):
        raise HTTPException(status_code=404, detail="Foto de llegada no disponible")

    clean_slot = rc101_clean_photo_slot(slot or order.get("arrival_photo_slot") or ARRIVAL_PHOTO_DEFAULT_SLOT)
    selected_slot = rc101_clean_photo_slot(order.get("arrival_photo_slot") or ARRIVAL_PHOTO_DEFAULT_SLOT)
    if clean_slot != selected_slot:
        clean_slot = selected_slot

    path = get_photo_asset_path(order["id"], clean_slot)
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Foto de llegada no encontrada")

    return FileResponse(
        path,
        media_type=guess_media_type_from_path(path),
        filename=f"eterna-llegada-{order['id']}-{clean_slot}{Path(path).suffix or '.jpg'}",
    )


@app.get("/video/sender-reaction/{sender_token}")
def get_sender_reaction_video(sender_token: str):
    order = get_order_by_sender_token_or_404(sender_token)
    local_path = best_reaction_local_path(order)

    if not local_path or not os.path.exists(local_path):
        raise HTTPException(status_code=404, detail="Vídeo no encontrado")

    return FileResponse(
        local_path,
        media_type=guess_reaction_media_type(order, local_path),
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
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
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
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
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
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
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
        "version": "RC94_SENDER_PACK_PIP_FRAME_9X16_NO_BANDS_SAFE",
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
        "smtp_configured": bool(EMAIL_ENABLED and SMTP_HOST and SMTP_PORT and SMTP_USER and SMTP_PASSWORD and SMTP_FROM),
        "security_headers_enabled": bool(SECURITY_HEADERS_ENABLED),
        "rate_limit_enabled": bool(RATE_LIMIT_ENABLED),
        "max_photo_size_mb": MAX_PHOTO_SIZE_MB,
        "max_reaction_video_mb": MAX_VIDEO_SIZE_MB,
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

    try:
        result["smtp_ok"] = bool(result.get("smtp_configured"))
    except Exception:
        result["smtp_ok"] = False

    critical_ok = bool(result["db"] and result["stripe_configured"] and result["video_engine_configured"])
    if not critical_ok:
        result["status"] = "degraded"

    return result


@app.get("/admin/dashboard-simple", response_class=HTMLResponse)
def admin_dashboard_simple(token: str = ""):
    """
    RC97 — panel privado simple. Solo lectura.
    No toca pedidos ni lógica de ETERNA.
    """
    rc74_admin_guard(token)
    stats = {
        "total": 0,
        "paid": 0,
        "completed": 0,
        "pending_reaction": 0,
        "sms_errors": 0,
        "today": 0,
    }
    recent = []
    try:
        conn = db_conn()
        row = conn.execute("SELECT COUNT(*) AS c FROM orders").fetchone()
        stats["total"] = int(row["c"] or 0)
        row = conn.execute("SELECT COUNT(*) AS c FROM orders WHERE paid=1").fetchone()
        stats["paid"] = int(row["c"] or 0)
        row = conn.execute("SELECT COUNT(*) AS c FROM orders WHERE eterna_completed=1 OR experience_completed=1").fetchone()
        stats["completed"] = int(row["c"] or 0)
        row = conn.execute("SELECT COUNT(*) AS c FROM orders WHERE paid=1 AND COALESCE(reaction_uploaded,0)=0").fetchone()
        stats["pending_reaction"] = int(row["c"] or 0)
        row = conn.execute("SELECT COUNT(*) AS c FROM orders WHERE COALESCE(recipient_sms_error,'')!='' OR COALESCE(sender_sms_error,'')!=''").fetchone()
        stats["sms_errors"] = int(row["c"] or 0)
        today_prefix = now_iso()[:10]
        row = conn.execute("SELECT COUNT(*) AS c FROM orders WHERE COALESCE(created_at,'') LIKE ?", (today_prefix + "%",)).fetchone()
        stats["today"] = int(row["c"] or 0)
        recent = conn.execute(
            """
            SELECT id, created_at, sender_name, recipient_name, paid, reaction_uploaded, experience_completed,
                   recipient_sms_error, sender_sms_error
            FROM orders
            ORDER BY created_at DESC
            LIMIT 12
            """
        ).fetchall()
        conn.close()
    except Exception as e:
        return HTMLResponse(f"<h1>ETERNA Dashboard</h1><p>Error leyendo estado: {safe_text(str(e))}</p>", status_code=500)

    def badge(value):
        return "✅" if value else "⏳"

    rows = ""
    for r in recent:
        err = (r["recipient_sms_error"] or r["sender_sms_error"] or "")
        rows += f"""
        <tr>
            <td><a href='/admin/order-status/{safe_attr(r['id'])}?token={safe_attr(token)}'>{safe_text(r['id'])}</a></td>
            <td>{safe_text((r['created_at'] or '')[:19])}</td>
            <td>{safe_text(r['sender_name'] or '')}</td>
            <td>{safe_text(r['recipient_name'] or '')}</td>
            <td>{badge(r['paid'])}</td>
            <td>{badge(r['reaction_uploaded'])}</td>
            <td>{badge(r['experience_completed'])}</td>
            <td>{safe_text(err[:80])}</td>
        </tr>
        """

    return HTMLResponse(f"""
<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>ETERNA Dashboard</title>
<style>
body{{margin:0;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;padding:24px}}
h1{{font-family:Georgia,serif;color:#f5d28b;margin:0 0 8px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:24px 0}}
.card{{border:1px solid rgba(245,210,139,.25);background:rgba(255,255,255,.045);border-radius:18px;padding:16px}}.num{{font-size:30px;color:#f5d28b;font-weight:700}}
table{{width:100%;border-collapse:collapse;margin-top:18px;background:rgba(255,255,255,.035);border-radius:18px;overflow:hidden}}td,th{{padding:10px;border-bottom:1px solid rgba(255,255,255,.08);font-size:13px;text-align:left}}th{{color:#f5d28b}}a{{color:#f5d28b}}.small{{opacity:.65;font-size:13px}}
</style></head><body>
<h1>ETERNA — Estado privado</h1><div class='small'>Solo lectura. No modifica pedidos. {safe_text(now_iso())}</div>
<div class='grid'>
<div class='card'><div class='num'>{stats['today']}</div><div>Pedidos hoy</div></div>
<div class='card'><div class='num'>{stats['total']}</div><div>Pedidos totales</div></div>
<div class='card'><div class='num'>{stats['paid']}</div><div>Pagados</div></div>
<div class='card'><div class='num'>{stats['completed']}</div><div>Completados</div></div>
<div class='card'><div class='num'>{stats['pending_reaction']}</div><div>Pendientes reacción</div></div>
<div class='card'><div class='num'>{stats['sms_errors']}</div><div>Con error SMS</div></div>
</div>
<h2>Últimos pedidos</h2>
<table><thead><tr><th>Pedido</th><th>Fecha</th><th>Regalante</th><th>Destinatario</th><th>Pago</th><th>Reacción</th><th>Completa</th><th>Error</th></tr></thead><tbody>{rows}</tbody></table>
</body></html>
""")



# =========================================================
# RC104 — FOUNDER EDITION SAFE
# Observabilidad + mantenimiento sin tocar el corazón de ETERNA.
# No toca Stripe Checkout, webhook, Twilio, WhatsApp, video engine,
# cámara, grabación, subida de reacción, Sender Pack ni workers actuales.
# =========================================================

RC104_FOUNDER_VERSION = "RC104_FOUNDER_EDITION_SAFE"
FOUNDER_REPORT_ENABLED = os.getenv("FOUNDER_REPORT_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
FOUNDER_REPORT_HOUR = int(os.getenv("FOUNDER_REPORT_HOUR", "0"))
FOUNDER_REPORT_TO = os.getenv("FOUNDER_REPORT_TO", ADMIN_ALERT_EMAIL or ETERNA_OPERATIONS_EMAIL).strip()
FOUNDER_REPORT_WORKER_INTERVAL_SECONDS = int(os.getenv("FOUNDER_REPORT_WORKER_INTERVAL_SECONDS", "900"))

AUTO_DB_BACKUP_ENABLED = os.getenv("AUTO_DB_BACKUP_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}
AUTO_DB_BACKUP_HOUR = int(os.getenv("AUTO_DB_BACKUP_HOUR", "3"))
AUTO_DB_BACKUP_FOLDER = Path(os.getenv("AUTO_DB_BACKUP_FOLDER", str(DATA_FOLDER / "backups")).strip() or str(DATA_FOLDER / "backups"))
AUTO_DB_BACKUP_KEEP_DAYS = int(os.getenv("AUTO_DB_BACKUP_KEEP_DAYS", "30"))

SAFE_CLEANUP_ENABLED = os.getenv("SAFE_CLEANUP_ENABLED", "0").strip().lower() in {"1", "true", "yes", "on"}
SAFE_CLEANUP_DAYS = int(os.getenv("SAFE_CLEANUP_DAYS", "14"))
SAFE_CLEANUP_DRY_RUN = os.getenv("SAFE_CLEANUP_DRY_RUN", "1").strip().lower() in {"1", "true", "yes", "on"}

RC104_WORKER_STARTED = False
RC104_WORKER_LOCK = threading.Lock()


def rc104_safe_float(value, default=0.0) -> float:
    try:
        return float(value or default)
    except Exception:
        return float(default)


def rc104_today_prefix() -> str:
    return now_iso()[:10]


def rc104_month_prefix() -> str:
    return now_iso()[:7]


def rc104_db_count(query: str, params: tuple = ()) -> int:
    conn = db_conn()
    try:
        row = conn.execute(query, params).fetchone()
        return int((row[0] if row else 0) or 0)
    finally:
        conn.close()


def rc104_db_sum(query: str, params: tuple = ()) -> float:
    conn = db_conn()
    try:
        row = conn.execute(query, params).fetchone()
        return float((row[0] if row else 0) or 0)
    finally:
        conn.close()


def rc104_founder_metrics() -> dict:
    """Métricas de negocio usando solo lectura de la DB."""
    today = rc104_today_prefix()
    month = rc104_month_prefix()
    metrics = {
        "date": today,
        "month": month,
        "orders_today": 0,
        "paid_today": 0,
        "completed_today": 0,
        "reactions_today": 0,
        "revenue_today": 0.0,
        "orders_month": 0,
        "paid_month": 0,
        "revenue_month": 0.0,
        "orders_total": 0,
        "paid_total": 0,
        "revenue_total": 0.0,
        "pending_render": 0,
        "pending_reaction": 0,
        "sms_errors": 0,
        "recent_errors": [],
        "top_occasions": [],
    }
    try:
        metrics["orders_today"] = rc104_db_count("SELECT COUNT(*) FROM orders WHERE COALESCE(created_at,'') LIKE ?", (today + "%",))
        metrics["paid_today"] = rc104_db_count("SELECT COUNT(*) FROM orders WHERE paid=1 AND COALESCE(updated_at, created_at, '') LIKE ?", (today + "%",))
        metrics["completed_today"] = rc104_db_count("SELECT COUNT(*) FROM orders WHERE COALESCE(eterna_completed,0)=1 AND COALESCE(updated_at, created_at, '') LIKE ?", (today + "%",))
        metrics["reactions_today"] = rc104_db_count("SELECT COUNT(*) FROM orders WHERE COALESCE(reaction_uploaded,0)=1 AND COALESCE(updated_at, created_at, '') LIKE ?", (today + "%",))
        metrics["revenue_today"] = rc104_db_sum("SELECT COALESCE(SUM(total_amount),0) FROM orders WHERE paid=1 AND COALESCE(updated_at, created_at, '') LIKE ?", (today + "%",))
        metrics["orders_month"] = rc104_db_count("SELECT COUNT(*) FROM orders WHERE COALESCE(created_at,'') LIKE ?", (month + "%",))
        metrics["paid_month"] = rc104_db_count("SELECT COUNT(*) FROM orders WHERE paid=1 AND COALESCE(updated_at, created_at, '') LIKE ?", (month + "%",))
        metrics["revenue_month"] = rc104_db_sum("SELECT COALESCE(SUM(total_amount),0) FROM orders WHERE paid=1 AND COALESCE(updated_at, created_at, '') LIKE ?", (month + "%",))
        metrics["orders_total"] = rc104_db_count("SELECT COUNT(*) FROM orders")
        metrics["paid_total"] = rc104_db_count("SELECT COUNT(*) FROM orders WHERE paid=1")
        metrics["revenue_total"] = rc104_db_sum("SELECT COALESCE(SUM(total_amount),0) FROM orders WHERE paid=1")
        metrics["pending_render"] = rc104_db_count("SELECT COUNT(*) FROM orders WHERE paid=1 AND COALESCE(video_render_requested,0)=1 AND COALESCE(experience_video_url,'')='' ")
        metrics["pending_reaction"] = rc104_db_count("SELECT COUNT(*) FROM orders WHERE paid=1 AND COALESCE(reaction_uploaded,0)=0")
        metrics["sms_errors"] = rc104_db_count("SELECT COUNT(*) FROM orders WHERE COALESCE(recipient_sms_error,'')!='' OR COALESCE(sender_sms_error,'')!=''")

        conn = db_conn()
        try:
            try:
                rows = conn.execute("""
                    SELECT occasion_type, COUNT(*) AS c
                    FROM memory_events
                    WHERE COALESCE(occasion_type,'')!=''
                    GROUP BY occasion_type
                    ORDER BY c DESC
                    LIMIT 5
                """).fetchall()
                metrics["top_occasions"] = [dict(r) for r in rows]
            except Exception:
                metrics["top_occasions"] = []
            try:
                rows = conn.execute("""
                    SELECT order_id, step, status, message, created_at
                    FROM order_events
                    WHERE LOWER(COALESCE(status,'')) IN ('error','failed')
                    ORDER BY id DESC
                    LIMIT 10
                """).fetchall()
                metrics["recent_errors"] = [dict(r) for r in rows]
            except Exception:
                metrics["recent_errors"] = []
        finally:
            conn.close()
    except Exception as e:
        metrics["metrics_error"] = str(e)
    return metrics


def rc104_system_health() -> dict:
    """Health monitor de solo lectura. No hace cargos ni envíos."""
    health = {
        "version": RC104_FOUNDER_VERSION,
        "timestamp": now_iso(),
        "db": {"status": "unknown"},
        "stripe": {"status": "configured" if bool(STRIPE_SECRET_KEY) else "missing_env"},
        "twilio_sms": {"status": "configured" if bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER) else "missing_env", "enabled": SMS_ENABLED},
        "twilio_whatsapp": {"status": "configured" if bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_WHATSAPP_FROM) else "missing_env", "enabled": WHATSAPP_ENABLED},
        "video_engine": {"status": "unknown", "url": VIDEO_ENGINE_URL},
        "r2": {"status": "configured" if r2_enabled() else "missing: " + ", ".join(r2_missing_config()), "bucket": R2_BUCKET or ""},
        "email": {"status": "configured" if email_enabled_and_configured() else "missing_env_or_disabled", "enabled": EMAIL_ENABLED},
        "safe_mode": ETERNA_SAFE_MODE,
    }
    try:
        conn = db_conn()
        conn.execute("SELECT 1").fetchone()
        order_count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        conn.close()
        health["db"] = {"status": "ok", "orders": int(order_count or 0)}
    except Exception as e:
        health["db"] = {"status": "error", "detail": str(e)[:180]}

    try:
        if VIDEO_ENGINE_URL:
            response = requests.get(f"{VIDEO_ENGINE_URL}/health", timeout=4)
            health["video_engine"] = {"status": "ok" if response.status_code < 500 else "degraded", "http_status": response.status_code, "url": VIDEO_ENGINE_URL}
    except Exception as e:
        health["video_engine"] = {"status": "error", "detail": str(e)[:180], "url": VIDEO_ENGINE_URL}

    overall = "ok"
    for key, value in health.items():
        if isinstance(value, dict) and value.get("status") in {"error"}:
            overall = "error"
            break
        if isinstance(value, dict) and value.get("status") in {"missing_env", "missing_env_or_public_url", "degraded"} and key in {"db", "video_engine"}:
            overall = "degraded"
    health["overall"] = overall
    return health


def rc104_build_founder_report_text(metrics: dict, health: dict) -> str:
    def money(v):
        return f"{rc104_safe_float(v):.2f} €"

    lines = []
    lines.append("🦋 ETERNA FOUNDER REPORT")
    lines.append("")
    lines.append(f"Fecha: {metrics.get('date')}")
    lines.append(f"Estado sistema: {str(health.get('overall') or '').upper()}")
    lines.append("")
    lines.append("VENTAS")
    lines.append(f"- Pedidos creados hoy: {metrics.get('orders_today', 0)}")
    lines.append(f"- Pedidos pagados hoy: {metrics.get('paid_today', 0)}")
    lines.append(f"- Facturación hoy: {money(metrics.get('revenue_today', 0))}")
    lines.append(f"- Facturación mes: {money(metrics.get('revenue_month', 0))}")
    lines.append(f"- Facturación total: {money(metrics.get('revenue_total', 0))}")
    lines.append("")
    lines.append("EXPERIENCIAS")
    lines.append(f"- Completadas hoy: {metrics.get('completed_today', 0)}")
    lines.append(f"- Reacciones recibidas hoy: {metrics.get('reactions_today', 0)}")
    lines.append(f"- Pendientes de reacción: {metrics.get('pending_reaction', 0)}")
    lines.append(f"- Pendientes de render: {metrics.get('pending_render', 0)}")
    lines.append("")
    lines.append("ERRORES")
    lines.append(f"- Pedidos con errores SMS: {metrics.get('sms_errors', 0)}")
    recent_errors = metrics.get("recent_errors") or []
    if recent_errors:
        lines.append("- Últimos errores:")
        for err in recent_errors[:5]:
            lines.append(f"  · {err.get('created_at','')[:19]} · {err.get('order_id','')} · {err.get('step','')} · {err.get('message','')[:90]}")
    else:
        lines.append("- Últimos errores: 0")
    lines.append("")
    lines.append("SISTEMA")
    for key in ["db", "stripe", "twilio_sms", "twilio_whatsapp", "video_engine", "r2", "email"]:
        item = health.get(key) or {}
        lines.append(f"- {key}: {item.get('status', 'unknown')}")
    lines.append("")
    lines.append("Accesos rápidos:")
    lines.append(f"- Dashboard: {PUBLIC_BASE_URL}/admin/dashboard-simple?token=TU_TOKEN")
    lines.append(f"- Health: {PUBLIC_BASE_URL}/admin/system?token=TU_TOKEN")
    lines.append(f"- Caja negra: {PUBLIC_BASE_URL}/admin/blackbox-latest?token=TU_TOKEN")
    return "\n".join(lines)


def rc104_send_founder_report(reason: str = "daily") -> dict:
    metrics = rc104_founder_metrics()
    health = rc104_system_health()
    body = rc104_build_founder_report_text(metrics, health)
    if not FOUNDER_REPORT_TO:
        return {"ok": False, "detail": "FOUNDER_REPORT_TO vacío", "preview": body}
    result = send_eterna_email(
        FOUNDER_REPORT_TO,
        f"🦋 ETERNA Founder Report — {metrics.get('date')} — {health.get('overall','unknown').upper()}",
        body,
    )
    return {"ok": bool(result.get("ok")), "email_result": result, "reason": reason, "metrics": metrics, "health": health}


def rc104_backup_db(reason: str = "manual") -> dict:
    """Copia segura de eterna.db. No borra ni modifica la DB original."""
    try:
        if not DB_PATH.exists():
            return {"ok": False, "detail": f"DB no existe: {DB_PATH}"}
        AUTO_DB_BACKUP_FOLDER.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        target = AUTO_DB_BACKUP_FOLDER / f"eterna_backup_{stamp}.db"
        shutil.copy2(DB_PATH, target)
        insert_order_event("SYSTEM", "rc104_db_backup", "ok", f"Backup DB creado: {target.name}", {"reason": reason, "path": str(target)})
        return {"ok": True, "backup_path": str(target), "backup_name": target.name, "bytes": target.stat().st_size}
    except Exception as e:
        print("[WARN] RC104 backup DB error:", e)
        return {"ok": False, "detail": str(e)}


def rc104_cleanup_old_backups() -> dict:
    """Limpia solo backups antiguos generados por RC104. Nunca toca eterna.db original."""
    deleted = []
    try:
        if not AUTO_DB_BACKUP_FOLDER.exists():
            return {"ok": True, "deleted": deleted}
        cutoff = time.time() - max(1, AUTO_DB_BACKUP_KEEP_DAYS) * 86400
        for p in AUTO_DB_BACKUP_FOLDER.glob("eterna_backup_*.db"):
            try:
                if p.is_file() and p.stat().st_mtime < cutoff:
                    p.unlink()
                    deleted.append(p.name)
            except Exception as e:
                print("[WARN] No pude borrar backup antiguo:", p, e)
        return {"ok": True, "deleted": deleted}
    except Exception as e:
        return {"ok": False, "detail": str(e), "deleted": deleted}


def rc104_safe_cleanup(dry_run: Optional[bool] = None) -> dict:
    """Limpieza segura: solo chunks temporales antiguos. Por defecto dry-run."""
    effective_dry_run = SAFE_CLEANUP_DRY_RUN if dry_run is None else bool(dry_run)
    cutoff = time.time() - max(1, SAFE_CLEANUP_DAYS) * 86400
    targets = [REACTION_CHUNKS_FOLDER]
    result = {"ok": True, "dry_run": effective_dry_run, "deleted_files": [], "candidate_files": [], "bytes_candidate": 0, "bytes_deleted": 0}
    try:
        for folder in targets:
            if not folder.exists() or not folder.is_dir():
                continue
            for p in folder.rglob("*"):
                try:
                    if not p.is_file():
                        continue
                    if p.stat().st_mtime >= cutoff:
                        continue
                    size = p.stat().st_size
                    result["candidate_files"].append(str(p))
                    result["bytes_candidate"] += size
                    if not effective_dry_run:
                        p.unlink()
                        result["deleted_files"].append(str(p))
                        result["bytes_deleted"] += size
                except Exception as e:
                    print("[WARN] RC104 cleanup file skipped:", p, e)
        return result
    except Exception as e:
        result["ok"] = False
        result["detail"] = str(e)
        return result


def rc104_heartbeat_tick():
    """Una vuelta de mantenimiento. No toca core de pedidos."""
    try:
        now = datetime.now(timezone.utc)
        state_file = DATA_FOLDER / "rc104_founder_state.json"
        state = {}
        if state_file.exists():
            try:
                state = json.loads(state_file.read_text(encoding="utf-8") or "{}")
            except Exception:
                state = {}

        today = now.date().isoformat()
        changed = False

        if AUTO_DB_BACKUP_ENABLED and now.hour == AUTO_DB_BACKUP_HOUR and state.get("last_backup_date") != today:
            rc104_backup_db(reason="auto_daily")
            rc104_cleanup_old_backups()
            state["last_backup_date"] = today
            changed = True

        if FOUNDER_REPORT_ENABLED and now.hour == FOUNDER_REPORT_HOUR and state.get("last_founder_report_date") != today:
            rc104_send_founder_report(reason="auto_daily")
            state["last_founder_report_date"] = today
            changed = True

        if SAFE_CLEANUP_ENABLED and state.get("last_safe_cleanup_date") != today:
            rc104_safe_cleanup(dry_run=SAFE_CLEANUP_DRY_RUN)
            state["last_safe_cleanup_date"] = today
            changed = True

        if changed:
            state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print("[WARN] RC104 heartbeat error:", e)


def rc104_worker_loop():
    print("🦋 RC104 Founder Worker iniciado")
    while True:
        try:
            rc104_heartbeat_tick()
        except Exception as e:
            print("[WARN] RC104 worker loop error:", e)
        time.sleep(max(60, FOUNDER_REPORT_WORKER_INTERVAL_SECONDS))


@app.on_event("startup")
def rc104_startup_event():
    global RC104_WORKER_STARTED
    with RC104_WORKER_LOCK:
        if RC104_WORKER_STARTED:
            return
        RC104_WORKER_STARTED = True
    try:
        threading.Thread(target=rc104_worker_loop, daemon=True, name="eterna-rc104-founder-worker").start()
    except Exception as e:
        print("[WARN] No pude iniciar RC104 Founder Worker:", e)


@app.get("/admin/system")
def admin_system_rc104(token: str = ""):
    rc74a_admin_guard(token)
    return rc104_system_health()


@app.get("/admin/founder-report/preview")
def admin_founder_report_preview(token: str = ""):
    rc74a_admin_guard(token)
    metrics = rc104_founder_metrics()
    health = rc104_system_health()
    return {
        "version": RC104_FOUNDER_VERSION,
        "preview_text": rc104_build_founder_report_text(metrics, health),
        "metrics": metrics,
        "health": health,
        "timestamp": now_iso(),
    }


@app.post("/admin/founder-report/send")
def admin_founder_report_send(token: str = ""):
    rc74a_admin_guard(token)
    return rc104_send_founder_report(reason="manual_admin")


@app.post("/admin/backup-db")
def admin_backup_db_rc104(token: str = ""):
    rc74a_admin_guard(token)
    return rc104_backup_db(reason="manual_admin")


@app.get("/admin/cleanup/preview")
def admin_cleanup_preview_rc104(token: str = ""):
    rc74a_admin_guard(token)
    return rc104_safe_cleanup(dry_run=True)


@app.post("/admin/cleanup/run")
def admin_cleanup_run_rc104(token: str = ""):
    rc74a_admin_guard(token)
    if not SAFE_CLEANUP_ENABLED:
        return {"ok": False, "detail": "SAFE_CLEANUP_ENABLED=0. Limpieza real desactivada por seguridad.", "preview": rc104_safe_cleanup(dry_run=True)}
    return rc104_safe_cleanup(dry_run=False)


@app.get("/admin/founder", response_class=HTMLResponse)
def admin_founder_panel_rc104(token: str = ""):
    rc74a_admin_guard(token)
    metrics = rc104_founder_metrics()
    health = rc104_system_health()
    report_text = rc104_build_founder_report_text(metrics, health)
    overall = safe_text(str(health.get("overall") or "unknown").upper())
    color = "#6ee7a8" if overall == "OK" else "#f5d28b"
    return HTMLResponse(f"""
<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>ETERNA Founder</title>
<style>
body{{margin:0;background:#02050a;color:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;padding:24px}}
h1{{font-family:Georgia,serif;color:#f5d28b;margin:0 0 8px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:22px 0}}
.card{{border:1px solid rgba(245,210,139,.22);background:rgba(255,255,255,.045);border-radius:18px;padding:16px}}.num{{font-size:28px;color:#f5d28b;font-weight:800}}.ok{{color:{color};font-weight:900}}
pre{{white-space:pre-wrap;background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.10);border-radius:18px;padding:18px;line-height:1.45}}a{{color:#f5d28b}}
</style></head><body>
<h1>🦋 ETERNA Founder</h1>
<div>Estado sistema: <span class='ok'>{overall}</span> · {safe_text(now_iso())}</div>
<div class='grid'>
<div class='card'><div class='num'>{metrics.get('orders_today',0)}</div><div>Pedidos hoy</div></div>
<div class='card'><div class='num'>{metrics.get('paid_today',0)}</div><div>Pagos hoy</div></div>
<div class='card'><div class='num'>{rc104_safe_float(metrics.get('revenue_today',0)):.2f} €</div><div>Facturación hoy</div></div>
<div class='card'><div class='num'>{rc104_safe_float(metrics.get('revenue_month',0)):.2f} €</div><div>Facturación mes</div></div>
<div class='card'><div class='num'>{metrics.get('pending_render',0)}</div><div>Pendientes render</div></div>
<div class='card'><div class='num'>{metrics.get('pending_reaction',0)}</div><div>Pendientes reacción</div></div>
</div>
<p><a href='/admin/system?token={safe_attr(token)}'>Health JSON</a> · <a href='/admin/blackbox-latest?token={safe_attr(token)}'>Caja negra</a> · <a href='/admin/cleanup/preview?token={safe_attr(token)}'>Preview limpieza</a></p>
<pre>{safe_text(report_text)}</pre>
</body></html>
""")

# =========================================================
# FIN RC104 — FOUNDER EDITION SAFE
# =========================================================


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port
    )

# =========================================================
# RC103 — CAJA NEGRA ETERNA READ ONLY
# No toca Stripe, Twilio, WhatsApp, video engine, cámara, reacción ni workers.
# Solo lee orders + order_events para saber dónde está cada pedido.
# =========================================================

def rc103_blackbox_public_order(order: dict) -> dict:
    """Resumen seguro y legible del pedido para admin."""
    if not order:
        return {}
    try:
        state = rc74a_order_public_state(order)
    except Exception:
        state = "UNKNOWN"

    fields = [
        "id", "paid", "delivered_to_recipient", "delivery_sent", "delivery_sent_at",
        "video_render_requested", "video_render_requested_at", "experience_video_url",
        "experience_started", "experience_completed", "reaction_uploaded", "sender_notified",
        "recipient_sms_attempts", "sender_sms_attempts", "recipient_sms_error", "sender_sms_error",
        "recipient_sms_sent_at", "sender_sms_sent_at", "created_at", "updated_at",
        "delivery_mode", "scheduled_delivery_at", "eterna_completed", "reaction_upload_error",
    ]
    data = {k: order.get(k) for k in fields if k in order.keys()}
    data["state"] = state
    data["minutes_since_created"] = rc74a_minutes_since(order.get("created_at"))
    data["minutes_since_render_requested"] = rc74a_minutes_since(order.get("video_render_requested_at"))
    data["has_experience_video"] = bool(order.get("experience_video_url"))
    data["has_reaction_local"] = bool(order.get("reaction_video_local"))
    data["has_reaction_public"] = bool(order.get("reaction_video_public_url"))
    return data


def rc103_blackbox_flags(order: dict, events: list) -> list:
    """Señales rápidas de atención. No modifica nada."""
    flags = []
    if not order:
        return ["pedido_no_encontrado"]

    if order.get("paid") and not order.get("video_render_requested"):
        flags.append("pagado_sin_render_solicitado")
    if order.get("video_render_requested") and not order.get("experience_video_url"):
        mins = rc74a_minutes_since(order.get("video_render_requested_at"))
        if mins is not None and mins >= ETERNA_RENDER_STUCK_MINUTES:
            flags.append("render_posiblemente_atascado")
    if order.get("experience_video_url") and not (order.get("delivered_to_recipient") or order.get("delivery_sent")):
        flags.append("video_listo_no_entregado")
    if order.get("experience_completed") and not order.get("reaction_uploaded"):
        flags.append("experiencia_completada_sin_reaccion")
    if order.get("reaction_uploaded") and not order.get("sender_notified"):
        flags.append("reaccion_lista_sender_pendiente")
    if order.get("recipient_sms_error"):
        flags.append("error_sms_destinatario")
    if order.get("sender_sms_error"):
        flags.append("error_sms_regalante")

    for ev in events or []:
        if str(ev.get("status") or "").lower() in {"error", "failed"}:
            flags.append("evento_error_en_timeline")
            break
    return flags


@app.get("/admin/blackbox/{order_id}")
def admin_blackbox_order(order_id: str, token: str = ""):
    """
    Caja Negra por pedido.
    Modo lectura: permite ver el viaje exacto del pedido sin tocar producción.
    """
    rc74a_admin_guard(token)
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="pedido_no_encontrado")

    events = list_order_events(order_id, limit=240)
    public_order = rc103_blackbox_public_order(order)
    flags = rc103_blackbox_flags(order, events)

    return {
        "version": "RC103_BLACKBOX_NO_ZOOM_VISITOR_SAFE",
        "mode": "read_only",
        "order": public_order,
        "flags": flags,
        "timeline": events,
        "quick_links": {
            "html_status": f"/admin/order-status/{order_id}?token=TU_TOKEN",
            "sender_pack": f"/sender/{order.get('sender_token')}" if order.get("sender_token") else None,
            "recipient_experience": f"/pedido/{order.get('recipient_token')}" if order.get("recipient_token") else None,
        },
        "timestamp": now_iso(),
    }


@app.get("/admin/blackbox-latest")
def admin_blackbox_latest(token: str = "", limit: int = 20):
    """
    Últimos pedidos en modo caja negra resumida.
    No cambia DB, no reintenta, no envía mensajes.
    """
    rc74a_admin_guard(token)
    clean_limit = max(1, min(int(limit or 20), 80))
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM orders
        ORDER BY created_at DESC
        LIMIT ?
    """, (clean_limit,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    items = []
    for order in rows:
        events = list_order_events(order.get("id"), limit=40)
        item = rc103_blackbox_public_order(order)
        item["flags"] = rc103_blackbox_flags(order, events)
        item["last_event"] = events[-1] if events else None
        items.append(item)

    return {
        "version": "RC103_BLACKBOX_NO_ZOOM_VISITOR_SAFE",
        "mode": "read_only",
        "count": len(items),
        "orders": items,
        "timestamp": now_iso(),
    }



# =========================================================
# RC112G — FULL ENGLISH SERVER-SIDE FORM PATCH
# Último parche: si /crear?lang=en, el HTML sale ya traducido desde servidor.
# No depende de que un botón JS recorra media pantalla.
# Solo afecta al formulario /crear. No toca Stripe, SMS, vídeo, sender pack ni reacción.
# =========================================================
_ORIGINAL_RENDER_CREATE_FORM_RC112G = render_create_form


def _eterna_force_english_create_form_html(html: str) -> str:
    replacements = {
        'lang="es"': 'lang="en"',
        '<title>Crear ETERNA</title>': '<title>Create ETERNA</title>',
        'Crea algo que no se abra. Se viva.': 'Create something they do not just open. They live it.',
        'No todo lo importante': 'Not everything important',
        'debería desaparecer.': 'should disappear.',
        'Haz que vuelva convertido': 'Make it return as',
        'en emoción real.': 'real emotion.',
        'Primero construimos el recuerdo. Luego decidimos cómo vuelve.': 'First we build the memory. Then we decide how it returns.',
        'Ahora dale intención: palabras, momento de entrega y pago seguro.': 'Now give it intention: words, delivery moment and secure payment.',
        'Quién lo crea': 'Who creates it',
        'QUIÉN LO CREA': 'WHO CREATES IT',
        'Quién lo va a vivir': 'Who will live it',
        'QUIÉN LO VA A VIVIR': 'WHO WILL LIVE IT',
        'Tu nombre': 'Your name',
        'Tu email': 'Your email',
        'Tu teléfono': 'Your phone',
        'Su nombre': 'Their name',
        'Su teléfono': 'Their phone',
        'Su email (opcional, por si el SMS falla)': 'Their email (optional, in case SMS fails)',
        'Escríbelo como lo tengas guardado 💛': 'Write it as you have it saved 💛',
        'No hace falta poner el prefijo.': 'No need to add the country code.',
        '¿Para quién es esta ETERNA?': 'Who is this ETERNA for?',
        'Elige una ocasión. Solo nos ayuda a entender el tono. No complica el proceso.': 'Choose an occasion. It only helps us understand the tone. It does not complicate the process.',
        '❤️ Pareja': '❤️ Partner',
        'Amor, aniversario o algo que no sabes decir.': 'Love, anniversary or something you do not know how to say.',
        '👩 Madre': '👩 Mother',
        'Para agradecer todo lo que siempre estuvo.': 'To thank everything that was always there.',
        '👨 Padre': '👨 Father',
        'Para reconocer lo que a veces no se dice.': 'To recognize what is not always said.',
        '🎂 Cumpleaños': '🎂 Birthday',
        'Una sorpresa que se vive de verdad.': 'A surprise that is truly lived.',
        '🤝 Amistad': '🤝 Friendship',
        'Para alguien que siempre estuvo cerca.': 'For someone who was always close.',
        '🌍 A distancia': '🌍 Long distance',
        'Cuando está lejos, pero sigue aquí.': 'When they are far away, but still here.',
        '✨ Otro momento': '✨ Another moment',
        'Cuando simplemente quieres emocionar.': 'When you simply want to move someone.',
        'El alma de Yul': "Yul's soul",
        'EL ALMA DE YUL': "YUL'S SOUL",
        'Una sola pista. Un lugar. Yul no necesita saber más para encontrar una puerta.': 'One clue. One place. Yul does not need more to find a doorway.',
        '¿Hay algún lugar que forme parte de vuestra historia?': 'Is there a place that belongs to your story?',
        'Ej: Cádiz, la montaña, la casa de la abuela, un banco, París...': 'E.g. Cádiz, the mountains, grandma’s house, a bench, Paris...',
        'No expliques el recuerdo. Solo escribe el lugar. Yul hará el resto.': 'Do not explain the memory. Just write the place. Yul will do the rest.',
        'Los recuerdos': 'The memories',
        'LOS RECUERDOS': 'THE MEMORIES',
        'Elige entre 4 y 6 fotos desde tu galería. ETERNA las optimiza automáticamente para que carguen mejor en móvil.': 'Choose 4 to 6 photos from your gallery. ETERNA will prepare them safely for mobile.',
        'Elige entre 4 y 6 fotos. Si subes 4, ETERNA completará el vídeo de forma discreta.': 'Choose 4 to 6 photos. If you upload 4, ETERNA will complete the video discreetly.',
        'Seleccionar recuerdos': 'Select memories',
        'Seleccionar 6 recuerdos': 'Select 6 memories',
        'Puedes elegir varias fotos de una vez. Después podrás cambiar cualquiera individualmente.': 'You can choose several photos at once. Afterwards, you can replace any of them individually.',
        'Puedes elegir las 6 fotos de una vez. Después podrás cambiar cualquiera individualmente.': 'You can choose all 6 photos at once. Afterwards, you can replace any of them individually.',
        'Abrir galería': 'Open gallery',
        'FOTO': 'PHOTO',
        'Foto': 'Photo',
        'Cambiar': 'Change',
        'Pendiente': 'Pending',
        'Recomendación: formato vertical. Lo importante es que sean recuerdos que de verdad tengan sentido.': 'Tip: vertical photos are ideal. What matters most is that they are real memories.',
        'Sube al menos 4 fotos. Si tienes 6, mejor.': 'Upload at least 4 photos. 6 is ideal.',
        '¿Quieres que la persona sepa quién le envía esta ETERNA?': 'Do you want the recipient to know who sent this ETERNA?',
        'Sí, mostrar una foto': 'Yes, show a photo',
        'No, mantener la sorpresa': 'No, keep the surprise',
        'Foto de llegada:': 'Arrival photo:',
        'Esta mini foto puede aparecer como imagen de llegada para dar confianza. No cambia el vídeo.': 'This mini photo may appear as an arrival image to build trust. It does not change the video.',
        'Qué quieres provocar': 'Type of emotion',
        'TIPO DE EMOCIÓN': 'TYPE OF EMOTION',
        'Cumpleaños': 'Birthday',
        'Un día que merece quedarse.': 'A day worth keeping.',
        'Amor': 'Love',
        'Cuando lo que sientes ya no cabe dentro.': 'When what you feel no longer fits inside.',
        'Mamá': 'Mom',
        'Para quien siempre fue hogar.': 'For the one who was always home.',
        'Papá': 'Dad',
        'Para quien dejó huella sin hacer ruido.': 'For the one who left a mark quietly.',
        'Familia': 'Family',
        'Para quienes siempre vuelven a ti.': 'For those who always come back to you.',
        'Amistad': 'Friendship',
        'Para esa persona que se quedó.': 'For the person who stayed.',
        'Distancia': 'Distance',
        'Cuando alguien está lejos, pero sigue cerca.': 'When someone is far away, but still close.',
        'Perdón': 'Forgiveness',
        'Para decir algo que cuesta decir.': 'To say something hard to say.',
        'Reencuentro': 'Reunion',
        'Cuando algo vuelve después del tiempo.': 'When something returns after time.',
        'Gracias': 'Thank you',
        'Para agradecer de verdad.': 'To truly say thank you.',
        'Superación': 'Overcoming',
        'Para recordarle todo lo que vale.': 'To remind them how much they are worth.',
        'Sorpresa': 'Surprise',
        'Cuando quieres tocar el corazón sin avisar.': 'When you want to touch their heart without warning.',
        'Esfuerzo': 'Effort',
        'No sé cómo decirlo': 'I do not know how to say it',
        'Cuando ETERNA debe decirlo por ti.': 'When ETERNA should say it for you.',

        'Elige 6 fotos directamente desde tu galería. Se cargan de forma nativa para que el proceso sea rápido.': 'Choose 6 photos directly from your gallery. They load natively so the process stays fast.',
        'Se cargan de forma nativa para que el proceso sea rápido.': 'They load natively so the process stays fast.',
        'para poder continuar. Si tienes 4, ETERNA completará las 6.': 'to continue. If you have 4, ETERNA will complete the 6.',
        'Toca esta foto otra vez para subirla.': 'Tap this photo again to upload it.',
        'Opcional si ya tienes 4 fotos.': 'Optional if you already have 4 photos.',
        'Necesaria para crear tu ETERNA.': 'Required to create your ETERNA.',
        'Las palabras': 'Your words',
        'TUS PALABRAS': 'YOUR WORDS',
        'Quiero que ETERNA encuentre las palabras': 'I want ETERNA to find the words',
        '(recomendado)': '(recommended)',
        'Quiero escribir lo que siento': 'I want to write what I feel',
        'Lo que nunca quieres que olvide': 'What you never want them to forget',
        'Eso que sientes y a veces no dices': 'What you feel and sometimes do not say',
        'La frase que quieres dejarle para siempre': 'The sentence you want to leave them forever',
        '¿Necesitas inspiración?': 'Need inspiration?',
        'Ver frases sugeridas': 'See suggested phrases',
        'Gracias por estar siempre.': 'Thank you for always being there.',
        'Hay personas que se quedan para siempre.': 'Some people stay forever.',
        'Hoy quería recordarte algo bonito.': 'Today I wanted to remind you of something beautiful.',
        'Aunque estemos lejos, sigues aquí.': 'Even if we are far apart, you are still here.',
        'Nunca olvides lo importante que eres para mí.': 'Never forget how important you are to me.',
        'El momento exacto': 'The exact moment',
        'Puedes dejar que llegue en cuanto esté lista...': 'You can let it arrive as soon as it is ready...',
        'o programar ese momento íntimo en el que sabes que podrá vivirla de verdad.': 'or schedule that intimate moment when you know they will truly be able to live it.',
        'Enviarlo en cuanto esté listo': 'Send it as soon as it is ready',
        'Sin coste extra.': 'No extra cost.',
        'Guardarlo y entregarlo en un momento exacto': 'Save it and deliver it at an exact moment',
        'para guardarlo y hacer que llegue exactamente cuando tú elijas.': 'to save it and deliver it exactly when you choose.',
        'Lo ideal es que pueda vivirlo con calma.': 'Ideally, they can experience it calmly.',
        'Con unos cascos. En silencio. Sin que nadie le moleste.': 'With headphones. In silence. Without being disturbed.',
        'Dinero a regalar': 'Gift amount',
        'DINERO A REGALAR': 'GIFT AMOUNT',
        'Precio base ETERNA:': 'Base ETERNA price:',
        'Si añades regalo económico:': 'If you add a money gift:',
        'gestión segura': 'secure handling',
        'del importe regalado': 'of the gifted amount',
        'Entrega programada:': 'Scheduled delivery:',
        'solo si eliges guardarlo y entregarlo en un momento exacto': 'only if you choose to save it and deliver it at an exact moment',
        'Privado y seguro': 'Private and secure',
        '✓ Tus fotos son privadas.': '✓ Your photos are private.',
        '✓ El pago se realiza de forma segura con Stripe.': '✓ Payment is processed securely with Stripe.',
        '✓ La reacción solo vuelve a quien crea esta ETERNA.': '✓ The reaction only returns to the person who creates this ETERNA.',
        '✓ Si añades dinero, lo recibirá la persona destinataria.': '✓ If you add money, the recipient will receive it.',
        '✓ Soporte:': '✓ Support:',
        'No solo eliges lo que va a sentir. También eliges cuándo debe ocurrir.': 'You do not only choose what they will feel. You also choose when it should happen.',
        'Acepto crear esta ETERNA de forma responsable. Entiendo que, si la persona destinataria vive la experiencia, podré recibir un recuerdo privado de ese momento. Me comprometo a tratar ese contenido con respeto, a no utilizarlo de forma ofensiva, invasiva o pública, y a compartirlo solo de manera responsable.': 'I accept creating this ETERNA responsibly. I understand that, if the recipient experiences it, I may receive a private memory of that moment. I commit to treating that content with respect, not using it in an offensive, invasive or public way, and sharing it only responsibly.',
        'Al continuar, aceptas las': 'By continuing, you accept the',
        'condiciones': 'terms',
        'política de privacidad': 'privacy policy',
        'y la': 'and the',
        'Crear y pasar al pago seguro': 'Continue to payment',
        'CONTINUAR AL PAGO': 'CONTINUE TO PAYMENT',
        'Abriendo pago seguro ETERNA': 'Opening secure ETERNA payment',
        'Fotos cargadas. Te faltan': 'Photos loaded. You still need',
        'para poder continuar. Si tienes 4, ETERNA completará las 6.': 'to continue. If you have 4, ETERNA will complete the 6.',
        '6 fotos listas. Puedes cambiar cualquiera tocando su casilla.': '6 photos ready. You can change any of them by tapping its box.',
        'fotos listas. ETERNA completará las 6.': 'photos ready. ETERNA will complete the 6.',
    }
    # RC112H — barrido final de textos visibles del formulario completo.
    replacements.update({
        'Elige 6 fotos directamente desde tu galería. Se cargan de forma nativa para que el proceso sea rápido.': 'Choose 6 photos directly from your gallery. They load natively so the process stays fast.',
        'Elige 6 fotos directamente desde tu galería. ETERNA las optimiza automáticamente para que carguen mejor en móvil.': 'Choose 6 photos directly from your gallery. They load natively so the process stays fast.',
        'Seleccionar 6 recuerdos': 'Select 6 memories',
        'Puedes elegir las 6 fotos de una vez. Después podrás cambiar cualquiera individualmente.': 'You can select all 6 photos at once. Afterwards, you can replace any of them individually.',
        'Pendiente': 'Pending', 'Cargando foto...': 'Loading photo...', 'Subiendo foto...': 'Uploading photo...',
        'Foto lista': 'Photo ready', 'Foto subida': 'Photo uploaded', 'Foto recuperada': 'Photo recovered',
        'Tus palabras': 'Your words', 'TUS PALABRAS': 'YOUR WORDS',
        'Dinero a regalar (€)': 'Gift amount (€)', 'Dinero a regalar': 'Gift amount', 'DINERO A REGALAR': 'GIFT AMOUNT',
        'Crear y pasar al pago seguro': 'Continue to secure payment', 'Abrir galería': 'Open gallery', 'Cambiar': 'Change',
        'FOTO 1': 'PHOTO 1', 'FOTO 2': 'PHOTO 2', 'FOTO 3': 'PHOTO 3', 'FOTO 4': 'PHOTO 4', 'FOTO 5': 'PHOTO 5', 'FOTO 6': 'PHOTO 6',
        'Foto 1': 'Photo 1', 'Foto 2': 'Photo 2', 'Foto 3': 'Photo 3', 'Foto 4': 'Photo 4', 'Foto 5': 'Photo 5', 'Foto 6': 'Photo 6',
        'Elige una ocasión. Solo nos ayuda a entender el tono. No complica el proceso.': 'Choose an occasion. It only helps us understand the tone. It does not complicate the process.',
        '¿Para quién es esta ETERNA?': 'Who is this ETERNA for?', 'Quién lo crea': 'Who creates it', 'Quién lo va a vivir': 'Who will receive it',
        'El alma de Yul': "Yul's soul",
        'Una sola pista. Un lugar. Yul no necesita saber más para encontrar una puerta.': 'One clue. One place. Yul does not need more to find a doorway.',
        '¿Hay algún lugar que forme parte de vuestra historia?': 'Is there a place that belongs to your story?',
        'Ej: Cádiz, la montaña, la casa de la abuela, un banco, París...': "E.g. Cádiz, the mountains, grandma's house, a bench, Paris...",
        'No expliques el recuerdo. Solo escribe el lugar. Yul hará el resto.': 'Do not explain the memory. Just write the place. Yul will do the rest.',
        'Los recuerdos': 'The memories', 'Qué quieres provocar': 'What do you want to make them feel?', 'TIPO DE EMOCIÓN': 'TYPE OF EMOTION',
        'Las palabras': 'Your words', 'El momento exacto': 'The exact moment',
        'Puedes dejar que llegue en cuanto esté lista...': 'You can let it arrive as soon as it is ready...',
        'o programar ese momento íntimo en el que sabes que podrá vivirla de verdad.': 'or schedule that intimate moment when you know they can truly live it.',
        'Enviarlo en cuanto esté listo': 'Send it as soon as it is ready', 'Sin coste extra.': 'No extra cost.',
        'Guardarlo y entregarlo en un momento exacto': 'Save it and deliver it at an exact moment',
        'para guardarlo y hacer que llegue exactamente cuando tú elijas.': 'to save it and make it arrive exactly when you choose.',
        'Lo ideal es que pueda vivirlo con calma.': 'Ideally, they should experience it calmly.',
        'Con unos cascos. En silencio. Sin que nadie le moleste.': 'With headphones. In silence. Without being disturbed.',
        'Precio base ETERNA': 'Base ETERNA price', 'Si añades regalo económico': 'If you add a money gift',
        'gestión segura': 'secure handling', 'del importe regalado': 'of the gifted amount',
        'Entrega programada': 'Scheduled delivery',
        'solo si eliges guardarlo y entregarlo en un momento exacto': 'only if you choose to save it and deliver it at an exact moment',
        'Privado y seguro': 'Private and secure', 'Tus fotos son privadas.': 'Your photos are private.',
        'El pago se realiza de forma segura con Stripe.': 'Payment is processed securely with Stripe.',
        'La reacción solo vuelve a quien crea esta ETERNA.': 'The reaction only returns to the person who created this ETERNA.',
        'Si añades dinero, lo recibirá la persona destinataria.': 'If you add money, the recipient will receive it.',
        'Soporte:': 'Support:',
        'No solo eliges lo que va a sentir. También eliges cuándo debe ocurrir.': 'You do not only choose what they will feel. You also choose when it should happen.',
        'Acepto crear esta ETERNA de forma responsable. Entiendo que, si la persona destinataria vive la experiencia, podré recibir un recuerdo privado de ese momento. Me comprometo a tratar ese contenido con respeto, a no utilizarlo de forma ofensiva, invasiva o pública, y a compartirlo solo de manera responsable.': 'I accept creating this ETERNA responsibly. I understand that, if the recipient lives the experience, I may receive a private memory of that moment. I commit to treating that content with respect, not using it in an offensive, invasive or public way, and sharing it only responsibly.',
        'Al continuar, aceptas las': 'By continuing, you accept the', 'condiciones': 'terms', 'y la': 'and the', 'política de privacidad': 'privacy policy',
        'Abriendo pago seguro ETERNA': 'Opening secure ETERNA payment',
        'Quiero que ETERNA encuentre las palabras': 'I want ETERNA to find the words', 'Quiero escribir lo que siento': 'I want to write what I feel',
        'Ver frases sugeridas': 'See suggested phrases', 'Gracias por estar siempre.': 'Thank you for always being there.',
        'Hay personas que se quedan para siempre.': 'Some people stay forever.', 'Hoy quería recordarte algo bonito.': 'Today I wanted to remind you of something beautiful.',
        'Aunque estemos lejos, sigues aquí.': 'Even if we are far apart, you are still here.', 'Nunca olvides lo importante que eres para mí.': 'Never forget how important you are to me.',
        'Lo que nunca quieres que olvide': 'What you never want them to forget', 'Eso que sientes y a veces no dices': 'What you feel and sometimes do not say',
        'La frase que quieres dejarle para siempre': 'The sentence you want to leave them forever', '¿Necesitas inspiración?': 'Need inspiration?',
        'Pareja': 'Partner', 'Madre': 'Mother', 'Padre': 'Father', 'Cumpleaños': 'Birthday', 'Amistad': 'Friendship', 'A distancia': 'Long distance',
        'Otro momento': 'Another moment', 'Amor': 'Love', 'Mamá': 'Mom', 'Papá': 'Dad', 'Familia': 'Family', 'Distancia': 'Distance', 'Perdón': 'Forgiveness', 'Reencuentro': 'Reunion', 'Gracias': 'Thank you', 'Superación': 'Overcoming', 'Sorpresa': 'Surprise', 'Esfuerzo': 'Effort', 'No sé cómo decirlo': 'I do not know how to say it',
        'Amor, aniversario o algo que no sabes decir.': 'Love, anniversary or something you do not know how to say.',
        'Para agradecer todo lo que siempre estuvo.': 'To thank everything that was always there.',
        'Para reconocer lo que a veces no se dice.': 'To recognize what is not always said.',
        'Una sorpresa que se vive de verdad.': 'A surprise that is truly lived.',
        'Para alguien que siempre estuvo cerca.': 'For someone who was always close.',
        'Cuando está lejos, pero sigue aquí.': 'When they are far away, but still here.',
        'Cuando simplemente quieres emocionar.': 'When you simply want to move someone.',
        'Un día que merece quedarse.': 'A day worth keeping.',
        'Cuando lo que sientes ya no cabe dentro.': 'When what you feel no longer fits inside.',
        'Para quien siempre fue hogar.': 'For the one who was always home.',
        'Para quien dejó huella sin hacer ruido.': 'For the one who left a mark quietly.',
        'Para quienes siempre vuelven a ti.': 'For those who always come back to you.',
        'Para esa persona que se quedó.': 'For the person who stayed.',
        'Cuando alguien está lejos, pero sigue cerca.': 'When someone is far away, but still close.',
        'Para decir algo que cuesta decir.': 'To say something hard to say.',
        'Cuando algo vuelve después del tiempo.': 'When something returns after time.',
        'Para agradecer de verdad.': 'To truly say thank you.',
        'Para recordarle todo lo que vale.': 'To remind them how much they are worth.',
        'Cuando quieres tocar el corazón sin avisar.': 'When you want to touch their heart without warning.',
        'Cuando ETERNA debe decirlo por ti.': 'When ETERNA should say it for you.',

        'Elige 6 fotos directamente desde tu galería. Se cargan de forma nativa para que el proceso sea rápido.': 'Choose 6 photos directly from your gallery. They load natively so the process stays fast.',
        'Se cargan de forma nativa para que el proceso sea rápido.': 'They load natively so the process stays fast.',
        'para poder continuar. Si tienes 4, ETERNA completará las 6.': 'to continue. If you have 4, ETERNA will complete the 6.',
        'Toca esta foto otra vez para subirla.': 'Tap this photo again to upload it.',
        'Opcional si ya tienes 4 fotos.': 'Optional if you already have 4 photos.',
        'Necesaria para crear tu ETERNA.': 'Required to create your ETERNA.',
    })
    for old, new in replacements.items():
        html = html.replace(old, new)
    # RC112I: no reemplazamos value="es" de forma global porque rompe data-lang="es"
    # del botón Español y cualquier otro atributo del formulario. Solo tocamos el hidden real.
    html = html.replace('name="language" id="language" value="es"', 'name="language" id="language" value="en"')
    # RC112J: algunos barridos de texto pueden tocar atributos data-lang por coincidencia.
    # Blindamos los botones: Español siempre data-lang=es; English siempre data-lang=en.
    html = html.replace('href="/crear?lang=es" role="button" class="language-option " data-lang="en"', 'href="/crear?lang=es" role="button" class="language-option " data-lang="es"')
    html = html.replace('href="/crear?lang=es" role="button" class="language-option active" data-lang="en"', 'href="/crear?lang=es" role="button" class="language-option active" data-lang="es"')
    return html


def render_create_form(initial_language: str = "es") -> str:
    lang = "en" if str(initial_language or "").lower().strip() == "en" else "es"
    html = _ORIGINAL_RENDER_CREATE_FORM_RC112G(lang)
    if lang == "en":
        html = _eterna_force_english_create_form_html(html)
    return html


# =========================================================
# RC113 — FORMULARIO ENGLISH FINAL SWEEP + NATIVE GALLERY SAFE
# Último cerrojo limitado al formulario /crear:
# - No toca Stripe, SMS, WhatsApp, vídeo, reacción, sender pack ni DB.
# - Corrige textos dinámicos de galería.
# - Traduce pantalla 422 básica de forma bilingüe.
# - Mantiene data-lang blindado.
# =========================================================
_ORIGINAL_RENDER_CREATE_FORM_RC113 = render_create_form

def _eterna_rc113_final_form_lock(html: str, lang: str = "es") -> str:
    if str(lang or "").lower().strip() != "en":
        return html

    final_replacements = {
        "Fotos cargadas. Te faltan": "Photos loaded. You still need",
        "para poder continuar. Si tienes 4, ETERNA completará las 6.": "to continue. If you have 4, ETERNA will complete the 6.",
        "6 fotos listas. Puedes cambiar cualquiera tocando su casilla.": "6 photos ready. You can change any of them by tapping its box.",
        "fotos listas. ETERNA completará las 6.": "photos ready. ETERNA will complete the 6.",
        "Elige 6 fotos directamente desde tu galería. Se cargan de forma nativa para que el proceso sea rápido.": "Choose 6 photos directly from your gallery. They load natively so the process stays fast.",
        "Elige 6 fotos directamente desde tu galería. ETERNA las optimiza automáticamente para que carguen mejor en iPhone.": "Choose 6 photos directly from your gallery. They load natively so the process stays fast.",
        "Elige 6 fotos directamente desde tu galería. ETERNA las optimiza automáticamente para que carguen mejor en móvil.": "Choose 6 photos directly from your gallery. They load natively so the process stays fast.",
        "Formulario incompleto / Incomplete form": "Incomplete form",
        "Vuelve a intentarlo desde el formulario. / Please try again from the form.": "Please try again from the form.",
        "Volver / Back to ETERNA": "Back to ETERNA",
    }
    for old, new in final_replacements.items():
        html = html.replace(old, new)

    # Blindaje de botones de idioma y hidden real.
    html = html.replace('name="language" id="language" value="es"', 'name="language" id="language" value="en"')
    html = html.replace('href="/crear?lang=es" role="button" class="language-option " data-lang="en"', 'href="/crear?lang=es" role="button" class="language-option " data-lang="es"')
    html = html.replace('href="/crear?lang=es" role="button" class="language-option active" data-lang="en"', 'href="/crear?lang=es" role="button" class="language-option active" data-lang="es"')
    html = html.replace('data-lang="es">🇬🇧 English', 'data-lang="en">🇬🇧 English')
    return html

def render_create_form(initial_language: str = "es") -> str:
    lang = "en" if str(initial_language or "").lower().strip() == "en" else "es"
    return _eterna_rc113_final_form_lock(_ORIGINAL_RENDER_CREATE_FORM_RC113(lang), lang)

# =========================================================
# RC114 — ACTIVE OVERRIDE: REAL I18N + NATIVE PHOTOS SAFE
# This final render_create_form intentionally overrides the older RC112/RC113
# patched versions above. It does not use html.replace for translation.
# =========================================================

def render_create_form(initial_language: str = "es") -> str:
    from string import Template

    lang = "en" if str(initial_language or "").lower().strip() == "en" else "es"

    TEXTS = {
        "es": {
            "html_lang":"es", "meta_title":"Crear ETERNA", "subtitle":"Crea algo que no se abra. Se viva.",
            "intro1":"No todo lo importante", "intro2":"debería desaparecer.", "intro3":"Haz que vuelva convertido", "intro4":"en emoción real.",
            "lang_es":"🇪🇸 Español", "lang_en":"🇬🇧 English",
            "creator_title":"QUIÉN LO CREA", "customer_name":"Tu nombre", "customer_email":"Tu email", "customer_phone":"Tu teléfono",
            "recipient_title":"QUIÉN LO RECIBE", "recipient_name":"Nombre de la persona que lo recibe", "recipient_phone":"Teléfono de quien lo recibe", "recipient_email":"Email opcional del destinatario",
            "photos_title":"Selecciona 6 recuerdos", "photos_copy":"Elige 6 fotos directamente desde tu galería. Se cargan de forma nativa para que el proceso sea rápido.", "open_gallery":"Abrir galería", "change_photo":"Cambiar foto", "photo":"Foto",
            "photo_required":"Necesaria para crear tu ETERNA.", "photo_optional":"Opcional si ya tienes 4 fotos.", "photo_ready":"Foto lista ✓", "photo_uploaded":"Foto subida ✓", "photo_uploading":"Subiendo foto...",
            "photos_hint_initial":"Necesitas al menos las primeras 4 fotos. Si tienes 4, ETERNA completará las 6.", "photos_hint_partial":"{count} fotos listas. Te faltan {missing} para continuar.", "photos_hint_ready4":"{count} fotos listas. Puedes continuar; ETERNA completará las 6 si falta alguna.", "photos_hint_ready6":"6 fotos listas. Puedes cambiar cualquiera tocando su casilla.",
            "occasion_title":"QUÉ MOMENTO ES", "occasion_date":"Fecha importante opcional", "emotion_title":"QUÉ QUIERES PROVOCAR", "words_title":"TUS PALABRAS", "phrase_auto":"Quiero que ETERNA encuentre las palabras", "phrase_manual":"Quiero escribir lo que siento",
            "phrase_1":"Lo que nunca quieres que olvide", "phrase_2":"Eso que sientes y a veces no dices", "phrase_3":"La frase que quieres dejarle para siempre", "suggestions_title":"¿Necesitas inspiración?", "suggestions_button":"Ver frases sugeridas",
            "yul_title":"YUL — detalle opcional", "yul_place":"Un lugar que recuerdes con esa persona", "yul_detail":"Un pequeño detalle que solo vosotros entendáis", "yul_tone":"Tono emocional que quieres provocar", "yul_hint":"Algo que ETERNA debería tener en cuenta",
            "delivery_title":"EL MOMENTO EXACTO", "delivery_copy":"Puedes dejar que llegue en cuanto esté lista... o programar ese momento íntimo en el que sabes que podrá vivirla de verdad.", "delivery_instant":"Enviarlo en cuanto esté listo", "delivery_instant_sub":"Sin coste extra.", "delivery_scheduled":"Guardarlo y entregarlo en un momento exacto", "delivery_scheduled_sub":"+{fee} para guardarlo y hacer que llegue exactamente cuando tú elijas.", "delivery_date":"Fecha de entrega", "delivery_time":"Hora de entrega", "delivery_hint":"Lo ideal es que pueda vivirlo con calma. Con unos cascos. En silencio. Sin que nadie le moleste.",
            "gift_title":"DINERO A REGALAR", "gift_placeholder":"Dinero a regalar (€)", "price_base":"Precio base ETERNA", "gift_fee":"Si añades regalo económico: gestión segura del importe regalado.", "scheduled_fee":"Entrega programada: solo si eliges guardarlo y entregarlo en un momento exacto.",
            "trust_title":"Privado y seguro", "trust_1":"Tus fotos son privadas.", "trust_2":"El pago se realiza de forma segura con Stripe.", "trust_3":"La reacción solo vuelve a quien crea esta ETERNA.", "trust_4":"Si añades dinero, lo recibirá la persona destinataria.", "trust_5":"Soporte:",
            "responsible":"Acepto crear esta ETERNA de forma responsable. Entiendo que, si la persona destinataria vive la experiencia, podré recibir un recuerdo privado de ese momento. Me comprometo a tratar ese contenido con respeto, a no utilizarlo de forma ofensiva, invasiva o pública, y a compartirlo solo de manera responsable.",
            "legal_before":"Al continuar, aceptas las", "terms":"condiciones", "legal_middle":"y la", "privacy":"política de privacidad", "submit_disabled":"Completa los datos y sube 4 fotos", "submit_ready":"Crear y continuar al pago seguro", "opening_checkout":"Abriendo pago seguro ETERNA...",
            "error_main":"Revisa los datos principales antes de continuar.", "error_photos":"Sube al menos las primeras 4 fotos para continuar.", "error_emotion":"Elige una emoción para continuar.", "error_manual":"Escribe tus 3 frases.", "error_responsible":"Debes aceptar el uso responsable de ETERNA.", "error_delivery":"Elige una fecha y hora de entrega válidas.", "error_amount":"El importe no es válido.", "error_generic":"Algo no ha ido bien. Revisa el formulario."
        },
        "en": {
            "html_lang":"en", "meta_title":"Create ETERNA", "subtitle":"Create something that isn't opened. It's lived.",
            "intro1":"Not everything important", "intro2":"should disappear.", "intro3":"Make it return as", "intro4":"real emotion.",
            "lang_es":"🇪🇸 Español", "lang_en":"🇬🇧 English",
            "creator_title":"WHO IS CREATING THIS?", "customer_name":"Your name", "customer_email":"Your email", "customer_phone":"Your phone",
            "recipient_title":"WHO RECEIVES IT?", "recipient_name":"Recipient's name", "recipient_phone":"Recipient's phone", "recipient_email":"Recipient email (optional)",
            "photos_title":"Select 6 memories", "photos_copy":"Choose 6 photos directly from your gallery. They load natively so the process stays fast.", "open_gallery":"Open gallery", "change_photo":"Change photo", "photo":"Photo",
            "photo_required":"Required to create your ETERNA.", "photo_optional":"Optional if you already have 4 photos.", "photo_ready":"Photo ready ✓", "photo_uploaded":"Photo uploaded ✓", "photo_uploading":"Uploading photo...",
            "photos_hint_initial":"You need at least the first 4 photos. If you have 4, ETERNA will complete the 6.", "photos_hint_partial":"{count} photos ready. You still need {missing} to continue.", "photos_hint_ready4":"{count} photos ready. You can continue; ETERNA will complete the 6 if needed.", "photos_hint_ready6":"6 photos ready. You can change any of them by tapping its box.",
            "occasion_title":"WHAT MOMENT IS IT?", "occasion_date":"Optional important date", "emotion_title":"WHAT DO YOU WANT TO MAKE THEM FEEL?", "words_title":"YOUR WORDS", "phrase_auto":"I want ETERNA to find the words", "phrase_manual":"I want to write what I feel",
            "phrase_1":"What you never want them to forget", "phrase_2":"What you feel and sometimes do not say", "phrase_3":"The sentence you want to leave them forever", "suggestions_title":"Need inspiration?", "suggestions_button":"See suggested phrases",
            "yul_title":"YUL — optional detail", "yul_place":"A place you remember with this person", "yul_detail":"A small detail only you both understand", "yul_tone":"The emotional tone you want", "yul_hint":"Something ETERNA should keep in mind",
            "delivery_title":"THE EXACT MOMENT", "delivery_copy":"You can let it arrive as soon as it is ready... or schedule the intimate moment when you know they can truly live it.", "delivery_instant":"Send it as soon as it is ready", "delivery_instant_sub":"No extra cost.", "delivery_scheduled":"Save it and deliver it at an exact moment", "delivery_scheduled_sub":"+{fee} to save it and make it arrive exactly when you choose.", "delivery_date":"Delivery date", "delivery_time":"Delivery time", "delivery_hint":"Ideally, they should be able to live it calmly. With headphones. In silence. Without being disturbed.",
            "gift_title":"GIFT AMOUNT", "gift_placeholder":"Gift amount (€)", "price_base":"Base ETERNA price", "gift_fee":"If you add a money gift: secure handling of the gifted amount.", "scheduled_fee":"Scheduled delivery: only if you choose to save it and deliver it at an exact moment.",
            "trust_title":"Private and secure", "trust_1":"Your photos are private.", "trust_2":"Payment is processed securely with Stripe.", "trust_3":"The reaction only returns to the person who creates this ETERNA.", "trust_4":"If you add money, the recipient will receive it.", "trust_5":"Support:",
            "responsible":"I accept creating this ETERNA responsibly. I understand that, if the recipient lives the experience, I may receive a private memory of that moment. I commit to treating that content with respect, not using it in an offensive, invasive or public way, and sharing it only responsibly.",
            "legal_before":"By continuing, you accept the", "terms":"terms", "legal_middle":"and the", "privacy":"privacy policy", "submit_disabled":"Complete the details and upload 4 photos", "submit_ready":"Create and continue to secure payment", "opening_checkout":"Opening secure ETERNA checkout...",
            "error_main":"Please review the main details before continuing.", "error_photos":"Upload at least the first 4 photos to continue.", "error_emotion":"Select an emotion to continue.", "error_manual":"Write your 3 messages.", "error_responsible":"Before continuing, you must accept ETERNA's responsible use.", "error_delivery":"Choose a valid delivery date and time.", "error_amount":"The amount is not valid.", "error_generic":"Something went wrong. Please review the form."
        }
    }
    OCCASIONS = {
        "es":[("pareja","❤️ Pareja","Amor, aniversario o algo que no sabes decir."),("madre","👩 Mamá","Para agradecer todo lo que siempre estuvo."),("padre","👨 Papá","Para reconocer lo que a veces no se dice."),("cumpleanos","🎂 Cumpleaños","Una sorpresa que se vive de verdad."),("amistad","🤝 Amistad","Para alguien que siempre estuvo cerca."),("distancia","🌍 A distancia","Cuando está lejos, pero sigue aquí."),("otro","✨ Otro momento","Cuando simplemente quieres emocionar.")],
        "en":[("pareja","❤️ Partner","Love, anniversary or something you do not know how to say."),("madre","👩 Mother","To thank everything that was always there."),("padre","👨 Father","To recognize what is not always said."),("cumpleanos","🎂 Birthday","A surprise that is truly experienced."),("amistad","🤝 Friendship","For someone who was always close."),("distancia","🌍 Long distance","When they are far away, but still here."),("otro","✨ Another moment","When you simply want to move someone.")]
    }
    EMOTIONS = {
        "es":[("cumpleanos","Cumpleaños","Un día que merece quedarse."),("amor","Amor","Cuando lo que sientes ya no cabe dentro."),("mama","Mamá","Para quien siempre fue hogar."),("papa","Papá","Para quien dejó huella sin hacer ruido."),("familia","Familia","Para quienes siempre vuelven a ti."),("amistad","Amistad","Para esa persona que se quedó."),("distancia","Distancia","Cuando alguien está lejos, pero sigue cerca."),("perdon","Perdón","Para decir algo que cuesta decir."),("reencuentro","Reencuentro","Cuando algo vuelve después del tiempo."),("gracias","Gracias","Para agradecer de verdad."),("superacion","Superación","Para recordarle todo lo que vale."),("sorpresa","Sorpresa","Cuando quieres tocar el corazón sin avisar."),("esfuerzo","Esfuerzo","Para reconocer todo lo que ha dado."),("no_se","No sé cómo decirlo","Cuando ETERNA debe decirlo por ti.")],
        "en":[("cumpleanos","Birthday","A day worth keeping."),("amor","Love","When what you feel no longer fits inside."),("mama","Mom","For the one who was always home."),("papa","Dad","For the one who left a mark quietly."),("familia","Family","For those who always come back to you."),("amistad","Friendship","For the person who stayed."),("distancia","Distance","When someone is far away, but still close."),("perdon","Forgiveness","To say something hard to say."),("reencuentro","Reunion","When something returns after time."),("gracias","Thank you","To truly say thank you."),("superacion","Overcoming","To remind them how much they are worth."),("sorpresa","Surprise","When you want to touch their heart without warning."),("esfuerzo","Effort","To recognize everything they have given."),("no_se","I do not know how to say it","When ETERNA should say it for you.")]
    }
    SUGGESTIONS = {"es":["Gracias por estar siempre.","Hay personas que se quedan para siempre.","Hoy quería recordarte algo bonito.","Aunque estemos lejos, sigues aquí.","Nunca olvides lo importante que eres para mí."],"en":["Thank you for always being there.","Some people stay forever.","Today I wanted to remind you of something beautiful.","Even if we are far apart, you are still here.","Never forget how important you are to me."]}
    T = TEXTS[lang]
    def esc(v):
        return html.escape(str(v or ""), quote=True)
    country_options = "".join([f'<option value="{esc(c)}"{" selected" if c=="+34" else ""}>{esc(c)}</option>' for c in KNOWN_COUNTRY_CODES])
    occasion_cards = "".join([f'<label class="choice-card"><input type="radio" name="occasion_type" value="{esc(v)}"><span class="choice-title">{esc(t)}</span><span class="choice-sub">{esc(d)}</span></label>' for v,t,d in OCCASIONS[lang]])
    emotion_cards = "".join([f'<label class="emotion-card"><input type="radio" name="message_type" value="{esc(v)}"><span class="emotion-title">{esc(t)}</span><span class="emotion-sub">{esc(d)}</span></label>' for v,t,d in EMOTIONS[lang]])
    suggestions = "".join([f'<button type="button" class="suggestion-chip" data-text="{esc(s)}">{esc(s)}</button>' for s in SUGGESTIONS[lang]])
    photo_slots = "".join([f'<label class="photo-box" for="photo{i}"><input id="photo{i}" name="photo{i}" type="file" accept="image/*" class="photo-input"><span class="photo-label">{esc(T["photo"])} {i}</span><span class="photo-preview" id="preview_photo{i}">{esc(T["change_photo"])}</span><span class="photo-status" id="status_photo{i}">{esc(T["photo_required"] if i<=4 else T["photo_optional"])}</span></label>' for i in range(1,7)])
    js_texts = json.dumps({k:T[k] for k in ["photo_ready","photo_uploaded","photo_uploading","photos_hint_initial","photos_hint_partial","photos_hint_ready4","photos_hint_ready6","submit_disabled","submit_ready","opening_checkout","error_main","error_photos","error_emotion","error_manual","error_responsible","error_delivery","error_amount","error_generic"]}, ensure_ascii=False)
    return Template(r'''
<!DOCTYPE html><html lang="$html_lang"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"><title>$meta_title</title><meta name="theme-color" content="#02050a"><style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}html,body{margin:0;min-height:100%;background:#02050a;color:#fff7e6;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}body{padding:18px;overflow-x:hidden;background:radial-gradient(circle at 50% -10%,rgba(245,210,139,.24),transparent 30%),linear-gradient(180deg,#020817,#000 52%,#020817)}.wrap{width:100%;max-width:920px;margin:0 auto}.card{border:1px solid rgba(245,210,139,.22);border-radius:30px;background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,.035));box-shadow:0 28px 100px rgba(0,0,0,.58);padding:24px}.brand{text-align:center;letter-spacing:.42em;color:#f5d28b;font-weight:900;font-size:13px;margin:8px 0 10px}h1{margin:0;text-align:center;font-size:clamp(38px,10vw,68px);letter-spacing:.12em;color:#f7dfaa}.subtitle{text-align:center;color:rgba(255,255,255,.72);margin:12px auto 20px;line-height:1.5}.language-switch{display:flex;justify-content:center;gap:10px;margin:14px 0 24px}.language-option{border:1px solid rgba(245,210,139,.25);border-radius:999px;padding:10px 14px;text-decoration:none;color:rgba(255,255,255,.68);font-weight:800;background:rgba(255,255,255,.04)}.language-option.active{color:#0b1018;background:#f5d28b}.intro{text-align:center;margin:8px auto 28px;max-width:620px}.intro p{margin:0;color:rgba(255,255,255,.88);font-size:19px;line-height:1.65}.section{margin:22px 0;padding:20px;border:1px solid rgba(255,255,255,.09);border-radius:24px;background:rgba(0,0,0,.20)}.section-title{font-size:13px;letter-spacing:.18em;color:#f5d28b;font-weight:900;margin-bottom:14px;text-transform:uppercase}.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.phone-row{display:grid;grid-template-columns:112px 1fr;gap:10px}input,select,textarea{width:100%;border:1px solid rgba(255,255,255,.14);border-radius:16px;background:rgba(255,255,255,.07);color:#fff;padding:15px;font-size:16px;outline:none}textarea{min-height:92px;resize:vertical}input::placeholder,textarea::placeholder{color:rgba(255,255,255,.42)}select option{background:#111;color:#fff}.soft-copy,.hint,.legal,.trust li{color:rgba(255,255,255,.70);line-height:1.55}.choice-grid,.emotion-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.choice-card,.emotion-card{display:block;border:1px solid rgba(255,255,255,.12);border-radius:18px;background:rgba(255,255,255,.05);padding:14px;cursor:pointer}.choice-card input,.emotion-card input{width:auto;margin-right:8px}.choice-title,.emotion-title{display:block;font-weight:900;color:#fff;margin-bottom:6px}.choice-sub,.emotion-sub{display:block;color:rgba(255,255,255,.60);font-size:13px;line-height:1.4}.photo-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:14px}.gallery-button{display:inline-flex;align-items:center;justify-content:center;border:0;border-radius:999px;background:#f5d28b;color:#08111d;padding:14px 18px;font-weight:900;cursor:pointer}.photo-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:16px}.photo-box{position:relative;min-height:178px;border:1px solid rgba(245,210,139,.18);border-radius:22px;background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,.035));padding:11px;display:flex;flex-direction:column;gap:8px;justify-content:space-between;overflow:hidden;cursor:pointer;box-shadow:inset 0 0 0 1px rgba(255,255,255,.035),0 14px 32px rgba(0,0,0,.22)}.photo-box.ready{border-color:rgba(245,210,139,.62);background:linear-gradient(180deg,rgba(245,210,139,.105),rgba(255,255,255,.035));box-shadow:0 0 0 1px rgba(245,210,139,.16),0 18px 42px rgba(0,0,0,.30),0 0 26px rgba(245,210,139,.10)}.photo-input{position:absolute;inset:0;opacity:0;cursor:pointer}.photo-label{font-weight:950;color:#f5d28b;z-index:2;font-size:12px;letter-spacing:.12em;text-transform:uppercase;text-shadow:0 1px 12px rgba(0,0,0,.55)}.photo-preview{flex:1;min-height:104px;border-radius:16px;background:radial-gradient(circle at 50% 30%,rgba(245,210,139,.10),rgba(0,0,0,.30));display:flex;align-items:center;justify-content:center;text-align:center;color:rgba(255,255,255,.54);font-size:12px;line-height:1.25;background-size:cover;background-position:center;z-index:1;box-shadow:inset 0 0 0 1px rgba(255,255,255,.06);overflow:hidden}.photo-preview.has-image{color:transparent;box-shadow:inset 0 0 0 1px rgba(245,210,139,.20),inset 0 -42px 58px rgba(0,0,0,.24)}.photo-status{font-size:11.5px;color:rgba(255,255,255,.58);z-index:2;line-height:1.25;min-height:28px}.photo-status.ready{color:#89ffc9}.photo-status.loading{color:#f5d28b}.error{display:none;border:1px solid rgba(255,80,80,.35);background:rgba(255,80,80,.12);color:#ffd6d6;border-radius:16px;padding:14px;margin:16px 0;line-height:1.45}.error.show{display:block}.radio-row{display:flex;gap:10px;align-items:flex-start;margin:10px 0;color:rgba(255,255,255,.82)}.radio-row input{width:auto;margin-top:3px}.hidden{display:none!important}.suggestions{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}.suggestion-chip{border:1px solid rgba(245,210,139,.25);border-radius:999px;background:rgba(245,210,139,.08);color:#f7dfaa;padding:9px 12px;cursor:pointer}.price-line{display:flex;justify-content:space-between;gap:16px;border-bottom:1px solid rgba(255,255,255,.08);padding:10px 0;color:rgba(255,255,255,.75)}.trust ul{padding-left:18px;margin:10px 0}.responsible{display:flex;gap:10px;align-items:flex-start;margin-top:16px;color:rgba(255,255,255,.76);line-height:1.5}.responsible input{width:auto;margin-top:3px}.submit{width:100%;border:0;border-radius:20px;min-height:62px;background:linear-gradient(135deg,#fff0b9,#d49c37);color:#08111d;font-size:17px;font-weight:950;cursor:pointer;margin-top:18px}.submit:disabled{opacity:.45;cursor:not-allowed;filter:grayscale(.6)}a{color:#f7dfaa}@media(max-width:720px){body{padding:14px}.card{padding:18px;border-radius:24px}.grid,.choice-grid,.emotion-grid{grid-template-columns:1fr}.photo-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.photo-box{min-height:168px;border-radius:20px;padding:10px}.photo-preview{min-height:96px;border-radius:15px}.phone-row{grid-template-columns:96px 1fr}.section{padding:16px}}
</style></head><body><div class="wrap"><main class="card"><div class="brand">ETERNA</div><h1>ETERNA</h1><p class="subtitle">$subtitle</p><nav class="language-switch"><a href="/crear?lang=es" class="language-option $es_active" data-lang="es">$lang_es</a><a href="/crear?lang=en" class="language-option $en_active" data-lang="en">$lang_en</a></nav><div class="intro"><p>$intro1</p><p>$intro2</p><p>$intro3</p><p>$intro4</p></div><form id="createForm" action="/crear" method="post" enctype="multipart/form-data" novalidate><input type="hidden" name="language" id="language" value="$lang"><input type="hidden" name="photo_upload_session" id="photo_upload_session" value=""><div id="formError" class="error"></div>
<section class="section"><div class="section-title">$creator_title</div><div class="grid"><input name="customer_name" id="customer_name" placeholder="$customer_name" required><input name="customer_email" id="customer_email" type="email" placeholder="$customer_email" required></div><div class="phone-row" style="margin-top:12px"><select name="customer_country_code">$country_options</select><input name="customer_phone" id="customer_phone" inputmode="tel" placeholder="$customer_phone" required></div></section>
<section class="section"><div class="section-title">$recipient_title</div><input name="recipient_name" id="recipient_name" placeholder="$recipient_name" required><div class="phone-row" style="margin-top:12px"><select name="recipient_country_code">$country_options</select><input name="recipient_phone" id="recipient_phone" inputmode="tel" placeholder="$recipient_phone" required></div><input style="margin-top:12px" name="recipient_email" id="recipient_email" type="email" placeholder="$recipient_email"></section>
<section class="section"><div class="section-title">$photos_title</div><div class="soft-copy">$photos_copy</div><div class="photo-actions"><label class="gallery-button" for="allPhotosInput">$open_gallery</label><input id="allPhotosInput" type="file" accept="image/*" multiple style="display:none"><span class="hint" id="photoHint">$photos_hint_initial</span></div><div class="photo-grid">$photo_slots</div></section>
<section class="section"><div class="section-title">$occasion_title</div><div class="choice-grid">$occasion_cards</div><input style="margin-top:12px" type="date" name="occasion_date" aria-label="$occasion_date"></section><section class="section"><div class="section-title">$emotion_title</div><div class="emotion-grid">$emotion_cards</div></section>
<section class="section"><div class="section-title">$words_title</div><label class="radio-row"><input type="radio" name="phrase_mode" value="auto" checked> <span>$phrase_auto</span></label><label class="radio-row"><input type="radio" name="phrase_mode" value="manual"> <span>$phrase_manual</span></label><div id="manualPhrases" class="hidden"><textarea name="phrase_1" id="phrase_1" maxlength="220" placeholder="$phrase_1"></textarea><textarea name="phrase_2" id="phrase_2" maxlength="220" placeholder="$phrase_2"></textarea><textarea name="phrase_3" id="phrase_3" maxlength="220" placeholder="$phrase_3"></textarea><div class="section-title" style="margin-top:12px">$suggestions_title</div><button type="button" class="gallery-button" id="suggestionsToggle">$suggestions_button</button><div class="suggestions hidden" id="suggestionsBox">$suggestions</div></div></section>
<section class="section"><div class="section-title">$yul_title</div><div class="grid"><input name="yul_memory_place" placeholder="$yul_place"><input name="yul_memory_detail" placeholder="$yul_detail"><input name="yul_emotion_tone" placeholder="$yul_tone"><input name="yul_magic_hint" placeholder="$yul_hint"></div></section>
<section class="section"><div class="section-title">$delivery_title</div><div class="soft-copy">$delivery_copy</div><label class="radio-row"><input type="radio" name="delivery_mode" value="instant" checked> <span><strong>$delivery_instant</strong><br><small>$delivery_instant_sub</small></span></label><label class="radio-row"><input type="radio" name="delivery_mode" value="scheduled"> <span><strong>$delivery_scheduled</strong><br><small>$delivery_scheduled_sub</small></span></label><div id="scheduledFields" class="grid hidden"><input type="date" name="delivery_date" id="delivery_date" aria-label="$delivery_date"><input type="time" name="delivery_time" id="delivery_time" aria-label="$delivery_time"></div><div class="hint">$delivery_hint</div></section>
<section class="section"><div class="section-title">$gift_title</div><input name="gift_amount" id="gift_amount" type="number" min="0" step="0.01" value="0" placeholder="$gift_placeholder" required><div class="price-line"><span>$price_base</span><strong>$base_price</strong></div><div class="price-line"><span>$gift_fee</span><strong>5%</strong></div><div class="price-line"><span>$scheduled_fee</span><strong>$scheduled_fee_value</strong></div></section>
<section class="section trust"><div class="section-title">$trust_title</div><ul><li>$trust_1</li><li>$trust_2</li><li>$trust_3</li><li>$trust_4</li><li>$trust_5 $support_email · $support_phone</li></ul><label class="responsible"><input type="checkbox" name="responsible_use_accepted" value="accepted" id="responsible_use_accepted"> <span>$responsible</span></label><p class="legal">$legal_before <a href="/condiciones" target="_blank">$terms</a> $legal_middle <a href="/privacidad" target="_blank">$privacy</a>.</p></section><button class="submit" id="submitBtn" type="submit" disabled>$submit_disabled</button></form></main></div>
<script>(function(){'use strict';const T=$js_texts;const IDS=['photo1','photo2','photo3','photo4','photo5','photo6'];const REQ=['photo1','photo2','photo3','photo4'];const form=document.getElementById('createForm'),btn=document.getElementById('submitBtn'),err=document.getElementById('formError'),multi=document.getElementById('allPhotosInput'),session=document.getElementById('photo_upload_session'),hint=document.getElementById('photoHint');const nativeFiles={},preuploaded={};if(session&&!session.value){session.value='rc114_'+Date.now().toString(36)+'_'+Math.random().toString(36).slice(2,8);}function show(m){if(err){err.textContent=m||T.error_generic;err.classList.add('show');err.scrollIntoView({behavior:'smooth',block:'center'});}}function clear(){if(err){err.textContent='';err.classList.remove('show');}}function ready(id){const i=document.getElementById(id);return !!(nativeFiles[id]||preuploaded[id]||(i&&i.files&&i.files.length));}function miss(){return REQ.filter(id=>!ready(id));}function count(){return IDS.filter(ready).length;}function setFile(input,file){if(!input||!file)return false;nativeFiles[input.id]=file;try{if(typeof DataTransfer==='undefined')throw new Error('no DataTransfer');const dt=new DataTransfer();dt.items.add(file);input.files=dt.files;return !!(input.files&&input.files.length);}catch(e){console.warn('RC114 keeps file in memory',input.id,e);return false;}}function preview(id,file){const box=document.getElementById(id)?.closest('.photo-box'),prev=document.getElementById('preview_'+id),st=document.getElementById('status_'+id);if(box)box.classList.add('ready');if(prev){prev.classList.add('has-image');try{prev.style.backgroundImage='url('+URL.createObjectURL(file)+')';}catch(e){}}if(st){st.textContent=T.photo_ready;st.classList.remove('loading');st.classList.add('ready');}}function status(id,msg,cls){const st=document.getElementById('status_'+id);if(!st)return;st.textContent=msg;st.classList.remove('ready','loading');if(cls)st.classList.add(cls);}function preupload(id,file){if(!file||!session)return;status(id,T.photo_uploading,'loading');const fd=new FormData();fd.append('photo_upload_session',session.value);fd.append('slot',id);fd.append('photo',file,file.name||id+'.jpg');fetch('/preupload-photo',{method:'POST',body:fd}).then(r=>{if(!r.ok)throw new Error(r.status);return r.json();}).then(j=>{if(j&&j.ok){preuploaded[id]=true;status(id,T.photo_uploaded,'ready');}}).catch(e=>{console.warn('RC114 preupload failed, native multipart fallback',id,e);status(id,T.photo_ready,'ready');}).finally(update);}function place(id,file){const input=document.getElementById(id);if(!input||!file)return;setFile(input,file);preview(id,file);preupload(id,file);update();}function update(){const c=count(),m=miss();if(hint){if(c>=6)hint.textContent=T.photos_hint_ready6;else if(!m.length)hint.textContent=T.photos_hint_ready4.replace('{count}',String(c));else if(c>0)hint.textContent=T.photos_hint_partial.replace('{count}',String(c)).replace('{missing}',String(m.length));else hint.textContent=T.photos_hint_initial;}const ok=basic(false)&&!m.length;if(btn){btn.disabled=!ok;btn.textContent=ok?T.submit_ready:T.submit_disabled;}}function basic(showErr){for(const id of ['customer_name','customer_email','customer_phone','recipient_name','recipient_phone']){const el=document.getElementById(id);if(!el||!String(el.value||'').trim()){if(showErr)show(T.error_main);return false;}}if(!document.querySelector('input[name="message_type"]:checked')){if(showErr)show(T.error_emotion);return false;}const manual=document.querySelector('input[name="phrase_mode"][value="manual"]');if(manual&&manual.checked){for(const id of ['phrase_1','phrase_2','phrase_3']){const el=document.getElementById(id);if(!el||!String(el.value||'').trim()){if(showErr)show(T.error_manual);return false;}}}const scheduled=document.querySelector('input[name="delivery_mode"][value="scheduled"]');if(scheduled&&scheduled.checked){const d=document.getElementById('delivery_date')?.value||'',tm=document.getElementById('delivery_time')?.value||'';const dt=new Date(d+'T'+tm);if(!d||!tm||isNaN(dt.getTime())||dt.getTime()<=Date.now()){if(showErr)show(T.error_delivery);return false;}}const amount=parseFloat(document.getElementById('gift_amount')?.value||'0');if(Number.isNaN(amount)||amount<0){if(showErr)show(T.error_amount);return false;}if(!document.getElementById('responsible_use_accepted')?.checked){if(showErr)show(T.error_responsible);return false;}return true;}if(multi){multi.addEventListener('change',()=>{clear();Array.from(multi.files||[]).slice(0,6).forEach((f,idx)=>place(IDS[idx],f));multi.value='';update();});}IDS.forEach(id=>{const input=document.getElementById(id);if(input)input.addEventListener('change',()=>{const f=input.files&&input.files[0];if(f){nativeFiles[id]=f;preview(id,f);preupload(id,f);}update();});});document.querySelectorAll('input,textarea,select').forEach(el=>{el.addEventListener('input',update);el.addEventListener('change',update);});document.querySelectorAll('input[name="phrase_mode"]').forEach(el=>el.addEventListener('change',()=>{document.getElementById('manualPhrases')?.classList.toggle('hidden',!(el.value==='manual'&&el.checked));update();}));document.querySelectorAll('input[name="delivery_mode"]').forEach(el=>el.addEventListener('change',()=>{document.getElementById('scheduledFields')?.classList.toggle('hidden',!document.querySelector('input[name="delivery_mode"][value="scheduled"]')?.checked);update();}));document.getElementById('suggestionsToggle')?.addEventListener('click',()=>document.getElementById('suggestionsBox')?.classList.toggle('hidden'));document.querySelectorAll('.suggestion-chip').forEach(b=>b.addEventListener('click',()=>{const t=['phrase_1','phrase_2','phrase_3'].map(id=>document.getElementById(id)).find(el=>el&&!String(el.value||'').trim());if(t){t.value=b.getAttribute('data-text')||b.textContent||'';t.dispatchEvent(new Event('input',{bubbles:true}));}}));if(form)form.addEventListener('submit',e=>{clear();if(!basic(true)){e.preventDefault();return false;}if(miss().length){e.preventDefault();show(T.error_photos);return false;}btn.disabled=true;btn.textContent=T.opening_checkout;return true;});update();})();</script></body></html>
''').safe_substitute(
        html_lang=esc(T["html_lang"]), meta_title=esc(T["meta_title"]), subtitle=esc(T["subtitle"]), es_active="active" if lang=="es" else "", en_active="active" if lang=="en" else "", lang_es=esc(T["lang_es"]), lang_en=esc(T["lang_en"]), intro1=esc(T["intro1"]), intro2=esc(T["intro2"]), intro3=esc(T["intro3"]), intro4=esc(T["intro4"]), lang=esc(lang), creator_title=esc(T["creator_title"]), customer_name=esc(T["customer_name"]), customer_email=esc(T["customer_email"]), customer_phone=esc(T["customer_phone"]), recipient_title=esc(T["recipient_title"]), recipient_name=esc(T["recipient_name"]), recipient_phone=esc(T["recipient_phone"]), recipient_email=esc(T["recipient_email"]), country_options=country_options, photos_title=esc(T["photos_title"]), photos_copy=esc(T["photos_copy"]), open_gallery=esc(T["open_gallery"]), photos_hint_initial=esc(T["photos_hint_initial"]), photo_slots=photo_slots, occasion_title=esc(T["occasion_title"]), occasion_cards=occasion_cards, occasion_date=esc(T["occasion_date"]), emotion_title=esc(T["emotion_title"]), emotion_cards=emotion_cards, words_title=esc(T["words_title"]), phrase_auto=esc(T["phrase_auto"]), phrase_manual=esc(T["phrase_manual"]), phrase_1=esc(T["phrase_1"]), phrase_2=esc(T["phrase_2"]), phrase_3=esc(T["phrase_3"]), suggestions_title=esc(T["suggestions_title"]), suggestions_button=esc(T["suggestions_button"]), suggestions=suggestions, yul_title=esc(T["yul_title"]), yul_place=esc(T["yul_place"]), yul_detail=esc(T["yul_detail"]), yul_tone=esc(T["yul_tone"]), yul_hint=esc(T["yul_hint"]), delivery_title=esc(T["delivery_title"]), delivery_copy=esc(T["delivery_copy"]), delivery_instant=esc(T["delivery_instant"]), delivery_instant_sub=esc(T["delivery_instant_sub"]), delivery_scheduled=esc(T["delivery_scheduled"]), delivery_scheduled_sub=esc(T["delivery_scheduled_sub"].format(fee=money(SCHEDULED_DELIVERY_FEE))), delivery_date=esc(T["delivery_date"]), delivery_time=esc(T["delivery_time"]), delivery_hint=esc(T["delivery_hint"]), gift_title=esc(T["gift_title"]), gift_placeholder=esc(T["gift_placeholder"]), price_base=esc(T["price_base"]), gift_fee=esc(T["gift_fee"]), scheduled_fee=esc(T["scheduled_fee"]), base_price=esc(money(BASE_PRICE)), scheduled_fee_value=esc(money(SCHEDULED_DELIVERY_FEE)), trust_title=esc(T["trust_title"]), trust_1=esc(T["trust_1"]), trust_2=esc(T["trust_2"]), trust_3=esc(T["trust_3"]), trust_4=esc(T["trust_4"]), trust_5=esc(T["trust_5"]), support_email=esc(ETERNA_SUPPORT_EMAIL), support_phone=esc(ETERNA_SUPPORT_PHONE), responsible=esc(T["responsible"]), legal_before=esc(T["legal_before"]), terms=esc(T["terms"]), legal_middle=esc(T["legal_middle"]), privacy=esc(T["privacy"]), submit_disabled=esc(T["submit_disabled"]), js_texts=js_texts)
