import base64


# read file into a @table
#
# @file_name: string
# @table: list of lists of strings
def get_table_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(",") for element in lines]
    return table


# write a @table into a file
#
# @file_name: string
# @table: list of lists of strings
def write_table_to_file(file_name, table):
    with open(file_name, "w") as file:
        for record in table:
            row = ','.join(record)
            file.write(row + "\n")


def base64_decoder(table, indices):
    for row in table:
        for i in indices:
            row[i] = base64.b64decode(row[i])
    return table


def base64_coder(table, indices):
    for row in table:
        for i in indices:
            row[i] = base64.b64encode(row[i])
    return table


def table_sort(table, sort_key_number, rev_boolean):
    table = sorted(table, key=lambda table: table[sort_key_number], reverse=rev_boolean)
    return table

