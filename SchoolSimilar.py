import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar, Style
import os
import time
import pandas as pd
import networkx as nx
import os

def gerar_edges(dados_para_conversao):
    edges = []
    for (index, item) in dados_para_conversao.iterrows():
        for index2, item2 in dados_para_conversao.iterrows():
            # 0 é o índice de código da escola
            if(item[0] != item2[0]):
                quantidade_de_associacoes = 0
                
                # 21 é o indice de combinações
                if(item[21] == item2[21]):
                    quantidade_de_associacoes = quantidade_de_associacoes+1

                # 9 é o indice de subgrupo
                if(item[9] == item2[9]):
                    quantidade_de_associacoes = quantidade_de_associacoes+1

                if(quantidade_de_associacoes > 0):
                    e = ((item[1]), (item2[1]), quantidade_de_associacoes)
                    edges.append(e)

    return edges

def gerar_atributos_de_rede(rede, arquivo_nome, urbano_ou_rural, pasta):
    
    global_efficiency = nx.global_efficiency(rede)
    local_efficiency = nx.local_efficiency(rede)
    modularity = nx.community.modularity(rede, nx.community.label_propagation_communities(rede))
    #fonte da densidade: networkx.org/documentation/stable/reference/generated/networkx.classes.function.density.html
    densidade = (2*len(rede.edges))/ (len(rede.nodes)*(len(rede.nodes)-1))
    assortativity = nx.degree_pearson_correlation_coefficient(rede)
    average_shortest_path = nx.average_shortest_path_length(rede)

    simrank_similarity = nx.simrank_similarity(rede)
    jaccard_coefficient = nx.jaccard_coefficient(rede)

    simrank_pd = pd.DataFrame(simrank_similarity)
    jaccard_coefficient_pd = pd.DataFrame(jaccard_coefficient)
    
    simrank_pd.melt()
    jaccard_coefficient_pd.melt()

    network_attributes = {
        'global_efficiency': global_efficiency,
        'local_efficiency': local_efficiency,
        'density': densidade,
        'modularity': modularity,
        'assortativity': assortativity,
        'average_shortest_path': average_shortest_path
    }

    network_attributes_df = pd.DataFrame(network_attributes.items())

    simrank_pd.to_csv(pasta+"/"+arquivo_nome[:-5]+" - "+urbano_ou_rural+" - SimRank.csv")
    jaccard_coefficient_pd.to_csv(pasta+"/"+arquivo_nome[:-5]+" - "+urbano_ou_rural+" - Jaccard.csv")
    network_attributes_df.to_csv(pasta+"/"+arquivo_nome[:-5]+" - "+urbano_ou_rural+".csv")
    

def gerar_graph(arquivo_nome,urbano_ou_rural, pasta):
    dados_para_conversao = pd.read_excel(pasta+"/"+arquivo_nome, engine="openpyxl", sheet_name=urbano_ou_rural)

    G = nx.Graph()
    for (index, item) in dados_para_conversao.iterrows():
        G.add_node(item[1], 
               Nome_da_Escola=item[1],
               Nome_do_Municipio=item[2],
               Nome_UF=item[3],
               Tipo_de_dependencia_administrativa=item[4],
               Tipo_de_Localizacao=item[5],
               Quantidade_de_alunos=item[6],
               INSE_Valor_Absoluto=item[7],
               INSE_Classificação=item[8],
               Subgrupo=item[9],
               Proficiencia_em_Matematica=item[10],
               Nivel_de_proficiência_em_Matematica=item[11],
               Proficiencia_em_Lingua_Portuguesa=item[12],
               Nivel_de_proficiencia_em_Lingua_Portuguesa=item[13],
               IDEB=item[14],
               Indicador_de_Rendimento=item[15],
               Taxa_de_Aprovacao=item[16],
               Taxa_de_Reprovacao=item[17],
               Taxa_de_Abandono=item[18],
               Projecao=item[19],
               Atingiu_ou_nao_a_projeção=item[20],
               Perfil=item[21]
    )
    edges = gerar_edges(dados_para_conversao)    
    G.add_weighted_edges_from(edges)

    gerar_atributos_de_rede(G, arquivo_nome,urbano_ou_rural, pasta)

    nx.write_graphml(G, pasta+"/"+arquivo_nome+" - "+urbano_ou_rural+".graphml", encoding='utf-8', prettyprint=True)
    
def processar_pasta(pasta):
    # Simulação do processo de processamento dos arquivos da pasta
    arquivos = os.listdir(pasta)
    files_xls = [f for f in arquivos if f[-4:] == 'xlsx']
    for idx, arquivo in enumerate(files_xls):
        # Simulação do processamento de um arquivo (1 segundo de espera)
        # gerar_graph(arquivo, "Urbana", pasta)
        gerar_graph(arquivo, "Rural", pasta)
        # Atualizar a barra de progresso
        progresso.set((idx + 1) * 100 / len(files_xls))
        root.update()
    # Exibir mensagem de conclusão ao finalizar o processamento
    label_concluido.config(text="Concluído!")

def procurar_pasta():
    pasta_escolhida = filedialog.askdirectory()
    if pasta_escolhida:
        # Ocultar a mensagem de conclusão antes de iniciar o processamento
        label_concluido.config(text="")
        label_carregando.config(text="Carregando...")
        processar_pasta(pasta_escolhida)
        # Exibir a mensagem de conclusão após finalizar o processamento
        label_carregando.config(text="")
        label_concluido.config(text="Concluído!")

# Configuração da janela principal
root = tk.Tk()
root.title("Interface para Processar Pasta")
root.geometry("800x300")  # Define o tamanho da janela (dobro do tamanho original)
root.resizable(False, False)  # Impede que o usuário redimensione a janela

# Configuração do degradê de fundo (dark blue to black)
style = Style()
style.configure("TFrame", background="linear-gradient(135, #1A237E, black)")  # Configura o fundo da janela
root.configure(bg="blue")  # Define a cor de fundo da janela principal (backup caso o degradê não funcione)

# Variável para controlar o progresso da barra de progresso
progresso = tk.DoubleVar()
progresso.set(0)  # Define o valor inicial da barra de progresso

# Barra de progresso
style.configure("Horizontal.TProgressbar", background='green')  # Altera a cor da barra de progresso
progress_bar = Progressbar(root, variable=progresso, style="Horizontal.TProgressbar", maximum=100, length=600)
progress_bar.pack(pady=20)

# Label "Carregando..."
label_carregando = tk.Label(root, text="Carregando...", font=("Helvetica", 20), foreground="white", background="blue")
label_carregando.pack()

# Label "Concluído!"
label_concluido = tk.Label(root, text="", font=("Helvetica", 20), foreground="white", background="blue")
label_concluido.pack()

# Botão "Procurar Pasta"
botao_procurar = tk.Button(root, text="Procurar Pasta", command=procurar_pasta, font=("Helvetica", 16), relief=tk.RIDGE, width=20)
botao_procurar.pack(pady=20)

# Iniciar a interface
root.mainloop()
