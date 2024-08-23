import numpy as np  # For array handling and mathematical operations
import pandas as pd  # For data manipulation and creating the DataFrame
from sklearn.cluster import KMeans  # For performing KMeans clustering
from tqdm import tqdm  # For progress bar


def create_interface_summary(clustered_atoms):
    interface_summary = {}
    for atom in clustered_atoms:
        key = (atom['chain_id'], atom['cluster'])
        if key not in interface_summary:
            interface_summary[key] = set()
        interface_summary[key].add(atom['res_pos'])

    # Convert the interface_summary to a DataFrame and save to a CSV file
    data = [(chain_id, cluster, res_pos) 
            for (chain_id, cluster), res_positions in interface_summary.items()
            for res_pos in res_positions]
    
    df = pd.DataFrame(data, columns=['chain_id', 'cluster', 'res_pos'])
    df.to_csv('interface_summary.csv', index=False)

    return interface_summary



def cluster_interface_atoms(interface_atoms, n_clusters=40):
    # Prepare lists for coordinates and atom details
    coords = []
    atom_details = []

    # Collect details from the dictionary
    for chain_atoms in tqdm(interface_atoms.values(), desc="Collecting atom details"):
        for atom in chain_atoms:
            coords.append(atom['coords'])
            atom_details.append(atom)  # Ensure atom already contains 'chain_id'

    # Convert to a NumPy array for clustering
    coords = np.array(coords)

    # Perform clustering with KMeans
    print("Performing KMeans clustering...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(coords)
    labels = kmeans.labels_

    # Assign cluster labels to the atoms' details with a progress bar
    for atom, label in tqdm(zip(atom_details, labels), total=len(labels), desc="Assigning cluster labels"):
        atom['cluster'] = label  # Add cluster information

    return atom_details

def find_interface_atoms(atoms, threshold=5):  # default 5 angstrom
    # Extract coordinates and chain IDs
    coords = np.array([atom['coords'] for atom in atoms])
    chain_ids = np.array([atom['chain_id'] for atom in atoms])

    # Compute distances using a vectorized approach
    dist_matrix = np.linalg.norm(coords[:, np.newaxis] - coords, axis=2)

    # Prepare a dictionary to hold interface atoms
    interface_atoms = {}

    # Filter pairs of atoms from different chains that are closer than the threshold
    print("Finding interface atoms...")
    for i in tqdm(range(len(atoms)), desc="Processing atoms"):
        for j in range(len(atoms)):
            if i != j and chain_ids[i] != chain_ids[j] and dist_matrix[i, j] < threshold:
                if chain_ids[i] not in interface_atoms:
                    interface_atoms[chain_ids[i]] = []
                if chain_ids[j] not in interface_atoms:
                    interface_atoms[chain_ids[j]] = []

                # Append entire atom dict, ensuring it includes 'chain_id'
                interface_atoms[chain_ids[i]].append(atoms[i])
                interface_atoms[chain_ids[j]].append(atoms[j])

    return interface_atoms


def parse_pdb(filename):
    atoms = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('ATOM'):
                chain_id = line[21]
                atom_id = line[12:16].strip()
                res_pos = int(line[22:26].strip())  # Cast residue position to integer
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                atoms.append({
                    'chain_id': chain_id,
                    'atom_id': atom_id,
                    'res_pos': res_pos,
                    'coords': (x, y, z)
                })
    return atoms