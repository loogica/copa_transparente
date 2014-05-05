# coding: utf-8

def extract_table_name(meta_name):
    values = meta_name.split('_')
    return values[0], meta_name.replace(values[0], '')


def fix_line(line, max_rows):
    ret = []
    for i, data in enumerate(line):
        if i >= max_rows:
            break
        if data.endswith('"'):
            new_data = line.pop(i + 1)
            data = "".join([data, new_data])
        ret.append(data)
    return ret

