import sys
sys.stdout = open("z88structure.txt", "w")

#input data
dimension = 3 #spatial dimension
kflag = 0 #1 for cylindrical coordinates
nodes_dof = 6 #3 for 3d elements, 6 for 2d elements
mesh = 2 #2 for 2d elements, 3 for 3d elements

#below change the name of Salome mesh file
with open("rura.dat", "r") as mesh_file:
    mesh_list = mesh_file.readlines()

#aurora finite elements numbers (nothing to change here)
triangle_number = 24
quadrilateral_number = 23
hex8nodes_number = 1
hex20nodes_number = 10
tet4nodes_number = 17
tet10nodes_number = 16

data_number = mesh_list[0].split()
nodes_number = int(data_number[0])
second_number = int(data_number[1])
dof = nodes_dof * nodes_number

node = ""

for i in range(1, nodes_number + 1):
    nodes_string = mesh_list[i].split()
    node = node + nodes_string[0] + " " + str(nodes_dof) + " " + nodes_string[1] + " " + nodes_string[2] + " " + nodes_string[3] + "\n"

if mesh == 2:

    triangle = ""
    triangle_counter = 0



    for i in range(nodes_number + 1, nodes_number + second_number + 1):
        if mesh_list[i].split()[1] == "206" and nodes_dof == 6:
            triangle_counter += 1
            triangle_string = mesh_list[i].split()
            triangle = triangle + str(triangle_counter) + " " + str(triangle_number) + "\n" + \
                       triangle_string[2] + " " + \
                       triangle_string[3] + " " + \
                       triangle_string[4] + " " + \
                       triangle_string[5] + " " + \
                       triangle_string[6] + " " + \
                       triangle_string[7] + "\n"

    quadrilateral = ""
    quadrilateral_counter = 0

    for i in range(nodes_number + 1, nodes_number + second_number + 1):
        if mesh_list[i].split()[1] == "208" and nodes_dof == 6:
            quadrilateral_counter += 1
            quadrilateral_string = mesh_list[i].split()
            quadrilateral = quadrilateral + str(triangle_counter + quadrilateral_counter) + " " + str(quadrilateral_number) + "\n" + \
                            quadrilateral_string[2] + " " + \
                            quadrilateral_string[3] + " " + \
                            quadrilateral_string[4] + " " + \
                            quadrilateral_string[5] + " " + \
                            quadrilateral_string[6] + " " + \
                            quadrilateral_string[7] + " " + \
                            quadrilateral_string[8] + " " + \
                            quadrilateral_string[9] + "\n"

