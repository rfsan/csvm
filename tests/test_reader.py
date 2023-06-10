import csvm
import pytest

MUTIPLE_TABLES_CSVM = """
[first_name._column_meta_.category_codes]
,third_name
[first_name._columns_]
id,valor
[first_name._data_]
1,0
2,0
3,1

[second_name._columns_]
nombre,edad
[second_name._data_]
adam,40
karl,30

[third_name.url]
www.example.com
# The following line has white spaces after the square bracket
[third_name._columns_]      
code,category
[third_name._data_]
0,RED
1,BLUE
"""

MULTIPLE_TABLES = [
    {
        "_name_": "first_name",
        "_column_meta_": {
            "valor": {
                "category_codes": "third_name",
            }
        },
        "_columns_": ["id", "valor"],
        "_data_": [["1", "0"], ["2", "0"], ["3", "1"]],
    },
    {
        "_name_": "second_name",
        "_columns_": ["nombre", "edad"],
        "_data_": [["adam", "40"], ["karl", "30"]],
    },
    {
        "_name_": "third_name",
        "_table_meta_": {"url": "www.example.com"},
        "_columns_": ["code", "category"],
        "_data_": [["0", "RED"], ["1", "BLUE"]],
    },
]

ONE_TABLE_CSVM = """
[url]
www.example.com
[_column_meta_.data_type]
int,category
[_columns_]
code,category
[_data_]
0,BOGOTA
1,CALI
"""

ONE_TABLE = [
    {
        "_column_meta_": {
            "code": {"data_type": "int"},
            "category": {"data_type": "category"},
        },
        "_columns_": ["code", "category"],
        "_data_": [["0", "BOGOTA"], ["1", "CALI"]],
        "_table_meta_": {"url": "www.example.com"},
    }
]

CONTENT = {
    "multiple_tables": {"csvm": MUTIPLE_TABLES_CSVM, "obj": MULTIPLE_TABLES},
    "one_table": {"csvm": ONE_TABLE_CSVM, "obj": ONE_TABLE},
}


@pytest.fixture(scope="session", params=["multiple_tables", "one_table"])
def csvm_file(request, tmp_path_factory):
    csvm_case = request.param
    fn = tmp_path_factory.mktemp("data") / f"{csvm_case}.csvm"
    fn.write_text(CONTENT[csvm_case]["csvm"].lstrip("\n"))
    return fn


def test_read_csvm(csvm_file):
    expected = CONTENT[csvm_file.name.replace(".csvm", "")]["obj"]
    result = csvm.read_csvm_as_list(str(csvm_file))
    assert expected == result
