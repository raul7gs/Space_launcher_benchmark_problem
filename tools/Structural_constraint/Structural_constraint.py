"""Tool used for the calculation of the vehicle structural constraint. It is checked if the maximum loads
during the trajectory phase overpass at any moment the maximum load the structure can withstand."""

import xml.etree.ElementTree as ET
import ast
import numpy
from ambiance import Atmosphere


def modified_atmosphere(x):    # Atmospheric model

    if 80000 > x > 0:
        rho = Atmosphere(x).density
    else:
        rho = Atmosphere(80000).density
    return rho


def read_input(path):
    """Inputs from the XML file are read."""

    tree = ET.parse(path)
    root = tree.getroot()

    qmax = float(root.find("Structure/Max_q").text)    # Maximum dynamic pressure in the whole mission
    h = ast.literal_eval(root.find("Trajectory/Height").text)
    v = numpy.array(ast.literal_eval(root.find("Trajectory/Velocity").text))

    return qmax, h, v


def calculate(qmax, h, v):
    """Calculation of the launcher structural constraint. It is considered to have overpassed the maximum
    structural load if it is positive."""

    rho = []
    for altitude in h:
        if altitude < 0:
            rho.append(1.225)
        else:
            rho.append(modified_atmosphere(altitude).tolist()[0])

    rho_array = numpy.array(rho)
    qvector = 0.5 * numpy.multiply(numpy.multiply(v, v), rho_array)
    difference = numpy.subtract(qvector, qmax * numpy.ones(len(qvector)))
    constraint = numpy.max(difference)

    return constraint


def write_output(path, constraint):
    """Generation of the output XML file"""

    root_output_tree = ET.Element('Rocket')
    structure_tree = ET.SubElement(root_output_tree, 'Structure')
    constraint_tree = ET.SubElement(structure_tree, 'Constraint')

    constraint_tree.text = str(constraint)

    tree_output = ET.ElementTree(root_output_tree)
    tree_output.write(path)

    pass


def run():
    """Execution of the tool"""

    qmax, h, v = read_input('ToolInput/toolinput.xml')
    constraint = calculate(qmax, h, v)
    write_output('ToolOutput/toolOutput.xml', constraint)


if __name__ == '__main__':
    run()
