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

    # Linha de inicialização do StringBuilder
    java_lines.append(f"StringBuilder {variable_name} = new StringBuilder();")

    # Adiciona cada linha do SQL com .append()
    for line in lines:
        escaped_line = escape_line(line)
        # Adiciona um espaço antes do \n para melhor formatação, como no exemplo
        java_lines.append(f'{variable_name}.append("{escaped_line} \\n");')

    return "\n".join(java_lines)