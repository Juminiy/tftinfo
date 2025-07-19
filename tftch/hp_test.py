from heapq import heapify,heappush,heappop

# ls=[1,9,10,28,0,4,5,2]
# heapify(ls)
# print(ls)
# while len(ls) > 0:
#     minval=heappop(ls)
#     print(minval)

ls=[]
for i in range(10,-1,-1):
    heappush(ls, i)

print(ls)

#       0          
#     1     5
#   4  2   9  6 
# 10 7 8 3