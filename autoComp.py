import nuke
import nukescripts
import glob
import re
from pathlib import Path
import os
#from . import helpers

COMP_DIR ="_NukeX"
CG_DIR = "_INPUT\\3D\\"

PATH_TO_GLB_GRAY = "X:/Projects/_Resources/PSL_anim/2D_library/Compositing/Templates/ANTA23_MERCEDES_PRINT/print_gray_mercedes_tree_ext_v08.nk"
PATH_TO_GLB_RED = "X:/Projects/_Resources/PSL_anim/2D_library/Compositing/Templates/ANTA23_MERCEDES_PRINT/print_red_mercedes_tree_ext_v06.nk"
PATH_TO_GLB_INT = "X:/Projects/_Resources/PSL_anim/2D_library/Compositing/Templates/ANTA23_MERCEDES_PRINT/print_int_mercedes_tree_ext_v05.nk"
PATH_TO_GLS_GRAY = "X:/Projects/_Resources/PSL_anim/2D_library/Compositing/Templates/ANTA23_MERCEDES_PRINT/print_gray_GLS_mercedes_tree_ext_v03.nk"
PATH_TO_GLS_GREEN = "X:/Projects/_Resources/PSL_anim/2D_library/Compositing/Templates/ANTA23_MERCEDES_PRINT/print_gray_GLS_mercedes_tree_ext_v01.nk"
PATH_TO_GLS_GRAY_INT = "X:/Projects/_Resources/PSL_anim/2D_library/Compositing/Templates/ANTA23_MERCEDES_PRINT/print_gray_GLS_mercedes_tree_int_v01.nk"
PATH_TO_GLS_GREEN_INT = "X:/Projects/_Resources/PSL_anim/2D_library/Compositing/Templates/ANTA23_MERCEDES_PRINT/print_green_GLS_mercedes_tree_int_v01.nk"
#PATH_TO_SCRIPT = "X:/Projects/_Resources/PSL_anim/2D_library/Compositing/Templates/ANTA23_MERCEDES/mercedes_tree_ext_v07.nk"

#PATH_TO_SCRIPT = helpers.read_config("ANTA23_MERCEDES")
MOVE_ADDITIONAL_X = 80
MOVE_ADDITIONAL_Y = 110
continue_script = False
prompt_layers = []
connectedText = ""

def promptStart():
    if nuke.ask('Are you sure you want to continue? This will delete everything and load the template from scratch'):
        global continue_script
        continue_script = True

def deleteStartTemplate():
    for a in nuke.allNodes():
        if a.name() != "Zombie_MetaNode":
            nuke.delete(a)

def setFormat():
    nuke.root()['format'].setValue( 'Still_Square' ) 


def resolve_path(base_path,node):
    tokens = {}
    zombie_meta_node = nuke.toNode('Zombie_MetaNode').knobs()
    zombie_meta = {'Zombie_Parent': zombie_meta_node['Zombie_Parent'].getValue(),
                   'Zombie_Context': zombie_meta_node['Zombie_Context'].getValue(),
                   'Zombie_Version': zombie_meta_node['Zombie_Version'].getValue(),
                   'Zombie_UserShort': zombie_meta_node['Zombie_UserShort'].getValue(),
                   'Zombie_Task': zombie_meta_node['Zombie_Task'].getValue(),
                   'Zombie_Project': zombie_meta_node['Zombie_Project'].getValue(),
                   'Zombie_ProjectID': int(zombie_meta_node['Zombie_ProjectID'].getValue()),
                   'Zombie_ParentID': int(zombie_meta_node['Zombie_ParentID'].getValue()),
                   'Zombie_TaskID': int(zombie_meta_node['Zombie_TaskID'].getValue()),
                   'Zombie_UserID': int(zombie_meta_node['Zombie_UserID'].getValue())}
    if not zombie_meta:
        print("no zombie meta exists")
    root_token = zombie_meta.get("rootdir")
    sg = helpers.get_sg()
    if not root_token:
        root_token = "//pslsrv10" 

    project = sg.find_one('Project', [['id', 'is', zombie_meta['Zombie_ProjectID']]], fields=['sg_name_code'])
    task = sg.find_one('Task', [['id', 'is', zombie_meta['Zombie_TaskID']]], fields=['step'])
    user = sg.find_one('HumanUser', [['id', 'is', zombie_meta['Zombie_UserID']]], fields=['sg_name_short'])

    tokens['$ROOT;'] = root_token

    tokens['$PROJECTNAME;'] = zombie_meta['Zombie_Project']

    tokens['$PROJECTSHORT;'] = project['sg_name_code']

    tokens['$CONTEXT;'] = zombie_meta['Zombie_Context'] + "s"

    tokens['$JOB;'] = zombie_meta['Zombie_Parent']

    tokens['$TASK;'] = zombie_meta['Zombie_Task']

    tokens['$NODE_NAME;'] = node.name()

    tokens['$VERSIONNUMBER;'] = zombie_meta['Zombie_Version'].zfill(3)

    tokens['$TASKSTEP;'] = task['step']['name']

    
    tokens['$USERSHORT;'] = user['sg_name_short']

    tokens['$EXT;'] = 'exr'
    print("here token")
    print(tokens)
    # -------------------------------------- generate saver path --------------------------------------
    for key, value in tokens.items():
        #logger.debug("" + key + ", " + value)
        base_path = base_path.replace(key, value)
    return base_path
    #logger.info("Saver Path is: " + saver_path)


