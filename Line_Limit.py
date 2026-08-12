import os
import tempfile
import time

file = 'modbus_log.csv'
max_size = 35242
print('Checking for Max Size')

while True:
    #checks if file is over max file size
    if os.path.getsize(file) > max_size:
        with open(file, 'r') as f:
            lines = f.readlines()
            first_line = lines[1].strip()
            oldest_date = first_line[:10]
            
            #finds lines we want to keep
            new_line = 0
            for i, line in enumerate(lines):
                if i==0:
                    continue
                if not line.startswith(oldest_date):
                    new_line = i
                    break
            keep_lines = [lines[0]] + lines[new_line:]

            #makes a temporary file to write the new lines to and then makes that our new file
            with open(file, 'w', newline='') as f:
                f.writelines(keep_lines)
    time.sleep(60)