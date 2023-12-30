#####
# Contributors: Sadie Levin, Proofreading by Cassie Ureda
# Last Edited: 12/11/2023
#####

import json
import csv
import random

# Opening JSON file
f = open('Wikipedia Nodes 914.json')
data = json.load(f)
f.close()

# Analyzes JSON-format graph, returns histogram data, prints analytics about graph
def lossless_check_longest_degree_of_separation_at(dataset, start_term = random.choice(list(data)), printing = False):
    """
    Input: a JSON-format graph
    Output: returns histogram data - binwidth = 1 degree of depth from root node
            prints analytics while running
            prints longest paths from root node, histogram data, length of longest paths upon completion
    """

    #About paths:
    #The central goal behind keeping track of "paths" is to identify each unique route from the starting point (start_term) and the other objects stored in the attached JSON file. The objects are stored in like vertices in a graph, where the key is the name (categorical index) of the vertex and its arcs (one-directional edges) are stored in the value as a list. This was so many words to say that our data is stored like the following:
    
    #{article_1:[article_2, article_3, article_4], article_2: [article_3, article_1, article_5], article_3: [article_5, article_6]...}
    
    #and our objective is to restructure this data in unique paths like the following:
    #[[article_1], [article_1, article_2], ... , [article_1, article_2, article_5], [article_1, article_3, article_5]...]

    #note that article_1 is the prefix for all paths. article_1 is passed into this function as start_term.

    #Initializes key data structures
    quantity_of_finished_paths_per_degree = []  #storing histogram data

    finished_paths = []                 #where all finished paths are stored to prevent redundancies
    finished_terms = set()              #a hash table of all completed terms, excluding their paths

    current_path = [start_term,]        #critical in assembling paths for storage
    queued_paths = [current_path,]      #ordered list of next paths to process

    while len(queued_paths) != 0:   #stop once all queued paths are processed
        seen_paths = []             #storing paths to be searched in next iteration of above loop
        for path in queued_paths:
            term = path[-1]         #takes last item in path to identify current working node (like how the last entry of a directory is a file name)
            if term not in finished_terms and term in dataset:      
                for subterm in dataset[term]:               #the subterm is the term of the child nodes
                    if subterm not in finished_terms:       #if the node has been processed before, do not add it to the queue of terms to process again
                        temporary_holding = path[:]         #temporary holding helps construct the path with its notation
                        temporary_holding.append(subterm)
                        seen_paths.append(temporary_holding)
                finished_paths.append(path)     #once a path has been processed completely, add it to a list of finished paths

        previous_loop_length = len(finished_terms)        #keeps track of the total number of finished terms FOR RUNTIME ANALYTICS
        for path in queued_paths:                         #iterates through all queued paths
            term = path[-1]                               #grabs term from path
            if term not in finished_terms:                # if term hasn't been processed yet
                finished_terms.add(term)    #adds all new known nodes to a blacklist to prevent longer paths from being recorded
        queued_paths = seen_paths           #recycles queued_paths variables
        quantity_of_finished_paths_per_degree.append(len(finished_terms) - previous_loop_length)    #back to analytics numbers tracking, constructs next bucket of histogram
        if printing:
            print(f"queued paths = {len(queued_paths)}, finished terms = {len(finished_terms)}/{len(dataset)}, finished paths = {len(finished_paths)}")


    ### THE FOLLOWING CODE gives analytics about the paths, providing info about longest data and insights about what is going on under the hood
    analytics_list = [quantity_of_finished_paths_per_degree]

    longest_path_length = 0
    for path in finished_paths:
        if len(path) > longest_path_length:
            longest_path_length = len(path)

    longest_paths = []
    for path in finished_paths:
        if len(path) == longest_path_length:
            longest_paths.append(path)
    
    if printing:
        for path in longest_paths:
            print(path)
        print("length = " + str(longest_path_length))
        print(quantity_of_finished_paths_per_degree)
        print(len(quantity_of_finished_paths_per_degree))
    return quantity_of_finished_paths_per_degree


if __name__ == "__main__":
    lossless_check_longest_degree_of_separation_at(data, start_term = "Hitler", printing=True)