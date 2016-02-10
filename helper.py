import ast, cmath, functools, itertools, jelly, math, sympy

inf = float('inf')
nan = float('nan')

def conv_dyadic_integer(link, larg, rarg):
	try:
		iconv_larg = int(larg)
		try:
			iconv_rarg = int(rarg)
			return link(iconv_larg, iconv_rarg)
		except:
			return iconv_larg
	except:
		try:
			return int(rarg)
		except:
			return 0

def conv_monadic_integer(link, arg):
	try:
		return link(int(arg))
	except:
		return 0

def from_base(digits, base):
	integer = 0
	for digit in digits:
		integer = base * integer + digit
	return integer

def from_exponents(exponents):
	integer = 1
	for index, exponent in enumerate(exponents):
		integer *= sympy.ntheory.generate.prime(index + 1) ** exponent
	return integer

def div(dividend, divisor, floor = False):
	if divisor == 0:
		return nan if dividend == 0 else inf
	if divisor == inf:
		return 0
	if floor or (type(dividend) == int and type(divisor) == int and not dividend % divisor):
		return int(dividend // divisor)
	return dividend / divisor

def eval(string, dirty = True):
	return listify(ast.literal_eval(string), dirty)

def flatten(argument):
	flat = []
	if type(argument) == list:
		for item in argument:
			flat += flatten(item)
	else:
		flat.append(argument)
	return flat

def identity(argument):
	return argument

def iterable(argument, range = False):
	return argument if type(argument) == list else (jelly.atoms['R'].call(argument) if range else [argument])

def index(haystack, needle):
	for index, item in enumerate(haystack):
		if item == needle:
			return 1 + index
	return 0

def isqrt(number):
	a = number
	b = (a + 1) // 2
	while b < a:
		a = b
		b = (a + number // a) // 2
	return int(a)

def last_input():
	if len(jelly.sys.argv) > 3:
		return eval(jelly.sys.argv[-1])
	return eval(input())

def listify(iterable, dirty = False):
	if type(iterable) == str and dirty:
		return list(iterable)
	if type(iterable) in (int, float, complex) or (type(iterable) == str and len(iterable) == 1):
		return iterable
	return list(listify(item, dirty) for item in iterable)

def multiset_difference(left, right):
	result = iterable(left)[::-1]
	for element in iterable(right):
		if element in result:
			result.remove(element)
	return result[::-1]

def multiset_intersect(left, right):
	right = iterable(right)[:]
	result = []
	for element in iterable(left):
		if element in right:
			result.append(element)
			right.remove(element)
	return result

def multiset_symdif(left, right):
	return multiset_union(multiset_difference(left, right), multiset_difference(right, left))

def multiset_union(left, right):
	return left + multiset_difference(right, left)

def ntimes(links, args, cumulative = False):
	ret, rarg = args
	cumret = []
	for _ in range(jelly.variadic_link(links[1], args) if len(links) == 2 else last_input()):
		if cumulative:
			cumret.append(ret)
		larg = ret
		ret = jelly.variadic_link(links[0], (larg, rarg))
		rarg = larg
	return cumret + [ret] if cumulative else ret

def overload(operators, *args):
	for operator in operators:
		try:
			ret = operator(*args)
		except:
			pass
		else:
			return ret

def Pi(number):
	if type(number) == int:
		return inf if number < 0 else math.factorial(number)
	return math.gamma(number + 1)

def rld(runs):
	return list(itertools.chain(*[[u] * v for u, v in runs]))

def rotate_left(array, units):
	array = iterable(array)
	length = len(array)
	return array[units % length :] + array[: units % length] if length else []

def sparse(link, args, indices):
	larg = args[0]
	indices = [index - 1 if index > 0 else index - 1 + len(larg) for index in iterable(jelly.variadic_link(indices, args))]
	ret = iterable(jelly.variadic_link(link, args))
	return [ret[t] if t in indices else u for t, u in enumerate(larg)]

def split_at(iterable, needle):
	chunk = []
	for element in iterable:
		if element == needle:
			yield chunk
			chunk = []
		else:
			chunk.append(element)
	yield chunk

def stringify(iterable, recurse = True):
	if type(iterable) != list:
		return iterable
	if str in map(type, iterable) and not list in map(type, iterable):
		return ''.join(map(str, iterable))
	iterable = [stringify(item) for item in iterable]
	return stringify(iterable, False) if recurse else iterable

def symmetric_mod(number, half_divisor):
	modulus = number % (2 * half_divisor)
	return modulus - 2 * half_divisor * (modulus > half_divisor)

def trim(trimmee, trimmer, left = False, right = False):
	lindex = 0
	rindex = len(trimmee)
	if left:
		while trimmee[lindex] in trimmer and lindex <= rindex:
			lindex += 1
	if right:
		while trimmee[rindex - 1] in trimmer and lindex <= rindex:
			rindex -= 1
	return trimmee[lindex:rindex]

def try_eval(string):
	try:
		return eval(string)
	except:
		return listify(string, True)

def to_base(integer, base):
	digits = []
	integer = abs(integer)
	base = abs(base)
	if base == 0:
		return [integer]
	if base == 1:
		return [1] * integer
	while integer:
		digits.append(integer % base)
		integer //= base
	return digits[::-1] or [0]

def to_exponents(integer):
	if integer == 1:
		return []
	pairs = sympy.ntheory.factor_.factorint(integer)
	exponents = []
	for prime in sympy.ntheory.generate.primerange(2, max(pairs.keys()) + 1):
		if prime in pairs.keys():
			exponents.append(pairs[prime])
		else:
			exponents.append(0)
	return exponents

def unique(iterable):
	result = []
	for element in iterable:
		if not element in result:
			result.append(element)
	return result

def while_loop(link, condition, args, cumulative = False):
	ret, rarg = args
	cumret = []
	while jelly.variadic_link(condition, (ret, rarg)):
		if cumulative:
			cumret.append(ret)
		larg = ret
		ret = jelly.variadic_link(link, (larg, rarg))
		rarg = larg
	return cumret + [ret] if cumulative else ret