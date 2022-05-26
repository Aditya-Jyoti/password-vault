from typing import List

def convert_dict_to_list(data: dict) -> List[List[str]]:
    main_list = [["S.NO", "WEBSITE", "USERNAME", "PASSWORD"]]

    for idx, entry in enumerate(data, start=1):
        sub_list = []
        sub_key = list(data[entry].keys())[0]
        
        sub_list.append(str(idx))
        sub_list.append(entry)
        sub_list.append(data[entry][sub_key])
        sub_list.append(sub_key)
        
        main_list.append(sub_list)

    return main_list


def printer(data: dict) -> int:
    table = convert_dict_to_list(data)

    width = [max([len(x[i]) for x in table]) for i in range(len(table[0]))]
    header = table.pop(0)
    
    for i in width:
        print("+-" + "-".center(i, "-"), end = "-+")
    print()
    
    for i, elem in enumerate(header):
        print("| " + elem.center(width[i], " "), end = " |")
    print()
    
    for i in width:
        print("+-" + "-".center(i, "-"), end = "-+")
    print()

    for row in table:
        for i, elem in enumerate(row):
            print("| " + elem.center(width[i], " "), end = " |")
        print()

    for i in width:
        print("+-" + "-".center(i, "-"), end = "-+")
    print()

    return len(width)
