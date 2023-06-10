# CSVM

CSVM is a file format that allows you to save multiple tables, add comments, and include metadata for both tables and columns

## File format explanation

1. Transform a `.csv` into a `.csvm`

    We start with a `.csv`

    ```csv
    first_name,last_name,instrument
    Syd,Barret,"guitar, vocals"
    David,Gilmour,"guitar, vocals"
    Roger,Waters,"bass, vocals"
    Richard,Wright,"keyboards, vocals"
    Nick,Mason,drums
    ```

    To transform it into a `.csvm` you add **table attributes**. Tha available table attributes are:
    
    - `[_columns_]` to define the column names
    - `[_data_]` to define the tabular data
    - `[_table_meta_.any_key.with_nested_keys]` to add table metadata
    - `[_columns_meta_.any_key.with_nested_keys]` to add column metadata. 
    
    
    For now we add the attributes `_columns_` and `_data`
    
    ```
    [_columns_]
    first_name,last_name,instrument
    [_data_]
    Syd,Barret,"guitar, vocals"
    David,Gilmour,"guitar, vocals"
    Roger,Waters,"bass, vocals"
    Richard,Wright,"keyboards, vocals"
    Nick,Mason,drums
    ```

2. Add comments and blank lines

    Every line that starts with a `#` is ignored when parsing the file

    ```
    # Pink Floyd band members

    [_columns_]
    first_name,last_name,instrument

    [_data_]
    Syd,Barret,"guitar, vocals"
    David,Gilmour,"guitar, vocals"
    Roger,Waters,"bass, vocals"
    Richard,Wright,"keyboards, vocals"
    Nick,Mason,drums
    ```

3. Add table metadata

    ```
    # Pink Floyd band members
    
    [_table_meta_.reference]
    "https://en.wikipedia.org/wiki/Pink_Floyd#Band_members"
    
    [_columns_]
    first_name,last_name,instrument

    [_data_]
    Syd,Barret,"guitar, vocals"
    David,Gilmour,"guitar, vocals"
    Roger,Waters,"bass, vocals"
    Richard,Wright,"keyboards, vocals"
    Nick,Mason,drums
    ```

4. Add column metadata

    ```
    # Pink Floyd band members
    
    [_table_meta_.reference]
    "https://en.wikipedia.org/wiki/Pink_Floyd#Band_members"
    
    [_column_meta_.unique]
    true,true,false
    
    [_columns_]
    first_name,last_name,instrument

    [_data_]
    Syd,Barret,"guitar, vocals"
    David,Gilmour,"guitar, vocals"
    Roger,Waters,"bass, vocals"
    Richard,Wright,"keyboards, vocals"
    Nick,Mason,drums
    ```

5. Save more than one table

    If you want to save more than one table you must use a **namespace** for each table. 

    ```
    # Table 1 - Pink Floyd band members
    
    [members._table_meta_.reference]
    "https://en.wikipedia.org/wiki/Pink_Floyd#Band_members"
    
    [members._column_meta_.unique]
    true,true,false
    
    [members._columns_]
    first_name,last_name,instrument

    [members._data_]
    Syd,Barret,"guitar, vocals"
    David,Gilmour,"guitar, vocals"
    Roger,Waters,"bass, vocals"
    Richard,Wright,"keyboards, vocals"
    Nick,Mason,drums
    
    # Table 2 - Pink Floyd albums

    [albums._columns_]
    name,year
    [albums._data_]
    Animals,1997
    "The Dark Side of the Moon",1973
    ```


## Read a `.csvm` file 

Installation `pip install csvm`

```python
import csvm

# Load TableCollection (if multiple tables) or Table (if one table)
tc = csvm.read_csvm("pink_floyd.csvm") 
print(tc.tables)
members = tc['members'] # get Table
# Access Table attributes if exist (i.e. Table.columns, Table.column_meta, Table.table_meta, Table.data, Table.name)
print(members.data) 
```
