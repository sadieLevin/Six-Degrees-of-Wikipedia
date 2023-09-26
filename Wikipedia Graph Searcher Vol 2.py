import json
import time
import sys

# Opening JSON file
f = open('Wikipedia Nodes 914.json')
data = json.load(f)
f.close()

#WARNING can be memory-intense 
def find_largest_wikipedia_number(dataset, start_term):

    #About paths:
    #The central goal behind keeping track of "paths" is to identify each unique route from the starting point (start_term) and the other objects stored in the attached JSON file. The objects are stored in like vertices in a graph, where the key is the name (categorical index) of the vertex and its arcs (one-directional edges) are stored in the value as a list. This was so many words to say that our data is stored like the following:
    
    #{article_1:[article_2, article_3, article_4], article_2: [article_3, article_1, article_5], article_3: [article_5, article_6]...}
    
    #and our objective is to restructure this data in unique paths like the following:
    #[[article_1], [article_1, article_2], ... , [article_1, article_2, article_5], [article_1, article_3, article_5]...]

    #note that article_1 is the prefix for all paths. article_1 is passed into this function as start_term.

    #Initializes key data structures

    finished_paths = []                 #where all finished paths are stored
    finished_terms = set()              #a hash table of all completed terms,

    current_path = [start_term,]        #paths are added to finished_paths
    queued_paths = [current_path,]

    while len(queued_paths) != 0:   #stop once all nodes that have arcs pointing to them also have paths
        
        ###TODO: BELOW CAN PROBABLY BE OPTIMIZED
        seen_paths = []                           #TODO: MAKE REDUNDANT, PUT INSTANCE OUTSIDE WHILE LOOP AND RESET IT AT THE BOTTOM FOR CLARITY
        for path in queued_paths:
            term = path[-1]
            if term not in finished_terms and term in dataset:
                for subterm in dataset[term]:
                    if subterm not in finished_terms:
                        temporary_holding = path[:]             #TODO: Replace temporary holding with something better if possible?
                        temporary_holding.append(subterm)
                        seen_paths.append(temporary_holding)
                finished_paths.append(path)

        ###ABOVE CAN PROBABLY BE OPTIMIZED

        for path in queued_paths:
            term = path[-1]                 #TODO: likely redundant due to "if term not in finished_terms" from above section, test removal
            if term not in finished_terms:  # " "
                finished_terms.add(term)    ####UNLIKE THE LAST TWO LINES, THIS ONE IS DEFINITELY NOT REDUNDANT - it adds all new known nodes to a blacklist to prevent longer paths from being recorded
        queued_paths = seen_paths           #MOVE SEEN_PATHS CLEAR BELOW HERE
        print(f"queued paths = {len(queued_paths)}, finished terms = {len(finished_terms)}/{len(dataset)}, finished paths = {len(finished_paths)}")


    ###HI READER
    #below is just some analytics! If... god forbid sadie puts this whole function in an __init__... you'd be able to extract all sorts of interesting information with getter functions. Until then, this is all you get.
    longest_path_length = 0
    for path in finished_paths:
        if len(path) > longest_path_length:
            longest_path_length = len(path)

    longest_paths = []
    for path in finished_paths:
        if len(path) == longest_path_length:
            longest_paths.append(path)

    for path in longest_paths:
        print(path)

    print("length = " + str(longest_path_length))


if __name__ == "__main__":
    find_largest_wikipedia_number(data, "Light")