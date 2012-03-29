#include <map>
#include <iostream>
#include <ostream>
#include <string>
#include <vector>

namespace
{
namespace durations
{
	enum type {moment, second, minute, hour, day, week, month, year, decade, century, size};
}

typedef std::map<durations::type, std::string> duration_map;

typedef long base_unit;

struct precision_step
{
	base_unit point;
	base_unit value;
};

class word
{
public:
explicit
word(
	std::string &_singular,
	std::string &_plural,
	bool _vowel_onset)
:
	singular_(
		_singular),
	plural_(
		_plural),
	vowel_onset_(
		_vowel_onset)
{
}

/*
explicit
word(
	std::string &_singular,
	bool _vowel_onset)
:
	singular_(
		_singular),
	plural_(
		_singular + "s"),
	vowel_onset_(
		_vowel_onset)
{
}

explicit
word(
	std::string &_singular,
	std::string &_plural)
:
	singular_(
		_singular),
	plural_(
		_plural),
	vowel_onset_(
		false)
{
}
*/

std::string
singular()
{
	return singular_;
}


std::string
plural()
{
	return plural_;
}

bool
vowel_onset()
{
	return vowel_onset_;
}

private:
	std::string singular_;
	std::string plural_;
	bool vowel_onset_;
};

class time_unit
{
public:
typedef
std::vector<precision_step>
precision_vector;

explicit
time_unit(
	base_unit _value,
	base_unit _limit,
	std::vector<precision_step> _precisions, // Kopie, egal!
	word _word)
:
	value_(
		_value),
	limit_(
		_limit),
	precisions_(
		_precisions),
	word_(
		_word)
{
}

base_unit const
value() const
{
	return value_;
}

base_unit const
limit() const
{
	return limit_;
}

precision_vector const &
precisions() const
{
	return precisions_;
}

word const &
word() const
{
	return word_;
}

private:

	base_unit value_;
	base_unit limit_;
	precision_vector precisions_;
	word word_;
};

}

int main(
	int argc,
	char * argv[])
{
	duration_map test_map;
	test_map[durations::minute] = "test";
	std::cout << "ASDASD" << std::endl;
	std::cout << durations::second << std::endl;
	std::cout << test_map[durations::minute] << std::endl;
	std::cout << test_map[durations::month] << std::endl;
}
