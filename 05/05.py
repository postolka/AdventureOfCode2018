lines = [line.rstrip('\n') for line in open('polymer.txt')]

chars = 'abcdefghijklmnopqrstuvwxyz'
rules = set(zip(list(chars), list(chars.upper())))


def will_dissolve(a, b):
	for rule in rules:
		if (a == rule[0] and b == rule[1]) or (a == rule[1] and b == rule[0]):
			return True
	return False


def retract(polymer):
	new_len = len(polymer)
	old_len = 0

	while old_len != new_len:
		# print('Current length: {}'.format(new_len))
		old_len = new_len
		polymer_new = []
		li = 0
		while li < new_len:
			if li == (new_len - 1):  # last letter
				polymer_new.append(polymer[li])
			elif not will_dissolve(polymer[li], polymer[li+1]):	 # not dissolve - copy current
				polymer_new.append(polymer[li])
			else:	 # will dissolve - skip to next
				# print('Dissolve: [{}]'.format(letters[li] + letters[li+1]))
				li += 1
			li += 1

		new_len = len(polymer_new)
		# print('Dissolved {} pairs'.format(int((old_len - new_len) / 2)))
		polymer = polymer_new

	return new_len


for line in lines:
	letters = list(line)
	retracted = retract(letters)

	print('Retracted length of original polymer is: {}'.format(retracted))
	minimum_length = len(letters)
	minimum_length_pair = None

	for pair in rules:
		# polymer without ruled-out letters
		letters_reduced = []
		# remove rule letters from whole polymer
		for l in letters:
			if l not in pair:
				letters_reduced.append(l)

		# measure
		letter_retracted = retract(letters_reduced)
		print('Retracting with {} omitted (base len {:>6}): {}'.format(''.join(pair), len(letters_reduced), letter_retracted))
		if letter_retracted < minimum_length:
			minimum_length = letter_retracted
			minimum_length_pair = ''.join(pair)

	print('Overall minimum length is {} for pair {}'.format(minimum_length, minimum_length_pair))
