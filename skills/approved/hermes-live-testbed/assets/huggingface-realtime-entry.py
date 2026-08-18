"""Hermes Live entrypoint for the pinned Hugging Face realtime server.

speech-to-speech 0.2.11 publishes the OpenAI Realtime ``create_response``
turn-detection field but always starts an LLM response after final STT. Hermes
Live needs the documented false setting so it can route explicit background
commands without a second, conflicting model decision.
"""

from __future__ import annotations

import importlib
import logging
import os
import sys
import time
from importlib.metadata import version
from pathlib import Path
from typing import Any


EXPECTED_VERSION = "0.2.11"


class _SilentContentConsole:
    """Drop upstream transcript rendering from the managed service logs."""

    def print(self, *_args: Any, **_kwargs: Any) -> None:
        return None


class _DropContentBelowWarning(logging.Filter):
    """Keep failures actionable without persisting ordinary conversation text."""

    _hermes_live_private_content_filter = True

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno >= logging.WARNING


def _install_private_runtime_logging_patch() -> None:
    """Suppress content-bearing output in the pinned managed runtime.

    The upstream Parakeet and Qwen handlers print transcripts directly to a
    Rich console, while its notifier and LLM output processor log the same
    content. Hermes Live runs this process as a background service, where that
    otherwise becomes an unexpected durable conversation log.
    """

    for module_name in (
        "speech_to_speech.STT.parakeet_tdt_handler",
        "speech_to_speech.TTS.qwen3_tts_handler",
    ):
        module = importlib.import_module(module_name)
        module.console = _SilentContentConsole()

    for logger_name in (
        "speech_to_speech.STT.transcription_notifier",
        "speech_to_speech.LLM.lm_output_processor",
    ):
        logger = logging.getLogger(logger_name)
        if not any(
            getattr(active, "_hermes_live_private_content_filter", False)
            for active in logger.filters
        ):
            logger.addFilter(_DropContentBelowWarning())


def _create_response_enabled(runtime_config: Any) -> bool:
    audio = getattr(getattr(runtime_config, "session", None), "audio", None)
    audio_input = getattr(audio, "input", None)
    turn_detection = getattr(audio_input, "turn_detection", None)
    if turn_detection is None:
        return True
    if isinstance(turn_detection, dict):
        value = turn_detection.get("create_response")
    else:
        value = getattr(turn_detection, "create_response", None)
    return True if value is None else bool(value)


def _install_create_response_patch() -> None:
    installed = version("speech-to-speech")
    if installed != EXPECTED_VERSION:
        raise RuntimeError(
            f"Hermes Live expected speech-to-speech {EXPECTED_VERSION}, got {installed}."
        )

    from speech_to_speech.api.openai_realtime.service import RealtimeService

    original = RealtimeService._on_transcription_completed
    if getattr(original, "_hermes_live_create_response_patch", False):
        return

    def patched(self: Any, conn_id: str, event: Any) -> Any:
        state = self._state(conn_id)
        if _create_response_enabled(state.runtime_config):
            return original(self, conn_id, event)

        # The upstream method performs all transcript bookkeeping and emits
        # the final protocol event. Temporarily withholding only its LLM queue
        # preserves that behavior while honoring create_response=false. The
        # handler is synchronous on one pipeline event loop, so no other
        # connection can observe this bounded substitution.
        queue = self.text_prompt_queue
        self.text_prompt_queue = None
        try:
            return original(self, conn_id, event)
        finally:
            self.text_prompt_queue = queue

    patched._hermes_live_create_response_patch = True  # type: ignore[attr-defined]
    RealtimeService._on_transcription_completed = patched


def _install_exact_speech_patch() -> None:
    from speech_to_speech.LLM.language_model import BaseLanguageModelHandler
    from speech_to_speech.pipeline.messages import (
        EndOfResponse,
        GenerateResponseRequest,
        LLMResponseChunk,
    )

    original = BaseLanguageModelHandler.process
    if getattr(original, "_hermes_live_exact_speech_patch", False):
        return

    def patched(self: Any, request: Any) -> Any:
        if isinstance(request, GenerateResponseRequest):
            response = request.response
            metadata = getattr(response, "metadata", None) if response else None
            purpose = metadata.get("hermes_live_purpose") if isinstance(metadata, dict) else None
            exact = metadata.get("hermes_live_exact_speech") if isinstance(metadata, dict) else None
            if purpose in {"conversation_answer", "tool_receipt", "task_notification"}:
                if (
                    not isinstance(exact, str)
                    or not exact.strip()
                    or len(exact) > 500
                    or any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in exact)
                ):
                    raise RuntimeError("Hermes Live exact speech metadata is invalid.")
                generation = self.cancel_scope.generation if self.cancel_scope else None
                yield LLMResponseChunk(
                    text=exact,
                    runtime_config=request.runtime_config,
                    response=response,
                    turn_id=request.turn_id,
                    turn_revision=request.turn_revision,
                    speech_stopped_at_s=request.speech_stopped_at_s,
                    cancel_generation=generation,
                )
                yield EndOfResponse(
                    turn_id=request.turn_id,
                    turn_revision=request.turn_revision,
                    cancel_generation=generation,
                )
                return
        yield from original(self, request)

    patched._hermes_live_exact_speech_patch = True  # type: ignore[attr-defined]
    BaseLanguageModelHandler.process = patched


