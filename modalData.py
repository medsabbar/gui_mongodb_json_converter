from collections import defaultdict
def print_fields(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            print_fields(value)
    elif isinstance(obj, list):
        for item in obj:
            print_fields(item)


def flatten_object(obj, parent_key='', myMap={}, dictionary=[], labe='labeleFr'):
    mongoObjects = {'$oid', '$date', '$numberInt', '$numberDouble',
                    '$numberLong', '$numberDecimal', '$timestamp'}

    flattened = {}

    stack = [(parent_key, obj)]
    while stack:
        key, value = stack.pop()

        if isinstance(value, dict):
            for k, v in value.items():
                stack.append((f"{key}.{k}" if key else k, v))
        else:
            if key in mongoObjects:
                flattened[parent_key] = value
            else:
                if isinstance(value, list):
                    flattened[key] = [
                        str(v) if isinstance(v, dict) else myMap.get(
                            v, next((d[labe] for d in dictionary if d['key'] == v), v))
                        for v in value
                    ]
                else:
                    flattened[key] = myMap.get(value, next(
                        (d[labe] for d in dictionary if d['key'] == value), value))

    return flattened


def flatten_object_no_translation(obj, parent_ke=''):
    mongoObjects = ['$oid', '$date', '$numberInt', '$numberDouble',
                    '$numberLong', '$numberDecimal', '$timestamp']

    flattened = {}
    stack = [(parent_ke, obj)]
    while stack:
        key, value = stack.pop()

        if isinstance(value, dict):
            for k, v in value.items():
                stack.append((f"{key}.{k}" if key else k, v))
        else:
            if key in mongoObjects:
                parent_ke = parent_ke[:-1]
                flattened[parent_ke] = value
            else:
                if isinstance(value, list):
                    for i, v in enumerate(value):
                        if isinstance(v, dict):
                            stack.append((f"{key}.{i}", v))
                        else:
                            flattened[f"{key}.{i}"] = v
                else:
                    flattened[key] = value

    return flattened

# export the pint_fields function
__all__ = ['print_fields', 'flatten_object', 'flatten_object_no_translation']
