# improved_app.py
"""
Improved Circular Queue Car Parking System with Tkinter
Features:
- Enqueue (park) with timestamp
- Dequeue (exit) with duration calculation
- Search by car ID (highlight)
- Remove car by ID anywhere in queue
- Dynamic resizing (preserve order)
- Dashboard showing occupancy, front, rear, free slots
- Visual circular layout and simple animations
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
            raise OverflowError("Queue full")
        idx = (self.front + self.size) % self.capacity
        self.data[idx] = item
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue empty")
        item = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item

    def content_list(self):
        out = []
        for i in range(self.size):
            out.append(self.data[(self.front + i) % self.capacity])
        return out

    def find_index_by_id(self, car_id):
        for i in range(self.size):
            idx = (self.front + i) % self.capacity
            item = self.data[idx]
            if item and item.get('id') == car_id:
                return idx
        return None

    def remove_by_index(self, idx_to_remove):
        # Remove element at absolute index idx_to_remove, rebuild preserving order
        if self.size == 0:
            return False
        items = self.content_list()
        # compute relative index
        rel = None
        for i in range(len(items)):
            if (self.front + i) % self.capacity == idx_to_remove:
                rel = i
                break
        if rel is None:
            return False
        new_items = items[:rel] + items[rel+1:]
        # rebuild internal structure with same capacity
        self.data = [None] * self.capacity
        self.front = 0
        self.size = 0
        for it in new_items:
            self.enqueue(it)
        return True

    def resize_preserve(self, new_capacity):
        items = self.content_list()
        self.capacity = max(4, new_capacity)
        self.data = [None] * self.capacity
        self.front = 0
        self.size = 0
        for it in items:
            if self.is_full(): break
            self.enqueue(it)

class ImprovedApp:
    def __init__(self, root):
        self.root = root
        root.title("Parking System - Circular Queue (Improved)")

        # queue and state
        self.queue = CircularQueue(capacity=8)
        self.highlighted_slot = None

        # Layout frames
        top = tk.Frame(root)
        top.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        btn_frame = tk.Frame(top)
        btn_frame.pack(side=tk.LEFT, padx=6)
        tk.Button(btn_frame, text="Park (Enqueue)", command=self.park_car).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Exit Front (Dequeue)", command=self.exit_car).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Search by ID", command=self.search_by_id).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Remove by ID", command=self.remove_by_id).pack(side=tk.LEFT, padx=4)

        control_right = tk.Frame(top)
        control_right.pack(side=tk.RIGHT)
        tk.Button(control_right, text="Resize", command=self.resize).pack(side=tk.LEFT, padx=4)
        tk.Button(control_right, text="Clear", command=self.clear_all).pack(side=tk.LEFT, padx=4)

        # Canvas for circle
        self.canvas = tk.Canvas(root, width=700, height=520, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.canvas.bind("<Configure>", lambda e: self.draw_slots())

        # Dashboard frame
        dash = tk.Frame(root)
        dash.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=6)
        self.occ_label = ttk.Label(dash, text="Occupancy: 0 / 0", anchor="center", width=25)
        self.ptr_label = ttk.Label(dash, text="Front: -  Rear: -", width=30)
        self.free_label = ttk.Label(dash, text="Free Slots: 0", width=20)
        self.occ_label.pack(side=tk.LEFT, padx=6)
        self.ptr_label.pack(side=tk.LEFT, padx=6)
        self.free_label.pack(side=tk.LEFT, padx=6)

        # tooltip/frame for details
        self.details_var = tk.StringVar()
        self.details_var.set("Select a slot or perform actions.")
        details = ttk.Label(root, textvariable=self.details_var, anchor="w")
        details.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=4)

        self.slot_items = []
        self.draw_slots()
        self.update_dashboard()

    def draw_slots(self):
        self.canvas.delete("all")
        self.slot_items.clear()
        w = self.canvas.winfo_width() or 700
        h = self.canvas.winfo_height() or 520
        cx, cy = w//2, h//2 - 20
        radius = min(w, h)//2 - 120
        n = self.queue.capacity
        for i in range(n):
            angle = 2*math.pi * i / n - math.pi/2
            x = cx + int(radius * math.cos(angle))
            y = cy + int(radius * math.sin(angle))
            r = 36
            oval = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#fafafa", outline="#444", width=2)
            idx_text = self.canvas.create_text(x, y-18, text=f"#{i}", font=("Helvetica", 9))
            content_text = self.canvas.create_text(x, y+6, text="", font=("Helvetica", 10, "bold"))
            time_text = self.canvas.create_text(x, y+22, text="", font=("Helvetica", 7))
            self.slot_items.append({
                'oval': oval, 'idx_text': idx_text, 'content': content_text, 'time': time_text,
                'coords': (x,y)
            })
        self.redraw_cars()

        # add interactivity: clicking a slot shows details
        for i, slot in enumerate(self.slot_items):
            self.canvas.tag_bind(slot['oval'], "<Button-1>", lambda e, i=i: self.on_slot_click(i))
            self.canvas.tag_bind(slot['content'], "<Button-1>", lambda e, i=i: self.on_slot_click(i))

    def redraw_cars(self):
        # populate slot visuals from queue.data (absolute indices)
        for abs_idx in range(self.queue.capacity):
            slot = self.slot_items[abs_idx]
            item = self.queue.data[abs_idx]
            if item is None:
                self.canvas.itemconfig(slot['oval'], fill="#f5f5f5")
                self.canvas.itemconfig(slot['content'], text="")
                self.canvas.itemconfig(slot['time'], text="")
            else:
                self.canvas.itemconfig(slot['oval'], fill="#b6f7c1")
                # show short id and entry time HH:MM
                cid = item.get('id', '')
                entry = item.get('entry')
                time_str = entry.strftime("%H:%M:%S") if entry else ""
                self.canvas.itemconfig(slot['content'], text=cid)
                self.canvas.itemconfig(slot['time'], text=time_str)

        # highlight front and rear slots
        if not self.queue.is_empty():
            front = self.queue.front
            rear = (self.queue.front + self.queue.size - 1) % self.queue.capacity
            # reset outlines
            for s in self.slot_items:
                self.canvas.itemconfig(s['oval'], outline="#444", width=2)
            self.canvas.itemconfig(self.slot_items[front]['oval'], outline="blue", width=3)
            self.canvas.itemconfig(self.slot_items[rear]['oval'], outline="red", width=3)
        else:
            for s in self.slot_items:
                self.canvas.itemconfig(s['oval'], outline="#444", width=2)

    def on_slot_click(self, abs_idx):
        item = self.queue.data[abs_idx]
        if item is None:
            self.details_var.set(f"Slot #{abs_idx}: empty.")
            return
        dur = datetime.now() - item['entry']
        dur_seconds = int(dur.total_seconds())
        self.details_var.set(f"Slot #{abs_idx}: Car {item['id']} | Entered: {item['entry'].strftime('%Y-%m-%d %H:%M:%S')} | Duration: {dur_seconds}s")
        # highlight briefly
        self.animate_highlight(abs_idx)

    def animate_highlight(self, idx, steps=6):
        # pulse the outline of the oval
        def step(i):
            if i >= steps:
                self.canvas.itemconfig(self.slot_items[idx]['oval'], width=3)
                return
            w = 2 + (i % 2) * 3
            self.canvas.itemconfig(self.slot_items[idx]['oval'], width=w)
            self.root.after(180, lambda: step(i+1))
        step(0)

    def park_car(self):
        if self.queue.is_full():
            messagebox.showwarning("Full", "Parking is full. Consider resizing.")
            return
        car_id = simpledialog.askstring("Car ID", "Enter Car ID (e.g. KA01AB1234):")
        if not car_id:
            return
        entry = datetime.now()
        record = {'id': car_id, 'entry': entry}
        try:
            self.queue.enqueue(record)
            self.redraw_cars()
            self.update_dashboard()
        except OverflowError:
            messagebox.showerror("Error", "Queue full")

    def exit_car(self):
        if self.queue.is_empty():
            messagebox.showinfo("Empty", "Parking is empty.")
            return
        item = self.queue.dequeue()
        if item:
            duration = datetime.now() - item['entry']
            mins = int(duration.total_seconds()//60)
            secs = int(duration.total_seconds()%60)
            messagebox.showinfo("Car Exited", f"Car {item['id']} has exited.\nDuration: {mins}m {secs}s")
            self.redraw_cars()
            self.update_dashboard()

    def search_by_id(self):
        if self.queue.is_empty():
            messagebox.showinfo("Empty", "Parking empty.")
            return
        car_id = simpledialog.askstring("Search", "Enter car ID to search:")
        if not car_id:
            return
        idx = self.queue.find_index_by_id(car_id)
        if idx is None:
            messagebox.showinfo("Not found", f"Car {car_id} not found.")
            return
        # show details and highlight
        self.on_slot_click(idx)

    def remove_by_id(self):
        if self.queue.is_empty():
            messagebox.showinfo("Empty", "Parking empty.")
            return
        car_id = simpledialog.askstring("Remove", "Enter car ID to remove:")
        if not car_id:
            return
        idx = self.queue.find_index_by_id(car_id)
        if idx is None:
            messagebox.showinfo("Not found", f"Car {car_id} not found.")
            return
        # remove
        removed = self.queue.remove_by_index(idx)
        if removed:
            messagebox.showinfo("Removed", f"Car {car_id} removed from parking.")
            self.redraw_cars()
            self.update_dashboard()
        else:
            messagebox.showerror("Error", "Could not remove car.")

    def resize(self):
        val = simpledialog.askinteger("Resize", "Enter new capacity (>=4):", minvalue=4, initialvalue=self.queue.capacity)
        if val is None:
            return
        self.queue.resize_preserve(val)
        self.draw_slots()
        self.update_dashboard()

    def clear_all(self):
        confirmed = messagebox.askyesno("Confirm", "Clear all parked cars?")
        if not confirmed:
            return
        self.queue = CircularQueue(capacity=self.queue.capacity)
        self.draw_slots()
        self.update_dashboard()

    def update_dashboard(self):
        occ = self.queue.size
        cap = self.queue.capacity
        front = self.queue.front if not self.queue.is_empty() else "-"
        rear = (self.queue.front + self.queue.size - 1) % self.queue.capacity if not self.queue.is_empty() else "-"
        free = cap - occ
        self.occ_label.config(text=f"Occupancy: {occ} / {cap}")
        self.ptr_label.config(text=f"Front: {front}    Rear: {rear}")
        self.free_label.config(text=f"Free Slots: {free}")
        self.redraw_cars()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImprovedApp(root)
    root.mainloop()
