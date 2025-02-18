import sqlite3
import logging
import platform
import psutil
import time
from agent.storage import initialize_database

# Set up logging
logger = logging.getLogger('p2p_agent')

class P2PAgent:
    def __init__(self, device_id):
        self.device_id = device_id

        # Initialize database and create connection
        initialize_database()  # Ensure table exists
        self.db_conn = sqlite3.connect("p2p_agent.db", check_same_thread=False)  # Open connection

    def collect_system_specs(self):
        """ Collect system specifications """
        specs = {
            "device_id": self.device_id,
            "platform": platform.system(),
            "platform_version": platform.version(),
            "processor": platform.processor(),
            "hostname": platform.node(),
            "cpu_count_physical": psutil.cpu_count(logical=False),
            "cpu_count_logical": psutil.cpu_count(logical=True),
            "total_memory": psutil.virtual_memory().total,
            "total_disk": psutil.disk_usage("/").total
        }
        return specs

    def monitor_loop(self):
        """ Continuously monitor and store system metrics """
        while True:
            try:
                cpu_usage = psutil.cpu_percent(interval=1)
                memory_usage = psutil.virtual_memory().percent
                disk_usage = psutil.disk_usage("/").percent

                # Store metrics
                self.store_metrics(cpu_usage, memory_usage, disk_usage)

                time.sleep(5)  # Adjust monitoring interval
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")

    def store_metrics(self, cpu, memory, disk):
        """ Store collected metrics in the database """
        try:
            cursor = self.db_conn.cursor()
            cursor.execute(
                "INSERT INTO metrics (cpu_usage, memory_usage, disk_usage, device_id) VALUES (?, ?, ?, ?)",
                (cpu, memory, disk, self.device_id),
            )
            self.db_conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database error while inserting metrics: {e}")

    def get_recent_metrics(self, limit=1):
        """ Retrieve recent metrics """
        try:
            cursor = self.db_conn.cursor()
            cursor.execute(f"SELECT * FROM metrics ORDER BY timestamp DESC LIMIT {limit}")
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            return []
