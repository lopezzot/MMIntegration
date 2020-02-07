# Returns all the combinations
# of size r in an array of size n
def get_combination(arr, n, r):
	# A temporary array to
	# store all combination
	# one by one
	data = [0]*r
	combination = []
	# save all combination
	# using temprary array data[]
	final_combination = combination_rec(arr, data, 0, n - 1, 0, r, [], combination)
	return final_combination
#-----------------------------------------------------------------------------------------------------------------#
def combination_rec(arr, data, start, end, index, r, final_combination, combination):
	# Current combination is ready
	# to be saved, save it
	if (index == r):
		combination = []
		for j in range(r):
			combination.append(data[j])
		final_combination.append(combination)
		return

	# replace index with all
	# possible elements. The
	# condition "end-i+1 >=
	# r-index" makes sure that
	# including one element at
	# index will make a combination
	# with remaining elements at
	# remaining positions
	i = start
	while(i <= end and end - i + 1 >= r - index):
		data[index] = arr[i]
		combination_rec(arr, data, i + 1, end, index + 1, r, final_combination, combination)
		i += 1
	return final_combination
#------------------------------------------------------------------------------------------------------------------#
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
#-------------------------------------------------------------------------------------------------------------------#
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
#-------------------------------------------------------------------------------------------------------------------#
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
	return probability
#-------------------------------------------------------------------------------------------------------------------#
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
	elif chamber_type == "SM1" or chamber_type == "LM1":
		for i in range(10):
			section_efficiency = []
			for j in range(8):
				section_efficiency.append(new_values[i+10*j])
			final_sectors.append(section_efficiency)
	else:
		print "Chamber type not found"
	for sector in final_sectors:
		# getting all the possible combinations for the layers
		section_probability = 0
		# calculating the probability for 4 , 3 , 2 or 1 layer detecting the particle
		for j in range(3):
			combinations = get_combination(sector, 8, 6+j)
			probability = get_section_probability(combinations, 6+j, 8, sector) #4+j, 8
			section_probability = section_probability + probability
		final_probabilities.append(section_probability)
	return final_probabilities
#-------------------------------------------------------------------------------------------------------------------#
def get_dw_probability(type_1, type_2, ch1_IP, ch2_IP, ch1_HO, ch2_HO):
	probability_1 = get_probability(ch1_IP, ch1_HO, type_1)
	probability_2 = get_probability(ch2_IP, ch2_HO, type_2)
	return probability_1 + probability_2
