import xml.etree.ElementTree as ET


def read_input(path):

    tree = ET.parse(path)
    root = tree.getroot()

    srb = len(root.findall("Stage/Engines/Solid/SRB"))
    p80 = len(root.findall("Stage/Engines/Solid/P80"))
    gem60 = len(root.findall("Stage/Engines/Solid/GEM60"))

    return srb, p80, gem60


def calculate(srb, p80, gem60):

    thrust = 0
    mdot = 0

    mdot_dic = {"SRB": 5290,
                "P80": 764,
                "GEM60": 463.18}

    thrust_per_engine = {"SRB": 12.45e6,
                         "P80": 2.1e6,
                         "GEM60": 1.245e6}

    if srb + p80 + gem60 > 0:
        thrust = srb * thrust_per_engine["SRB"] + p80 * thrust_per_engine["P80"] + gem60 * thrust_per_engine["GEM60"]
    if srb > 0:
        mdot = mdot_dic["SRB"] * srb
    if p80 > 0:
        mdot = mdot_dic["P80"] * p80
    if gem60 > 0:
        mdot = mdot_dic["GEM60"] * gem60

    return thrust, mdot


def write_output(path, thrust, mdot):

    root_output_tree = ET.Element('Rocket')
    stage_tree = ET.SubElement(root_output_tree, 'Stage')
    engines_tree = ET.SubElement(stage_tree, 'Engines')
    thrust_tree = ET.SubElement(engines_tree, 'Thrust')
    mdot_tree = ET.SubElement(engines_tree, 'mdot')

    thrust_tree.text = str(thrust)
    mdot_tree.text = str(mdot)

    tree_output = ET.ElementTree(root_output_tree)
    tree_output.write(path)
    pass


def run():

    srb, p80, gem60 = read_input('ToolInput/toolinput.xml')
    thrust, mdot = calculate(srb, p80, gem60)
    write_output('ToolOutput/toolOutput.xml', thrust, mdot)


if __name__ == '__main__':
    run()
