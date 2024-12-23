def print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times):
    print("Gantt Chart:")
    print("P\tAT\tBT\tWT\tTAT\tCT\tRT")
    for i in range(len(processes)):
        print(f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t{wait_times[i]}\t{turn_around_times[i]}\t{completion_times[i]}\t{response_times[i]}")

    print(f"\nAverage Waiting Time: {sum(wait_times) / len(wait_times):.2f}")
    print(f"Average Turnaround Time: {sum(turn_around_times) / len(turn_around_times):.2f}")
    
def non_preemptive_priority_round_robin(processes, arrival_times, burst_times, priorities, time_quantum):
    n = len(processes)
    remaining_times = burst_times[:]
    completion_times = [0] * n
    wait_times = [0] * n
    turn_around_times = [0] * n
    response_times = [-1] * n

    current_time = 0
    queue = []
    
    sorted_processes = sorted(range(n), key=lambda x: (priorities[x], arrival_times[x]))
    
    for process_index in sorted_processes:
        if arrival_times[process_index] <= current_time:
            queue.append(process_index)

    while queue:
        process_index = queue.pop(0)
        if response_times[process_index] == -1:
            response_times[process_index] = current_time - arrival_times[process_index]
        
        if remaining_times[process_index] > time_quantum:
            current_time += time_quantum
            remaining_times[process_index] -= time_quantum
            queue.append(process_index)
        else:
            current_time += remaining_times[process_index]
            completion_times[process_index] = current_time
            remaining_times[process_index] = 0

    for i in range(n):
        turn_around_times[i] = completion_times[i] - arrival_times[i]
        wait_times[i] = turn_around_times[i] - burst_times[i]
    
    print_gantt_chart(processes, arrival_times, burst_times, wait_times, turn_around_times, completion_times, response_times)

processes = ["A", "B", "C", "D"]
arrival_times = [0, 1, 2, 3]
burst_times = [5, 3, 8, 6]
time_quantum = 2
priorities = [1, 1, 2, 2]

non_preemptive_priority_round_robin(processes, arrival_times, burst_times, time_quantum, priorities)