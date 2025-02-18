import sqlite3
import psutil
import uuid
import platform
import logging
import time
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database file path
DB_PATH = 'p2p_agent.db'

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the table if it does not exist (removed default timestamp)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY,
            cpu_usage REAL,
            memory_usage REAL,
            disk_usage REAL,
            device_id TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()
    logger.info("Database and table initialized.")

def insert_metrics(cpu_usage, memory_usage, disk_usage, device_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Generate current timestamp using Python
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Insert metrics with explicit timestamp
    cursor.execute(''' 
        INSERT INTO metrics (cpu_usage, memory_usage, disk_usage, device_id, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (cpu_usage, memory_usage, disk_usage, device_id, timestamp))
    
    conn.commit()
    conn.close()
    logger.info(f"Inserted metrics: CPU={cpu_usage}%, Memory={memory_usage}%, Disk={disk_usage}%, Timestamp={timestamp}")

def collect_system_metrics():
    # Collect system metrics
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    device_id = str(uuid.uuid4())  # You can change this to a fixed value if required
    logger.info(f"System Metrics: CPU={cpu_usage}%, Memory={memory_usage}%, Disk={disk_usage}%")
    return cpu_usage, memory_usage, disk_usage, device_id

if __name__ == "__main__":
    initialize_database()

    # Collect and insert metrics every 10 seconds (or whatever interval you want)
    try:
        while True:
            cpu, memory, disk, device_id = collect_system_metrics()
            insert_metrics(cpu, memory, disk, device_id)
            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("Script interrupted by user.")
