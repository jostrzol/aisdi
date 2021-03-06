def quicksort(lst: list, start=0, end=None, copy=True):
    if copy:
        lst = list(lst)

    if end is None:
        end = len(lst)

    if end - start <= 1:
        return lst

    pivot = lst[end-1]
    i = start
    for j in range(start, end - 1):
        if lst[j] < pivot:
            tmp = lst[i]
            lst[i] = lst[j]
            lst[j] = tmp
            i += 1

    lst[end-1] = lst[i]
    lst[i] = pivot
    quicksort(lst, start=start, end=i, copy=False)
    quicksort(lst, start=i+1, end=end, copy=False)
    return lst


def bubblesort(lst: list, copy=True):
    if copy:
        lst = list(lst)

    # dla n-elementowej listy algorytm
    # obróci się (n-1) razy
    for i in range(len(lst), 1, -1):
        for j in range(i-1):
            if lst[j] > lst[j+1]:
                tmp = lst[j]
                lst[j] = lst[j+1]
                lst[j+1] = tmp
    return lst


def mergesort(lst: list, copy=True):
    if copy:
        lst = list(lst)
    if len(lst) > 1:
        mid = len(lst)//2
        L = lst[:mid]
        R = lst[mid:]
        mergesort(L, False)
        mergesort(R, False)

        L_counter = R_counter = counter = 0

        # dopóki w lewej i prawej
        # połówce są jakieś elementy
        while L_counter < len(L) and R_counter < len(R):
            if L[L_counter] < R[R_counter]:
                lst[counter] = L[L_counter]
                L_counter += 1
            else:
                lst[counter] = R[R_counter]
                R_counter += 1
            counter += 1

        # gdy jedna z połówek jest pusta,
        # przepisz zawartość drugiej do
        # sortowanej listy
        while L_counter < len(L):
            lst[counter] = L[L_counter]
            L_counter += 1
            counter += 1
        while R_counter < len(R):
            lst[counter] = R[R_counter]
            R_counter += 1
            counter += 1

    return lst


def countsort_char(lst: list, copy=True):
    if copy:
        lst = list(lst)

    if len(lst) <= 1:
        return lst

    size = len(lst)

    lst_min = ord(min(lst))
    lst_max = ord(max(lst))

    # tworzymy listę zawierającą liczbę wystąpień
    # danej liczby w zakresie sortowanej tablicy
    count = [0] * len(range(lst_min, lst_max+1))
    for i in range(0, size):
        count[ord(lst[i])-lst_min] += 1

    # zastępujemy liczby w sortowanej tablicy
    # korzystając z listy zawierającej liczbę
    # wystąpień poszczególnych liczb
    count_i = count_v = 0
    for elem in count:
        for i in range(elem):
            lst[count_i] = chr(lst_min + count_v)
            count_i += 1
        count_v += 1

    return lst


def countsort_int(lst: list, copy=True):
    if copy:
        lst = list(lst)

    if len(lst) <= 1:
        return lst

    size = len(lst)

    # analogicznie do countsort_char,
    # tylko na liczbach całkowitych
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
