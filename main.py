import re

import plotly.graph_objects as go

if __name__ == '__main__':
    f = open("results.csv", "r")
    num_addr = 0
    num_none = 0
    num_atleast_one = 0
    num_v4_and_v6 = 0
    num_v4 = 0
    avg_v4 = 0
    num_v6 = 0
    avg_v6 = 0
    conn_v4 = 0
    conn_v6 = 0
    conn_both = 0
    v6_no_v4 = 0
    v4_no_v6 = 0
    conn_v6_no_v4 = 0
    conn_v6_no_v4_addr = 0
    conn_v4_no_v6 = 0
    conn_v4_no_v6_addr = 0
    v4_faster_v6 = 0
    v6_faster_v4 = 0
    v6_delta = 0
    v4_delta = 0
    v4_same_v6 = 0

    for x in f:
        num_addr += 1
        line = x.split(";")
        # print(line)
        if int(line[2]) > 0:
            num_v4 += 1
            avg_v4 += int(line[2])
            if int(line[5]) == 0:
                v4_no_v6 += 1
            else:
                num_v4_and_v6 += 1

        if int(line[5]) > 0:
            num_v6 += 1
            avg_v6 += int(line[2])
            if int(line[2]) == 0:
                print("Just v6: " + line[0])
                v6_no_v4 += 1

        if int(line[5]) == 0 and int(line[2]) == 0:
            num_none += 1
        else:
            num_atleast_one += 1

        if line[3] != "0":
            conn_v4 += 1
            if line[6] == "0\n":
                conn_v4_no_v6 += 1
                if int(line[5]) != 0:
                    conn_v4_no_v6_addr += 1
            else:
                conn_both += 1
                if int(line[3]) > int(line[6]):
                    v6_faster_v4 += 1
                    v6_delta += (int(line[3]) - int(line[6]))
                    print("v6 was " + str((int(line[3]) - int(line[6]))) + " faster than v4")
                elif int(line[6]) > int(line[3]):
                    v4_faster_v6 += 1
                    v4_delta += (int(line[6]) - int(line[3]))
                    print("v4 was " + str((int(line[6]) - int(line[3]))) + " faster than v6")
                elif int(line[6]) == int(line[3]):
                    v4_same_v6 += 1
                    print("v4 was " + str((int(line[6]) - int(line[3]))) + " faster than v6 (i.e. the same)")

        if line[6] != "0\n":
            conn_v6 += 1
            if line[3] == "0":
                conn_v6_no_v4 += 1
                if int(line[2]) != 0:
                    conn_v6_no_v4_addr += 1

    avg_v4 = avg_v4 / num_v4
    avg_v6 = avg_v6 / num_v6

print("Number of hosts: " + str(num_addr))
print("Number of hosts with no resolved addresses: " + str(num_none))
print("Number of hosts with v4: " + str(num_v4))
print("Average number of v4 addresses: " + str(avg_v4))
print("Number of connected v4 hosts: " + str(conn_v4))
print("Number of hosts with v6: " + str(num_v6))
print("Average number of v6 addresses: " + str(avg_v6))
print("Number of connected v6 hosts: " + str(conn_v6))

print("Number of hosts with v4 but not v6: " + str(v4_no_v6))
print("Number of hosts with v6 but not v4: " + str(v6_no_v4))
print("Number of hosts connected with v4 but not v6: " + str(conn_v4_no_v6))
print("Number of hosts connected with v6 but not v4: " + str(conn_v6_no_v4))
print("Number of hosts connected with v4 but not v6 even though there is a v6 addr: " + str(conn_v4_no_v6_addr))
print("Number of hosts connected with v6 but not v4 even though there is a v4 addr: " + str(conn_v6_no_v4_addr))
print("Number of hosts faster with v4 than v6: " + str(v4_faster_v6))
print("Number of hosts faster with v6 than v4: " + str(v6_faster_v4))
print("Number of hosts with same time for v6 and v4: " + str(v4_same_v6))
print("Avg time v6 was faster: " + str(v6_delta/v6_faster_v4))
print("Avg time v4 was faster: " + str(v4_delta/v4_faster_v6))
# data
label = ["Hosts", "Hosts with no resolved address", "Hosts with at least one resolved address", "Hosts with v4 and v6",
         "Hosts with just v4", "Hosts with just v6", "Hosts connected with v4 and v6", "Hosts connected with just v4",
         "Hosts connected with just v6", "v4 connected faster", "v6 connected faster", "v4 was just as fast as v6"]
source = [0, 0, 2, 2, 2, 3, 3, 3, 6, 6, 6]
target = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
value = [num_none, num_atleast_one, num_v4_and_v6, v4_no_v6, v6_no_v4, conn_both, conn_v4_no_v6_addr, conn_v6_no_v4_addr,
         v4_faster_v6, v6_faster_v4, v4_same_v6]
# data to dict, dict to sankey
link = dict(source=source, target=target, value=value)
node = dict(label=label, pad=50, thickness=5)
data = go.Sankey(link=link, node=node)
# plot
fig = go.Figure(data)
fig.show()
