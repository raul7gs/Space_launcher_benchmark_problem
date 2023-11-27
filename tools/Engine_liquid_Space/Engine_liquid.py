"""Tool used for the calculation regarding propulsion when a liquid propellant is used. The input is an
XML file containing the engines used in a certain stage. It provides as output the total maximum thrust the
 stage can provide, as well as its mass flow. The expansion ratio of each nozzle is also provided as output.

 More information about the references used can be found in the following link:"""

import xml.etree.ElementTree as ET


def read_input(path):
    """Inputs from the XML file are read."""

    tree = ET.parse(path)
    root = tree.getroot()

    # The number of engines of each possible model are taken from the XML input file.
    vulcain = len(root.findall("Stage/Engines/Liquid/VULCAIN"))
    rs68 = len(root.findall("Stage/Engines/Liquid/RS68"))
    s_ivb = len(root.findall("Stage/Engines/Liquid/SIVB"))

    return vulcain, rs68, s_ivb


def calculate(vulcain, rs68, s_ivb):
    """Calculation of the stage propulsion properties."""

    thrust = 0
    expansion_ratio = 0
    mdot = 0

    expansion_ratios = {"VULCAIN": 45,
                        "RS68": 21.5,
                        "S_IVB": 28}

    mdot_dic = {"VULCAIN": 188.33,    # Mass flow in kg/s
                "RS68": 807.39,
                "S_IVB": 247}

    thrust_per_engine = {"VULCAIN": 0.8e6,    # Thrust in N
                         "RS68": 2.891e6,
                         "S_IVB": 0.486e6}

    if vulcain + rs68 + s_ivb > 0:
        thrust = vulcain * thrust_per_engine["VULCAIN"] + rs68 * thrust_per_engine["RS68"] + s_ivb * thrust_per_engine[
            "S_IVB"]

    if vulcain > 0:
        expansion_ratio = expansion_ratios["VULCAIN"]
        mdot = mdot_dic["VULCAIN"] * vulcain

    if rs68 > 0:
        expansion_ratio = expansion_ratios["RS68"]
        mdot = mdot_dic["RS68"] * rs68

    if s_ivb > 0:
        expansion_ratio = expansion_ratios["S_IVB"]
        mdot = mdot_dic["S_IVB"] * s_ivb

    return thrust, expansion_ratio, mdot


def write_output(path, thrust, expansion_ratio, mdot):
    """Generation of the output XML file"""

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
    tree_output.write(path)

    pass


def run():
    """Execution of the tool"""

    vulcain, rs68, s_ivb = read_input('ToolInput/toolinput.xml')
    thrust, expansion_ratio, mdot = calculate(vulcain, rs68, s_ivb)
    write_output('ToolOutput/toolOutput.xml', thrust, expansion_ratio, mdot)


if __name__ == '__main__':
    run()
