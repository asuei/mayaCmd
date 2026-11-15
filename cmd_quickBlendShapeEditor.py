import maya.cmds as cmds

WINDOW = "QuickBlendShapeEditor"

EDIT_STATE = {
    "node": None,
    "index": None
}

NORMAL_COLOR = (0.36, 0.36, 0.36)
EDIT_COLOR = (0.65, 0.12, 0.12)

# Create BlendShape
def create_quick_blendshape():

    selection = cmds.ls(sl=True, long=True, type="transform")

    if len(selection) != 2:
        cmds.warning("Please select exactly TWO polygon objects.")
        return

    source = selection[0]
    target = selection[1]

    # Validate polygon meshes
    for obj in selection:
        shapes = cmds.listRelatives(obj,shapes=True,noIntermediate=True,type="mesh")
        if not shapes:
            cmds.warning("{} is not a polygon mesh.".format(obj))
            return
    duplicate = cmds.duplicate(source,name="temp_blendShape")[0] # Duplicate source

    try:
        bs = cmds.blendShape(duplicate,target,name=target.split("|")[-1] + "_BS",origin="local")[0]
    finally:
        if cmds.objExists(duplicate):
            cmds.delete(duplicate)

    # Get target index
    indices = cmds.getAttr(bs + ".weight",multiIndices=True) or []
    if not indices:
        cmds.warning("No blendShape target found.")
        return
    index = indices[0]

    # Set initial weight to 1
    cmds.setAttr("{}.weight[{}]".format(bs, index),1.0)

    show_quick_editor(bs, index)


# End Target Editing
def end_edit():

    node = EDIT_STATE["node"]

    if node and cmds.objExists(node):

        try:
            cmds.sculptTarget(node,edit=True,target=-1)

        except Exception as e:
            cmds.warning(str(e))

    EDIT_STATE["node"] = None
    EDIT_STATE["index"] = None


# Toggle Edit Mode
def toggle_edit(node, index, button):

    # Finish editing
    if EDIT_STATE["node"] == node:
        end_edit()
        cmds.button(button,edit=True,label="Edit",backgroundColor=NORMAL_COLOR)
        return

    # Finish previous editing session
    end_edit()

    try:

        # Enter Maya native Target Editing Mode
        cmds.sculptTarget(node,edit=True,target=index)

        EDIT_STATE["node"] = node
        EDIT_STATE["index"] = index

        cmds.button(button,edit=True,label="Finish Editing",backgroundColor=EDIT_COLOR)

        cmds.select(clear=True)

    except Exception as e:

        cmds.warning("Cannot enter Target Editing Mode: {}".format(e))


# Create Final Shape
def create_final_shape(node, index, target):

    if not cmds.objExists(node):
        cmds.warning("BlendShape node no longer exists.")
        return

    if not cmds.objExists(target):
        cmds.warning("Target object no longer exists.")
        return

    try:
        # End Target Editing if active
        end_edit()

        cmds.setAttr("{}.weight[{}]".format(node, index),1.0)
        new_mesh = cmds.duplicate(target,returnRootsOnly=True,name=target.split("|")[-1] + "_FinalShape")[0]
        cmds.delete(new_mesh,constructionHistory=True)

        current_x = cmds.getAttr(new_mesh + ".translateX")
        cmds.setAttr(new_mesh + ".translateX",current_x + 3.0)
        cmds.delete(node)

        if cmds.window(WINDOW, exists=True):
            cmds.deleteUI(WINDOW)

        cmds.select(new_mesh, replace=True)

    except Exception as e:
        cmds.warning("Create Final Shape failed: {}".format(e))


# Quick BlendShape Editor UI
def show_quick_editor(node, index):

    if cmds.window(WINDOW, exists=True):
        cmds.deleteUI(WINDOW)

    end_edit()

    # Get target name
    aliases = cmds.aliasAttr(node, query=True) or []

    target_name = "Target_{}".format(index)

    for i in range(0, len(aliases), 2):

        if aliases[i + 1] == "weight[{}]".format(index):
            target_name = aliases[i]
            break

    attr = "{}.weight[{}]".format(node, index)

    # Get target mesh
    target = cmds.listConnections(node + ".outputGeometry",source=False,destination=True,type="mesh")

    # Use the blendShape destination geometry's parent
    geometries = cmds.blendShape(node,query=True,geometry=True)

    if not geometries:
        cmds.warning("Cannot find blendShape target geometry.")
        return

    target = geometries[0]

    # Create window
    cmds.window(WINDOW,title="Quick BlendShape Editor",widthHeight=(380, 180),sizeable=True)
    cmds.columnLayout(adjustableColumn=True,rowSpacing=10,columnOffset=("both", 12))

    cmds.separator(height=5)
    cmds.text(label="Target: {}".format(target_name),align="left")
    
    cmds.attrFieldSliderGrp(label="Weight",attribute=attr,minValue=0.0,maxValue=1.0,step=0.01)
    
    edit_button = cmds.button(label="Edit",height=32,backgroundColor=NORMAL_COLOR)

    cmds.button(edit_button,edit=True,command=lambda *_:toggle_edit(node, index, edit_button))
    cmds.button(label="Finish",command=lambda *_:create_final_shape(node, index, target))
    cmds.showWindow(WINDOW)
    cmds.separator(height=5)

create_quick_blendshape()
