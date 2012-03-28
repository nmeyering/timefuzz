class Namespace:
	def __init__(self, **names):
		for name in names.keys():
			setattr(self, name, names[name])

# helper class for "speaking" units..
# singular and plural are the respective forms, plural defaults to a regular "s"-plural
# vowel_onset determines whether or not to use "an" for the indefinite article
class Word:
	def __init__(
			self,
			singular,
			plural = None,
			vowel_onset = False):
		self.singular = singular
		self.plural = plural or singular + "s"
		self.vowel_onset = vowel_onset

class TimeUnit:
	def __init__(
			self,
			value,
			limit,
			precisions,
			word):
		self.value = value
		self.limit = limit
		self.precisions = precisions
		self.word = word

duration = Namespace()
setattr(duration, "second", 1)
setattr(duration, "minute", duration.second * 60)
setattr(duration, "hour", duration.minute * 60)
setattr(duration, "day", duration.hour * 24)
setattr(duration, "week", duration.day * 7)
setattr(duration, "year", int(duration.day * 365.25))
setattr(duration, "month", duration.year // 12)
setattr(duration, "decade", duration.year * 10)
setattr(duration, "century", duration.year * 100)

unit = Namespace(
moment = TimeUnit(0,
	duration.second,
	[],
	Word("moment")),
second = TimeUnit(duration.second,
	duration.minute,
	[(5,1),(30,5),(60,10),(120,30)],
	Word("second")),
minute = TimeUnit(duration.minute,
	duration.hour,
	[(5,1),(30,5),(60,10),(120,30)],
	Word("minute")),
hour = TimeUnit(duration.hour,
	duration.day,
	[(6,1),(24,3)],
	Word("hour",
	vowel_onset = True)),
day = TimeUnit(duration.day,
	duration.week,
	[(6,1)],
	Word("day")),
week = TimeUnit(duration.week,
	2 * duration.month,
	[(4,1)],
	Word("week")),
month = TimeUnit(duration.month,
	duration.year,
	[(12,1),(24,6)],
	Word("month")),
year = TimeUnit(duration.year,
	2 * duration.decade,
	[(10,1),(100,10),(1000,100)],
	Word("year")),
decade = TimeUnit(duration.decade,
	duration.century,
	[(9,1)],
	Word("decade")),
century = TimeUnit(duration.century,
	-1,
	[(1,1)],
	Word("century", plural = "centuries")))

# all limits in a central place
limits = dict([(getattr(unit, u), getattr(unit, u).limit) for u in vars(unit)])
# the inverse dictionary to look up units by limits
inv_limits = dict([(v,k) for (k,v) in limits.items()])

def get_unit(time):
	"""
	The appropriate time unit to use for a given duration in seconds,
	as defined via the limits dictionary above."""
	thresholds = list(limits.values())
	thresholds.sort()
	for t in thresholds:
		if time < t:
			return inv_limits[t]
	return unit.century

def fuzz(time, granularity=1):
	"""
	A human-readable approximate representation of a time duration.
	The granularity parameter can be used to fine-tune granularity.
	values > 1 mean less precision;	values < 1 mean more precision."""
	# first determine appropriate time unit...
	t_unit = get_unit(time)

	# next, the magnitude given our time unit
	value = 0 if t_unit == unit.moment else int(time // t_unit.value)

	# lastly, figure out the custom precision stuff
	p = t_unit.precisions
	p.sort()
	try:
		thresh = value * granularity
		key = next(filter(lambda x: x > thresh, (x[0] for x in p)))
		precision = dict(p)[key]
	except StopIteration:
		# don't use a numeral at all if number too high
		precision = 0

	# values of 0 are used to express "unspecified" as in: "months ago"
	value = 0 if (precision == 0) else ((value // precision) * precision)

	# natural lanugage stuff: spit out the correct word forms and such:
	# TODO make this more configurable
	if value == 0:
		return t_unit.word.plural # "months ago", not "0 months" or "0 month"
	if value == 1:
		return "an " if t_unit.word.vowel_onset else "a " + t_unit.word.singular
	return "{} {}".format(
			value,
			t_unit.word.plural)
