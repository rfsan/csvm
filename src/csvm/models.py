class Table:
    def __init__(
        self, name=None, columns=None, data=None, meta=None, column_meta=None
    ) -> None:
        self.name = name
        self.columns = columns
        self.data = data
        self.meta = meta
        self.column_meta = column_meta

    @staticmethod
    def from_dict(d):
        name = d.get("_name_")
        columns = d.get("_columns_")
        data = d.get("_data_")
        meta = d.get("_meta_")
        column_meta = d.get("_column_meta_")
        return Table(name, columns, data, meta, column_meta)


class TableCollection:
    def __init__(self, tables: list[Table]) -> None:
        self._tables_map = {t.name: t for t in tables}
        self.tables = list(self._tables_map.keys())

    def __getitem__(self, index):
        return self._tables_map[index]

    @staticmethod
    def from_list(l):
        return TableCollection([Table.from_dict(d) for d in l])
