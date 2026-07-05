#!/usr/bin/env python3
"""Pool Referee — Headless RTSP + HoughCircles Detection
No GUI needed. Uses ffmpeg for RTSP frame capture, OpenCV for ball detection.
"""
import cv2
import numpy as np
import os, sys, time, json

RTSP = os.environ.get("RTSP_URL", "rtsp://admin:farm1234@192.168.1.162:554/cam/realmonitor?channel=1&subtype=0")

def get_frame():
    """Grab a single frame via OpenCV (RTSP works, just don't imshow)."""
    cap = cv2.VideoCapture(RTSP, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    # Resize to manageable size for detection
    return cv2.resize(frame, (1280, 720))

def detect_balls(frame):
    """HoughCircles + HSV color classification."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    circles = cv2.HoughCircles(
        cv2.GaussianBlur(gray, (9, 9), 2),
        cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
        param1=50, param2=30, minRadius=5, maxRadius=60
    )
    
    balls = []
    if circles is not None:
        for (x, y, r) in np.round(circles[0]).astype(int):
            # Sample HSV at ball center
            if 0 <= y < hsv.shape[0] and 0 <= x < hsv.shape[1]:
                h, s, v = hsv[y, x]
                balls.append({"x": int(x), "y": int(y), "r": int(r),
                             "h": int(h), "s": int(s), "v": int(v)})
    return balls

def classify(h, s, v):
    """Simple ball color classification matching pool_ball_yolo11 IDs."""
    if s < 30 and v > 200: return 0          # cue
    if v < 60: return 8                       # eight
    if s < 50 and v > 180: return "stripe_band"  # stripe marker
    
    if h < 10 or h > 170:  return 10 if False else 3   # red
    if h < 25:              return 13 if False else 5   # orange
    if h < 35:              return 9 if False else 1    # yellow
    if h < 80:              return 14 if False else 6   # green
    if h < 130:             return 11 if False else 2   # blue
    if h < 160:             return 12 if False else 4   # purple
    return 7  # maroon

def check_stripe(hsv, x, y, r):
    """Check for white stripe band (simplified)."""
    y_top = max(0, y - r//4)
    y_bot = min(hsv.shape[0], y + r//4)
    x_l = max(0, x - r//2)
    x_r = min(hsv.shape[1], x + r//2)
    band = hsv[y_top:y_bot, x_l:x_r]
    if band.size == 0: return False
    return np.mean(band[:,:,1]) < 50 and np.mean(band[:,:,2]) > 180

def main():
    print("🏀 Pool Referee — Headless RTSP Detection")
    print(f"📷 Camera: {RTSP[:50]}...")
    
    while True:
        frame = get_frame()
        if frame is None:
            print("⚠️ Frame grab failed, retrying...")
            time.sleep(2)
            continue
        
        balls = detect_balls(frame)
        print(f"\r🎱 Balls: {len(balls)}", end="", flush=True)
        
        if len(balls) >= 10:  # Likely a rack
            print(f" | Colorful detections: {len(balls)}")
            # Show ball IDs
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            for b in balls:
                is_stripe = check_stripe(hsv, b["x"], b["y"], b["r"])
                bid = classify(b["h"], b["s"], b["v"])
                name = {0:"cue",1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",
                        8:"8",9:"9",10:"10",11:"11",12:"12",13:"13",14:"14",15:"15"}
                s = "S" if is_stripe else " "
                print(f"  {name.get(bid,'?'):>4}{s} @({b['x']},{b['y']}) h={b['h']} s={b['s']} v={b['v']}")
            break
        
        time.sleep(1)
    
    print("\n✅ Running — press Ctrl+C to stop")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n👋 Stopped")

if __name__ == "__main__":
    main()