# This is SpringPaper, a Chinese papercut art simulator!
from cmu_graphics import *
import math
import copy


# PaperCut Class
class PaperCut:
    def __init__(self, folds = 6, radius = 200, cx = 200, cy = 200): # default settings for sector
        self.folds = folds
        self.radius = radius
        self.sectorAngle = 360 / folds
        self.cutPaths = []
        self.currentPath = []
        self.cx = cx
        self.cy = cy
        self.paperColor = "red"

    def inSector(self, x, y ):
        cx, cy = self.cx, self.cy
        dx, dyMath = x - cx, cy -y
        r = math.hypot(dx, dyMath)
        
        if r > self.radius:
            return False
        
        angle = math.degrees(math.atan2(dyMath, dx))
        if angle <0:
            angle+=360
        
        # return sector angle to be at middle
        mid = 90
        half = self.sectorAngle /2
        start = (mid - half) % 360
        end = (mid + half) % 360
        if start <= end:
            return start <= angle <= end
        else: return angle >= start or angle<=end
        
    def addPoint(self, x, y):
        if self.inSector(x, y):
            self.currentPath.append((x,y)) # do real cut on
            

    def drawSector(self, cx, cy, themeColor):
        self.cx = cx
        self.cy=cy
        r = self.radius
        mid = 90
        start = mid - self.sectorAngle / 2
        sweep = self.sectorAngle
        
        # Draw the arc here
        drawArc(cx, cy, 2* r, 2*r,start, sweep, fill = self.paperColor)
            
            
        # drawArc(cx, cy, 2* r, 2*r,start, sweep, fill = gradient(self.paperColor, "fireBrick", start = "top"))
        
        
        
        drawArc(cx, cy, 2* r, 2*r,start, sweep, fill = None, border = "darkred", borderWidth = 3, opacity = 50)
        
        # draw the paths
        for path in self.cutPaths: # finished paths
            self.drawPathLines(path, "black", 3) # color and width
            self.drawFilledCut(path,themeColor)
        if len(self.currentPath) > 1: # new paths ing
            self.drawPathLines(self.currentPath, "black", 3)
            
    def drawFinal(self, cx, cy, themeColor):
        self.cx = cx
        self.cy = cy
        cx, cy = self.cx, self.cy
        r = self.radius
        #draw the circle
        # drawCircle(cx, cy ,r, fill = self.paperColor)
        drawCircle(cx+6, cy+6 ,r, fill = "black", opacity =25)
        drawCircle(cx, cy, r, fill = self.paperColor)
        drawCircle(cx, cy, r, fill = None, border = "darkred", borderWidth = 3, opacity = 60)

        for i in range(self.folds):
            theta = math.radians(i*self.sectorAngle)
            cosTrans = math.cos(theta)
            sinTrans = math.sin(theta)
            
            mirror = (-1 if (i%2 ==1)else 1)
            
            for path in self.cutPaths:
                transformed = []
                for (x, y) in path:
                    dx = x - cx
                    dyMath = cy -y
                    
                    dx *= mirror
                    
                    x2 = dx * cosTrans - dyMath * sinTrans
                    y2 = dx * sinTrans + dyMath * cosTrans
                    
                    transformed.append((cx+x2,cy-y2))
                self.drawFilledCut(transformed, themeColor)
                
                
    def drawPathLines(self, path, color, width):
        for i in range(len(path)-1):
            (x1, y1) = path[i]
            (x2, y2) = path[i+1]
            drawLine(x1, y1, x2, y2, fill = color, lineWidth = width)
    
    def drawFilledCut(self, path, themeColor):
        flat = []
        for (x, y) in path:
            flat += [x,y]
        if len(flat) >= 6:
            drawPolygon(*flat, fill = themeColor)
        # drawPolygon(*flat, fill = "white")
    

