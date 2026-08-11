from __future__ import annotations

import argparse
import ipaddress
import json
import shutil
import subprocess
import threading
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse, urlsplit

from .media import ProductionError, discover_assets, produce_project
from .project import (
    ProjectStateError,
    begin_project_run,
    create_project,
    latest_project,
    load_project,
    project_path,
    recover_interrupted_projects,
)


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "web" / "index.html"
ACTIVE_JOBS: set[str] = set()
ACTIVE_JOBS_LOCK = threading.Lock()


def is_loopback_name(hostname: str | None) -> bool:
    if not hostname:
        return False
    if hostname.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(hostname).is_loopback
    except ValueError:
        return False


def host_is_allowed(host_header: str | None, port: int) -> bool:
    if not host_header:
        return False
    try:
        parsed = urlsplit(f"//{host_header}")
        return is_loopback_name(parsed.hostname) and parsed.port == port
    except ValueError:
        return False


def origin_is_allowed(origin: str | None, port: int) -> bool:
    if origin is None:
        return True
    try:
        parsed = urlsplit(origin)
        return (
            parsed.scheme == "http"
            and is_loopback_name(parsed.hostname)
            and parsed.port == port
        )
    except ValueError:
        return False


class Handler(BaseHTTPRequestHandler):
    server_version = "YouTubeMusicAuto/1.0"

    def log_message(self, format: str, *args: object) -> None:
        return

    def send_json(self, status: int, payload: dict | list | None) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'")
        self.end_headers()
        self.wfile.write(body)

    def request_is_allowed(self, *, mutation: bool = False) -> bool:
        port = self.server.server_address[1]
        if not host_is_allowed(self.headers.get("Host"), port):
            self.send_json(HTTPStatus.FORBIDDEN, {"error": "허용되지 않은 Host 요청입니다."})
            return False
        if mutation:
            if self.headers.get("Sec-Fetch-Site") == "cross-site":
                self.send_json(HTTPStatus.FORBIDDEN, {"error": "외부 사이트의 요청은 허용되지 않습니다."})
                return False
            if not origin_is_allowed(self.headers.get("Origin"), port):
                self.send_json(HTTPStatus.FORBIDDEN, {"error": "허용되지 않은 Origin 요청입니다."})
                return False
        return True

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > 1_000_000:
            raise ValueError("요청 크기가 올바르지 않습니다.")
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self) -> None:
        if not self.request_is_allowed():
            return
        parsed = urlparse(self.path)
        if parsed.path == "/":
            body = INDEX_PATH.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'")
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path == "/api/health":
            self.send_json(
                HTTPStatus.OK,
                {
                    "python": True,
                    "ffmpeg": shutil.which("ffmpeg") is not None,
                    "ffprobe": shutil.which("ffprobe") is not None,
                    "mode": "manual-assets",
                },
            )
            return
        if parsed.path == "/api/latest":
            self.send_json(HTTPStatus.OK, latest_project())
            return
        if parsed.path.startswith("/api/projects/"):
            project_id = parsed.path.removeprefix("/api/projects/")
            try:
                self.send_json(HTTPStatus.OK, load_project(project_id))
            except (ValueError, FileNotFoundError) as error:
                self.send_json(HTTPStatus.NOT_FOUND, {"error": str(error)})
            return
        self.send_json(HTTPStatus.NOT_FOUND, {"error": "경로를 찾을 수 없습니다."})

    def do_POST(self) -> None:
        if not self.request_is_allowed(mutation=True):
            return
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/api/projects":
                payload = self.read_json()
                manifest = create_project(str(payload.get("theme", "")))
                self.send_json(HTTPStatus.CREATED, manifest)
                return
            if parsed.path.endswith("/continue") and parsed.path.startswith("/api/projects/"):
                project_id = parsed.path.removeprefix("/api/projects/").removesuffix("/continue")
                discover_assets(project_id)
                with ACTIVE_JOBS_LOCK:
                    if project_id in ACTIVE_JOBS:
                        self.send_json(HTTPStatus.CONFLICT, {"error": "이미 제작이 진행 중입니다."})
                        return
                    manifest = begin_project_run(project_id)
                    ACTIVE_JOBS.add(project_id)

                def worker() -> None:
                    try:
                        produce_project(project_id)
                    finally:
                        with ACTIVE_JOBS_LOCK:
                            ACTIVE_JOBS.discard(project_id)

                threading.Thread(target=worker, daemon=True).start()
                self.send_json(HTTPStatus.ACCEPTED, manifest)
                return
            if parsed.path.endswith("/open") and parsed.path.startswith("/api/projects/"):
                project_id = parsed.path.removeprefix("/api/projects/").removesuffix("/open")
                target_name = parse_qs(parsed.query).get("target", ["project"])[0]
                root = project_path(project_id)
                targets = {
                    "project": root,
                    "tracks": root / "work" / "tracks",
                    "image": root / "work" / "image",
                    "output": root / "output",
                }
                target = targets.get(target_name)
                if target is None:
                    raise ValueError("열 수 없는 폴더입니다.")
                subprocess.Popen(["open", str(target)])
                self.send_json(HTTPStatus.OK, {"opened": str(target)})
                return
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "경로를 찾을 수 없습니다."})
        except ProjectStateError as error:
            self.send_json(HTTPStatus.CONFLICT, {"error": str(error)})
        except (ValueError, FileNotFoundError, ProductionError, json.JSONDecodeError) as error:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except Exception as error:
            self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"실행 오류: {error}"})


def main() -> None:
    parser = argparse.ArgumentParser(description="API 없는 YouTube 재즈 영상 제작 프로그램")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    if not is_loopback_name(args.host):
        raise SystemExit("보안을 위해 127.0.0.1 또는 localhost에서만 실행할 수 있습니다.")
    if not INDEX_PATH.exists():
        raise SystemExit("web/index.html 파일을 찾을 수 없습니다.")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("FFmpeg와 FFprobe가 필요합니다.")

    recovered = recover_interrupted_projects()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host}:{args.port}"
    print(f"YouTube Music Auto 실행 중: {url}")
    if recovered:
        print(f"비정상 종료된 프로젝트 {recovered}개를 재시도 가능한 상태로 복구했습니다.")
    print("종료하려면 Control+C를 누르세요.")
    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
