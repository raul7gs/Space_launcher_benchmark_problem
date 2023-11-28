# Space launcher benchmark problem
This Github repository contains all the necessary element to execute the dynamic MDA regarding the multistage launcher problem widely discussed in (thesis link). Multiple design disciplines are used together to design a launcher that maximizes the mass of payload to be lifted to a circular orbit while reducing the cost. Different constraints are also added to ensure the design feasibility. The problem is intended to be executed in RCE. There are three different folders in the repository. The first folder contains the RCE workflow file. The second folder contains some example architectures to observe the dynamic behaviour in the execution process.  Finally, the third folder contains all the tools that are needed to be integrated in RCE to execute the problem.

![cohetes(2)](https://github.com/raul7gs/Space_launcher_benchmark_problem/assets/116161286/6d7c0382-e0bd-44dd-ae71-e342352584ef)

# Integration of tools in the workflow

Before executing any architecture, it is necessary to integrate the tools in RCE. The process is the following:
1. First download the tools folder and the wokflow file.
2. Open the RCE workflow found in the repository.
3. In RCE, click on "Tool integration" (upper bar) and then on "Integrate tool".
4. Then select the option to create a new tool from a template and afterwards the option with the return directory.
5. In the next window (tool description) introduce a name to identify the tool wanted to be integrated.
6. Press next twice until you arrive to the Launch setting window. Here press on the Add button. In the Tool directory press again on the three dots and select the folder with the location of the tool (the Cost discipline for example). Then input a version (for example 1.0) and click on "Create arbitrary directory". Press OK and next.
7. In the next window, unclick the option merging the static input. Then again jump to the next window.
8. Finally, click on execution command for windows. Here write python "name" where name is the python file name in the tool. For example, in the case of the Cost discipline, the name is Cost.py, so it is necessary to write "python Cost.py"

The tool is already integrated in RCE. To integrate the tool in the workflow, first you need to delete its corresponding block in the RCE workflow, which is represented by a square with gears in the center. Then drag your tool from the palette tolbar on the right (if it does not appear, activate from window/show view). Finally, make the necessary connections. Connect the input filter with the tool (pressing on the connection button in the palette). Finally, connect the CPACs out folder from the tool with both files in the output filter

<img width="439" alt="rcetutorial2" src="https://github.com/raul7gs/Space_launcher_benchmark_problem/assets/116161286/3a33bc8d-b3ae-46a1-999e-6f7db61db927">


PD: In the case of the trajectory and the structural constraint tools, it is necessary to install an additional package in a virtual environment for the calculations. This package, called ambiance (https://pypi.org/project/ambiance/), is used for all the calculations involving atmospheric properties. As a consequence, it is necessary to include in the first line inside the execution command the activation of the environment. As an example, if conda is used for managing environments and the name of this environment is "space_problem", the line to be added would be "conda activate space_problem".

# How to execute the workflow

Once all the tools have been integrated both in RCE and in the workflow file, click twice on the input provider (top left block). After that, click inside the properties window in the output file called XML and afterward on edit. Here select the one of the XML files from the XML folder (after clicking on the "Select from project" button).

Once this is done, it is just necessary to press play. It is important to remark that is necessary to have Python installed to execute the workflow (as well as the environment mentioned previously). RCE will ask before execution for the location of a Python executable, which can be found in the folder where Python is installed.

There are three examples in this repository, each one with a different number of stages. All of them are feasible and optimum desings. There are different head shapes and types of propulsion, so that all the architectural influences can be observed.

# How to observe the process and the results

Architectural influences can easily be observed during the execution process. Discipline repetition and activation are easily observed in the RCE GUI. To observe data connection and conditional variables it is necessary to observe the modifications applied to the workflow XML file during the execution. This can be done in the workflow data browser, which can be activated in a similar manner as the Palette. 

To obtain the output XML file, click on the output writer inside the workflow data browser. Then right click on the output XML file and click on export.

PD: To try more architectures, just modifify the one of the XML workflow files. Enough information is given in the thesis to do so.

# Optimization process

Right now, the repository only contains the MDA file, so the analysis can be tested, but not the optimization. To perform the optimization, a tool integrating ADORE was used. In the future, an open-source file able to perform the optimization process might be added to the repository. In the meantime, some pieces of advice are given for the user in case it is wanted to implement the optimization. First, it is necessary to remove from all iterator blocks the line stating "RCE.close_all_outputs()", which allows to not end the process after only a full analysis is executed. Then, it is necessary to add an optimizer. There are two possibilities. The first recommended option is to use RCE default optimizer, being necessary to include all the design variables (including the architectural decisions) mentioned in the thesis. A second possible option would be to add an external architecture generator that is open source, as it might be that there are some of them available on the Internet.

If it is achieved to be done correctly, the optimization problem could be solved and a Pareto front could be obtained. For reference, the thesis prohect mentioned before could be used.

# Brother project

This problem has a brother problem based on Fourier series. Its repository can be found in https://github.com/raul7gs/Fourier-benchmark-problem/tree/main

# Contact information

In case the reader finds any error during the execution process, please report it on the email later attached. Also it is encouraged to contact the author in case any problem is found in the MDA implementation process (or even in a possible approach to implement the optimization process)

Email: raulgarcia.alh@gmail.com 

