import xml.etree.ElementTree as ET

tree = ET.parse('ToolInput/toolInput.xml')
root = tree.getroot()

# The output of this tool is the propellant mas of each stage
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


densities_per_material = {"PBAN": 1715,
                          "HTPB1912": 1810,
                          "HTPB_APCP": 1650,
                          "LOX": 1140,
                          "LH2": 71}

corrections_per_material = {"PBAN": 1,
                            "HTPB1912": 1,
                            "HTPB_APCP": 1,
                            "LOX": 0.94}

volume_tank = float(root.find("Stage/Geometry/Stage_volume").text)


if SRB > 0:
    propellant_mass = densities_per_material["PBAN"] * corrections_per_material["PBAN"] * volume_tank
    propellant_tree = ET.SubElement(mass_tree, 'Propellant')
    propellant_tree.text = str(propellant_mass)
elif P80 > 0:
    propellant_mass = densities_per_material["HTPB1912"] * corrections_per_material["HTPB1912"] * volume_tank
    propellant_tree = ET.SubElement(mass_tree, 'Propellant')
    propellant_tree.text = str(propellant_mass)
elif GEM60 > 0:
    propellant_mass = densities_per_material["HTPB_APCP"] * corrections_per_material["HTPB_APCP"] * volume_tank
    propellant_tree = ET.SubElement(mass_tree, 'Propellant')
    propellant_tree.text = str(propellant_mass)
else:
    volume_h2 = float(root.find("Stage/Geometry/Fuel_tank_volume").text)
    volume_lox = float(root.find("Stage/Geometry/Oxidizer_tank_volume").text)
    h2_mass = volume_h2 * densities_per_material["LH2"] * corrections_per_material["LOX"]
    lox_mass = volume_lox * densities_per_material["LOX"] * corrections_per_material["LOX"]
    hydrogen_tree = ET.SubElement(mass_tree, 'Hydrogen')
    hydrogen_tree.text = str(h2_mass)
    lox_tree = ET.SubElement(mass_tree, 'LOX')
    lox_tree.text = str(lox_mass)




tree_output = ET.ElementTree(root_output_tree)
tree_output.write('ToolOutput/toolOutput.xml')
