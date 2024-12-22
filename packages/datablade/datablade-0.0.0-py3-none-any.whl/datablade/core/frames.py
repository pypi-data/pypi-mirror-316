import pandas as pd 
import pyarrow as pa
import numpy as np 

from .messages import print_verbose
from .strings  import sql_quotename

def try_cast_string_columns_to_numeric(df: pd.DataFrame=None, convert_partial: bool=False, verbose: bool=False) -> pd.DataFrame|None:
    """
    Attempt to cast DataFrame string columns to numeric values where possible.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to process.
        convert_partial (bool): If True, columns with some values convertible to numeric types
                                will be converted to numeric types with NaNs where conversion failed.
                                If False, only columns where all values can be converted will be converted.
    
    Returns:
        pd.DataFrame: DataFrame with string columns converted to numeric types where possible.
    """
    if df is None:
        print_verbose("No DataFrame provided; exiting try_cast_string_columns_to_numeric.", verbose)
        exit # Exit the function if no DataFrame is provided

    for col in df.columns:
        if df[col].dtype == 'object':
            converted = pd.to_numeric(df[col], errors='coerce')
            has_nan = converted.isnull().any()
            if not has_nan:
                df[col] = converted
                print_verbose(f"Column '{col}' successfully converted to numeric.", verbose)
            else:
                if convert_partial:
                    df[col] = converted
                    print_verbose(f"Column '{col}' partially converted to numeric with NaNs where conversion failed.", verbose)
                else:
                    print_verbose(f"Column '{col}' could not be fully converted to numeric; leaving as is.", verbose)
    return df

