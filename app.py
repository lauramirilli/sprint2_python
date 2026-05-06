from deep_translator import GoogleTranslator
import pyperclip


# DADOS GLOBAIS (simulação da base de dados em listas)
 
# Biblioteca de materiais digitalizados
# Estrutura: [id, titulo, materia, tipo, conteudo_texto, idioma]
materiais = [
    [1, "Brasil Colônia", "História", "lousa",
     "Período Pré-Colonial, O Governo Geral, A formação social do Brasil Colônia, A crise do sistema colonial.",
     "Português"],
    [2, "Filosofia Grega", "Filosofia", "slide",
     "Período Pré-Socrático, Período Clássico, Período Helenístico.",
     "Português"],
    [3, "Números complexos", "Matemática", "caderno",
     "Forma algébrica de um número complexo, Operações com números complexos, Plano de Argand-Gauss.",
     "Português"],
]
 
# Histórico de traduções realizadas na sessão
historico_traducoes = []
 
# Contador de ID para novos materiais
proximo_id = 4
 
# Matérias disponíveis para organização
MATERIAS_DISPONIVEIS = [
    "Matemática", "Física", "Química", "História", "Geografia", "Filosofia", "Outro"
]
 
# Tipos de material reconhecidos pelo modo Estudo
TIPOS_MATERIAL = ["lousa", "slide", "caderno"]
 
 
# UTILITÁRIOS
 
def linha(char="─", tam=58):
    """Imprime linha separadora."""
    print(char * tam)


def titulo(texto, subtexto=""):
    """Imprime cabeçalho de seção."""
    linha("═")
    print(f"  {texto}")
    if subtexto:
        print(f"  {subtexto}")
    linha("═")


def pausar():
    """Aguarda o usuário antes de voltar ao menu."""
    input("\n  ↩  Pressione ENTER para voltar ao menu...")


def input_validado(msg, tipo="str", opcoes=None, min_val=None, max_val=None):
    """
    Lê e valida entrada do usuário.
    Suporta validação de tipo inteiro, lista de opções e faixa numérica.
    """
    while True:
        entrada = input(msg).strip()
 
        if not entrada:
            print("  !!  Campo obrigatório. Tente novamente.")
            continue
 
        if tipo == "int":
            if not entrada.lstrip("-").isdigit():
                print("  !!  Digite apenas números inteiros.")
                continue
            valor = int(entrada)
            if min_val is not None and valor < min_val:
                print(f"  !!  Valor mínimo: {min_val}.")
                continue
            if max_val is not None and valor > max_val:
                print(f"  !!  Valor máximo: {max_val}.")
                continue
            return valor
 
        if opcoes:
            # Aceita número ou texto da opção
            if entrada.lower() not in [str(opcao).lower() for opcao in opcoes]:
                print(f"  !!  Opções válidas: {', '.join([str(opcao) for opcao in opcoes])}.")
                continue
 
        return entrada


def buscar_material_por_id(id_busca):
    """Retorna o material com o ID informado, ou None se não encontrado."""
    for material in materiais:
        if material[0] == id_busca:
            return material
    return None
 

# FUNCIONALIDADE 1 (Digitalizar Foto de Aula)
 
def digitalizar_foto():
    """
    Simula a digitalização de um material fotográfico (lousa, slide,
    caderno). O usuário informa o tipo de material, a matéria e o
    conteúdo capturado. O sistema organiza e salva na biblioteca.
 
    Regra de negócio: o material é salvo com matéria, tipo e título
    definidos pelo estudante, tornando-o pesquisável depois.
    """
    global proximo_id
 
    titulo("📷  DIGITALIZAR FOTO DE AULA",
           "Registre o conteúdo capturado pela câmera")
 
    print("\n  Tipo de material fotografado:\n")
    for i, tipo in enumerate(TIPOS_MATERIAL, 1):
        print(f"  [{i}] {tipo.capitalize()}")
 
    print()
    escolha_tipo = input_validado(
        "  ➤ Tipo do material (número): ",
        tipo="int", min_val=1, max_val=len(TIPOS_MATERIAL)
    )
    tipo_material = TIPOS_MATERIAL[escolha_tipo - 1]
 
    # Título do material
    titulo_mat = input_validado(
        f"\n  Título para este {tipo_material} (ex: 'Aula 03'): "
    )
 
    # Seleção de matéria
    print("\n  Matérias disponíveis:\n")
    for i, materia in enumerate(MATERIAS_DISPONIVEIS, 1):
        print(f"  [{i}] {materia}")
 
    escolha_mat = input_validado(
        "\n  ➤ Matéria (número): ",
        tipo="int", min_val=1, max_val=len(MATERIAS_DISPONIVEIS)
    )
    materia = MATERIAS_DISPONIVEIS[escolha_mat - 1]
 
    # Conteúdo extraído (simula o OCR/texto digitalizado)
    print(f"\n  Cole ou digite o texto extraído da foto ({tipo_material}):")
    print("  (Em uma versão real, o Google Lens extrairia automaticamente da imagem)\n")
    conteudo = input_validado("  Conteúdo: ")
 
    # Salva na biblioteca
    novo_material = [proximo_id, titulo_mat, materia, tipo_material, conteudo, "Português"]
    materiais.append(novo_material)
    proximo_id += 1
 
    linha()
    print(f"\n Material digitalizado com sucesso!")
    print(f"\n ID       : {novo_material[0]}")
    print(f" Matéria  : {materia}")
    print(f" Tipo     : {tipo_material.capitalize()}")
    print(f" Título   : {titulo_mat}")
    print(f"\n Conteúdo salvo ({len(conteudo)} caracteres).")
    linha()
 
    pausar()
 

