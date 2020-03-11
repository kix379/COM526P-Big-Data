"""
Dynamic Intemset Counting:
1. Given: M and min_Support
2. 4 different states which an item can be in - dashed_circle, solid_circle, dashed_square, solid_square
3. Initialise single items as dashed_circle
4. Do 1 pass of M transactions, keep a count for each item on how many transactions we have covered,
whenever we finish the entire set, then the item gets solid status
    - after this pass, if the count of an item exceeds min support then convert status to a dashed_square
    - check the immediate super set of each item and check if all subsets of that superset are some form of a square, if so then generate new item with dashed circle status
5. Stop when there are no more dashed items
"""
import itertools


transactions = [[1, 2, 5],
                [2, 4],
                [2, 3],
                [1, 2, 4],
                [1, 3],
                [2, 3],
                [1, 3],
                [1, 2, 3, 5],
                [1, 2, 3],
                [4,5]]
transactions=[ list(map(str,x)) for x in transactions ]
M=5
min_Support=2
unique_items=sorted(list(set(itertools.chain(*transactions))))
print(unique_items)

DC=dict.fromkeys(unique_items,0)
DS={}
SC={}
SS={}
index=0

supersets=[]
supersets.append(dict.fromkeys(unique_items,0))

for i in range(1,len(unique_items)):
    supersets.append(dict.fromkeys([''.join([x,y[-1]]) for x in supersets[i-1] for y in supersets[i-1] if x[:-1]==y[:-1] and x[-1]<y[-1]],0))

print(supersets)

while len(DC)!=0 or len(DS)!=0:
    for i in transactions[index:index+M]:
        for j in list(DC.keys()):
            if set(list(j)).issubset(set(i)):
                DC[j]=DC[j]+1
            supersets[len(j)-1][j]=supersets[len(j)-1][j]+1
        for j in list(DS.keys()):
            if set(list(j)).issubset(set(i)):
                DS[j]=DS[j]+1
            supersets[len(j)-1][j]=supersets[len(j)-1][j]+1

    print(DC,DS)

    for i in DC.copy():
        if DC[i]>=min_Support:
            DS.update({i:DC[i]})
            del DC[i]
            #check immediate supersets of i and check if all the subsets of that superset are some square
            for j in supersets[len(i)]:
                if set(list(i)).issubset(set(j)):
                    if all(((''.join(k) in DS) or (''.join(k) in SS)) for k in list(itertools.combinations(j, len(j)-1))):
                        DC.update({j:0})

    for i in DS.copy():
        if supersets[len(i)-1][i]==len(transactions):
            SS.update({i:DS[i]})
            del DS[i]
    for i in DC.copy():
        if supersets[len(i)-1][i]==len(transactions):
            SC.update({i:DC[i]})
            del DC[i]
    print(SS,SC,DS,DC)
    index=(index+M)%len(transactions)
    print(supersets)

print(SS)
