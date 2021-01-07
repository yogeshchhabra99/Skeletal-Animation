import math
from time import sleep
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import csv
import os


SPHERE_RADIUS=0.2
PI=math.pi

global selected
selected='a'
if os.path.exists("output.csv"):
    os.remove("output.csv")

#relative to default pose
relativeAnglesDict={
    "a":0,
    "b":0,
    "c":0,
    "d":0,
    "e":0,
    "f":0,
    "g":0,
    "h":0,
    "i":0,
    "j":0,
    "k":0,
    "l":0,
    "m":0,
    "n":0,
    "z":0
}

print(relativeAnglesDict["a"])

def getColor(i):
    r= (i& 0x000000FF)>>0
    g= (i& 0x0000FF00)>>8
    b= (i& 0x00FF0000)>>16
    return (r,g,b,1.0)

class Bone():
    #must have either parent or startingPoint (one only)
    def __init__(self,startPoint, parent, rotation, length,id_,key):
        self.rotation=rotation #relative rotation
        self.parent=parent
        self.startPoint=startPoint
        self.length=length
        self.id=id_
        self.key=key
        

    def getEndPoint(self):
        if self.parent==None:
            return (
                self.startPoint[0]+self.length*math.cos(self.getRotation()),
                self.startPoint[1]+self.length*math.sin(self.getRotation()),
                0
                )
        else:
            startPoint=self.parent.getEndPoint()
            return (
                startPoint[0]+self.length*math.cos(self.getRotation()),
                startPoint[1]+self.length*math.sin(self.getRotation()),
                0
                )

    def getRotation(self):
        if self.parent==None:
            return self.rotation + relativeAnglesDict[self.key]
        else:
            return self.parent.getRotation()+self.rotation+relativeAnglesDict[self.key]

    def draw(self):
        if self.parent==None:
            center=self.startPoint
        else:
            center=self.parent.getEndPoint()

        #print("Bone")
        #print(center)
        #print(self.getRotation()*180/PI)
        glTranslatef(round(center[0],2),round(center[1],2),0)
        
        glRotatef((self.getRotation()*180)/PI-90,0,0,1)
        glRotatef(-90,1,0,0)
        glColor4f(1.0,0.0,0.0,0.0)
        glutSolidCylinder(0.06,self.length,32,32)
        glRotatef(90,1,0,0)
        glRotatef(-1*((self.getRotation()*180)/PI-90),0,0,1)
        
        glTranslatef(-1*round(center[0],2),-1*round(center[1],2),0)

    def drawVertices(self):
        pt1=self.getEndPoint()
        s1=Sphere((pt1[0],pt1[1]),SPHERE_RADIUS,self,getColor(self.id))
        s1.draw()
        if self.parent==None:
            pt2=self.startPoint
            s2=Sphere((pt2[0],pt2[1]),SPHERE_RADIUS,self,None)
            s2.draw()


class Sphere():
    def __init__(self,center,radius,bone,color):
        self.center=center
        self.radius=radius
        self.parent=bone
        self.color=color

    def draw(self):
        #print("draw sphere")
        #print(1.0*self.color[0]/255)
        #print(str(round(self.center[0],2))+","+str(round(self.center[1],2)))
        glTranslatef(round(self.center[0],2),round(self.center[1],2),0)
        
        glColor4f(1.0*self.color[0]/255,1.0*self.color[1]/255,1.0*self.color[2]/255,self.color[3])
        glutSolidSphere(self.radius,32,32)
        glTranslatef(-1*round(self.center[0],2),-1*round(self.center[1],2),0)

name = 'OpenGL Python Teapot'
eyeX=0
eyeY=0
eyeZ=20

def specialKeys(key,x,y):
    if selected=="m":
        if key==GLUT_KEY_UP:
            relativeAnglesDict["n"]=relativeAnglesDict["n"]+0.02
            glutPostRedisplay()
        
        if key==GLUT_KEY_DOWN:
            relativeAnglesDict["n"]=relativeAnglesDict["n"]-0.02
            glutPostRedisplay()

        if key==GLUT_KEY_LEFT:
            relativeAnglesDict["m"]=relativeAnglesDict["m"]-0.02
            glutPostRedisplay()
        
        if key==GLUT_KEY_RIGHT:
            relativeAnglesDict["m"]=relativeAnglesDict["m"]+0.02
            glutPostRedisplay()

        return

    if key==GLUT_KEY_LEFT:
        print("left "+selected)
        relativeAnglesDict[selected]=relativeAnglesDict[selected]+0.05
        glutPostRedisplay()

    if key==GLUT_KEY_RIGHT:
        print("right "+selected)
        relativeAnglesDict[selected]=relativeAnglesDict[selected]-0.05
        glutPostRedisplay()
    
    

