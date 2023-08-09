
import maya.cmds as cmds
import maya.mel as mel
from itertools import izip
import maya.OpenMaya as om

#=======================================================#
#   Prune vertex influenced with more than 4 joints
#=======================================================#
maxInf = 4
# define the max influences
def prune_vertex(item):
    print item
    sk = mel.eval('findRelatedSkinCluster '+item)
    pe = cmds.polyEvaluate(v=1)
    vs = []
    i=0
    inf = cmds.skinCluster(sk,query=True,inf=True)
    for jo in inf:
        cmds.setAttr(jo+'.liw',0)  
    while i < pe :
        sp = cmds.skinPercent(sk,item+'.vtx['+str(i)+']',q=1,v=1)
        n=0
        for j in sp:         
            if j > 0:
                n+=1            
                if n > maxInf: 
                    vtx2 = item+'.vtx['+str(i)+']'
                    if vtx2 not in vs:
                        vs.append(item+'.vtx['+str(i)+']')             
        i+=1
    for k in vs:
        sp2 = cmds.skinPercent(sk,k,q=1,v=1)
        d = dict(izip(sp2,inf))            
        while sp2.count(0)>0:
            sp2.remove(0)
        sp2.sort()
        sp2.reverse()        
        sp3 = sp2[maxInf:]
        for n in sp3:
            cmds.skinPercent(sk,k,transformValue=(d[n],0))
    return vs
      
sel = cmds.ls(sl=1)
for obj in sel:
    while len(sel)<1:
        om.MGlobal.displayError('no object is selected')
        break
    else:
        hehe=prune_vertex(obj)         
    cmds.select(hehe,add=1)
    cmds.select(obj,d=1)
    
om.MGlobal.displayInfo('Done')