def set_write_nodes():
    
    
    
    
    for node in nuke.allNodes( 'Write' ):
        if "latestEXRSaver" in node.name():
            xml_name = "saver_latest"
        else:
            xml_name = "saver_shot_asset_level"
        path = helpers.read_xml(xml_name)
        if not path:
            print("Path in XMl not set right")
            continue
        node_path = resolve_path(path,node)
        node.knob("file").setValue(node_path)

def loadLooktree():

    p = nuke.Panel('Select Look Tree')
    p.addEnumerationPulldown('Tree', 'GLB_200/Gray GLB_180/Red GLB_Interior GLS_Gray GLS_Gray_INT GLS_Green_INT')
    ret = p.show()
    # save values of previous zombie metanode
    #meta_values = save_metanode()
    if p.value('Tree') == "GLB_200/Gray":
        nuke.nodePaste(PATH_TO_GLB_GRAY)
    elif p.value('Tree') == "GLB_180/Red":
        nuke.nodePaste(PATH_TO_GLB_RED)
    elif p.value('Tree') == "GLB_Interior":
        nuke.nodePaste(PATH_TO_GLB_INT)
    elif p.value('Tree') == "GLS_Gray":
        nuke.nodePaste(PATH_TO_GLS_GRAY)
    elif p.value('Tree') == "GLS_Gray_INT":
        nuke.nodePaste(PATH_TO_GLS_GRAY_INT)
    elif p.value('Tree') == "GLS_Green_INT":
        nuke.nodePaste(PATH_TO_GLS_GREEN_INT)
    else:
        global continue_script
        continue_script = False

def getDir():

    print("\n")

    #Shot path
    shot_dir = str(Path(nuke.script_directory()).parents[1]).split(COMP_DIR)[0]


    #Shot name
    shot_dir = shot_dir.split('\\')[-1]

    #Shotname + CG layers path
    shot_dir = shot_dir + CG_DIR

    #CG layer directory established
    shot_dir = str(Path(nuke.script_directory()).parents[2]) + "\\"+ shot_dir
    #print (shot_dir)
    return shot_dir

def getLayers():

    #List layers folders
    layers = os.listdir(getDir())
    #print(layers)
    return layers

def getLatestReadPaths(layer_list):

    versionNr = 0
    layer_name =""
    appended_utility_list = []
    global moveAdditionalFactor
    moveAdditionalFactor = 0

    #print(layer_list)
    #Iterate over the list of layers inside the CG directory
    for layer in layer_list:

        #Set name variable for read creation
        layer_name = layer

        #Get paths for each layer
        layer_path = getDir() + layer
        #print(layer_path)
        
        #Iterate over versions inside the layer paths
        layer_versions = os.listdir(layer_path)
        #print(layer_versions)
        
        #Iterate over versions to find latest
        for version in layer_versions:
            if int(version[1:]) > versionNr:
                versionNr = int(version[1:])

            #Pad version nr according to renders ****.exr
            latest_version = "v" + str(versionNr).zfill(3)

        #Latest version path for each layer    
        file_path = layer_path + "\\" + latest_version + "\\"

        print (file_path)
        global prompt_version
        prompt_version = latest_version

        versionNr = 0

        if "utility" in layer.lower():
        
            print("found utility layers")

            utility_list = os.listdir(file_path)
            
            for utility_layer in utility_list:
                utility_layer = utility_layer.split(".")[1]

                try:
                    if not isinstance(int(utility_layer), int):
                        pass
                        
                except:
                    appended_utility_list.append(utility_layer)

            appended_utility_list = list(set(appended_utility_list))

        #Get EXR file name based on the latest path

        file_name = (os.listdir(file_path))[0]
        print (file_name)
        file_name = file_name.split(".")[0]
        #print(file_name)

        file_path = file_path + file_name
        #print(file_path)

        createRead(layer, file_path, file_name, appended_utility_list, latest_version)
        moveAdditionalFactor +=1

