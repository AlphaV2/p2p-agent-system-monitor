import logging
import threading
import sqlite3
import time

import psutil  # For monitoring CPU, memory, disk usage

from agent.core import P2PAgent
from agent.storage import initialize_database, insert_metrics  # Ensure DB setup before usage
from gui import setup_ui  # Import GUI setup

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the database
initialize_database()

# Create P2P Agent instance
agent = P2PAgent(device_id="3b935cb1-aef8-4c83-ba29-3878be958300")
logger = logging.getLogger('p2p_agent')

logger.info(f"P2P Agent initialized with device ID: {agent.device_id}")

# Collect system specs
specs = agent.collect_system_specs()
logger.info(f"System Specifications: {specs}")

# Function to collect and insert system metrics into the database
def collect_and_insert_metrics():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)  # 1 second interval
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        # Insert the collected data into the database
        insert_metrics(cpu_usage, memory_usage, disk_usage, agent.device_id)
        logger.info(f"Inserted metrics: CPU={cpu_usage}%, Memory={memory_usage}%, Disk={disk_usage}%")

        # Sleep for a while before collecting again (e.g., every 10 seconds)
        time.sleep(10)

# Start the monitoring loop in a separate thread
monitor_thread = threading.Thread(target=collect_and_insert_metrics, daemon=True)
monitor_thread.start()

# Fetch recent metrics
try:
    recent = agent.get_recent_metrics(1)
    if recent:
        logger.info(f"Recent metrics: {recent[0]}")
    else:
        logger.warning("No recent metrics found.")
except sqlite3.OperationalError as e:
    logger.error(f"Database error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")

# Start the GUI in the main thread
setup_ui()  # Launch the Tkinter UI

# Keep the script running to monitor and insert data
while True:
    time.sleep(1)
