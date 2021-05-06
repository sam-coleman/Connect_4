import matplotlib.pyplot as plt
from statistics import mean

if __name__=="__main__":
    times = []
    for line in open('connect4cks_output.txt','r'):
        if len(line) > 0:
            line = line.split(')')
            for entry in line:
                if entry != '':
                    entry_format = entry.strip('(').split(',')
                    move_num = int(entry_format[0])
                    time = float(entry_format[1])
                    if len(times) >= move_num:
                        times[move_num-1].append(time)
                    else: 
                        times.append([time])
    avg_time = []
    for time in times:
        avg_time.append(mean(time))

plt.plot(avg_time)
plt.xlabel('move number')
plt.ylabel('time (s)')
plt.title(f"Average time per move for {len(times[0])} games at depth 4")
plt.show()

