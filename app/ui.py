import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from .converter import convert_sql_to_java_builder, convert_java_to_sql

class MainApplicationWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor SQL <-> Java StringBuilder")
        self.root.geometry("1200x450")

        self._create_widgets()

    def _create_widgets(self):
        """Cria e posiciona todos os componentes visuais (widgets) na janela."""
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_pane = tk.Frame(main_frame, padx=5)
        center_pane = tk.Frame(main_frame, padx=10)
        right_pane = tk.Frame(main_frame, padx=5)

        left_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        center_pane.pack(side=tk.LEFT, fill=tk.Y)
        right_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(left_pane, text="Código SQL:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        self.sql_input = scrolledtext.ScrolledText(left_pane, height=10, wrap=tk.WORD, undo=True)
        self.sql_input.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        sql_buttons_frame = tk.Frame(left_pane)
        sql_buttons_frame.pack(fill=tk.X)
        self.load_button = tk.Button(sql_buttons_frame, text="Carregar de .sql...", command=self.load_sql_file)
        self.load_button.pack(side=tk.LEFT)
        self.copy_sql_button = tk.Button(sql_buttons_frame, text="Copiar SQL", command=lambda: self.copy_to_clipboard(self.sql_input))
        self.copy_sql_button.pack(side=tk.RIGHT)
        
        tk.Label(center_pane, text="Ações", font=("Helvetica", 12, "bold")).pack(pady=(0, 10))
        
        conversion_frame = tk.LabelFrame(center_pane, text="Conversão", padx=10, pady=10)
        conversion_frame.pack(fill=tk.X, pady=10)
        
        self.s2j_button = tk.Button(conversion_frame, text="-->", command=self.perform_sql_to_java, font=("Helvetica", 10, "bold"))
        self.s2j_button.pack(pady=5, fill=tk.X)
        
        self.j2s_button = tk.Button(conversion_frame, text="<--", command=self.perform_java_to_sql, font=("Helvetica", 10, "bold"))
        self.j2s_button.pack(pady=5, fill=tk.X)

        tk.Label(conversion_frame, text="Nome da Var. Java:").pack(pady=(10, 0))
        self.variable_name_entry = tk.Entry(conversion_frame, width=20)
        self.variable_name_entry.insert(0, "sql")
        self.variable_name_entry.pack()

        assign_var_frame = tk.LabelFrame(center_pane, text="Atribuir Variável", padx=10, pady=10)
        assign_var_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(assign_var_frame, text="Nome da Variável:").pack()
        self.param_name_entry = tk.Entry(assign_var_frame)
        self.param_name_entry.pack(pady=5, fill=tk.X)
        
        self.assign_var_button = tk.Button(assign_var_frame, text="Atribuir à Seleção", command=self._assign_variable_to_selection)
        self.assign_var_button.pack(pady=5, fill=tk.X)

        tk.Label(right_pane, text="Java StringBuilder:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        self.java_output = scrolledtext.ScrolledText(right_pane, height=10, wrap=tk.WORD, undo=True)
        self.java_output.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        java_buttons_frame = tk.Frame(right_pane)
        java_buttons_frame.pack(fill=tk.X)
        self.copy_java_button = tk.Button(java_buttons_frame, text="Copiar Java", command=lambda: self.copy_to_clipboard(self.java_output))
        self.copy_java_button.pack(side=tk.RIGHT)

        self.status_label = tk.Label(self.root, text="Pronto.", bd=1, relief=tk.SUNKEN, anchor=tk.W, padx=5)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def _assign_variable_to_selection(self):
        """Substitui o texto selecionado no campo focado por um placeholder de variável."""
        param_name = self.param_name_entry.get().strip()
        if not param_name:
            self.status_label.config(text="Erro: Nome da variável não pode ser vazio.")
            return

        focused_widget = self.root.focus_get()
        target_widget, placeholder = None, ""

        if focused_widget == self.sql_input:
            target_widget = self.sql_input
            placeholder = f"{{{{{param_name}}}}}"
        elif focused_widget == self.java_output:
            target_widget = self.java_output
            placeholder = f'" + {param_name} + "'
        else:
            self.status_label.config(text="Erro: Selecione texto no campo SQL ou Java para atribuir a variável.")
            return

        try:
            start = target_widget.index(tk.SEL_FIRST)
            end = target_widget.index(tk.SEL_LAST)
            target_widget.delete(start, end)
            target_widget.insert(start, placeholder)
            self.status_label.config(text=f"Variável '{param_name}' atribuída com sucesso.")
        except tk.TclError:
            self.status_label.config(text="Erro: Nenhum texto selecionado no campo de destino.")

    def load_sql_file(self):
        filepath = filedialog.askopenfilename(title="Abrir arquivo SQL", filetypes=[("SQL Files", "*.sql"), ("All Files", "*.*")])
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

    def perform_sql_to_java(self):
        sql_text = self.sql_input.get('1.0', tk.END).strip()
        if not sql_text:
            self.status_label.config(text="O campo de SQL está vazio.")
            return

        variable_name = self.variable_name_entry.get()
        java_code = convert_sql_to_java_builder(sql_text, variable_name)

        self.java_output.delete('1.0', tk.END)
        self.java_output.insert(tk.END, java_code)
        self.status_label.config(text="Conversão de SQL para Java realizada com sucesso!")

    def perform_java_to_sql(self):
        java_text = self.java_output.get('1.0', tk.END).strip()
        if not java_text:
            self.status_label.config(text="O campo Java está vazio.")
            return
            
        sql_code = convert_java_to_sql(java_text)
        
        self.sql_input.delete('1.0', tk.END)
        self.sql_input.insert(tk.END, sql_code)
        self.status_label.config(text="Conversão de Java para SQL realizada com sucesso!")

    def copy_to_clipboard(self, text_widget):
        content = text_widget.get('1.0', tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.status_label.config(text="Copiado para a área de transferência!")
        else:
            self.status_label.config(text="Nada para copiar.")