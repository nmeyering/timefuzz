from datetime import datetime

second = 1
minute = 60 * second
hour = 60 * minute
day = 24 * hour
week = 7 * day
year = 365 * day
decade = 10 * year

def fuzz(time):
	if time < minute:
		if time < 10:
			return _fuzz_str("second", time)
		else:
			return _fuzz_str("second", round(time * 2, -1) // 2)
	elif time < hour:
		if time // minute <= 5:
			return _fuzz_str("minute", time//minute)
		else:
			return _fuzz_str("minute", round((time // minute) * 2, -1) // 2)
	elif time < 6 * hour:
		return _fuzz_str("hour", time//hour)
	elif time < week:
		return _fuzz_str("day", time//day)
	elif time < year:
		return _fuzz_str("week", time//week)
	elif time < decade:
		return _fuzz_str("year", time//year)
	elif time < 6 * decade:
		return _fuzz_str("decade", time//decade)
	else:
		return "really long"

def _fuzz_str(unit, magnitude):
	return "about {} {}{}".format(magnitude, unit, "s" if magnitude > 1 else "")
