from random import shuffle
from itertools import combinations
from utils import flatten, get_direction, is_facing_wampa


# KNOWLEDGE BASE
class KB:
    def __init__(self, agent):
        self.all_locs = {agent.loc}  # set of rooms that are known to exist
        self.safe_rooms = {agent.loc}  # set of rooms that are known to be safe
        self.visited_rooms = {agent.loc}  # set of visited rooms (x, y)
        self.stench = set()  # set of rooms where stench has been perceived
        self.breeze = set()  # set of rooms where breeze has been perceived
        self.bump = dict()  # {loc: direction} of most recent bump in loc
        self.gasp = False  # True if gasp has been perceived
        self.scream = False  # True if scream has been perceived
        self.walls = set()  # set of rooms (x, y) that are known to be walls
        self.pits = set()  # set of rooms (x, y) that are known to be pits
        self.wampa = None  # room (x, y) that is known to be the Wampa
        self.luke = None  # room (x, y) that is known to be Luke


# AGENT
class Agent:
    def __init__(self, world):
        self.world = world
        self.loc = (0, 0)
        self.score = 0
        self.degrees = 0
        self.blaster = True
        self.has_luke = False
        self.orientation_to_delta = {
            "up": (0, 1),  # (dx, dy)
            "down": (0, -1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        self.KB = KB(self)

    def turn_left(self):
        self.degrees -= 90

    def turn_right(self):
        self.degrees += 90

    def adjacent_locs(self, room):
        """Returns a set of tuples representing all possible adjacent
        locations to 'room'. Use this function to update KB.all_locs."""
        # TODO:
        ...
        pass

    def record_percepts(self, sensed_percepts):
        """Update the percepts in agent's KB with the percepts sensed in the
        current location, and update visited_rooms and update all_locs with
        each adjacent location to the current location (since each adjacent
        location to the current location must exist)."""
        present_percepts = set(p for p in sensed_percepts if p)
        # TODO:
        ...
        pass

    def enumerate_possible_worlds(self):
        """Return the set of all possible worlds, where a possible world is a
        tuple of (pit_rooms, wampa_room), pit_rooms is a frozenset of tuples
        representing possible pit rooms, and wampa_room is a tuple representing
        a possible wampa room.

        Since the goal is to combinatorially enumerate all the possible worlds
        (pit and wampa locations) over the set of rooms that could potentially
        have a pit or a wampa, we first want to find that set. To do that,
        subtract the set of rooms that you know cannot have a pit or wampa from
        the set of all rooms. For example, you know that a room with a wall
        cannot have a pit or wampa. A world with no pits or wampas is
        represented by (frozenset({()}), ())

        Then use itertools.combinations to return the set of possible worlds,
        or all combinations of possible pit and wampa locations.

        You may find the utils.flatten(tup) method useful here for flattening
        wampa_room from a tuple of tuples into a tuple.

        The output of this function will be queried to find the model of the
        query, and will be checked for consistency with the KB
        to find the model of the KB."""
        # TODO:
        ...
        pass

    def pit_room_is_consistent_with_KB(self, pit_room):
        """Return True if the room could be a pit given breeze in KB, False
        otherwise. A room could be a pit if all adjacent rooms that have been
        visited have had breeze perceived in them. A room cannot be a pit if
        any adjacent rooms that have been visited have not had breeze perceived
        in them. This will be used to find the model of the KB."""
        if pit_room == ():  # It is possible that there are no pits
            return not self.KB.breeze  # if no breeze has been perceived yet
        # TODO:
        ...
        pass

    def wampa_room_is_consistent_with_KB(self, wampa_room):
        """Return True if the room could be a wampa given stench in KB, False
        otherwise. A queried wampa room is consistent with the KB if all
        adjacent rooms that have been visited have had stench perceived in them
        and if all rooms with stench are adjacent to the queried room.
        A room cannot be a wampa if any adjacent rooms that have been visited
        have not had stench perceived in them.
        This will be used to find the model of the KB."""
        if wampa_room == ():  # It is possible that there is no Wampa
            return not self.KB.stench  # if no stench has been perceived yet
        # TODO:
        ...
        pass

    def find_model_of_KB(self, possible_worlds):
        """Return the subset of all possible worlds consistent with KB.
        possible_worlds is a set of tuples (pit_rooms, wampa_room),
        pit_rooms is a frozenset of tuples of possible pit rooms,
        and wampa_room is a tuple representing a possible wampa room.
        A world is consistent with the KB if wampa_room is consistent
        and all pit rooms are consistent with the KB."""
        # TODO:
        ...
        pass

    def find_model_of_query(self, query, room, possible_worlds):
        """Where query can be "pit_in_room", "wampa_in_room", "no_pit_in_room"
        or "no_wampa_in_room", filter the set of possible worlds
        according to the query and room."""
        # TODO:
        ...
        pass

    def infer_wall_locations(self):
        """If a bump is perceived, infer wall locations along the entire known
        length of the room."""
        if not self.KB.bump:
            return
        room, orientation = self.KB.bump.popitem()
        dx, dy = self.orientation_to_delta[orientation]

        min_x = min(self.KB.all_locs, key=lambda loc: loc[0])[0]
        max_x = max(self.KB.all_locs, key=lambda loc: loc[0])[0]
        min_y = min(self.KB.all_locs, key=lambda loc: loc[1])[1]
        max_y = max(self.KB.all_locs, key=lambda loc: loc[1])[1]
        _min = {"up": min_x, "down": min_x, "left": min_y, "right": min_y}
        _max = {"up": max_x, "down": max_x, "left": max_y, "right": max_y}

        for i in range(_min[orientation], _max[orientation] + 1):
            wall = {"up": (i, room[1] + dy), "down": (i, room[1] + dy),
                    "left": (room[0] + dx, i), "right": (room[0] + dx, i)}
            self.KB.walls.add(wall[orientation])

    def inference_algorithm(self):
        """First, make some basic inferences:
        1. If there is no breeze or stench in current location, infer that the
        adjacent rooms are safe.
        2. Infer wall locations given bump percept.
        3. Infer Luke's location given gasp percept.
        4. Infer whether the Wampa is alive given scream percept. Clear stench
        from the KB if Wampa is dead.

        Then, infer whether each adjacent room is safe, pit or wampa by
        following the backward-chaining resolution algorithm:
        1. Enumerate possible worlds.
        2. Find the model of the KB, i.e. the subset of possible worlds
        consistent with the KB.
        3. For each adjacent room and each query, find the model of the query.
        4. If the model of the KB is a subset of the model of the query, the
        query is entailed by the KB.
        5. Update KB.pits, KB.wampa, and KB.safe_rooms based on any newly
        derived knowledge.
        """
        # TODO:
        ...
        pass

    def all_safe_next_actions(self):
        """Define R2D2's valid and safe next actions based on his current
        location and knowledge of the environment."""
        safe_actions = []
        x, y = self.loc
        dx, dy = self.orientation_to_delta[get_direction(self.degrees)]
        forward_room = (x+dx, y+dy)
        # TODO:
        ...
        return safe_actions

    def choose_next_action(self):
        """Choose next action from all safe next actions. You may want to
        prioritize some actions based on current state. For example, if R2D2
        knows Luke's location and is in the same room as Luke, you may want
        to prioritize 'grab' over all other actions. Similarly, if R2D2 has
        Luke, you may want to prioritize moving toward the exit. You can
        implement this as basically (randomly choosing between safe actions)
        or as sophisticated (optimizing exploration of unvisited states,
        finding shortest paths, etc.) as you like."""
        actions = self.all_safe_next_actions()
        # TODO:
        ...
        return actions


# Approximately how many hours did you spend on this assignment?
feedback_question_1 = ...

# Which aspects of this assignment did you find most challenging?
# Were there any significant stumbling blocks?
feedback_question_2 = """..."""

# Which aspects of this assignment did you like?
# Is there anything you would have changed?
feedback_question_3 = """..."""
