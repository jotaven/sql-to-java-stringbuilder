import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from .converter import convert_sql_to_java_builder

class MainApplicationWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de SQL para Java StringBuilder")
        self.root.geometry("800x650")

        self._create_widgets()

    def _create_widgets(self):
        """Cria e posiciona todos os componentes visuais (widgets) na janela."""
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        config_frame = tk.Frame(main_frame)
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(config_frame, text="Nome da variável StringBuilder:").pack(side=tk.LEFT, padx=(0, 5))
        self.variable_name_entry = tk.Entry(config_frame, width=30)
        self.variable_name_entry.insert(0, "sql")
        self.variable_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.load_button = tk.Button(config_frame, text="Carregar de .sql...", command=self.load_sql_file)
        self.load_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Label(main_frame, text="Insira ou cole seu código SQL aqui:").pack(anchor="w")
        self.sql_input = scrolledtext.ScrolledText(main_frame, height=10, wrap=tk.WORD, undo=True)
        self.sql_input.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.sql_input.insert(tk.END, "SELECT\n    nome,\n    preco\nFROM\n    produtos\nWHERE\n    id = ?;")
        self.sql_input.insert(tk.END, "SELECT\n    nome,\n    preco\nFROM\n    produtos\nWHERE\n    id = {{id}};")

        assign_var_frame = tk.Frame(main_frame)
        assign_var_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(assign_var_frame, text="Nome da Variável p/ Seleção:").pack(side=tk.LEFT)
        self.param_name_entry = tk.Entry(assign_var_frame)
        self.param_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.assign_var_button = tk.Button(assign_var_frame, text="Atribuir Variável", command=self._assign_variable_to_selection)
        self.assign_var_button.pack(side=tk.LEFT)

        self.convert_button = tk.Button(main_frame, text="Converter para Java", command=self.perform_conversion, 
                                      font=("Helvetica", 12, "bold"), height=2)
        self.convert_button.pack(fill=tk.X, pady=(5, 10))

        tk.Label(main_frame, text="Código Java Gerado:").pack(anchor="w")
        self.java_output = scrolledtext.ScrolledText(main_frame, height=10, wrap=tk.WORD)
        self.java_output.pack(fill=tk.BOTH, expand=True)
        self.java_output.config(state='disabled')
        
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.copy_button = tk.Button(bottom_frame, text="Copiar Resultado", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(bottom_frame, text="Pronto.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

    def _assign_variable_to_selection(self):
        """Substitui o texto selecionado no input de SQL por um placeholder de variável."""
        try:
            start = self.sql_input.index(tk.SEL_FIRST)
            end = self.sql_input.index(tk.SEL_LAST)
        except tk.TclError:
            self.status_label.config(text="Erro: Nenhum texto selecionado.")
            return

        param_name = self.param_name_entry.get().strip()
        if not param_name:
            self.status_label.config(text="Erro: Nome da variável não pode ser vazio.")
            return
        
        placeholder = f"{{{{{param_name}}}}}"
        
        self.sql_input.delete(start, end)
        self.sql_input.insert(start, placeholder)
        self.status_label.config(text=f"Variável '{param_name}' atribuída.")

    def load_sql_file(self):
        filepath = filedialog.askopenfilename(
            title="Abrir arquivo SQL",
            filetypes=[("SQL Files", "*.sql"), ("All Files", "*.*")]
        )
        if not filepath: return
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.sql_input.delete('1.0', tk.END)
                self.sql_input.insert(tk.END, content)
                self.status_label.config(text=f"Arquivo '{filepath.split('/')[-1]}' carregado.")
        except Exception as e:
            messagebox.showerror("Erro de Leitura", f"Não foi possível ler o arquivo:\n{e}")
            self.status_label.config(text="Falha ao carregar arquivo.")

    def perform_conversion(self):
        sql_text = self.sql_input.get('1.0', tk.END).strip()
        if not sql_text:
            self.status_label.config(text="O campo de SQL está vazio.")
            return

        variable_name = self.variable_name_entry.get()
        java_code = convert_sql_to_java_builder(sql_text, variable_name)

        self.java_output.config(state='normal')
        self.java_output.delete('1.0', tk.END)
        self.java_output.insert(tk.END, java_code)
        self.java_output.config(state='disabled')
        self.status_label.config(text="Conversão realizada com sucesso!")

    def copy_to_clipboard(self):
        content = self.java_output.get('1.0', tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.status_label.config(text="Copiado para a área de transferência!")
        else:
            self.status_label.config(text="Nada para copiar.")