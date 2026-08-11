from collections import deque

def keep_lines(file,max_lines = 50):
    with open(file, "r") as f:
        first_line = f.readline()
        rest_of_lines = f.readlines()
        total_lines = len(rest_of_lines + 1)
    
    if total_line < max_lines:
        kept_lines = deque(file, maxlen = max_lines-1)

        with open(file, "w") as f:
            f.write(first_line)
            f.writelines(kept_lines)

keep_lines("modbus_log.csv", max_lines = 50)