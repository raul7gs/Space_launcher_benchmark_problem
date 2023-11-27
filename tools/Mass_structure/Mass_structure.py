"""Tool used for the calculation of all the components' masses contributing to the launcher total mass,
excluding the propellant."""

import xml.etree.ElementTree as ET
from numpy import pi


def read_input(path):
    """Inputs from the XML file are read."""

    tree = ET.parse(path)
    root = tree.getroot()

    srb = len(root.findall("Stage/Engines/Solid/SRB"))
    p80 = len(root.findall("Stage/Engines/Solid/P80"))
    gem60 = len(root.findall("Stage/Engines/Solid/GEM60"))
    vulcain = len(root.findall("Stage/Engines/Liquid/VULCAIN"))
    rs68 = len(root.findall("Stage/Engines/Liquid/RS68"))
    s_ivb = len(root.findall("Stage/Engines/Liquid/SIVB"))

    try:    # Solid propellant
        mass_propellant = float(root.find("Stage/Mass/Propellant").text)
        thrust = float(root.find("Stage/Engines/Thrust").text)
        expansion_ratio = 0
        oxidizer_tank_volume = 0
        fuel_tank_volume = 0
        s_tank_oxidizer = 0
        s_tank_fuel = 0
    except AttributeError:    # Liquid propellant
        mass_propellant = 0
        thrust = float(root.find("Stage/Engines/Thrust").text)
        expansion_ratio = float(root.find("Stage/Engines/Expansion_ratio").text)
        oxidizer_tank_volume = float(root.find("Stage/Geometry/Oxidizer_tank_volume").text)
        fuel_tank_volume = float(root.find("Stage/Geometry/Fuel_tank_volume").text)
        s_tank_oxidizer = float(root.find("Stage/Geometry/Oxidizer_tank_surface").text)
        s_tank_fuel = float(root.find("Stage/Geometry/Fuel_tank_surface").text)

    try:    # If last stage
        head_surface = float(root.find("Stage/Geometry/Head_surface").text)
    except AttributeError:
        head_surface = 0

    return mass_propellant, thrust, expansion_ratio, oxidizer_tank_volume, fuel_tank_volume, s_tank_oxidizer, \
           s_tank_fuel, srb, p80, gem60, vulcain, rs68, s_ivb, head_surface


def calculate(mass_propellant, thrust, expansion_ratio, oxidizer_tank_volume, fuel_tank_volume, s_tank_oxidizer,
              s_tank_fuel, srb, p80, gem60, vulcain, rs68, s_ivb, head_surface):
    """Calculation of the launcher structural mass."""

    if srb + p80 + gem60 > 0:  # Solid
        mass_casing = 0.135 * mass_propellant
        mass_tank = 0
        mass_insulation = 0
        pumps_mass = 0
    else:  # Liquid
        mass_casing = 0
        n_engines = vulcain + rs68 + s_ivb
        thrust_per_engine = thrust / n_engines

        mass_oxidizer_tank = 12.158 * oxidizer_tank_volume
        mass_fuel_tank = 9.0911 * fuel_tank_volume
        mass_tank = mass_oxidizer_tank + mass_fuel_tank
        mass_oxidizer_insulation = 1.123 * s_tank_oxidizer
        mass_fuel_insulation = 2.88 * s_tank_fuel
        mass_insulation = mass_oxidizer_insulation + mass_fuel_insulation
        pumps_mass = (7.81e-4 * thrust_per_engine + 3.37e-5 * expansion_ratio ** 0.5 + 59) * n_engines

    if head_surface > 0:
        material_density = 2780  # kg/m3
        thickness = 0.005
        structure_mass = head_surface * thickness * material_density
    else:
        structure_mass = 0

    return mass_casing, mass_tank, mass_insulation, pumps_mass, structure_mass


def write_output(path, mass_casing, mass_tank, mass_insulation, pumps_mass, structure_mass):
    """Generation of the output XML file"""

    root_output_tree = ET.Element('Rocket')
    stage_tree = ET.SubElement(root_output_tree, 'Stage')
    mass_tree = ET.SubElement(stage_tree, 'Mass')

    if mass_casing > 0:    # Solid
        casing_tree = ET.SubElement(mass_tree, 'Casing')
        casing_tree.text = str(mass_casing)
    else:    # Liquid
        tanks_tree = ET.SubElement(mass_tree, 'Tanks')
        tanks_tree.text = str(mass_tank)

        insulation_tree = ET.SubElement(mass_tree, 'Insulation')
        insulation_tree.text = str(mass_insulation)

        pumps_tree = ET.SubElement(mass_tree, 'Pumps')
        pumps_tree.text = str(pumps_mass)

    if structure_mass > 0:     # Last stage
        structure_mass_tree = ET.SubElement(mass_tree, 'Structure')
        structure_mass_tree.text = str(structure_mass)

    tree_output = ET.ElementTree(root_output_tree)
    tree_output.write(path)

    pass


def run():
    """Execution of the tool"""

    mass_propellant, thrust, expansion_ratio, oxidizer_tank_volume, fuel_tank_volume, s_tank_oxidizer, s_tank_fuel, \
    srb, p80, gem60, vulcain, rs68, s_ivb, head_surface = read_input('ToolInput/toolinput.xml')
    mass_casing, mass_tank, mass_insulation, pumps_mass, structure_mass = calculate(mass_propellant, thrust,
    expansion_ratio, oxidizer_tank_volume, fuel_tank_volume, s_tank_oxidizer, s_tank_fuel, srb, p80, gem60, vulcain,
    rs68, s_ivb, head_surface)
    write_output('ToolOutput/toolOutput.xml', mass_casing, mass_tank, mass_insulation, pumps_mass, structure_mass)


if __name__ == '__main__':
    run()
