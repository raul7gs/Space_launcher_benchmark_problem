import xml.etree.ElementTree as ET


tree = ET.parse('ToolInput/toolInput.xml')
root = tree.getroot()

thrust = 0
expansion_ratio = 0
mdot = 0

expansion_ratios = {"VULCAIN": 45,
                    "RS68": 21.5,
                    "S_IVB": 28}

mdot_dic = {"VULCAIN": 188.33,
            "RS68": 807.39,
            "S_IVB": 247}

try:
    VULCAIN = len(root.findall("Stage/Engines/Liquid/VULCAIN"))
except:
    VULCAIN = 0

try:
    RS68 = len(root.findall("Stage/Engines/Liquid/RS68"))
except:
    RS68 = 0

try:
    S_IVB = len(root.findall("Stage/Engines/Liquid/SIVB"))
except:
    S_IVB = 0

thrust_per_engine = {"VULCAIN": 0.8e6,
                     "RS68": 2.891e6,
                     "S_IVB": 0.486e6}

if VULCAIN + RS68 + S_IVB> 0:
    thrust = VULCAIN * thrust_per_engine["VULCAIN"] + RS68 * thrust_per_engine["RS68"] + S_IVB * thrust_per_engine["S_IVB"]

if VULCAIN > 0:
    expansion_ratio = expansion_ratios["VULCAIN"]
    mdot = mdot_dic["VULCAIN"] * VULCAIN

if RS68 > 0:
    expansion_ratio = expansion_ratios["RS68"]
    mdot = mdot_dic["RS68"] * RS68

if S_IVB > 0:
    expansion_ratio = expansion_ratios["S_IVB"]
    mdot = mdot_dic["S_IVB"] * S_IVB


root_output_tree = ET.Element('Rocket')
stage_tree = ET.SubElement(root_output_tree, 'Stage')
engines_tree = ET.SubElement(stage_tree, 'Engines')
thrust_tree = ET.SubElement(engines_tree, 'Thrust')
expansion_tree = ET.SubElement(engines_tree, 'Expansion_ratio')
mdot_tree = ET.SubElement(engines_tree, 'mdot')

thrust_tree.text = str(thrust)
expansion_tree.text = str(expansion_ratio)
mdot_tree.text = str(mdot)

tree_output = ET.ElementTree(root_output_tree)
tree_output.write('ToolOutput/toolOutput.xml')


def read_input(path):
    return a, b, c

def calculate(a, b, c):
    return e, f

def write_output(path, e, f):
    pass


def run():
    a, b, c = read_input('toolinput.xml')
    e, f = calculate(a, b, c)
    write_output('tooloutput.xml', e, f)


if __name__ == '__main__':
    run()
