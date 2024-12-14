import sys
from scenarios import *
from agent import Agent
from visualize_world import visualize_world
from utils import get_direction, is_facing_wampa

def fit_grid(grid, item):
    """Used for calculating breeze and stench locationsbased on pit and wampa
    locations."""
    grid_x, grid_y = grid
    x, y = item
    loc = []

    if x < grid_x - 1:
        loc += [[x+1, y]]
    if x > 0:
        loc += [[x-1, y]]
    if y < grid_y - 1:
        loc += [[x, y+1]]
    if y > 0:
        loc += [[x, y-1]]

    return loc

# ENVIRONMENT
class WampaWorld:
    def __init__(self, worldInit):
        self.gridsize = worldInit['grid']
        self.X = self.gridsize[0]
        self.Y = self.gridsize[1]
        self.wampa = worldInit['wampa']
        self.pits = worldInit['pits']
        self.luke = worldInit['luke']
        self.wampaAlive = True
        self.is_playing = True

        # calculate breeze and stench locations
        breeze = []
        for pit in self.pits:
            breeze += fit_grid(self.gridsize, pit)
        stench = fit_grid(self.gridsize, self.wampa)

        # prepopulate grid with percepts
        self.grid = [
            [
                [
                    "stench" if [x, y] in stench else None,
                    "breeze" if [x, y] in breeze else None,
                    None,  # "gasp" index
                    None,  # "bump" index
                    None   # "scream" index
                ]
                for y in range(self.Y)
            ]
            for x in range(self.X)
        ]

        # set "gasp" percept at Luke's location
        self.grid[self.luke[0]][self.luke[1]][2] = "gasp"
        self.agent = Agent(self)

    def get_percepts(self):
        x, y = self.agent.loc
        return self.grid[x][y]

    def take_action(self, action):
        x, y = self.agent.loc
        self.agent.score -= 1

        #R2 moves forward from whatever direction he's facing
        if action == "forward":
            moved = True
            orientation = get_direction(self.agent.degrees)
            movements = {
                "up": (0, 1),
                "down": (0, -1),
                "left": (-1, 0),
                "right": (1, 0)
            }

            dx, dy = movements.get(orientation, (0, 0))
            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < len(self.grid) and 0 <= new_y < len(self.grid[0]):
                self.agent.loc = (new_x, new_y)
            else:
                moved = False

            if (self.get_location() == self.wampa and self.wampaAlive) or \
                self.get_location() in self.pits:
                self.agent.score -= 1000
                print("R2-D2 has been crushed, -1000 points")
                print("Your final score is: ", self.agent.score)
                self.is_playing = False
            
            percepts = self.get_percepts()
            percepts[3] = "bump" if not moved else None  # reset bump = None if no bump

        #R2 turns left
        elif action == "left":
            self.agent.turn_left()
            percepts = self.get_percepts()
            percepts[3] = None  # cannot experience a bump upon a turn

        #R2 turns right
        elif action == "right":
            self.agent.turn_right()
            percepts = self.get_percepts()
            percepts[3] = None  # cannot experience a bump upon a turn

        #R2 fires his blaster
        elif action == "shoot":
            if self.agent.blaster:
                self.agent.blaster = False
                if is_facing_wampa(self.agent):
                    self.wampaAlive = False
                    self.wampa = None
                    for x in range(self.gridsize[0]):
                        for y in range(self.gridsize[1]):
                            self.grid[x][y][4] = "scream"  # scream everywhere
                            self.grid[x][y][0] = None  # stench is gone
                print("Blaster bolt was shot")
            print("No more blaster bolts available")

        #R2 grabs Luke
        elif action == "grab":
            if self.get_location() == self.luke and not self.agent.has_luke:
                self.agent.has_luke = True
                self.luke = None
                print("R2-D2 has picked up Luke")
            elif self.agent.has_luke:
                print("R2 already has Luke")
            else:
                print("R2 cannot pick up Luke here")

        #R2 climbs out
        elif action == "climb":
            if self.agent.has_luke and self.agent.loc == (0, 0):
                self.agent.score += 1000
                print("Congrats! R2 has saved Luke! +1000 points!")
                print("Your final score is: ", self.agent.score)
                self.is_playing = False
            else:
                print("Climb requirements are not met yet")

        else:
            raise ValueError("R2-D2 can only move Forward, turn Left, turn \
                             Right, Shoot, Grab, or Climb.")
    
    def get_location(self):
        x, y = self.agent.loc
        return [x, y]

# RUN THE GAME
def run_game(scenario):
    w = WampaWorld(scenario)
    while w.is_playing:
        visualize_world(w)
        w.agent.record_percepts(w.get_percepts())
        w.agent.inference_algorithm()
        action = w.agent.choose_next_action()
        w.take_action(action)
    return w.agent.score, w.agent.has_luke, w.agent.loc


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 wampa_world.py <scenario>")
        quit()
    
    scenario_name = sys.argv[1]

    try:
        scenario = eval(scenario_name)
    except:
        print(f"Scenario {scenario_name} not found.")
        quit()

    run_game(scenario)

if __name__ == "__main__":
    main()