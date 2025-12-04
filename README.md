Parking_cq

# 🚗 Circular Queue Car Parking System (Python + Tkinter)

A fully interactive **Car Parking Management System** built using a **Circular Queue (DSA)** and **Tkinter GUI**.  
I built this project as part of my **Data Structures & Algorithms (DSA) end-semester submission**, where the objective was to convert a core DSA concept into a working real-world application.

---

## 🧠 Project Overview

This system simulates a parking lot using the logic of a **Circular Queue**, enabling efficient car entry, exit, search, and management.  

It includes two versions:

- **Basic Version (`app.py`)** – Implements enqueue/dequeue operations with a circular visual layout.  
- **Improved Version (`improved_app.py`)** – Adds timestamps, search functionality, animations, dashboard insights, and dynamic UI enhancements.

---

## ✨ Features

### ✅ Basic Version (`app.py`)
- Circular Queue implementation  
- Park car (enqueue operation)  
- Exit car (dequeue operation)  
- Real-time circular slot visualization (Tkinter Canvas)  
- Queue resizing (increase/decrease capacity)  
- Dashboard: occupancy, front pointer, queue size  
- Reset/Clear all cars  

---

### 🚀 Improved Version (`improved_app.py`)
Includes all basic features plus:

#### 🔍 Car Management
- Search for a car by ID  
- Remove a car by ID (even from the middle of the queue)  
- Highlighted slot visualization  

#### ⏱ Time Tracking
- Entry timestamp  
- Duration calculation at exit  

#### 📊 Enhanced Dashboard
- Occupancy tracking  
- Front & rear pointers  
- Free slot calculation  

#### 🎨 UI Improvements
- Circular parking layout with car IDs + entry time  
- Smooth highlight animations  
- Slot click details (entry time, duration, car ID)  

---

## 🖼 Demo (Screenshots / GIFs)

> Add your own screenshots or GIF demonstrations inside the `assets/` folder.

| Basic Version | Improved Version |
|---------------|------------------|
| ![Basic Demo](assets/basic-demo.gif) | ![Improved Demo](assets/improved-demo.gif) |

---

## 📁 Folder Structure

parking-circular-queue/
│
├── app.py # Basic circular queue parking simulator
├── improved_app.py # Advanced version with search, timestamps, and UI enhancements
├── README.md # Documentation
└── assets/ # Screenshots and GIFs (optional)


---

## 🛠 Tech Stack

- **Python 3.x**
- **Tkinter** (Graphical User Interface)
- **Circular Queue (Data Structure)**
- Standard Python libraries: `tkinter`, `datetime`, `math`

No external packages required.

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/circular-queue-parking-system.git
cd circular-queue-parking-system

2️⃣ Run the Basic App
python app.py

3️⃣ Run the Improved App
python improved_app.py

🎯 How It Works
🔄 Circular Queue Logic

Each parking slot represents an index in a circular queue.
Operations:

Enqueue → Park Car

Dequeue → Exit Car

The queue wraps around automatically (circular indexing)

🗂 Search & Remove Logic

To remove a specific car:

Convert the circular queue into a linear list

Remove the selected car

Rebuild the queue while maintaining original order

This ensures proper circular queue behavior.
