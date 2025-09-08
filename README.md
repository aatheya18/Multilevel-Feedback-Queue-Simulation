# Multilevel-Feedback-Queue-Scheduler-Simulation

# Project Overview
This project is a simulation of a Multilevel Feedback Queue (MLFQ) Scheduler, implemented in Python with a graphical user interface (GUI) built using Tkinter. The primary goal is to provide a visual and interactive tool for understanding how an operating system manages CPU scheduling.

The scheduler simulates the dynamic movement of processes between multiple priority queues based on their execution history. This approach demonstrates key concepts of process management, such as preventing starvation and ensuring fairness among different types of processes.

This project was developed for the Operating Systems course (2CS506CC23) at Nirma University by Aadhiya Hirani and Dhruva Kothari, under the guidance of Dr. Parita Oza.

# Features
The simulation includes the following key features:
- Multilevel Queues: The scheduler manages five distinct queues, each with its own scheduling policy. Processes start in a higher-priority queue and move to lower-priority queues if they do not complete their execution within a specified time quantum.
- Dynamic Priority Adjustment: The MLFQ algorithm dynamically adjusts the priority of processes, ensuring that short processes are completed quickly while longer processes are not starved of CPU time.
- Interactive GUI: The Tkinter-based user interface allows for:
-- Adding new processes with custom attributes (PID, arrival time, CPU burst time, priority).
-- Viewing process status in real time.
-- Step-by-step simulation of the scheduling process.
-- Clearing all processes to restart the simulation.
- Process Representation: Each process is represented as an object with detailed attributes, including PID, arrival time, CPU burst time, priority, and current queue level.

#Implementation Details
The project is structured with three core components:

- Process Class: Defines the data structure for a process, managing its state and attributes.
- MLFQScheduler Class: Contains the core logic for the scheduling algorithm, handling queue management, process execution, and priority adjustments.
- Tkinter GUI: Provides the interactive front-end, allowing users to control and observe the simulation.

# How to Run
Ensure you have Python installed on your system.
The project uses the built-in tkinter library, so no additional installations are required.
Run the Python script directly.

# Future Scope
The project can be enhanced with the following features:
- Visual Queue Representation: A graphical visualization of processes moving between queues would make the simulation even more intuitive.
- Performance Metrics: Add key performance indicators such as average wait time, turnaround time, and CPU utilization.
- Advanced Algorithms: Implement other CPU scheduling algorithms (e.g., Shortest Job Next, Priority Scheduling) for comparative analysis.
