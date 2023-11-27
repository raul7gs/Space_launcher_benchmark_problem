"""Tool used for the calculation of the launcher cost. There are three contributors. These are the engines,
the propellant and the head structure."""

from lxml import etree


def read_input(path):
    """Inputs from the XML file are read."""

    tree = etree.parse(path)
    root = tree.getroot()

    stages = root.xpath("Stage")

    n_engines_list = []
    m_engine_list = []
    m_solid_list = []
    m_h2_list = []
    m_lox_list = []
    structure_mass_list = []

    for stage in stages:

        engines_solid = 0
        engines_liquid = 0

        try:
            engines_solid = len(stage.xpath("Engines/Solid")[0].getchildren())
        except IndexError:
            engines_liquid = len(stage.xpath("Engines/Liquid")[0].getchildren())

        n_engines = engines_solid + engines_liquid
        n_engines_list.append(n_engines)

        try:    # Solid
            m_engine = float(stage.xpath("Mass/Casing/text()")[0])
            m_solid = float(stage.xpath("Mass/Propellant/text()")[0])
            m_h2 = 0
            m_lox = 0
        except IndexError:    # Liquid
            m_engine = float(stage.xpath("Mass/Tanks/text()")[0]) + \
                       float(stage.xpath("Mass/Insulation/text()")[0]) + float(stage.xpath("Mass/Pumps/text()")[0])
            m_solid = 0
            m_h2 = float(stage.xpath("Mass/Hydrogen/text()")[0])
            m_lox = float(stage.xpath("Mass/LOX/text()")[0])

        try:
            structure_mass = float(stage.xpath("Mass/Structure/text()")[0])
        except IndexError:
            structure_mass = 0

        m_engine_list.append(m_engine)
        m_solid_list.append(m_solid)
        m_h2_list.append(m_h2)
        m_lox_list.append(m_lox)
        structure_mass_list.append(structure_mass)

    return n_engines_list, m_engine_list, m_solid_list, m_h2_list, m_lox_list, structure_mass_list


def calculate(n_engines_list, m_engine_list, m_solid_list, m_h2_list, m_lox_list, structure_mass_list):
    """Calculation of the launcher cost."""

    # Fuel costs
    fuel_cost_per_kg = {"Solid": 5,
                        "LOX": 0.27,
                        "LH2": 6.1}

    total_cost = 0

    for index in range(len(n_engines_list)):
        n_engines = n_engines_list[index]
        m_engine = m_engine_list[index]
        m_solid = m_solid_list[index]
        m_h2 = m_h2_list[index]
        m_lox = m_lox_list[index]
        structure_mass = structure_mass_list[index]

        # Engine cost
        if m_solid > 0:  # Solid
            production_cost_engines_stage = 0.85 * n_engines * 2.3 * (m_engine + m_solid) ** 0.399  # page 125 TRANSCOST
        else:    # Liquid
            production_cost_engines_stage = 0.85 * n_engines * 5.16 * m_engine ** 0.45  # page 129 TRANSCOST

        engine_cost_years = production_cost_engines_stage
        engine_cost_stage = engine_cost_years * 366518  # Conversion to dollars

        # Propellant cost
        if m_h2 > 0:
            fuel_cost_stage = m_h2 * fuel_cost_per_kg["LH2"] + m_lox * fuel_cost_per_kg["LOX"]
        else:
            fuel_cost_stage = m_solid * fuel_cost_per_kg["Solid"]

        # Structure cost
        if structure_mass > 0:
            material_cost = 3  # Dollars per kg
            structure_cost_stage = material_cost * structure_mass
        else:
            structure_cost_stage = 0

        total_cost = total_cost + engine_cost_stage + fuel_cost_stage + structure_cost_stage

    return total_cost


def write_output(path, total_cost):
    """Generation of the output XML file"""

    root_output = etree.Element("Rocket")
    cost_tree = etree.SubElement(root_output, "Cost")
    total_cost_tree = etree.SubElement(cost_tree, "Total_cost")
    total_cost_tree.text = str(total_cost)

    tree_output = etree.ElementTree(root_output)
    tree_output.write(path)

    pass


def run():
    """Execution of the tool"""
    
    n_engines_list, m_engine_list, m_solid_list, m_h2_list, m_lox_list, structure_mass_list = \
        read_input('ToolInput/toolinput.xml')
    total_cost = calculate(n_engines_list, m_engine_list, m_solid_list, m_h2_list, m_lox_list, structure_mass_list)
    write_output('ToolOutput/toolOutput.xml', total_cost)


if __name__ == '__main__':
    run()
