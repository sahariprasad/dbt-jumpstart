import pandas as pd
import openpyxl
import os

# function for adding a line
def add_line(str1, str2):
    str1 = str1 + '\n' + str2
    return str1

# function for adding a line with a comma at the end
def add_line_with_comma(str1, str2):
    str1 = str1 + '\n' + str2 + ","
    return str1

def make_models(input_file_path, output_file_path):
    model_output_path = output_file_path

    tables_file = pd.ExcelFile(os.path.join(input_file_path, "tables.xlsx"))
    tables_dfs = {sheet_name: tables_file.parse(sheet_name) for sheet_name in tables_file.sheet_names}

    columns_file = pd.ExcelFile(os.path.join(input_file_path, "columns.xlsx"))
    columns_dfs = {sheet_name: columns_file.parse(sheet_name) for sheet_name in columns_file.sheet_names}

    # convert the dataframes in the columns_dfs to dicts and create a new larger dict containing everything
    columns_dict = {}
    for sheet in columns_dfs:
        columns_dict[sheet] = columns_dfs[sheet].to_dict('records')

    # convert the dataframes in the tables_dfs to dicts and create a new larger dict containing everything
    tables_dict = {}
    for sheet in tables_dfs:
        tables_dict = tables_dfs[sheet].to_dict('records')

    # put all the info about tables and columns into main_dict
    main_dict = {}
    for item in tables_dict:
        main_dict[item["name"]] = {}
        main_dict[item["name"]]["source"] = item["source"]
        main_dict[item["name"]]["description"] = item["description"]
        main_dict[item["name"]]["alias"] = item["alias"]
        main_dict[item["name"]]["materialization"] = item["materialization"]
        main_dict[item["name"]]["source_or_ref"] = item["source_or_ref"]
        main_dict[item["name"]]["columns"] = columns_dict[item["name"]]

    tab2 = "  "
    tab3 = "   "
    tab4 = 2 * tab2
    tab6 = 3 * tab2
    tab8 = 4 * tab2

    # mother dough for schema.yml
    schema_str = """ 
    version: 2 
    
    models:"""

    # build model
    for table in main_dict:
        # config part
        config_str = """{{ 
         config( 
            alias = '""" + main_dict[table]["alias"] + """', 
            materialized = '""" + main_dict[table]["materialization"] + """' 
        ) 
    }} 
    
"""
        # SQL part
        model_str = "select"
        for column in main_dict[table]["columns"]:
            if column is not main_dict[table]["columns"][-1]:
                model_str = add_line_with_comma(model_str, tab4 + '"' + column["name"] + '"' + " as " + column["alias"])
            else:
                model_str = add_line(model_str, tab4 + '"' + column["name"] + '"' + " as " + column["alias"])
        if main_dict[table]["source_or_ref"] == "source":
            model_str = add_line(model_str, "from " + main_dict[table]["source"])
        else:
            model_str = add_line(model_str, "from {{ ref('" + main_dict[table]["source"] + "') }}")

        output_file = open(os.path.join(model_output_path, "{}.sql".format(table)), "w", encoding="utf-8")
        output_file.write(config_str + model_str)
        output_file.close()

        # build schema.yml
        schema_str = add_line(schema_str, tab4 + "- name: " + table)
        schema_str = add_line(schema_str, tab4 + "  description: \"" + main_dict[table]["description"] + "\"")
        schema_str = add_line(schema_str, tab4 + "  columns:")
        for column in main_dict[table]["columns"]:
            schema_str = add_line(schema_str, tab8 + "-")
            schema_str = add_line(schema_str, tab8 + "  name: " + column["name"])
            schema_str = add_line(schema_str, tab8 + "  description: \"" + column["description"] + "\"")
        schema_str = add_line(schema_str, "")
    output_file = open(os.path.join(model_output_path, "schema.yml"), "w", encoding="utf-8")
    output_file.write(schema_str)
    output_file.close()
