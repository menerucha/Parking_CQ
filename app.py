# app.py
"""
Basic Circular Queue Car Parking Visualizer
- Enqueue (park) and Dequeue (exit)
- Visual circular layout using tkinter Canvas
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import math

class CircularQueue:
    def __init__(self, capacity=8):
        self.capacity = max(4, capacity)
        self.data = [None] * self.capacity
        self.front = 0
        self.size = 0

    def is_full(self):
        return self.size == self.capacity

    def is_empty(self):
        return self.size == 0

    def enqueue(self, item):
        if self.is_full():
            raise OverflowError("Queue is full")
        idx = (self.front + self.size) % self.capacity
        self.data[idx] = item
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        item = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item

    def content_list(self):
        items = []
        for i in range(self.size):
            idx = (self.front + i) % self.capacity
            items.append(self.data[idx])
        return items

class BasicApp:
    def __init__(self, root):
        self.root = root
        root.title("Circular Queue Parking - Basic")
        self.queue = CircularQueue(capacity=8)

        # Top frame for controls
        ctrl = tk.Frame(root)
        ctrl.pack(side=tk.TOP, fill=tk.X, padx=8, pady=8)

        tk.Button(ctrl, text="Park Car (Enqueue)", command=self.park_car).pack(side=tk.LEFT, padx=4)
        tk.Button(ctrl, text="Exit Car (Dequeue)", command=self.exit_car).pack(side=tk.LEFT, padx=4)
        tk.Button(ctrl, text="Resize (set capacity)", command=self.resize_capacity).pack(side=tk.LEFT, padx=4)
        tk.Button(ctrl, text="Clear", command=self.clear_all).pack(side=tk.LEFT, padx=4)

        # Canvas for visual
        self.canvas = tk.Canvas(root, width=600, height=480, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Dashboard
        self.info_label = tk.Label(root, text="Occupancy: 0 / {}".format(self.queue.capacity))
        self.info_label.pack(side=tk.BOTTOM, pady=6)

        self.slot_items = []  # store canvas ids for slots
        self.draw_slots()
        self.update_dashboard()

    def draw_slots(self):
        self.canvas.delete("all")
        self.slot_items.clear()
        w = int(self.canvas['width'])
        h = int(self.canvas['height'])
        cx, cy = w//2, h//2
        radius = min(w, h)//2 - 80
        n = self.queue.capacity
        for i in range(n):
            angle = 2*math.pi * i / n - math.pi/2  # start at top
            x = cx + int(radius * math.cos(angle))
            y = cy + int(radius * math.sin(angle))
            r = 28
            oval = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#f0f0f0", outline="black", width=2)
            text = self.canvas.create_text(x, y, text=str(i), font=("Helvetica", 10, "bold"))
            self.slot_items.append((oval, text))
        self.redraw_cars()

    def redraw_cars(self):
        # Update slot visuals based on queue
        for i in range(self.queue.capacity):
            item = self.queue.data[i]
            oval_id, text_id = self.slot_items[i]
            if item is None:
                self.canvas.itemconfig(oval_id, fill="#f0f0f0")
                self.canvas.itemconfig(text_id, text=str(i))
            else:
                # show car id (short) inside the slot circle
                car_label = item.get('id') if isinstance(item, dict) else str(item)
                self.canvas.itemconfig(oval_id, fill="#90ee90")
                self.canvas.itemconfig(text_id, text=car_label)

        # highlight front and rear if present
        if not self.queue.is_empty():
            front_idx = self.queue.front
            rear_idx = (self.queue.front + self.queue.size - 1) % self.queue.capacity
            self.canvas.itemconfig(self.slot_items[front_idx][0], outline="blue", width=3)
            self.canvas.itemconfig(self.slot_items[rear_idx][0], outline="red", width=3)
        # reset outlines for empty
        for i in range(self.queue.capacity):
            if self.canvas.itemcget(self.slot_items[i][0], "outline") not in ("blue", "red"):
                self.canvas.itemconfig(self.slot_items[i][0], outline="black", width=2)

    def park_car(self):
        if self.queue.is_full():
            messagebox.showwarning("Full", "Parking full! Resize or remove a car.")
            return
        car_id = simpledialog.askstring("Car ID", "Enter car ID (e.g. KA01AB1234):")
        if not car_id:
            return
        entry = {'id': car_id, 'entry': datetime.now()}
        try:
            self.queue.enqueue(entry)
        except OverflowError:
            messagebox.showerror("Error", "Queue is full")
        self.redraw_cars()
        self.update_dashboard()

    def exit_car(self):
        if self.queue.is_empty():
            messagebox.showinfo("Empty", "Parking empty.")
            return
        item = self.queue.dequeue()
        if isinstance(item, dict):
            duration = datetime.now() - item['entry']
            messagebox.showinfo("Car Exited", f"Car {item['id']} exited.\nDuration: {duration}")
        self.redraw_cars()
        self.update_dashboard()

    def resize_capacity(self):
        val = simpledialog.askinteger("Resize", "Enter new capacity (>=4):", minvalue=4)
        if val is None:
            return
        # rebuild queue preserving order
        old_items = self.queue.content_list()
        newq = CircularQueue(capacity=val)
        for it in old_items:
            if newq.is_full():
                break
            newq.enqueue(it)
        self.queue = newq
        self.draw_slots()
        self.update_dashboard()

    def clear_all(self):
        self.queue = CircularQueue(capacity=self.queue.capacity)
        self.draw_slots()
        self.update_dashboard()

    def update_dashboard(self):
        occ = self.queue.size
        cap = self.queue.capacity
        self.info_label.config(text=f"Occupancy: {occ} / {cap}  |  Front: {self.queue.front}  |  Size: {self.queue.size}")
        # redraw cars to update highlights
        self.redraw_cars()

if __name__ == "__main__":
    root = tk.Tk()
    app = BasicApp(root)
    root.mainloop()
