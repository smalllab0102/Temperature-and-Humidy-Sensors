from collections import deque

def keep_lines(file,max_lines = 1500000):
    with open(file, "r") as file:
        kept_lines = deque(file, maxlen = max_lines)

    with open(file, "w") as file:
        file.writelines(kept_lines)

keep_lines("modbus_log.csv", max_lines = 1500000)