# -------------------------------------------------------------------
# auto-connect when cutting on the edges


    def finishCut(self):
        if len(self.currentPath)<3:
            self.currentPath = []
            return
        
        path = self.currentPath[:]
        start=path[0]
        end=path[-1]
        
        cx, cy = self.cx, self.cy
        r = self.radius
        
        def angleOf(point):
            dx = point[0] - cx
            dyMath = cy - point[1]
            return math.degrees(math.atan2(dyMath, dx)) % 360
        
        # if one point on the curve
        def snapToArc(point):
            a = angleOf(point)
            rad =math.radians(a)
            return (cx+r*math.cos(rad), cy - r*math.sin(rad))
            
        def snapToSide(point, isLeft):
            mid = 90
            half = self.sectorAngle /2
            ang = math.radians(mid-half if isLeft else mid+half)
            dx = math.cos(ang)
            dy = -math.sin(ang)
            t = ((point[0]- cx)*dx + (point[1] - cy) * dy)
            t = max(0, min(r, t))
            
            return (cx + t*dx, cy + t* dy)
            
        def whichEdge(point):
            realR= math.hypot(point[0]- cx, cy - point[1])
            if abs(realR -r)<8:
                return "arc"
            a = angleOf(point)
            mid = 90
            half= self.sectorAngle/2
            startAng = (mid-half)%360
            endAng= (mid+half)% 360
            def diff(u, v):
                return min (abs(u-v), 360-abs(u-v))

            if diff(a, startAng) < 6: # can adjust here
                return "left"
            elif diff(a, endAng) < 6:
                return "right"
            return None
            
        startEdge = whichEdge(start)
        endEdge= whichEdge(end)
        
        # if perfectly closed
        if math.hypot(start[0]-end[0], start[1]-end[1]) < 20:
            path.append(path[0])
            self.cutPaths.append(path)
            self.currentPath=[]
            return 
        
        # if both points on edge
        if startEdge and endEdge:
            if startEdge == endEdge == "arc":
                a1= angleOf(start)
                a2 = angleOf(end)
                if (a2-a1) % 360 > 180:
                    a1, a2 = a2, a1
                for i in range(1, 12):
                    a = a1 + (a2-a1) * i/12
                    rad =math.radians(a)
                    path.append((cx+r*math.cos(rad), cy- r*math.sin(rad)))
            elif startEdge == endEdge == "left":
                start = snapToSide(start, True)
                end = snapToSide(end, True)
                path = [start] + path + [end]
                
            elif startEdge== endEdge == "right":
                start = snapToSide(start, False)
                end = snapToSide(end, False)
                path = [start] + path + [end]
           
                    
            path.append(path[0])
            self.cutPaths.append(path)
        
        
        self.currentPath=[]
        
        
            
    def isOnLeftEdge(self, x, y, toleA = 6):
        cx, cy = self.cx, self.cy
        r, angle = self.polarOf(x,y)
        
        mid = 90
        half=slef.sectorAngle/2
        startAng = (mid - half)% 360
        
        def angDiff(a, b):
            d = abs(a-b)% 360
            return min(d, 360-d)
            
        return angDiff(angle, startAng) < toleA and r <= self.radius +10
    
    def isOnRightEdge(self, x, y, toleA=6):
        cx, cy = self.cx, self.cy
        r, angle = self.polarOf(x, y)
        
        mid = 90
        half=slef.sectorAngle/2
        endAng = (mid + half)% 360
        
        def angDiff(a, b):
            d = abs(a-b)% 360
            return min(d, 360-d)
            
        return angDiff(angle, startAng) < toleA and r <= self.radius +10
        
    def isOnArc(self, x, y, toleR=10):
        r, temp = self.polarOf(x,y)
        return abs(r - self.radius)< toleR
    
    def edgeType(self, x, y):
        if self.isOnArc(x, y) == True:
            return "arc"
        if self.isOnLeftEdge(x, y)== True:
            return "left"
        if self.isOnRightEdge(x, y)== True:
            return "right"
            
        return None
        
def drawSectorAtAngle(cx, cy, r, startDegree, sweepDegree, color):
    points = [(cx, cy)]
    steps = 60 # "pixel" of the arc
    for i in range(steps + 1):
        angle = math.radians(startDegree + sweepDegree * i / steps)
        x = cx + r* math.cos(angle)
        y = cy + r* math.sin(angle)
        points.append((x,y))
    flatPoints= []
    for (x,y) in points:
        flatPoints += [x, y]
    drawPolygon(*flatPoints, fill =color) 
