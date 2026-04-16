import streamlit as st

# ==============================================
# FUNÇÃO DE FORMATAÇÃO (BR)
# ==============================================

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ==============================================
# FUNÇÕES DE CUSTO
# ==============================================

def mo_retirada(cat):
    return {
        30: 1023.17,
        80: 1151,
        120: 1278.97,
        180: 1278.97
    }.get(cat, 0)


def mo_instalacao(cat):
    return {
        80: 6020.61,
        120: 7129.66,
        180: 8070.83
    }.get(cat, 0)


def material_instalacao(cat):
    return {
        80: 27386.28,
        120: 34268.51,
        180: 48494.16
    }.get(cat, 0)


# ==============================================
# BASE SIGFI
# ==============================================

BASE_SIGFI = {
    30: "PU",
    80: "PU",
    120: "PC",
    180: "PC"
}


# ==============================================
# CÁLCULO
# ==============================================

def calcular_orcamento(tipo_solicitacao, sigfi_atual, sigfi_pedido):

    if tipo_solicitacao == "Ligação Nova":
        return "SEM CUSTO AO CLIENTE", None, None, None, None

    if sigfi_pedido not in BASE_SIGFI:
        return "ERRO: SIGFI inválido", None, None, None, None

    tipo_projeto = BASE_SIGFI[sigfi_pedido]

    if tipo_projeto == "PU":
        return "SEM CUSTO AO CLIENTE", None, None, None, None

    mo_ret = mo_retirada(sigfi_atual)
    mo_inst = mo_instalacao(sigfi_pedido)
    material = material_instalacao(sigfi_pedido)
    total = mo_ret + mo_inst + material

    return "COM CUSTO AO CLIENTE", mo_ret, mo_inst, material, total


# ==============================================
# INTERFACE WEB
# ==============================================

st.set_page_config(page_title="Orçamento SIGFI", layout="centered")

st.title("Calculadora de Orçamento SIGFI")

tipo = st.radio(
    "Tipo de solicitação",
    ["Ligação Nova", "Alteração de carga"]
)

sigfi_atual = st.selectbox(
    "SIGFI atual",
    [30, 80, 120, 180]
)

sigfi_pedido = st.selectbox(
    "SIGFI pedido",
    [80, 120, 180]
)

if st.button("Calcular"):

    status, mo_ret, mo_inst, material, total = calcular_orcamento(
        tipo, sigfi_atual, sigfi_pedido
    )

    st.subheader("Resultado")

    if "ERRO" in status:
        st.error(status)
    else:
        st.write("Status:", status)

        if total is not None:
            st.write(f"Mão de obra retirada: {formatar_moeda(mo_ret)}")
            st.write(f"Mão de obra instalação: {formatar_moeda(mo_inst)}")
            st.write(f"Material: {formatar_moeda(material)}")
            st.success(f"TOTAL: {formatar_moeda(total)}")
        else:
            st.info("Sem custo ao cliente.")
