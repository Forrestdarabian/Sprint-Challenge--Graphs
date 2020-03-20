from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


# Queue and Stack to avoid import errors


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


# Reverse Directions


def reverse(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    else:
        return 'e'


# Entering a New Room Functionality


def entry(room, visited_rooms):
    visited_rooms[room.id] = {}
    for exit_direction in room.get_exits():
        visited_rooms[room.id][exit_direction] = '?'


# BFS


def breadth_first_search(visited_rooms):
    # Define our variables
    visited = set()
    q = Queue()
    room = player.current_room
    # Enqueue the Room ID
    q.enqueue([room.id])
    # While theres room...
    while q.size() > 0:
        # Dequeue the Path
        path = q.dequeue()
        # Define last Node
        end = path[-1]
        # If our last Node isnt visited...
        if end not in visited:
            # Add it to visited
            visited.add(end)
            # Create a for loop and check if the last room has been visited
            for exit_direction in visited_rooms[end]:
                # If there is no exit direction in the last room...
                if (visited_rooms[end][exit_direction] == '?'):
                    # Return path
                    return path
                # However, if it hasnt been visited...
                elif (visited_rooms[end][exit_direction] not in visited):
                    # Create a new path
                    new_path = path + [visited_rooms[end][exit_direction]]
                    # Enqueue the new path
                    q.enqueue(new_path)
    return path


# Load world


world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"


map_file = "maps/main_maze.txt"


# Loads the map into a dictionary


room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)


# Print an ASCII map


world.print_rooms()
player = Player(world.starting_room)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']


traversal_path = ['n', 's', 'e', 'w']
visited_rooms = {}

# while the length of visited rooms is less than the length of the entire map...
while(len(visited_rooms) < len(room_graph)):
    # This should traverse the player through rooms
    if player.current_room.id not in visited_rooms:
        entry(player.current_room, visited_rooms)

    # exits is a list
    exits = []
    # loop over visited Rooms
    for new_direction in visited_rooms[player.current_room.id]:
        # this takes care of the ? and appends a new direction to exit
        if (visited_rooms[player.current_room.id][new_direction] == '?'):
            exits.append(new_direction)

    # if the length of exits is 0
    if (len(exits) == 0):
        # use our BFS Traversal
        path = breadth_first_search(visited_rooms)
        # translate Room ID to direction
        for id in path:
            for exit_direction in visited_rooms[player.current_room.id]:
                if (exit_direction in visited_rooms[player.current_room.id]):
                    # print(f"Current room is {player.current_room.id} and direction is {exit_direction}")
                    # if the current rooms exit direction is comparable to id and the current rooms id is not equal to ID///
                    if (visited_rooms[player.current_room.id][exit_direction] == id and player.current_room.id != id):
                        # append the exit direction to our traversal path
                        traversal_path.append(exit_direction)
                        # set new room equal to the exit direction of the room were currently in
                        new_room = player.current_room.get_room_in_direction(
                            exit_direction)
                        # then our new room ID is equal to that room
                        visited_rooms[player.current_room.id][exit_direction] = new_room.id
                        # if new rooms ID isnt in visited rooms...
                        if (new_room.id not in visited_rooms):
                            # run our entry function to enter a new room
                            entry(new_room, visited_rooms)
                        # and reverse directions since we need to find a new route
                        visited_rooms[new_room.id][reverse(
                            exit_direction)] = player.current_room.id
                        # then finally have the player traverse through to the exit
                        player.travel(exit_direction)

    else:
        # set new exit to a random exit
        new_exit = random.choice(exits)
        # append that new exit to our traversal path
        traversal_path.append(new_exit)
        # make new room equal to getting the new exit
        new_room = player.current_room.get_room_in_direction(new_exit)
        # then our exit is equal to our new room ID
        visited_rooms[player.current_room.id][new_exit] = new_room.id
        # if a new room ID isnt in visited rooms...
        if (new_room.id not in visited_rooms):
            # run our entry function to enter a new room
            entry(new_room, visited_rooms)
        # and reverse directions since we need to find a new route
        visited_rooms[new_room.id][reverse(new_exit)] = player.current_room.id
        # then finally have the player traverse through to the exit
        player.travel(new_exit)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


# #######
# # UNCOMMENT TO WALK AROUND
# #######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
