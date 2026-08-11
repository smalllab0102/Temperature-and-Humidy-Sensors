import csv
import os
import time
from datetime import datetime
from pymodbus.client import ModbusTcpClient

# --- CONFIGURATION ---
SERVER_IP = "192.168.2.3"  # <-- DOUBLE-CHECK THIS IP MATCHES YOUR DEVICE
SERVER_PORT = 502
UNIT_ID = 1
LOG_FILE = "modbus_log.csv"

HEADERS = [
    "Timestamp", "Temp F", "Temp C", "Humidity", 
    "Year", "Month", "Day", "Day of Week", "Hour", "Minute", "Second"
]

def initialize_csv():
    """Creates the log file with headers if it doesn't exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
        print(f"Created new log file: {LOG_FILE}")

def read_modbus_block(client, start_address, count):
    """Safely reads a sequential block of Modbus registers."""
    try:
        response = client.read_holding_registers(
            address=start_address, count=count, slave=UNIT_ID
        )
        if response is None or response.isError():
            return None
        return response.registers
    except Exception:
        return None

def log_data(client):
    """Polls Modbus data, scales specific values, and logs to CSV."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Read data blocks from device
    block1 = read_modbus_block(client, 100, 2)
    block2 = read_modbus_block(client, 304, 1)
    block3 = read_modbus_block(client, 1239, 7)

    # Start building row data
    row = [timestamp]

    # Process addresses 100 & 101 (Move decimal over by 1)
    if block1 and len(block1) >= 2:
        val_100 = block1[0] / 10.0
        val_101 = block1[1] / 10.0
        row.extend([val_100, val_101])
    else:
        row.extend(["NaN", "NaN"])

    # Process address 304 (Move decimal over by 1)
    if block2 and len(block2) >= 1:
        val_304 = block2[0] / 10.0
        row.extend([val_304])
    else:
        row.extend(["NaN"])

    # Process addresses 1239-1245 (Keep as raw integers)
    if block3 and len(block3) >= 7:
        row.extend(block3)
    else:
        row.extend(["NaN"] * 7)

    # Append data to file
    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)
        
    print(f"[{timestamp}] Data logged. Success states: B1={block1 is not None}, B2={block2 is not None}, B3={block3 is not None}")

def main():
    initialize_csv()
    
    # Safely create the client object first so it always exists
    client = ModbusTcpClient(SERVER_IP, port=SERVER_PORT)
    
    print(f"Connecting to {SERVER_IP}:{SERVER_PORT} and logging data...")

    try:
        while True:
            # Check connection and try to connect if offline
            if not client.connected:
                print(f"Attempting connection to {SERVER_IP}...")
                client.connect()
                
            if client.connected:
                log_data(client)
            else:
                print("Device unreachable. Retrying in 5 seconds...")
                # Log an all-NaN row to preserve time continuity if desired,
                # or quietly wait. Here we just wait:
                
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nStopping logging script...")
    finally:
        # This will now always execute safely without UnboundLocalError
        if client:
            client.close()
            print("Connection closed safely.")

if __name__ == "__main__":
    main()