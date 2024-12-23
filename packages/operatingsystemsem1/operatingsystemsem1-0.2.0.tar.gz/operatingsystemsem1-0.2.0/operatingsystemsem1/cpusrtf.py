def print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times):
    print("Gantt Chart:")
    print("P\tAT\tBT\tWT\tTAT\tCT\tRT")
    for i in range(len(processes)):
        print(f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t{wait_times[i]}\t{turn_around_times[i]}\t{completion_times[i]}\t{response_times[i]}")

    print(f"\nAverage Waiting Time: {sum(wait_times) / len(wait_times):.2f}")
    print(f"Average Turnaround Time: {sum(turn_around_times) / len(turn_around_times):.2f}")

def srtf(processes, arrival_times, burst_times):
    n = len(processes)
    remaining_times = burst_times[:]
    completion_times = [0] * n
    wait_times = [0] * n
    turn_around_times = [0] * n
    response_times = [-1] * n

    current_time = 0
    completed = 0

    while completed < n:
        shortest = -1
        min_time = float('inf')
        for i in range(n):
            if arrival_times[i] <= current_time and remaining_times[i] > 0:
                if remaining_times[i] < min_time or (remaining_times[i] == min_time and arrival_times[i] < arrival_times[shortest]):
                    shortest = i
                    min_time = remaining_times[i]

        if shortest == -1:
            current_time += 1
            continue

        if response_times[shortest] == -1:
            response_times[shortest] = current_time - arrival_times[shortest]

        current_time += 1
        remaining_times[shortest] -= 1

        if remaining_times[shortest] == 0:
            completed += 1
            completion_times[shortest] = current_time

    for i in range(n):
        turn_around_times[i] = completion_times[i] - arrival_times[i]
        wait_times[i] = turn_around_times[i] - burst_times[i]

    print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times)


processes = ["A", "B", "C", "D"]
arrival_times = [0, 1, 2, 3]
burst_times = [5, 3, 8, 6]

print("\n--- SRTF ---")
srtf(processes, arrival_times, burst_times)