elif mesh == 3:

    hex8nodes = ""
    hex8nodes_counter = 0

    for i in range(nodes_number + 1, nodes_number + second_number + 1):
        if mesh_list[i].split()[1] == "308" and nodes_dof == 3:
            hex8nodes_counter += 1
            hex8nodes_string = mesh_list[i].split()
            hex8nodes = hex8nodes + str(hex8nodes_counter) + " " + str(hex8nodes_number) + "\n" + \
                        hex8nodes_string[2] + " " + \
                        hex8nodes_string[3] + " " + \
                        hex8nodes_string[4] + " " + \
                        hex8nodes_string[5] + " " + \
                        hex8nodes_string[6] + " " + \
                        hex8nodes_string[7] + " " + \
                        hex8nodes_string[8] + " " + \
                        hex8nodes_string[9] + "\n"

    hex20nodes = ""
    hex20nodes_counter = 0

    for i in range(nodes_number + 1, nodes_number + second_number + 1):
        if mesh_list[i].split()[1] == "320" and nodes_dof == 3:
            hex20nodes_counter += 1
            hex20nodes_string = mesh_list[i].split()
            hex20nodes = hex20nodes + str(hex20nodes_counter) + " " + str(hex20nodes_number) + "\n" + \
                         hex20nodes_string[2] + " " + \
                         hex20nodes_string[3] + " " + \
                         hex20nodes_string[4] + " " + \
                         hex20nodes_string[5] + " " + \
                         hex20nodes_string[6] + " " + \
                         hex20nodes_string[7] + " " + \
                         hex20nodes_string[8] + " " + \
                         hex20nodes_string[9] + " " + \
                         hex20nodes_string[10] + " " + \
                         hex20nodes_string[11] + " " + \
                         hex20nodes_string[12] + " " + \
                         hex20nodes_string[13] + " " + \
                         hex20nodes_string[14] + " " + \
                         hex20nodes_string[15] + " " + \
                         hex20nodes_string[16] + " " + \
                         hex20nodes_string[17] + " " + \
                         hex20nodes_string[18] + " " + \
                         hex20nodes_string[19] + " " + \
                         hex20nodes_string[20] + " " + \
                         hex20nodes_string[21] + "\n"

    tet4nodes = ""
    tet4nodes_counter = 0

    for i in range(nodes_number + 1, nodes_number + second_number + 1):
        if mesh_list[i].split()[1] == "304" and nodes_dof == 3:
            tet4nodes_counter += 1
            tet4nodes_string = mesh_list[i].split()
            tet4nodes = tet4nodes + str(tet4nodes_counter) + " " + str(tet4nodes_number) + "\n" + \
                        tet4nodes_string[2] + " " + \
                        tet4nodes_string[3] + " " + \
                        tet4nodes_string[4] + " " + \
                        tet4nodes_string[5] + "\n"

    tet10nodes = ""
    tet10nodes_counter = 0

    for i in range(nodes_number + 1, nodes_number + second_number + 1):
        if mesh_list[i].split()[1] == "310" and nodes_dof == 3:
            tet10nodes_counter += 1
            tet10nodes_string = mesh_list[i].split()
            tet10nodes = tet10nodes + str(tet10nodes_counter) + " " + str(tet10nodes_number) + "\n" + \
                         tet10nodes_string[3] + " " + \
                         tet10nodes_string[5] + " " + \
                         tet10nodes_string[4] + " " + \
                         tet10nodes_string[2] + " " + \
                         tet10nodes_string[10] + " " + \
                         tet10nodes_string[11] + " " + \
                         tet10nodes_string[7] + " " + \
                         tet10nodes_string[9] + " " + \
                         tet10nodes_string[8] + " " + \
                         tet10nodes_string[6] + "\n"

if mesh == 2:
    elements_number = triangle_counter + quadrilateral_counter
elif mesh == 3:
    elements_number = hex8nodes_counter + hex20nodes_counter + tet4nodes_counter + tet10nodes_counter

if mesh == 2:
    output_mesh = str(dimension) + " " + \
            str(nodes_number) + " " + \
            str(elements_number) + " " + \
            str(dof) + " " + \
            str(kflag) + " " + \
            "AURORA_V2" + "\n" +\
            node + \
            triangle + \
            quadrilateral

if mesh == 3:
    output_mesh = str(dimension) + " " + \
            str(nodes_number) + " " + \
            str(elements_number) + " " + \
            str(dof) + " " + \
            str(kflag) + " " + \
            "AURORA_V2" + "\n" +\
            node + \
            hex8nodes + \
            hex20nodes + \
            tet4nodes + \
            tet10nodes

print output_mesh

