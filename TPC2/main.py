import sys

def split(line, delim):			#splits a string by the delimeter and also adds that delimiter to the resulting list
	res = line.split(delim)
	a = []
	for l in res:
		a.append(l)
		a.append(delim)
	op = a.pop()
	return a

def multi_split(line):			#splits a string into a list of strings separated by the different delimiters adding them to the list as well
	l = line
	c = []
	res = []
	a = split(l, 'on')
	for s in a:
		c.extend(split(s, 'off'))
	for s in c:
		res.extend(split(s, '='))
	return res

def getnumber(line):			#extracts the number values in a string
	res = list(filter(str.isdigit, line))
	if res:
		res = int("".join(res))
		return res
	else:
		return 0

def main():
	on = True
	mysum = 0

	lines = []
	for line in sys.stdin:
		line = str.lower(line.rstrip('\n'))
		splitted = multi_split(line)
		for i in splitted:
			if i == "on":
				on = True
			elif i == "off":
				on = False
			elif i == "=":
				print(f"The accumulated numbers equal: {mysum}")
			else:
				if on:
					mysum+=getnumber(i)
				else:
					mysum+=0

if __name__ == "__main__":
    main()