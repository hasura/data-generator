def mod_tuples(schema, tuple_list):
    modded_list = []
    for t in tuple_list:
        if len(t) == 2:
            p1, p3 = t
            _p1 = f"{schema}\\.{p1}"
            _p2 = f"^(?!.*_id$).*"
            modded_list.append((_p1, _p2, p3))
        elif len(t) == 3:
            p1, p2, p3 = t
            _p1 = f"{schema}\\.{p1}"
            _p2 = f"^{p2}$"
            modded_list.append((_p1, _p2, p3))
        else:
            raise Exception('Invalid tuple')
    return modded_list
