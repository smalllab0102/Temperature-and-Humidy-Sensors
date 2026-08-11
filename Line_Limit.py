from collections import deque
import time

def keep_lines(file,max_lines = 1500000):
    with open(file, "r") as f:
        first_line = f.readline()
        rest_of_lines = f.readlines()
        total_lines = len(rest_of_lines) + 1
        f.seek(0)
        first_line = f.readline()
    
    if total_lines > max_lines:
        kept_lines = deque(file, maxlen = max_lines-1)

        with open(file, "w") as f:
            f.write(first_line)
            f.writelines(kept_lines)

while True:
    keep_lines("modbus_log.csv", max_lines = 1500000)
    time.sleep(86400)