"""sys.stdout = open("z88sets.txt", "w")

with open("rura.unv", "r") as sets_file:
    sets_list = sets_file.readlines()

lines_number_list = []
elements_number_list = []
elements_counter = 0

for i in range(nodes_number, len(sets_list)):
    if (len(sets_list[i].split()[0]) >= 4 \
            and sets_list[i].split()[0][0] == "N" \
            and sets_list[i].split()[0][1] == "O" \
            and sets_list[i].split()[0][2] == "D") \
            or (len(sets_list[i].split()[0]) >= 4 \
            and sets_list[i].split()[0][0] == "M" \
            and sets_list[i].split()[0][1] == "A" \
            and sets_list[i].split()[0][2] == "T"):
        lines_number_list.append(i)
        elements_counter += 1
    elif (len(sets_list[i].split()[0]) >= 4 \
            and sets_list[i].split()[0][0] == "E" \
            and sets_list[i].split()[0][1] == "L" \
            and sets_list[i].split()[0][2] == "E"):
        lines_number_list.append(i)
        elements_counter += 1
        elements_number_list.append(elements_counter)

lines_number_list.append(len(sets_list))

output_group = str(len(lines_number_list) - 1)

for i in range(0, len(lines_number_list) - 1):
    group = []
    full_group = ""
    for j in range(lines_number_list[i] + 1, lines_number_list[i+1] - 1):
        if (i+1) in elements_number_list:
            if (sets_list[j].split()[0] == "7" or sets_list[j].split()[0] == "8") and len(sets_list[j].split()) == 4:
                group.append(str(int(sets_list[j].split()[1])-768))
            elif (sets_list[j].split()[0] == "7" or sets_list[j].split()[0] == "8") and len(sets_list[j].split()) == 8:
                group.append(str(int(sets_list[j].split()[1])-768))
                group.append(str(int(sets_list[j].split()[5])-768))
        else:
            if (sets_list[j].split()[0] == "7" or sets_list[j].split()[0] == "8") and len(sets_list[j].split()) == 4:
                group.append(str(int(sets_list[j].split()[1])))
            elif (sets_list[j].split()[0] == "7" or sets_list[j].split()[0] == "8") and len(sets_list[j].split()) == 8:
                group.append(str(int(sets_list[j].split()[1])))
                group.append(str(int(sets_list[j].split()[5])))
    group_quantity = len(group)
    group.sort()
    group_string = "         "

    for j in range(0, group_quantity):
        if group[j] != group[group_quantity - 1]:
            if j == 9:
                group_string = group_string + str(group[j]) + "\n         "
            elif j > 10 and (j - 9) % 10 == 0:
                group_string = group_string + str(group[j]) + "\n         "
            else:
                group_string = group_string + str(group[j]) + "         "
        else:
            group_string = group_string + str(group[j])
    if sets_list[lines_number_list[i]].strip()[0] + sets_list[lines_number_list[i]].strip()[1] + sets_list[lines_number_list[i]].strip()[2] == "NOD":
        full_group = "\n#NODES UNKNOWN " + str(i+1) + " " + str(group_quantity) + " " + '"' + sets_list[lines_number_list[i]].strip() + '"' + "\n" + group_string
    elif sets_list[lines_number_list[i]].strip()[0] + sets_list[lines_number_list[i]].strip()[1] + sets_list[lines_number_list[i]].strip()[2] == "ELE":
        full_group = "\n#ELEMENTS ELEMENTGEO " + str(i+1) + " " + str(group_quantity) + " " + '"' + sets_list[lines_number_list[i]].strip() + '"' + "\n" + group_string
    output_group = output_group + full_group

print output_group

sys.stdout = open("z88setsactive.txt", "w")

with open("z88sets.txt", "r") as setsactive_file:
    setsactive_list = setsactive_file.readlines()

setsactive_counter = 0
output_setsactive = ""

for i in range(0, len(setsactive_list) - 1):
    if (len(setsactive_list[i].split()[0]) >= 4 \
            and setsactive_list[i].split()[0][1] == "E" \
            and setsactive_list[i].split()[0][2] == "L" \
            and setsactive_list[i].split()[0][3] == "E"):

        setsactive_counter += 1
        setsactive = "\n#ELEMENTS ELEMENTGEO 1 " + str(setsactive_counter) + " " + setsactive_list[i].split()[2] + " 9 " + " 1.0 " + setsactive_list[i].split()[-1]
        output_setsactive += setsactive

finish_setsactive = str(setsactive_counter) + output_setsactive

print finish_setsactive"""
