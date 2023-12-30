#####
# Contributors: Courtney St. Onge, Editing by Sadie Levin, Proofreading by Cassie Ureda
# Last Edited: 12/11/2023
#####

from pgl import GWindow, GOval, GRect, GLabel, GLine
import math
from json import load
from random import choice

#window-specific dimensions for PGL
GWINDOW_WIDTH = 600      
GWINDOW_HEIGHT = 600
CIRC_WIDTH = 15
CIRC_RAD = 7.5
BIG_CIRC_RAD=210

#loading in the JSON file
f = open('Wikipedia Nodes 914.json')
dataset = load(f)
f.close()

#initializing variables
keys=list(dataset.keys())
values=list(dataset.values())

#initializing GWindow
gw=GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)

def run_program():
    def construct_graph(root_node):     #places all nodes and vertices, assigns values to nodes
        """Input: int
            Number of dots to be connected to the center vertex
            Output: A dot in the middle with evenly spaced dots with lines connecting them"""

        ####first, clear all old items
        gw.clear()
        
        ####next, recreate labels
        #Label recreation necessary due to PGL limitation
        #recreate child label
        gw.child_label = GLabel("Hover over a node to display its name!")
        gw.child_label.set_font("25px 'times new roman'")
        gw.child_label_x= ((GWINDOW_WIDTH/2)- gw.child_label.get_width()/2)
        gw.child_label_y= ((GWINDOW_HEIGHT-15)- gw.child_label.get_ascent()/2)
        gw.add(gw.child_label, gw.child_label_x, gw.child_label_y)
        
        #recreate parent label
        gw.parent_label = GLabel(f"Root Node: {root_node}")
        gw.parent_label.set_font("25px 'times new roman'")
        gw.parent_label_x= ((GWINDOW_WIDTH/2)- gw.parent_label.get_width()/2)
        gw.parent_label_y= (gw.parent_label.get_ascent() + 15)
        gw.add(gw.parent_label, gw.parent_label_x, gw.parent_label_y)
        
        #gets children of root node from dataset, 
        child_node_list = dataset[root_node]
        quantity_of_child_nodes = len(child_node_list)

        #start by making middle vertex
        mid_x=(GWINDOW_WIDTH/2-CIRC_WIDTH/2)
        mid_y=(GWINDOW_HEIGHT/2-CIRC_WIDTH/2)

        #next, draw vertices
        if len(child_node_list) > 0:        #failsafe in case of childless nodes
            start=(2*math.pi)/quantity_of_child_nodes
        current_node_index=1         
        for child_node in child_node_list:
            #constructs line going out from center
            out_line=GLine(mid_x+CIRC_RAD,mid_y+CIRC_RAD,(BIG_CIRC_RAD*((current_node_index%3 + 1)/3))*math.cos(start)+mid_x+CIRC_RAD,(BIG_CIRC_RAD*((current_node_index%3 + 1)/3))*math.sin(start)+mid_y+CIRC_RAD)
            gw.add(out_line)
            #constructs node at end of line
            vert= GOval((BIG_CIRC_RAD*((current_node_index%3 + 1)/3))*math.cos(start)+mid_x,(BIG_CIRC_RAD*((current_node_index%3 + 1)/3))*math.sin(start)+mid_y,CIRC_WIDTH,CIRC_WIDTH, value = child_node)
            vert.set_filled(True)
            gw.add(vert)
            #stagger node distance
            current_node_index+=1
            start+=(2*math.pi)/quantity_of_child_nodes
        
        #adds root node
        mid_vert = GOval(mid_x,mid_y,CIRC_WIDTH,CIRC_WIDTH, value = root_node)
        mid_vert.set_filled(True)
        gw.add(mid_vert)
        
    #when mouse hovers over node, update label and display node's value
    def show_label(event):      
        mousex= event.get_x()
        mousey= event.get_y()
        if gw.get_element_at(mousex,mousey) is not None:
            if gw.get_element_at(mousex,mousey).get_value() != "line":
                gw.child_label.set_label(gw.get_element_at(mousex,mousey).get_value())
                gw.child_label.x = (GWINDOW_WIDTH/2)- gw.child_label.get_width()/2
                gw.child_label_y = (GWINDOW_HEIGHT-15)- gw.child_label.get_ascent()/2
                gw.child_label._update_location()

    #when clicked on something, if node, update graph with selected node as root node
    def on_down(event):     
        #gets element at mo
        mousex = event.get_x()
        mousey = event.get_y()
        if gw.get_element_at(mousex,mousey) is not None:
            if gw.get_element_at(mousex,mousey).get_value() != "line":
                construct_graph(gw.get_element_at(mousex,mousey).get_value())

    #initializes graphics and user input listeners
    #construct_graph(choice(list(dataset)))
    construct_graph("Hitler")
    gw.add_event_listener("mousemove", show_label)
    gw.add_event_listener("press", on_down)
    
if __name__ == "__main__":
    run_program()