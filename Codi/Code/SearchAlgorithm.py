# This file contains all the required routines to make an A* search algorithm.
#
__author__ = '1634264'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Curs 2023 - 2024
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    path_list=[]
    conexio=map.connections[path.last]
    for station in conexio:
        new_path=Path(list(path.route))
        new_path.add_route(station)
        new_path.g = path.g
        new_path.h = path.h
        new_path.f = path.f
        path_list.append(new_path)
        
    
    return path_list


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    ret_path_list = []
    for path in path_list:
        if len(path.route) == len(set(path.route)):
                ret_path_list.append(path)
    
    return ret_path_list


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return expand_paths + list_of_path


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    llista_ret = [Path(origin_id)]

    while llista_ret[0].last != destination_id and len(llista_ret) != 0:
        c = llista_ret[0]
        e = expand(c, map)
        e = remove_cycles(e)
        llista_ret = insert_depth_first_search(e, llista_ret[1:])

    
    if llista_ret[0].last == destination_id:
        return llista_ret[0]
    else:
        print("No existeix Solucio")
        return llista_ret[0]


def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return list_of_path + expand_paths 


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    llista_ret = [Path(origin_id)]

    while llista_ret[0].last != destination_id and len(llista_ret) != 0:
        c = llista_ret[0]
        e = expand(c, map)
        e = remove_cycles(e)
        llista_ret = insert_breadth_first_search(e, llista_ret[1:])

    
    if llista_ret[0].last == destination_id:
        return llista_ret[0]
    else:
        print("No existeix Solucio")
        return llista_ret[0]


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    
    if type_preference == 0:
        for path in expand_paths:
            path.update_g(1)
    elif type_preference == 1:
        for path in expand_paths:
            path.update_g(map.connections[path.penultimate][path.last])
    elif type_preference == 2:
        for path in expand_paths:
            if map.stations[path.penultimate]['name'] != map.stations[path.last]['name']:
                aux = map.connections[path.penultimate][path.last] * map.velocity[map.stations[path.penultimate]['line']]
                path.update_g(aux)  
    elif type_preference == 3:
        for path in expand_paths:
            if map.stations[path.penultimate]['line'] != map.stations[path.last]['line']:
                path.update_g(1) 
            else:
                path.update_g(0)
    
    return expand_paths


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    list_of_path = list_of_path + expand_paths
    list_of_path = sorted(list_of_path, key=lambda x: x.g)
    return list_of_path
                


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    llista_ret = [Path(origin_id)]
    while llista_ret[0].last != destination_id and len(llista_ret) != 0:
        c = llista_ret[0]
        e = expand(c, map)
        e = remove_cycles(e)
        e = calculate_cost(e, map, type_preference)
        llista_ret = insert_cost(e, llista_ret[1:])
        
    if llista_ret[0].last == destination_id:
        return llista_ret[0]
    else:
        return llista_ret[0]


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            destination_id (int): Final station id
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    if type_preference == 0:
        for path in expand_paths:
            if path.last == destination_id or destination_id in map.connections[path.last]:
                path.update_h(0)
            else:
                path.update_h(1)
    elif type_preference == 1:
        for path in expand_paths:
            list_coord_p = (map.stations[path.last]['x'], map.stations[path.last]['y'])
            list_cood = (map.stations[destination_id]['x'], map.stations[destination_id]['y'])
            res = euclidean_dist(list_coord_p, list_cood)
            v = max(map.velocity.values())
            ret = res / v
            path.update_h(ret)
    elif type_preference == 2:
        for path in expand_paths:
            list_coord_p = (map.stations[path.last]['x'], map.stations[path.last]['y'])
            list_cood_end = (map.stations[destination_id]['x'], map.stations[destination_id]['y'])
            res = euclidean_dist(list_coord_p, list_cood_end)
            path.update_h(res)
    elif type_preference == 3:
        for path in expand_paths:
            if map.stations[path.last]['line'] != map.stations[destination_id]['line']:
                path.update_h(1)
            else:
                path.update_h(0)
    return expand_paths


def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for path in expand_paths:
        path.update_f()
    return expand_paths	


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g-cost at this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
             visited_stations_cost (dict): Updated visited stations cost
    """
    for path in expand_paths:
        if path.last in visited_stations_cost.keys():
            if path.g >= visited_stations_cost[path.last]:
                expand_paths.remove(path)
            elif path.g < visited_stations_cost[path.last]:
                visited_stations_cost[path.last] = path.g
                for path_l in list_of_path:
                    if path_l.last == path.last:
                        list_of_path.remove(path_l)
        else:
            visited_stations_cost[path.last] = path.g
    return expand_paths, list_of_path, visited_stations_cost




def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    list_of_path = list_of_path + expand_paths
    list_of_path = sorted(list_of_path, key=lambda x: x.f)
    return list_of_path


def distance_to_stations(coord, map):
    """
        From coordinates, it computes the distance to all stations in map.
        Format of the parameter is:
        Args:
            coord (list): Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            (dict): Dictionary containing as keys, all the Indexes of all the stations in the map, and as values, the
            distance between each station and the coord point
    """
    dict_ret = {}
    for station_id, station_dist in map.stations.items():
        list_cood = (station_dist['x'], station_dist['y'])
        res = euclidean_dist(coord, list_cood)
        dict_ret[station_id] = res
    dict_ord = dict(sorted(dict_ret.items(), key= lambda item: (item[1], item[0])))
    return dict_ord


def Astar(origin_id, destination_id, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    dict_visited = {}
    llista_ret = [Path(origin_id)]
    while llista_ret[0].last != destination_id and len(llista_ret) != 0:
        c = llista_ret[0]
        e = expand(c, map)
        e = remove_cycles(e)
        e = calculate_heuristics(e, map, destination_id, type_preference)
        e = calculate_cost(e, map, type_preference)
        e = update_f(e)
        e, llista_ret, dict_visited = remove_redundant_paths(e, llista_ret, dict_visited)
        llista_ret = insert_cost_f(e, llista_ret[1:])
    if llista_ret[0].last == destination_id:
        return llista_ret[0]
    else:
        return llista_ret[0]

def Astar_improved(origin_coord, destination_coord, map):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_coord (list): Two REAL values, which refer to the coordinates of the starting position
            destination_coord (list): Two REAL values, which refer to the coordinates of the final position
            map (object of Map class): All the map information

        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_coord to destination_coord
    """
    origin_id = distance_to_stations(origin_coord, map)
    destination_id = distance_to_stations(destination_coord, map)
    dict_cam = {}
    map.add_velocity(5)
    llista_ret = [Path(origin_id[0])]
    while llista_ret[0].last != destination_id[0] and len(llista_ret) != 0:
        c = llista_ret[0]
        e = expand(c, map)
        e = remove_cycles(e)
        e = calculate_heuristics(e, map, destination_id, 1)
        e = calculate_cost(e, map, 1) 
        e, llista_ret, dict_cam = remove_redundant_paths(e, llista_ret, dict_cam)
        llista_ret = insert_cost_f(e, llista_ret[1:])
    if llista_ret[0].last == destination_id[0]:
        return llista_ret[0]
    else:
        return llista_ret[0]


