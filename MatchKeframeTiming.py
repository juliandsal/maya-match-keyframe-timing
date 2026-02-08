import maya.cmds as cmds

reference_control = None
target_controls = []

def select_reference():
    global reference_control
    sel = cmds.ls(selection=True)
    if sel:
        reference_control = sel[0]
        cmds.textField("refField", edit=True, text=reference_control)
    else:
        cmds.warning("Please select a reference control.")

def select_targets():
    global target_controls
    sel = cmds.ls(selection=True)
    if sel:
        target_controls = sel
        cmds.textField("targetField", edit=True, text=", ".join(target_controls))
    else:
        cmds.warning("Please select one or more target controls.")

def bake_controls():
    global reference_control, target_controls

    if not reference_control or not target_controls:
        cmds.warning("You must select both a reference control and at least one target control.")
        return

    key_times = cmds.keyframe(reference_control, query=True, timeChange=True)
    if not key_times:
        cmds.warning("Reference control has no keyframes.")
        return

    key_times = sorted(set(round(t, 3) for t in key_times))  # round to avoid float precision bugs

    for target in target_controls:
        # Get all existing keys on the target
        existing_keys = cmds.keyframe(target, query=True, timeChange=True) or []
        existing_keys = set(round(k, 3) for k in existing_keys)

        # Delete keys NOT in reference keyframes
        keys_to_delete = [k for k in existing_keys if k not in key_times]
        for time in keys_to_delete:
            cmds.cutKey(target, time=(time, time), option="keys")

    for time in key_times:
        cmds.currentTime(time, edit=True)
        for target in target_controls:
            cmds.setKeyframe(target, attribute='translate')
            cmds.setKeyframe(target, attribute='rotate')

    cmds.inViewMessage(amg="✅Keys baked at reference keyframes only. Animation preserved.", pos='midCenter', fade=True)

def create_bake_ui():
    if cmds.window("bakeKeysUI", exists=True):
        cmds.deleteUI("bakeKeysUI")

    window = cmds.window("bakeKeysUI", title="Bake Keys to Reference", widthHeight=(400, 220), sizeable=True)
    form = cmds.formLayout()

    col = cmds.columnLayout(adjustableColumn=True, rowSpacing=10)
    cmds.text(label="Step 1: Select Reference Control")
    cmds.button(label="Set Reference Control", command=lambda *_: select_reference(), height=30)
    cmds.textField("refField", editable=False)

    cmds.text(label="Step 2: Select Target Controls")
    cmds.button(label="Set Target Controls", command=lambda *_: select_targets(), height=30)
    cmds.textField("targetField", editable=False)

    cmds.separator(height=10, style='in')

    cmds.setParent(form)
    bake_btn = cmds.button(label="Bake Keys", command=lambda *_: bake_controls(),
                           backgroundColor=(0.5, 1, 0.5), height=40)

    cmds.formLayout(form, edit=True,
        attachForm=[
            (col, 'top', 10),
            (col, 'left', 10),
            (col, 'right', 10),
            (bake_btn, 'left', 10),
            (bake_btn, 'right', 10),
            (bake_btn, 'bottom', 10)
        ],
        attachControl=[
            (bake_btn, 'top', 10, col)
        ]
    )

    cmds.showWindow(window)

# Run this
create_bake_ui()

