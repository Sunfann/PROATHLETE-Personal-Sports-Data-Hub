#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROATHLETE Garmin 同步后端 — 中国区 (garmin.cn) 专用版
========================================================
强制使用 is_cn=True，适配 Garmin 中国版账号的认证流程。

前置要求（务必先执行）:
    pip install --upgrade "garminconnect>=0.3.4" curl_cffi ua-generator

启动:
    python garmin_server.py

前端后端地址填写: http://localhost:5000
"""

import io
import os
import sys
import time
import base64
import zipfile
import threading
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from flask import Flask, jsonify, request
from flask_cors import CORS

# ---------------------------------------------------------------------------
# 导入 garminconnect（强制要求较新版本）
# ---------------------------------------------------------------------------
GARMINCONNECT_AVAILABLE = False
GARMINCONNECT_VERSION = "not installed"
Garmin = None

try:
    import garminconnect as _gc_mod
    from garminconnect import Garmin
    GARMINCONNECT_AVAILABLE = True
    GARMINCONNECT_VERSION = getattr(_gc_mod, "__version__", "unknown")
except ImportError as e:
    _IMPORT_ERROR = str(e)
else:
    _IMPORT_ERROR = ""

# ---------------------------------------------------------------------------
# 检查 curl_cffi 是否可用（中国区必需）
# ---------------------------------------------------------------------------
CURL_CFFI_AVAILABLE = False
try:
    import curl_cffi  # noqa: F401
    CURL_CFFI_AVAILABLE = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Flask 应用
# ---------------------------------------------------------------------------
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ---------------------------------------------------------------------------
# 任务状态存储
# ---------------------------------------------------------------------------
_tasks_lock = threading.Lock()
_tasks: Dict[str, Dict[str, Any]] = {}
_TASK_TTL = 3600


def _cleanup_old_tasks():
    now = time.time()
    expired = []
    with _tasks_lock:
        for tid, info in _tasks.items():
            if info.get("finished_at") and (now - info["finished_at"]) > _TASK_TTL:
                expired.append(tid)
        for tid in expired:
            _tasks.pop(tid, None)


def _new_task() -> str:
    import uuid
    task_id = uuid.uuid4().hex[:12]
    with _tasks_lock:
        _tasks[task_id] = {
            "status": "pending",
            "message": "任务已创建，等待执行...",
            "done": 0,
            "total": 0,
            "files": [],
            "error": None,
            "created_at": time.time(),
            "finished_at": None,
        }
    return task_id


def _update_task(task_id: str, **kwargs):
    with _tasks_lock:
        if task_id in _tasks:
            _tasks[task_id].update(kwargs)


def _get_task(task_id: str) -> Optional[Dict[str, Any]]:
    with _tasks_lock:
        return dict(_tasks.get(task_id)) if task_id in _tasks else None


# ---------------------------------------------------------------------------
# Garmin 中国区登录
# ---------------------------------------------------------------------------
def _login_garmin_cn(email: str, password: str) -> "Garmin":
    """
    登录 Garmin Connect 中国版 (garmin.cn)。
    强制 is_cn=True，并依赖 garminconnect>=0.3.4 的域名感知认证修复。
    """
    if not GARMINCONNECT_AVAILABLE:
        raise RuntimeError(
            f"garminconnect 库不可用（{_IMPORT_ERROR}）。"
            "请执行: pip install --upgrade 'garminconnect>=0.3.4'"
        )

    # ---- 版本检查：中国区认证修复需要 >= 0.3.4 ----
    try:
        ver_parts = [int(x) for x in str(GARMINCONNECT_VERSION).split(".")[:3]]
        while len(ver_parts) < 3:
            ver_parts.append(0)
        if ver_parts < [0, 3, 4]:
            raise RuntimeError(
                f"当前 garminconnect 版本为 {GARMINCONNECT_VERSION}，"
                "中国区认证修复需要 >= 0.3.4。"
                "请执行: pip install --upgrade 'garminconnect>=0.3.4'"
            )
    except RuntimeError:
        raise
    except Exception:
        pass  # 版本号无法解析时跳过检查，让实际登录暴露问题

    # ---- 检查 curl_cffi（Cloudflare 绕过） ----
    if not CURL_CFFI_AVAILABLE:
        print(
            "[警告] 未检测到 curl_cffi。中国区 SSO 端点 (sso.garmin.cn) "
            "可能因 Cloudflare TLS 指纹检测而失败。\n"
            "       建议执行: pip install curl_cffi ua-generator",
            file=sys.stderr,
        )

    # ---- 登录 ----
    try:
        client = Garmin(email, password, is_cn=True)
        client.login()
        return client

    except Exception as e:
        err_msg = str(e).lower()
        original = str(e)

        # 401：认证失败——区分几种可能原因
        if "401" in err_msg or "unauthorized" in err_msg or "invalid username" in err_msg:
            # 检查是否真的走了中国区端点
            cn_hint = ""
            if not CURL_CFFI_AVAILABLE:
                cn_hint = (
                    "\n  → 未安装 curl_cffi，中国区 SSO 可能被 Cloudflare 拦截。"
                    "\n    请执行: pip install curl_cffi ua-generator"
                )
            raise RuntimeError(
                "Garmin 中国区账号认证失败（401）。请依次检查：\n"
                "  1. 邮箱和密码是否与 garmin.cn 一致（不是 garmin.com）\n"
                "  2. garminconnect 是否已升级到 >= 0.3.4\n"
                "  3. 是否安装了 curl_cffi 和 ua-generator\n"
                "  4. 账号是否启用了 MFA（多因素认证）\n"
                f"  原始错误: {original}"
                f"{cn_hint}"
            ) from e

        if "mfa" in err_msg or "multi" in err_msg or "verification" in err_msg:
            raise RuntimeError(
                "Garmin 账号启用了多因素认证（MFA），程序化登录无法直接完成。"
                "请暂时关闭 MFA 后重试。"
            ) from e

        if "rate" in err_msg or "429" in err_msg:
            raise RuntimeError(
                "请求被 Garmin 限流（429）。请等待数小时后再试，"
                "或切换网络环境（如使用手机热点）更换公网 IP。"
            ) from e

        if "cloudflare" in err_msg or "403" in err_msg:
            raise RuntimeError(
                "请求被 Cloudflare 拦截（403）。请确认已安装 curl_cffi：\n"
                "  pip install curl_cffi ua-generator"
            ) from e

        raise RuntimeError(f"Garmin 中国区登录失败: {original}") from e


# ---------------------------------------------------------------------------
# 下载 FIT 并转 Base64
# ---------------------------------------------------------------------------
def _download_fit_b64(client: "Garmin", activity_id: int) -> Optional[str]:
    """
    下载指定活动的 FIT 文件，解压 ZIP 后返回 Base64 字符串。
    兼容不同版本的 garminconnect API。
    """
    try:
        raw = None

        # ---- 尝试 download_activity ----
        if hasattr(client, "download_activity"):
            try:
                from garminconnect import ActivityDownloadFormat
                raw = client.download_activity(
                    activity_id, dl_fmt=ActivityDownloadFormat.ORIGINAL
                )
            except (ImportError, TypeError):
                try:
                    raw = client.download_activity(activity_id, dl_fmt="fit")
                except Exception:
                    raw = client.download_activity(activity_id)
            except Exception:
                raw = None

        # ---- 备用 get_activity_fit ----
        if raw is None and hasattr(client, "get_activity_fit"):
            try:
                raw = client.get_activity_fit(activity_id)
            except Exception:
                raw = None

        if not raw:
            return None

        # ---- 统一转为 bytes 并处理 ----
        if isinstance(raw, str):
            if os.path.exists(raw):
                with open(raw, "rb") as f:
                    data = f.read()
            else:
                # 假设已是 base64 字符串
                return raw
        elif isinstance(raw, bytes):
            data = raw
        else:
            return None

        # ---- 解 ZIP ----
        if data[:2] == b"PK":
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                fit_names = [n for n in zf.namelist() if n.lower().endswith(".fit")]
                if not fit_names:
                    return None
                fit_bytes = zf.read(fit_names[0])
                return base64.b64encode(fit_bytes).decode("ascii")

        # ---- 直接是 FIT ----
        return base64.b64encode(data).decode("ascii")

    except Exception:
        return None


# ---------------------------------------------------------------------------
# 同步工作线程
# ---------------------------------------------------------------------------
def _sync_worker(
    task_id: str,
    email: str,
    password: str,
    last_sync: Optional[str],
    days_back: int,
):
    try:
        _update_task(task_id, status="running", message="正在登录 Garmin 中国区...")

        client = _login_garmin_cn(email, password)
        _update_task(task_id, message="登录成功，正在获取活动列表...")

        today = datetime.now().date()
        try:
            db = int(days_back)
        except Exception:
            db = 30
        # days_back > 0 时始终以用户配置的天数为准（避免增量同步被压缩成最近一天）
        if db > 0:
            start_date = today - timedelta(days=db)
        elif last_sync:
            try:
                start_date = datetime.strptime(last_sync, "%Y-%m-%d").date() - timedelta(days=1)
            except Exception:
                start_date = today - timedelta(days=30)
        else:
            start_date = today - timedelta(days=30)

        start_str = start_date.isoformat()
        end_str = today.isoformat()
        span_days = (today - start_date).days

        _update_task(task_id, message=f"获取 {start_str} 至 {end_str} 的活动（共 {span_days} 天）...")

        # ---- 获取活动列表（按 60 天分块，避免大范围一次性拉取失败）----
        activities: List[Dict[str, Any]] = []
        seen_ids = set()
        try:
            if hasattr(client, "get_activities_by_date"):
                CHUNK = 60
                cur = start_date
                while cur <= today:
                    seg_end = min(cur + timedelta(days=CHUNK - 1), today)
                    part = None
                    try:
                        part = client.get_activities_by_date(cur.isoformat(), seg_end.isoformat()) or []
                    except Exception as seg_err:
                        print(f"[Sync] 分段 {cur}~{seg_end} 获取失败: {seg_err}", file=sys.stderr)
                        part = []
                    for a in part:
                        aid = a.get("activityId")
                        if aid is not None and aid in seen_ids:
                            continue
                        if aid is not None:
                            seen_ids.add(aid)
                        activities.append(a)
                    _update_task(
                        task_id,
                        message=f"已获取 {cur.isoformat()}~{seg_end.isoformat()} 的活动，累计 {len(activities)} 条",
                    )
                    cur = seg_end + timedelta(days=1)
                    time.sleep(0.3)
            elif hasattr(client, "get_activities"):
                offset = 0
                while True:
                    batch = client.get_activities(offset, 200) or []
                    if not batch:
                        break
                    for a in batch:
                        act_date = (a.get("startTimeLocal") or "")[:10]
                        if start_str <= act_date <= end_str:
                            aid = a.get("activityId")
                            if aid is not None and aid in seen_ids:
                                continue
                            if aid is not None:
                                seen_ids.add(aid)
                            activities.append(a)
                    offset += 200
                    if len(batch) < 200:
                        break
        except Exception as e:
            raise RuntimeError(f"获取活动列表失败: {e}") from e

        if not activities:
            _update_task(
                task_id, status="completed",
                message="没有新活动需要同步",
                done=0, total=0, files=[],
                finished_at=time.time(),
            )
            return

        total = len(activities)
        _update_task(
            task_id,
            message=f"找到 {total} 条活动，开始下载 FIT...",
            total=total, done=0,
        )

        # ---- 逐个下载 ----
        files_out: List[Dict[str, str]] = []
        for idx, act in enumerate(activities):
            act_id = act.get("activityId")
            if act_id is None:
                continue

            start_time = act.get("startTimeLocal") or ""
            date_part = start_time[:10] if start_time else "unknown"
            filename = f"{date_part}_{act_id}.fit"

            b64 = _download_fit_b64(client, act_id)
            if b64:
                files_out.append({"name": filename, "data": b64})

            done = idx + 1
            _update_task(
                task_id, done=done,
                message=f"下载中... {done}/{total}",
            )
            time.sleep(0.35)  # 温和限速，避免触发 Garmin 风控

        _update_task(
            task_id, status="completed",
            message=f"同步完成，共获取 {len(files_out)} 个 FIT 文件",
            done=total, total=total,
            files=files_out,
            finished_at=time.time(),
        )

    except Exception as e:
        tb = traceback.format_exc()
        print(f"[Sync Error] {e}\n{tb}", file=sys.stderr)
        _update_task(
            task_id, status="failed",
            message=str(e), error=str(e),
            finished_at=time.time(),
        )


# ---------------------------------------------------------------------------
# API 路由
# ---------------------------------------------------------------------------
@app.route("/api/garmin/health", methods=["GET"])
def health():
    return jsonify(
        status="ok",
        version="2.0.0-cn",
        region="cn",
        garminconnect=GARMINCONNECT_AVAILABLE,
        garminconnect_version=GARMINCONNECT_VERSION,
        curl_cffi=CURL_CFFI_AVAILABLE,
        server_time=datetime.now().isoformat(),
    )


@app.route("/api/garmin/sync", methods=["POST"])
def start_sync():
    if not GARMINCONNECT_AVAILABLE:
        return jsonify({
            "error": (
                "garminconnect 库不可用。请执行：\n"
                "pip install --upgrade 'garminconnect>=0.3.4' curl_cffi ua-generator"
            )
        }), 500

    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    last_sync = (data.get("last_sync") or "").strip() or None
    days_back = int(data.get("days_back") or 30)

    if not email or not password:
        return jsonify({"error": "缺少邮箱或密码"}), 400

    _cleanup_old_tasks()
    task_id = _new_task()

    threading.Thread(
        target=_sync_worker,
        args=(task_id, email, password, last_sync, days_back),
        daemon=True,
    ).start()

    return jsonify({"task_id": task_id})


@app.route("/api/garmin/sync/<task_id>", methods=["GET"])
def sync_status(task_id: str):
    info = _get_task(task_id)
    if not info:
        return jsonify({"error": "任务不存在或已过期"}), 404
    return jsonify({
        "status": info.get("status"),
        "message": info.get("message"),
        "done": info.get("done", 0),
        "total": info.get("total", 0),
        "files": info.get("files", []),
        "error": info.get("error"),
    })


@app.route("/api/garmin/sync/<task_id>", methods=["DELETE"])
def cancel_task(task_id: str):
    with _tasks_lock:
        _tasks.pop(task_id, None)
    return jsonify({"ok": True})


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 62)
    print("  PROATHLETE Garmin Sync Server  ·  中国区 (garmin.cn)")
    print("=" * 62)
    print(f"  garminconnect : {'可用 ' + GARMINCONNECT_VERSION if GARMINCONNECT_AVAILABLE else '未安装'}")
    print(f"  curl_cffi     : {'可用' if CURL_CFFI_AVAILABLE else '未安装 (中国区建议安装)'}")
    print(f"  区域模式      : is_cn=True (强制)")
    print()
    if not GARMINCONNECT_AVAILABLE:
        print("  [!] 请先执行:")
        print("      pip install --upgrade 'garminconnect>=0.3.4' curl_cffi ua-generator")
        print()
    if not CURL_CFFI_AVAILABLE:
        print("  [!] 未安装 curl_cffi，中国区 SSO 可能被 Cloudflare 拦截:")
        print("      pip install curl_cffi ua-generator")
        print()
    print("  监听: http://0.0.0.0:5000")
    print("  前端填写: http://localhost:5000")
    print("  按 Ctrl+C 停止")
    print("=" * 62)

    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)