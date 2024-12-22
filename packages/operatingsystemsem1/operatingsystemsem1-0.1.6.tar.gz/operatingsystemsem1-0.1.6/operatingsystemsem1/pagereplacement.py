from collections import deque

def fifo_replacement(pages, capacity):
    page_faults = 0
    frames = deque(maxlen=capacity)
    frame_states = []
    fault_list = []
    
    for page in pages:
        is_fault = page not in frames
        if is_fault:
            page_faults += 1
            if len(frames) == capacity:
                frames.popleft()
            frames.append(page)
        fault_list.append('F' if is_fault else 'H')
        frame_states.append(list(frames))
            
    return page_faults, frame_states, fault_list

def lru_replacement(pages, capacity):
    page_faults = 0
    frames = []
    page_usage = {}
    frame_states = []
    fault_list = []
    
    for time, page in enumerate(pages):
        is_fault = page not in frames
        if is_fault:
            page_faults += 1
            if len(frames) == capacity:
                lru_page = min(frames, key=lambda x: page_usage[x])
                frames.remove(lru_page)
            frames.append(page)
        
        page_usage[page] = time
        fault_list.append('F' if is_fault else 'H')
        frame_states.append(list(frames))
            
    return page_faults, frame_states, fault_list

def optimal_replacement(pages, capacity):
    page_faults = 0
    frames = []
    frame_states = []
    fault_list = []
    
    for i, page in enumerate(pages):
        is_fault = page not in frames
        if is_fault:
            page_faults += 1
            if len(frames) == capacity:
                future_usage = {}
                for frame in frames:
                    try:
                        future_usage[frame] = pages[i+1:].index(frame)
                    except ValueError:
                        future_usage[frame] = float('inf')
                
                victim_page = max(frames, key=lambda x: future_usage[x])
                frames.remove(victim_page)
            frames.append(page)
        fault_list.append('F' if is_fault else 'H')
        frame_states.append(list(frames))
            
    return page_faults, frame_states, fault_list

def print_page_table(algorithm_name, pages, frame_states, fault_list):
    print(f"\n{algorithm_name} Page Table:\n")
    
    print("Ref    :", end=" ")
    for page in pages:
        print(f"{page:2}", end=" ")
    print()
        
    print("" + "-" * (len(pages) * 3 + 10))
    
    for frame_idx in range(len(frame_states[-1])):
        print(f"Frame {frame_idx}:", end=" ")
        for state in frame_states:
            if frame_idx < len(state):
                print(f"{state[frame_idx]:2}", end=" ")
            else:
                print(" -", end=" ")
        print()

    print("" + "-" * (len(pages) * 3 + 10))

    print("Status :  ", end="")

    for status in fault_list:
        print(f"{status:2}", end=" ")


pages = [6, 1, 1, 2, 0, 3, 4, 6, 0, 2, 1, 2, 1, 2, 0, 3, 2, 1, 2, 0]
capacity = 3

fifo_faults, fifo_states, fifo_fault_list = fifo_replacement(pages, capacity)
lru_faults, lru_states, lru_fault_list = lru_replacement(pages, capacity)
optimal_faults, optimal_states, optimal_fault_list = optimal_replacement(pages, capacity)

print("Page Reference String:", pages)
print("Number of Frames:", capacity)

print_page_table("FIFO", pages, fifo_states, fifo_fault_list)
print("\n\nFIFO Page Faults:", fifo_faults, end="\n\n")

print_page_table("LRU", pages, lru_states, lru_fault_list)
print("\n\nLRU Page Faults:", lru_faults, end="\n\n")

print_page_table("Optimal", pages, optimal_states, optimal_fault_list)
print("\n\nOptimal Page Faults:", optimal_faults, end="\n\n")