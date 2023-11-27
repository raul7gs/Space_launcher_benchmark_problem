"""Tool used for the calculation of the launcher propellant mass."""

import xml.etree.ElementTree as ET


def read_input(path):
    """Inputs from the XML file are read."""

    tree = ET.parse(path)
    root = tree.getroot()

    srb = len(root.findall("Stage/Engines/Solid/SRB"))
    p80 = len(root.findall("Stage/Engines/Solid/P80"))
    gem60 = len(root.findall("Stage/Engines/Solid/GEM60"))

    volume_tank = float(root.find("Stage/Geometry/Stage_volume").text)

    try:    # Liquid
        volume_h2 = float(root.find("Stage/Geometry/Fuel_tank_volume").text)
        volume_lox = float(root.find("Stage/Geometry/Oxidizer_tank_volume").text)
    except AttributeError:
        volume_h2 = 0
        volume_lox = 0

    return srb, p80, gem60, volume_tank, volume_h2, volume_lox


def calculate(srb, p80, gem60, volume_tank, volume_h2, volume_lox):
    """Calculation of the launcher propellant mass."""

    propellant_mass = 0
    h2_mass = 0
    lox_mass = 0

    densities_per_material = {"PBAN": 1715,    # Propellant densities in kg/m^3
                              "HTPB1912": 1810,
                              "HTPB_APCP": 1650,
                              "LOX": 1140,
                              "LH2": 71}

    corrections_per_material = {"PBAN": 1,    # Correction for ullage volume
                                "HTPB1912": 1,
                                "HTPB_APCP": 1,
                                "LOX": 0.94}

    if srb > 0:
        propellant_mass = densities_per_material["PBAN"] * corrections_per_material["PBAN"] * volume_tank
    elif p80 > 0:
        propellant_mass = densities_per_material["HTPB1912"] * corrections_per_material["HTPB1912"] * volume_tank
    elif gem60 > 0:
        propellant_mass = densities_per_material["HTPB_APCP"] * corrections_per_material["HTPB_APCP"] * volume_tank
    else:
        h2_mass = volume_h2 * densities_per_material["LH2"] * corrections_per_material["LOX"]
        lox_mass = volume_lox * densities_per_material["LOX"] * corrections_per_material["LOX"]

    return propellant_mass, h2_mass, lox_mass


def write_output(path, propellant_mass, h2_mass, lox_mass):
    """Generation of the output XML file"""

    root_output_tree = ET.Element('Rocket')
    stage_tree = ET.SubElement(root_output_tree, 'Stage')
    mass_tree = ET.SubElement(stage_tree, 'Mass')

    if propellant_mass > 0:    # Solid
        propellant_tree = ET.SubElement(mass_tree, 'Propellant')
        propellant_tree.text = str(propellant_mass)

    if h2_mass > 0:    # Liquid
        hydrogen_tree = ET.SubElement(mass_tree, 'Hydrogen')
        hydrogen_tree.text = str(h2_mass)
        lox_tree = ET.SubElement(mass_tree, 'LOX')
        lox_tree.text = str(lox_mass)

    tree_output = ET.ElementTree(root_output_tree)
    tree_output.write(path)

    pass


def run():
    """Execution of the tool"""
    
    srb, p80, gem60, volume_tank, volume_h2, volume_lox = read_input('ToolInput/toolinput.xml')
    propellant_mass, h2_mass, lox_mass = calculate(srb, p80, gem60, volume_tank, volume_h2, volume_lox)
    write_output('ToolOutput/toolOutput.xml', propellant_mass, h2_mass, lox_mass)


if __name__ == '__main__':
    run()
