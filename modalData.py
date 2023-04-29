def print_fields(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            print(key)
            print_fields(value)
    elif isinstance(obj, list):
        for item in obj:
            print_fields(item)


def flatten_object(obj, parent_key='', myMap={}, dictionary=[], labe='labeleFr'):
    mongoObjects = ['$oid', '$date', '$numberInt', '$numberDouble',
                    '$numberLong', '$numberDecimal', '$timestamp']
    if parent_key != '':
        parent_key += '.'
    flattened = {}
    print('obj')
    print(obj)
    for key, value in obj.items():
        if isinstance(value, dict):
            flattened.update(flatten_object(
                value, parent_key + key, myMap, dictionary))
        else:
            if key in mongoObjects:
                parent_key = parent_key[:-1]
                flattened[parent_key] = value
            else:
                if isinstance(value, list):
                    for i in range(len(value)):
                        if isinstance(value[i], dict):
                            flattened.update(flatten_object(
                                value[i], parent_key + key + '.' + str(i), myMap, dictionary))
                        else:
                            flattened[parent_key + key +
                                      '.' + str(i)] = value[i]
                elif value in myMap:
                    flattened[parent_key + key] = myMap[value]
                else:
                    for j in range(len(dictionary)):
                        if value == dictionary[j]['key']:
                            flattened[parent_key + key] = dictionary[j][labe]
                            myMap[value] = dictionary[j][labe]
                            break
                        elif j == len(dictionary) - 1:
                            flattened[parent_key + key] = value

    print('flattened')
    print(flattened)
    return flattened


def flatten_object_no_translation(obj, parent_ke=''):
    mongoObjects = ['$oid', '$date', '$numberInt', '$numberDouble',
                    '$numberLong', '$numberDecimal', '$timestamp']
    if parent_ke != '':
        parent_ke += '.'
    flattened = {}
    for key, value in obj.items():
        if isinstance(value, dict):
            flattened.update(flatten_object_no_translation(
                value, parent_ke + key))
        else:
            if key in mongoObjects:
                parent_ke = parent_ke[:-1]
                flattened[parent_ke] = value
            else:
                if isinstance(value, list):
                    for i in range(len(value)):
                        if isinstance(value[i], dict):
                            flattened.update(flatten_object_no_translation(
                                value[i], parent_ke + key + '.' + str(i)))
                        else:
                            flattened[parent_ke + key +
                                      '.' + str(i)] = value[i]
                else:
                    flattened[parent_ke + key] = value
    return flattened


# export the pint_fields function
__all__ = ['print_fields', 'flatten_object', 'flatten_object_no_translation']
