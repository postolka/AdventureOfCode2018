import re

current = 0
fList = set()
fList.add(0)

lines = [line.rstrip('\n') for line in open('nums.txt')]
printFirst = True

iteration = 100000

resultTotal = None
resultRepeat = None

while iteration:
	iteration -= 1

	for line in lines:
		m = re.match('^([-+])(\\d+)$', line)
		num = int(m.group(2))
		if m.group(1) == '-':
			num *= -1
		# print('{} + ({}) = {}'.format(total, num, total + num))
		current += num

		# fList.add(total)
		if current in fList:
			if resultRepeat is None:
				resultRepeat = current
			iteration = 0
		# print('Adding: {}'.format(total))
		fList.add(current)

	if resultTotal is None:
		resultTotal = current


print('Frequency: {}'.format(resultTotal))
print('Repeat:    {}'.format(resultRepeat))
