import matplotlib.pyplot as ppl
import random
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry import Polygon


def line(x1,y1,x2,y2):          #JOINS THE TWO CLOSEST NODES AND PLOTS IN THE GRAPH
    x=[x1,x2]
    y=[y1,y2]
    ppl.plot(x,y,'g')


def nearest(pts,x,y):           #TO FIND THE NEAREST NODE IN THE TREE IN THE DIRECTION OF THE RANDOM POINT GENERATED 
    min=5000
    for i in pts:
        d=((x-i[0])**2+(y-i[1])**2)**0.5
        if d<min:
            temp=i
            min=d
    return temp


def nxtnode(nrst,x,y,stepd):   #TO GET THE NEXT CLOSEST NODE AND ADD IT TO THE TREE
    l=LineString([(nrst[0],nrst[1]),(x,y)])    #SHAPELY CREATES A LINE BETWEEN THE CURRETN NODE AND RANDOM POINT GENERATED IN THE WORK SPACE
    p=Point(nrst[0],nrst[1])           
    r=p.buffer(stepd).boundary              #CREATES A BOUNDARY AROUND THE POINT OF REQUIRRED RADIUS
    i=r.intersection(l)                     #FINDS THE POINT WHICH IS THE INTERSECTION OF THE LINE AND THE BOUNDARY AND TAKES THIS AS THE NEXT NODE
    return i.coords[0]                      #RETURNS THE COORDINATES OF THE NODE


def RRT(start,goal,ol):
    ppl.plot(start[0],start[1],'bo')        #PLOTS THE START AND GOAL POINTS WITH DIFFERENT COLOURS
    ppl.plot(goal[0],goal[1],'ro')
    start=(start[0],start[1],None,None)
    pts=[start]                             #LIST OF NODES THAT BECOME PART OF THE TREE
    stp=0.5                                 #MAXIMUM DISTANCE BETWEEN THE NODES IN THE TREE
    nodes=10000
    count=0
    path=[]                                 #STORE THE NEXT NODE AND PARENT NODE WHICH FORMS PATH BETWEEN THE START AND GOAL
    g=Point(goal)
    gl=g.buffer(1)                          #CREATES A RADIUS AROUND THE GOAL POINT TO SEE WHICH NODE IS WITHIN THIS CIRCLE
    polys=[Polygon(i) for i in ol]          #CREATES POLYGONS
    while count<nodes:
        x=random.uniform(0,10)
        y=random.uniform(0,10)
        nrst=nearest(pts,x,y)
        try:
            r1,r2=nxtnode(nrst,x,y,stp)
        except:
            continue
        p=Point(r1,r2)
        flag=False
        l=LineString([(r1,r2),(nrst[0],nrst[1])])
        for i in polys:                      #TO CHECK WHETHER THE NODE LIES WITHIN THE POLYGON OR ANY PATH DRAWN INTERSECT THE POLYGON
            if i.intersection(l) :
                flag=True
                break
        if flag:                            #IF FLAG IS TRUE IMPLIES IT LIES OR INTERSECTS POLYGON SO CURRENT NODE IS SKIPPED
            continue
        pts.append((r1,r2,nrst[0],nrst[1]))

        if p.within(gl):                    #CHECKS IF IT LIES WITHIN THE GOAL RADIUS
            pts.append((goal[0],goal[1],r1,r2))     #IF IT DOES IT ADDS THE GOAL POINT AS PART OF THE TREE
            t1,t2=goal[0],goal[1]
            while (t1,t2)!=(start[0],start[1]):     #THIS IS TO TRACE BACK TO THE START POINT AND ADD THESE NODES TO THE PATH LIST
                for i in pts:
                    if (i[0],i[1])==(t1,t2):
                        path.append(i)
                        t1,t2=i[2],i[3]
            break
        count+=1
    return path



def visualize(path,obs): # TO PLOT THE PATH AND POLYGONS IN THE GRAPH
    for coord in obs:
        coord.append(coord[0]) #repeat the first point to create a 'closed loop'
        xs, ys = zip(*coord) #create lists of x and y values
        ppl.plot(xs,ys)
    for i in path:
            line(i[0],i[1],i[2],i[3])
    ppl.show()







