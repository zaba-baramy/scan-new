import cv2
import easyocr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext
import json
import time
import threading

# --------------------------
# Load Vehicle Database
# --------------------------
with open("database.json", "r") as f:
    VEHICLE_DB = json.load(f)

LOG_FILE = "logs.json"

# --------------------------
# Initialize Text-to-Speech
# --------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# --------------------------
# Vehicle Queue
# --------------------------
display_queue = []  # Each item: {"plate":..., "students":..., "status":..., "announced":..., "timestamp":...}

# --------------------------
# Functions
# --------------------------
def add_vehicle(plate_text):
    global display_queue
    plate_text = plate_text.strip().upper()

    # Check if vehicle already in queue
    exists = next((v for v in display_queue if v["plate"] == plate_text), None)
    if exists:
        # Treat as exit
        remove_vehicle(plate_text)
        return

    # Authorized or not
    if plate_text in VEHICLE_DB:
        status = "AUTHORIZED"
        students = VEHICLE_DB[plate_text]
    else:
        status = "UNAUTHORIZED"
        students = []
        log_unauthorized(plate_text)

    vehicle_entry = {
        "plate": plate_text,
        "students": students,
        "status": status,
        "announced": False,
        "timestamp": time.time()
    }
    display_queue.append(vehicle_entry)
    print(f"[INFO] Vehicle Added: {plate_text}")

def remove_vehicle(plate_text):
    global display_queue
    display_queue = [v for v in display_queue if v["plate"] != plate_text]
    print(f"[INFO] Vehicle Removed: {plate_text}")

def log_unauthorized(plate_text):
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append({
        "plate": plate_text,
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "UNAUTHORIZED"
    })

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)
    print(f"[ALERT] Unauthorized Vehicle: {plate_text}")

def announce_vehicle(vehicle):
    if vehicle["announced"]:
        return
    if vehicle["status"] == "AUTHORIZED":
        names_str = ", ".join(vehicle["students"])
        message = f"{names_str}, please come to the vehicle."
        engine.say(message)
        engine.runAndWait()
    elif vehicle["status"] == "UNAUTHORIZED":
        engine.say("Unauthorized vehicle detected!")
        engine.runAndWait()
    vehicle["announced"] = True

def update_display():
    display_area.config(state='normal')
    display_area.delete(1.0, tk.END)
    
    for v in display_queue:
        if v["status"] == "AUTHORIZED":
            display_area.insert(tk.END, f"VEHICLE AUTHORIZED\nPlate: {v['plate']}\nStudents: {', '.join(v['students'])}\n\n")
        else:
            display_area.insert(tk.END, f"UNAUTHORIZED VEHICLE\nPlate: {v['plate']}\nALERT!\n\n")

    display_area.config(state='disabled')

    for v in display_queue:
        if not v["announced"]:
            announce_vehicle(v)

    root.after(1000, update_display)

# --------------------------
# OpenCV + EasyOCR Thread
# --------------------------
def camera_loop():
    reader = easyocr.Reader(['en'])
    cap = cv2.VideoCapture(0)  # Use default webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame for faster processing (optional)
        frame_resized = cv2.resize(frame, (640, 480))

        # OCR Detection
        results = reader.readtext(frame_resized)
        for (_, text, prob) in results:
            plate_text = text.replace(" ", "").upper()
            if prob > 0.4 and len(plate_text) >= 6:  # confidence + min length
                add_vehicle(plate_text)

        # Optional: show live feed
        cv2.imshow("Camera Feed (Press Q to Quit)", frame_resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# --------------------------
# Tkinter GUI Setup
# --------------------------
root = tk.Tk()
root.title("School Vehicle Display")

display_area = scrolledtext.ScrolledText(root, width=50, height=20, font=("Arial", 14))
display_area.pack(padx=10, pady=10)
display_area.config(state='disabled')

# Exit Button for manual close
btn_exit = tk.Button(root, text="Exit Program", width=20, command=root.destroy)
btn_exit.pack(pady=5)

# Start Display Loop
root.after(1000, update_display)

# Start Camera Loop in Separate Thread
cam_thread = threading.Thread(target=camera_loop, daemon=True)
cam_thread.start()

root.mainloop()
