"""Autenticación básica: registro, login y validación de token.

Implementa:
- Hash de contraseñas (no se almacenan en texto plano).
- Emisión de token opaco con expiración configurable por entorno.
- Validación de token vigente para operaciones protegidas.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import os
from uuid import uuid4

from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from . import auth_common
from .store import guardar_credenciales, actualizar_token


def _token_ttl_minutes() -> int:
    """TTL de tokens en minutos (default 60).

    Se toma desde AUTH_TOKEN_TTL_MINUTES y se sanea para asegurar un
    entero >= 1. Si el valor es inválido, usa 60.
    """
    raw = os.environ.get("AUTH_TOKEN_TTL_MINUTES", "60")
    try:
        value = int(raw)
    except ValueError:
        return 60
    return max(1, value)


def registrar_usuario_auth():
    """Handler para POST /auth/registro.

    - Crea el usuario correctamente.
    - Guarda la contraseña hasheada en password_hash.
    """
    parsed, error = auth_common.parse_register_body()
    if error is not None:
        return error
    assert parsed is not None
    username = parsed["username"]
    nombre = parsed["nombre"]
    password = parsed["password"]

    dup_error = auth_common.ensure_username_unique(username)
    if dup_error is not None:
        return dup_error

    usuario = auth_common.crear_usuario_basico(nombre)

    password_hash = generate_password_hash(password)
    guardar_credenciales(usuario["id"], username, password_hash)

    return jsonify(usuario), 201


def login():
    """Handler para POST /auth/login.

    - Compara la contraseña contra el hash almacenado.
    - Genera un token aleatorio y lo guarda con una expiración.
    """
    parsed, error = auth_common.parse_login_body()
    if error is not None:
        return error
    assert parsed is not None
    username = parsed["username"]
    password = parsed["password"]

    cred, error = auth_common.get_credenciales_or_401(username)
    if error is not None:
        return error
    assert cred is not None

    if not check_password_hash(cred["password_hash"], password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = uuid4().hex
    expira_en_dt = datetime.now(timezone.utc) + timedelta(minutes=_token_ttl_minutes())
    expira_en = expira_en_dt.isoformat().replace("+00:00", "Z")
    actualizar_token(cred["usuario_id"], token, expira_en)

    return jsonify({"token": token})


def _parse_token_expira_en(raw_value: object) -> datetime | None:
    """Parsea token_expira_en ISO8601 y devuelve datetime con tz, o None."""
    if not isinstance(raw_value, str):
        return None

    value = raw_value.strip()
    if not value:
        return None

    if value.endswith("Z"):
        value = value[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None

    return parsed if parsed.tzinfo is not None else None


def _parse_usuario_id(raw_value: object) -> int | None:
    """Convierte usuario_id a int o devuelve None si no es válido."""
    if raw_value is None:
        return None
    try:
        return int(raw_value)
    except (TypeError, ValueError):
        return None


def obtener_usuario_actual() -> int | None:
    """Devuelve usuario_id asociado al token o None si el token es inválido o expiró.

        - Extrae token del header Authorization.
        - Obtiene datos del token (incluyendo token_expira_en).
        - Si token_expira_en es inválido o expiró, devuelve None.
    """
    token = auth_common.extraer_token_de_header()
    if not token:
        return None
    data = auth_common.obtener_datos_token(token)
    if data is None:
        return None

    token_expira_dt = _parse_token_expira_en(data.get("token_expira_en"))
    if token_expira_dt is None:
        return None

    ahora = datetime.now(timezone.utc)
    if token_expira_dt <= ahora:
        return None

    return _parse_usuario_id(data.get("usuario_id"))

