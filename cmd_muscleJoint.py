import maya.cmds as cmds
a = 'y'
av = [0,1,0]
dir = 1.0

sl = cmds.ls(selection=1)
p = cmds.listRelatives(sl[0],parent=1)[0]
n = sl[0].split('_')[1]

crv = cmds.curve(p=[(0,0,0),(0,0,0),(0,0,0)],degree=2,name='crv_'+n)
crvS = cmds.listRelatives(crv,shapes=1)[0]
cmds.parent(crv,p,relative=1)
crvL = cmds.curve(p=[(0,0,0),(0,0,0)],degree=1,name=crv+'Linear')
crvLS = cmds.listRelatives(crvL,shapes=1)[0]
cmds.parent(crvL,p,relative=1)
for i in range(3) : cmds.connectAttr(sl[i]+'.translate',crvS+'.controlPoints['+str(i)+']')
cmds.connectAttr(sl[0]+'.translate',crvLS+'.controlPoints[0]')
cmds.connectAttr(sl[2]+'.translate',crvLS+'.controlPoints[1]')
poci = cmds.createNode('pointOnCurveInfo')
npoc = cmds.createNode('nearestPointOnCurve')
cmds.connectAttr(crvLS+'.local',poci+'.inputCurve')
cmds.setAttr(poci+'.parameter',0.5)
cmds.connectAttr(poci+'.result.position',npoc+'.inPosition')
cmds.connectAttr(crvS+'.local',npoc+'.inputCurve')
cons = [] ; len = [] ; jo =[]
for i in range(2) :
 cons.append(cmds.createNode('transform',name=sl[i].replace('pos_','cons_'),parent=p))
 len.append(cmds.createNode('transform',name=sl[i].replace('pos_','len_'),parent=cons[i]))
 jo.append(cmds.createNode('joint',name=sl[i].replace('pos_','jo_'),parent=cons[i]))
 jEnd = cmds.createNode('joint',name=jo[i]+'End',parent=jo[i])
 cmds.setAttr(jEnd+'.t'+a,1)
 cmds.setAttr(jEnd+'.v',0)

cmds.connectAttr(sl[0]+'.translate',cons[0]+'.translate')
poci = cmds.createNode('pointOnCurveInfo')
cmds.connectAttr(crvS+'.local',poci+'.inputCurve')
#cmds.setAttr(poci+'.parameter',0.5)
cmds.connectAttr(npoc+'.parameter',poci+'.parameter')
cmds.connectAttr(poci+'.result.position',cons[1]+'.translate')
cmds.aimConstraint(cons[1],cons[0],aimVector=av,upVector=[0,1,0],worldUpType='none')
cmds.aimConstraint(sl[2],cons[1],aimVector=av,upVector=[0,1,0],worldUpType='none')
cmds.pointConstraint(cons[1],len[0])
cmds.pointConstraint(sl[2],len[1])
cmds.connectAttr(len[0]+'.t'+a,jo[0]+'.s'+a)
cmds.connectAttr(len[1]+'.t'+a,jo[1]+'.s'+a)
