import streamlit as st
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('estoque.db')
c = conn.cursor()

# Criar a tabela de produtos se ainda não existir
c.execute('''CREATE TABLE IF NOT EXISTS produtos (
             id INTEGER PRIMARY KEY,
             data_compra DATE,
             nome TEXT,
             data_validade DATE,
             quantidade INTEGER
             )''')

# Função para adicionar um novo produto ao estoque
def adicionar_produto(data_compra, nome, data_validade, quantidade):
    c.execute("INSERT INTO produtos (data_compra, nome, data_validade, quantidade) VALUES (?, ?, ?, ?)",
              (data_compra, nome, data_validade, quantidade))
    conn.commit()
    st.success('Produto adicionado com sucesso!')

# Função para mostrar os produtos disponíveis
def mostrar_produtos():
    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()
    return produtos

# Função para selecionar os produtos para uma cesta
def selecionar_cesta(tipo_cesta):
    from datetime import datetime

def selecionar_cesta(tipo_cesta):
    # Defina os produtos disponíveis para cada tipo de cesta
    produtos_cesta_grande = [
        "Arroz", "Feijão", "Óleo", "Açúcar", "Café moído", "Sal", "Extrato de tomate", 
        "Vinagre", "Bolacha recheada", "Bolacha salgada", "Macarrão Espaguete", 
        "Macarrão parafuso", "Macarrão instantâneo", "Farinha de trigo", 
        "Farinha temperada", "Achocolatado em pó", "Leite", "Goiabada", "Suco em pó", 
        "Mistura pra bolo", "Tempero", "Sardinha", "Creme dental", "Papel higiênico", 
        "Sabonete"
    ]
    produtos_cesta_pequena = [
        "Arroz", "Feijão", "Óleo", "Açúcar", "Café moído", "Sal", "Extrato de tomate", 
        "Bolacha", "Macarrão", "Farinha de trigo", "Farinha temperada", "Goiabada", 
        "Suco em pó", "Sardinha", "Creme dental", "Papel higiênico", "Sabonete", 
        "Milharina", "Tempero"
    ]

    # Selecione os produtos com a data de validade mais próxima
    if tipo_cesta == "grande":
        produtos_disponiveis = produtos_cesta_grande
        numero_itens = 28
    elif tipo_cesta == "pequena":
        produtos_disponiveis = produtos_cesta_pequena
        numero_itens = 19

    c.execute("SELECT nome, data_validade, quantidade FROM produtos WHERE nome IN ({seq}) ORDER BY data_validade ASC"
              .format(seq=','.join(['?']*len(produtos_disponiveis))), produtos_disponiveis)
    produtos_selecionados = c.fetchall()

    # Montar a cesta com os produtos selecionados
    cesta = []
    for produto in produtos_selecionados:
        if numero_itens > 0:
            cesta.append(produto)
            numero_itens -= 1
        else:
            break

    return cesta

# Exemplo de como usar a função
cesta_grande = selecionar_cesta("grande")
print("Cesta Grande:")
print(cesta_grande)

cesta_pequena = selecionar_cesta("pequena")
print("Cesta Pequena:")
print(cesta_pequena)
    # Retorne os produtos selecionados
pass

# Função principal da aplicação
def main():
    st.title('Controle de Estoque - Empresa de Cesta Básica')

    # Barra lateral para adicionar produtos
    st.sidebar.title('Adicionar Produto')
    data_compra = st.sidebar.date_input('Data da Compra')
    nome = st.sidebar.text_input('Nome do Produto')
    data_validade = st.sidebar.date_input('Data de Validade')
    quantidade = st.sidebar.number_input('Quantidade', min_value=1)

    if st.sidebar.button('Adicionar'):
        adicionar_produto(data_compra, nome, data_validade, quantidade)

    # Mostrar os produtos disponíveis
    st.subheader('Produtos Disponíveis')
    produtos = mostrar_produtos()
    if produtos:
        for produto in produtos:
            st.write(produto)
    else:
        st.write('Nenhum produto disponível')
def main():
    st.title('Controle de Estoque - Empresa de Cesta Básica')

    # Barra lateral para adicionar produtos
produtos_disponiveis = [
    "Arroz", "Feijão", "Óleo", "Açúcar", "Café moído", "Sal", "Extrato de tomate", 
    "Vinagre", "Bolacha recheada", "Bolacha salgada", "Macarrão Espaguete", 
    "Macarrão parafuso", "Macarrão instantâneo", "Farinha de trigo", 
    "Farinha temperada", "Achocolatado em pó", "Leite", "Goiabada", "Suco em pó", 
    "Mistura pra bolo", "Tempero", "Sardinha", "Creme dental", "Papel higiênico", 
    "Sabonete", "Milharina"
]

def main():
    st.title('Controle de Estoque - Empresa de Cesta Básica')

    # Barra lateral para adicionar produtos
    st.sidebar.title('Adicionar Produto')
    data_compra = st.sidebar.date_input('Data da Compra')
    nome = st.sidebar.selectbox('Selecione o Produto:', produtos_disponiveis)
    data_validade = st.sidebar.date_input('Data de Validade')
    quantidade = st.sidebar.number_input('Quantidade', min_value=1)

    if st.sidebar.button('Adicionar'):
        adicionar_produto(data_compra, nome, data_validade, quantidade)

    # Mostrar os produtos disponíveis
    st.subheader('Produtos Disponíveis')
    produtos = mostrar_produtos()
    if produtos:
        for produto in produtos:
            st.write(produto)
    else:
        st.write('Nenhum produto disponível')

    # Barra lateral para selecionar uma cesta
    st.sidebar.subheader('Montar Cesta')
    tipo_cesta = st.sidebar.radio("Selecione o tipo de cesta:", ("Grande", "Pequena"))

    if st.sidebar.button('Montar Cesta'):
        produtos_cesta = selecionar_cesta(tipo_cesta)
        if produtos_cesta:
            st.subheader('Produtos para Cesta {}'.format(tipo_cesta))
            for produto in produtos_cesta:
                st.write(produto)
        else:
            st.write('Nenhum produto disponível para a cesta {}'.format(tipo_cesta))

    # Consultar o banco de dados para selecionar os produtos da cesta
    c.execute("SELECT nome, data_validade, quantidade FROM produtos WHERE nome IN ({seq}) ORDER BY data_validade ASC"
              .format(seq=','.join(['?']*len(produtos_disponiveis))), produtos_disponiveis)
    produtos_selecionados = c.fetchall()

    # Verificar se todos os itens da cesta estão disponíveis no estoque
    produtos_faltando = [item for item in produtos_disponiveis if item not in [produto[0] for produto in produtos_selecionados]]

    if produtos_faltando:
        st.warning("Os seguintes itens não foram encontrados no estoque: {}".format(", ".join(produtos_faltando)))

    # Atualizar o estoque subtraindo os produtos selecionados
    for produto in produtos_selecionados:
        if numero_itens > 0:
            nome_produto = produto[0]
            quantidade_produto = produto[2]
            c.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE nome = ? AND quantidade >= ?", (quantidade_produto, nome_produto, quantidade_produto))
            conn.commit()
            numero_itens -= 1
        else:
            break

    return produtos_selecionados

# Código para executar a aplicação
if __name__ == '__main__':
    main()