def _install_empty_response_tools_patch() -> None:
    from speech_to_speech.LLM.language_model import BaseLanguageModelHandler
    from speech_to_speech.pipeline.messages import GenerateResponseRequest

    original = BaseLanguageModelHandler.process
    if getattr(original, "_hermes_live_empty_tools_patch", False):
        return

    def patched(self: Any, request: Any) -> Any:
        response = request.response if isinstance(request, GenerateResponseRequest) else None
        fields = getattr(response, "model_fields_set", set()) if response else set()
        if response and "tools" in fields and response.tools == []:
            session = request.runtime_config.session
            previous = session.tools
            session.tools = []
            try:
                yield from original(self, request)
            finally:
                session.tools = previous
            return
        yield from original(self, request)

    patched._hermes_live_empty_tools_patch = True  # type: ignore[attr-defined]
    BaseLanguageModelHandler.process = patched


def _install_transformers_tool_content_patch() -> None:
    """Keep MLX/Hugging Face chat templates compatible after tool calls.

    speech-to-speech 0.2.11 serializes assistant function-call history without
    a ``content`` key. Qwen templates read that key even when ``tool_calls`` is
    present, so the follow-up response fails before generation. Normalize only
    that assistant history shape and leave every other message unchanged.
    """

    from speech_to_speech.LLM.chat import Chat

    original = Chat.to_transformers_chat
    if getattr(original, "_hermes_live_tool_content_patch", False):
        return

    def patched(self: Any) -> list[dict[str, Any]]:
        messages = original(self)
        for message in messages:
            if (
                isinstance(message, dict)
                and message.get("role") == "assistant"
                and isinstance(message.get("tool_calls"), list)
            ):
                message.setdefault("content", "")
        return messages

    patched._hermes_live_tool_content_patch = True  # type: ignore[attr-defined]
    Chat.to_transformers_chat = patched


def _install_latency_instrumentation_patch() -> None:
    """Emit privacy-safe monotonic stage markers for realtime voice turns.

    Markers intentionally contain only stage, timestamp, and opaque turn/revision
    identifiers. They make VAD/STT/LLM/TTS regressions measurable without
    persisting transcript or response content in the service journal.
    """

    timing_logger = logging.getLogger("hermes_live.voice_timing")

    def mark(stage: str, **fields: Any) -> None:
        suffix = " ".join(f"{key}={value}" for key, value in fields.items() if value is not None)
        timing_logger.info("VOICE_TIMING stage=%s t=%.6f%s", stage, time.perf_counter(), f" {suffix}" if suffix else "")

    from speech_to_speech.STT.faster_whisper_handler import FasterWhisperSTTHandler

    original_stt = FasterWhisperSTTHandler.process
    if not getattr(original_stt, "_hermes_live_latency_patch", False):
        def timed_stt(self: Any, vad_audio: Any) -> Any:
            fields = {"turn": getattr(vad_audio, "turn_id", None), "rev": getattr(vad_audio, "turn_revision", None)}
            mark("vad_end_stt_start", **fields)
            emitted = False
            for output in original_stt(self, vad_audio):
                if not emitted:
                    mark("stt_complete", **fields)
                    emitted = True
                yield output
            if not emitted:
                mark("stt_empty", **fields)

        timed_stt._hermes_live_latency_patch = True  # type: ignore[attr-defined]
        FasterWhisperSTTHandler.process = timed_stt

    from speech_to_speech.LLM.chat_completions_language_model import ChatCompletionsApiModelHandler
    from speech_to_speech.LLM.base_openai_compatible_language_model import TextDelta

    original_request = ChatCompletionsApiModelHandler._request
    if not getattr(original_request, "_hermes_live_latency_patch", False):
        def timed_request(self: Any, api_input: Any, optional_kwargs: Any) -> Any:
            mark("llm_request_start")
            return original_request(self, api_input, optional_kwargs)

        timed_request._hermes_live_latency_patch = True  # type: ignore[attr-defined]
        ChatCompletionsApiModelHandler._request = timed_request

    original_stream = ChatCompletionsApiModelHandler._iter_stream_events
    if not getattr(original_stream, "_hermes_live_latency_patch", False):
        def timed_stream(self: Any, api_response: Any) -> Any:
            first_text = False
            for output in original_stream(self, api_response):
                if not first_text and isinstance(output, TextDelta) and output.text:
                    mark("llm_first_token")
                    first_text = True
                yield output

        timed_stream._hermes_live_latency_patch = True  # type: ignore[attr-defined]
        ChatCompletionsApiModelHandler._iter_stream_events = timed_stream

    from speech_to_speech.TTS.kokoro_handler import KokoroTTSHandler
    from speech_to_speech.pipeline.messages import TTSInput

    original_tts = KokoroTTSHandler.process
    if not getattr(original_tts, "_hermes_live_latency_patch", False):
        def timed_tts(self: Any, tts_input: Any) -> Any:
            # The handler may run in a child process whose PyTorch thread pool
            # did not inherit the entry-process setting. Enforce the measured
            # eight-core optimum at the actual synthesis boundary.
            import torch

            if torch.get_num_threads() != 8:
                torch.set_num_threads(8)
            fields = {"turn": getattr(tts_input, "turn_id", None), "rev": getattr(tts_input, "turn_revision", None)}
            is_text = isinstance(tts_input, TTSInput)
            if is_text:
                mark("tts_start", **fields)
            emitted = False
            for output in original_tts(self, tts_input):
                if is_text and not emitted:
                    mark("tts_first_audio", **fields)
                    emitted = True
                yield output

        timed_tts._hermes_live_latency_patch = True  # type: ignore[attr-defined]
        KokoroTTSHandler.process = timed_tts