# -------------------------------------------------------------------
# Real App here
def onAppStart(app):
    
    app.mode = "cut"
    app.width = 750
    app.height =500
    app.cx = app.width/2
    app.cy = app.height/2
    app.holdingC = False
    app.paper = PaperCut(folds =6,cx = app.cx, cy = app.cy)
    app.mouseX = None
    app.mouseY = None
    
    # for paper color control
    app.colorGradient = ["darkred", "red", "crimson", "tomato", "hotPink", "deepPink", "mediumVioletRed", "pink", "royalBlue", "blue","purple"]
    app.currentPaperColor = app.colorGradient[1] # make it default red
    app.sliderX= 80
    app.sliderY= app.height-30
    app.sliderW = app.width -160
    app.sliderNowX = app.sliderX + 1/(len(app.colorGradient)-1)*app.sliderW
    app.sliderDragging = False
    app.paper.paperColor = app.currentPaperColor
    
    # for background theme control:
    app.themes = [("lightyellow", "white"), ("linen","oldLace"), ("burlywood", "linen"), ("lightYellow", "cornsilk"), ("lavender", "thistle")]
    app.currentTheme = 0
    app.boxSize= 40
    
    # add pre-set shapes
    app.shapePalette = [{"kind":"circle", "cx" : 50, "cy": 120, "size":18},
    {"kind":"square", "cx" : 50, "cy": 170, "size":18},
    {"kind":"triangle", "cx" : 50, "cy": 220, "size":20},
    {"kind":"star", "cx" : 50, "cy": 270, "size":20},
    {"kind":"diamond", "cx" : 50, "cy": 320, "size":20},
    {"kind":"petal", "cx" : 50, "cy": 370, "size":18}
    ]
    
    app.dragShape = None
    app.dragX = None
    app.dragY = None
    
    # store pics
    app.sampleImages = "cmu://1073090/43668026/paperArtSamples.jpg"
    # store sounds
    app.popSound =Sound("cmu://1073090/43668105/pop-402324.mp3")
    
# def onStep(app):
#     app.cx = app.width/2
#     app.cy = app.height/2
#     app.paper.cx = app.cx
#     app.paper.cy = app.cy
    
def mainScreen_redrawAll(app):
    # background 
    outer, inner = app.themes[app.currentTheme]
    drawRect(0,0, app.width,app.height, fill = outer)
    drawRect(5, 5, app.width - 10, app.height -10, fill = inner)
    
    # switch screens
    drawRect(app.width- 150, 20, 130, 30, fill = "lavender")
    drawLabel("Instructions", app.width- 85, 35, size = 14)
    drawRect(app.width- 150, 60, 130, 30, fill = "lavender")
    drawLabel("Samples", app.width- 85,75, size = 14)
    
    
    # titles
    # drawRect(0, 0, app.width, app.height, fill = None, borderWidth = 4, border = "lightyellow")
    drawLabel("SpringPaper", 20, 20, size = 30, font="caveat", bold= True, align = "left")
    drawLabel("A Chinese Papercut", 20, 50, size = 22, font="caveat", bold= True, align = "left")
    drawLabel("Art Simulator", 20, 75, size = 22, font="caveat", bold= True, align = "left")
    # drawLabel("Press r to restart", app.width/2, 15, size = 22, font = "caveat")
    

    
    
    
    if app.mode == "cut":
    
        # drawLabel("Press 6 or 8 to choose your sector size",  app.width/2, 30, size = 15, font = "caveat")
        # drawLabel("Press c and mouse to cut", app.width/2, 40, size = 15, font = "caveat")
        # drawLabel("Press d to display your art!",  app.width/2, 50, size = 15, font = "caveat")
        # drawLabel("Press b to back one cut step!",  app.width/2,60, size = 15, font = "caveat")
        
        # # draw color selection here
        # drawLabel("Select paper color: ", 80, 470, font = "caveat", size = 20)
        
        app.paper.drawSector(app.cx, app.cy, inner)
        
        
        if app.holdingC and app.mouseX!=None and app.mouseY !=None:
            size =9
            x, y = app.mouseX,app.mouseY
            drawLine(x-size, y-size, x+size, y+size, fill = "snow", lineWidth = 3)
            drawLine(x-size,  y+size, x+size, y-size, fill = "snow", lineWidth =3)
            
        # draw the color slider
        # drawLabel(app.currentPaperColor, app.sliderNowX, app.sliderY-20, size =12, bold= True)
        drawLabel("Paper Color", app.sliderNowX, app.sliderY-20, size =12, bold= True)
        drawRect(app.sliderX, app.sliderY-5, app.sliderW, 10, fill = gradient("darkred", "red", "hotPink", "royalBlue","purple", start="left"))
        drawCircle(app.sliderNowX, app.sliderY, 10, fill = "black")


        # draw shape selections
        for shape in app.shapePalette:
            drawShape(shape["kind"], shape["cx"], shape["cy"], shape["size"], outline = "black", fill =None)
            
        if app.dragShape != None and app.dragX != None:
            drawShape(app.dragShape["kind"], app.dragX, app.dragY, app.dragShape["size"], outline ="black", fill = None)
        
        

        # draw theme selection boxes
        size = app.boxSize
        startX = app.width - 70
        startY= 100
        
        for i in range(5):
            bgOuter, bgInner = app.themes[i]
            y = startY + i*(size + 15)
            drawRect(startX, y, size, size, fill = bgOuter)
            drawRect(startX +8, y +8, size-16, size -16, fill = bgInner)
        
            if i == app.currentTheme:
                drawCircle (startX+size/2, y + size/2,  5, fill = "black")
        
    elif app.mode == "display":
        drawLabel("Here is your paper flower. Awesome job!", app.width/2, app.height - 22, size = 22, font="caveat", bold= True)
        app.paper.drawFinal(app.cx, app.cy, inner)
    
    
    
    
