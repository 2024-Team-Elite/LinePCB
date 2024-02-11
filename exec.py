import math, pcbnew

def isBetween(a, b, c, eps):
    distance = pointToLine(a,b,c)
    return distance < eps

def pointToLine(a,b,c):
    crossproduct = (a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0])
    return abs(crossproduct/math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2))

def pointToCircle(p, center, radius):
    distancesq = (p[0] - center[0])**2 + (p[1] - center[1])**2
    return abs(math.sqrt(distancesq) - radius)

def isOnCircle(p, center, radius, eps):
    distance = pointToCircle(p, center, radius)
    return distance < eps

    
    
def place_circle(refdes):
    # 2 is an arc
    # 0 is a line
    # 3 is a circle
    pcb = pcbnew.GetBoard()
    for rd in refdes:
        part = pcb.FindFootprintByReference(rd)
        pos = part.GetPosition()
        minDist = 10000
        for d in pcb.GetDrawings():
            if d.GetLayerName() == 'Edge.Cuts':
                if d.GetShape() == 0:
                    start = d.GetStart()
                    end = d.GetEnd()

                    minDist = min(minDist, pointToLine(start, end, pos))

                    if isBetween(start, end, pos, 500):
                        delta_y = end[1] - start[1]
                        delta_x = end[0] - start[0]
                        angle = math.atan2(delta_x, delta_y) 
                        angle *= 180/math.pi
                        angle %= 360
                        part.SetOrientationDegrees(angle)
                        print("set " + str(rd) + " to " + str(angle))
                if d.GetShape() == 2:
                    center = d.GetCenter()
                    radius = d.GetRadius()

                    minDist = min(minDist, pointToCircle(pos, center, radius))
                    # print(radius, math.sqrt((center[0] - pos[0])**2 + (center[1] - pos[1])**2))

                    if isOnCircle(pos, center, radius, 500):
                        delta_y = center[1] - pos[1]
                        delta_x = center[0] - pos[0]
                        angle = math.atan2(delta_x, delta_y) 
                        angle *= 180/math.pi
                        angle += 90
                        if angle < 0:
                            angle += 360
                        part.SetOrientationDegrees(angle)
                        print("set " + str(rd) + " to " + str(angle))
        print(str(rd) + ": " + str(minDist))





    pcbnew.Refresh()          
    print("Placement finished.")


refdes_list = []
for i in range(1,49):
    refdes_list.append("D" + str(i))
place_circle(refdes_list)
