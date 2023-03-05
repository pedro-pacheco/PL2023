import re


#prints the dictionary
def printDict(proc):
	res = f'{"Year":<5} | {"No of processes":<5}\n'
	res += '-'*23 + '\n'
	for key in proc:
		res += '{:<5} | {:<5}\n'.format(str(key), proc[key])
	res = res[:len(res)-1] # para tirar o \n no fim
	print(res)

def main():

	f = open("processos.txt", "rt")
	f.readline()
	
	processes_by_year = dict()
	
	er = re.compile(r'::(\d{4})')
	
	for line in f:
		res = er.search(line)
		if res:
			year = res.group(1)
			if year in processes_by_year:
				processes_by_year[year]+= 1
			else:
				processes_by_year[year] = 1
	
	printDict(dict(sorted(processes_by_year.items())))

if __name__ == "__main__":
    main()