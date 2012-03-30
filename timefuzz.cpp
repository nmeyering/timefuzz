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

typedef long base_unit;

struct precision_step
{
	base_unit point_;
	base_unit value_;

	precision_step(){};

	explicit
	precision_step(
			base_unit _point,
			base_unit _value)
	:
		point_(
				_point),
		value_(
				_value)
	{
	}
};

class word
{
public:
	explicit
	word(
		std::string const &_singular,
		std::string const &_plural,
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

	explicit
	word(
		std::string const &_singular)
	:
		singular_(
			_singular),
		plural_(
			_singular + "s"),
		vowel_onset_(
			false)
	{
	}

	explicit
	word(
		std::string const &_singular,
		std::string const &_plural)
	:
		singular_(
			_singular),
		plural_(
			_plural),
		vowel_onset_(
			false)
		{
	}

	std::string const &
	singular()
	{
		return singular_;
	}


	std::string const &
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
		word _designation)
	:
		value_(
			_value),
		limit_(
			_limit),
		precisions_(
			_precisions),
		designation_(
			_designation)
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
	designation() const
	{
		return designation_;
	}

private:
	base_unit value_;
	base_unit limit_;
	precision_vector precisions_;
	word designation_;
};


}

int main(
	int argc,
	char * argv[])
{
	typedef std::map<durations::type, time_unit> duration_map;
	duration_map foo;
	std::vector<precision_step> asd{precision_step(0u,0u)};
	time_unit tu(0, 1, asd, word(std::string("moment")));
	std::cout << tu.value() << std::endl;
	// won't work:
	//foo[durations::moment] = tu;
	//std::cout << foo[durations::moment];
}
