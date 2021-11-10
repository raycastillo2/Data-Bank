# Python 241 project part 2
import csv
import os


class Song:  # classifies song
    def __init__(self, info):
        self.title = info[1]
        self.artist = info[2]
        self.duration = info[3]
        self.track_ID = info[4]
        self.collabs = info[5]  # part for collaborations


class SongLibrary:
    def __init__(self):
        self.total_songs = 0  # attributes
        self.song_list = []
        self.graph = {}

    def load_library(self):
        with open(os.path.expanduser('~/Desktop/TenKsongs_proj2.csv'), mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                self.song_list.append(Song(row))
                self.total_songs += 1       # load library method
        self.graph = Connections()        # init class connections
        for i in self.song_list:            # getting each song
            self.graph.add_artist(i.artist)                  # we add main artist as a node
            self.graph.feats.get(i.artist).songs_wrote += 1      # count that as one song they wrote
            f = tuple(i.collabs[:len(i.collabs)].split(';'))   # breaks up the collabs individually
            for j in f:
                self.graph.add_connect(i.artist, j)          # for each collab we add that connect
        totalWeight, totalEdges, totalArtists = 0, 0, 0       # this is how i keep track of the numbers
        for v in self.graph:                                  # this is how i print it out neatly
            print(" %s {" % v.get_id())                        # prints artist
            totalArtists += 1
            for w in v.get_feats():
                print("( %s , %s )" % (w, v.get_weight(w)))        # prints features
                totalWeight += v.get_weight(w)
            totalEdges += len(v.get_feats())
            print('}')
        print("total weight: " + str(totalWeight) + "    total edges: " + str(totalEdges/2) + "    total Artists: " + str(
            totalArtists))  # how i see the info on the stack

    def search_artist(self, artist):                      # search artist function
        artist_sa = self.graph.feats.get(artist)                   # gets artist from dictionary
        written = self.graph.feats.get(artist).songs_wrote        # number of songs written
        print("~~~Search Artist~~~")
        print(str(artist) + " => songs written: " + str(written) + " {")
        for b in artist_sa.get_feats():
            print(str(b) + ' ' + str(artist_sa.get_weight(b)))     # prints out info
        print("}")
        return

    def find_new_friends(self, artist):
        artist_fnf = self.graph.feats.get(artist)
        print("~~~Find New Friends~~~")                      # this function just calls all features of there features
        print(str(artist) + " {")                                  # and as ling as they are not the feature of the
        count = 0
        for a in artist_fnf.get_feats():                           # main artist it can be printed out
            artist_a = self.graph.feats.get(a)
            for b in artist_a.get_feats():
                if b not in artist_fnf.connects and b != artist:
                    print(b)
                    count += 1
        print("}" + str(count))

    def find_new_collaborator(self, artist):
        artist_fnc = self.graph.feats.get(artist)
        print("~~~Find New Collaborators~~~")
        print(str(artist) + " {")

        class CollabDict(dict):              # i just make a dict for easy searching and adding
            def add(self, key, w):
                if key in self:
                    self[key] = self[key] + w          # sets the weight equal to all co feats
                else:
                    self[key] = w

        nc_dict = CollabDict()
        for a in artist_fnc.get_feats():                           # what i do hear is add all 2nd hop collabs
            artist_a = self.graph.feats.get(a)                      # to the collabs_dict and if its already in there
            for b in artist_a.get_feats():                          # i just add the weights
                if b != artist and b not in artist_fnc.connects:        # so i get the best collabs
                    artist_b_weight = artist_a.get_weight(b)
                    nc_dict.add(b, artist_b_weight)
        most_collabs = max(nc_dict, key=nc_dict.get)
        num_collabs = max(nc_dict.values())
        print(str(most_collabs) + " with " + str(num_collabs) + " collaborations }")    # and print it here
        print()

    class BinHeap:                                 # how i make the binary heap aka pro que
        def __init__(self):            # init values
            self.heapList = [0]
            self.currentSize = 0

        def just_add(self, something):         # for the first element with a dis of zero
            self.heapList.append(something)
            self.currentSize = self.currentSize + 1

        def perc_Up(self, i):                         # percolates a new item as far up in the tree as it
            while i // 2 > 0:                                    # needs to go to maintain the heap property
                if self.heapList[i] < self.heapList[i // 2]:
                    tmp = self.heapList[i // 2]
                    self.heapList[i // 2] = self.heapList[i]
                    self.heapList[i] = tmp               # here its being moved up
                i = i // 2

        def insert(self, k):           # for adding the values that i det from Dj algorithm
            self.heapList.append(k)
            self.currentSize = self.currentSize + 1
            self.perc_Up(self.currentSize)    # call per so i maintain heap

        def perc_Down(self, i):            # how we send the min value down the tree
            while (i * 2) <= self.currentSize:
                mc = self.minChild(i)
                if self.heapList[i] > self.heapList[mc]:        # where the compare are made so ned it down
                    tmp = self.heapList[i]
                    self.heapList[i] = self.heapList[mc]
                    self.heapList[mc] = tmp
                i = mc

        def minChild(self, i):              # helper to find min of tree
            if i * 2 + 1 > self.currentSize:
                return i * 2
            else:
                if self.heapList[i * 2] < self.heapList[i * 2 + 1]:     # where its compared to travel to the min child
                    return i * 2
                else:
                    return i * 2 + 1

        def delMin(self):                    # this is how we get the smallest value
            retval = self.heapList[1]
            self.heapList[1] = self.heapList[self.currentSize]   # controls size of heap
            self.currentSize = self.currentSize - 1      # when removes it makes it smaller
            self.heapList.pop()
            self.perc_Down(1)
            return retval

    def find_distances(self, starting_vertex):
        distances = {vertex: float('infinity') for vertex in self.graph.feats}    # so we have big values that will get
        distances[starting_vertex] = 0          # starting point                            replaced after pathing
        pq = self.BinHeap()      # ints our heap to keep track of values
        pq.just_add([0, starting_vertex])      # adds first value
        while pq.currentSize > 0:
            current_distance, current_vertex = pq.delMin()      # we pop the smallest to compare
            for neighbor in self.graph.feats.get(current_vertex).get_feats():  # so for all its features we get the dis
                distance = current_distance + 1    # add one to the distance and then
                if distance < distances[neighbor]:  # if its less we add it to both the que and the distances
                    distances[neighbor] = distance     # distances can be constantly over written but because it has no
                    pq.insert([distance, neighbor])         # actual distance it wont be
        print("~~~Find Shortest Path~~~")
        print(str(starting_vertex) + " " + str(distances))   # prints them out
        countertemp = 0
        for i, j in distances.items():
            if j == 1:
                countertemp += 1
        print(countertemp)


class Artist:                            # artist class that all artist have
    def __init__(self, key):
        self.id = key                         # each artist
        self.connects = {}                    # who they have features with
        self.songs_wrote = 0                  # numb songs they wrote

    def add_feat(self, nbr):                     # adds a feature
        if nbr in self.connects:
            temp = int(self.get_weight(nbr))           # if it is already there it will add to weight only
            self.connects[nbr] = temp + 1
        else:
            self.connects[nbr] = 1
        if not nbr:
            self.connects[nbr] = 0

    def get_feats(self):                      # get functions to return needed values for above functions
        return self.connects.keys()

    def get_id(self):
        return self.id

    def get_weight(self, nbr):
        return self.connects[nbr]


class Connections:                  # class for the whole graph
    def __init__(self):
        self.feats = {}             # all artist will appear here
        self.numFeats = 0               # numb of all artist

    def add_artist(self, key):
        if str(key) not in self.feats:          # will add artist if not already in the data base
            self.numFeats = self.numFeats + 1
            new_artist = Artist(key)
            self.feats[key] = new_artist

    def add_connect(self, art, art2):           # adds feature by calling functions in artist class
        if str(art2) not in self.feats:
            self.add_artist(art2)
        self.feats[art2].add_feat(art)
        self.feats[art].add_feat(art2)

    def get_vertices(self):                 # get to receive info from above functions
        return self.feats.keys()

    def __iter__(self):
        return iter(self.feats.values())


song = SongLibrary()
song.load_library()
song.search_artist("Mariah Carey")
song.find_new_friends("Mariah Carey")
song.find_new_collaborator("Mariah Carey")
song.find_distances("Mariah Carey")
