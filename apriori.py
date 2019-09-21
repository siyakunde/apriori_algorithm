import time
import operator
from itertools import chain, combinations

def powerset(iterable):
	# This function will create and return a powerset of the passed in items
	xs = list(iterable)
	return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

def getL(C, T, min_sup):
	candidateFrequency = {}
	# Scan transaction viz for lower time used to process
	# For each transaction
	for transaction in T:
		# For each candidate
		for candidate in C:
			# If the candidate is a subset of the transaction
			if(candidate.issubset(transaction)):
				# Update candidate frequency value
				if(candidate not in candidateFrequency): 
					candidateFrequency[candidate] = 1
				else: 
					candidateFrequency[candidate] += 1

	numberOfTransactions = len(T)
	L = []
	supportL = {}
	
	# Pruining Operation
	# For each frequent candidate
	for candidate in candidateFrequency:
		# Compute the support
		support = candidateFrequency[candidate]/numberOfTransactions
		# If the support is greater than or equal to the minimum support then add it to L
		if(support >= min_sup):
			L.insert(0,candidate)
			supportL[candidate] = support

	return L, supportL, candidateFrequency

def getC(Lk, k):
	Ck = []
	# For each pair of itemset in L
	for i in range(len(Lk)):
		for j in range(i+1, len(Lk)): 
			# Sort the two itemsets so that the first k-1 items (from 0 to k-2) will be the same, and only the last item will be different
			part_i = list(Lk[i])
			part_i.sort()
			part_i_pre = part_i[:k-2]

			part_j = list(Lk[j])
			part_j.sort()
			part_j_pre = part_j[:k-2]

			# print(part_i, part_j, len(Lk[i].symmetric_difference(Lk[j])), Lk[i].symmetric_difference(Lk[j]))

			# Join Operation
			# If the first k-1 parts are found to be the same, we can join the two sets.
			if part_i_pre == part_j_pre:
				tempC = Lk[i].union(Lk[j])
				tempC = list(tempC)
				tempC = sorted(tempC, key=str.lower)
				# print(tempC)
				tempC = frozenset(tempC)
				Ck.append(tempC)
			# print('-------------------------------------------------------------------------------------------')
	return Ck

def getR(L, supportL, candidateFrequency, min_conf):
	# Creation of variables to store rules, confidence
	rules = []
	confRules = {}

	for i in range(0, len(L)):
		frequentItemsetList = L[i]
		# For each of the frequent itemsets
		for frequentSet in frequentItemsetList:	
			itemList = []
			for item in frequentSet:
				itemList.insert(0,item)

			subsets = powerset(itemList)
			subsets = [frozenset(aset) for aset in subsets]

			for aset in subsets:
				if(aset is not itemList and len(aset) > 0):
					if(len(frequentSet) is not 0 and len(aset) is not 0 and len(frequentSet-aset) is not 0):
						confidence = candidateFrequency[frequentSet]/candidateFrequency[frequentSet-aset]
						if (confidence) >= min_conf:
							newrule = str(list(frequentSet-aset)) + ' ' + str(candidateFrequency[frequentSet-aset]) + ' ->' + str(list(aset)) + ' ' + str(candidateFrequency[frequentSet]) + ' conf:<' + str(confidence) + '>'
							# print ('RULE----------------------------------------'+newrule)
							rules.insert(0, newrule)
							confRules[newrule] = confidence

	return rules, confRules

def main(dataset, min_sup, min_conf):
	start_time = time.time()

	# This round conputes C and L for k = 1
	T = dataset.apply(frozenset, axis=1)
	C = []
	# Scan database once and create a set of unique 1-itemsets
	for index, row in dataset.iterrows():
		for item in row:
			if [item] not in C:
				C.append([item])
	C.sort()
	C = list(map(frozenset, C))
	L, supportL, candidateFrequency = getL(C, T, min_sup)
	L = [L]
	# print(T)
	# print(C)
	# print(L)
	# print(supportL)

	# Set k to 2 since we have computed C1 and L1 previously and next we will compute next level itemsets starting with C2 and L2
	k = 2
	# While the set is not empty
	while (len(L[k-2]) > 0): 
		# Candidate generation step
		Ck = getC(L[k-2], k) 
		Lk, supportLk, candidateFrequencyk = getL(Ck, T, min_sup)
		L.append(Lk)
		supportL.update(supportLk)
		candidateFrequency.update(candidateFrequencyk)
		k += 1

	R, confidenceR = getR(L, supportL, candidateFrequency, min_conf)
	confidenceR = sorted(confidenceR.items(), key=operator.itemgetter(1), reverse=True)

	end_time = time.time()

	return start_time, end_time, C, L, supportL, R, confidenceR