def createRead(layer, file_path, file_name, appended_utility_list, latest_version):

    frames = []

    #Search filepaths for frames
    glob_search_results = glob.glob(file_path + ".*exr")
    for f in glob_search_results:
        frame = re.findall('\\d+', f)[(-1)]
        frames.append(frame)

    frames = sorted(frames)
    firstframe = frames[0]
    lastframe = frames[(len(frames) - 1)]
    if int(lastframe) < 0:
        lastframe = firstframe

    global prompt_first
    global prompt_last
    prompt_first = firstframe
    prompt_last = lastframe
    global prompt_layers
    

    #Set final read path, frame range and name
    if "utility" in layer.lower():
        appended_utility_list.insert(0, "")
        #print (appended_utility_list)
        for utility_pass in appended_utility_list:
            tempDir = file_path + utility_pass + ".%04d.exr"
            tempDir = file_path + ".%04d.exr"
            tempDir = tempDir.replace("\\", "/")
            r = nuke.createNode('Read')
            r.knob('file').setValue(tempDir)
            r.knob('first').setValue(int(firstframe))
            r.knob('last').setValue(int(lastframe))
            r.knob('origfirst').setValue(int(firstframe))
            r.knob('origlast').setValue(int(lastframe))
            r.knob('name').setValue(f"{layer}_{utility_pass}_read")
            prompt_layers.append([layer + " " + utility_pass, latest_version, firstframe, lastframe])

    else:
        #print(file_path)
        tempDir = file_path + ".%04d.exr"
        tempDir = tempDir.replace("\\", "/")
        r = nuke.createNode('Read')
        r.knob('file').setValue(tempDir)
        r.knob('first').setValue(int(firstframe))
        r.knob('last').setValue(int(lastframe))
        r.knob('origfirst').setValue(int(firstframe))
        r.knob('origlast').setValue(int(lastframe))
        r.knob('name').setValue(f"{layer}_read")
        prompt_layers.append([layer, latest_version, firstframe, lastframe])

    connectCG(layer, appended_utility_list)

def connectCG(layer, appended_utility_list):

    global connectedText

    if "utility" in layer.lower():
        for utility_pass in appended_utility_list:

            print (f"{layer}_{utility_pass}_read")
            read = nuke.toNode( f"{layer}_{utility_pass}_read" )
            input_dot = nuke.toNode(f"{utility_pass.lower()}_dot")

            if nuke.exists(f"{utility_pass.lower()}_dot"):
                input_dot.connectInput(0, read)
                read['ypos'].setValue(input_dot['ypos'].value()-111)
                read['xpos'].setValue(input_dot['xpos'].value()-33)
                connectedText += f"{layer}_{utility_pass}_read connected to {utility_pass.lower()}_dot \n"

            else:
                backdrop= nuke.toNode("additional_reads")
                read['ypos'].setValue(backdrop['ypos'].value()+ MOVE_ADDITIONAL_Y)
                read['xpos'].setValue(backdrop['xpos'].value()+ MOVE_ADDITIONAL_X * moveAdditionalFactor )
                nuke.autoplace(read)



    else:
        read = nuke.toNode( f"{layer}_read" )
        input_dot = nuke.toNode(f"{layer.lower()}_dot")

        if nuke.exists(f"{layer.lower()}_dot"):
            input_dot.connectInput(0, read)
            read['ypos'].setValue(input_dot['ypos'].value()-111)
            read['xpos'].setValue(input_dot['xpos'].value()-33)
            connectedText += f"{layer}_read connected to {layer.lower()}_dot \n"
        else:
            backdrop= nuke.toNode("additional_reads")
            read['ypos'].setValue(backdrop['ypos'].value()+ MOVE_ADDITIONAL_Y)
            read['xpos'].setValue(backdrop['xpos'].value()+ MOVE_ADDITIONAL_X * moveAdditionalFactor )
            nuke.autoplace(read)


def promptChanges():
    nuke.message(f'Latest version is {prompt_version}, root range set to {prompt_first}-{prompt_last}')

def setRootRange():

    frames=[]
    for layer in prompt_layers:
        frames.append(int(layer[2]))
        frames.append(int(layer[3]))
    frames = sorted(frames)
    
    firstframe = frames[0]
    lastframe = frames[-1]

    nuke.root()['first_frame'].setValue(firstframe)
    nuke.root()['last_frame'].setValue(lastframe)

    promptLayersRanges(firstframe, lastframe)

def promptLayersRanges(firstframe, lastframe):
    message = ""
    global prompt_layers
    global connectedText
    for layer in prompt_layers:
        message += layer[0] + " " + layer[1] + ", frames " +layer[2] + "-"+layer[3]+"\n\n"
    nuke.message(f" Set root range to {firstframe}-{lastframe} \n\n\nLoaded these layers: \n\n" + message + "\n\nAuto-Connected these layers:\n" + connectedText)
    prompt_layers = []
    connectedText = ""

def get_current_metandoe():
    metanode_name = helpers.read_config("metanode_name")

    metaNode = nuke.toNode(metanode_name )
    return metaNode

def main():

    # Checks if user wants to continue script deleting
    promptStart()
    if continue_script:
        
        setFormat()
        # check if the previous script has a zombie metanode
        #metanode = get_current_metandoe()
        #if not metanode:
            #TODO log this proper
            #print("no metanode in scene")
            #return
        deleteStartTemplate()
        loadLooktree()
        #set_write_nodes()

        if continue_script:

            layer_list = getLayers()
            #print(layer_list)
            #This pushes the layers through the other functions
            getLatestReadPaths(layer_list)
            setRootRange()
            #promptLayersRanges()

if __name__ == "__main__":
    main()

#main()