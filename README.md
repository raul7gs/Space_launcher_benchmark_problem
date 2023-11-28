# Space launcher benchmark problem
This Github repository contains all the necessary element to execute the dynamic MDA regarding the multistage launcher problem widely discussed in (thesis link). Multiple design disciplines are used together to design a launcher that maximizes the mass of payload to be lifted to a circular orbit while reducing the cost. Different constraints are also added to ensure the design feasibility. The problem is intended to be executed in RCE. There are three different folders in the repository. The first folder contains the RCE workflow file. The second folder contains some example architectures to observe the dynamic behaviour in the execution process.  Finally, the third folder contains all the tools that are needed to be integrated in RCE to execute the problem.

![cohetes(2)](https://github.com/raul7gs/Space_launcher_benchmark_problem/assets/116161286/cfb403c9-fd98-4b4c-bfc3-14e384bd2a48)

<p align="center">
  <img src="http://some_place.com/image.png" />
</p>


# Integration of tools in the workflow

Before executing any architecture, it is necessary to integrate the tools in RCE. The process is the following:
1. First download the tools folder and the wokflow file.
2. Open the RCE workflow found in the repository.
3. In RCE, click on "Tool integration" (upper bar) and then on "Integrate tool".
4. Then select the option to create a new tool from a template and afterwards the option with the return directory.
5. In the next window (tool description) introduce a name to identify the tool wanted to be integrated.
6. Press next twice until you arrive to the Launch setting window. Here press on the Add button. In the Tool directory press again on the three dots and select the folder with the location of the tool (the Y discipline for example). Then input a version (for example 1.0) and click on "Create arbitrary directory". Press OK and next.
7. In the next window, unclick the option merging the static input. Then again jump to the next window.
8. Finally, click on execution command for windows. Here write python "name" where name is the python file name in the tool. For example, in the case of the Y discipline, the name is Y.py, so it is necessary to write python Y.py

The tool is already integrated in RCE. To integrate the tool in the workflow, first you need to delete its corresponding block in the RCE workflow, which is represented by a square with gears in the center. Then drag your tool from the palette tolbar on the right (if it does not appear, activate from window/show view). Finally, make the necessary connections. Connect the input filter with the tool (pressing on the connection button in the palette). Finally, connect the CPACs out folder from the tool with both files in the output filter

<img width="356" alt="tutorialrce" src="https://github.com/raul7gs/Fourier-benchmark-problem/assets/116161286/cda1491b-c166-4442-8cf2-868c33fb5a8f">

