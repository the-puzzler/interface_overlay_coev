from create_interface_summary_funcs import *

reference_pdb_file = r'/file_path'
print('Loading pdb')
reference_atoms = parse_pdb(reference_pdb_file)
print('Finding Interface Atoms')
interface_atoms = find_interface_atoms(reference_atoms)
print('Clustering')
clustered_atoms = cluster_interface_atoms(interface_atoms)
print('Generating summary csv')
interface_summary = create_interface_summary(clustered_atoms)

