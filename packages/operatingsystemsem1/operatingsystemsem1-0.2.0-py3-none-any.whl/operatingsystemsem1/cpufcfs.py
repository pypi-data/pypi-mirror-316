def print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times):
    print("Gantt Chart:")
    print("P\tAT\tBT\tWT\tTAT\tCT\tRT")
    for i in range(len(processes)):
        print(f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t{wait_times[i]}\t{turn_around_times[i]}\t{completion_times[i]}\t{response_times[i]}")

    print(f"\nAverage Waiting Time: {sum(wait_times) / len(wait_times):.2f}")
    print(f"Average Turnaround Time: {sum(turn_around_times) / len(turn_around_times):.2f}")

def fcfs(processes, arrival_times, burst_times):
    n = len(processes)
    completion_times = [0] * n
    wait_times = [0] * n
    turn_around_times = [0] * n
    response_times = [0] * n

    completion_times[0] = arrival_times[0] + burst_times[0]
    for i in range(1, n):
        completion_times[i] = max(completion_times[i - 1], arrival_times[i]) + burst_times[i]

    for i in range(n):
        turn_around_times[i] = completion_times[i] - arrival_times[i]
        wait_times[i] = turn_around_times[i] - burst_times[i]
        response_times[i] = wait_times[i]

    print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times)

processes = ["A", "B", "C", "D"]
arrival_times = [0, 1, 2, 3]
burst_times = [5, 3, 8, 6]
priorities = [3, 2, 1, 4]
time_quantum = 2

print("\n--- FCFS ---")
fcfs(processes, arrival_times, burst_times)