def _install_hermes_voice_request_patch() -> None:
    """Request no model reasoning for the low-latency spoken lane only.

    The local Hermes OpenAI-compatible endpoint accepts this as a request-scoped
    ``model_options`` override.  It leaves Tom's normal Hermes/Codex sessions and
    global config untouched while avoiding hidden reasoning before a short voice
    answer.  Other OpenAI-compatible endpoints retain their upstream behavior.
    """

    from speech_to_speech.LLM.chat_completions_language_model import ChatCompletionsApiModelHandler

    original = ChatCompletionsApiModelHandler._build_extra_body
    if getattr(original, "_hermes_live_voice_request_patch", False):
        return

    @classmethod
    def patched(cls: Any, base_url: str | None, disable_thinking: bool, reasoning_effort: str | None) -> Any:
        normalized = (base_url or "").rstrip("/")
        if normalized in {"http://127.0.0.1:8642/v1", "http://localhost:8642/v1"}:
            return {"model_options": {"reasoning_effort": "none"}}
        return original(base_url, disable_thinking, reasoning_effort)

    patched._hermes_live_voice_request_patch = True  # type: ignore[attr-defined]
    ChatCompletionsApiModelHandler._build_extra_body = patched


def _tune_cpu_inference_threads() -> None:
    """Give Kokoro one worker per physical core instead of the inherited 1."""

    import torch

    # Charles has 8 physical Zen 3 cores. Direct Kokoro measurement for the
    # pinned voice/phrase was ~1.43 s at one thread and ~0.31 s at eight;
    # additional SMT threads regressed latency.
    torch.set_num_threads(8)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        # PyTorch allows this only before inter-op work starts.
        pass


def _inject_file_backed_llm_key() -> None:
    """Load the Hermes API bearer key without exposing it in the OS command line."""

    key_file = os.environ.get("HERMES_LIVE_LLM_API_KEY_FILE", "").strip()
    if not key_file or "--responses_api_api_key" in sys.argv or "--responses-api-api-key" in sys.argv:
        return
    path = Path(key_file).expanduser().resolve()
    key = path.read_text(encoding="utf-8").strip()
    if not key or any(char.isspace() for char in key):
        raise RuntimeError("Hermes Live LLM API key file is empty or invalid.")
    sys.argv.extend(["--responses_api_api_key", key])


def main() -> None:
    _inject_file_backed_llm_key()
    _tune_cpu_inference_threads()
    _install_create_response_patch()
    _install_exact_speech_patch()
    _install_empty_response_tools_patch()
    _install_transformers_tool_content_patch()
    _install_hermes_voice_request_patch()
    _install_latency_instrumentation_patch()
    _install_private_runtime_logging_patch()
    from speech_to_speech.s2s_pipeline import main as upstream_main

    upstream_main()


if __name__ == "__main__":
    main()
