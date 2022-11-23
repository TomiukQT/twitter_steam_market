
@staticmethod
def get_nested(json, *args):
    res = json
    for k in args:
        res = res[k]
    return res
