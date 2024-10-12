sl = cmds.ls(sl=1)
dpc = cmds.duplicate(sl[0])[0]
s0 = cmds.listRelatives(dpc,shapes=1)[0]
s1 = cmds.listRelatives(sl[1],shapes=1)[0]
cmds.parent(s0,sl[1],r=1,s=1)
if cmds.objExists('AllSet') :
    cmds.sets(s0,e=1,addElement='AllSet')
cmds.delete(s1,dpc)
cmds.rename(s0,s1)