from utils import get_direction

SPACING = 2

def visualize_world(world):
    r2d2_location = world.agent.loc
    r2d2_direction = get_direction(world.agent.degrees)
    grid_size = world.gridsize
    wampa = world.wampa
    pits = world.pits
    luke = world.luke
    safe_rooms = world.agent.KB.safe_rooms
    
    dir_symbols = {'left': '<', 'right': '>', 'up': '^', 'down': 'v'}
    
    # Create an empty grid
    grid = [['.' for _ in range(grid_size[0])] for _ in range(grid_size[1])]

    # Place safe rooms. Use this to visualize whether your inference algorithm
    # is correctly inferring room safety.
    # for room in safe_rooms:
    #     if 0 <= room[1] < grid_size[1] and 0 <= room[0] < grid_size[0]:
    #         grid[room[1]][room[0]] = 's'
    
    # Place Wampa
    if wampa:
        grid[wampa[1]][wampa[0]] = 'W'
    
    # Place pits
    for pit in pits:
        grid[pit[1]][pit[0]] = 'P'
    
    # Place Luke
    if luke:
        grid[luke[1]][luke[0]] = 'L'
    
    # Place R2D2
    grid[r2d2_location[1]][r2d2_location[0]] = dir_symbols[r2d2_direction]

    grid.reverse()
    print("\n" * SPACING)
    for row in grid:
        print(' '.join(row))
