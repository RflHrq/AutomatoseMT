import tkinter as tk
import subprocess
from tkinter import scrolledtext, messagebox
from main import Automatos, AFD, AFDMinimizado

class AutomatoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Autômatos")
        self.afn = Automatos()
        self.afd = None
        self.afd_minimizado = None

        # Configuração da Scrollbar
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Widgets para entrada de dados
        self.criar_widgets()

    def criar_widgets(self):
        tk.Label(self.inner_frame, text="Insira os estados:").pack(anchor="w")
        self.estados_entry = tk.Entry(self.inner_frame)
        self.estados_entry.pack(fill=tk.X)

        tk.Label(self.inner_frame, text="Insira os símbolos do alfabeto:").pack(anchor="w")
        self.alfabeto_entry = tk.Entry(self.inner_frame)
        self.alfabeto_entry.pack(fill=tk.X)

        tk.Label(self.inner_frame, text="Insira o estado inicial:").pack(anchor="w")
        self.estado_inicial_entry = tk.Entry(self.inner_frame)
        self.estado_inicial_entry.pack(fill=tk.X)

        tk.Label(self.inner_frame, text="Insira os estados finais:").pack(anchor="w")
        self.estados_finais_entry = tk.Entry(self.inner_frame)
        self.estados_finais_entry.pack(fill=tk.X)

        tk.Label(self.inner_frame, text="Insira as transições (estado,símbolo,estados_destino separados por 'Enter'):").pack(anchor="w")
        self.transicoes_text = scrolledtext.ScrolledText(self.inner_frame, height=10)
        self.transicoes_text.pack(fill=tk.X)

        self.botao_criar_afn = tk.Button(self.inner_frame, text="Criar Automato", command=self.criar_afn)
        self.botao_criar_afn.pack(pady=10)

        # Área de texto para saída do autômato
        tk.Label(self.inner_frame, text="Resultado:").pack(anchor="w")
        self.text_output_automato = scrolledtext.ScrolledText(self.inner_frame, height=10)
        self.text_output_automato.pack(fill=tk.BOTH, expand=True)

        # Entrada para testar a palavra
        tk.Label(self.inner_frame, text="Teste uma palavra:").pack(anchor="w")
        self.entry_palavra = tk.Entry(self.inner_frame)
        self.entry_palavra.pack(fill=tk.X)

        # Botão para testar a palavra
        self.botao_testar_palavra = tk.Button(self.inner_frame, text="Testar Palavra", command=self.testar_palavra)
        self.botao_testar_palavra.pack(pady=10)

        # Área de texto para saída dos resultados de teste
        self.text_output_palavra = scrolledtext.ScrolledText(self.inner_frame, height=10)
        self.text_output_palavra.pack(fill=tk.BOTH, expand=True)

    def criar_afn(self):
        try:
            # Adicionando estados
            estados = self.estados_entry.get().split()
            for estado in estados:
                self.afn.adicionar_estado(estado)

            # Adicionando símbolos do alfabeto
            simbolos = self.alfabeto_entry.get().split()
            for simbolo in simbolos:
                self.afn.adicionar_simbolo_alfabeto(simbolo)

            # Definindo estado inicial
            estado_inicial = self.estado_inicial_entry.get()
            self.afn.definir_estado_inicial(estado_inicial)

            # Adicionando estados finais
            estados_finais = self.estados_finais_entry.get().split()
            for estado_final in estados_finais:
                self.afn.adicionar_estado_final(estado_final)

            # Adicionando transições
            transicoes = self.transicoes_text.get("1.0", tk.END).strip().split("\n")
            for transicao in transicoes:
                try:
                    de_estado, simbolo, para_estados_str = transicao.split(',')
                    para_estados = set(para_estados_str.split())
                    self.afn.adicionar_transicao(de_estado, simbolo, para_estados)
                except ValueError as e:
                    messagebox.showerror("Erro de Transição", f"Formato de transição inválido: {transicao}")
                    return

            # Exibindo o autômato criado
            self.text_output_automato.delete("1.0", tk.END)  # Limpa a área de texto
            resultado_afn = self.formatar_automato(self.afn)
            if resultado_afn:
                self.text_output_automato.insert(tk.END, resultado_afn)
            else:
                self.text_output_automato.insert(tk.END, "Erro ao imprimir o Automato.")
            self.verificar_tipo_automato()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def verificar_tipo_automato(self):
        if self.afn.eh_deterministico():
            self.text_output_automato.insert(tk.END, "\nO autômato é um AFD.\n")
            self.afd = self.afn  # Se for um AFD, não precisa de conversão
            resultado_afd = self.formatar_automato(self.afd)
            if resultado_afd:
                self.text_output_automato.insert(tk.END, "\nAFD:\n")
                self.text_output_automato.insert(tk.END, resultado_afd)
            
            # Minimiza o AFD
            self.afd_minimizado = AFDMinimizado(self.afd)  # Minimiza o AFD
            resultado_afd_minimizado = self.formatar_automato(self.afd_minimizado)
            if resultado_afd_minimizado:
                self.text_output_automato.insert(tk.END, "\nAFD Minimizado:\n")
                self.text_output_automato.insert(tk.END, resultado_afd_minimizado)
        else:
            self.text_output_automato.insert(tk.END, "\nO autômato é um AFN. Convertendo para AFD...\n")
            self.afd = AFD(self.afn)
            resultado_afd = self.formatar_automato(self.afd)
            if resultado_afd:
                self.text_output_automato.insert(tk.END, "\nAFD:\n")
                self.text_output_automato.insert(tk.END, resultado_afd)
            
            # Minimiza o AFD
            self.afd_minimizado = AFDMinimizado(self.afd)  # Minimiza o AFD
            resultado_afd_minimizado = self.formatar_automato(self.afd_minimizado)
            if resultado_afd_minimizado:
                self.text_output_automato.insert(tk.END, "\nAFD Minimizado:\n")
                self.text_output_automato.insert(tk.END, resultado_afd_minimizado)

    def formatar_automato(self, automato):
        automato_dados = {}
        tipo = "Desconhecido"

        # Identifica o tipo do autômato e obtém os dados apropriados
        if isinstance(automato, AFDMinimizado):
            automato_dados = automato.minimizado
            tipo = "AFD Minimizado"
        elif isinstance(automato, AFD):
            automato_dados = automato.dfa
            tipo = "AFD"
        elif isinstance(automato, Automatos):
            # Usar diretamente os atributos do AFN
            automato_dados = {
                'estados': list(automato.estados),
                'alfabeto': list(automato.alfabeto),
                'estado_inicial': automato.estado_inicial,
                'estados_finais': list(automato.estados_finais),
                'transicoes': automato.transicoes
            }
            tipo = "Automato"
        else:
            return "Tipo de autômato não reconhecido."

        # Garantir que todos os campos esperados estejam presentes
        estados = automato_dados.get('estados', [])
        alfabeto = automato_dados.get('alfabeto', [])
        estado_inicial = automato_dados.get('estado_inicial', '')
        estados_finais = automato_dados.get('estados_finais', [])
        transicoes = automato_dados.get('transicoes', {})

        # Converter itens para strings, se necessário
        estados = [str(item) for item in estados]
        alfabeto = [str(item) for item in alfabeto]
        estados_finais = [str(item) for item in estados_finais]

        # Formata as transições
        transicoes_formatadas = []
        for estado_origem, transicoes_dict in transicoes.items():
            for simbolo, estado_destino in transicoes_dict.items():
                transicoes_formatadas.append(f"  {estado_origem} --{simbolo}--> {estado_destino}")

        # Retorna o formato do autômato
        return (f"Tipo: {tipo}\n"
                f"Estados: {', '.join(estados)}\n"
                f"Alfabeto: {', '.join(alfabeto)}\n"
                f"Estado inicial: {estado_inicial}\n"
                f"Estados finais: {', '.join(estados_finais)}\n"
                f"Transições:\n" + "\n".join(transicoes_formatadas))


    def testar_palavra(self):
            palavra = self.entry_palavra.get()
            if not palavra:
                messagebox.showerror("Erro", "Digite uma palavra para testar.")
                return

            resultado = ""
            if self.afn:
                resultado += f"\nTeste de Palavra no AFN:\n"
                resultado += "Aceita" if self.afn.aceita(palavra) else "Não aceita"
            
            if self.afd:
                resultado += f"\n\nTeste de Palavra no AFD:\n"
                resultado += "Aceita" if self.afd.aceita(palavra) else "Não aceita"
            
            if self.afd_minimizado:
                resultado += f"\n\nTeste de Palavra no AFD Minimizado:\n"
                resultado += "Aceita" if self.afd_minimizado.aceita(palavra) else "Não aceita"
            
            self.text_output_palavra.delete("1.0", tk.END)  # Limpa a área de texto
            self.text_output_palavra.insert(tk.END, resultado)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomatoApp(root)
    root.mainloop()
