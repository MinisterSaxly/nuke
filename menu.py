# --------------------------------------------------------------
# Last Updated: sometime 2023
# --------------------------------------------------------------
import nuke
import nukescripts
import os
import colorsys, operator, sys
from pathlib import Path
import readFromWrite
import KnobScripter


nuke.menu('Nuke').addCommand('My file menu/Read from Write', 'readFromWrite.ReadFromWrite()', 'shift+r')
nuke.menu('Nuke').addCommand('My file menu/Remove nr in dot name', 'from removeNrFromDotName import removeNrFromDotName;removeNrFromDotName.main()')



#nuke.menu('Nuke').addCommand('Mercedes Tools/Auto Root Range', 'import autoRootRange;autoRootRange.main()')

# --------------------------------------------------------------
# LAYOUT
# --------------------------------------------------------------
maxPanels = nuke.toNode('preferences')['maxPanels']
maxPanels.setValue(2)

# --------------------------------------------------------------
# HOTKEYS
# --------------------------------------------------------------
nuke.menu('Nodes').addCommand("Transform/Tracker", "nuke.createNode('Tracker4')", "ctrl+alt+t", shortcutContext=2)
nuke.menu('Nodes').addCommand("Channel/Shuffle", "nuke.createNode('Shuffle')", "ctrl+alt+s", shortcutContext=2)

# --------------------------------------------------------------
# DEFAULTS
# --------------------------------------------------------------
nuke.knobDefault('Tracker4.shutteroffset', "centered")
nuke.knobDefault('TimeBlur.shutteroffset', "centered")
nuke.knobDefault('Transform.shutteroffset', "centered")
nuke.knobDefault('CornerPin2D.shutteroffset', "centered")
nuke.knobDefault('MotionBlur2D.shutteroffset', "centered")
nuke.knobDefault('MotionBlur3D.shutteroffset', "centered")
nuke.knobDefault('ScanlineRender.shutteroffset', "centered")
nuke.knobDefault('Remove.operation', 'keep')
nuke.knobDefault('Remove.channels', 'rgba')
nuke.knobDefault('Merge2.bbox', 'union')
nuke.knobDefault('Project3D2.crop', "false")
nuke.knobDefault('Tracker4.label', "Motion: [value transform]\nRef Frame: [value reference_frame]")
nuke.knobDefault('Shuffle.label', "[value in]")
nuke.knobDefault('Camera2.frame_rate', '25')
nuke.knobDefault('ReadGeo2.frame_rate', '25')
nuke.knobDefault('Roto.cliptype', 'no clip')
nuke.knobDefault('Read.on_error', 'nearest frame')
nuke.knobDefault('Reformat.pbb', 'true')
nuke.knobDefault('LayerContactSheet.showLayerNames', 'true')
nuke.knobDefault('P_Matte.in', 'P')





# --------------------------------------------------------------
# TOOLBARS
# --------------------------------------------------------------

# menubar=nuke.menu("MenuType")
# m=menubar.addMenu("&NewMenu")
# m.addCommand("&NewItem", "PythonCode", "templates/CG_tree_v001.nk", icon="IconName", index=#)