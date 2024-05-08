import random

r_random_sequence = [
    0,
    63,
    127
]

g_random_sequence = [
    0,
    42,
    106
]

b_random_sequence = [
    0,
    21,
    85
]

list1 = [2, 1, 1] # 100%
list2 = [2, 1, 0] # 75%
list3 = [2, 0, 0] # 50%
list4 = [1, 1, 1] # 75%
list5 = [1, 1, 0] # 50%
list6 = [1, 0, 0] # 25%
list7 = [0, 0, 0] # 0%
lists = [list1, list2, list3, list4, list5, list6, list7]
final_list = random.choice(lists)
# let's shuffle random the values of the list
final_list = random.sample(final_list, len(final_list))
r = r_random_sequence[final_list[0]]
g = r_random_sequence[final_list[1]]
b = r_random_sequence[final_list[2]]
