# z88
Mesh translator Salome .dat format to Z88 Aurora mesh

Just choose the element number and add Salome mesh file in .dat format.

sys.stdout = open("z88structure.txt", "w")

Change these lines in code:

#input data
dimension = 3
kflag = 0 #1 for cylindrical coordinates
nodes_dof = 6
mesh = 2

#aurora finite elements numbers
triangle_number = 24
quadrilateral_number = 23
hex8nodes_number = 1
hex20nodes_number = 10 #unsupported due to Z88 strange nodes ordering procedure
tet4nodes_number = 17
tet10nodes_number = 16 #unsupported due to Z88 strange nodes ordering procedure

with open("rura.dat", "r") as mesh_file:
    mesh_list = mesh_file.readlines()
