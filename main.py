class Automatos:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.estado_inicial = None
        self.estados_finais = set()
        self.transicoes = {}

    def adicionar_estado(self, estado):
        if estado in self.estados:
            raise ValueError("Estado já existente")
        self.estados.add(estado)

    def adicionar_simbolo_alfabeto(self, simbolo):
        if simbolo in self.alfabeto:
            raise ValueError("Símbolo já existente")
        self.alfabeto.add(simbolo)

    def definir_estado_inicial(self, estado):
        if estado not in self.estados:
            raise ValueError("Estado inicial deve estar nos estados inseridos")
        self.estado_inicial = estado

    def adicionar_estado_final(self, estado):
        if estado not in self.estados:
            raise ValueError("Estado final deve estar nos estados inseridos")
        self.estados_finais.add(estado)

    def adicionar_transicao(self, estado_origem, simbolo, estados_destino):
        if estado_origem not in self.estados:
            raise ValueError("Estado de origem deve estar nos estados inseridos")
        if simbolo not in self.alfabeto:
            raise ValueError("Símbolo de transição deve estar no alfabeto inserido")
        if not estados_destino.issubset(self.estados):
            raise ValueError("Estados de destino devem estar nos estados inseridos")
        
        if estado_origem not in self.transicoes:
            self.transicoes[estado_origem] = {}
        if simbolo not in self.transicoes[estado_origem]:
            self.transicoes[estado_origem][simbolo] = set()
        self.transicoes[estado_origem][simbolo].update(estados_destino)

    def get_estados(self):
        return list(self.estados)

    def get_alfabeto(self):
        return list(self.alfabeto)

    def get_estado_inicial(self):
        return self.estado_inicial

    def get_estados_finais(self):
        return list(self.estados_finais)

    def get_transicoes(self):
        return self.transicoes

    def imprimir_automato(self):
        print("Autômato:")
        print("Estados:", self.estados)
        print("Alfabeto:", self.alfabeto)
        print("Estado inicial:", self.estado_inicial)
        print("Estados finais:", self.estados_finais)
        print("Transições:")
        for estado_origem, transicoes in self.transicoes.items():
            for simbolo, estados_destino in transicoes.items():
                print(f"  {estado_origem} --{simbolo}--> {estados_destino}")

    def eh_deterministico(self):
        for estado in self.transicoes:
            for simbolo in self.transicoes[estado]:
                # Se houver mais de um estado de destino para um dado símbolo, não é determinístico
                if len(self.transicoes[estado][simbolo]) > 1:
                    return False
        return True

    def _dfs(self, estado_atual, palavra):
        if len(palavra) == 0:
            return estado_atual in self.estados_finais
        if estado_atual not in self.transicoes or palavra[0] not in self.transicoes[estado_atual]:
            return False
        proximos_estados = self.transicoes[estado_atual][palavra[0]]
        for estado in proximos_estados:
            if self._dfs(estado, palavra[1:]):
                return True
        return False

    def aceita(self, palavra):
        return self._dfs(self.estado_inicial, palavra)

