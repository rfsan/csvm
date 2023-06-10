import csv
import json
from collections import defaultdict
from itertools import groupby
from csvm.models import Table, TableCollection


class NestedDefaultDict:
    nested_defaultdict = lambda: defaultdict(NestedDefaultDict.nested_defaultdict)

    def __init__(self) -> None:
        self.dict = NestedDefaultDict.nested_defaultdict()

    def set(self, keys, value):
        self.set_nested_value(self.dict, keys, value)

    @staticmethod
    def set_nested_value(default_dict, keys, value):
        key = keys[0]
        if len(keys) == 1:
            default_dict[key] = value
        else:
            NestedDefaultDict.set_nested_value(default_dict[key], keys[1:], value)


def read_csvm_line_by_line(filename):
    with open(filename) as csvm_file:
        reader = csv.reader(csvm_file, delimiter=",")
        for line in reader:
            if not line or line[0].startswith("#"):
                continue
            yield line
        yield


def read_csvm_as_list(filename: str):
    # Read the data as a key: value pairs
    csvm_reader = read_csvm_line_by_line(filename)
    data = defaultdict(list)
    loading_table = None
    while True:
        line = next(csvm_reader)
        if not line:
            break
        elem0 = line[0]
        if elem0.startswith("["):
            loading_table = None
            key = elem0.rstrip()[1:-1]
            if "_data_" in elem0:
                loading_table = key
            else:
                value = next(csvm_reader)
                if not value:
                    raise
                data[key] = value
        elif loading_table:
            data[loading_table].append(line)

    # Group the data by table names
    multiple_tables = "_data_" not in data.keys()
    tables_grouped = []
    if multiple_tables:
        for k, group in groupby(data, lambda x: x.split(".")[0]):
            table_obj = {}
            table_obj["_name_"] = k
            for g in group:
                prop_name = g.replace(f"{k}.", "")
                table_obj[prop_name] = data[g]
            tables_grouped.append(table_obj)
    else:
        tables_grouped.append(data)

    # For each group transform data into a tree structure
    csvm_data = []
    for table in tables_grouped:
        table_obj = NestedDefaultDict()
        for prop, v in table.items():
            nested_route = prop.split(".")
            if isinstance(v, list) and len(v) == 1:
                v = v[0]
            if not nested_route[0].startswith("_"):
                table_obj.set(["_table_meta_"] + nested_route, v)
            elif nested_route[0] == "_column_meta_":
                columns = [v for k, v in table.items() if "_columns_" in k][0]
                for col, col_v in zip(columns, v):
                    keys = [nested_route[0]] + [col] + nested_route[1:]
                    if col_v:
                        table_obj.set(keys, col_v)
            else:
                table_obj.set(nested_route, v)

        csvm_data.append(table_obj.dict)

    csvm_data_with_regular_dicts = json.loads(json.dumps(csvm_data))
    return csvm_data_with_regular_dicts


def read_csvm(filename: str):
    csv_data = read_csvm_as_list(filename)
    if len(csv_data) > 1:
        return TableCollection.from_list(csv_data)
    else:
        return Table.from_dict(csv_data[0])
