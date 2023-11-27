"""Tool used for the calculation of geometric properties later used by other disciplines."""

from lxml import etree
from math import tan, pi
import numpy as np


def read_input(path):
    """Inputs from the XML file are read."""

    tree = etree.parse(path)
    root = tree.getroot()

    stages = root.xpath("Stage")
    l_d = float(root.xpath("Geometry/L_D/text()")[0])

    length_stages_list = []  # The length of each stage is stored in a list

    for stage in stages:
        length_stage = float(stage.xpath("Geometry/Length/text()")[0])
        length_stages_list.append(length_stage)

    head_shape = root.xpath("Geometry/Head_shape/text()")[0]

    try:  # Conical head
        cone_angle = float(root.xpath("Geometry/Cone_angle/text()")[0])
    except IndexError:
        cone_angle = 0

    try:  # Elliptical head
        l_ratio = float(root.xpath("Geometry/L_ratio_ellipse/text()")[0])
    except IndexError:
        l_ratio = 0

    engines_stages = []  # The engines of each stage are stored in a list

    for stage in stages:
        if len(stage.xpath("Engines/Solid/SRB")) > 0:
            engine_stage = "srb" * len(stage.xpath("Engines/Solid/SRB"))
        if len(stage.xpath("Engines/Solid/P80")) > 0:
            engine_stage = "p80" * len(stage.xpath("Engines/Solid/P80"))
        if len(stage.xpath("Engines/Solid/GEM60")) > 0:
            engine_stage = "gem60" * len(stage.xpath("Engines/Solid/GEM60"))
        if len(stage.xpath("Engines/Liquid/VULCAIN")) > 0:
            engine_stage = "vulcain" * len(stage.xpath("Engines/Liquid/VULCAIN"))
        if len(stage.xpath("Engines/Liquid/RS68")) > 0:
            engine_stage = "rs68" * len(stage.xpath("Engines/Liquid/RS68"))
        if len(stage.xpath("Engines/Liquid/SIVB")) > 0:
            engine_stage = "s_ivb" * len(stage.xpath("Engines/Liquid/SIVB"))
        engines_stages.append(engine_stage)

    return l_d, length_stages_list, head_shape, cone_angle, l_ratio, engines_stages


def calculate(l_d, length_stages_list, head_shape, cone_angle, l_ratio, engines_stages):
    """Calculation of the launcher geometric properties."""

    ratio_o_f = 7.937  # Stoichiometric oxidizer to fuel ratio
    densities_per_material = {"LOX": 1140,
                              "LH2": 71}

    total_length = sum(length_stages_list)
    diameter = total_length / l_d
    radius = diameter / 2

    # Head geometric properties
    if head_shape == "Cone":
        h_cone = radius / tan(cone_angle * pi / 180)
        volume_available = 1 / 3 * pi * h_cone * radius ** 2
        g = (radius ** 2 + h_cone ** 2) ** 0.5
        surface_tip = pi * radius * g
    elif head_shape == "Sphere":
        volume_available = 4 / 3 * pi * radius ** 3 / 2
        surface_tip = 2 * pi * radius ** 2
    else:
        l_ellipse = l_ratio * total_length
        volume_available = 2 / 3 * pi * l_ellipse * radius ** 2
        eps = ((l_ellipse ** 2 - radius ** 2) ** 0.5) / l_ellipse
        surface_tip = pi * l_ellipse ** 2 + (np.log((1 + eps) / (1 - eps)) * pi / eps * radius ** 2) / 2

    stages_volume = []
    fuel_volumes = []
    oxidizer_volumes = []
    fuel_surfaces = []
    oxidizer_surfaces = []

    # Propellant related geometric properties
    for stage in range(len(length_stages_list)):

        length_stage = length_stages_list[stage]
        volume_stage = pi * diameter ** 2 / 4 * length_stage
        stages_volume.append(volume_stage)

        vulcain = engines_stages[stage].count("vulcain")
        rs68 = engines_stages[stage].count("rs68")
        s_ivb = engines_stages[stage].count("s_ivb")

        if vulcain + rs68 + s_ivb > 0:
            volume_h2 = volume_stage / (densities_per_material["LH2"] * ratio_o_f / densities_per_material["LOX"] + 1)
            volume_lox = volume_stage - volume_h2
            height_oxidizer = volume_lox / pi / radius / radius
            height_fuel = volume_h2 / pi / radius / radius
            s_tank_oxidizer = pi * radius ** 2 * 2 + 2 * pi * radius * height_oxidizer
            s_tank_fuel = pi * radius ** 2 * 2 + 2 * pi * radius * height_fuel
            fuel_volumes.append(volume_h2)
            oxidizer_volumes.append(volume_lox)
            fuel_surfaces.append(s_tank_fuel)
            oxidizer_surfaces.append(s_tank_oxidizer)
        else:
            volume_h2 = 0
            volume_lox = 0
            s_tank_oxidizer = 0
            s_tank_fuel = 0
            fuel_volumes.append(volume_h2)
            oxidizer_volumes.append(volume_lox)
            fuel_surfaces.append(s_tank_fuel)
            oxidizer_surfaces.append(s_tank_oxidizer)

    return diameter, surface_tip, volume_available, stages_volume, fuel_volumes, oxidizer_volumes, fuel_surfaces, \
           oxidizer_surfaces


