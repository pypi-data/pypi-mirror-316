def fcfs(requests, head_start, total_tracks):
    sequence = []
    total_movement = 0
    current_head = head_start
    
    print("\nFCFS Disk Scheduling")
    print("-------------------")
    print("Sequence:", end=" ")
    
    for request in requests:
        movement = abs(request - current_head)
        total_movement += movement
        current_head = request
        sequence.append(request)
        print(request, end=" ")
    
    print("\nTotal head movement:", total_movement)
    print("Average head movement:", round(total_movement/len(requests), 2))
    return sequence, total_movement

requests = [45, 21, 67, 90, 4, 89, 52, 61, 87, 25]
head_start = 50
total_tracks = 100

print("Input Values:")
print("Request sequence:", requests)
print("Initial head position:", head_start)
print("Total tracks:", total_tracks)

fcfs(requests.copy(), head_start, total_tracks)