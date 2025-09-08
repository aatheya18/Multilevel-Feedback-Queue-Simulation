import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

class Process:
    def __init__(self, pid, arrival, cpu, priority):
        self.pid = pid
        self.arrival = arrival
        self.original_cpu = cpu
        self.remaining_cpu = cpu
        self.priority = priority
        self.queue_level = 1  # All processes start in Queue 1
        self.last_executed_time = -1
        self.time_in_current_queue = 0  # Track time spent in current queue
        self.time_since_last_execution = 0  # Track time since last execution for aging

class MLFQScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Multilevel Feedback Queue Scheduling")
        self.root.state("zoomed")  # Fullscreen
        self.processes = []
        self.queues = {
            1: deque(),  # Queue 1 (RR with time_quantum1)
            2: deque(),  # Queue 2 (RR with time_quantum2)
            3: deque(),  # Queue 3 (Priority 1 - RR)
            4: deque(),  # Queue 4 (Priority 2 - RR)
            5: deque()   # Queue 5 (Priority 3 - RR)
        }
        self.terminated = []
        self.time_quantum1 = tk.IntVar(value=4)
        self.time_quantum2 = tk.IntVar(value=8)
        self.current_time = tk.IntVar(value=0)
        self.setup_ui()
    
    def setup_ui(self):
        self.root.configure(bg="#e0f7fa")
        
        # Center Frame
        frame = ttk.Frame(self.root)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Time Quantum 1:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ttk.Entry(frame, textvariable=self.time_quantum1, font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Time Quantum 2:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        ttk.Entry(frame, textvariable=self.time_quantum2, font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Process ID:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.pid_entry = ttk.Entry(frame, font=("Arial", 12))
        self.pid_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Arrival Time:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.arrival_entry = ttk.Entry(frame, font=("Arial", 12))
        self.arrival_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="CPU Time:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        self.cpu_entry = ttk.Entry(frame, font=("Arial", 12))
        self.cpu_entry.grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Priority (1-3):", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        self.priority_entry = ttk.Entry(frame, font=("Arial", 12))
        self.priority_entry.grid(row=5, column=1, padx=10, pady=5)
        
        ttk.Button(frame, text="Add Process", command=self.add_process).grid(row=6, column=0, columnspan=2, pady=10)

        self.process_table = ttk.Treeview(frame, columns=("PID", "Arrival", "CPU", "Priority"), show="headings", height=8)
        self.process_table.heading("PID", text="PID")
        self.process_table.heading("Arrival", text="Arrival Time")
        self.process_table.heading("CPU", text="CPU Time")
        self.process_table.heading("Priority", text="Priority")
        self.process_table.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        ttk.Label(frame, text="Time Instance:", font=("Arial", 12)).grid(row=8, column=0, padx=10, pady=5, sticky="ew")
        ttk.Entry(frame, textvariable=self.current_time, font=("Arial", 12)).grid(row=8, column=1, padx=10, pady=5)

        # Buttons in the same row
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        ttk.Button(button_frame, text="Simulate", command=self.simulate).pack(side="left", expand=True, padx=5)
        ttk.Button(button_frame, text="Next Step", command=self.next_step).pack(side="left", expand=True, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(side="right", expand=True, padx=5)

        self.result_text = tk.Text(frame, height=15, width=80, font=("Arial", 12), bg="#ffffff", fg="#000000")
        self.result_text.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    def add_process(self):
        try:
            pid = self.pid_entry.get()
            arrival = int(self.arrival_entry.get())
            cpu = int(self.cpu_entry.get())
            priority = int(self.priority_entry.get())
            if priority not in [1, 2, 3]:
                raise ValueError("Priority must be 1, 2, or 3")
            process = Process(pid, arrival, cpu, priority)
            self.processes.append(process)
            self.process_table.insert("", tk.END, values=(pid, arrival, cpu, priority))
            messagebox.showinfo("Success", f"Process {pid} added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def simulate(self):
        time = self.current_time.get()
        self.run_scheduler(time)
        self.display_queues(time)

    def next_step(self):
        self.current_time.set(self.current_time.get() + 1)
        self.simulate()

    def run_scheduler(self, time):
        # Add arriving processes to queue 1
        for process in self.processes:
            if process.arrival == time and process.queue_level == 1 and process not in self.terminated:
                self.queues[1].append(process)
                process.time_in_current_queue = 0
                process.time_since_last_execution = 0
    
        # Check for aging in priority queues (3-5)
        for queue_num in [3, 4, 5]:
            for process in list(self.queues[queue_num]):
                process.time_since_last_execution += 1
                
                # Check if process needs to be aged up
                if process.time_since_last_execution >= (self.time_quantum1.get() + self.time_quantum2.get()):
                    # Age the process (move to higher priority queue)
                    if queue_num > 3:  # Can't age up from queue 3 (highest priority)
                        new_queue = queue_num - 1
                        self.queues[queue_num].remove(process)
                        process.queue_level = new_queue
                        process.time_in_current_queue = 0
                        process.time_since_last_execution = 0
                        self.queues[new_queue].append(process)
    
        # Execute processes in queue order
        executed_process = None
        for queue_num in [1, 2, 3, 4, 5]:
            if self.queues[queue_num]:
                process = self.queues[queue_num][0]
                executed_process = process
                break
    
        if executed_process:
            # Execute the process for 1 time unit
            executed_process.remaining_cpu -= 1
            executed_process.time_in_current_queue += 1
            executed_process.last_executed_time = time
            executed_process.time_since_last_execution = 0  # Reset aging counter
        
            # Check for completion
            if executed_process.remaining_cpu <= 0:
                self.terminated.append(executed_process)
                self.queues[executed_process.queue_level].popleft()
            else:
                # Check for queue promotion
                if executed_process.queue_level == 1 and executed_process.time_in_current_queue >= self.time_quantum1.get():
                    executed_process.queue_level = 2
                    executed_process.time_in_current_queue = 0
                    self.queues[2].append(self.queues[1].popleft())
                elif executed_process.queue_level == 2 and executed_process.time_in_current_queue >= self.time_quantum2.get():
                    executed_process.queue_level = executed_process.priority + 2
                    executed_process.time_in_current_queue = 0
                    self.queues[executed_process.queue_level].append(self.queues[2].popleft())

    def display_queues(self, time):
        result = f"""Time {time}:
Queue 1 (Q={self.time_quantum1.get()}): {[p.pid for p in self.queues[1]]}
Queue 2 (Q={self.time_quantum2.get()}): {[p.pid for p in self.queues[2]]}
Queue 3 (P1): {[p.pid for p in self.queues[3]]}
Queue 4 (P2): {[p.pid for p in self.queues[4]]}
Queue 5 (P3): {[p.pid for p in self.queues[5]]}
Terminated: {[p.pid for p in self.terminated]}\n"""
    
        # Show currently executing process
        executing = []
        for queue_num in [1, 2, 3, 4, 5]:
            if self.queues[queue_num]:
                process = self.queues[queue_num][0]
                if process.last_executed_time == time:
                    executing.append(f"Executing: {process.pid} in Q{queue_num} (Remaining: {process.remaining_cpu})")
                    break
    
        if not executing:
            executing.append("No process executing")
    
        result += "\n".join(executing) + "\n\nProcess States:\n"
    
        for p in sorted(self.processes, key=lambda x: x.pid):
            status = []
            if p in self.terminated:
                status.append("Terminated")
            elif any(p in q for q in self.queues.values()):
                status.append(f"Q{p.queue_level}")
                if p.queue_level >= 3:
                    status.append(f"Aging: {p.time_since_last_execution}/{(self.time_quantum1.get() + self.time_quantum2.get())}")
            elif p.arrival > time:
                status.append(f"Arrives at {p.arrival}")
            else:
                status.append("Waiting")
        
            status.append(f"{p.remaining_cpu} units left")
            result += f"{p.pid}: {', '.join(status)}\n"
    
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result) 

    def clear_all(self):
        self.processes.clear()
        self.queues = {i: deque() for i in range(1, 6)}
        self.terminated.clear()
        self.process_table.delete(*self.process_table.get_children())
        self.result_text.delete(1.0, tk.END)
        self.current_time.set(0)
        messagebox.showinfo("Cleared", "All processes have been removed!")

root = tk.Tk()
app = MLFQScheduler(root)
root.mainloop()