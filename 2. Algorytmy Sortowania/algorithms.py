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
    for i in range(len(lst), 0, -1):
        for j in range(i-1):
            if lst[j] > lst[j+1]:
                tmp = lst[j]
                lst[j] = lst[j+1]
                lst[j+1] = tmp
    return lst
