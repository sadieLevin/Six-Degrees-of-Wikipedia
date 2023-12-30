#####
# Contributors: Sadie Levin, Proofreading by Cassie Ureda
# Last Edited: 12/11/2023
#####

import bs4 as bs
import urllib.request
import json
import time

#scrapes wikipedia starting from a node and stores graph as adjacency list in json file
def download_simple_wikiedia(print_rate = 100):

    print("Starting Simple Wikipedia Scan :)")
    """ Input: preferred number of articles between prints
        Output: JSON file containing graph of simple wikipedia, starting with the initial root node at Architecture"""
    #initializing necessary variables
    start_time = time.time()        #for troubleshooting and timing estimates
    i = 1
    source = urllib.request.urlopen('https://simple.wikipedia.org/wiki/Architecture').read()    #webscraping boilerplate
    soup = bs.BeautifulSoup(source, 'lxml')
    body = soup.body

    #base case
    #seeds list with initial links and enters first node into link_node_dict
    current_link = "Architecture"
    link_node_dict = {}         #dictionary with the article title as the key and the nodes it links to in a list as its value 
    search_list = []            #list of pending articles to search
    temp_link_list = []         #holding space for vertices that haven't been assigned to their respective nodes
    for paragraph in body.find_all('p'):        #continues populating initial variables with critical data
        for url in paragraph.find_all('a'):
            link = url.get('href')
            #filter unwanted cases by neglecting to include them when unwanted cases come up
            #most notably, eliminates supplementary files, commentary, user pages, and image files
            if link is not None and (link.find(":") == -1 or link.find(":_") != -1) and link.find("/wiki/") == 0 and link.find("#") == -1:
                temp_link_list.append(link.lstrip("/wiki/"))    #populates
                if link_node_dict.get(link.lstrip("/wiki/")) is None and link.lstrip("/wiki/") not in search_list:
                    search_list.append(link.lstrip("/wiki/"))
            
    link_node_dict.update({current_link: temp_link_list})
    
    #repeat base case until there are no more available links
    while len(search_list) != 0:
        
        #get next link
        current_link = search_list.pop(0)
        try: 
            #grab article from wikipedia and make BeautifulSoup object
            source = urllib.request.urlopen('https://simple.wikipedia.org/wiki/' + current_link).read()
            soup = bs.BeautifulSoup(source, 'lxml')
            body = soup.body

            #find and vets links in the article, notes adjacency in dictionary
            temp_link_list = []
            for paragraph in body.find_all('p'):
                for url in paragraph.find_all('a'):
                    link = url.get('href')
                    #filter unwanted cases by neglecting to include them when unwanted cases come up
                    if link is not None and (link.find(":") == -1 or link.find(":_") != -1) and link.find("/wiki/") == 0:
                        temp_link_list.append(link.lstrip("/wiki/"))
                        if link_node_dict.get(link.lstrip("/wiki/")) is None and link.lstrip("/wiki/") not in search_list:
                            search_list.append(link.lstrip("/wiki/"))
            link_node_dict.update({current_link: temp_link_list})
            i += 1          #to keep track of how many articles we've gone through for printing purposes
        except:
            print(f"Error thrown at {current_link}, item {i}")  #prints exception case 
        if i%print_rate == 0:   #status updates to make sure things are still working, keeps track of rate of completion
            print(f"finished {current_link}, {len(link_node_dict)} scanned, {len(search_list)} seen, rate: {round(print_rate / (time.time() - start_time), 6)} per second")
            start_time = time.time()

    #outputs json file
    with open("Wikipedia Nodes 914.json", "w") as outfile:
        json.dump(link_node_dict, outfile)
    print("Done :D")

if __name__ == "__main__":
    download_simple_wikiedia(print_rate = 10)
