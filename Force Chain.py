import pandas as pd
import numpy as np
import pyvista as pv
import glob
import os

# Constants
DIAMETER = 0.0002  # Diameter of each particle in meters
RADIUS = DIAMETER / 2
E = 1e6  # Young's modulus in Pascals
NU = 0.3  # Poisson's ratio

# Effective Young's modulus for Hertz-Mindlin model
E_star = E / (2 * (1 - NU ** 2))

# Reduced radius (for identical particles)
R_star = RADIUS / 2

# Function to calculate the distance between two particles
def calculate_distance(p1, p2):
    return np.sqrt((p1['Points:0'] - p2['Points:0'])**2 + 
                   (p1['Points:1'] - p2['Points:1'])**2 + 
                   (p1['Points:2'] - p2['Points:2'])**2)

# Function to calculate normal force using Hertz-Mindlin model
def hertz_mindlin_normal_force(delta):
    # Normal force
    F_n = (4/3) * E_star * np.sqrt(R_star) * delta ** (3/2)
    return F_n

# Function to process a single CSV file
def process_csv(file_path):
    try:
        # Read particle data from CSV file
        df = pd.read_csv(file_path)

        # Ensure the required columns are present
        if not all(col in df.columns for col in ['PointIds', 'Points:0', 'Points:1', 'Points:2']):
            print(f"Required columns are missing in {file_path}")
            return

        # List to store contact results
        contact_results = []

        # Check each pair of particles for contact and calculate forces
        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                p1 = df.iloc[i]
                p2 = df.iloc[j]
                distance = calculate_distance(p1, p2)
                
                # Check if the particles are in contact
                if distance <= DIAMETER:
                    # Overlap or deformation
                    delta = DIAMETER - distance
                    # Calculate normal force using Hertz-Mindlin model
                    F_n = hertz_mindlin_normal_force(delta)
                    # Store results
                    contact_results.append((p1['PointIds'], p2['PointIds'], p1['Points:0'], p1['Points:1'], p1['Points:2'], p2['Points:0'], p2['Points:1'], p2['Points:2'], F_n))

        if not contact_results:
            print(f"No contacts found in {file_path}")
            return

        # Create VTK data for visualization in ParaView
        points = []
        lines = []
        forces = []

        point_index_map = {}  # To store the index of each point

        for contact in contact_results:
            x1, y1, z1 = contact[2], contact[3], contact[4]
            x2, y2, z2 = contact[5], contact[6], contact[7]
            F_n = contact[8]

            # Create or get the index of point1
            point1 = (x1, y1, z1)
            if point1 not in point_index_map:
                point_index_map[point1] = len(points)
                points.append(point1)

            # Create or get the index of point2
            point2 = (x2, y2, z2)
            if point2 not in point_index_map:
                point_index_map[point2] = len(points)
                points.append(point2)
            
            # Get the indices of the points
            idx1 = point_index_map[point1]
            idx2 = point_index_map[point2]
            
            # Add the line
            lines.append([2, idx1, idx2])  # Ensure the format is [2, idx1, idx2]
            # Store the force for the line
            forces.append(F_n)

        # Convert to numpy array for VTK
        points = np.array(points)

        # Check that points have three values
        if points.shape[1] != 3:
            print(f"Error in points data for {file_path}: points do not have three values each.")
            return

        lines = np.array(lines)  # Directly convert lines to a numpy array

        # Create a pyvista PolyData object
        poly_data = pv.PolyData()
        poly_data.points = points
        poly_data.lines = lines

        # Add the force as a scalar to the cells (lines)
        if len(forces) == poly_data.n_lines:
            poly_data.cell_data['Force'] = forces
        else:
            print(f"Mismatch: {len(forces)} forces and {poly_data.n_lines} lines.")

        # Save the PolyData to a VTK file in ASCII format (more compatible with older ParaView versions)
        vtk_file_path = file_path.replace('.csv', '.vtk')  # Update the output path for VTK
        poly_data.save(vtk_file_path, binary=False)  # Save in ASCII format for better compatibility

        print(f'VTK file saved to {vtk_file_path}')

    except FileNotFoundError:
        print(f"File not found: {file_path}. Please ensure the file path is correct and the file exists.")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

# Directory containing CSV files
directory_path = r'C:\Users\Dayan\Desktop\ssa\New folder\\'

# Find all CSV files in the directory
csv_files = glob.glob(os.path.join(directory_path, '*.csv'))

# Sort files numerically based on their filenames
csv_files.sort(key=lambda f: int(''.join(filter(str.isdigit, os.path.basename(f)))))

# Process each CSV file
for csv_file in csv_files:
    print(f'Processing file: {csv_file}')
    process_csv(csv_file)
