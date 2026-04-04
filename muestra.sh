#!/usr/bin/env python3
"""Script de demostración para el video del laboratorio.

Uso:
  python3 muestra.sh users
  python3 muestra.sh juegos
  python3 muestra.sh wikidata
  python3 muestra.sh calidad
  python3 muestra.sh all

Opcional:
  API_BASE=http://localhost:5000 python3 muestra.sh users
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import unicodedata
from datetime import datetime
from typing import Any
from urllib.parse import urlencode
from uuid import uuid4

API_BASE = os.environ.get("API_BASE", "http://localhost:5000").rstrip("/")


def _print_title(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def _print_cmd(cmd: list[str]) -> None:
    print("$ " + " ".join(shlex.quote(x) for x in cmd))


def _print_step(title: str) -> None:
    print(f"\n--- {title} ---")


def _run_cmd(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    _print_cmd(cmd)
    print()
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip())
    if result.returncode != 0:
        raise RuntimeError(f"Comando falló con código {result.returncode}")
    return result


def _run_curl(
    method: str,
    path: str,
    *,
    headers: dict[str, str] | None = None,
    json_body: dict[str, Any] | None = None,
) -> tuple[int, Any, str]:
    url = f"{API_BASE}{path}"
    cmd = [
        "curl",
        "-sS",
        "-X",
        method,
        url,
        "-w",
        "\n__HTTP_STATUS__:%{http_code}\n",
    ]
    for k, v in (headers or {}).items():
        cmd.extend(["-H", f"{k}: {v}"])
    if json_body is not None:
        cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps(json_body, ensure_ascii=False)])

    _print_cmd(cmd)
    print()
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        if result.stderr:
            print(result.stderr.rstrip())
        raise RuntimeError(f"curl falló con código {result.returncode}")

    text = result.stdout
    marker = "__HTTP_STATUS__:"
    if marker not in text:
        print(text.rstrip())
        raise RuntimeError("No se pudo parsear el código HTTP de la respuesta")

    body, status_part = text.rsplit(marker, 1)
    body = body.rstrip("\n")
    status = int(status_part.strip())

    parsed: Any = body
    if body:
        try:
            parsed = json.loads(body)
            print(json.dumps(parsed, ensure_ascii=False, indent=2))
        except json.JSONDecodeError:
            print(body)
    else:
        print("<sin body>")

    print(f"HTTP {status}")
    return status, parsed, body


def _normalize(text: str) -> str:
    base = unicodedata.normalize("NFKD", text)
    no_marks = "".join(ch for ch in base if not unicodedata.combining(ch))
    return no_marks.lower()


def _unique_user(prefix: str) -> tuple[str, str, str]:
    suffix = datetime.now().strftime("%H%M%S") + "_" + uuid4().hex[:6]
    username = f"{prefix}_{suffix}"
    nombre = f"{prefix}_{suffix}"
    password = "1234"
    return username, nombre, password


def _create_and_login(prefix: str) -> tuple[int, str]:
    username, nombre, password = _unique_user(prefix)

    status, reg, _ = _run_curl(
        "POST",
        "/auth/registro",
        json_body={"username": username, "nombre": nombre, "password": password},
    )
    if status != 201 or not isinstance(reg, dict) or "id" not in reg:
        raise RuntimeError("No se pudo registrar usuario para demo")
    usuario_id = int(reg["id"])

    status, log, _ = _run_curl(
        "POST",
        "/auth/login",
        json_body={"username": username, "password": password},
    )
    if status != 200 or not isinstance(log, dict) or "token" not in log:
        raise RuntimeError("No se pudo loguear usuario para demo")

    token = str(log["token"])
    print(f"\nUsuario demo creado: id={usuario_id}, username={username}")
    print(f"Token demo: {token}")
    return usuario_id, token


def section_users() -> None:
    _print_title("1) API de usuarios")

    # Mostrar creación vía /usuarios (representativa)
    _print_step("CREAR USUARIO (POST /usuarios)")
    _run_curl("POST", "/usuarios", json_body={"nombre": "UsuarioSoloCRUD"})

    # Flujo principal con usuario autenticado (necesario para PUT/DELETE)
    _print_step("REGISTRAR + LOGIN (OBTENER ID Y TOKEN)")
    user_id, token = _create_and_login("demo_users")

    _print_step("LISTAR USUARIOS (GET /usuarios)")
    _run_curl("GET", "/usuarios")
    _print_step("OBTENER USUARIO POR ID (GET /usuarios/<id>)")
    _run_curl("GET", f"/usuarios/{user_id}")
    _print_step("ACTUALIZAR USUARIO (PUT /usuarios/<id>)")
    _run_curl(
        "PUT",
        f"/usuarios/{user_id}",
        headers={"Authorization": f"Token {token}"},
        json_body={"nombre": "Usuario Editado Demo"},
    )
    _print_step("ELIMINAR USUARIO (DELETE /usuarios/<id>)")
    _run_curl(
        "DELETE",
        f"/usuarios/{user_id}",
        headers={"Authorization": f"Token {token}"},
    )
    _print_step("VERIFICAR BORRADO (GET /usuarios/<id>)")
    _run_curl("GET", f"/usuarios/{user_id}")


def _buscar_wikidata(q: str) -> list[dict[str, Any]]:
    status, data, _ = _run_curl("GET", f"/juegos?{urlencode({'q': q, 'fuente': 'wikidata'})}")
    if status != 200 or not isinstance(data, list):
        return []
    return [x for x in data if isinstance(x, dict) and x.get("id")]


def section_juegos() -> None:
    _print_title("2) Lista de juegos por usuario")
    _print_step("REGISTRAR + LOGIN (OBTENER ID Y TOKEN)")
    user_id, token = _create_and_login("demo_juegos")
    auth_headers = {"Authorization": f"Token {token}"}

    # Buscar candidatos en Wikidata
    terms = ["zelda", "mario", "metroid", "halo", "assassin"]
    all_games: list[dict[str, Any]] = []
    seen: set[str] = set()

    for term in terms:
        _print_step(f"BUSCAR JUEGOS EN WIKIDATA (q={term})")
        for game in _buscar_wikidata(term):
            gid = str(game.get("id"))
            if gid in seen:
                continue
            seen.add(gid)
            all_games.append(game)
        if len(all_games) >= 8:
            break

    if len(all_games) < 3:
        raise RuntimeError("No se encontraron suficientes juegos para la demo de lista")

    action_games = [g for g in all_games if "accion" in _normalize(str(g.get("genero", "")))]

    selected: list[dict[str, Any]] = []
    selected.extend(action_games[:2])
    for g in all_games:
        if len(selected) >= 3:
            break
        if all(str(x.get("id")) != str(g.get("id")) for x in selected):
            selected.append(g)

    if len(selected) < 3:
        raise RuntimeError("No se pudieron armar 3 juegos distintos para la demo")

    print("\nJuegos elegidos para demo:")
    for g in selected:
        print(f"- {g.get('id')} | {g.get('nombre')} | genero={g.get('genero')}")

    flags = [
        {"tengo": True, "quiero": False, "jugado": False, "me_gusta": False},
        {"tengo": True, "quiero": True, "jugado": False, "me_gusta": False},
        {"tengo": False, "quiero": True, "jugado": False, "me_gusta": False},
    ]

    for game, state in zip(selected, flags, strict=False):
        _print_step(f"AGREGAR JUEGO A LISTA (POST /usuarios/{user_id}/juegos) [{game['id']}]")
        _run_curl(
            "POST",
            f"/usuarios/{user_id}/juegos",
            headers=auth_headers,
            json_body={"juego_id": game["id"], **state},
        )

    _print_step("LISTAR JUEGOS DEL USUARIO")
    _run_curl("GET", f"/usuarios/{user_id}/juegos")

    # Filtrar y ordenar por género (desc)
    genero_objetivo = str(selected[0].get("genero") or "")
    query = urlencode({"genero": genero_objetivo, "ordenar": "nombre", "orden": "desc"})
    _print_step("FILTRAR POR GÉNERO + ORDENAR DESC")
    _run_curl("GET", f"/usuarios/{user_id}/juegos?{query}")

    # Actualizar 1er ítem
    _print_step("ACTUALIZAR ÍTEM DE LISTA")
    _run_curl(
        "PUT",
        f"/usuarios/{user_id}/juegos/{selected[0]['id']}",
        headers=auth_headers,
        json_body={"jugado": True, "me_gusta": True},
    )

    # Eliminar 3er ítem y listar nuevamente
    _print_step("ELIMINAR ÍTEM DE LISTA")
    _run_curl("DELETE", f"/usuarios/{user_id}/juegos/{selected[2]['id']}", headers=auth_headers)
    _print_step("LISTAR NUEVAMENTE (POST-DELETE)")
    _run_curl("GET", f"/usuarios/{user_id}/juegos")


def section_wikidata() -> None:
    _print_title("3) Integración con Wikidata")

    _print_step("BUSCAR EN WIKIDATA (GET /juegos?q=...&fuente=wikidata)")
    juegos = _buscar_wikidata("zelda")
    if not juegos:
        raise RuntimeError("No hubo resultados de Wikidata para la demo")

    juego_id = str(juegos[0]["id"])
    _print_step("OBTENER JUEGO POR ID (GET /juegos/<id>)")
    _run_curl("GET", f"/juegos/{juego_id}")

    _print_step("CREAR USUARIO + LOGIN PARA AGREGAR A LISTA")
    user_id, token = _create_and_login("demo_wikidata")
    _print_step("AGREGAR JUEGO DE WIKIDATA A LISTA DE USUARIO")
    _run_curl(
        "POST",
        f"/usuarios/{user_id}/juegos",
        headers={"Authorization": f"Token {token}"},
        json_body={
            "juego_id": juego_id,
            "tengo": True,
            "quiero": False,
            "jugado": False,
            "me_gusta": False,
        },
    )

    print("\nNota para video: si Wikidata no responde, el endpoint /juegos?q=...&fuente=wikidata devuelve 502.")


def section_calidad() -> None:
    _print_title("4) Pruebas y calidad")
    _print_step("BORRAR :memory:")
    _run_cmd(["rm", "-f", ":memory:"])
    _print_step("LIMPIAR BASE SQLITE")
    _run_cmd(["make", "clean-db"])
    _print_step("EJECUTAR GRADING COMPLETO")
    _run_cmd(["make", "grade"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Demo por secciones para el video")
    parser.add_argument(
        "seccion",
        choices=["users", "juegos", "wikidata", "calidad", "all"],
        help="Qué sección ejecutar",
    )
    args = parser.parse_args()

    try:
        if args.seccion == "users":
            section_users()
        elif args.seccion == "juegos":
            section_juegos()
        elif args.seccion == "wikidata":
            section_wikidata()
        elif args.seccion == "calidad":
            section_calidad()
        else:
            section_users()
            section_juegos()
            section_wikidata()
            section_calidad()
    except RuntimeError as e:
        print(f"\nERROR: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
