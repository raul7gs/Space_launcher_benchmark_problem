from lxml import etree
import numpy as np
from scipy.integrate import solve_ivp
from ambiance import Atmosphere


# Equations


def modified_atmosphere(x):
    if x < 80000 and x > 0:
        rho = Atmosphere(x).density
    else:
        rho = Atmosphere(80000).density
    return rho


def first_stage(t, y):
    x = y[0]
    v = y[1]
    return [v, T / ((m0 + mpay) - mdot * t) * np.cos(alpha) - 1 / 2 / (
            (m0 + mpay) - mdot * t) * S * cd * modified_atmosphere(x) * v ** 2 - g * np.sin(gamma)]


tree = etree.parse('ToolInput/toolInput.xml')
root = tree.getroot()

shape = root.xpath("Geometry/Head_shape/text()")[0]
if shape == "Cone":
    cone_angle = float(root.xpath("Geometry/Cone_angle/text()")[0])
    cd = 0.0122 * cone_angle + 0.162
elif shape == "Sphere":
    cd = 0.42
else:
    length_ratio = float(root.xpath("Geometry/L_ratio_ellipse/text()")[0])
    m = -0.01 / 15  # experimental data
    cd = 0.305 + m * (length_ratio - 10)

diameter = float(root.xpath("Geometry/Diameter/text()")[0])
S = np.pi + diameter ** 2 / 4

stages = root.xpath("Stage")

T_stages = []
M_structural_stages = []
Mp_stages = []
mdot_stages = []

for stage in stages:
    T_stages.append(float(stage.xpath("Engines/Thrust/text()")[0]))
    mdot_stages.append(float(stage.xpath("Engines/mdot/text()")[0]))
    try:  # Liquid
        m_pumps = float(stage.xpath("Mass/Pumps/text()")[0])
        m_hydrogen = float(stage.xpath("Mass/Hydrogen/text()")[0])
        m_lox = float(stage.xpath("Mass/LOX/text()")[0])
        m_tanks = float(stage.xpath("Mass/Tanks/text()")[0])
        m_insulation = float(stage.xpath("Mass/Insulation/text()")[0])
        m_structure = m_pumps + m_tanks + m_insulation
        m_p = m_hydrogen + m_lox
    except:  # solid
        m_propellant = float(stage.xpath("Mass/Propellant/text()")[0])
        m_casing = float(stage.xpath("Mass/Casing/text()")[0])
        m_structure =  m_casing
        m_p = m_propellant
    try:
        m_structure = m_structure + float(stage.xpath("Mass/Structure/text()")[0])
    except:
        pass
    M_structural_stages.append(m_structure)
    Mp_stages.append(m_p)

mpay = 0
feasible = 1
h_vector = []
v_vector = []
t_vector = []
stages_max = len(stages) - 1