def mainScreen_onMousePress(app, mouseX, mouseY):
    if app.width-150<=mouseX<=app.width-20 and 20<=mouseY<= 50:
        setActiveScreen("instructions")
        app.popSound.play(restart=True)
        return
    if app.width-150<=mouseX<=app.width-20 and 60<=mouseY<= 90:
        setActiveScreen("samples")
        app.popSound.play(restart=True)
        return
    
    # select shape
    for shape in app.shapePalette:
        if hitShape(shape, mouseX, mouseY):
            app.dragShape= shape
            app.dragX = mouseX
            app.dragY = mouseY
            return
    
    #select background theme
    size = app.boxSize
    startX = app.width-70
    startY = 100
    for i in range(5):
        y = startY + i * (size +15)
        if startX <= mouseX<= startX + size and y <=mouseY<= y+size:
            app.currentTheme =i
            return
    
    # others
    if insideSlider(app, mouseX, mouseY):
        app.sliderDragging = True
    elif app.mode== "cut" and app.holdingC== True:
        app.paper.currentPath = [(mouseX, mouseY)]
        app.paper.addPoint(mouseX, mouseY)
    

def mainScreen_onMouseDrag(app, mouseX, mouseY):
    
    if app.dragShape !=None:
        app.dragX = mouseX
        app.dragY = mouseY
        return
    
    if app.mode== "cut" and app.holdingC == True:
        app.paper.addPoint(mouseX, mouseY)
        app.mouseX = mouseX
        app.mouseY = mouseY
        
    if app.sliderDragging == True:
        app.sliderNowX = max(app.sliderX, min(mouseX, app.sliderX+ app.sliderW))
        updatePaperColor(app)
    
def mainScreen_onMouseRelease(app, mouseX, mouseY):
    if app.dragShape != None:
        kind = app.dragShape["kind"]
        cxS, cyS = app.dragX, app.dragY
    
        if app.paper.inSector(cxS, cyS):
            path = createShapePath(kind, cxS, cyS, app.dragShape["size"])
            if len(path) >= 3:
                path.append(path[0])
                app.paper.cutPaths.append(path)
        app.dragShape = None
        app.dragX = None
        app.dragY = None
        return
    
    if app.mode == "cut":
        app.paper.finishCut()
        app.mouseX = None
        app.mouseY = None
    app.sliderDragging = False
    
def mainScreen_onKeyPress(app, key):
    if key == "6":
        app.paper= PaperCut(folds = 6, radius = app.paper.radius, cx = app.cx, cy = app.cy)
    elif key == "8":
        app.paper=PaperCut(folds = 8, radius = app.paper.radius, cx = app.cx, cy = app.cy)
    elif key == "d":
        app.mode="display"
        app.popSound.play(restart=True)

        
    elif key == "c":
        app.holdingC = True
        
    elif key == "r":
        app.mode = "cut"
        app.paper.cutPaths= []
        app.popSound.play(restart=True)
        
    elif key=="b": # back one step
        if len(app.paper.cutPaths)>0:
            app.popSound.play(restart=True)
            app.paper.cutPaths.pop()
            
            
    
def mainScreen_onKeyRelease(app, key):
    if key == "d":
        app.mode="cut"
       
    elif key == "c":
        app.holdingC = False
    
# for the color selection slider
def insideSlider(app, mouseX, mouseY):
    return abs(mouseX-app.sliderNowX) < 12 and abs(mouseY - app.sliderY)<12
    
def updatePaperColor(app):
    ratio = (app.sliderNowX - app.sliderX) / app.sliderW
    index = int(ratio*(len(app.colorGradient)-1))
    index = max(0, min(index, len(app.colorGradient)-1))
    app.currentPaperColor = app.colorGradient[index]
    app.paper.paperColor = app.currentPaperColor
    
    
