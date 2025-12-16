# scan-new
scanner but updated
Absolutely! I can create a **well-structured project report** for your ANPR-based school vehicle monitoring system, summarizing everything so far. You can directly use this as a **prompt for documentation, GitHub README, or college submission**. I’ll make it **concise, professional, and clear**.

---

# **Project Report: School Vehicle Monitoring System Using ANPR**

## 1. Project Overview

The project is a **prototype Automated Number Plate Recognition (ANPR) system** designed for school vehicle management. It detects vehicles entering and exiting the school, identifies the students associated with the vehicles, displays the student names on an internal monitor, and alerts for unauthorized vehicles. The project demonstrates integration of **computer vision, OCR, data handling, GUI display, and text-to-speech announcement**.

**Key Objectives:**

* Detect vehicle number plates in real-time using a camera.
* Match detected plates with a predefined database of vehicles and students.
* Display student names on a monitor for school staff or students.
* Announce student names once per vehicle.
* Identify and log unauthorized vehicles.
* Maintain a queue of active vehicles to handle multiple simultaneous entries.

---

## 2. Technology Stack

| Component                           | Technology/Library     | Purpose                                           |
| ----------------------------------- | ---------------------- | ------------------------------------------------- |
| Number Plate Detection              | OpenCV                 | Capturing camera frames and preprocessing         |
| Optical Character Recognition (OCR) | EasyOCR                | Extracting text from vehicle plates               |
| Text-to-Speech Announcement         | pyttsx3                | Announcing student names to the vehicle occupants |
| GUI Display                         | Tkinter                | Displaying active vehicles and student names      |
| Database                            | JSON (`database.json`) | Stores mapping of vehicle plates to students      |
| Unauthorized Vehicle Log            | JSON (`logs.json`)     | Logs any unauthorized vehicles detected           |
| Threading                           | Python threading       | Runs camera capture and GUI concurrently          |

---

## 3. Database Structure

**database.json**:

```json
{
    "KA01AB1234": ["Aarav Sharma"],
    "MH12CD5678": ["Riya Patel", "Ananya Patel"]
}
```

* **Keys**: Vehicle number plates
* **Values**: List of students associated with the vehicle

**logs.json**:

* Automatically created on first detection of an unauthorized vehicle.
* Each entry includes `plate`, `time`, and `status`.

---

## 4. System Architecture

**1. Entry/Exit Detection**

* Camera captures vehicles approaching the school.
* EasyOCR detects and extracts the number plate.
* If the plate is **not in the queue**, it is treated as **entry**; added to queue and announced.
* If the plate is **already in the queue**, it is treated as **exit**; removed from queue.

**2. Vehicle Queue**

* Maintains all vehicles currently “inside” the school.
* Ensures multiple vehicles are tracked simultaneously.
* Prevents repeated announcements by using an `announced` flag for each vehicle.

**3. Display**

* Tkinter GUI displays:

  * Vehicle plate number
  * Associated student names
  * Alerts for unauthorized vehicles

**4. Announcements**

* Authorized vehicles trigger text-to-speech announcement of student names **only once**.
* Unauthorized vehicles trigger alert announcement.

**5. Unauthorized Vehicle Logging**

* Any plate not in `database.json` is logged into `logs.json` with timestamp.

---

## 5. Workflow Diagram

```
[Vehicle Approaches] 
        |
        v
 [Camera Capture] ---> [EasyOCR Plate Recognition]
        |
        v
[Check Queue & Database] --> [Authorized?] 
      | Yes                         | No
      v                             v
[Add to Queue + Announce]       [Log & Alert Unauthorized]
      |
      v
 [Update Tkinter Display]
      |
      v
[Vehicle Exits] ---> [Remove from Queue]
```

---

## 6. Features

* Real-time number plate detection
* Automatic entry/exit management
* Multiple students per vehicle supported
* Live GUI display of active vehicles and student names
* Single announcement per vehicle
* Unauthorized vehicle detection and logging
* Scalable for multiple vehicles during peak times

---

## 7. Demo Instructions

1. Place `database.json` in project folder with authorized vehicle-student mappings.
2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the main program:

   ```bash
   python main.py
   ```
4. Present printed plates or phone images to the camera:

   * Authorized vehicle → student names displayed and announced once.
   * Unauthorized vehicle → alert displayed and logged.
5. Rescan same plate → vehicle removed from queue (simulates exit).
6. Press `Q` in the camera window to quit, or use the Exit button in GUI.

---

## 8. Advantages & Scope

* Demonstrates **real-world ANPR system** for school safety.
* Integrates **computer vision, OCR, GUI, and TTS** in one project.
* Scalable to multiple vehicles and multiple students per vehicle.
* Easy to extend:

  * Add database backend (SQL, MongoDB) for larger scale
  * Add bounding box visualization for detected plates
  * Integrate notifications to school staff

---

This report fully covers your **current project structure and workflow**.

---

If you want, I can also **write a GitHub-ready `README.md`** version of this report with badges, instructions, and screenshots placeholders — it’ll be ready to push directly without modification.

Do you want me to do that next?

