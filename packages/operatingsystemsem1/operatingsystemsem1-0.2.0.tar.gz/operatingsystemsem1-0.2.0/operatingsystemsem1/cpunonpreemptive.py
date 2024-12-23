def print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times):
    print("Gantt Chart:")
    print("P\tAT\tBT\tWT\tTAT\tCT\tRT")
    for i in range(len(processes)):
        print(f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t{wait_times[i]}\t{turn_around_times[i]}\t{completion_times[i]}\t{response_times[i]}")

    print(f"\nAverage Waiting Time: {sum(wait_times) / len(wait_times):.2f}")
    print(f"Average Turnaround Time: {sum(turn_around_times) / len(turn_around_times):.2f}")

def priority_non_preemptive(processes, arrival_times, burst_times, priorities):
    n = len(processes)
    completion_times = [0] * n
    wait_times = [0] * n
    turn_around_times = [0] * n
    response_times = [0] * n
    is_completed = [False] * n

    current_time = 0
    completed = 0

    while completed < n:
        max_priority = -1
        selected = -1
        for i in range(n):
            if arrival_times[i] <= current_time and not is_completed[i]:
                if priorities[i] > max_priority:
                    max_priority = priorities[i]
                    selected = i

        if selected == -1:
            current_time += 1
            continue

        current_time += burst_times[selected]
        completion_times[selected] = current_time
        turn_around_times[selected] = completion_times[selected] - arrival_times[selected]
        wait_times[selected] = turn_around_times[selected] - burst_times[selected]
        response_times[selected] = wait_times[selected]

        is_completed[selected] = True
        completed += 1

    print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times)

processes = ["A", "B", "C", "D"]
arrival_times = [0, 1, 2, 3]
burst_times = [5, 3, 8, 6]
priorities = [3, 2, 1, 4]
time_quantum = 2

print("\n--- Non-Preemptive Priority ---")
priority_non_preemptive(processes, arrival_times, burst_times, priorities)