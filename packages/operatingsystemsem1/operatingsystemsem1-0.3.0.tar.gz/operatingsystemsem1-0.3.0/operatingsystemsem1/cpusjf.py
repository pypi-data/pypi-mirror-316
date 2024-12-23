def print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times):
    print("Gantt Chart:")
    print("P\tAT\tBT\tWT\tTAT\tCT\tRT")
    for i in range(len(processes)):
        print(f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t{wait_times[i]}\t{turn_around_times[i]}\t{completion_times[i]}\t{response_times[i]}")

    print(f"\nAverage Waiting Time: {sum(wait_times) / len(wait_times):.2f}")
    print(f"Average Turnaround Time: {sum(turn_around_times) / len(turn_around_times):.2f}")

def sjf(processes, arrival_times, burst_times):
    n = len(processes)
    remaining_times = burst_times[:]
    completion_times = [0] * n
    wait_times = [0] * n
    turn_around_times = [0] * n
    response_times = [0] * n

    completed = 0
    current_time = 0
    is_completed = [False] * n

    while completed < n:
        shortest = -1
        min_burst = float('inf')
        for i in range(n):
            if arrival_times[i] <= current_time and not is_completed[i] and burst_times[i] < min_burst:
                shortest = i
                min_burst = burst_times[i]

        if shortest == -1:
            current_time += 1
            continue

        current_time += burst_times[shortest]
        completion_times[shortest] = current_time
        turn_around_times[shortest] = completion_times[shortest] - arrival_times[shortest]
        wait_times[shortest] = turn_around_times[shortest] - burst_times[shortest]
        response_times[shortest] = wait_times[shortest]

        is_completed[shortest] = True
        completed += 1

    print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times)

processes = ["A", "B", "C", "D"]
arrival_times = [0, 1, 2, 3]
burst_times = [5, 3, 8, 6]

print("\n--- SJF ---")
sjf(processes, arrival_times, burst_times)