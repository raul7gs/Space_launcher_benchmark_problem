from lxml import etree


tree = etree.parse('ToolInput/toolInput.xml')
root = tree.getroot()
total_cost = 0

stages = root.xpath("Stage")

for stage in stages:

    # Engine costs
    try:
        engines_solid = len(stage.xpath("Engines/Solid")[0].getchildren())
    except:
        engines_solid = 0

    try:
        engines_liquid = len(stage.xpath("Engines/Liquid")[0].getchildren())
    except:
        engines_liquid = 0

    n_engines = engines_solid+engines_liquid
    try:    #Solid
        m_engine = float(stage.xpath("Mass/Casing/text()")[0])
        m_solid = float(stage.xpath("Mass/Propellant/text()")[0])
        #development_cost_engines_stage = 10.4 * m_engine**0.6    #page 47
        production_cost_engines_stage = 0.85*n_engines * 2.3 * (m_engine+m_solid)**0.399      #page 125
    except:
        m_engine = float(stage.xpath("Mass/Tanks/text()")[0]) + float(stage.xpath("Mass/Insulation/text()")[0]) + float(stage.xpath("Mass/Pumps/text()")[0])
        #development_cost_engines_stage = 277 * m_engine**0.48    #page 37
        production_cost_engines_stage = 0.85*n_engines * 5.16 * m_engine ** 0.45    #page 129

    engine_cost_years =  production_cost_engines_stage
    engine_cost_stage = engine_cost_years * 366518   # Conversion to dollars

    # Fuel costs
    fuel_cost_per_kg = {"Solid": 5,
                        "LOX": 0.27,
                        "LH2": 6.1}

    try:
        m_h2 = float(stage.xpath("Mass/Hydrogen/text()")[0])
        m_lox = float(stage.xpath("Mass/LOX/text()")[0])
        fuel_cost_stage = m_h2*fuel_cost_per_kg["LH2"]+m_lox*fuel_cost_per_kg["LOX"]
    except:
        fuel_cost_stage = m_solid * fuel_cost_per_kg["Solid"]

    # Structure cost
    try:
        structure_mass = float(stage.xpath("Mass/Structure/text()")[0])
        material_cost = 3    # Dollars per kg
        structure_cost_stage = material_cost*structure_mass
    except:
        structure_cost_stage = 0

    total_cost = total_cost + engine_cost_stage + fuel_cost_stage + structure_cost_stage

root_output = etree.Element("Rocket")
cost_tree = etree.SubElement(root_output, "Cost")
total_cost_tree = etree.SubElement(cost_tree, "Total_cost")
total_cost_tree.text = str(total_cost)

tree_output = etree.ElementTree(root_output)
tree_output.write('ToolOutput/toolOutput.xml')

