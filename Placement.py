import math, pcbnew



def between_two_numbers(a,b,num):
    return (min(a, b) <= num <= max(a, b))

def reverseAngle(center, outline):
    distance = math.sqrt((math.pow((center[0]-outline[0]),2)) + (math.pow((center[1]-outline[1]),2)))
    inverseX = outline[0]-center[0]
    inverseY = center[1]-outline[1]
    inverseX = inverseX/distance
    inverseY = inverseY/distance
    rVal = math.degrees(math.atan2(inverseX,inverseY))
    if(rVal < 0):
        rVal = rVal + 360
    return rVal

    
def place_circle(refdes, channelOffset=0):
    pcb = pcbnew.GetBoard()
    len_refdes = len(refdes)
    circles = []
    for d in pcb.GetDrawings():
      if d.GetLayerName() == 'Edge.Cuts' and d.GetShape() == 3:
        circles.append(d)
    len_circles = len(circles)

    circlesSorted = []
    usedCircles = [circles[0]]
    refdes = refdes[channelOffset:] + refdes[:channelOffset]
    for j in range(len(circles)):
        shortestDistance = 1000000000000000000000
        closestCircle = circles[0]
        for i in range(len(circles)):
            if circles[i] not in usedCircles:
                distance = math.sqrt((math.pow((usedCircles[-1].GetCenter().Get()[0]-circles[i].GetCenter().Get()[0]),2)) + (math.pow((usedCircles[-1].GetCenter().Get()[1]-circles[i].GetCenter().Get()[1]),2)))
                if distance < shortestDistance:
                    shortestDistance = distance
                    closestCircle = circles[i]
        circlesSorted.append(closestCircle)
        usedCircles.append(closestCircle)
    

    for i in range(len(refdes)):    
      part = pcb.FindFootprintByReference(refdes[i])
      center = circlesSorted[i].GetCenter()
      part.SetPosition(center)
    
    
        
    pcbnew.Refresh()          
    print("Placement finished.")



pcb = pcbnew.GetBoard()
# To Find all Sensors
refdes_sensor = []
for i in range(1,49):
    for j in range(1,len(pcb.GetFootprints())):
        footprint = pcb.FindFootprintByReference("D" + str(j))
        if footprint is not None:
            
            for pad in footprint.Pads():
                netcode = pad.GetNet().GetNetname()
                if netcode == "Ch" + str(i):
                    refdes_sensor.append("D" + str(j))

# To Find all sensor resistors
refdes_sensorRes = []
for i in range(1,49):
    for j in range(1,len(pcb.GetFootprints())):
        footprint = pcb.FindFootprintByReference("R" + str(j))
        if footprint is not None:
            
            for pad in footprint.Pads():
                netcode = pad.GetNet().GetNetname()
                if netcode == "Ch" + str(i):
                    refdes_sensorRes.append("R" + str(j))

# To Find all LEDs
refdes_led = []
for j in range(1,len(pcb.GetFootprints())):
    footprint = pcb.FindFootprintByReference("D" + str(j))
    if footprint is not None:
        
        for pad in footprint.Pads():
            netcode = pad.GetNet().GetNetname()
            if netcode.find("D"+str(j)) != -1:
                refdes_led.append("D" + str(j))
            
# To Find all LED Resistors
### Must run LEDs search first before running this
refdes_ledRes = []
for j in range(1,len(pcb.GetFootprints())):
    footprint = pcb.FindFootprintByReference("R" + str(j))
    for i in refdes_led:
      if footprint is not None:
          for pad in footprint.Pads():
              netcode = pad.GetNet().GetNetname()
              if netcode.find(i) != -1:
                  refdes_ledRes.append("R" + str(j))
