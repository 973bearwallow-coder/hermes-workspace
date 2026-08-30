#!/usr/bin/env python3
"""Headless visual acceptance check for Atlas Mission Control."""

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "https://charles-1.taila0a481.ts.net/mission/"
ARTIFACTS = Path("/home/tom/hermes-workspace/artifacts")
ARTIFACTS.mkdir(parents=True, exist_ok=True)

results = []
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        executable_path="/usr/bin/google-chrome",
        headless=True,
        args=["--no-sandbox"],
    )
    for name, viewport in (
        ("desktop", {"width": 1440, "height": 1000}),
        ("samsung-s24", {"width": 412, "height": 915}),
    ):
        page = browser.new_page(viewport=viewport, device_scale_factor=1)
        console_errors = []
        bad_responses = []
        page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
        page.on("response", lambda reply: bad_responses.append({"url": reply.url, "status": reply.status}) if reply.status >= 400 else None)
        response = page.goto(URL, wait_until="networkidle", timeout=20000)
        page.screenshot(path=str(ARTIFACTS / f"mission-control-{name}.png"), full_page=True)
        result = page.evaluate(
            """() => ({
              title: document.title,
              h1: document.querySelector('h1')?.innerText,
              sections: [...document.querySelectorAll('section h2')].map(x => x.innerText),
              appNames: [...document.querySelectorAll('.app-card h3')].map(x => x.innerText),
              appLinks: [...document.querySelectorAll('.app-card')].map(x => x.href),
              talkLinks: [...document.querySelectorAll('.hero .button')].map(x => x.href),
              horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
              bodyWidth: document.body.getBoundingClientRect().width,
              viewportWidth: window.innerWidth
            })"""
        )
        result.update(
            layout=name,
            http_status=response.status if response else None,
            console_errors=console_errors,
            bad_responses=bad_responses,
            screenshot=str(ARTIFACTS / f"mission-control-{name}.png"),
        )
        required = {"Talk to Atlas", "Needs Your Attention", "Active Work", "Upcoming Projects", "Your Apps"}
        assert result["http_status"] == 200, result
        assert result["title"] == "Atlas Mission Control", result
        assert required.issubset(set(result["sections"])), result
        assert len(result["appNames"]) >= 4, result
        assert len(result["talkLinks"]) == 2, result
        voice_url = "https://charles-1.taila0a481.ts.net:8443/"
        assert result["talkLinks"][0] == voice_url, result
        assert not result["horizontalOverflow"], result
        assert not console_errors, result

        voice_page = browser.new_page(viewport=viewport, device_scale_factor=1)
        voice_response = voice_page.goto(voice_url, wait_until="networkidle", timeout=20000)
        voice_result = voice_page.evaluate(
            """() => ({
              title: document.title,
              h1: document.querySelector('h1')?.innerText,
              buttons: [...document.querySelectorAll('button')].map(x => x.innerText),
              horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
            })"""
        )
        assert voice_response and voice_response.status == 200, voice_result
        assert voice_result["title"] == "Atlas Voice Bridge", voice_result
        assert voice_result["h1"] == "Atlas Voice Bridge", voice_result
        assert "Start hands-free" in voice_result["buttons"], voice_result
        assert "Connect" not in voice_result["buttons"], voice_result
        assert not voice_result["horizontalOverflow"], voice_result
        result["atlas_voice"] = voice_result
        voice_page.close()

        results.append(result)
        page.close()
    browser.close()

print(json.dumps(results, indent=2))
