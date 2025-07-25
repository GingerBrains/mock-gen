def write_sql(data, table_name='test_table', output_file=None):
    """Write data as SQL insert statements. If output_file is None, print to stdout."""
    if not data:
        return
    fieldnames = data[0].keys()
    lines = []
    for row in data:
        values = []
        for field in fieldnames:
            val = row[field]
            if isinstance(val, str):
                val = val.replace("'", "''")
                values.append(f"'{val}'")
            else:
                values.append(str(val))
        line = f"INSERT INTO {table_name} ({', '.join(fieldnames)}) VALUES ({', '.join(values)});"
        lines.append(line)
    sql_output = '\n'.join(lines)
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sql_output)
    else:
        print(sql_output) 