from lxml import etree
from math import tan, pi
import numpy as np

tree = etree.parse('ToolInput/toolInput.xml')
root = tree.getroot()

ratio_o_f = 7.937

densities_per_material = {"LOX": 1140,
                          "LH2": 71}

stages = root.xpath("Stage")
l_d = float(root.xpath("Geometry/L_D/text()")[0])

length_stages_list = []

for stage in stages:
    length_stage = float(stage.xpath("Geometry/Length/text()")[0])
    length_stages_list.append(length_stage)

total_length = sum(length_stages_list)
diameter = total_length / l_d
radius = diameter/2

head_shape = root.xpath("Geometry/Head_shape/text()")[0]

if head_shape == "Cone":
    cone_angle = float(root.xpath("Geometry/Cone_angle/text()")[0])
    h_cone = radius/tan(cone_angle*pi/180)
    volume_available = 1/3 * pi * h_cone * radius**2
    g = (radius ** 2 + h_cone ** 2) ** 0.5
    #surface_tip = pi * radius ** 2 + pi * radius * g
    surface_tip = pi * radius * g
elif head_shape == "Sphere":
    volume_available = 4/3 * pi * radius**3 / 2
    surface_tip = 2 * pi * radius ** 2
else:
    l_ratio = float(root.xpath("Geometry/L_ratio_ellipse/text()")[0])
    l_ellipse = l_ratio * total_length
    volume_available = 2/3 * pi * l_ellipse * radius**2
    eps = ((l_ellipse**2-radius**2)**0.5)/l_ellipse
    surface_tip = pi * l_ellipse**2 + (np.log((1+eps)/(1-eps))*pi/eps*radius**2)/2

root_output = etree.Element("Rocket")

stage_counter = 1

for stage in stages:
    try:
        SRB = len(stage.xpath("Engines/Solid/SRB"))
    except:
        SRB = 0

    try:
        P80 = len(stage.xpath("Engines/Solid/P80"))
    except:
        P80 = 0

    try:
        GEM60 = len(stage.xpath("Engines/Solid/GEM60"))
    except:
        GEM60 = 0

    try:
        VULCAIN = len(stage.xpath("Engines/Liquid/VULCAIN"))
    except:
        VULCAIN = 0

    try:
        RS68 = len(stage.xpath("Engines/Liquid/RS68"))
    except:
        RS68 = 0

    try:
        S_IVB = len(stage.xpath("Engines/Liquid/SIVB"))
    except:
        S_IVB = 0

    length_stage = float(stage.xpath("Geometry/Length/text()")[0])
    volume_stage = pi * diameter ** 2 / 4 * length_stage

    if VULCAIN + RS68 + S_IVB > 0:
        volume_h2 = volume_stage / (densities_per_material["LH2"] * ratio_o_f / densities_per_material["LOX"] + 1)
        volume_lox = volume_stage-volume_h2
        height_oxidizer = volume_lox / pi / radius / radius
        height_fuel = volume_h2 / pi / radius / radius
        s_tank_oxidizer = pi * radius ** 2 * 2 + 2 * pi * radius * height_oxidizer
        s_tank_fuel = pi * radius ** 2 * 2 + 2 * pi * radius * height_fuel
    else:
        volume_h2 = 0
        volume_lox = 0
        s_tank_oxidizer = 0
        s_tank_fuel = 0

    stage = etree.SubElement(root_output, "Stage")
    stage.attrib["UID"] = "stage_{INDEX}".format(INDEX=stage_counter)
    Geometry = etree.SubElement(stage, "Geometry")
    if volume_h2 > 0:
        Oxidizer_tank_volume = etree.SubElement(Geometry, "Oxidizer_tank_volume")
        Oxidizer_tank_volume.text = str(volume_lox)
        Fuel_tank_volume = etree.SubElement(Geometry, "Fuel_tank_volume")
        Fuel_tank_volume.text = str(volume_h2)
        Oxidizer_tank_surface = etree.SubElement(Geometry, "Oxidizer_tank_surface")
        Oxidizer_tank_surface.text = str(s_tank_oxidizer)
        Fuel_tank_surface = etree.SubElement(Geometry, "Fuel_tank_surface")
        Fuel_tank_surface.text = str(s_tank_fuel)

    Stage_volume = etree.SubElement(Geometry, "Stage_volume")
    Stage_volume.text = str(volume_stage)
    stage_counter = stage_counter + 1

#In the last stage
Head_surface = etree.SubElement(Geometry, "Head_surface")
Head_surface.text = str(surface_tip)

payload = etree.SubElement(root_output, "Payload")
Available_volume = etree.SubElement(payload, "Available_volume")
Available_volume.text = str(volume_available)

geom = etree.SubElement(root_output, "Geometry")
Diameter = etree.SubElement(geom, "Diameter")
Diameter.text = str(diameter)


tree_output = etree.ElementTree(root_output)


tree_output.write('ToolOutput/toolOutput.xml')


