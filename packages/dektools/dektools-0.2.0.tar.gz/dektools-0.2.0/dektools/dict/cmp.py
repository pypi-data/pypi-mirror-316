from .simple import is_dict


def diff_dict_weight(a, b):
    weight = 0
    aa, bb = set(a), set(b)
    same = aa & bb
    for k in same:
        ax, bx = a[k], b[k]
        if is_dict(ax):
            if is_dict(bx):
                weight += diff_dict_weight(ax, bx)
            else:
                weight += 1 + diff_dict_weight(ax, {})
        elif ax != bx:
            weight += 1
    for k in aa - same:
        ax = a[k]
        weight += 1
        if is_dict(ax):
            weight += diff_dict_weight(ax, {})
    weight += len(bb) - len(same)
    return weight
