import xml.etree.ElementTree as ET


tree = ET.parse('ToolInput/toolInput.xml')
root = tree.getroot()

thrust = 0
mdot = 0

mdot_dic = {"SRB": 5290,
            "P80": 764,
            "GEM60": 463.18}

try:
    SRB = len(root.findall("Stage/Engines/Solid/SRB"))
except:
    SRB = 0

try:
    P80 = len(root.findall("Stage/Engines/Solid/P80"))
except:
    P80 = 0

try:
    GEM60 = len(root.findall("Stage/Engines/Solid/GEM60"))
except:
    GEM60 = 0

thrust_per_engine = {"SRB": 12.45e6,
                     "P80": 2.1e6,
                     "GEM60": 1.245e6}

if SRB + P80 + GEM60 > 0:
    thrust = SRB * thrust_per_engine["SRB"] + P80 * thrust_per_engine["P80"] + GEM60 * thrust_per_engine["GEM60"]
if SRB > 0:
    mdot = mdot_dic["SRB"] * SRB
if P80 > 0:
    mdot = mdot_dic["P80"] * P80
if GEM60 > 0:
    mdot = mdot_dic["GEM60"] * GEM60


root_output_tree = ET.Element('Rocket')
stage_tree = ET.SubElement(root_output_tree, 'Stage')
engines_tree = ET.SubElement(stage_tree, 'Engines')
thrust_tree = ET.SubElement(engines_tree, 'Thrust')
mdot_tree = ET.SubElement(engines_tree, 'mdot')

thrust_tree.text = str(thrust)
mdot_tree.text = str(mdot)

tree_output = ET.ElementTree(root_output_tree)
tree_output.write('ToolOutput/toolOutput.xml')

