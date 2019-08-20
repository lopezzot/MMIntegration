# Returns all the combinations
# of size r in an array of size n
def get_combination(arr, n, r):
	# A temporary array to
	# store all combination
	# one by one
	data = [0]*r;
	combination = []
	# Print all combination
	# using temprary array data[]
	final_combination = combination_rec(arr, data, 0, n - 1, 0, r, [], combination);
	return final_combination

def combination_rec(arr, data, start, end, index, r, final_combination, combination):
	# Current combination is ready
	# to be printed, print it
	if (index == r):
		combination = []
		for j in range(r):
			combination.append(data[j])
		final_combination.append(combination)
		return;

	# replace index with all
	# possible elements. The
	# condition "end-i+1 >=
	# r-index" makes sure that
	# including one element at
	# index will make a combination
	# with remaining elements at
	# remaining positions
	i = start;
	while(i <= end and end - i + 1 >= r - index):
		data[index] = arr[i];
		combination_rec(arr, data, i + 1, end, index + 1, r, final_combination, combination);
		i += 1;

	return final_combination

def get_other_probabilities(combination, all_probabilities):
	other = []
	final_value = 1
	for value in all_probabilities:
		if len(combination):
			for i, num in enumerate(combination):
				if num == value:
					combination.pop(i)
					break
				else:
					other.append(value)
					break
		else:
			other.append(value)
	for value in other:
		final_value = final_value * (1-value)
	return final_value

# Returns the probability of
# detecting the particle
# in x layers out of n layers
# in a specific section
def get_section_probability(combinations, x, n, all_probabilities):
	probability = 0
	for values in combinations:
		# gets the probability of the combination
		result = get_combinations_probability(values, x, n, all_probabilities)
		# multiplies all the probabilities
		probability = result + probability
	return probability

# Returns the probability of a combination
def get_combinations_probability(values, x, n, all_probabilities):
	total = 1
	values_copy = []
	for x in values:
		values_copy.append(x)
	other_probability = get_other_probabilities(values_copy, all_probabilities)
	# multiplies all the probabilities of the different layers
	for value in values:
		total = total * value
	# calculates the probability using the binomial distribution
	# probability function
	probability =  total * other_probability
	print "prib"
	print probability

	return probability

# Read the list with efficiency values
# Divide the efficiency values per sections (L1, R1, L2, R2 ...)
def get_probability(values_1, values_2, chamber_type):
	new_values = []
	final_sectors = []
	final_probabilities = []
	# combining the efficincies for the chamber 1 and for the chamber 2
	efficiency = values_1 + values_2
	for value in efficiency:
		new_values.append(float(value)/100)
	# In case it is SM2 or LM2
	if chamber_type == "SM2" or chamber_type == "LM2":
		for i in range(6):
			section_efficiency = []
			for j in range(8):
				section_efficiency.append(new_values[i+6*j])
			final_sectors.append(section_efficiency)
	# In case it is SM1 or LM1
	else:
		for i in range(10):
	#	for i in range(2):
			section_efficiency = []
			for j in range(8):
		#	for j in range(4):
				section_efficiency.append(new_values[i+10*j])
			#	section_efficiency.append(new_values[i+2*j])
			final_sectors.append(section_efficiency)
			print final_sectors

	for sector in final_sectors:
		# getting all the possible combinations for the layers
		#combinations = get_combination(sector, 8, 4)
		section_probability = 0
		# calculating the probability for 4 , 3 , 2 or 1 layer detecting the particle
		for j in range(5):
			combinations = get_combination(sector, 8, 4+j)
			#combinations = get_combination(sector, 4, 2+j)
			probability = get_section_probability(combinations, 4+j, 8, sector) #4+j, 8
			section_probability = section_probability + probability
		final_probabilities.append(section_probability)
	return final_probabilities


# def main():
# 	arr = [1, 2, 3]
# 	r = 2
# 	final_combination = []
# 	n = len(arr)
# 	final_combination = getCombination(arr, n, r)
# 	print final_combination

def main():
	# array = [0.8, 0.85, 0.9]
	# n = 3
	# r = 2
	# comb =  getCombination(array, n, r)
	# print comb
	# print get_section_probability(comb)
	#eff = [100, 80, 40 ,50, 60, 85, 100, 80, 40 ,50, 60, 85, 100, 80, 40 ,50, 60, 85, 100, 80, 40 ,50, 60, 85]
	 eff1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
	 eff2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
	 print get_probability(eff1, eff2, "SM1")
	#	eff1 = [100, 90, 85, 95]
	#	eff2 = [93, 97, 89, 90]
	# p = [.25,0.63,0.25,0.71,0.28,0.71]
	# comb = [0.71, 0.25, 0.89]
	# get_other_probabilities(comb, p)
if __name__ == '__main__':
    main()
