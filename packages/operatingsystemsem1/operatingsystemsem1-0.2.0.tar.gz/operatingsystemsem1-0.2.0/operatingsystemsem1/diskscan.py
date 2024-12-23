def scan(requests, head_start, total_tracks, direction="right"):
    sequence = []
    total_movement = 0
    current_head = head_start
    remaining = sorted(requests)
    
    print("\nSCAN Disk Scheduling")
    print("-------------------")
    print("Direction:", direction)
    print("Sequence:", end=" ")
    
    if direction == "right":
        for request in [r for r in remaining if r >= current_head]:
            movement = abs(request - current_head)
            total_movement += movement
            current_head = request
            sequence.append(request)
            print(request, end=" ")
        
        if current_head < total_tracks - 1:
            total_movement += (total_tracks - 1 - current_head)
            current_head = total_tracks - 1
            print(total_tracks - 1, end=" ")
        
        for request in [r for r in remaining if r < head_start][::-1]:
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

scan(requests.copy(), head_start, total_tracks, "right")