import maya.cmds as cmds
import random as rnd
from random import randint
import math
import random

if 'myWin' in globals():
    if cmds.window(myWin, exists=True):
        cmds.deleteUI(myWin, window=True)

myWin = cmds.window(title="Tree Gen", menuBar = True)

cmds.menu(label="File")

cmds.menuItem(label="NewScene", command=('cmds.file(new=True, force=True)'))


cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,100), (2,100)])

cmds.setParent('..')




cmds.frameLayout(collapsable=False, label="Fractal Degree", width=500)
cmds.intSliderGrp('fracDeg',l="Fractal Degree", f=True, min=1, max=7, value=7)
cmds.setParent('..')

cmds.frameLayout(collapsable=False, label="Tree Height", width=500)
cmds.intSliderGrp('treeHeight', l="Tree Height", f=True, min=5, max=10, value=7)
cmds.setParent('..')


cmds.frameLayout(collapsable=False, label="Season", width=500)
cmds.rowColumnLayout(numberOfColumns=4, columnWidth=[(1,125), (2,125), (3,125), (4,125)])
cmds.radioCollection(nci=True)
cmds.radioButton('spring', label='Spring', sl=True)
cmds.radioButton('summer', label='Summer')
cmds.radioButton('fall', label='Fall')
cmds.radioButton('winter', label='Winter')


cmds.setParent('..')
cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1,500)])
cmds.button(label="Generate Tree", command=('generateTree()'))
cmds.setParent('..')

cmds.showWindow(myWin)

def generateTree():
    
    season = 1
    
    seasonRad = cmds.radioButton('spring', query = True, select = True)
    if seasonRad == True:
        season = 1
    
    seasonRad = cmds.radioButton('summer', query = True, select = True)
    if seasonRad == True:
        season = 2
        
    seasonRad = cmds.radioButton('fall', query = True, select = True)
    if seasonRad == True:
        season = 3
        
    seasonRad = cmds.radioButton('winter', query = True, select = True)
    if seasonRad == True:
        season = 4
    
    cmds.select( d=True )
    
    fracDeg = cmds.intSliderGrp('fracDeg', q=True, v=True)
    treeHeight = cmds.intSliderGrp('treeHeight', q=True, v=True)
    
    branchCountA = 1
    branchCountB = 1
    maxJnts = 7
    yVal = 0
    angle = 10
    zTrans = 4
    maxY = 20
    planeCnt = 1
    
####### creating base structure ######
    
    for i in range(1, treeHeight):
        strNum = str(i)
        name = "base" + strNum
        angleDeg = randint(-10,10)
        yVal = randint(8,maxY)
        
        if i == 1:
            cmds.joint(r = True, angleX=angleDeg, n=name, p=(0, 0, 0) )
        else:
            cmds.joint(r = True, angleX=angleDeg, n=name, p=(randint(-3, 3), yVal, 0) )
        maxY -= 1
        
        if season != 4:
            if i == (treeHeight - 1):
                cmds.select(name)
                jointPosWorld = cmds.joint(name, a=True, query=True, p=True)
                generateLeaf(jointPosWorld, planeCnt, name)
                planeCnt += 1

