def flatten(tup):
    """This may help flatten the output of itertools.combinations()
    into a tuple. You may find that you don't need it!"""
    if len(tup) == 1:
        return tup[0]
    return tup

def get_direction(degrees):
    fraction = (degrees % 360) / 360
    orientation = None
    match fraction:
        case 0:
            orientation = "up"
        case 0.25:
            orientation = "right"
        case 0.5:
            orientation = "down"
        case 0.75:
            orientation = "left"
    return orientation

def is_facing_wampa(agent):
    """You may wish to use this in all_safe_next_actions"""
    if not agent.KB.wampa:
        return False
    x, y = agent.loc
    wx, wy = agent.KB.wampa
    direction = get_direction(agent.degrees)
    return (direction == "up" and wx == x and wy > y) or \
            (direction == "down" and wx == x and wy < y) or \
            (direction == "left" and wx < x and wy == y) or \
            (direction == "right" and wx > x and wy == y)