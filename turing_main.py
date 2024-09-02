import tkinter as tk
from tkinter import messagebox
import subprocess

class MaquinaDeTuringPalindromo:
    def __init__(self):
        self.estados = {'Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q_rejeicao'}
        self.alfabeto_entrada = {'a', 'b'}
        self.alfabeto_fita = {'a', 'b', '_'}
        self.estado_inicial = 'Q0'
        self.estado_rejeicao = 'Q_rejeicao'
        self.estados_aceitacao = {'Q7'}
        
        # Transições para a Máquina de Turing
        self.transicoes = {
            ('Q0', 'a'): ('Q1', '_', 'R'),
            ('Q0', 'b'): ('Q4', '_', 'R'),
            ('Q0', '_'): ('Q7', '_', 'R'),
            
            ('Q1', 'a'): ('Q1', 'a', 'R'),
            ('Q1', 'b'): ('Q1', 'b', 'R'),
            ('Q1', '_'): ('Q2', '_', 'L'),
            
            ('Q2', 'a'): ('Q3', '_', 'L'),
            ('Q2', 'b'): ('Q_rejeicao', '_', 'R'),
            
            ('Q3', 'a'): ('Q3', 'a', 'L'),
            ('Q3', 'b'): ('Q3', 'b', 'L'),
            ('Q3', '_'): ('Q0', '_', 'R'),
            
            ('Q4', 'a'): ('Q4', 'a', 'R'),
            ('Q4', 'b'): ('Q4', 'b', 'R'),
            ('Q4', '_'): ('Q5', '_', 'L'),
            
            ('Q5', 'a'): ('Q_rejeicao', '_', 'R'),
            ('Q5', 'b'): ('Q6', '_', 'L'),
            
            ('Q6', 'a'): ('Q6', 'a', 'L'),
            ('Q6', 'b'): ('Q6', 'b', 'L'),
            ('Q6', '_'): ('Q0', '_', 'R')
        }

    def inicializar_fita(self, palavra):
        self.fita = list(palavra) + ['_']
        self.head = 0
        self.estado_atual = self.estado_inicial

    def mover_cabeca(self, direcao):
        if direcao == 'R':
            self.head += 1
            if self.head == len(self.fita):
                self.fita.append('_')
        elif direcao == 'L':
            self.head = max(0, self.head - 1)

    def executar(self, palavra):
        self.inicializar_fita(palavra)

        while True:
            simbolo_atual = self.fita[self.head]
            if (self.estado_atual, simbolo_atual) in self.transicoes:
                estado_prox, simbolo_prox, direcao = self.transicoes[(self.estado_atual, simbolo_atual)]
                self.fita[self.head] = simbolo_prox
                self.mover_cabeca(direcao)
                self.estado_atual = estado_prox

                if self.estado_atual in self.estados_aceitacao:
                    return "Sim"
                if self.estado_atual == self.estado_rejeicao:
                    return "Não"
            else:
                return "Não"

class MaquinaDeTuringBinario:
    def __init__(self):
        self.estados = {'Q0', 'Q1', 'Q2', 'Q3'}
        self.alfabeto_entrada = {'0', '1'}
        self.alfabeto_fita = {'0', '1', '#', '_'}
        self.estado_inicial = 'Q0'
        self.estado_rejeicao = ''
        self.estados_aceitacao = {'Q3'}
        
        # Transições para a Máquina de Turing
        self.transicoes = {
            ('Q0', '#'): ('Q1', '#', 'R'),
            ('Q1', '0'): ('Q1', '0', 'R'),
            ('Q1', '1'): ('Q1', '1', 'R'),
            ('Q1', '_'): ('Q2', '_', 'L'),
            ('Q2', '0'): ('Q3', '1', 'R'),
            ('Q2', '1'): ('Q2', '0', 'L'),
            ('Q2', '#'): ('Q3', '1', 'R'),
        }

    def inicializar_fita(self, palavra):
        self.fita = list(palavra) + ['_']
        self.head = 0
        self.estado_atual = self.estado_inicial

    def mover_cabeca(self, direcao):
        if direcao == 'R':
            self.head += 1
            if self.head == len(self.fita):
                self.fita.append('_')
        elif direcao == 'L':
            self.head = max(0, self.head - 1)

    def executar(self, palavra):
        self.inicializar_fita(palavra)

        while True:
            simbolo_atual = self.fita[self.head]
            if (self.estado_atual, simbolo_atual) in self.transicoes:
                estado_prox, simbolo_prox, direcao = self.transicoes[(self.estado_atual, simbolo_atual)]
                self.fita[self.head] = simbolo_prox
                self.mover_cabeca(direcao)
                self.estado_atual = estado_prox

                if self.estado_atual in self.estados_aceitacao:
                    return ''.join(self.fita).strip('_')
                if self.estado_atual == self.estado_rejeicao:
                    return "Erro"
            else:
                return "Erro"

class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Máquina de Turing")

        self.mt_palindromo = MaquinaDeTuringPalindromo()
        self.mt_binario = MaquinaDeTuringBinario()

        # Configurando interface
        self.frame_palindromo = tk.Frame(self.root)
        self.frame_palindromo.pack(pady=10)

        self.label_palindromo = tk.Label(self.frame_palindromo, text="Digite uma palavra para verificar se é um palíndromo:")
        self.label_palindromo.pack()

        self.entry_palindromo = tk.Entry(self.frame_palindromo)
        self.entry_palindromo.pack()

        self.button_palindromo = tk.Button(self.frame_palindromo, text="Verificar Palíndromo", command=self.verificar_palindromo)
        self.button_palindromo.pack()

        # Configurando interface para números binários
        self.frame_binario = tk.Frame(self.root)
        self.frame_binario.pack(pady=10)

        self.label_binario = tk.Label(self.frame_binario, text="Digite um número binário para incrementar(Coloque uma # antes do numero):")
        self.label_binario.pack()

        self.entry_binario = tk.Entry(self.frame_binario)
        self.entry_binario.pack()

        self.button_binario = tk.Button(self.frame_binario, text="Incrementar", command=self.incrementar_binario)
        self.button_binario.pack()

    def verificar_palindromo(self):
        palavra = self.entry_palindromo.get()
        resultado = self.mt_palindromo.executar(palavra)
        messagebox.showinfo("Resultado", f"A palavra '{palavra}' é um palíndromo? {resultado}")

    def incrementar_binario(self):
        numero = self.entry_binario.get()
        resultado = self.mt_binario.executar(numero)
        messagebox.showinfo("Resultado", f"O número binário {numero} após incremento é: {resultado}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()
