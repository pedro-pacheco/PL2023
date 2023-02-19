import matplotlib.pyplot as plt

#calculates the max and min values for age and cholesterol
def calculate_extremes(age, chol, min_age, max_age, min_chol, max_chol):
	if(age<min_age):
		min_age=age
	if(age>max_age):
		max_age=age
	if(chol<min_chol):
		min_chol=chol
	if(chol>max_chol):
		max_chol=chol
	return(min_age, max_age, min_chol, max_chol)

#calculates the max and min limits of the distribution for age and cholesterol
def calculate_distribution_limits(min_age, max_age, min_chol, max_chol):
	age_lower = 5 * (min_age//5)
	age_upper = 5 * ((max_age//5)+1)
	chol_lower = 10 * (min_chol//10)
	chol_upper = 10 * ((max_chol//10)+1)

	return(age_lower, age_upper, chol_lower, chol_upper)

#creates a list with the values for the keys of the age distribution
def create_age_distribution_keys(lower_limit, upper_limit):
	l = []
	res = []
	l.append(lower_limit)
	for x in range(lower_limit+1, upper_limit+1):
		if(x%5==0):
			l.append(x-1)
			l.append(x)
	l.remove(upper_limit)
	for x in range(0, len(l)):
		if(x%2==0):
			res.append((l[x], l[x+1]))
	return res

#creates a list with the values for the keys of the chol distribution
def create_chol_distribution_keys(lower_limit, upper_limit):
	l = []
	res = []
	l.append(lower_limit)
	for x in range(lower_limit+1, upper_limit+1):
		if(x%10==0):
			l.append(x-1)
			l.append(x)
	l.remove(upper_limit)
	for x in range(0, len(l)):
		if(x%2==0):
			res.append((l[x], l[x+1]))
	return res

#creates a dictionary with the distribution of the disease by age
def create_age_distribution(keys_tuples, age_list):
	age_dist = dict()
	for x in keys_tuples:
		a = str(x[0])+'-'+str(x[1])
		age_dist[a] = 0

	for a in age_list:
		for k in keys_tuples:
			if a in range(k[0], k[1]+1):
				age_dist[str(k[0])+'-'+str(k[1])] += 1

	#removing entries with value 0
	for k in list(age_dist.keys()):
		if age_dist[k]==0:
			del age_dist[k]
	return age_dist

#creates a dictionary with the distribution of the disease by cholesterol level
def create_chol_distribution(keys_tuples, chol_list):
	chol_dist = dict()
	for x in keys_tuples:
		a = str(x[0])+'-'+str(x[1])
		chol_dist[a] = 0

	for a in chol_list:
		for k in keys_tuples:
			if a in range(k[0], k[1]+1):
				chol_dist[str(k[0])+'-'+str(k[1])] += 1

	#removing entries with value 0
	for k in list(chol_dist.keys()):
		if chol_dist[k]==0:
			del chol_dist[k]
	return chol_dist

#formats a list with the distribution of the disease by age for printing
def printAgeDist(dist):
	res = f'{"Ages":<6} | {"Total":<5}\n'
	res += '-'*14 + '\n'
	for key in dist:
		res += '{:<6} | {:<5}\n'.format(str(key), dist[key])
	res = res[:len(res)-1] # para tirar o \n no fim
	return res

#formats a list with the distribution of the disease by cholesterol level for printing
def printCholDist(dist):
	res = f'{"Cholesterol":<10} | {"Total":<5}\n'
	res += '-'*19 + '\n'
	for key in dist:
		res += '{:<11} | {:<5}\n'.format(str(key), dist[key])
	res = res[:len(res)-1] # para tirar o \n no fim
	return res

#formats a list with the distribution of the disease by gender for printing
def printGenderDist(dist):
	res = f'{"Gender":<10} | {"Total":<5}\n'
	res += '-'*18 + '\n'
	res += '{:<10} | {:<5}\n'.format('Masculine', dist['M'])
	res += '{:<10} | {:<5}'.format('Feminine', dist['F'])
	return res

#partitions a line from the input file
def partition_line(line):
	(age, gender, bp, chol, beats, disease) = line.rsplit(",")

	return(age, gender, bp, chol, beats, disease)

def main():
	f = open("myheart.csv", "rt")
	f.readline()
	
	min_age = 999
	max_age = 0
	min_chol = 9999
	max_chol = 0

	age_list = []
	chol_list = []

	gender_dist = {"M":0, "F": 0}
	chol_dist = dict()

	for line in f:
		line = line.rstrip('\n')
		(age, gender, bp, chol, beats, disease) = partition_line(line)
		(min_age, max_age, min_chol, max_chol) = calculate_extremes(int(age), int(chol), min_age, max_age, min_chol, max_chol)
		(al, au, cl, cu) = calculate_distribution_limits(min_age, max_age, min_chol, max_chol)
		if(disease=="1"):
			gender_dist[gender]+=1
			age_list.append(int (age))
			chol_list.append(int (chol))

	f.close()

	keys_tuples_age = create_age_distribution_keys(al, au)
	keys_tuples_chol = create_chol_distribution_keys(cl, cu)

	dist_gender = printGenderDist(gender_dist)
	dist_age = printAgeDist	(create_age_distribution(keys_tuples_age, age_list))
	dist_chol = printCholDist(create_chol_distribution(keys_tuples_chol, chol_list))

	print(f"The distribution of the disease by gender is:\n{dist_gender}\n")
	print(f"The distribution of the disease by age is:\n{dist_age}\n")
	print(f"The distribution of the disease by cholesterol level is:\n{dist_chol}")


	plt.subplot(1, 3, 1)
	plt.bar(list(gender_dist.keys()),list(gender_dist.values())) 
	plt.title('Disease distribution by gender')

	plt.subplot(1, 3, 2)
	plt.title('Disease distribution by age')
	ad = create_age_distribution(keys_tuples_age, age_list)
	ages = list(ad.keys())
	values = list(ad.values())
	plt.bar(ages, values)

	plt.subplot(1, 3, 3)
	plt.title('Disease distribution by cholesterol level')
	cd = create_chol_distribution(keys_tuples_chol, chol_list)
	chols = list(cd.keys())
	values2 = list(cd.values())
	plt.barh(chols, values2)

	plt.show()


if __name__ == "__main__":
    main()