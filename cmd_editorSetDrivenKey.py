import sys
import maya.cmds as cmds
import maya.mel as mm
import re as re

def cmd_editorSetDrivenKey():
 ses = mm.eval('getShapeEditorTreeviewSelection(24)')
 bs = ses[0].split('.')[0]
 id = int(ses[0].split('.')[1])
 idS = 'weight['+str(id)+']'
 aList = cmds.aliasAttr(bs,query=1)
 ses = ''
 for i in range(0,len(aList),2) :
  if aList[i+1]==idS : ses = aList[i]
 
 attrRule = '.+_[x|X|y|Y|z|Z][0-9]+'
 if(len(re.findall(attrRule,ses))==0):
     cmds.warning('Attribute name incorrect.')
     return 0

 rule = 'j[clr][A-Z]\d+_[a-zA-Z0-9]+' ; djo = '' # drive joint
 for x in cmds.ls(type='joint'):
  xp = x.split('_')
  if len(xp)>1:
   if xp[1] == ses.split('_')[0]:
    if len(re.findall(rule,x))>0 : djo = x

 if djo == '' :
  sl = cmds.ls(selection=1)
  if len(sl) > 0 :
   djo = sl[-1]

 ax = ses.split('_')[1][0]

 da = '' # drive attribute
 if ax in ['X','x'] : da = 'quatX'
 if ax in ['Y','y'] : da = 'quatY'
 if ax in ['Z','z'] : da = 'quatZ'
 if(cmds.objExists(djo+'.'+da)==0):
  cmd_editorSetDrivenKey_quatAttr(djo,ax)
 pm = 1 # plus or minus
 if ax in ['x','y','z'] : pm = -1
 ag = float(ses.split('_')[1][1:])
 ga = cmds.getAttr(djo+'.'+da)
 print djo+'.'+ax

 cmds.setDrivenKeyframe(bs+'.'+ses,currentDriver=djo+'.'+da,inTangentType='flat',value=0,outTangentType='flat')
 cmds.setDrivenKeyframe(bs+'.'+ses,currentDriver=djo+'.'+da,driverValue=ag*pm,value=1,inTangentType='spline',outTangentType='spline')
 cmds.setDrivenKeyframe(bs+'.'+ses,currentDriver=djo+'.'+da,driverValue=(((ag*pm)-ga)*1.15)+ga,value=1.1,inTangentType='flat',outTangentType='flat')
 cmds.setDrivenKeyframe(bs+'.'+ses,currentDriver=djo+'.'+da,driverValue=(((ag*pm)-ga)*0.5)+ga,value=0.3,inTangentType='spline',outTangentType='spline')
    
def cmd_editorSetDrivenKey_quatAttr(djo,ax):
 ro = 1 # rotate order
 if ax=='x' : ax = 'X' ; ro = 1
 if ax=='y' : ax = 'Y' ; ro = 2
 if ax=='z' : ax = 'Z' ; ro = 0
 cmds.addAttr(djo,longName='quat'+ax,attributeType='long',keyable=1)
 la = cmds.listConnections(djo+'.rotate',type='eulerToQuat')
 if la : e2q = la[0]
 else :
  e2q = cmds.createNode('eulerToQuat',name=('e2q_'+djo+ax),skipSelect=1)
  cmds.connectAttr(djo+'.rotate',e2q+'.inputRotate')
  cmds.connectAttr(djo+'.rotateOrder',e2q+'.inputRotateOrder')
 q2e = cmds.createNode('quatToEuler',name=('q2e_'+djo+ax),skipSelect=1)
 cmds.connectAttr(e2q+'.outputQuat'+ax,q2e+'.inputQuat'+ax)
 cmds.connectAttr(e2q+'.outputQuatW',q2e+'.inputQuatW')
 cmds.connectAttr(q2e+'.outputRotate.outputRotate'+ax,djo+'.quat'+ax)
 cmds.setAttr(q2e+'.inputRotateOrder',ro)

cmd_editorSetDrivenKey()
