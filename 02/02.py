lines = [line.rstrip('\n') for line in open('boxes.txt')]


def letter_sums(box_id):
	totals = {}
	result = {}
	for l in list(box_id):
		if l in totals:
			totals[l] += 1
		else:
			totals[l] = 1

	for l, cnt in totals.items():
		if cnt in result:
			result[cnt] += 1
		else:
			result[cnt] = 1

	return result


def non_zero(n_sums):
	n_zero = []
	for i, cnt in n_sums.items():
		if cnt:
			n_zero.append(i)
	return n_zero


def box_diff(box_a, box_b, max_diff = 1):
	list_a = list(box_a)
	list_b = list(box_b)
	box_len = len(list_a)
	if box_len != len(list_b):
		raise Exception('not compatible: [{}][{}]'.format(box_a, box_b))

	diff = 0
	for l in range(0, box_len-1):
		if list_a[l] != list_b[l]:
			diff += 1
		if diff > max_diff:
			return box_len

	return diff


def box_common(box_a, box_b):
	list_a = list(box_a)
	list_b = list(box_b)
	box_len = len(list_a)
	if box_len != len(list_b):
		raise Exception('not compatible: [{}][{}]'.format(box_a, box_b))

	common = []
	for l in range(0, box_len-1):
		if list_a[l] == list_b[l]:
			common.append(list_a[l])
	return ''.join(common)


l_2 = 0
l_3 = 0
check_lines = []
connected = []

for line in lines:
	sums = non_zero(letter_sums(line))
	if 2 in sums:
		l_2 += 1
	if 3 in sums:
		l_3 += 1

	for check_line in check_lines:
		if box_diff(check_line, line) == 1:
			connected.append((check_line, line))
	check_lines.append(line)


print('{} * {} = {}'.format(l_2, l_3, l_2 * l_3))

for conn in connected:
	print('Connected: {}'.format(box_common(*conn)))
