import re


def print_fabric(f_fabric, size=40):
	for f_row in f_fabric[0:size]:
		rs = []
		for f_cell in f_row[0:size]:
			rs.append('#' if cell > 10 else str(f_cell))
		print(''.join(rs))


lines = [line.rstrip('\n') for line in open('proposals.txt')]

claims = []

max_x = 0
max_y = 0

for line in lines:
	claim_str = re.match('^#(\\d+)\\s+@\\s+(\\d+),(\\d+):\\s+(\\d+)x(\\d+)$', line).group(1, 2, 3, 4, 5)

	claim = tuple([int(x) for x in claim_str])
	claims.append(claim)
	claim_id, left, top, width, height = claim
	max_x = max(max_x, left + width)
	max_y = max(max_y, top + height)

print('Fabric size must be at least {}x{}'.format(max_x, max_y))


fab_row = [0 for x in range(max_x)]
fabric = [fab_row[:] for y in range(max_y)]

clean_claims = []

for claim in claims:
	claim_id, left, top, width, height = claim
	# print('Claim# {}: L{} T{} W{}xH{}'.format(*claim))
	for y in range(top, top + height):
		for x in range(left, left + width):
			fabric[y][x] += 1

for claim in claims:
	claim_id, left, top, width, height = claim

	# print('Claim# {}: L{} T{} W{}xH{}'.format(*claim))
	is_clean = True
	for y in range(top, top + height):
		for x in range(left, left + width):
			is_clean &= fabric[y][x] == 1
	if is_clean:
		clean_claims.append(claim_id)

overlaps = 0
for row in fabric:
	for cell in row:
		if cell > 1:
			overlaps += 1

# print_fabric(fabric)

print('Overlapping area: {}'.format(overlaps))
for claim_id in clean_claims:
	print('Clean claim: {}'.format(claim_id))
