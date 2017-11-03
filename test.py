import networkx as nx
import numpy as np
import copy as cp
from requests import Requests
from wavelength import Wavelength

number_of_requests = 3
a = 5
muy = 1
lam = a * muy

# Generate network

G = nx.Graph()
for index in range(1, 18):
    G.add_node(index)
for index in range(1, 17):
    G.add_edge(index, index + 1, weight=0)
G.add_edge(17, 1, weight=0)
G.add_edge(17, 2, weight=0)
G.add_edge(17, 3, weight=0)
G.add_edge(17, 10, weight=0)
G.add_edge(17, 14, weight=0)
G.add_edge(17, 16, weight=0)
G.add_edge(16, 1, weight=0)
G.add_edge(14, 11, weight=0)
G.add_edge(10, 3, weight=0)
G.add_edge(10, 4, weight=0)
G.add_edge(7, 4, weight=0)

edges = list(G.edges())
comEdges = {}

for index in range(0, G.number_of_edges()):
    comEdges[edges[index]] = Wavelength()

# Generate source and destination
while True:
    check = False
    source = np.random.randint(1, 18, number_of_requests)
    destination = np.random.randint(1, 18, number_of_requests)
    for index in range(0, number_of_requests):
        if source[index] == destination[index]:
            check = True
    if not check:
        break


# Generate exponential interval time and holding time of requests
def generate_time(mean, n_o_r):
    while True:
        condition = False
        time = np.random.exponential(mean, n_o_r)
        for t in time:
            if t == 0: condition = True
        if not condition: break
    return time


events_time = generate_time(1 / lam, number_of_requests)
holding_time = generate_time(1 / muy, number_of_requests)

s = 0
time = []
for e in events_time:
    s += e
    time.append(s)

time_line = []
for index in range(0, number_of_requests):
    time_line.append(time[index] + holding_time[index])

time_new = time + time_line
# print("before",timeNew)

# sort the whole time line
for index in range(len(time_new)):
    for j in range(len(time_new) - 1 - index):
        if time_new[j] > time_new[j + 1]:
            time_new[j], time_new[j + 1] = time_new[j + 1], time_new[j]


# put each request into a list
Req = []
for index in range(0, number_of_requests):
    req = Requests(time[index], time_line[index], source[index], destination[index], index)
    Req.append(req)

# put each request into a list following time_new
Events = []
for index in range(len(time_new)):
    for req in Req:
        if req.inTime == time_new[index]:
            Events.append(req)
        elif req.outTime == time_new[index]:
            temp = cp.copy(req)
            temp.isCall = 1
            Events.append(temp)

print(len(Events))


def binding_edges(request):
    print("src:", request.source)
    print("des:", request.des)
    # while True:
    #     check = False
    request.path = nx.shortest_path(G, request.source, request.des, weight='weight')
    for i in range(0, len(request.path) - 1):
        for edges in comEdges:
            if edges == (request.path[i], request.path[i + 1]) or edges == (request.path[i + 1], request.path[i]):
                comEdges[edges].use_wavelength(1)
                print("wavelength 1 on ", edges, ": ", comEdges[edges].get_wavelength(1))
    request.printDetails()
    for e in Events:
        if e != request and e.inTime == request.inTime:
            e.path = request.path
            e.printDetails()
            print()
            break
            # for i in range(0, len(req.path) - 1):
            #     for edges in comEdges:
            #         if edges == (req.path[i], req.path[i+1]) or edges == (req.path[i+1], req.path[i]):
            #             comEdges[edges].fiber1[1] += 1
            #             print(edges, comEdges[edges].fiber1)

            # if G[req.path[i]][req.path[i+1]]['weight'] < 1:
            #     G[req.path[i]][req.path[i + 1]]['weight'] += 1
            # elif


def release_edges(request):
    request.path = []


for e in Events:
    if e.isCall == 0:
        binding_edges(e)
    elif e.isCall == 1:
        release_edges(e)
        # for e in Events:
        #     if e != Events[0] and e.inTime == Events[0].inTime:
        #         e.path = Events[0].path
        #         e.printDetails()

        # print(G.number_of_nodes())
        # print(events)
        # print(holding_time)
        # print(time)
        # print(time_line)
        # print("final source:     ", source)
        # print("final destination:", destination)