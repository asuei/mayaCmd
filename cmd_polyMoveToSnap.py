import maya.cmds as cmds
sl = cmds.ls(selection=1)
for i in range(cmds.polyEvaluate(sl[0],vertex=True )):
    t =  cmds.xform(sl[0]+'.vtx['+str(i)+']',q=1,ws=1,t=1)
    cmds.move(t[0],t[1],t[2],sl[1]+'.vtx['+str(i)+']', absolute=True)