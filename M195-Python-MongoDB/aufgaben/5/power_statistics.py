import psutil
import datetime
import time
from pymongo import MongoClient

class Power:
    def __init__(self, cpu=None, ram_total=None, ram_used=None, timestamp=None):
        if cpu is None or ram_total is None or ram_used is None or timestamp is None:
            self.cpu = psutil.cpu_percent(interval=1)
            self.ram_total = psutil.virtual_memory().total
            self.ram_used = psutil.virtual_memory().used
            self.timestamp = datetime.datetime.now()
        else:
            self.cpu = cpu
            self.ram_total = ram_total
            self.ram_used = ram_used
            self.timestamp = timestamp

    def to_dict(self):
        return {
            "cpu": self.cpu,
            "ram_total": self.ram_total,
            "ram_used": self.ram_used,
            "timestamp": self.timestamp
        }

def log_power_stats():
    client = MongoClient("mongodb://localhost:27017")
    db = client["power_stats"]
    collection = db["logs"]

    power = Power()
    collection.insert_one(power.to_dict())


    total_logs = collection.count_documents({})
    if total_logs > 10000:
        to_delete = total_logs - 10000
        old_logs = collection.find().sort("timestamp", 1).limit(to_delete)
        for log in old_logs:
            collection.delete_one({"_id": log["_id"]})

    client.close()


def main():
    while True:
        log_power_stats()
        time.sleep(1)

if __name__ == "__main__":
    main()
