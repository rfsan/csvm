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

    To transform it into a `.csvm` add the following two sections

    - `[_columns_]` to define the column names
    - `[_data_]` to define the tabular data

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
    false,false,true
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
    # Pink Floyd band members
    [members._table_meta_.reference]
    "https://en.wikipedia.org/wiki/Pink_Floyd#Band_members"
    [members._column_meta_.unique]
    false,false,true
    [members._columns_]
    first_name,last_name,instrument

    [members._data_]
    Syd,Barret,"guitar, vocals"
    David,Gilmour,"guitar, vocals"
    Roger,Waters,"bass, vocals"
    Richard,Wright,"keyboards, vocals"
    Nick,Mason,drums

    [albums._columns_]
    [albums._data_]
    ```


## Read a `.csvm` file 

