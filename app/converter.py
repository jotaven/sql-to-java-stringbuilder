def convert_sql_to_java_builder(sql_string: str, variable_name: str) -> str:
    """
    Converte uma string SQL em linhas de código Java usando StringBuilder.

    Args:
        sql_string (str): O código SQL a ser convertido.
        variable_name (str): O nome desejado para a variável StringBuilder.

    Returns:
        str: O código Java formatado.
    """
    if not variable_name.strip():
        variable_name = "sql"

    def escape_line(line: str) -> str:
        """Escapa caracteres especiais para strings Java: aspas duplas e barras invertidas."""
        return line.replace('\\', '\\\\').replace('"', '\\"')

    lines = sql_string.splitlines()
    java_lines = []

    java_lines.append(f"StringBuilder {variable_name} = new StringBuilder();")

    for line in lines:
        escaped_line = escape_line(line)
        java_lines.append(f'{variable_name}.append("{escaped_line} \\n");')

    return "\n".join(java_lines)