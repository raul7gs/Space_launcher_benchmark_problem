import xml.etree.ElementTree as ET
import ast
import numpy
from ambiance import Atmosphere


def modified_temperature(x):
    if x < 80000 and x > 0:
        temp = Atmosphere(x).temperature
    else:
        temp = Atmosphere(80000).temperature
    return temp

def modified_sound_speed(x):
    if x < 80000 and x > 0:
        sound_speed = Atmosphere(x).speed_of_sound
    else:
        sound_speed = Atmosphere(80000).speed_of_sound
    return sound_speed

tree = ET.parse('ToolInput/toolInput.xml')
root = tree.getroot()

tmax = float(root.find("Temperature/T_max").text)


try:
    h = ast.literal_eval(root.find("Trajectory/Height").text)
    v = numpy.array(ast.literal_eval(root.find("Trajectory/Velocity").text))

    temp = []
    sound_speed = []
    for altitude in h:
        temp.append(modified_temperature(altitude).tolist()[0])
        sound_speed.append(modified_sound_speed(altitude).tolist()[0])

    temp_array = numpy.array(temp)

    sound_speed_array = numpy.array(sound_speed)

    mach = numpy.divide(v,sound_speed_array)

    dynamic_temp = 0.2 * numpy.multiply(numpy.multiply(mach,mach),temp_array)

    total_temp = numpy.sum([temp_array, dynamic_temp], axis=0)

    difference = numpy.subtract(total_temp, tmax * numpy.ones(len(total_temp)))

    constraint = numpy.max(difference)
except:
    constraint = 10000

root_output_tree = ET.Element('Rocket')
temperature_tree = ET.SubElement(root_output_tree, 'Temperature')
constraint_tree = ET.SubElement(temperature_tree, 'Constraint')

constraint_tree.text = str(constraint)

tree_output = ET.ElementTree(root_output_tree)
tree_output.write('ToolOutput/toolOutput.xml')

