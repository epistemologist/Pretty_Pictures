# Implementation of Elementary Cellular Automata
RULE = 190
LENGTH = 64
RULE_SET = map(int, bin(RULE)[2:])
RULE_SET = [0]*(8-len(RULE_SET)) + RULE_SET
RULE_SET = RULE_SET[::-1]
# Set up the initial row
init_row = [0]*LENGTH
init_row[LENGTH/2] = 1
rows = [init_row]

def next_row():
	out = [0]
	for section in [rows[-1][i:i+3] for i in range(len(rows[-1])-2)]:
		out.append(RULE_SET[4*section[0]+2*section[1]+section[2]])
	out.append(0)
	return out

def print_row():
	print("".join([' ' if i==0 else '#' for i in rows[-1]]))
	rows.append(next_row())

for i in range(100):
	print_row()
