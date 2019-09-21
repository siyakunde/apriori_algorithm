----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
Apriori Algorithm and Rule generation
----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
TO RUN:
Copy the folder apriori_algorithm. 
Type cd apriori_algorithm to enter the forlder.
To run the program type a command as follows with dataset, support, confidence:
python3 main.py vote.arff 0.55 0.9
The output will be in the file apriori_algorithm_experiment_data.csv
----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
PROGRAM DESCRIPTION:
For the Apriori Algorithm the following functions are used:

1) getL(C, T, min_sup)
This function creates the candidate list by processing the data by considering one transaction at a time.
For each transaction, and for each candidate, if the candidate is a subset of the transaction, it's added to the list and frequency is updated.
Once all candidates are available, the ones with support greater than or equal to the minimum support are added to L. Finally L is returned.

2) getC(Lk, k)
For each pair of itemset in L, compare them in a item-sorted order.
If the first k-1 items are the same, and only the last item is different, then perform the join and add to C. Finally C is returned.

3) getR(L, supportL, candidateFrequency, min_conf)
For each of the frequent itemset in L, find subsets and generate rules by filtering with the minimum confidence provided.
Finally rules and their confidence values are returned.

4) main(dataset, min_sup, min_conf)
This is simple the invoker function. First the transaction set is built, C and subsequent L are initialized, and then we repeatedly call getC and getL until L is empty.
----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------