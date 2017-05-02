import base64
import time
import datetime

# read file into a @table
#
# @file_name: string
# @table: list of lists of strings
def get_table_from_file(file_name, indices):
    with open(file_name, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(",") for element in lines]
    table = base64_decoder(table, indices)
    table = get_timeform_from_stamp(table)
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
            row[i] = base64.b64decode(row[i]).decode("utf-8")
    return table


def base64_coder(table, indices):
    for row in table:
        for i in indices:
            row[i] = base64.b64encode(bytearray(row[i].encode))
    return table


def table_sort(table, sort_key_number, rev_boolean):
    table = sorted(table, key=lambda table: table[sort_key_number], reverse=rev_boolean)
    return table


def get_time_stamp():
    return int(time.time())


def get_timeform_from_stamp(table):
    for row in table:
        row[1] = datetime.datetime.fromtimestamp(int(row[1])).strftime('%Y-%m-%d %H:%M:%S')
    return table




