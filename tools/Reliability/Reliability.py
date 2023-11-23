from lxml import etree
from math import tan, pi

tree = etree.parse('ToolInput/toolInput.xml')
root = tree.getroot()


stages = root.xpath("Stage")
reliability_stages = []

for stage in stages:
    try:
        SRB = len(stage.xpath("Engines/SRB"))
        beta = 8
    except:
        SRB = 0

    try:
        P80 = len(stage.xpath("Engines/P80"))
        beta = 8
    except:
        P80 = 0

    try:
        GEM60 = len(stage.xpath("Engines/GEM60"))
        beta = 8
    except:
        GEM60 = 0

    try:
        VULCAIN = len(stage.xpath("Engines/VULCAIN"))
        beta = 5
    except:
        VULCAIN = 0

    try:
        RS68 = len(stage.xpath("Engines/RS68"))
        beta = 5
    except:
        RS68 = 0

    try:
        S_IVB = len(stage.xpath("Engines/S_IVB"))
        beta = 5
    except:
        S_IVB = 0




root_output = etree.Element("Rocket")
payload = etree.SubElement(root_output, "Payload")
Available_volume = etree.SubElement(payload, "Available_volume")
Available_volume.text = str(volume_available)

tree_output = etree.ElementTree(root_output)


tree_output.write('ToolOutput/toolOutput.xml')


