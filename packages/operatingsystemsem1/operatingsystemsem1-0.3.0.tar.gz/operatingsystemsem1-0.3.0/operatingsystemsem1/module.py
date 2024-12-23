# os-sem1/module.py

def scan(initial, requests, disk_size, direction):
    requests.sort()
    left = [r for r in requests if r < initial]
    right = [r for r in requests if r >= initial]

    if direction == "up":
        sequence = right + [disk_size - 1] + left[::-1]
    else:
        sequence = left[::-1] + [0] + right

    seek_time = 0
    current = initial
    for pos in sequence:
        seek_time += abs(pos - current)
        current = pos

    print(f"SCAN Order: {sequence}")
    print(f"Total Seek Time: {seek_time}")


requests = [82, 170, 43, 140, 24, 16, 190]
initial = 50
disk_size = 200
direction = "up"

scan(initial, requests, disk_size, direction)










def fifo(pages, frames):
    memory = []
    page_faults = 0

    for page in pages:
        if page not in memory:
            if len(memory) >= frames:
                memory.pop(0)
            memory.append(page)
            page_faults += 1

    return page_faults

def lru(pages, frames):
    memory = []
    page_faults = 0

    for page in pages:
        if page not in memory:
            if len(memory) >= frames:
                memory.pop(-1)
            page_faults += 1
    return

def optimal(pages, frames):
    memory = []
    page_faults = 0

    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                farthest = -1
                victim = -1
                for mem_page in memory:
                    if mem_page not in pages[i+1:]:
                        victim = mem_page
                        break
                    else:
                        idx = pages[i+1:].index(mem_page)
                        if idx > farthest:
                            farthest = idx
                            victim = mem_page
                memory[memory.index(victim)] = page
            page_faults += 1

    return page_faults

# pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
# frames = 3

# print("FIFO Page Faults:", fifo(pages, frames))
# print("LRU Page Faults:", lru(pages, frames))
# print("Optimal Page Faults:", optimal(pages, frames))