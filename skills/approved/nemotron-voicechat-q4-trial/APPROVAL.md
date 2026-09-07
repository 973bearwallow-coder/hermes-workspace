# Approved bounded Nemotron VoiceChat runtime

- Upstream: https://github.com/sansamour/llama-voicechat.cpp.git
- Branch: `voicechat`
- Commit: `f45001fc3d8013c72beb6753d3eb0b976b6a9fff`
- Quarantine source: `/home/tom/hermes-live-testbed/benchmarks/quarantine/sansamour-llama-voicechat.cpp`
- Purpose: isolated RTX 3090 Q4 VoiceChat benchmark only.

## Sanitization

- Removed `.git`, `.github`, app, examples, pocs, tests, docs, media, devops, scripts, converter/debug Python, and every unrelated tool subtree.
- `tools/CMakeLists.txt` builds only `mtmd` and `voicechat`.
- Configure flags disable server, app, UI, tests, examples, OpenSSL, subprocess, RPC, dynamic backends, native tuning, and install targets.
- The VoiceChat CLI source contains no socket, HTTP, subprocess, shell, or external tool implementation.
- Model paths and output WAV paths are explicit local files.
- Real tools remain unavailable. Any model function event is captured and answered only by the benchmark's fixed denial response.

## Model manifest

Repository: `hoidhxd/NVIDIA-NemotronLabs-VoiceChat-11B-GGUF`
Revision inspected: API state on 2026-09-06.

- `llamacpp/nemotron_voicechat_11b-stt-llm-Q4_0.gguf`, 5,015,077,920 bytes, SHA-256/LFS oid `dc31d53bfe853b1ec106b9becf184d3bc55569473bd5aee68ef12f0ae9d86342`
- `llamacpp/nemotron_voicechat_11b-stt-llm-Q4_0-function-head.gguf`, 330,302,208 bytes, SHA-256/LFS oid `7ecb89e4ef21975ad9c5f173abb2d3a224c0231e6fe937f099011a519251765e`
- `llamacpp/mmproj-voicechat-perception-Q4_0.gguf`, 456,089,120 bytes, SHA-256/LFS oid `4b07cc374e7690cdca3d525eca36f74998943daf495a4fcdb07e774f469d7c2a`
- `llamacpp/voicechat-tts-Q4_0.gguf`, 718,740,608 bytes, SHA-256/LFS oid `07420c7b0eccdf56334f4cfd5cd002a61a591b37ff25e2b6377b9f1e6b3396aa`

Total: 6,520,209,856 bytes (6.07 GiB).
