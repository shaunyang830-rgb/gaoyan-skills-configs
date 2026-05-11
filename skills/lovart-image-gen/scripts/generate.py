#!/usr/bin/env python3
"""
Lovart OpenClaw 图像生成脚本
使用 ak/sk 认证调用 Lovart API 生成图像
"""

import argparse
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path


def sign_request(method: str, path: str, body: str, access_key: str, secret_key: str) -> dict:
    """生成 HMAC-SHA256 签名请求头"""
    timestamp = str(int(time.time()))
    nonce = hashlib.md5(f"{timestamp}{access_key}".encode()).hexdigest()[:16]

    # 签名字符串：method + path + timestamp + nonce + body_md5
    body_md5 = hashlib.md5(body.encode("utf-8")).hexdigest()
    sign_str = f"{method.upper()}\n{path}\n{timestamp}\n{nonce}\n{body_md5}"

    signature = hmac.new(
        secret_key.encode("utf-8"),
        sign_str.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return {
        "Content-Type": "application/json",
        "X-Access-Key": access_key,
        "X-Timestamp": timestamp,
        "X-Nonce": nonce,
        "X-Signature": signature,
    }


def generate_image(prompt: str, output_dir: str, width: int = 1024, height: int = 1024, style: str = "") -> str:
    access_key = os.environ.get("LOVART_ACCESS_KEY", "ak_2324d3ef5ae927c4f23f694a1ac5893f")
    secret_key = os.environ.get("LOVART_SECRET_KEY", "sk_1071c58e546ebe10e815e88161f4a002e048afe93ad60078005018fa41d2041c")

    base_url = "https://api.lovart.ai"
    path = "/v1/images/generate"

    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
    }
    if style:
        payload["style"] = style

    body = json.dumps(payload)
    headers = sign_request("POST", path, body, access_key, secret_key)

    print(f"[Lovart] 正在生成图像: {prompt[:60]}...")

    req = urllib.request.Request(
        f"{base_url}{path}",
        data=body.encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"[错误] HTTP {e.code}: {error_body}", file=sys.stderr)
        # 尝试备用端点格式
        return try_fallback(prompt, output_dir, width, height, style, access_key, secret_key)

    image_url = (
        result.get("data", {}).get("url")
        or result.get("url")
        or result.get("image_url")
        or (result.get("data", [{}])[0].get("url") if isinstance(result.get("data"), list) else None)
    )

    if not image_url:
        print(f"[错误] 响应中未找到图像URL: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    # 下载图片
    return download_image(image_url, output_dir, prompt)


def try_fallback(prompt, output_dir, width, height, style, access_key, secret_key):
    """尝试备用API端点"""
    base_url = "https://api.lovart.ai"
    path = "/v1/design/generate"

    payload = {"prompt": prompt, "width": width, "height": height}
    if style:
        payload["style"] = style

    body = json.dumps(payload)
    headers = sign_request("POST", path, body, access_key, secret_key)

    print(f"[Lovart] 尝试备用端点 {path}...")

    req = urllib.request.Request(
        f"{base_url}{path}",
        data=body.encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"[错误] 备用端点也失败 HTTP {e.code}: {error_body}", file=sys.stderr)
        print("\n提示：Lovart API 端点可能与预期不同，请提供官方API文档链接以便更新。", file=sys.stderr)
        sys.exit(1)

    image_url = (
        result.get("data", {}).get("url")
        or result.get("url")
        or result.get("image_url")
    )

    if not image_url:
        print(f"[错误] 备用响应中未找到图像URL: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    return download_image(image_url, output_dir, prompt)


def download_image(image_url: str, output_dir: str, prompt: str) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in prompt[:30]).strip()
    filename = f"lovart_{safe_name}_{timestamp}.png"
    output_path = str(Path(output_dir) / filename)

    print(f"[Lovart] 下载图像: {image_url[:80]}...")
    urllib.request.urlretrieve(image_url, output_path)

    print(f"[Lovart] ✅ 图像已保存: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Lovart OpenClaw 图像生成")
    parser.add_argument("--prompt", required=True, help="图像描述")
    parser.add_argument(
        "--output",
        default="C:/Users/杨顺/Documents/Obsidian Vault/Gaoyan Projects/其他/",
        help="保存目录"
    )
    parser.add_argument("--width", type=int, default=1024, help="图像宽度")
    parser.add_argument("--height", type=int, default=1024, help="图像高度")
    parser.add_argument("--style", default="", help="风格")
    args = parser.parse_args()

    output_path = generate_image(args.prompt, args.output, args.width, args.height, args.style)
    print(f"\n生成完成：{output_path}")


if __name__ == "__main__":
    main()
