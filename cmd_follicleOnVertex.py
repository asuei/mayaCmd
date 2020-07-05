#cmd_follicleOnVertex.py
import maya.cmds as cmds
import re as re


import maya.cmds as cmds
import re as re


for x in cmds.ls(selection=1) :
 gn = x.split('.')[0]
 s = cmds.listRelatives(gn,shapes=1,noIntermediate=1)[0]
 mat = '\[[0-9]+'
 num = re.findall(mat,x)[0]
 num = num.replace('[','')


 fn = cmds.createNode('follicle')
 print fn
 cmds.connectAttr(s+'.outMesh',fn+'.inputMesh')
 cmds.connectAttr(s+'.worldMatrix[0]',fn+'.inputWorldMatrix')
 fp = cmds.listRelatives(fn,parent=1)[0]
 cmds.connectAttr(fn+'.outTranslate',fp+'.translate')
 cmds.connectAttr(fn+'.outRotate',fp+'.rotate')


 uvList = cmds.polyListComponentConversion(x,fromVertex=1,toUV=1)
 cmds.polyEditUV(uvList[0],q=1)
 cmds.setAttr(fn+'.parameterU',cmds.polyEditUV(uvList[0],q=1)[0])
 cmds.setAttr(fn+'.parameterV',cmds.polyEditUV(uvList[0],q=1)[1])


#
'''
for x in cmds.ls(selection=1) :
 gn = x.split('.')[0]
 gns = gn.split('_')[1]
 s = cmds.listRelatives(gn,shapes=1,noIntermediate=1)[0]
 mat = '\[[0-9]+'
 num = re.findall(mat,x)[0]
 num = num.replace('[','')
 fn = 'flc_'+gns+num


 cmds.createNode('follicle',name=fn)
 cmds.connectAttr(s+'.outMesh',fn+'.inputMesh')
 cmds.connectAttr(s+'.worldMatrix[0]',fn+'.inputWorldMatrix')
 fp = cmds.listRelatives(fn,parent=1)[0]
 fp = cmds.rename(fp,'flcTrans_'+gns+num)
 cmds.connectAttr(fn+'.outTranslate',fp+'.translate')
 cmds.connectAttr(fn+'.outRotate',fp+'.rotate')


 uvList = cmds.polyListComponentConversion(x,fromVertex=1,toUV=1)
 cmds.polyEditUV(uvList[0],q=1)
 cmds.setAttr(fn+'.parameterU',cmds.polyEditUV(uvList[0],q=1)[0])
 cmds.setAttr(fn+'.parameterV',cmds.polyEditUV(uvList[0],q=1)[1])
 
 cs = 0.5
 cmds.curve(d=1,p=[(-cs,0,cs),(0,cs,0),(cs,0,cs),(0,-cs,0),(cs,0,-cs),(0,cs,0),(-cs,0,-cs),(0,-cs,0),(-cs,0,cs),(cs,0,cs),(cs,0,-cs),(-cs,0,-cs),(-cs,0,cs)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12],name='ctrl_'+gns+num)
 cmds.parent('ctrl_'+gns+num,'flcTrans_'+gns+num,relative=1)
 tx = x.replace('Poly','Adj')
 cmds.createNode('transform',name='flcTrans_'+gns+num+'_pCons')
 cmds.createNode('transform',name='v_'+gns+num,parent='flcTrans_'+gns+num+'_pCons')
 cmds.pointConstraint('flcTrans_'+gns+num,'flcTrans_'+gns+num+'_pCons')
 cmds.pointConstraint('ctrl_'+gns+num,'v_'+gns+num)
 cc = cmds.cluster(tx)
 cmds.connectAttr('v_'+gns+num+'.t',cc[1]+'.t')
'''