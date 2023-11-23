import xml.etree.ElementTree as ET
import ast
import numpy
from ambiance import Atmosphere

def modified_atmosphere(x):
    if x < 80000 and x > 0:
        rho = Atmosphere(x).density
    else:
        rho = Atmosphere(80000).density
    return rho

tree = ET.parse('ToolInput/toolInput.xml')
root = tree.getroot()

qmax = float(root.find("Structure/Max_q").text)

try:
    h = ast.literal_eval(root.find("Trajectory/Height").text)
    rho = []
    for altitude in h:
        if altitude < 0:
            rho.append(1.225)
        else:
            rho.append(modified_atmosphere(altitude).tolist()[0])


    v = numpy.array(ast.literal_eval(root.find("Trajectory/Velocity").text))
    rho_array = numpy.array(rho)
    qvector = 0.5 * numpy.multiply(numpy.multiply(v, v), rho_array)

    difference = numpy.subtract(qvector,qmax * numpy.ones(len(qvector)))

    constraint = numpy.max(difference)
except:
    constraint = 10000

root_output_tree = ET.Element('Rocket')
structure_tree = ET.SubElement(root_output_tree, 'Structure')
constraint_tree = ET.SubElement(structure_tree, 'Constraint')

constraint_tree.text = str(constraint)

tree_output = ET.ElementTree(root_output_tree)
tree_output.write('ToolOutput/toolOutput.xml')

