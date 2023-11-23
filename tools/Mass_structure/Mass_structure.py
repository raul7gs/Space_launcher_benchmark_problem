import xml.etree.ElementTree as ET
from numpy import pi

tree = ET.parse('ToolInput/toolInput.xml')
root = tree.getroot()




length = float(root.find("Stage/Geometry/Length").text)


root_output_tree = ET.Element('Rocket')
stage_tree = ET.SubElement(root_output_tree, 'Stage')
mass_tree = ET.SubElement(stage_tree, 'Mass')


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

try:
    VULCAIN = len(root.findall("Stage/Engines/Liquid/VULCAIN"))
    tag = "VULCAIN"
except:
    VULCAIN = 0

try:
    RS68 = len(root.findall("Stage/Engines/Liquid/RS68"))
    tag = "RS68"
except:
    RS68 = 0

try:
    S_IVB = len(root.findall("Stage/Engines/Liquid/SIVB"))
    tag = "S_IVB"
except:
    S_IVB = 0


if SRB + P80 + GEM60 > 0:    # Solid
    mass_propellant = float(root.find("Stage/Mass/Propellant").text)
    mass_casing = 0.135 * mass_propellant
    casing_tree = ET.SubElement(mass_tree, 'Casing')
    casing_tree.text = str(mass_casing)
else:    # Liquid
    n_engines = VULCAIN + RS68 + S_IVB
    thrust = float(root.find("Stage/Engines/Thrust").text)/n_engines
    expansion_ratio = float(root.find("Stage/Engines/Expansion_ratio").text)
    oxidizer_tank_volume = float(root.find("Stage/Geometry/Oxidizer_tank_volume").text)
    mass_oxidizer_tank = 12.158 * oxidizer_tank_volume
    fuel_tank_volume = float(root.find("Stage/Geometry/Fuel_tank_volume").text)
    mass_fuel_tank = 9.0911 * fuel_tank_volume
    mass_tank = mass_oxidizer_tank + mass_fuel_tank

    s_tank_oxidizer = float(root.find("Stage/Geometry/Oxidizer_tank_surface").text)
    s_tank_fuel = float(root.find("Stage/Geometry/Fuel_tank_surface").text)

    mass_oxidizer_insulation = 1.123 * s_tank_oxidizer
    mass_fuel_insulation = 2.88 * s_tank_fuel
    mass_insulation = mass_oxidizer_insulation + mass_fuel_insulation

    pumps_mass = (7.81e-4 * thrust + 3.37e-5 * expansion_ratio ** 0.5 + 59) * n_engines

    tanks_tree = ET.SubElement(mass_tree, 'Tanks')
    tanks_tree.text = str(mass_tank)

    insulation_tree = ET.SubElement(mass_tree, 'Insulation')
    insulation_tree.text = str(mass_insulation)

    pumps_tree = ET.SubElement(mass_tree, 'Pumps')
    pumps_tree.text = str(pumps_mass)


try:
    head_surface = float(root.find("Stage/Geometry/Head_surface").text)
    surface_stage = head_surface
    material_density = 2780  # kg/m3
    thickness = 0.005

    structure_mass = head_surface * thickness * material_density
    structure_mass_tree = ET.SubElement(mass_tree, 'Structure')
    structure_mass_tree.text = str(structure_mass)
except:
    pass

















tree_output = ET.ElementTree(root_output_tree)
tree_output.write('ToolOutput/toolOutput.xml')
