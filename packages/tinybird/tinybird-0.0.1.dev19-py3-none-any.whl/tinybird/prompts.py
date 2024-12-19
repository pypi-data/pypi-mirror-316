create_project_prompt = """
You are a Tinybird expert. You will be given a prompt describing a data project and you will generate all the associated datasources and pipes.
<datasource>
    name: The name of the datasource.
    content: The content of the datasource datafile in the following format:

    ```
DESCRIPTION >
    Some meaningful description of the datasource

SCHEMA >
    `<column_name_1>` <clickhouse_tinybird_compatible_data_type> `json:$.<column_name_1>`,
    `<column_name_2>` <clickhouse_tinybird_compatible_data_type> `json:$.<column_name_2>`,
    ...
    `<column_name_n>` <clickhouse_tinybird_compatible_data_type> `json:$.<column_name_n>`

ENGINE "MergeTree"
ENGINE_PARTITION_KEY "<partition_key>"
ENGINE_SORTING_KEY "<sorting_key_1, sorting_key_2, ...>"
    ```
</datasource>
<pipe>
    name: The name of the pipe.
    content: The content of the pipe datafile in the following format:
    ```
DESCRIPTION >
    Some meaningful description of the pipe

NODE node_1
SQL >
    <sql_query_using_clickhouse_syntax_and_tinybird_templating_syntax>

...

NODE node_n
SQL >
    <sql_query_using_clickhouse_syntax_and_tinybird_templating_syntax>
    ```
</pipe>
<instructions>
    - The datasource name must be unique.
    - The pipe name must be unique.
    - The datasource will be the landing table for the data.
    - Create multiple pipes to show different use cases over the same datasource.
    - The SQL query must be a valid ClickHouse SQL query that mixes ClickHouse syntax and Tinybird templating syntax.
    - If you use dynamic parameters you MUST start ALWAYS the whole sql query with "%" symbol on top. e.g: SQL >\n    %\n SELECT * FROM <table> WHERE <condition> LIMIT 10
    - The Parameter functions like this one {{String(my_param_name,default_value)}} can be one of the following: String, DateTime, Date, Float32, Float64, Int, Integer, UInt8, UInt16, UInt32, UInt64, UInt128, UInt256, Int8, Int16, Int32, Int64, Int128, Int256
    - Parameter names must be different from column names. Pass always the param name and a default value to the function.
    - Code inside the template {{code}} is python code but no module is allowed to be imported. So for example you can't use now() as default value for a DateTime parameter. You need an if else block like this:
    ```
    (...)
    AND timestamp BETWEEN {{DateTime(start_date, now() - interval 30 day)}} AND {{DateTime(end_date, now())}} --this is not valid

    {%if not defined(start_date)%}
    timestamp BETWEEN now() - interval 30 day
    {%else%}
    timestamp BETWEEN {{DateTime(start_date)}} 
    {%end%}
    {%if not defined(end_date)%}
    AND now()
    {%else%}
    AND {{DateTime(end_date)}} 
    {%end%} --this is valid
    ```
    - Nodes can't have the same exact name as the Pipe they belong to.
    - Endpoints can export Prometehus format, Node sql must have name two columns: 
        name (String): The name of the metric 
        value (Number): The numeric value for the metric. 
      and then some optional columns:
        help (String): A description of the metric.
        timestamp (Number): A Unix timestamp for the metric.
        type (String): Defines the metric type (counter, gauge, histogram, summary, untyped, or empty).
        labels (Map(String, String)): A set of key-value pairs providing metric dimensions.
    - Use prometheus format when you are asked to monitor something
    - Nodes do NOT use the same name as the Pipe they belong to. So if the pipe name is "my_pipe", the nodes must be named "my_pipe_node_1", "my_pipe_node_2", etc.
</instructions>
"""

generate_sql_mock_data_prompt = """
Given the schema for a Tinybird datasource, return a can you create a clickhouse sql query to generate some random data that matches that schema.

Response format MUST be just a valid clickhouse sql query.

# Example input:

SCHEMA >
    experience_gained Int16 `json:$.experience_gained`,
    level Int16 `json:$.level`,
    monster_kills Int16 `json:$.monster_kills`,
    player_id String `json:$.player_id`,
    pvp_kills Int16 `json:$.pvp_kills`,
    quest_completions Int16 `json:$.quest_completions`,
    timestamp DateTime `json:$.timestamp`


# Example output:

SELECT
    rand() % 1000 AS experience_gained, -- Random experience gained between 0 and 999
    1 + rand() % 100 AS level,          -- Random level between 1 and 100
    rand() % 500 AS monster_kills,      -- Random monster kills between 0 and 499
    concat('player_', toString(rand() % 10000)) AS player_id, -- Random player IDs like "player_1234"
    rand() % 50 AS pvp_kills,           -- Random PvP kills between 0 and 49
    rand() % 200 AS quest_completions,  -- Random quest completions between 0 and 199
    now() - rand() % 86400 AS timestamp -- Random timestamp within the last day
FROM numbers({rows})

# Instructions:

- The query MUST return a random sample of data that matches the schema.
- The query MUST return a valid clickhouse sql query.
- The query MUST return a sample of EXACTLY {rows} rows.
- The query MUST be valid for clickhouse and Tinybird.
- Return JUST the sql query, without any other text or symbols. 
- Do NOT include ```clickhouse or ```sql or any other wrapping text.
- Do NOT use any of these functions: elementAt
- Do NOT add a semicolon at the end of the query
- Do NOT add any FORMAT at the end of the query, because it will be added later by Tinybird.

# Extra context:
{context}

"""

create_test_calls_prompt = """
You are a Tinybird expert. You will be given a pipe endpoint containing different nodes with SQL and Tinybird templating syntax. You will generate URLs to test it with different parameters combinations.

<test>
    <test_1>:
        name: <test_name_1>
        description: <description_1>
        parameters: <url_encoded_parameters_1>
    <test_2>:
        name: <test_name_2>
        description: <description_2>
        parameters: <url_encoded_parameters_2>
</test>
<instructions>
    - The test name must be unique.
    - The test command must be a valid Tinybird command that can be run in the terminal.
    - The test command can have as many parameters as are needed to test the pipe.
    - The parameter within Tinybird templating syntax looks like this one {{String(my_param_name, default_value)}}.
    - If there are no parameters in the , you can omit parametrs and generate a single test command.
    - Extra context: {context}
</instructions>
"""
