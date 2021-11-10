# Python 241 project
import csv
import os
import time
import random


class Song:     # classifies song
    def __init__(self, info):
        self.title = info[1]
        self.artist = info[2]
        self.duration = info[3]
        self.track_ID = info[4]


class SongLibrary:    # main class for whole library
    def __init__(self):
        self.total_songs = 0         # attributes
        self.song_list = []
        self.tree = []
        self.sorted = False
        self.counter = 0
        self.ttl = 0
        self.ttb = 0
        self.obj_loc = []


    def load_library(self):   # this opens and loads library of csv file into an array
        with open(os.path.expanduser('~/Desktop/TenKsongs.csv'), mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:                 # for each row we init class Song so we can assign attributes to it
                self.song_list.append(Song(row))
                self.total_songs += 1              # counts each song

    def linear_search(self, attribute, query):    # searches through one by one
        tsl = time.perf_counter()
        counter = 0
        if attribute == 'Title':    # just seeing what attribute is being looked for
            for i in self.song_list:  # for loop that goes through all the data and counts to see if what we are looking for is right
                if i.title == query:
                    counter += 1          # adds to counter
            tel = time.perf_counter()
            self.ttl += tel - tsl
            return counter
        elif attribute == 'Artist':
            for i in self.song_list:  # just if you wanted to find the artist
                if i.artist == query:
                    counter += 1
            return counter
        else:
            return "Unknown attribute"

    def quick_sort(self):  # quick sort function more like how i did it before but now in line
        def swapper(low, high):       # the window of our array
            nextWindow = (low - 1)               # will change based on number of swaps and is the window for next quicksort call
            pivot = self.song_list[high]  # sets our pivot
            for j in range(low, high):          # for all elements in our window
                if self.song_list[j].title <= pivot.title:      # if number is smaller then pivot then me move it to the end
                    nextWindow = nextWindow + 1
                    self.song_list[nextWindow], self.song_list[j] = self.song_list[j], self.song_list[nextWindow]
                    # ^^ then we swap it with the nextwindow so we know that elemts less then the window are really small
            self.song_list[nextWindow + 1], self.song_list[high] = self.song_list[high], self.song_list[nextWindow + 1]
            return nextWindow + 1

        def quickSort(low, high):              # this is where we have the recursive calls
            if len(self.song_list) == 1:           # base of recursive call
                return self.song_list
            if low < high:
                pi = swapper(low, high)          # this is the inilization of the swapper
                quickSort(low, pi - 1)           # then this will call itself for the lower array
                quickSort(pi + 1, high)          # this will call itself for the upper array

        quickSort(0, self.total_songs-1)
        for i in range(len(self.song_list)):     # will call it for each version of itself
            print(self.song_list[i].title)

    def binary_tree(self, attribute, query):
        class Node:                                # initializing object attributes under class Node
            def __init__(self, data):
                self.data = data           # what the song is
                self.parent = None         # bst parent info
                self.left = None           # bst left child info
                self.right = None          # bst right child info
                self.balance = 0           # our balancing key
                self.top = None

        class Rooted:
            def __init__(self):
                self.root = None

            def TreeScale(self, node):                        # this is what scales the nodes
                if node.balance < -1 or node.balance > 1:   # this is what calls the rebalancing so it can be evened out
                    self.Rebalance(node)
                    return
                if node.parent != None:                 # this is the scale that makes sure that it is even
                    if node == node.parent.left:             # For example if the left is to big it will be a neg number
                        node.parent.balance -= 1
                    if node == node.parent.right:            # else if to far right we have a pos number
                        node.parent.balance += 1
                    if node.parent.balance != 0:             # call it again for next level ie parent
                        self.TreeScale(node.parent)

            def Rebalance(self, node):                 # this is what is the brain that calls the adjustment methods
                if node.balance > 0:                     # if pos then we will call the right rotate for the
                    if node.right.balance < 0:                # right child of the very first parent
                        self.rightRotate(node.right)                # and then rotate left the parent to the left child
                        self.leftRotate(node)
                    else:                                      # same as what is in text book
                        self.leftRotate(node)
                elif node.balance < 0:                   # just does opposite of above
                    if node.left.balance > 0:
                        self.leftRotate(node.left)
                        self.rightRotate(node)
                    else:
                        self.rightRotate(node)

            def leftRotate(self, par):       # where we rotate things to the left similar to txtbk
                chi = par.right           # setting the chi to the par right child
                par.right = chi.left        # then shift children
                if chi.left != None:          # then if empty we can push it down
                    chi.left.parent = par
                chi.parent = par.parent
                if par.parent == None:        # do same with this
                    self.root = chi
                elif par == par.parent.left:      # seeing if it has the a parent left and if it does it will set the chi to it
                    par.parent.left = chi
                else:
                    par.parent.right = chi
                chi.left = par                       # this is where we see it turn ans swap balances
                par.parent = chi
                par.balance = par.balance - 1 - max(0, chi.balance)
                chi.balance = chi.balance - 1 + min(0, par.balance)

            def rightRotate(self, par):    # kinda same as left rotate
                chi = par.left
                par.left = chi.right;
                if chi.right != None:
                    chi.right.parent = par
                chi.parent = par.parent;
                if par.parent == None:
                    self.root = chi
                elif par == par.parent.right:
                    par.parent.right = chi
                else:
                    par.parent.left = chi
                chi.right = par
                par.parent = chi
                par.balance = par.balance + 1 - min(0, chi.balance)
                chi.balance = chi.balance + 1 + max(0, par.balance)


            def insert(self, key):       # waht puts the values into the binary tree
                node = Node(key)            # this is out particular data point and inniates tha class Node
                last_roots = None
                roots = self.root             # this is what we go to see what its root is from the class Rooted
                while roots != None:                  # for out entries that have already been called
                    last_roots = roots
                    if node.data.title < roots.data.title:    # we compaire to the first entrie
                        roots = roots.left                    # and if it fits we can put it in
                    else:
                        roots = roots.right
                node.parent = last_roots
                if last_roots == None:             # if
                    self.root = node
                elif node.data.title < last_roots.data.title:    # how we go up and down the tree looking for spots to fill in
                    last_roots.left = node
                else:
                    last_roots.right = node
                self.TreeScale(node)                   # we make sure to scale the tree to keep it balanced
        if not self.sorted:                     # what we use to add all data points to the BST but make it only once
            tsbi = time.perf_counter()       # counter
            song_root = Rooted()                       # sets class to this var
            self.sorted = True                         # changes the bool sorted var
            for i in range(len(self.song_list)):
                song_root.insert(self.song_list[i])          # we call insert function for each item in the song list
            tebi = time.perf_counter()                   # timer
            self.ttb += tebi - tsbi
            self.top = song_root.root            # what the very top element is for other uses

        def obj_data(obj):
            print(obj)

        def finder(node, attribute, query):   # finds parts of binary tree
            tsb = time.perf_counter()
            if attribute == 'Title':
                if not node:            # if you get to the end and there is nothing (base)
                    return
                if query < node.data.title:                     # if query is less then we wanna go right
                    finder(node.left, attribute, query)
                elif query > node.data.title:                   # else we go left
                    finder(node.right, attribute, query)
                elif query == node.data.title:                  # we found the data
                    self.counter += 1
                    finder(node.right, attribute, query)
                    obj_data(node.data.artist)

            else:
                return "Unknown attribute"

            teb = time.perf_counter()
            self.ttb += teb + - tsb
        finder(self.top, attribute, query)

        def maxDepth(root):       # good way to check the depth
            if root == None:       # base
                return 0
            left_Depth = maxDepth(root.left)   # revursive deep dive
            right_Depth = maxDepth(root.right)
            if left_Depth > right_Depth:
                return left_Depth + 1
            else:
                return right_Depth + 1
        # print(str(maxDepth(self.top)) + " Depth of tree")

        def Preorder(root):  # a wat to see the preorder representation of the tree
            tree = []
            if root:
                tree.append(root.data.title)
                tree = tree + Preorder(root.left)
                tree = tree + Preorder(root.right)
            return tree
        # print(Preorder(self.top))

    def __str__(self):
        return str(self.song_list)


# Main Code

songs = SongLibrary()
songs.load_library()
# print(songs)
print(str(songs.linear_search("Title", "Palavras")) + " result for linear search of Title Qing Yi Shi")
# songs.binary_tree("Title", "Palavras")
nummies = []
for i in range(100):
    nummies.append(random.randint(0, 9709))
TotalLinearTime = 0
TotalBinaryTime = 0
for i in nummies:
    songs.linear_search("Title", songs.song_list[i].title)
    TotalLinearTime = songs.ttl
    songs.binary_tree("Title", songs.song_list[i].title)
    TotalBinaryTime = songs.ttb
songs.binary_tree("Title", "Coma")

print(str(TotalLinearTime) + " Linear time")
print(str(TotalBinaryTime) + " Binary Search Tree time")
ray = input("Wanna sort and print the list? (Y/N): ")
if ray == 'Y':
    songs.quick_sort()

