# python3
import re
import argparse

LEVEL_0_TAGS = set(['INDI', 'FAM', 'NOTE', 'TRLR', 'HEAD'])
LEVEL_1_TAGS = set(['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'])
LEVEL_2_TAGS = set(['DATE'])
EXCEPTIONAL_TAGS = set(['FAM', 'INDI'])


def print_line(line):
    items = re.split(r'[ ]', line.strip(), 2)
    items_to_print = []
    if len(items) < 3:
        last_item = None
    else:
        last_item = items[2].strip()
    if items[1] not in LEVEL_0_TAGS | LEVEL_1_TAGS | LEVEL_2_TAGS:
        if last_item and items[2].strip() in EXCEPTIONAL_TAGS:
            items_to_print += [items[0], items[2].strip(), 'Y']
            last_item = items[1]
        else:
            items_to_print += [items[0], items[2].strip(), 'N']
    else:
        items_to_print += items[:2]
        if items[1] in LEVEL_0_TAGS:
            if items[0] == '0':
                items_to_print += ['Y']
            else:
                items_to_print += ['N']
        elif items[1] in LEVEL_1_TAGS:
            if items[0] == '1':
                items_to_print += ['Y']
            else:
                items_to_print += ['N']
        elif items[1] in LEVEL_2_TAGS:
            if items[0] == '2':
                items_to_print += ['Y']
            else:
                items_to_print += ['N']
    if last_item:
        items_to_print.append(last_item)
    print('<-- '+'|'.join(items_to_print))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add GEDCOM file')
    parser.add_argument('-f', action="store", dest='filename', required=True)
    args = parser.parse_args()
    filename = args.filename
    with open(filename, 'r') as f:
        for line in f.readlines():
            print('--> ' + line.strip())
            print_line(line)
