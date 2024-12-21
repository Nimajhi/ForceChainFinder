# ForceChainFinder
A Python-based tool designed to identify and analyze force chains in granular or particulate systems. This script processes simulation data, detects continuous paths of inter-particle forces, and provides insights into their structure and dynamics. Ideal for researchers working in granular mechanics, physics, or CFD-DEM simulations.

## How to use
#### 1. Export Data from ParaView:

Save the simulation data for all time steps as separate CSV files.
Ensure that each CSV file contains the necessary columns, such as ID and Points.

#### 2. Set the Sphere Diameter:

If analyzing data for a single sphere diameter, ensure the simulation setup reflects this.

#### 3. Configure the Script:

Open the Python code and update the file paths to point to the exported CSV files.

Modify any calculation-specific properties in the script, such as force thresholds, material properties, or parameters needed for force chain analysis.
#### 4. Run the Script:

Execute the script to analyze the data and detect force chains.
Output visualizations and metrics will be generated for further study.
