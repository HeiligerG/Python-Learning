from pymongo import MongoClient
import matplotlib.pyplot as plt

def visualize_data():
    client = MongoClient("mongodb://localhost:27017")
    db = client["power_stats"]
    collection = db["logs"]

    logs = list(collection.find().sort("timestamp", 1))

    if not logs:
        print("Keine daten vorhanden")
        return

    timestamps = [log["timestamp"] for log in logs]
    cpu_values = [log["cpu"] for log in logs]
    ram_used = [log["ram_used"] / (1024 ** 3) for log in logs]

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, cpu_values, label="CPU %", color="blue")
    plt.plot(timestamps, ram_used, label="RAM verwendet (GB)", color="green")
    plt.xlabel("Zeit")
    plt.ylabel("Nutzung")
    plt.title("Systemauslastung")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

  
    plt.show()

   
    plt.savefig("systemauslastung.png")
    print("Grafik wurde als png gespeichert")

    client.close()

if __name__ == "__main__":
    visualize_data()