####### creating primary main branch from the third last joint of the base, this makes all the fractal degrees as specified by user ######

    startingJnt = str((treeHeight - 3))
    growFrom = 'base' + startingJnt #dynamically finds the third highest joint from the base and starts growing from there
    
    for i in range(1,fracDeg):
        
        cmds.select( growFrom )
        
        yVal = 0
        
        for i in range(1,maxJnts):
            strNum = str(i)
            branchNumA = str(branchCountA)
            name = "branchA"+ branchNumA + "_" + strNum
            yVal = randint(3,9)
            angle = randint(-15,15)
            cmds.joint(r = True, angleX=angle, n=name, p=(randint(-10, 10), yVal, zTrans) )
            
            if season != 4:
                if i == (maxJnts - 1):
                    cmds.select(name)
                    jointPosWorld = cmds.joint(name, a=True, query=True, p=True)
                    generateLeaf(jointPosWorld, planeCnt, name)
                    planeCnt += 1
        
        origin = str((maxJnts / 3))
        growFrom = "branchA"+ branchNumA + "_" + origin
        
        zTrans *= 1
        angle *= 1
        yVal = 0
        branchCountA += 1
        maxJnts -=1
    
    
    maxJnts = 7
    zTrans = 4
    maxY = 20


    ####### creating secondary main branch from the second last joint of the base ######
    
    growFrom = 'base' + (str((treeHeight - 2)))
    randFracDeg = (randint(1, fracDeg))
    for i in range(1, randFracDeg):
        
        cmds.select( growFrom )
        
        yVal = 0
        
        for i in range(1,maxJnts):
            strNum = str(i)
            branchNumB = str(branchCountB)
            name = "branchB"+ branchNumB + "_" + strNum
            yVal = randint(3,9)
            angle = randint(-45,45)
            cmds.joint(r = True, angleX=angle, n=name, p=(randint(-10, 10), yVal, zTrans) )
            
            if season != 4:
                if i == (maxJnts - 1):
                    cmds.select(name)
                    jointPosWorld = cmds.joint(name, a=True, query=True, p=True)
                    generateLeaf(jointPosWorld, planeCnt, name)
                    planeCnt += 1            
        
        origin = str((maxJnts / 3))
        growFrom = "branchB"+ branchNumB + "_" + origin
        
        zTrans *= 1
        angle *= 1
        yVal = 0
        branchCountB += 1
        maxJnts -=1
    
    #### initial cylinder setup for base
    rotationVal=cmds.joint('base1', query=True,ax=True, ay=True, az=True)
    rotationValRelative=cmds.joint('base1', query=True,ax=True, ay=True, az=True, r=True)
    
    jointPosWorld = cmds.joint('base1', a=True, query=True, p=True)
    jointPosRelative = cmds.joint('base1', r=True, query=True, p=True)

    
    cmds.polyCylinder(n='bark', sx=20, sy=0, sz=0, h=8, r = 2)
    cmds.move(8/2, y=True)
    cmds.select( d=True )
    
    
    #select and delete cylinder faces, reorient pivot, flip remaining face (normal reverse didn't work on one face)
    for i in range(20): 
        cmds.select('bark.f[' + (str(i)) + ']', add=True)
    cmds.select('bark.f[21]', add=True)
    cmds.delete(s=True)
    cmds.select('bark')
    cmds.move(0, 0, 0, "bark.scalePivot","bark.rotatePivot", absolute=True)
    cmds.rotate(180, rotateZ=True, r=True)
    cmds.rotate(str(rotationVal[0])+'deg', str(rotationVal[1])+'deg', str(rotationVal[2])+'deg', r=True)
    
    #how much to scale base bark by for each extrusion
    localScale = 0.7
    
    if (treeHeight == 10):
        localScale = 0.8
        
    if (treeHeight == 5):
        localScale = 0.6
    
    #base bark loop
    for i in range (2, treeHeight):
        rotationVal=cmds.joint('base'+(str(i)), query=True,ax=True, ay=True, az=True)
        
        jointPosWorld = cmds.joint('base'+(str(i)), a=True, query=True, p=True)
        jointPosRelative = cmds.joint('base'+(str(i)), r=True, query=True, p=True)
        
        cmds.move(jointPosWorld[0], jointPosWorld[1], jointPosWorld[2], "bark.scalePivot","bark.rotatePivot", absolute=True)
        cmds.select('bark.f[0]')
        cmds.polyExtrudeFacet(ls = [localScale, localScale, localScale], lrx = rotationVal[0], lry = rotationVal[2], lrz = rotationVal[1], ltx = jointPosRelative[0], lty = -jointPosRelative[2], ltz = jointPosRelative[1])
        if i == treeHeight-1:
            cmds.polySphere(r = localScale/2)
            cmds.move(jointPosWorld[0], jointPosWorld[1], jointPosWorld[2])
    
    
    #branch mesh setup
    
    myBranch = {}
    myBranch[1] = branchCountA
    myBranch[2] = branchCountB
    
    myLetter = {}
    myLetter[1] = 'A'
    myLetter[2] = 'B'
    
    for h in range (1,3):
        maxJnts = 6
        jointNum = 6
        for i in range(1, myBranch[h]):
            maxJnts-=1
            for j in range(1, maxJnts+2):
                branchNode = 'branch'+myLetter[h]+str(i)+'_'+str(j)
                branchParent = cmds.listRelatives(branchNode, p=True)
                
                branchMesh('branch'+myLetter[h]+str(i)+'_'+str(j), 'branchBark'+myLetter[h]+ str(i)+'_'+str(j), branchNode, branchParent)
                
                
    applyShaders(treeHeight, planeCnt, myBranch, myLetter, season)

