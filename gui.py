import tkinter as tk
import psutil
import uuid
import threading
import platform

# Function to get system specs
def get_device_specs():
    device_id = str(uuid.uuid4())  # Unique device ID
    specs = {
        'device_id': device_id,
        'platform': platform.system(),
        'platform_version': platform.version(),
        'processor': platform.processor(),
        'cpu_count': psutil.cpu_count(),
        'total_memory': psutil.virtual_memory().total / (1024 ** 3),  # Convert to GB
        'total_disk': psutil.disk_usage('/').total / (1024 ** 3)  # Convert to GB
    }
    return specs

# Function to update metrics and system specs
def update_metrics(root, cpu_label, memory_label, disk_label, device_id_label, specs_labels):
    # Collect system metrics
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    device_id = get_device_specs()['device_id']

    # Update the labels with the collected data
    device_id_label.config(text=f"Device ID: {device_id}")
    cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
    memory_label.config(text=f"Memory Usage: {memory_usage}%")
    disk_label.config(text=f"Disk Usage: {disk_usage}%")

    # Update the system specs labels
    specs = get_device_specs()
    specs_labels['platform'].config(text=f"Platform: {specs['platform']} {specs['platform_version']}")
    specs_labels['processor'].config(text=f"Processor: {specs['processor']}")
    specs_labels['cpu_count'].config(text=f"CPU Count: {specs['cpu_count']}")
    specs_labels['total_memory'].config(text=f"Total Memory: {specs['total_memory']:.2f} GB")
    specs_labels['total_disk'].config(text=f"Total Disk: {specs['total_disk']:.2f} GB")

    # Call the function every 5 seconds to update the data
    root.after(5000, update_metrics, root, cpu_label, memory_label, disk_label, device_id_label, specs_labels)

# Setup the UI
def setup_ui():
    # Create the main window
    root = tk.Tk()
    root.title("System Performance Monitor")

    # Set the window size and make it resizable
    root.geometry("600x400")
    root.resizable(False, False)

    # Labels to display system information
    device_id_label = tk.Label(root, text="Device ID:", font=("Helvetica", 10))
    device_id_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    cpu_label = tk.Label(root, text="CPU Usage: 0%", font=("Helvetica", 12))
    cpu_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    memory_label = tk.Label(root, text="Memory Usage: 0%", font=("Helvetica", 12))
    memory_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    disk_label = tk.Label(root, text="Disk Usage: 0%", font=("Helvetica", 12))
    disk_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

    # Fetch system specs
    specs = get_device_specs()

    # Display system specifications
    specs_labels = {
        'platform': tk.Label(root, text=f"Platform: {specs['platform']} {specs['platform_version']}", font=("Helvetica", 10)),
        'processor': tk.Label(root, text=f"Processor: {specs['processor']}", font=("Helvetica", 10)),
        'cpu_count': tk.Label(root, text=f"CPU Count: {specs['cpu_count']}", font=("Helvetica", 10)),
        'total_memory': tk.Label(root, text=f"Total Memory: {specs['total_memory']:.2f} GB", font=("Helvetica", 10)),
        'total_disk': tk.Label(root, text=f"Total Disk: {specs['total_disk']:.2f} GB", font=("Helvetica", 10))
    }

    # Place the system specs labels in the UI
    row = 4
    for key, label in specs_labels.items():
        label.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        row += 1

    # Start the UI and update the metrics
    update_metrics(root, cpu_label, memory_label, disk_label, device_id_label, specs_labels)

    # Start the UI loop
    root.mainloop()
