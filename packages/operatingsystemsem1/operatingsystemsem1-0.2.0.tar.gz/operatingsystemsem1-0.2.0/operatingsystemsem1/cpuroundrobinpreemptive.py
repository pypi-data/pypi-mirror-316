def print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times):
    print("Gantt Chart:")
    print("P\tAT\tBT\tWT\tTAT\tCT\tRT")
    for i in range(len(processes)):
        print(f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t{wait_times[i]}\t{turn_around_times[i]}\t{completion_times[i]}\t{response_times[i]}")

    print(f"\nAverage Waiting Time: {sum(wait_times) / len(wait_times):.2f}")
    print(f"Average Turnaround Time: {sum(turn_around_times) / len(turn_around_times):.2f}")
    
def preemptive_priority_round_robin(processes, arrival_times, burst_times, time_quantum, priorities):
    n = len(processes)
    remaining_times = burst_times[:]
    completion_times = [0] * n
    wait_times = [0] * n
    turn_around_times = [0] * n
    response_times = [-1] * n

    current_time = 0
    queue = []
    visited = [False] * n
    completed = 0

    # Combine processes based on priority
    while completed < n:
        # Find the process with the highest priority (lowest priority number) and not completed
        highest_priority_process = None
        for i in range(n):
            if arrival_times[i] <= current_time and remaining_times[i] > 0:
                if highest_priority_process is None or priorities[i] < priorities[highest_priority_process]:
                    highest_priority_process = i

        if highest_priority_process is None:
            current_time += 1
            continue

        # If a process is found, check if it's the first time it's being processed
        process_index = highest_priority_process
        if response_times[process_index] == -1:
            response_times[process_index] = current_time - arrival_times[process_index]

        # Execute the process using Round-Robin if it shares the same priority
        if remaining_times[process_index] > time_quantum:
            current_time += time_quantum
            remaining_times[process_index] -= time_quantum
        else:
            current_time += remaining_times[process_index]
            completion_times[process_index] = current_time
            remaining_times[process_index] = 0
            completed += 1

    for i in range(n):
        turn_around_times[i] = completion_times[i] - arrival_times[i]
        wait_times[i] = turn_around_times[i] - burst_times[i]

    print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times)

processes = ["A", "B", "C", "D"]
arrival_times = [0, 1, 2, 3]
burst_times = [5, 3, 8, 6]
time_quantum = 2
priorities = [1, 1, 2, 2]

print("\n--- Preemptive Round Robin ---")
preemptive_priority_round_robin(processes, arrival_times, burst_times, time_quantum, priorities)
