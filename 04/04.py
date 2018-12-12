import re


def base_n(num, b=None, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
	if not b:
		b = len(numerals)
	return ((num == 0) and numerals[0]) or (base_n(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])


def print_hours(hours):
	return ''.join([base_n(s) for s in hours])


def print_header(line):
	if line == 0:
		return '000000000011111111112222222222333333333344444444445555555555'
	if line == 1:
		return '012345678901234567890123456789012345678901234567890123456789'


def sleepiest_minute(night_hour):
	_max_nights = night_hour[0]
	_max_minute = {0}
	for _minute, _nights in enumerate(night_hour):
		if _nights > _max_nights:
			_max_minute = {_minute}
			_max_nights = _nights
		elif _nights == _max_nights:
			_max_minute.add(_minute)
	return _max_minute, _max_nights


lines = [line.rstrip('\n') for line in open('records.txt')]

guards = {}
new_hour = [0 for x in range(60)]

guard = None
sleep_start = None
line_last = None

# examine_guard = 761
# examine_guard_progress = 761
examine_guard = None
examine_guard_progress = None

debug_hour = new_hour[:]

# for line in sorted(lines)[0:20]:
for line in sorted(lines):
	# print(line)
	record = re.match('^\\[(\\d{4})-(\\d{2})-(\\d{2})\\s+(\\d{2}):(\\d{2})\\]\\s+(.*)$', line).group(1, 2, 3, 4, 5, 6)
	time_data = tuple([int(x) for x in record[0:5]])
	year, month, day, hour, minute = time_data

	if hour == 23:
		minute = 0
		hour = 0
		day += 1

	action = record[5]

	m_guard = re.match('^Guard\\s+#(\\d+)\\s+begins shift$', action)

	if m_guard:
		if sleep_start is not None:
			raise Exception('Guard is already sleeping!')

		if guard and (guard == examine_guard_progress):
			print('  ' + print_header(0))
			print('  ' + print_header(1))
			print('+ ' + print_hours(debug_hour))
			print('> ' + print_hours(guards[examine_guard_progress]))

		debug_hour = new_hour[:]
		guard = int(m_guard.group(1))
		if guard == examine_guard:
			print(line)
			print('Guard coming: {}'.format(guard))
		if guard not in guards:
			guards[guard] = new_hour[:]

	elif guard:
		if guard == examine_guard:
			print(line)
		if action == 'falls asleep':
			if sleep_start is not None:
				raise Exception('Guard is already sleeping!')
				# print(line)
			else:
				sleep_start = minute
		elif action == 'wakes up':
			if sleep_start is None:
				raise Exception('Guard is not sleeping!')
				# print(line)
			else:
				for m in range(sleep_start, minute):
					debug_hour[m] = 1
					guards[guard][m] += 1
				if guard == examine_guard:
					print('Sleeping between [{} - {}]'.format(sleep_start, minute - 1))
				sleep_start = None

guard_sleep_total = {}
guard_sleep_max = 0
guard_sleep_max_id = None

guard_record_max = 0
guard_record_max_id = None

for guard_id, guard_sleep in guards.items():
	# print('Guard {:>6}: '.format('#' + str(guard_id)) + ''.join([str(s) for s in guard_sleep]))

	# total sleep for all nights
	sleep_total = sum(guard_sleep)
	if sleep_total > guard_sleep_max:
		guard_sleep_max = sleep_total
		guard_sleep_max_id = guard_id

	# most slept nights in certain minute
	max_guard_sleep = max(guard_sleep)
	if guard_record_max < max_guard_sleep:
		guard_record_max = max_guard_sleep
		guard_record_max_id = guard_id

	guard_sleep_total[guard_id] = sleep_total

print('Sleepiest guard is {} ({}): '.format('#' + str(guard_sleep_max_id), guard_sleep_max) + print_hours(guards[guard_sleep_max_id]))
# print('Time: {}-{}-{} {}:{}'.format(*time_data))

max_minute, max_nights = sleepiest_minute(guards[guard_sleep_max_id])
print('Sleepiest minute is: [{}] ({} nights asleep)'.format(', '.join([str(m) for m in max_minute]), max_nights))
for m in max_minute:
	print('{} x {} = {}'.format(guard_sleep_max_id, m, guard_sleep_max_id * m))

print('RecordMan guard is {} ({}): '.format('#' + str(guard_record_max_id), guard_record_max) + print_hours(guards[guard_record_max_id]))
max_minute, max_nights = sleepiest_minute(guards[guard_record_max_id])
print('RecordMan minute is: [{}] ({} nights asleep)'.format(', '.join([str(m) for m in max_minute]), max_nights))
for m in max_minute:
	print('{} x {} = {}'.format(guard_record_max_id, m, guard_record_max_id * m))
