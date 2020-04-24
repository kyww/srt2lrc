#!/usr/bin/env python3

# LRC Sample: 
# [00:07.63] blahblah...

from datetime import datetime
import sys

TIME_FORMAT = "%M:%S.%f"

def parse_time(t):
    return datetime.strptime(t, TIME_FORMAT)

def process_file(filename):
    line_list = []
    time_offset = None

    with open(filename) as f:
        for line in f.readlines():
            start = line.find('[')
            end = line.find(']')
            if start == -1 or end == -1:
                line_list.append(line)
                continue

            t = line[start + 1:end]
            dt = parse_time(t)
            new_dt = None
            if time_offset == None:
                t = '00:00.00'
                time_offset = dt - parse_time(t)
            else:
                new_dt = dt - time_offset
                t = datetime.strftime(new_dt, TIME_FORMAT)[:-4]

            line = line[:start + 1] + t + line[end:]
            line_list.append(line)

    with open(filename, 'w') as f:
        f.write(''.join(line_list))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage:\n  {} [LRC_FILE]...\n\n  Adjust LRC timestamp to start from 00:00.00".format(sys.argv[0]))

    for filename in sys.argv[1:]:
        process_file(filename)
