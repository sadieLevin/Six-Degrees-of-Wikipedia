# Six-Degrees-of-Wikipedia

Hi reader! 

This is an overview of the Six Degrees of Wikipedia project I've been working on since June 2023. 

### OBJECTIVE
Inspired by the proper [Six Degrees of Wikipedia](https://www.sixdegreesofwikipedia.com/) website, this program seeks to find the answer to the task at hand...
*what is the longest optimal Wikipedia path?*
This program utilizes basic Graph Theory, optimizations including hash tables and integer comparisons, and data wrangling to improve runtime, sustainability, and efficiency. 

### DEPENDENCIES
The JSON package for Python, Python 3, around 500MB of available memory and like 30 seconds tops of processing time per run.

### IMPLEMENTATION
The .json file is a sample of Simple Wikipedia as scraped by a web crawler (DO NOT SCRAPE WIKIPEDIA FASTER THAN ONE QUERY PER SECOND >:( IT'S RUDE). It includes roughly 50% of the non-orphaned Simple Wikipedia pages. 

The .py file is commented to hell and back, but there's some extra important information for running. The find_largest_wikipedia_number() function takes two values; the dataset to be analyzed and the root node. The dataset should be read in from the JSON file as a dictionary and the starting word has a fallback value with a random node in the dataset. 

### RUNNING
Attached are two documents, a .py file and a .json file. Download both and open them using the IDE of your choice within the same space and run the .py file. The output gives some diagnostics which I will explain below:

Sample output:

```
queued paths = 5, finished terms = 1/59400, finished paths = 1
queued paths = 32, finished terms = 6/59400, finished paths = 5
queued paths = 425, finished terms = 33/59400, finished paths = 22
...

...
queued paths = 500, finished terms = 81518/59400, finished paths = 531431
queued paths = 517, finished terms = 81529/59400, finished paths = 531721
queued paths = 0, finished terms = 81535/59400, finished paths = 531850
```

Take the case "beans" for example. If "beans" has the children \["legumes", ... "agriculture"\] where the length of the list is 5, Wikipedia Graph Searcher Vol 2 (abbreviated WGS) will queue all items in the list as the next nodes to check. The variable "queued_paths" is the number of queued paths at that given moment. Whenever all shortest paths from the root to a given node are found, the node name is added to the hash table "finished_terms", and the length of such is displayed in the console periodically, alongside the estimated number of terms to be iterated through. The variable "finished_paths" is a list of identified paths and its length is displayed. 

Every time the program prints, it indicates that it has found all paths of a given length. In the above example, line one indicates that there's one (trivial) path with a length of one, line two indicates that there are five paths with a length of two or less, and so on. 
