#!/usr/bin/env python3
"""
vision_analyze.py — Analyze images using a vision-capable LLM via OpenRouter.

Default model: nvidia/nemotron-nano-12b-v2-vl:free (vision+language, 128K ctx)
Fallback: google/gemma-4-26b-a4b-it:free (huge 262K ctx)

Usage:
    python3 vision_analyze.py <image_path> [prompt]
    python3 vision_analyze.py --ocr <image_path>
    python3 vision_analyze.py --compare <image1> <image2> [prompt]
    python3 vision_analyze.py --batch <image_dir> [prompt]
    python3 vision_analyze.py --screenshot [prompt]        # analyze current screen
    python3 vision_analyze.py --model <model_name> <image>  # use specific model
"""

import sys
import os
import json
import base64
import argparse
import subprocess
from pathlib import Path

DEFAULT_MODEL = "nvidia/nemotron-nano-12b-v2-vl:free"
FALLBACK_MODEL = "google/gemma-4-26b-a4b-it:free"

def load_env(path=None):
    if path is None:
        path = os.path.expanduser("~/.hermes/.env")
    env = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k.startswith('export '):
                        k = k[7:]
                    env[k] = v
    return env

def encode_image(image_path):
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    suffix = path.suffix.lower()
    mime_map = {
        '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.webp': 'image/webp', '.gif': 'image/gif', '.bmp': 'image/bmp',
    }
    mime = mime_map.get(suffix, 'image/jpeg')
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:{mime};base64,{data}"

def take_screenshot(path="/tmp/vision_screenshot.png"):
    """Take a screenshot using scrot."""
    import shutil
    if not shutil.which("scrot"):
        raise RuntimeError("scrot not installed. Run: sudo apt install scrot")
    for disp in [":1", ":0"]:
        env = os.environ.copy()
        env['DISPLAY'] = disp
        try:
            subprocess.run(["scrot", "-o", path], capture_output=True, timeout=10, env=env)
            if Path(path).exists():
                return path
        except:
            pass
    raise RuntimeError("Could not take screenshot. Is X running?")

def call_vision_api(images, prompt, model=DEFAULT_MODEL, api_key=None):
    """Call OpenRouter vision API. images = list of file paths."""
    import urllib.request
    
    if api_key is None:
        env = load_env()
        api_key = env.get('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError("No OPENROUTER_API_KEY in ~/.hermes/.env")

    content = [{"type": "text", "text": prompt}]
    for img_path in images:
        data_url = encode_image(img_path)
        content.append({"type": "image_url", "image_url": {"url": data_url}})

    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 2048
    }).encode('utf-8')

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://hermes-agent.nousresearch.com",
            "X-Title": "Atlas Vision"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode())
            return result['choices'][0]['message']['content']
    except Exception as e:
        if model != FALLBACK_MODEL:
            print(f"[WARN] {model} failed: {e}, trying fallback...", file=sys.stderr)
            return call_vision_api(images, prompt, FALLBACK_MODEL, api_key)
        raise

def main():
    parser = argparse.ArgumentParser(description="Analyze images with vision LLM")
    parser.add_argument('image', nargs='?', help="Path to image file")
    parser.add_argument('prompt', nargs='?', default=None, help="Analysis prompt")
    parser.add_argument('--ocr', action='store_true', help="Extract all text from image")
    parser.add_argument('--compare', nargs=2, metavar=('IMG1', 'IMG2'), help="Compare two images")
    parser.add_argument('--batch', help="Analyze all images in a directory")
    parser.add_argument('--screenshot', action='store_true', help="Screenshot current screen and analyze")
    parser.add_argument('--model', default=DEFAULT_MODEL, help=f"Model (default: {DEFAULT_MODEL})")
    parser.add_argument('--json', action='store_true', help="Output raw JSON")
    
    args = parser.parse_args()
    
    if args.ocr:
        prompt = ("Extract and transcribe ALL text in this image exactly as it appears. "
                 "Preserve formatting, line breaks, and structure. If there is no text, say 'No text found'.")
    elif args.prompt:
        prompt = args.prompt
    else:
        prompt = ("Describe this image in detail. Include objects, colors, text, people, "
                 "setting, and any notable features.")

    try:
        if args.screenshot:
            path = take_screenshot()
            print(f"[Screenshot: {path}]\n")
            result = call_vision_api([path], prompt, args.model)
            print(result)
        elif args.compare:
            result = call_vision_api(list(args.compare), prompt, args.model)
            print(result)
        elif args.batch:
            img_dir = Path(args.batch)
            images = sorted(
                list(img_dir.glob('*.png')) + list(img_dir.glob('*.jpg')) +
                list(img_dir.glob('*.jpeg')) + list(img_dir.glob('*.webp'))
            )
            if not images:
                print(f"No images found in {img_dir}")
                sys.exit(1)
            print(f"Analyzing {len(images)} images...\n")
            for img_path in images:
                print(f"=== {img_path.name} ===")
                result = call_vision_api([str(img_path)], prompt, args.model)
                print(result)
                print()
        elif args.image:
            result = call_vision_api([args.image], prompt, args.model)
            print(result)
        else:
            parser.print_help()
            sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
