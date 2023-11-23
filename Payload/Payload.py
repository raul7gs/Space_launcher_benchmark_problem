import xml.etree.ElementTree as ET


tree = ET.parse('ToolInput/toolInput.xml')
root = tree.getroot()

available_volume = float(root.find("Payload/Available_volume").text)
mass = float(root.find("Payload/Mass").text)
density = float(root.find("Payload/Density").text)

volume_payload = mass/density

difference = volume_payload - available_volume


root_output_tree = ET.Element('Rocket')
payload_tree = ET.SubElement(root_output_tree, 'Payload')
constraint_tree = ET.SubElement(payload_tree, 'Constraint')

constraint_tree.text = str(difference)

tree_output = ET.ElementTree(root_output_tree)
tree_output.write('ToolOutput/toolOutput.xml')