def clean_dataframe_columns(df: pd.DataFrame=None, verbose: bool=False) -> pd.DataFrame|None:
    """
    Clean the DataFrame columns by:
    - Flattening MultiIndex columns
    - Converting non-string column names to strings
    - Removing duplicate columns, keeping the first occurrence

    Parameters:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    if df is None:
        print_verbose("No DataFrame provided; exiting clean_dataframe_columns.", verbose)
        exit 
    # Step 1: Flatten MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]
        print_verbose("Flattened MultiIndex columns.", verbose)

    # Step 2: Convert non-string column names to strings
    df.columns = df.columns.map(str)
    print_verbose("Converted column names to strings.", verbose)

    # Step 3: Remove duplicate columns, keeping the first occurrence
    duplicates = df.columns.duplicated()
    if duplicates.any():
        duplicate_cols = df.columns[duplicates]
        print_verbose(f"Duplicate columns found: {list(duplicate_cols)}", verbose)
        df = df.loc[:, ~duplicates]
        print_verbose("Removed duplicate columns, keeping the first occurrence.", verbose)

    return df

def generate_parquet_schema(df: pd.DataFrame=None, verbose: bool=False) -> pa.Schema|None:
    """
    Generate a PyArrow Schema from a pandas DataFrame.
    Parameters:
        df (pandas.DataFrame): The DataFrame to generate the schema from.
    Returns:
        pyarrow.Schema: The PyArrow Schema object.
    """
    if df is None:
        print_verbose("No DataFrame provided; exiting generate_parquet_schema.", verbose)
        exit 
    
    fields = []
    for column in df.columns:
        col_data = df[column]
        col_name = column
        dtype = col_data.dtype

        # Determine if the column contains any nulls
        nullable = col_data.isnull().any()

        # Map pandas dtype to PyArrow type
        pa_type = None

        if pd.api.types.is_integer_dtype(dtype):
            # Check the range to determine the smallest integer type
            min_value = col_data.min()
            max_value = col_data.max()
            if min_value >= np.iinfo(np.int8).min and max_value <= np.iinfo(np.int8).max:
                pa_type = pa.int8()
            elif min_value >= np.iinfo(np.int16).min and max_value <= np.iinfo(np.int16).max:
                pa_type = pa.int16()
            elif min_value >= np.iinfo(np.int32).min and max_value <= np.iinfo(np.int32).max:
                pa_type = pa.int32()
            else:
                pa_type = pa.int64()

        elif pd.api.types.is_float_dtype(dtype):
            pa_type = pa.float64()

        elif pd.api.types.is_bool_dtype(dtype):
            pa_type = pa.bool_()

        elif pd.api.types.is_datetime64_any_dtype(dtype):
            pa_type = pa.timestamp('ms')

        elif isinstance(dtype, pd.CategoricalDtype) or pd.api.types.is_object_dtype(dtype):
            pa_type = pa.string()

        else:
            pa_type = pa.string()

        # Create a field
        field = pa.field(col_name, pa_type, nullable=nullable)
        fields.append(field)

    schema = pa.schema(fields)
    return schema

def pandas_to_parquet_table(df: pd.DataFrame=None, convert: bool=True, partial: bool=False, preserve_index: bool=False, verbose: bool=False) -> pa.Table|None:
    """
    Generate a PyArrow Table from a pandas DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame to generate the table from.
        table (str): The name of the table.

    Returns:
        pyarrow.Table: The PyArrow Table object.
    """
    if df is None:
        print_verbose("No DataFrame provided; exiting generate_parquet_table.", verbose)
        exit 
    
    df     = clean_dataframe_columns(df=df, verbose=verbose)
    
    if convert:
        df = try_cast_string_columns_to_numeric(df=df, convert_partial=partial, verbose=verbose)

    schema = generate_parquet_schema(df=df, verbose=verbose)
    try:
        table = pa.Table.from_pandas(df, schema=schema, preserve_index=preserve_index)
        return table
    except Exception as e:
        print_verbose(f"Error generating PyArrow Table: {e}", verbose)
        exit 

def generate_sql_server_create_table_string(df: pd.DataFrame=None, catalog: str='database', schema: str='dbo', table: str='table', dropexisting: bool=True, verbose: bool=False) -> str|None:
    """
    Generate a SQL Server CREATE TABLE string from a pandas DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame to generate the schema from.
        table_name (str): The name of the SQL table.

    Returns:
        str: The SQL Server CREATE TABLE statement.
    """
    if df is None:
        print_verbose("No DataFrame provided; exiting try_cast_string_columns_to_numeric.", verbose)
        exit 
    
    table_name = f"{sql_quotename(catalog)}.{sql_quotename(schema)}.{sql_quotename(table)}"
    drop_statement = f"use {sql_quotename(catalog)}\rgo\rif object_id('{table_name}') is not null drop table {table_name};\r" if dropexisting else ""
    
    create_statement = [f"{drop_statement};create table {table_name} ("]
    indent = "    "
    column_lines = []

    for column in df.columns:
        col_data = df[column]
        col_name = column
        dtype = col_data.dtype

        # Determine if the column contains any nulls
        nullable = col_data.isnull().any()
        null_str = f"{'   ' if nullable else 'not'} null"

        # Map pandas dtype to SQL Server type
        sql_type = None

        if pd.api.types.is_integer_dtype(dtype):
            min_value = col_data.min()
            max_value = col_data.max()
            if min_value >= 0 and max_value <= 255:
                sql_type = "tinyint"
            elif min_value >= -32768 and max_value <= 32767:
                sql_type = "smallint"
            elif min_value >= -2147483648 and max_value <= 2147483647:
                sql_type = "int"
            else:
                sql_type = "bigint"

        elif pd.api.types.is_float_dtype(dtype):
            sql_type = "float"

        elif pd.api.types.is_bool_dtype(dtype):
            sql_type = "bit"

        elif pd.api.types.is_datetime64_any_dtype(dtype):
            sql_type = "datetime2"

        elif isinstance(dtype, pd.CategoricalDtype) or pd.api.types.is_object_dtype(dtype):
            # Determine maximum length of string data
            max_length = col_data.dropna().astype(str).map(len).max()
            sql_type = f"nvarchar({str(max_length) if max_length <= 4000 else 'max'})"
            
        else:
            sql_type = "nvarchar(max)"

        # Build the column definition
        column_line = f"{indent}{sql_quotename(col_name)} {sql_type} {null_str},"
        column_lines.append(column_line)

    # Remove the last comma from the last column definition
    if column_lines:
        column_lines[-1] = column_lines[-1].rstrip(',')

    create_statement.extend(column_lines)
    create_statement.append(");")
    return_statement = "\r".join(create_statement)
    return return_statement