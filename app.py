import streamlit as st
from tinydb import TinyDB, where

# Inicializa o banco de dados e cria as duas tabelas
db = TinyDB("loja.json")
estoque = db.table("estoque")
vendas = db.table("vendas")

st.title("🛒 Sistema de Loja Simples")

aba_estoque, aba_cadastrar, aba_vender, aba_vendas = st.tabs(
    ["📦 Estoque", "➕ Cadastrar", "🛒 Vender", "📊 Vendas"]
)

with aba_estoque:
    st.header("Estoque Atual")
    produtos = estoque.all()
    if produtos:
        st.table(produtos)
    else:
        st.info("Nenhum produto cadastrado.")

with aba_cadastrar:
    st.header("Cadastrar Produto")

    nome = st.text_input("Nome do Produto:", key="cad_nome")
    preco = st.number_input("Preço (R$):", min_value=0.01, step=0.5, key="cad_preco")
    qtd = st.number_input("Quantidade Inicial:", min_value=1, step=1, key="cad_qtd")

    if st.button("Salvar Produto", key="btn_cadastrar"):
        if not nome.strip():
            st.error("O nome do produto não pode ficar vazio!")
        else:
            estoque.insert({
                "nome": nome.strip(),
                "preco": float(preco),
                "quantidade": int(qtd)
            })
            st.success(f"Produto '{nome}' cadastrado com sucesso!")

with aba_vender:
    st.header("Realizar Venda")
    produtos = estoque.all()

    if len(produtos) == 0:
        st.info("Sem produtos cadastrados para vender")
    else:
        nomes = [p["nome"] for p in produtos if p["quantidade"] > 0]

        if len(nomes) == 0:
            st.warning("Tudo zerado! Cadastre produtos no estoque antes de vender")
        else:
            prod_escolhido = st.selectbox("Produto", nomes, key="v_prod")
            produto = estoque.get(where("nome") == prod_escolhido)

            qtd_v = st.number_input(
                "Quantidade",
                min_value=1,
                max_value=int(produto["quantidade"]),
                step=1,
                key="v_qtd",
            )
            cliente = st.text_input("Cliente", key="v_cli")

            total = produto["preco"] * qtd_v
            st.write(f"Total: R$ {total:.2f}")

            if st.button("Confirmar venda", type="primary", key="btn_vender"):
                vendas.insert({
                    "produto": prod_escolhido,
                    "quantidade": int(qtd_v),
                    "total": float(total),
                    "cliente": cliente,
                })
                estoque.update(
                    {"quantidade": produto["quantidade"] - int(qtd_v)},
                    where("nome") == prod_escolhido,
                )
                st.success("Venda registrada!")
                st.balloons()

with aba_vendas:
    st.header("Histórico de vendas")
    lista = vendas.all()

    if len(lista) == 0:
        st.info("Sem vendas ainda")
    else:
        st.table(lista)