class AFD:
    def __init__(self, afn):
        self.afn = afn
        self.dfa = {
            'estados': set(),
            'alfabeto': afn.alfabeto,
            'estado_inicial': None,
            'estados_finais': set(),
            'transicoes': {}
        }
        self.converter_afn_para_afd()

    def converter_afn_para_afd(self):
        estado_inicial = frozenset([self.afn.estado_inicial])
        self.dfa['estado_inicial'] = estado_inicial
        self.dfa['estados'].add(estado_inicial)
        fila = [estado_inicial]

        while fila:
            estado_atual = fila.pop(0)
            for simbolo in self.afn.alfabeto:
                novos_estados = set()
                for estado in estado_atual:
                    if simbolo in self.afn.transicoes.get(estado, {}):
                        novos_estados.update(self.afn.transicoes[estado][simbolo])
                
                novos_estados = frozenset(novos_estados)
                
                if novos_estados:
                    if novos_estados not in self.dfa['estados']:
                        self.dfa['estados'].add(novos_estados)
                        fila.append(novos_estados)

                    if estado_atual not in self.dfa['transicoes']:
                        self.dfa['transicoes'][estado_atual] = {}
                    
                    self.dfa['transicoes'][estado_atual][simbolo] = novos_estados

                    if novos_estados & self.afn.estados_finais:
                        self.dfa['estados_finais'].add(novos_estados)

    def imprimir_afd(self):
        print("AFD gerado:")
        print("Estados:", self.dfa['estados'])
        print("Alfabeto:", self.dfa['alfabeto'])
        print("Estado inicial:", self.dfa['estado_inicial'])
        print("Estados finais:", self.dfa['estados_finais'])
        print("Transições:")
        for estado_origem, transicoes in self.dfa['transicoes'].items():
            for simbolo, estado_destino in transicoes.items():
                print(f"  {estado_origem} --{simbolo}--> {estado_destino}")

    def aceita(self, palavra):
        estado_atual = self.dfa['estado_inicial']
        for simbolo in palavra:
            if simbolo not in self.dfa['transicoes'].get(estado_atual, {}):
                return False
            estado_atual = self.dfa['transicoes'][estado_atual][simbolo]
        return estado_atual in self.dfa['estados_finais']


class AFDMinimizado:
    def __init__(self, afd):
        # Verifica se afd é uma instância da classe AFD
        if isinstance(afd, AFD):
            self.afd = afd
        elif isinstance(afd, Automatos):
            # Se for uma instância de Automatos, converte para AFD
            self.afd = AFD(afd)
        else:
            raise TypeError("Esperado um objeto do tipo AFD ou Automatos.")

        self.minimizado = {
            'estados': set(),
            'alfabeto': self.afd.dfa['alfabeto'],
            'estado_inicial': None,
            'estados_finais': set(),
            'transicoes': {}
        }
        self.minimizar()

    def minimizar(self):
        P = {frozenset(self.afd.dfa['estados_finais']), 
             frozenset(self.afd.dfa['estados'] - self.afd.dfa['estados_finais'])}
        W = {frozenset(self.afd.dfa['estados_finais'])}

        while W:
            A = W.pop()
            for simbolo in self.afd.dfa['alfabeto']:
                X = frozenset({q for q in self.afd.dfa['estados'] 
                               if simbolo in self.afd.dfa['transicoes'].get(q, {}) 
                               and self.afd.dfa['transicoes'][q][simbolo] in A})
                novos_p = set()
                for Y in P:
                    intersecao = X & Y
                    diferenca = Y - X
                    if intersecao and diferenca:
                        novos_p.add(intersecao)
                        novos_p.add(diferenca)
                        if Y in W:
                            W.remove(Y)
                            W.add(intersecao)
                            W.add(diferenca)
                        else:
                            if len(intersecao) <= len(diferenca):
                                W.add(intersecao)
                            else:
                                W.add(diferenca)
                    else:
                        novos_p.add(Y)
                P = novos_p

        # Construção do AFD minimizado
        estado_map = {}
        for idx, grupo in enumerate(P):
            estado_map[grupo] = f"q{idx}"
            if self.afd.dfa['estado_inicial'] in grupo:
                self.minimizado['estado_inicial'] = f"q{idx}"
            if grupo & self.afd.dfa['estados_finais']:
                self.minimizado['estados_finais'].add(f"q{idx}")
            self.minimizado['estados'].add(f"q{idx}")

        for grupo in P:
            representante = next(iter(grupo))
            estado_origem_min = estado_map[grupo]
            if representante in self.afd.dfa['transicoes']:
                self.minimizado['transicoes'][estado_origem_min] = {}
                for simbolo, estado_destino in self.afd.dfa['transicoes'][representante].items():
                    for grp in P:
                        if estado_destino in grp:
                            estado_destino_min = estado_map[grp]
                            self.minimizado['transicoes'][estado_origem_min][simbolo] = estado_destino_min
                            break

    def imprimir_afd_minimizado(self):
        print("AFD Minimizado:")
        print("Estados:", self.minimizado['estados'])
        print("Alfabeto:", self.minimizado['alfabeto'])
        print("Estado inicial:", self.minimizado['estado_inicial'])
        print("Estados finais:", self.minimizado['estados_finais'])
        print("Transições:")
        for estado_origem, transicoes in self.minimizado['transicoes'].items():
            for simbolo, estado_destino in transicoes.items():
                print(f"  {estado_origem} --{simbolo}--> {estado_destino}")

    def aceita(self, palavra):
        estado_atual = self.minimizado['estado_inicial']
        for simbolo in palavra:
            if simbolo not in self.minimizado['transicoes'].get(estado_atual, {}):
                return False
            estado_atual = self.minimizado['transicoes'][estado_atual][simbolo]
        return estado_atual in self.minimizado['estados_finais']


