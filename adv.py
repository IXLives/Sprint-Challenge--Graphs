from room import Room
from player import Player
from world import World

import random
from random import randint
from util import Queue, Stack
from graph import Graph
from ast import literal_eval

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
traversal_path = []


# Use EXPLORED set to store rooms in map_graph that have NO REMAINING ? ROOMS
def reverse_dir(dir):
    if dir == 'n':
        return('s')
    if dir == 's':
        return('n')
    if dir == 'e':
        return('w')
    if dir == 'w':
        return('e')


def traversal():
    # my graph
    map_graph = []
    # my visited set
    explored = set()
    # initialization
    map_graph.append(0)

    # while # of explored rooms < # of rooms in graph
    while len(explored) < len(room_graph):
        # our current location
        current_room = map_graph[-1]
        print(f'Current Room: {current_room}')
        # mark as visited
        explored.add(current_room)
        # get the exits from the given graph
        exits = room_graph[current_room][-1]
        print(f'Exits: {exits}')
        # reset the exploration queue for each room
        to_explore = []
        # if any room in exits is not in visited, add it to the exploration queue
        for key, value in exits.items():
            if value not in explored:
                to_explore.append(value)
                print(f'{value} added to exploration queue')
        # if there are any rooms left unexplored
        if len(to_explore) > 0:
            # pick the first unvisited room
            room_to_visit = to_explore[0]
            # add to graph
            map_graph.append(room_to_visit)
        # if not
        else:
            # return to previous room
            room_to_visit = map_graph[-2]
            # remove 'last' room from graph
            map_graph.pop()
        # if our exit leads to a destination room, go there
        for key, value in exits.items():
            if value == room_to_visit:
                # this is where the magic happens
                traversal_path.append(value)


traversal()

# TRAVERSAL TEST - DO NOT MODIFY
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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
