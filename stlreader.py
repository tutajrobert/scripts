def read():
    user_prompt = raw_input("Stereolitography file name:" + 
                        "\n")
    if ".stl" in user_prompt:
        pass
    else:
        user_prompt += ".stl"

    nodes_x, nodes_y, nodes_z = [], [], []

    with open(user_prompt) as file:
        file_lines = file.readlines()

    file_length = len(file_lines)
    file_name = file_lines[0].split()[1]

    print("\nsterelitography file loaded \nmodel name: " + file_name)

    for i in range(3, file_length - 2, 7):
        for j in range(0, 3):
            nodes_x.append(float(file_lines[i + j].split()[1]))
            nodes_y.append(float(file_lines[i + j].split()[2]))
            nodes_z.append(float(file_lines[i + j].split()[3]))

    min_x, max_x = min(nodes_x), max(nodes_x)
    min_y, max_y = min(nodes_y), max(nodes_y)
    min_z, max_z = min(nodes_z), max(nodes_z)
    d_x, d_y, d_z = abs(max_x - min_x), abs(max_y - min_y), abs(max_z - min_z)
    cen_x, cen_y, cen_z = (max_x - min_x) / 2, (max_y - min_y)/ 2, (max_z - min_z) / 2

    print ("\ncenX: " + str(cen_x) + ", dX " + str(d_x) + 
           "\ncenY: " + str(cen_y) + ", dY " + str(d_y) +
           "\ncenZ: " + str(cen_z) + ", dZ " + str(d_z))

    return {"file_name" : file_name, "cenX" : cen_x, "cenY" : cen_y, "cenZ" : cen_z,
            "dX" : d_x, "dX" : d_y, "dX" : d_z}