# FUNCIONALIDADE 2 (Copiar Conteúdo da Foto)
def copiar_conteudo():
    """
    Simula a função de copiar o conteúdo diretamente de
    imagens capturadas, facilitando o uso e reaproveitamento do conteúdo.
    """
    titulo("COPIAR CONTEÚDO")
    exibir_lista_materiais(materiais)
    id_mat = input_validado(
        "\n  ➤ Selecione o ID do material que deseja copiar o conteúdo: ",
        tipo="int", min_val=1
    )
    material = buscar_material_por_id(id_mat)
    if not material:
        print(f"\n  !!  Material ID {id_mat} não encontrado.")
        pausar()
        return
    
    texto = material[4]
    pyperclip.copy(texto)
    conteudo = pyperclip.paste()
    print(f"Conteúdo copiado: {conteudo}")
    
    pausar()

# FUNCIONALIDADE 2 (Biblioteca de Materiais)
 
def minha_biblioteca():
    """
    Exibe, busca e lê os materiais digitalizados pelo estudante.
    Resolve a dor principal: fotos perdidas na galeria misturadas
    com selfies, aqui tudo fica organizado por matéria e tipo.
    """
    titulo("MINHA BIBLIOTECA",
           "Seus materiais de estudo organizados")
 
    if not materiais:
        print("\n    Biblioteca vazia. Digitalize uma foto primeiro.\n")
        pausar()
        return
 
    print("\n  [1] Ver todos os materiais")
    print("  [2] Filtrar por matéria")
    print("  [3] Buscar por palavra-chave")
    print("  [4] Ler conteúdo de um material")
    print("  [5] Resumo de um material")
    print()
 
    opc = input_validado("  ➤ Opção: ", opcoes=["1", "2", "3", "4", "5"])
 
    # Ver todos
    if opc == "1":
        exibir_lista_materiais(materiais)
 
    # Filtrar por matéria
    elif opc == "2":
        print("\n  Matérias disponíveis na biblioteca:\n")
        # Coleta matérias únicas dos materiais salvos
        materias_salvas = list({material[2] for material in materiais})
        for i, material in enumerate(materias_salvas, 1):
            print(f"  [{i}] {material}")
 
        escolha = input_validado(
            "\n  ➤ Número da matéria: ",
            tipo="int", min_val=1, max_val=len(materias_salvas)
        )
        materia_filtro = materias_salvas[escolha - 1]
        filtrados = [material for material in materiais if material[2] == materia_filtro]
        print(f"\n  Materiais de '{materia_filtro}':")
        exibir_lista_materiais(filtrados)
 
    # Buscar por palavra-chave
    elif opc == "3":
        termo = input_validado("\n  Palavra-chave para busca: ").lower()
        encontrados = [
            material for material in materiais
            if termo in material[1].lower() or termo in material[4].lower()
        ]
        if encontrados:
            print(f"\n  {len(encontrados)} resultado(s) para '{termo}':")
            exibir_lista_materiais(encontrados)
        else:
            print(f"\n    Nenhum material encontrado com '{termo}'.")
 
    # Ler conteúdo
    elif opc == "4":
        exibir_lista_materiais(materiais)
        id_leitura = input_validado(
            "\n  ➤ ID do material para ler: ",
            tipo="int", min_val=1
        )
        material = buscar_material_por_id(id_leitura)
        if material:
            linha()
            print(f"\n    {material[1]}")
            print(f"    {material[2]}  |  {material[3].capitalize()}  |  {material[5]}")
            linha("-")
            print(f"\n  {material[4]}\n")
            linha()
        else:
            print(f"\n  !!  Material ID {id_leitura} não encontrado.")

    elif opc == "5":
        print("Para esse protótipo estão disponivéis apenas os resumos dos conteúdos de exemplo!")
        exibir_lista_materiais(materiais[:3])
        id_leitura = input_validado(
            "\n  ➤ ID do material para resumir: ",
            tipo="int", min_val=1
        )
        material = buscar_material_por_id(id_leitura)
        
        if material[0] == 1:
            print("    Brasil Colônia: Período de exploração por Portugal (1500–1822), " \
            "baseado na extração de recursos e trabalho escravizado.")

        elif material[0] == 2:
            print("    Filosofia grega: Busca racional por explicações sobre o mundo, o conhecimento e a ética, " \
            "com pensadores como Sócrates, Platão e Aristóteles.")

        elif material[0] == 3:
            print("    Números complexos: Conjunto numérico que inclui a unidade imaginária (i), " \
            "permitindo representar raízes de números negativos.")

 
    pausar()
 
 
