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
    map_graph = Graph()
    mapped = set()
    explored = {}
    to_explore = []
    current_room = player.current_room.id

    while len(explored) < len(room_graph):
        prev_room = current_room
        current_room = player.current_room.id
        exits = player.current_room.get_exits()
        random_dir = exits[randint(0, (len(exits) - 1))]
        reverse = reverse_dir(random_dir)
        # print(random_dir, reverse)
        if current_room not in explored:
            # this room has been explored but not mapped
            explored[current_room] = {exit: '?' for exit in exits}
            explored[current_room][reverse] = prev_room
        if prev_room != current_room:
            explored[current_room][reverse] = prev_room
            explored[prev_room][random_dir] = current_room
        # else:
            # if len(exits) > 1:
            #     exits.remove(random_dir)
            #     random_dir = exits[randint(0, (len(exits) - 1))]
            #     reverse = reverse_dir(random_dir)
            # else:
            #     random_dir = exits[0]
            #     reverse = reverse_dir(random_dir)
        player.travel(random_dir)
        print(explored, '\n', explored[current_room],
              '\n', f'{random_dir} to {explored[current_room][random_dir]}')
        traversal_path.append(random_dir)
    print(explored)


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
