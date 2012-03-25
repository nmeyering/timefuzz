class Enum:
	"""enum helper class"""
	def __init__(self, *names):
		for number, name in enumerate(names):
			setattr(self, name, number)

duration = Enum(
	"moment",
	"second",
	"minute",
	"hour",
	"day",
	"week",
	"month",
	"year",
	"decade",
	"century")

# each pair (lim, step) represents a limit below which a stepsize of step is used
# this can be changed to suit desired behavior
precisions = {
duration.moment:		[],
duration.second:		[(5,1),(30,5),(60,10),(120,30)],
duration.minute:		[(5,1),(30,5),(60,10),(120,30)],
duration.hour:			[(6,1),(24,3)],
duration.day:				[(6,1)],
duration.week:			[(4,1)],
duration.month:			[(12,1),(24,6)],
duration.year:			[(10,1),(100,10),(1000,100)],
duration.decade:		[(9,1)],
duration.century:		[(1,1)],
}

second = 1
minute = 60 * second
hour = 60 * minute
day = 24 * hour
week = 7 * day
year = 365.25 * day
month = year / 12
decade = 10 * year
century = 100 * year

# these limits determine which time unit to use:
# e.g. for durations below 1 minute, use 'seconds'
limits = {
duration.moment:		1,
duration.second:		1 * minute,
duration.minute:		1 * hour,
duration.hour:			1 * day,
duration.day:				1 * week,
duration.week:			2 * month,
duration.month:			1 * year,
duration.year:			2 * decade,
duration.decade:		1 * century,
duration.century:		-1,
}

# the inverse dictionary to look up units by limits
inv_limits = dict([(v,k) for (k,v) in limits.items()])

# these represent the numerical values of the
# various time units
values = {
duration.moment:		0,
duration.second:		second,
duration.minute:		minute,
duration.hour:			hour,
duration.day:				day,
duration.week:			week,
duration.year:			year,
duration.month:			month,
duration.decade:		decade,
duration.century:		century,
}

del second, minute, hour, day, week, year, month, decade, century

# helper class for "speaking" units..
# singular and plural are the respective forms, plural defaults to a regular "s"-plural
# vowel_onset determines whether or not to use "an" for the indefinite article
class word:
	def __init__(
			self,
			singular,
			plural = None,
			vowel_onset = False):
		self.singular = singular
		self.plural = plural or singular + "s"
		self.vowel_onset = vowel_onset

words = {
duration.moment:		word("moment"),
duration.second:		word("second"),
duration.minute:		word("minute"),
duration.hour:			word("hour", vowel_onset = True),
duration.day:				word("day"),
duration.week:			word("week"),
duration.month:			word("month"),
duration.year:			word("year"),
duration.decade:		word("decade"),
duration.century:		word("century", plural = "centuries"),
#duration.wy:	word("Wyoming"),
}

# This function could probably be replaced by
# using data structures more cleverly.
def unit(time):
	"""The appropriate time unit to use for a given duration in seconds,
as defined via the limits dictionary above."""
	thresholds = list(limits.values())
	thresholds.sort()
	for t in thresholds:
		if time < t:
			return inv_limits[t]
	return duration.century

def fuzz(time, granularity=1):
	"""A human-readable approximate representation of a time duration.
		The granularity parameter can be used to fine-tune granularity.
		values > 1 mean less precision;	values < 1 mean more precision.
	"""
	# first determine appropriate time unit...
	t_unit = unit(time)

	# next, the magnitude given our time unit
	value = 0 if t_unit == duration.moment else int(time // values[t_unit])

	# lastly, figure out the custom precision stuff
	p = precisions[t_unit]
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
	word = words[t_unit]
	if value == 0:
		return word.plural # "months ago", not "0 months" or "0 month"
	if value == 1:
		return "an " if word.vowel_onset else "a " + word.singular
	return "{} {}".format(
			value,
			word.plural)
