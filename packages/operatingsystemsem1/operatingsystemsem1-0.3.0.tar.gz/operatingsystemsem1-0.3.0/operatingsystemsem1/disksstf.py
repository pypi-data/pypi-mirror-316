def sstf(requests, head_start, total_tracks):
    sequence = []
    total_movement = 0
    current_head = head_start
    remaining = requests.copy()
    
    print("\nSSTF Disk Scheduling")
    print("-------------------")
    print("Sequence:", end=" ")
    
    while remaining:
        closest = min(remaining, key=lambda x: abs(x - current_head))
        movement = abs(closest - current_head)
        total_movement += movement
        current_head = closest
        remaining.remove(closest)
        sequence.append(closest)
        print(closest, end=" ")
    
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

sstf(requests.copy(), head_start, total_tracks)