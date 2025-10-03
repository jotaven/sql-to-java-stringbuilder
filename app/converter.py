import re

def convert_sql_to_java_builder(sql_string: str, variable_name: str) -> str:
    """
    Converte uma string SQL em linhas de código Java usando StringBuilder,
    reconhecendo placeholders no formato {{variavel}} para concatenação.
    """
    if not variable_name.strip():
        variable_name = "sql"

    def escape_line(line: str) -> str:
        """Escapa aspas duplas e barras invertidas para strings Java."""
        return line.replace('\\', '\\\\').replace('"', '\\"')

    lines = sql_string.splitlines()
    java_lines = []

    java_lines.append(f"StringBuilder {variable_name} = new StringBuilder();")

    placeholder_regex = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")

    for line in lines:
        matches = list(placeholder_regex.finditer(line))

        if not matches:
            escaped_line = escape_line(line)
            java_lines.append(f'{variable_name}.append("{escaped_line} \\n");')
        else:
            line_parts = []
            last_index = 0
            for match in matches:
                start, end = match.span()
                text_part = line[last_index:start]
                if text_part:
                    line_parts.append(f'"{escape_line(text_part)}"')
                
                var_name = match.group(1)
                line_parts.append(var_name)
                
                last_index = end

            remaining_text = line[last_index:]
            if remaining_text:
                line_parts.append(f'"{escape_line(remaining_text)}"')
            
            full_append_statement = " + ".join(line_parts)
            java_lines.append(f'{variable_name}.append({full_append_statement} + " \\n");')


    return "\n".join(java_lines)