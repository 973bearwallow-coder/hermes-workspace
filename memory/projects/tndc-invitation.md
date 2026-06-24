# TNDC Invitation Image/Video Project

## Goal
Create a classy invitation image (and eventually video) featuring a Playboy centerfold model in a gazebo setting, inviting guys to Thursday Night Drinking Club.

## Setup
- Model: Realistic Vision V5.1 at `~/models/realistic-vision-v5`
- Venv: `~/hermes-workspace/venvs/stable-diffusion/`
- Centerfold: `/home/tom/tndc_work/page-410.jpg` (mid-90s, 367x800)
- GPU: RTX 3090 24GB

## What Works
- Gazebo scene generation looks good at 768x768
- Face detection + basic blending works
- Color matching between face and scene works

## Known Issues
- SD-generated faces are often mangled (even with Realistic Vision)
- Face swap alignment is imprecise with Haar cascades
- **Clothing conflict**: SD generates dressed women, centerfold is nude
- Can't see images myself (vision provider not authenticated)

## Next Approaches to Try
1. **Inpainting** — generate clothed scene, then inpaint body areas to nude
2. **Full centerfold img2img** — use entire centerfold at strength ~0.5
3. **IP-Adapter + regional prompting** — face identity lock + separate body prompt
4. **MediaPipe face landmarks** for better alignment (installed but API changed)

## TNDC Details for Invitation
- Thursday 7:30 PM - ~10:00 PM
- Bourbon, cigars, politics, guns, jokes
- Location: Tom's place
- Style: classy but fun

## Files
- Test images: `/tmp/rv_gazebo_*.png`, `/tmp/face_blend_v*.png`
- Scripts: `/tmp/face_blend_v3.py`, `/tmp/test_rv_hires.py`
