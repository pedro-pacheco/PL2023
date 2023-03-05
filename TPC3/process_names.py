import re

def printDicnames(proc):
	res = f'{"Century":<3} | {"First Name":<5} | {"Total":<5}\n'
	res += '-'*28 + '\n'
	for key in proc:		#printing first names
		for fname in proc[key][0]:
			for k in fname:
				res += '{:<2}th    | {:<10} | {:<5}\n'.format(str(key), str(k), str(fname[k]))
	res += '-'*28 + '\n'
	res += '-'*28 + '\n'
	res += f'{"Century":<3} | {"Last Name":<12} | {"Total":<5}\n'
	res += '-'*30 + '\n'
	for key in proc:		#printing last names
		for lname in proc[key][1]:
			for k in lname:
				res += '{:<2}th    | {:<12} | {:<5}\n'.format(str(key), str(k), str(lname[k]))
	print(res)

def printTops(tops, century):
	res = ' '*16 + '-'*14 + '\n'
	res += f'                |{century:<2}th Century|\n'
	res += ' '*16 + '-'*14 + '\n'
	res += f'{"First Name":<10} | {"Total":<5}          {"Last Name":<10} | {"Total":<5}\n'
	res += '-'*18 + ' '*10 + '-'*18 + '\n'
	lf = tops[0]
	lf.sort(key=lambda a: a[1])
	ll = tops[1]
	ll.sort(key=lambda b: b[1])

	for p in range(0, 5):
		res += '{:<10} | {:<5}          {:<10} | {:<5}\n'.format(lf[p][0], lf[p][1], ll[p][0], ll[p][1])
	print(res)
	

def find_lowest(top):
	i=0
	for c, (name, no) in enumerate(top):
		if no<top[i][1]:
			i=c
	return i

def top5(tup):
	top5Last = []
	top5First = []
	lowestf = 100000000
	lowestl = 100000000
	lowest_index_firsts = 0
	lowest_index_lasts = 0
	for fname in tup[0]:
		for k in fname:
			if len(top5First) < 5:
				if fname[k]<lowestf:
					lowestf = fname[k]
					lowest_index_firsts=len(top5First)
				top5First.append((k, fname[k]))
			else:
				lowest_index_firsts=find_lowest(top5First)
				if fname[k]>top5First[lowest_index_firsts][1]:
					del top5First[lowest_index_firsts]
					top5First.append((k, fname[k]))
	for lname in tup[1]:
		for j in lname:
			if len(top5Last)<5:
				if lname[j]<lowestl:
					lowestl=lname[j]
					lowest_index_lasts=len(top5Last)
				top5Last.append((j, lname[j]))
			else:
				lowest_index_lasts=find_lowest(top5Last)
				if lname[j]>top5Last[lowest_index_lasts][1]:
					del top5Last[lowest_index_lasts]
					top5Last.append((j, lname[j]))
	return (top5First, top5Last)



def main():

	f = open("processos.txt", "rt")
	f.readline()

	processes_by_names=dict()

	year_re = re.compile(r'::(\d{4})')
	first_name_re = re.compile(r'::([A-Za-z]+)')
	last_name_re = re.compile(r'([A-Za-z]+)::')

	for line in f:
		res_year=year_re.search(line)
		res_first=first_name_re.search(line)
		res_last=last_name_re.search(line)
		if res_year and res_first and res_last:
			year = int(res_year.group(1))
			f_name = res_first.group(1)
			l_name = res_last.group(1)
			century = (year//100) + 1
			if century in processes_by_names:										#if there's at least one entry in that century
				list_of_fnames = processes_by_names[century][0]						
				list_of_lnames = processes_by_names[century][1]
				flagf = 1
				flagl = 1
				for n in list_of_fnames:											#search for the first name in that century's dictionary
					if f_name in n and flagf:
						n.update({f_name: (n.get(f_name))+1})						#if present, update the value
						flagf = 0
				if flagf:															#first name not in dictionary
					new = {f_name: 1}												#create dictionary entry with value 1
					list_of_fnames.append(new)										#append to list of first names

				for a in list_of_lnames:											#search for the last name in that century's dictionary
					if l_name in a and flagl:
						a.update({l_name: (a.get(l_name))+1})						#if present, update the value
						flagl = 0
				if flagl:															#last name not in dictionary
					newL = {l_name: 1}												#create dictionary entry with value 1
					list_of_lnames.append(newL)										#append to list of last names

				newtuple = (list_of_fnames, list_of_lnames)							#create new tuple of first names and last names for that century
				processes_by_names[century] = newtuple								#update that century with new tuple

			else:																	#if no entries for that century exist
				processes_by_names[century] = ([{f_name: 1}], [{l_name: 1}])		#create a new entry for the century with list of first names and last names with one entry each

	printDicnames(processes_by_names)
	print(f' '*12 + 'TOP 5 NAMES BY CENTURY')
	for k in processes_by_names:
		printTops(top5(processes_by_names[k]), k)

	



if __name__ == "__main__":
    main()