def write_output(path, diameter, surface_tip, volume_available, stages_volume, fuel_volumes, oxidizer_volumes,
                 fuel_surfaces, oxidizer_surfaces):
    """Generation of the output XML file"""

    root_output = etree.Element("Rocket")

    for stage_counter in range(len(stages_volume)):

        # The output file already contains all stages. A different tag is added to each stage to ensure correct merging.
        stage = etree.SubElement(root_output, "Stage")
        stage.attrib["UID"] = "stage_{INDEX}".format(INDEX=stage_counter + 1)
        geometry = etree.SubElement(stage, "Geometry")

        stage_volume = etree.SubElement(geometry, "Stage_volume")
        stage_volume.text = str(stages_volume[stage_counter])

        if fuel_volumes[stage_counter] > 0:    # Liquid propellant
            oxidizer_tank_volume = etree.SubElement(geometry, "Oxidizer_tank_volume")
            oxidizer_tank_volume.text = str(oxidizer_volumes[stage_counter])
            fuel_tank_volume = etree.SubElement(geometry, "Fuel_tank_volume")
            fuel_tank_volume.text = str(fuel_volumes[stage_counter])
            oxidizer_tank_surface = etree.SubElement(geometry, "Oxidizer_tank_surface")
            oxidizer_tank_surface.text = str(oxidizer_surfaces[stage_counter])
            fuel_tank_surface = etree.SubElement(geometry, "Fuel_tank_surface")
            fuel_tank_surface.text = str(fuel_surfaces[stage_counter])

    # The head surface is written in the last stage of the XML file
    head_surface = etree.SubElement(geometry, "Head_surface")
    head_surface.text = str(surface_tip)

    payload = etree.SubElement(root_output, "Payload")
    available_volume = etree.SubElement(payload, "Available_volume")
    available_volume.text = str(volume_available)

    geom = etree.SubElement(root_output, "Geometry")
    diameter_tree = etree.SubElement(geom, "Diameter")
    diameter_tree.text = str(diameter)

    tree_output = etree.ElementTree(root_output)

    tree_output.write(path)
    pass


def run():
    """Execution of the tool"""

    l_d, length_stages_list, head_shape, cone_angle, l_ratio, engines_stages = read_input('ToolInput/toolinput.xml')
    diameter, surface_tip, volume_available, stages_volume, fuel_volumes, oxidizer_volumes, fuel_surfaces, \
    oxidizer_surfaces = calculate(l_d, length_stages_list, head_shape, cone_angle, l_ratio, engines_stages)
    write_output('ToolOutput/toolOutput.xml', diameter, surface_tip, volume_available, stages_volume, fuel_volumes,
                 oxidizer_volumes, fuel_surfaces, oxidizer_surfaces)


if __name__ == '__main__':
    run()