def branchMesh(branchName, branchBark, branchNode, branchParent):
    
    #setup new cylinder for each branch
    jointPosWorld = cmds.joint(branchParent, a=True, query=True, p=True)
    cmds.polySphere(r=0.5)
    cmds.move(jointPosWorld[0],jointPosWorld[1], jointPosWorld[2])
    
    cmds.polyCylinder(n=branchBark, sx=20, sy=0, sz=0, h=8, r = 2)
    cmds.move(8/2, y=True)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.select( d=True )
    for k in range(20): 
        cmds.select(branchBark+'.f[' + (str(k)) + ']', add=True)
    cmds.select(branchBark+'.f[21]', add=True)
    cmds.delete(s=True)
    
    cmds.move(0,0,0, branchBark+".scalePivot",branchBark+".rotatePivot", absolute=True)
    
    cmds.select(d=True)
    cmds.select(branchBark)
    cmds.move(jointPosWorld[0],jointPosWorld[1], jointPosWorld[2])    
    
    #aims cylinder face at next node position, then rotates so extrusion with ltz can be performed
    cmds.aimConstraint( branchNode, branchBark )
    cmds.aimConstraint( branchNode, branchBark, rm=True)
    cmds.select(branchBark)
    cmds.rotate('90deg', rotateZ=True, os=True, r=True)
    cmds.scale(0.25,0.25,0.25)
    
    rotationVal=cmds.joint(branchName, query=True,ax=True, ay=True, az=True)
    
    jointPosWorld = cmds.joint(branchName, a=True, query=True, p=True)
    jointPosRelative = cmds.joint(branchName, r=True, query=True, p=True)
    
    cmds.move(jointPosWorld[0], jointPosWorld[1], jointPosWorld[2], branchBark+'.scalePivot',branchBark+'.rotatePivot', absolute=True)
    cmds.select(branchBark+'.f[0]')
    
    localZ = math.sqrt((math.pow(jointPosRelative[0], 2)) + (math.pow(jointPosRelative[1], 2)) + (math.pow(jointPosRelative[2], 2)))
    
    cmds.polyExtrudeFacet(lrx = rotationVal[0], ltx = 0, lty = 0, ltz = localZ)
   
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.select(branchBark+'.f[0]', d=True)
    
    
def applyShaders(treeHeight, planeCnt, myBranch, myLetter, season):
    
    barkMat = cmds.shadingNode('lambert', asShader=True, n='barkMat')
    cmds.setAttr('barkMat'+'.color', 0.45, 0.30, 0.2)
    
    #green - spring
    leafMat1 = cmds.shadingNode('lambert', asShader=True, n='leafMat1')
    cmds.setAttr('leafMat1'+'.color', 0.0, 0.90, 0.2)
    
    #green - summer
    leafMat2 = cmds.shadingNode('lambert', asShader=True, n='leafMat2')
    cmds.setAttr('leafMat2'+'.color', 0.2, 1.5, 0.0)
    
    #orange/red - fall
    leafMat2 = cmds.shadingNode('lambert', asShader=True, n='leafMat3')
    cmds.setAttr('leafMat3'+'.color', 1.5, 0.30, 0.05)
    
    #apply bark
    cmds.select(all=True)
    for i in range (1, treeHeight):
        cmds.select('base'+str(i), d=True)
    for i in range (1, planeCnt):
        cmds.select('leaf'+str(i), d=True)
    cmds.polyUnite(o=True, n='barkUnite')
    cmds.hyperShade(assign=barkMat)
    cmds.delete(ch=True)
    cmds.select(d = True)
    
    #apply leaf if not winter
    if season != 4:
        for i in range (1, planeCnt):
            cmds.select('leaf'+str(i), add=True)
        cmds.hyperShade(assign='leafMat'+str(season))
        cmds.select('barkUnite', add=True)
        cmds.polyUnite(o=True, n='treeMesh')
        cmds.select(d=True)
        cmds.select('treeMesh')
        cmds.delete(ch=True)
    
    for i in range (1, treeHeight):
        cmds.select('base'+str(i), add=True)
    
    if season == 4:
        cmds.select('barkUnite', add=True)
    
    #select joints one by one (select all doesn't work)
    for h in range (1,3):
        maxJnts = 6
        jointNum = 6
        for i in range(1, myBranch[h]):
            maxJnts-=1
            for j in range(1, maxJnts+2):
                cmds.select('branch'+myLetter[h]+str(i)+'_'+str(j), add=True)
                          
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.bindSkin(tsb=True)
    cmds.delete(ch=True)
    
    
#this function generates an individual leaf using the respective joint position in world space
def generateLeaf(jointPosWorld, planeCnt, jntName):
    cmds.polySphere(r=0.475)
    cmds.move(jointPosWorld[0], jointPosWorld[1], jointPosWorld[2]) #xyz values of joint stored in an array
    cmds.polyPlane(n='leaf'+str(planeCnt), sx=1, sy=3, w=2, h=3)
    shape = 'leaf' + str(planeCnt)
    
    cmds.select(shape + '.e[0]') #selecting the edges and scaling them down to get leaf shape
    cmds.scale( 0.1, 1, 1 )

    cmds.select(shape + '.e[9]')
    cmds.scale( 0, 1, 1 )
    
    cmds.select(shape)
    cmds.polySmooth( shape, dv=2, sdt=1) #smooth it out to round out edges
    cmds.move(0, 0, 1.46, shape + ".scalePivot", shape + ".rotatePivot", absolute=True)
    
    cmds.move(jointPosWorld[0], jointPosWorld[1], (jointPosWorld[2] - 1.31))
    cmds.aimConstraint( jntName, shape )
    cmds.aimConstraint( jntName, shape, rm=True )
    cmds.rotate((str((randint(0,180)))) + 'deg', (str((randint(0,180)))) + 'deg', (str((randint(0,180)))) + 'deg', r=True )
    cmds.polyExtrudeFacet(ltz=0.1) #extrude the leaf to get rid of null sides
    
    #each leaf has a unique size chosen by a random scale value
    scaleVal = random.uniform(0.8,1.2)
    cmds.scale( scaleVal, scaleVal, scaleVal )