def main():
    #print("main")
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(400,400)
    glutCreateWindow(name)

    glClearColor(1.,1.,1.,1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    #glEnable(GL_DEPTH_TEST)
    #glEnable(GL_LIGHTING)
    lightZeroPosition = [-20.,2.,-2.,1.]
    lightZeroColor = [1.8,1.0,0.8,1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glutDisplayFunc(display1)

    glutMouseFunc(mouseClicks)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(specialKeys)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,40.)
    glMatrixMode(GL_MODELVIEW)
    
    glPushMatrix()
    glutMainLoop()
    return

def keyboard(key,xmouse,ymouse):
    global selected
    #print(key)
    #print(xmouse)
    selected=key
    print("selected="+selected)
    

def mouseClicks(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state==GLUT_DOWN:
        #print("debug "+str(x)+","+str(y))
        c=glReadPixels(x,y,1,1,GL_RGBA,GL_FLOAT,None)
        print(str(relativeAnglesDict["a"])+","+
        str(relativeAnglesDict["b"])+","+
        str(relativeAnglesDict["c"])+","+
        str(relativeAnglesDict["d"])+","+
        str(relativeAnglesDict["e"])+","+
        str(relativeAnglesDict["f"])+","+
        str(relativeAnglesDict["g"])+","+
        str(relativeAnglesDict["h"])+","+
        str(relativeAnglesDict["i"])+","+
        str(relativeAnglesDict["j"])+","+
        str(relativeAnglesDict["k"])+","+
        str(relativeAnglesDict["l"])+","+
        str(relativeAnglesDict["m"])+","+
        str(relativeAnglesDict["n"])+","+
        str(relativeAnglesDict["z"]))
        #print(c)
        with open('output.csv', mode='a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            employee_writer.writerow([
                str(relativeAnglesDict["a"]),
                str(relativeAnglesDict["b"]),
                str(relativeAnglesDict["c"]),
                str(relativeAnglesDict["d"]),
                str(relativeAnglesDict["e"]),
                str(relativeAnglesDict["f"]),
                str(relativeAnglesDict["g"]),
                str(relativeAnglesDict["h"]),
                str(relativeAnglesDict["i"]),
                str(relativeAnglesDict["j"]),
                str(relativeAnglesDict["k"]),
                str(relativeAnglesDict["l"]),
                str(relativeAnglesDict["m"]),
                str(relativeAnglesDict["n"]),
                str(relativeAnglesDict["z"])
            ])



def rotate():
    global eyeX,eyeY,eyeZ,angle
    x=eyeX
    z=eyeZ
    angle=1*math.pi/180
    eyeX=round(x*math.cos(angle) + z*math.sin(angle),5)
    eyeZ=round(z*math.cos(angle) - x*math.sin(angle),5)
    #print(str(eyeX)+" "+str(eyeZ)) 
    glutPostRedisplay()
    sleep(0.015)
    

def display1():
    #print("display")
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    color = [1.0,0.0,0.0,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    #glRotatef(180,1,0,0)
    #glRotatef(-45,0,1,0)

    #Lookat takes the parameters of the eye, the first 3 are the position of the eye, we'll rotate this position
    gluLookAt(eyeX,eyeY,eyeZ,
              0,0,0,
              0,1,0)
    
    #s1=Sphere((0,0),SPHERE_RADIUS)
    #s1.draw()

    id_=1
    rootBone=Bone((0+relativeAnglesDict["m"],-0.5+relativeAnglesDict["n"]),None,0,0,id_,'z')
    id_=id_+1

    spineBoneLow=Bone(None,rootBone,PI/2,0.5,id_,'a')
    spineBoneLow.draw()
    spineBoneLow.drawVertices()
    id_=id_+1

    spineBoneDown=Bone(None,rootBone,-PI/2,0.5,id_,'b')
    spineBoneDown.draw()
    spineBoneDown.drawVertices()
    id_=id_+1

    spineBoneTop=Bone(None,spineBoneLow,0,2,id_,'c')
    spineBoneTop.draw()
    spineBoneTop.drawVertices()
    id_=id_+1

    rightArmBone=Bone(None,spineBoneTop,-3*PI/4,2,id_,'d')
    rightArmBone.draw()
    rightArmBone.drawVertices()
    id_=id_+1

    leftArmBone=Bone(None,spineBoneTop,3*PI/4,2,id_,'e')
    leftArmBone.draw()
    leftArmBone.drawVertices()
    id_=id_+1

    rightHandBone=Bone(None,rightArmBone,-PI/8,1.5,id_,'f')
    rightHandBone.draw()
    rightHandBone.drawVertices()
    id_=id_+1

    leftHandBone=Bone(None,leftArmBone,PI/8,1.5,id_,'g')
    leftHandBone.draw()
    leftHandBone.drawVertices()
    id_=id_+1

    leftLegUpper=Bone(None, spineBoneDown,-PI/6,1.7,id_,'h')
    leftLegUpper.draw()
    leftLegUpper.drawVertices()
    id_=id_+1

    rightLegUpper=Bone(None, spineBoneDown,PI/6,1.7,id_,'i')
    rightLegUpper.draw()
    rightLegUpper.drawVertices()
    id_=id_+1

    leftLegBotton=Bone(None,leftLegUpper,PI/10,2,id_,'j')
    leftLegBotton.draw()
    leftLegBotton.drawVertices()
    id_=id_+1

    rightLegBotton=Bone(None,rightLegUpper,-1*PI/10,2,id_,'k')
    rightLegBotton.draw()
    rightLegBotton.drawVertices()
    id_=id_+1

    head=Bone(None,spineBoneTop,0,1,id_,'l')
    head.draw()
    head.drawVertices()


    glPopMatrix()
    glutSwapBuffers()
    
    return

if __name__ == '__main__': main()
