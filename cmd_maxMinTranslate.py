sl = cmds.ls(selection=1)
sL = cmds.ls(selection=1,long=1)
n = sl[2].replace(sl[2].split('_')[0]+'_','')
plus = cmds.createNode('plusMinusAverage',name='plus_'+n,skipSelect=1)
cmds.connectAttr(sL[0]+'.translate',plus+'.input3D[0]')
cmds.connectAttr(sL[1]+'.translate',plus+'.input3D[1]')
clamp = cmds.createNode('clamp',name='clp_'+n,skipSelect=1)
cmds.connectAttr(plus+'.output3D',clamp+'.input')

listA = ['X','Y','Z'] ; listB = ['R','G','B']
for a,b in zip(listA,listB):
 cds = cmds.createNode('condition',name='cds_'+n+a,skipSelect=1)
 cmds.setAttr(cds+'.operation',2)
 cmds.connectAttr(sL[0]+'.translate'+a,cds+'.firstTerm')
 cmds.connectAttr(sL[0]+'.translate'+a,cds+'.colorIfTrue.colorIfTrueR')
 cmds.connectAttr(sL[0]+'.translate'+a,cds+'.colorIfFalse.colorIfFalseG')
 cmds.connectAttr(sL[1]+'.translate'+a,cds+'.secondTerm')
 cmds.connectAttr(sL[1]+'.translate'+a,cds+'.colorIfFalse.colorIfFalseR')
 cmds.connectAttr(sL[1]+'.translate'+a,cds+'.colorIfTrue.colorIfTrueG')
 cmds.connectAttr(cds+'.outColor.outColorR',clamp+'.max.max'+b)
 cmds.connectAttr(cds+'.outColor.outColorG',clamp+'.min.min'+b)
 
cmds.connectAttr(clamp+'.output',sL[2]+'.translate')