def createShapePath(kind, cx, cy, size):
    points = []
    if kind =="circle":
        steps = 24
        for i in range(steps):
            angle = 2* math.pi *i / steps
            x = cx + size*math.cos(angle)
            y = cy + size*math.sin(angle)
            points.append((x, y))
    elif kind == "square":
        points = [(cx - size, cy -size), (cx + size, cy -size), (cx + size, cy + size), (cx - size, cy + size),]
    elif kind == "triangle":
        points = [(cx, cy -size), (cx+size, cy +size), (cx - size, cy + size),]
        
    elif kind == "diamond":
        points = [(cx, cy -size), (cx-size, cy), (cx, cy+size), (cx + size, cy),]
        
    elif kind == "star":
        for i in range(10):
            angleDegree = -90 + 36*i
            angle = math.radians(angleDegree)
            if i % 2 ==0:
                r = size
            else: r = size*0.4
            x = cx + r*math.cos(angle)
            y= cy + r* math.sin(angle)
            points.append((x,y))
    elif kind == "petal":
        steps = 100
        for i in range(steps):
            angle= 2 * math.pi * i/steps
            r = size *(0.6+0.4*math.cos(5*angle))
            x = cx + r*math.cos(angle)
            y= cy + r* math.sin(angle)
            points.append((x,y))
    return points
    
def drawShape(kind, cx, cy, size, outline = "black", fill = None):
    path = createShapePath(kind, cx, cy, size)
    flatPath = []
    for (x,y) in path:
        flatPath.extend([x,y])
    drawPolygon(*flatPath, fill = fill, border = outline)

def hitShape(shape, x, y): # determine only by the square block
    cx = shape["cx"]
    cy = shape["cy"]
    size= shape["size"]
    return (abs(x-cx) <= size ) and (abs(y-cy) <= size)


# -------------------------------------------------------------------
# Instruction screen
def instructions_redrawAll(app):
    drawLabel("How to use SpringPapar", app.width/2, 60, size =35, bold= True, font = "caveat")
    y = 100
    dy = 30
    drawLabel("- Press 6 or 8: change sector folds", app.width/2, y+dy, size = 20, font = "caveat")
    drawLabel("- Press C and press mouse: cut freely", app.width/2, y+2*dy, size = 20, font = "caveat")
    drawLabel("- Press D: display full paper", app.width/2, y+3*dy, size = 20, font = "caveat")
    drawLabel("- Press B: undo last cut", app.width/2, y+4*dy, size = 20, font = "caveat")
    drawLabel("- Press R: restart", app.width/2, y+5*dy, size = 20, font = "caveat")
    drawLabel("- Drag shapes from left to cut", app.width/2, y+6*dy, size = 20, font = "caveat")
    drawLabel("- Select background-theme from right", app.width/2, y+7*dy, size = 20, font = "caveat")
    drawLabel("- Change paper color at the bottom", app.width/2, y+8*dy, size = 20, font = "caveat")
    
    # back button
    buttonX = app.width/2 - 70
    buttonY = app.height - 90
    drawRect(buttonX, buttonY, 140, 40, fill = "pink")
    drawLabel("Back to Main", app.width/2, buttonY + 20, size = 18)
    
def instructions_onMousePress(app, mouseX, mouseY):
    buttonX = app.width/2 - 70
    buttonY = app.height - 90
    if buttonX<=mouseX <= buttonX + 140 and buttonY<= mouseY <= buttonY+40:
        app.popSound.play(restart=True)
        setActiveScreen("mainScreen")
    
# -------------------------------------------------------------------


# -------------------------------------------------------------------
# Samples screen
def samples_redrawAll(app):
    drawLabel("Sample designs below, and have fun!", app.width/2, 60, size =35, bold= True, font = "caveat")
    
    url = app.sampleImages 
    
    imageW, imageH = getImageSize(url)
    scale = 0.45
    drawImage(url, app.width/2,app.height/2-5, width = imageW*scale, height = imageH * scale, align="center")
    
    
    # back button
    buttonX = app.width/2 - 70
    buttonY = app.height - 90
    drawRect(buttonX, buttonY, 140, 40, fill = "pink")
    drawLabel("Back to Main", app.width/2, buttonY + 20, size = 18)
    
def samples_onMousePress(app, mouseX, mouseY):
    buttonX = app.width/2 - 70
    buttonY = app.height - 90
    if buttonX<=mouseX <= buttonX + 140 and buttonY<= mouseY <= buttonY+40:
        app.popSound.play(restart=True)
        setActiveScreen("mainScreen")
    
# -------------------------------------------------------------------
    
    
def main():
    print('Program starts!')
    # -------------------------------------------------------------------
    # To read files from GitHub
    def readFile(path):
        with open(path) as f:
            return f.read()
            
    path = 'https://raw.githubusercontent.com/Jacky-111111/SpringPaper/main/description.txt'
    contents = readFile(path)
    print(contents)
    # -------------------------------------------------------------------
    
    # runApp()
    runAppWithScreens(initialScreen="mainScreen")
    


main()
