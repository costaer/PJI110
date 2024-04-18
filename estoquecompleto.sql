--tabela de Produtos--
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);
select * from produtos

INSERT INTO produtos (nome)
VALUES ('');


--tabela de cestas--
CREATE TABLE cestas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

select * from cestas
DROP TABLE IF EXISTS cestas;
ALTER TABLE cestas
ADD CONSTRAINT nome_unico UNIQUE (nome);

INSERT INTO cestas (nome)
VALUES ('Cesta 2');

--tabela cestas de produtos--
CREATE TABLE produtos_cestas (
    id SERIAL PRIMARY KEY,
    id_produto INTEGER NOT NULL,
    id_cesta INTEGER NOT NULL,
    FOREIGN KEY (id_produto) REFERENCES produtos(id),
    FOREIGN KEY (id_cesta) REFERENCES cestas(id),
    CONSTRAINT unique_produto_cesta UNIQUE (id_produto, id_cesta)
);

select * from produtos_cestas

INSERT INTO produtos_cestas (id_produto, id_cesta)
VALUES ('5', '1');


--tabela de entrada de mercadorias--
CREATE TABLE entrada_mercadorias (
    id SERIAL PRIMARY KEY,
    id_produto INTEGER NOT NULL,
    data_compra DATE NOT NULL,
    data_validade DATE NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (id_produto) REFERENCES produtos(id)
);

select * from entrada_mercadorias
DELETE FROM entrada_mercadorias
WHERE id = 8;
UPDATE entrada_mercadorias AS e
SET quantidade = CASE
                    WHEN e.quantidade > qtd_vendida THEN e.quantidade - qtd_vendida
                    ELSE 0
                 END
FROM (
    SELECT em.id_produto, COALESCE(SUM(sm.quantidade_cestas), 0) AS qtd_vendida
    FROM entrada_mercadorias AS em
    LEFT JOIN (
        SELECT pc.id_produto, COALESCE(SUM(s.quantidade_cestas), 0) AS quantidade_cestas
        FROM produtos_cestas AS pc
        JOIN cestas AS c ON pc.id_cesta = c.id
        JOIN saida_mercadorias AS s ON c.nome = s.tipo_cesta
        GROUP BY pc.id_produto
    ) AS sm ON em.id_produto = sm.id_produto
    GROUP BY em.id_produto
) AS vendas
WHERE e.id_produto = vendas.id_produto;

INSERT INTO entrada_mercadorias (id_produto, data_compra, data_validade, quantidade)
VALUES ('1', '2024-04-08', '2025-12-01', '10');


--tabela saida de mercadorias--
CREATE TABLE saida_mercadorias (
    id SERIAL PRIMARY KEY,
    quantidade_cestas INTEGER NOT NULL, 
    tipo_cesta VARCHAR(20) NOT NULL, 
    data_venda DATE NOT NULL,
    FOREIGN KEY (tipo_cesta) REFERENCES cestas(nome)
);

select * from saida_mercadorias
DROP TABLE IF EXISTS saida_mercadorias;

INSERT INTO saida_mercadorias (quantidade_cestas, tipo_cesta, data_venda )
VALUES ('1', 'Cesta 1', '202-04-08');