from main_app import list_to_float
from locale import atof, setlocale, LC_NUMERIC

def list_to_float2(grade_list):
    return_list = []
    for item in grade_list:
        temp_item = item
        try:
            temp_item = float(atof(item))
        except (ValueError, TypeError):
            pass
        return_list.append(temp_item)
    return return_list


if __name__ == '__main__':
    setlocale(LC_NUMERIC, 'de_DE')

    l = ['x', '2', '2.3', '7,7']

    print(l)

    l2 = list_to_float2(l)

    print(l2)
