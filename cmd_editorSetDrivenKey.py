import maya.cmds as cmds
import maya.mel as mm
import re as re

ses = mm.eval('getShapeEditorTreeviewSelection(24)')
bs = ses[0].split('.')[0]
id = int(ses[0].split('.')[1]) ; idS = 'weight['+str(id)+']'
aList = cmds.aliasAttr(bs,query=1) ; ses = ''
for i in range(0,len(aList),2) :
 if aList[i+1]==idS : ses = aList[i]

rule = 'j[clr][A-Z]\d+_[a-zA-Z0-9]+' ; djo = '' # drive joint
for x in cmds.ls(type='joint'):
 xp = x.split('_')
 if len(xp)>1:
  if xp[1] == ses.split('_')[0]:
   if len(re.findall(rule,x))>0 : djo = x

ax = ses.split('_')[1][0]

da = '' # drive attribute
if ax in ['X','x'] : da = 'quatX'
if ax in ['Y','y'] : da = 'quatY'
if ax in ['Z','z'] : da = 'quatZ'
pm = 1 # plus or minus
if ax in ['x','y','z'] : pm = -1
ag = float(ses.split('_')[1][1:])
ga = cmds.getAttr(djo+'.'+da)
print djo

cmds.setDrivenKeyframe(bs+'.'+ses,currentDriver=djo+'.'+da,inTangentType='flat',value=0,outTangentType='flat')
cmds.setDrivenKeyframe(bs+'.'+ses,currentDriver=djo+'.'+da,driverValue=ag*pm,value=1,inTangentType='spline',outTangentType='spline')
cmds.setDrivenKeyframe(bs+'.'+ses,currentDriver=djo+'.'+da,driverValue=(((ag*pm)-ga)*1.15)+ga,value=1.1,inTangentType='flat',outTangentType='flat')
cmds.setDrivenKeyframe(bs+'.'+ses,currentDriver=djo+'.'+da,driverValue=(((ag*pm)-ga)*0.5)+ga,value=0.3,inTangentType='spline',outTangentType='spline')