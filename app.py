import streamlit as st
import sqlite3
from datetime import datetime

# Criar conexão com o banco de dados
conn = sqlite3.connect('estoque.db')
c = conn.cursor()

# Criar tabela se não existir
c.execute('''CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                data_compra DATE,
                data_validade DATE,
                quantidade INTEGER
            )''')

# Lista de produtos disponíveis
opcoes_produtos = ['Arroz', 'Feijão', 'Óleo', 'Açúcar', 'Café moído', 'Sal', 'Extrato de tomate',
                   'Vinagre', 'Bolacha recheada', 'Bolacha salgada', 'Macarrão Espaguete',
                   'Macarrão parafuso', 'Macarrão instantâneo', 'Farinha de trigo', 'Farinha temperada',
                   'Achocolatado em pó', 'Leite', 'Goiabada', 'Suco em pó', 'Mistura pra bolo', 'Tempero',
                   'Sardinha', 'Creme dental', 'Papel higiênico', 'Sabonete', 'Milharina']


# Função para adicionar produto ao estoque
def adicionar_produto(nome, data_compra, data_validade, quantidade):
    c.execute('''INSERT INTO produtos (nome, data_compra, data_validade, quantidade)
                  VALUES (?, ?, ?, ?)''', (nome, data_compra, data_validade, quantidade))
    conn.commit()

# Função para buscar todos os produtos ordenados por nome
def buscar_produtos():
    c.execute('''SELECT * FROM produtos ORDER BY nome''')
    return c.fetchall()

# Função para buscar produtos por nome
def buscar_produto_por_nome(nome):
    c.execute('''SELECT * FROM produtos WHERE nome = ?''', (nome,))
    return c.fetchall()

# Função para atualizar quantidade do produto no estoque
def atualizar_quantidade_produto(id_produto, nova_quantidade):
    c.execute('''UPDATE produtos SET quantidade = ? WHERE id = ?''', (nova_quantidade, id_produto))
    conn.commit()

# Função para montar a cesta
def montar_cesta(cesta):
    itens_cesta = []
    for item in cesta:
        produtos = buscar_produto_por_nome(item)
        for produto in produtos:
            itens_cesta.append(produto)
            nova_quantidade = produto[4] - 1
            atualizar_quantidade_produto(produto[0], nova_quantidade)
    return itens_cesta

# Função para calcular a diferença de dias entre duas datas
def diferenca_dias(data1, data2):
    data1 = datetime.strptime(data1, "%Y-%m-%d")
    data2 = datetime.strptime(data2, "%Y-%m-%d")
    return abs((data2 - data1).days)

# Função para selecionar produtos mais próximos da validade
def selecionar_proximos_validade(produtos, quantidade):
    produtos_ordenados = sorted(produtos, key=lambda x: x[3])
    return produtos_ordenados[:quantidade]

# Interface do Streamlit
st.title('Controle de Estoque de Cesta Básica')

# Barra lateral para cadastrar produtos
st.sidebar.header('Cadastrar Produto')
nome_produto = st.sidebar.selectbox('Nome do Produto', opcoes_produtos)
data_compra = st.sidebar.date_input('Data da Compra')
data_validade = st.sidebar.date_input('Data de Validade')
quantidade = st.sidebar.number_input('Quantidade', min_value=1, value=1)
adicionar = st.sidebar.button('Adicionar Produto')

if adicionar:
    adicionar_produto(nome_produto, data_compra, data_validade, quantidade)
    st.sidebar.success('Produto adicionado com sucesso!')

# Barra lateral para selecionar cesta
st.sidebar.header('Montar Cesta')
opcoes_cesta = ['Pequena (19 itens)', 'Grande (28 itens)']
tipo_cesta = st.sidebar.selectbox('Selecione o tipo de cesta:', opcoes_cesta)
montar = st.sidebar.button('Montar Cesta')

if montar:
    if tipo_cesta == 'Pequena (19 itens)':
        cesta = ['Arroz', 'Feijão', 'Óleo', 'Açúcar', 'Café moído', 'Sal', 'Extrato de tomate', 'Bolacha',
                 'Macarrão', 'Farinha de trigo', 'Farinha temperada', 'Goiabada', 'Suco em pó', 'Sardinha',
                 'Creme dental', 'Papel higiênico', 'Sabonete', 'Milharina', 'Tempero']
    else:
        cesta = ['Arroz', 'Feijão', 'Óleo', 'Açúcar', 'Café moído', 'Sal', 'Extrato de tomate', 'Vinagre',
                 'Bolacha recheada', 'Bolacha salgada', 'Macarrão Espaguete', 'Macarrão parafuso',
                 'Macarrão instantâneo', 'Farinha de trigo', 'Farinha temperada', 'Achocolatado em pó', 'Leite',
                 'Goiabada', 'Suco em pó', 'Mistura pra bolo', 'Tempero', 'Sardinha', 'Creme dental',
                 'Papel higiênico', 'Sabonete']
    
    # Buscar produtos disponíveis
    produtos_disponiveis = buscar_produtos()
    
    # Selecionar produtos mais próximos da validade
    produtos_para_cesta = selecionar_proximos_validade(produtos_disponiveis, len(cesta))
    
    # Montar a cesta
    itens_cesta = montar_cesta(cesta)
    
    # Exibir os itens da cesta
    st.subheader('Itens da Cesta:')
    for item in itens_cesta:
        st.write(f'{item[4]} x {item[1]} - Compra: {item[2]} - Validade: {item[3]}')

# Exibir estoque
st.header('Estoque:')
produtos_estoque = buscar_produtos()
for produto in produtos_estoque:
    st.write(f'{produto[4]} x {produto[1]} - Compra: {produto[2]} - Validade: {produto[3]}')

# Fechar conexão com o banco de dados
conn.close()
