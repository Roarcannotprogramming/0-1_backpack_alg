# coding=UTF-8

import random

obj_cnt = 10
bp_room = 100
weight_list = [50, 4 ,10 ,34, 27, 33, 77, 43, 61, 48]
value_list = [37, 14, 12, 20, 33, 27, 49, 52, 61, 50]

# Enum
def bpEnum():

    max_num = 0;
    bin_enum = 0;
    for i in range(2 ** obj_cnt):
        j = i
        w_sum = 0
        v_sum = 0
        for k in range(obj_cnt):
            if(j & 1):
                w_sum += weight_list[k]
                v_sum += value_list[k]
            j = (j >> 1)
        if w_sum <= bp_room and v_sum > max_num:
            max_num = v_sum
            bin_enum = i
    return max_num, bin(bin_enum)

print("穷举法: " + str(bpEnum()[0]))



# DP
def bpFillSumList():
    sum_list = [ [0 for j in range(bp_room+1)] for i in range(obj_cnt) ]
    if(weight_list[0]<=bp_room):
        for j in range(weight_list[0], bp_room+1):
            sum_list[0][j] = value_list[0]

    for j in range(bp_room+1):
        for i in range(obj_cnt):
            if(j-weight_list[i] < 0):
                sum_list[i][j] = sum_list[i-1][j]
            else:
                sum_list[i][j] =\
                    max(sum_list[i-1][j],\
                        sum_list[i-1][j-weight_list[i]] + value_list[i])

    return sum_list[obj_cnt-1][bp_room]

print("动态规划: " + str(bpFillSumList()))



# NoteBook
def bpNoteBook(i, j):
    if j < 0:
        return 0
    if i == 0:
        if j < weight_list[0]:
            return 0
        return value_list[0]
    if(j - weight_list[i] < 0):
        return bpNoteBook(i-1, j)
    return max(bpNoteBook(i-1, j), bpNoteBook(i-1, j-weight_list[i])\
               + value_list[i])

print("自顶向下的备忘录法: " + str(bpNoteBook(obj_cnt-1, bp_room)))



# TraceBack
max_value =0
per_val_list = per_val_list = [(float(value_list[i])/weight_list[i],i) for i in range(obj_cnt)]
per_val_list.sort(reverse=True)
max_for_depth = [0 for i in range(obj_cnt + 1)]
for i in range(obj_cnt):
    backpack_room = bp_room
    for j in range(obj_cnt):
        if per_val_list[j][1] >= i:
            if backpack_room < weight_list[per_val_list[j][1]]:
                max_for_depth[i] += per_val_list[j][0] * backpack_room
                break
            else:
                max_for_depth[i] += value_list[per_val_list[j][1]]
                backpack_room -= weight_list[per_val_list[j][1]]

def bpBackTrace(depth, weight, value):
    if depth == obj_cnt:
        global max_value
        max_value = max(max_value, value)
        return
    bpBackTrace(depth +1, weight, value)
    new_w = weight + weight_list[depth]
    if new_w <= bp_room and value + max_for_depth[depth] > max_value:
        bpBackTrace(depth + 1, new_w, value + value_list[depth])

bpBackTrace(0, 0, 0)
print("回溯法: " + str(max_value))



# BranchBound
def bpBranchBound():
    node_num = 2 ** (obj_cnt + 1) - 1
    priority_queue = []
    priority_queue.append((max_for_depth[0], 0, 0, bp_room))  # (预计最大值 目前最大值 深度 目前容量)
    while priority_queue:
        current = max(priority_queue)
        if current[2] == obj_cnt:
            return current[0]
        priority_queue.remove(current)
        priority_queue.append((max_for_depth[current[2]+1] + current[1], current[1], current[2]+1, current[3]))
        if current[3] > weight_list[current[2]]:
            priority_queue.append((max_for_depth[current[2]+1] + value_list[current[2]] + current[1], value_list[current[2]] + current[1], current[2] + 1, current[3] - weight_list[current[2]]))

print("分支限界法: " + str(bpBranchBound()))

def bpMonteCarlo():
    max_num = 0
    mod = 2 ** obj_cnt
    for i in range(10000):
        rand = random.randint(0, mod-1)
        w_sum = 0
        v_sum = 0
        for j in range(obj_cnt):
            if(rand & 1):
                w_sum += weight_list[j]
                v_sum += value_list[j]
            rand = (rand >> 1)
        if w_sum <= bp_room and v_sum > max_num:
            max_num = v_sum
    return max_num

print("蒙特卡洛法: " + str(bpMonteCarlo()))













