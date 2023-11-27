"""Tool used for the calculation of the payload constraint. It is checked if the mass of payload calculated
in the trajectory discipline fits inside the rocket's head."""

import xml.etree.ElementTree as ET


def read_input(path):
    """Inputs from the XML file are read."""

    tree = ET.parse(path)
    root = tree.getroot()

    available_volume = float(root.find("Payload/Available_volume").text)
    mass = float(root.find("Payload/Mass").text)
    density = float(root.find("Payload/Density").text)

    return available_volume, mass, density


def calculate(available_volume, mass, density):
    """Calculation of the constraint. The constraint is satisfied when negative"""

    volume_payload = mass / density
    difference = volume_payload - available_volume

    return difference


def write_output(path, difference):
    """Generation of the output XML file"""

    root_output_tree = ET.Element('Rocket')
    payload_tree = ET.SubElement(root_output_tree, 'Payload')
    constraint_tree = ET.SubElement(payload_tree, 'Constraint')

    constraint_tree.text = str(difference)

    tree_output = ET.ElementTree(root_output_tree)
    tree_output.write(path)

    pass


def run():
    """Execution of the tool"""

    available_volume, mass, density = read_input('ToolInput/toolinput.xml')
    difference = calculate(available_volume, mass, density)
    write_output('ToolOutput/toolOutput.xml', difference)


if __name__ == '__main__':
    run()
