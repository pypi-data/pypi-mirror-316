def print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times):
    print("Gantt Chart:")
    print("P\tAT\tBT\tWT\tTAT\tCT\tRT")
    for i in range(len(processes)):
        print(f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t{wait_times[i]}\t{turn_around_times[i]}\t{completion_times[i]}\t{response_times[i]}")

    print(f"\nAverage Waiting Time: {sum(wait_times) / len(wait_times):.2f}")
    print(f"Average Turnaround Time: {sum(turn_around_times) / len(turn_around_times):.2f}")

def priority_preemptive(processes, arrival_times, burst_times, priorities):
    n = len(processes)
    remaining_times = burst_times[:]
    completion_times = [0] * n
    wait_times = [0] * n
    turn_around_times = [0] * n
    response_times = [-1] * n

    current_time = 0
    completed = 0

    while completed < n:
        highest_priority = float('-inf')
        selected = -1
        for i in range(n):
            if arrival_times[i] <= current_time and remaining_times[i] > 0:
                if priorities[i] > highest_priority or (priorities[i] == highest_priority and arrival_times[i] < arrival_times[selected]):
                    highest_priority = priorities[i]
                    selected = i

        if selected == -1:
            current_time += 1
            continue

        if response_times[selected] == -1:
            response_times[selected] = current_time - arrival_times[selected]

        remaining_times[selected] -= 1
        current_time += 1

        if remaining_times[selected] == 0:
            completed += 1
            completion_times[selected] = current_time

    for i in range(n):
        turn_around_times[i] = completion_times[i] - arrival_times[i]
        wait_times[i] = turn_around_times[i] - burst_times[i]

    print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times)

processes = ["A", "B", "C", "D"]
arrival_times = [0, 1, 2, 3]
burst_times = [5, 3, 8, 6]
priorities = [3, 2, 1, 4]
time_quantum = 2

print("\n--- Preemptive Priority ---")
priority_preemptive(processes, arrival_times, burst_times, priorities)