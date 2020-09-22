# encoding: utf-8
import maya.cmds as cmds

def muscleJoint():
 axis = 'x'
 axisVector = [1,0,0]

 sl = cmds.ls(selection=1)
 if len(sl) < 3 : cmds.warning('Most select 3 transforms.') ; return 0
 p = cmds.listRelatives(sl[0],parent=1)
 if p is None : cmds.warning('on the root.') ; return 0
 else : p = p[0]
 
 x0 = cmds.xform(sl[0],q=1,translation=1,objectSpace=1)
 x2 = cmds.xform(sl[2],q=1,translation=1,objectSpace=1)
 xd = x2[0] - x0[0]
 yd = x2[1] - x0[1]
 zd = x2[2] - x0[2]
 if max(abs(xd),abs(yd),abs(zd)) == abs(xd) and xd > 0 : axis = 'x' ; axisVector = [1,0,0]
 if max(abs(xd),abs(yd),abs(zd)) == abs(xd) and xd < 0 : axis = 'x' ; axisVector = [-1,0,0]
 if max(abs(xd),abs(yd),abs(zd)) == abs(yd) and yd > 0 : axis = 'y' ; axisVector = [0,1,0]
 if max(abs(xd),abs(yd),abs(zd)) == abs(yd) and yd < 0 : axis = 'y' ; axisVector = [0,-1,0]
 if max(abs(xd),abs(yd),abs(zd)) == abs(zd) and zd > 0 : axis = 'z' ; axisVector = [0,0,1]
 if max(abs(xd),abs(yd),abs(zd)) == abs(zd) and zd < 0 : axis = 'z' ; axisVector = [0,0,-1]
 
 nList = [sl[0],sl[1],sl[2]]
 for i in range(len(nList)) :
  if nList[i][0:4] == 'pos_' : nList[i] = nList[i][4:]
  else :
   sl_ = nList[i].split('_')
   if len(sl_) >= 2 :
    nList[i] = max(sl_,key=len)
    
 crv = cmds.curve(p=[(0,0,0),(0,0,0),(0,0,0)],degree=2,name='crv_'+nList[0])
 crvS = cmds.listRelatives(crv,shapes=1)[0]
 cmds.parent(crv,p,relative=1)
 crvL = cmds.curve(p=[(0,0,0),(0,0,0)],degree=1,name='wireCrv_'+nList[0])
 crvLS = cmds.listRelatives(crvL,shapes=1)[0]
 cmds.parent(crvL,p,relative=1)
 cmds.setAttr(crvL+'.v',0)
 
 for i in range(3) : cmds.connectAttr(sl[i]+'.translate',crvS+'.controlPoints['+str(i)+']')
 cmds.connectAttr(sl[0]+'.translate',crvLS+'.controlPoints[0]')
 cmds.connectAttr(sl[2]+'.translate',crvLS+'.controlPoints[1]')
 crvB = cmds.duplicate(crvL,name='wireBase_'+nList[0],renameChildren=1)
 crvBS = cmds.listRelatives(crvB[0],shapes=1)[0]
 w = cmds.wire(crvS+'.controlPoints[1]',envelope=0.5,dropoffDistance=[0,100])
 cmds.connectAttr(crvLS+'.worldSpace[0]',w[0]+'.deformedWire[0]')
 cmds.connectAttr(crvBS+'.worldSpace[0]',w[0]+'.baseWire[0]')
 cmds.rebuildCurve(crv,spans=20,degree=3,keepRange=0,constructionHistory=1,replaceOriginal=1)

 poci = cmds.createNode('pointOnCurveInfo')
 cmds.connectAttr(crvLS+'.local',poci+'.inputCurve')
 cmds.setAttr(poci+'.parameter',0.5)
 cons = [] ; lenList = [] ; jo =[]
 for i in range(2) :
  cons.append(cmds.createNode('transform',name='cons_'+nList[i],parent=p))
  lenList.append(cmds.createNode('transform',name='len_'+nList[i],parent=cons[i]))
  jo.append(cmds.createNode('joint',name='jo_'+nList[i],parent=cons[i]))
  jEnd = cmds.createNode('joint',name=jo[i]+'End',parent=jo[i])
  cmds.setAttr(jEnd+'.t'+axis,1)
  cmds.setAttr(jEnd+'.v',0)

 cmds.connectAttr(sl[0]+'.translate',cons[0]+'.translate')
 poci = cmds.createNode('pointOnCurveInfo')
 cmds.connectAttr(crvS+'.local',poci+'.inputCurve')
 cmds.setAttr(poci+'.parameter',0.5)
 cmds.connectAttr(poci+'.result.position',cons[1]+'.translate')
 cmds.aimConstraint(cons[1],cons[0],aimVector=axisVector,upVector=[0,1,0],worldUpType='none')
 cmds.aimConstraint(sl[2],cons[1],aimVector=axisVector,upVector=[0,1,0],worldUpType='none')
 cmds.pointConstraint(cons[1],lenList[0])
 cmds.pointConstraint(sl[2],lenList[1])
 cmds.connectAttr(lenList[0]+'.t'+axis,jo[0]+'.s'+axis)
 cmds.connectAttr(lenList[1]+'.t'+axis,jo[1]+'.s'+axis)
 pin3 = cmds.createNode('transform',name='pin_'+nList[2],parent=p)
 cmds.matchTransform(pin3,sl[2])
 cmds.pointConstraint(pin3,sl[2])

muscleJoint()
