# Delete the element at index `i` from the
# unordered lists in the tuple `lists`.
def del_unordered(lists, i):
    n = len(lists[0])
    last = n - 1
    for v in lists:
        assert(len(v) == n)  # All lists must be the same length.
        v[i] = v[last]
        del v[last]

def set_str_char(str, index, char):
    return str[: index] + char + str[index + 1 :]