def exibir_lista_materiais(lista):
    """Função auxiliar para exibir tabela de materiais."""
    linha("-")
    print(f"  {'ID':<5} {'TÍTULO':<32} {'MATÉRIA':<22} {'TIPO'}")
    linha("-")
    for m in lista:
        print(f"  {m[0]:<5} {m[1][:31]:<32} {m[2][:21]:<22} {m[3].capitalize()}")
    linha("-")
    print(f"  Total: {len(lista)} material(is).")
 

#  FUNCIONALIDADE 3 (Traduzir Conteúdo)
 
def traduzir_conteudo():
    """
    Simula a tradução de texto extraído de uma foto ou de material
    já salvo na biblioteca. Suporta Português → Inglês (simulado).
 
    Regra de negócio: tradução preserva o contexto acadêmico;
    o resultado é salvo no histórico de traduções da sessão e
    pode ser exportado como novo material.
    """
    titulo("TRADUZIR CONTEÚDO",
           "Português → Inglês  |  +50 idiomas na versão completa")
 
    print("\n  Fonte do texto:\n")
    print("  [1] Digitar texto manualmente")
    print("  [2] Traduzir material da biblioteca")
    print()
 
    fonte = input_validado("  ➤ Opção: ", opcoes=["1", "2"])
 
    texto_original = ""
    origem_titulo = "Texto avulso"
 
    if fonte == "1":
        print("\n  Digite o texto em Português para traduzir:\n")
        texto_original = input_validado("  Texto: ")
 
    elif fonte == "2":
        if not materiais:
            print("\n  !!  Biblioteca vazia. Digitalize um material primeiro.")
            pausar()
            return
        exibir_lista_materiais(materiais)
        id_mat = input_validado(
            "\n  ➤ ID do material: ",
            tipo="int", min_val=1
        )
        material = buscar_material_por_id(id_mat)
        if not material:
            print(f"\n  !!  Material ID {id_mat} não encontrado.")
            pausar()
            return
        texto_original = material[4]
        origem_titulo = material[1]

    texto_traduzido = GoogleTranslator(source='pt', target='en').translate(texto_original)
 
    # Exibe resultado
    linha()
    print(f"\n ORIGINAL:\n  {texto_original}\n")
    linha("-")
    print(f"\n TRADUÇÃO (EN):\n  {texto_traduzido}\n")
    linha()
 
    # Salva no histórico
    registro = {
        "origem": origem_titulo,
        "original": texto_original[:60] + ("..." if len(texto_original) > 60 else ""),
        "traduzido": texto_traduzido[:60] + ("..." if len(texto_traduzido) > 60 else ""),
    }
    historico_traducoes.append(registro)
    print(f"    Tradução salva no histórico ({len(historico_traducoes)} total).")
 
    # Opção de salvar como novo material
    print("\n  Deseja salvar a tradução como novo material na biblioteca?")
    salvar = input_validado("  (s/n): ", opcoes=["s", "n", "S", "N"])
 
    if salvar.lower() == "s":
        global proximo_id
        novo = [
            proximo_id,
            f"[EN] {origem_titulo}",
            "Tradução",
            "documento",
            texto_traduzido,
            "English"
        ]
        materiais.append(novo)
        proximo_id += 1
        print(f"    Salvo na biblioteca com ID {novo[0]}.")
 
    pausar()


#  MENU PRINCIPAL
 
def exibir_menu():
    """Renderiza o menu principal com estatísticas da sessão."""
    titulo("📸  JOVI Study Lens",
           "Transforme imagens em conhecimento")
    print(f"  Biblioteca: {len(materiais)} material(is)  |  "
          f"Traduções: {len(historico_traducoes)}\n")
    print("  [1] Digitalizar")
    print("  [2] Copiar")
    print("  [3] Traduzir")
    print("  [4] Biblioteca de Conteúdos")
    print("  [0] Sair")
    linha()
 
 
def main():
    """Ponto de entrada, loop principal do programa."""
    print("\n" + "═" * 58)
    print("  JOVI Study Lens  📸  Transforme imagens em conhecimento")
    print("  Challenge FIAP 2026 | Sprint 2 | Python")
    print("═" * 58)
    print("\n  Bem-vindo! 3 materiais de exemplo já estão na biblioteca.")
 
    while True:
        print()
        exibir_menu()
 
        opcao = input_validado(
            "  ➤ Escolha uma opção: ",
            tipo="int", min_val=0, max_val=5
        )
 
        match opcao:
            case 1:
                digitalizar_foto()
            case 2:
                copiar_conteudo()
            case 3:
                traduzir_conteudo()
            case 4:
                minha_biblioteca()
            case 0:
                linha("═")
                print("  Até logo! Continue transformando fotos em aprendizado. 📸")
                linha("═")
                break
 
 
#  PONTO DE ENTRADA

if __name__ == "__main__":
    main()