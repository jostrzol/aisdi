def quicksort(lst: list):
    if len(lst) <= 1:
        return lst
    pivot = lst[-1]
    i = 0
    for j, el in enumerate(lst[:-1]):
        if el < pivot:
            tmp = lst[i]
            lst[i] = el
            lst[j] = tmp
            i += 1
    lst[-1] = lst[i]
    lst[i] = pivot
    return [*quicksort(lst[:i]), pivot, *quicksort(lst[i+1:])]


def bubblesort(lst: list):
    for i in range(len(lst), 1, -1):
        for j in range(i-1):
            if lst[j] > lst[j+1]:
                tmp = lst[j]
                lst[j] = lst[j+1]
                lst[j+1] = tmp
    return lst


def mergesort(lst: list):
    if len(lst) > 1:
        mid = len(lst)//2
        L = lst[:mid]
        R = lst[mid:]
        mergesort(L)
        mergesort(R)

        L_counter = R_counter = counter = 0
        while L_counter < len(L) and R_counter < len(R):
            if L[L_counter] < R[R_counter]:
                lst[counter] = L[L_counter]
                L_counter += 1
            else:
                lst[counter] = R[R_counter]
                R_counter += 1
            counter += 1

        while L_counter < len(L):
            lst[counter] = L[L_counter]
            L_counter += 1
            counter += 1
        while R_counter < len(R):
            lst[counter] = R[R_counter]
            R_counter += 1
            counter += 1

    return lst


def countsort(lst: list):
    size = len(lst)
    lst_min = min(lst)
    lst_max = max(lst)

    count = [0] * len(range(lst_min, lst_max+1))
    for i in range(0, size):
        count[lst[i]-lst_min] += 1

    count_i = count_v = 0
    for elem in count:
        for i in range(elem):
            lst[count_i] = lst_min + count_v
            count_i += 1
        count_v += 1

    return lst
