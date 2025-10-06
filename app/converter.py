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
    java_lines = [f"StringBuilder {variable_name} = new StringBuilder();"]
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
            
            base_statement = " + ".join(part for part in line_parts if part and part != '""')

            final_part = f'"{escape_line(remaining_text)} \\n"'

            if base_statement:
                full_append_statement = f"{base_statement} + {final_part}"
            else: # Caso a linha seja SÓ uma variável, como {{minha_var}}
                full_append_statement = final_part

            java_lines.append(f'{variable_name}.append({full_append_statement});')

    return "\n".join(java_lines)

def convert_java_to_sql(java_code: str) -> str:
    """
    Converte código Java StringBuilder de volta para uma string SQL.
    Reconhece concatenações de variáveis e as converte para o formato {{variavel}}.
    """
    sql_lines = []
    
    append_content_regex = re.compile(r'\.append\((.*?)\);', re.DOTALL)
    
    def unescape_java_string(s: str) -> str:
        if s.startswith('"') and s.endswith('"'):
            s = s[1:-1]
        return s.replace('\\"', '"').replace('\\\\', '\\')

    for line in java_code.splitlines():
        match = append_content_regex.search(line)
        if not match:
            continue

        content = match.group(1).strip()
        
        if content.endswith('+ " \\n"'):
            content = content[:-7].strip()

        sql_line_parts = []
        parts = re.split(r'\s*\+\s*', content)

        for part in parts:
            part = part.strip()
            if part.startswith('"') and part.endswith('"'):
                text = unescape_java_string(part)
                if text.endswith(' \\n'):
                    text = text[:-3]
                sql_line_parts.append(text)
            elif part:
                sql_line_parts.append(f"{{{{{part}}}}}")
        
        sql_lines.append("".join(sql_line_parts))

    return "\n".join(sql_lines)