def main():
    # Cria o automato
    automato = Automatos()

    # Inserção de estados
    while True:
        estado = input("Insira um estado (ou deixe vazio para terminar): ")
        if estado == "":
            break
        try:
            automato.adicionar_estado(estado)
        except ValueError as e:
            print(e)

    # Inserção do alfabeto
    while True:
        simbolo = input("Insira um símbolo do alfabeto (ou deixe vazio para terminar): ")
        if simbolo == "":
            break
        try:
            automato.adicionar_simbolo_alfabeto(simbolo)
        except ValueError as e:
            print(e)

    # Definição do estado inicial
    while True:
        estado_inicial = input("Insira o estado inicial: ")
        try:
            automato.definir_estado_inicial(estado_inicial)
            break
        except ValueError as e:
            print(e)

    # Definição dos estados finais
    while True:
        estado_final = input("Insira um estado final (ou deixe vazio para terminar): ")
        if estado_final == "":
            break
        try:
            automato.adicionar_estado_final(estado_final)
        except ValueError as e:
            print(e)

    # Inserção de transições
    while True:
        transicao = input("Insira uma transição no formato 'estado,símbolo,estados_destino' (ou deixe vazio para terminar): ")
        if transicao == "":
            break
        try:
            estado_origem, simbolo, estados_destino_str = transicao.split(',')
            estados_destino = set(estados_destino_str.split())
            automato.adicionar_transicao(estado_origem, simbolo, estados_destino)
        except ValueError as e:
            print(e)
        except Exception as e:
            print("Formato inválido. Use 'estado,símbolo,estados_destino'")

    automato.imprimir_automato()

    # Verificar se é determinístico
    if automato.eh_deterministico():
        print("O autômato é determinístico.")
        afd = automato
    else:
        print("O autômato é não determinístico. Convertendo para AFD...")
        afd = AFD(automato)  # Converte o AFN para AFD
        afd.imprimir_afd()

    # Minimizar o AFD
    print("Minimizando o AFD...")
    afd_minimizado = AFDMinimizado(afd)
    afd_minimizado.imprimir_afd_minimizado()

    # Teste de aceitação de palavras
    while True:
        palavra = input("Insira uma palavra para testar no automato (ou deixe vazio para terminar): ")
        if palavra == "":
            break

        # Testar a palavra no autômato original (AFN ou AFD)
        resultado_original = automato.aceita(palavra)
        print("Resultado no autômato original:")
        print("A palavra foi aceita." if resultado_original else "A palavra foi rejeitada.")

        # Testar a palavra no AFD convertido (se necessário e possível)
        if not automato.eh_deterministico():
            # Usar o objeto AFD que já foi criado na conversão
            resultado_convertido = afd.aceita(palavra)
            print("Resultado no AFD convertido:")
            print("A palavra foi aceita." if resultado_convertido else "A palavra foi rejeitada.")
        else:
            print("O autômato original já é um AFD.")

        # Testar a palavra no AFD minimizado
        resultado_minimizado = afd_minimizado.aceita(palavra)
        print("Resultado no AFD minimizado:")
        print("A palavra foi aceita." if resultado_minimizado else "A palavra foi rejeitada.")

if __name__ == "__main__":
    main()