# Start of the loop
while feasible == 1:
    try:
        # First stage
        h_first = []
        v_first = []
        stage = 0
        T = T_stages[stage]
        gamma = 90 * np.pi / 180
        alpha = 0
        m_unloaded = sum(M_structural_stages[stage:])
        m0 = m_unloaded + sum(Mp_stages[stage:])
        mdot = mdot_stages[stage]

        g = 9.81
        tfinal = Mp_stages[stage] / mdot - 5
        t = np.linspace(0, tfinal, 500)
        sol = solve_ivp(fun=first_stage, t_span=[t[0], t[-1]], y0=[0, 0], t_eval=t)
        h = sol.y[0]
        v = sol.y[1]
        pos, = np.where(h > 10000)

        if len(pos) == 0 and stage < stages_max:  # This means that we needed second rocket stage
            h_first.append(h.tolist())
            v_first.append(v.tolist())
            stage = stage + 1
            T = T_stages[stage]
            m_unloaded = sum(M_structural_stages[stage:])
            m0 = m_unloaded + sum(Mp_stages[stage:])
            mdot = mdot_stages[stage]
            tfinal = Mp_stages[stage] / mdot - 5
            t = np.linspace(0, tfinal, 500)
            sol = solve_ivp(fun=first_stage, t_span=[t[0], t[-1]], y0=[h[-1], v[-1]], t_eval=t)
            h = sol.y[0]
            v = sol.y[1]
            pos, = np.where(h > 10000)
            if len(pos) == 0 and stage < stages_max:  # This means that we needed third rocket stage
                h_first.append(h.tolist())
                v_first.append(v.tolist())
                stage = stage + 1
                T = T_stages[stage]
                m_unloaded = sum(M_structural_stages[stage:])
                m0 = m_unloaded + sum(Mp_stages[stage:])
                mdot = mdot_stages[stage]
                tfinal = Mp_stages[stage] / mdot - 5
                t = np.linspace(0, tfinal, 500)
                sol = solve_ivp(fun=first_stage, t_span=[t[0], t[-1]], y0=[h[-1], v[-1]], t_eval=t)
                h = sol.y[0]
                v = sol.y[1]
                pos, = np.where(h > 10000)
                if len(pos) == 0:
                    h_first.append(h.tolist())
                    v_first.append(v.tolist())
                else:
                    h_append = h[0:pos[0]]
                    v_append = v[0:pos[0]]
                    h_first.append(h_append.tolist())
                    v_first.append(v_append.tolist())
            else:
                h_append = h[0:pos[0]]
                v_append = v[0:pos[0]]
                h_first.append(h_append.tolist())
                v_first.append(v_append.tolist())
        elif len(pos) > 0:
            h_append = h[0:pos[0]]
            v_append = v[0:pos[0]]
            h_first.append(h_append.tolist())
            v_first.append(v_append.tolist())
        else:
            h_first.append(h.tolist())
            v_first.append(v.tolist())

        # Second stage
        h_0 = h[pos[0]]
        v_0 = v[pos[0]]
        t_0 = t[pos[0]]
        m0 = m0 - mdot * t_0
        mp_remaining = Mp_stages[stage] - mdot * t_0  # It could be that the previous stage did not finish
        h_second = []
        v_second = []

        alpha = 5 * np.pi / 180
        gamma = 135 * np.pi / 180

        tfinal = mp_remaining / mdot - 5
        t = np.linspace(0, tfinal, 500)
        sol2 = solve_ivp(fun=first_stage, t_span=[t[0], t[-1]], y0=[h_0, v_0], t_eval=t)
        h = sol2.y[0]
        v = sol2.y[1]
        pos2, = np.where(h > 100000)
        if len(pos2) == 0 and stage < stages_max:  # This means that we needed another rocket stage
            h_second.append(h.tolist())
            v_second.append(v.tolist())
            stage = stage + 1
            mp_remaining = Mp_stages[stage]
            T = T_stages[stage]
            m_unloaded = sum(M_structural_stages[stage:])
            m0 = m_unloaded + sum(Mp_stages[stage:])
            mdot = mdot_stages[stage]
            tfinal = Mp_stages[stage] / mdot - 5
            t = np.linspace(0, tfinal, 500)
            sol2 = solve_ivp(fun=first_stage, t_span=[t[0], t[-1]], y0=[h[-1], v[-1]], t_eval=t)
            h = sol2.y[0]
            v = sol2.y[1]
            pos2, = np.where(h > 100000)
            if len(pos2) == 0 and stage < stages_max:  # This means that we needed another rocket stage
                h_second.append(h.tolist())
                v_second.append(v.tolist())
                stage = stage + 1
                mp_remaining = Mp_stages[stage]
                T = T_stages[stage]
                m_unloaded = sum(M_structural_stages[stage:])
                m0 = m_unloaded + sum(Mp_stages[stage:])
                mdot = mdot_stages[stage]
                tfinal = Mp_stages[stage] / mdot - 5
                t = np.linspace(0, tfinal, 500)
                sol2 = solve_ivp(fun=first_stage, t_span=[t[0], t[-1]], y0=[h[-1], v[-1]], t_eval=t)
                h = sol2.y[0]
                v = sol2.y[1]
                pos2, = np.where(h > 100000)
                if len(pos2) == 0:
                    h_second.append(h.tolist())
                    v_second.append(v.tolist())
                else:
                    h_append = h[0:pos2[0]]
                    v_append = v[0:pos2[0]]
                    h_second.append(h_append.tolist())
                    v_second.append(v_append.tolist())
            else:
                h_append = h[0:pos2[0]]
                v_append = v[0:pos2[0]]
                h_second.append(h_append.tolist())
                v_second.append(v_append.tolist())
        elif len(pos2) > 0:
            h_append = h[0:pos2[0]]
            v_append = v[0:pos2[0]]
            h_second.append(h_append.tolist())
            v_second.append(v_append.tolist())
        else:
            h_second.append(h.tolist())
            v_second.append(v.tolist())

        # Third stage
        v_0 = v[pos2[0]]
        t_0 = t[pos2[0]]
        m0 = m0 - mdot * t_0
        mp_remaining = mp_remaining - mdot * t_0
        tfinal = mp_remaining / mdot
        delta_v = T/mdot * np.log((m0+mpay)/(m0+mpay-mp_remaining))
        v_final = v_0 / 2 + delta_v

        if stage < stages_max:
            stage = stage + 1
            T = T_stages[stage]
            m_unloaded = sum(M_structural_stages[stage:])
            m0 = m_unloaded + sum(Mp_stages[stage:])
            mdot = mdot_stages[stage]
            tfinal = Mp_stages[stage] / mdot
            delta_v = T / ((m0 + mpay) - mdot * tfinal) * tfinal
            v_final = v_final + delta_v
            if stage < stages_max:
                stage = stage + 1
                T = T_stages[stage]
                m_unloaded = sum(M_structural_stages[stage:])
                m0 = m_unloaded + sum(Mp_stages[stage:])
                mdot = mdot_stages[stage]
                tfinal = Mp_stages[stage] / mdot
                delta_v = T / ((m0 + mpay) - mdot * tfinal) * tfinal
                v_final = v_final + delta_v
        mu = 3.986004418e14
        R_earth = 6378e3
        h = 400e3
        v_orbit = (mu / (R_earth + h)) ** 0.5

        if v_final > v_orbit:
            feasible = 1
            mpay = mpay + 100
            h1 = [item for sublist in h_first for item in sublist]
            h2 = [item for sublist in h_second for item in sublist]
            v1 = [item for sublist in v_first for item in sublist]
            v2 = [item for sublist in v_second for item in sublist]
            h_vector = h1 + h2
            v_vector = v1 + v2
        else:
            feasible = 0
    except:
        feasible = 0

mpay = max(mpay - 100, 0)

if mpay ==0:
    h1 = [item for sublist in h_first for item in sublist]
    v1 = [item for sublist in v_first for item in sublist]
    try:
        h2 = [item for sublist in h_second for item in sublist]
        v2 = [item for sublist in v_second for item in sublist]
        h_vector = h1 + h2
        v_vector = v1 + v2
    except:
        h_vector = h1
        v_vector = v1

# Here the outputs are written in the tree

root_output = etree.Element("Rocket")
payload_tree = etree.SubElement(root_output, "Payload")
mass_tree = etree.SubElement(payload_tree, "Mass")
mass_tree.text = str(mpay)

trajectory_tree = etree.SubElement(root_output, "Trajectory")
height_tree = etree.SubElement(trajectory_tree, "Height")
height_tree.text = str(h_vector)
velocity_tree = etree.SubElement(trajectory_tree, "Velocity")
velocity_tree.text = str(v_vector)

tree_output = etree.ElementTree(root_output)
tree_output.write('ToolOutput/toolOutput.xml')
