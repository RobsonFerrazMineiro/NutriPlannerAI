# app.py
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

st.set_page_config(page_title="NutriPlanner AI", page_icon="🥗", layout="wide")

load_dotenv()

# Configurar a API Key do Google
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Chave da API do Google não encontrada. Verifique seu arquivo .env.")
        st.stop() # Impede a execução do restante do script se a chave não for encontrada
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Erro ao configurar a API do Google: {e}")
    st.stop()

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 0,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Inicializar o modelo
try:
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
except Exception as e:
    st.error(f"Erro ao inicializar o modelo Generativo: {e}")
    st.stop()

if 'historico_cardapios' not in st.session_state:
    st.session_state.historico_cardapios = []

if 'tipo_planejamento' not in st.session_state:
    st.session_state.tipo_planejamento = "Dias"


st.title("🥗 NutriPlanner AI: Seu Planejador de Cardápio Inteligente")
st.markdown("Preencha os campos abaixo para gerar um cardápio semanal personalizado!")


# Colunas para melhor organização dos inputs
col1, col2 = st.columns(2)

with col1:
    tipo_planejamento = st.radio(
        "Planejar por:",
        ("Dias", "Semanas/Meses"),
        index=0, # Padrão: Dias
        horizontal=True,
        key="tipo_planejamento" # Adicionar uma chave para referenciar o estado
    )

    if st.session_state.tipo_planejamento == "Dias":
        dias_semana = st.number_input(
            "Para quantos dias você quer o cardápio?",
            min_value=1, max_value=30, value=3, step=1, # Aumentei o max_value para dias, caso queira até 1 mês
            help="Defina o número de dias para o planejamento (1 a 30)."
        )
        periodo_texto = f"{dias_semana} dias"
    else: # Semanas/Meses
        # Desabilitar o input de dias quando meses é selecionado
        dias_semana_placeholder = st.empty() # Criar um placeholder
        with dias_semana_placeholder:
            st.number_input(
                "Para quantos dias você quer o cardápio?",
                min_value=1, max_value=7, value=7, step=1,
                help="Defina o número de dias para o planejamento (1 a 7).",
                disabled=True # Desabilitado
            )

        num_semanas = st.number_input(
            "Para quantas semanas você quer o cardápio?",
            min_value=1, max_value=12, value=1, step=1, # Ex: até 3 meses (12 semanas)
            help="Defina o número de semanas para o planejamento (1 a 12)."
        )
        dias_semana = num_semanas * 7 # Calcular o total de dias para o prompt
        periodo_texto = f"{num_semanas} semana(s)"
        if num_semanas >=4:
            meses_aprox = round(num_semanas / 4)
            periodo_texto = f"aproximadamente {meses_aprox} mês(es) ({num_semanas} semanas)"
            
    refeicoes_opcoes = ["Café da Manhã", "Lanche da Manhã", "Almoço", "Lanche da Tarde", "Jantar", "Ceia"]
    refeicoes_selecionadas = st.multiselect(
        "Quais refeições incluir?",
        refeicoes_opcoes,
        default=["Café da Manhã", "Almoço", "Jantar"],
        help="Selecione as refeições que deseja planejar."
    )
    objetivo = st.selectbox(
        "Qual seu objetivo principal com o cardápio?",
        [
            "Alimentação Saudável Geral",
            "Perda de Peso (Déficit Calórico Leve)",
            "Ganho de Massa Muscular (Superávit Calórico Leve)",
            "Praticidade e Rapidez no Preparo",
            "Economia (Ingredientes Acessíveis)",
            "Vegetariano/Vegano",
            "Baixo Carboidrato (Low Carb)",
            "Controle da Diabetes (Índice Glicêmico Baixo/Moderado)",
            "Controle da Hipertensão (Baixo Sódio)" 
        ],
        index=0, # Padrão: Alimentação Saudável Geral
        help="Escolha o foco principal do seu plano alimentar."
    )

with col2:
    preferencias = st.text_area(
        "Preferências alimentares e alimentos que você GOSTA:",
        placeholder="Ex: adoro peixe e frango, prefiro vegetais cozidos, gosto de frutas cítricas...",
        height=100,
        help="Liste alimentos ou tipos de pratos que você aprecia."
    )
    restricoes = st.text_area(
        "Restrições, alergias ou alimentos que você NÃO GOSTA/NÃO PODE COMER:",
        placeholder="Ex: sem glúten, intolerância à lactose, alergia a amendoim, não como carne vermelha...",
        height=100,
        help="Importante para personalizar seu cardápio e evitar ingredientes indesejados."
    )
    ingredientes_casa = st.text_area(
        "Ingredientes que você já tem em casa e gostaria de usar (opcional):",
        placeholder="Ex: arroz, feijão, batata, ovos, uma caixa de tomates...",
        height=100,
        help="Ajuda a IA a sugerir receitas que aproveitem o que você já tem."
    )

# Botão para gerar o cardápio
if st.button("✨ Gerar Meu Cardápio Inteligente!", use_container_width=True):
    if not dias_semana or not refeicoes_selecionadas:
        st.warning("Por favor, preencha pelo menos o número de dias e as refeições desejadas.")
    else:
        # Montar o prompt para a IA
        prompt_partes = [
            "Você é um nutricionista e chef de cozinha virtual especializado em criar cardápios semanais personalizados, chamado NutriPlanner AI.",
            f"Por favor, crie um plano de refeições detalhado para {dias_semana} dias, incluindo as seguintes refeições: {', '.join(refeicoes_selecionadas)}.",
            f"O objetivo principal do usuário é: {objetivo}.",
            f"Preferências alimentares (alimentos que gosta): {preferencias if preferencias else 'Nenhuma específica, mas priorize variedade e sabor.'}.",
            f"Restrições, alergias ou alimentos a evitar: {restricoes if restricoes else 'Nenhuma específica.'}.",
            f"Ingredientes que o usuário já tem em casa e gostaria de aproveitar (se possível): {ingredientes_casa if ingredientes_casa else 'Nenhum específico, utilize ingredientes comuns e acessíveis.'}.",
            "\nO cardápio deve ser:",
            "- Balanceado, nutritivo e saboroso.",
            "- Variado, evitando repetições excessivas de pratos principais nos mesmos dias ou dias seguidos, a menos que seja prático (ex: sobras para o almoço do dia seguinte).",
            "- Com sugestões de pratos e preparações que sejam relativamente fáceis ou de complexidade média, adequados para o dia a dia.",
            "- Para cada refeição, sugira o prato principal e, se aplicável, acompanhamentos ou complementos.",
            "- Se o objetivo for perda de peso ou ganho de massa, tente adequar as sugestões, mas sem prescrever calorias exatas (apenas direcione para alimentos mais leves ou mais proteicos, conforme o caso).",
            "\nApresente o cardápio de forma clara e organizada, dia por dia e refeição por refeição. Use markdown para formatação (negrito para dias e refeições).",
            "Exemplo de formato para cada dia:",
            "**Dia 1:**",
            f"  - **{refeicoes_selecionadas[0] if len(refeicoes_selecionadas) > 0 else 'Refeição 1'}**: [Sugestão detalhada do prato]",
            f"  - **{refeicoes_selecionadas[1] if len(refeicoes_selecionadas) > 1 else 'Refeição 2'}**: [Sugestão detalhada do prato]",
            "  ...",
            "\nAo final do cardápio, adicione uma seção chamada '**Lista de Compras Sugerida:**'",
            "Nesta seção, liste os principais ingredientes frescos e chave (vegetais, frutas, proteínas, laticínios/alternativas) necessários para preparar as refeições do cardápio gerado.",
            "Não precisa listar temperos básicos como sal, pimenta, azeite, a menos que seja algo muito específico.",
            "Organize a lista de compras por categorias (Ex: Vegetais, Frutas, Proteínas, Grãos/Carboidratos, Laticínios/Outros) para facilitar.",
            "O tom deve ser amigável, encorajador e profissional."
        ]

        condicoes_especiais_prompt = []
        if objetivo == "Controle da Diabetes (Índice Glicêmico Baixo/Moderado)":
            condicoes_especiais_prompt.append(
                "Foco em alimentos de baixo a moderado índice glicêmico, ricos em fibras. Evitar açúcares simples e carboidratos refinados em excesso."
            )
        if objetivo == "Controle da Hipertensão (Baixo Sódio)":
            condicoes_especiais_prompt.append(
                "Priorizar alimentos com baixo teor de sódio. Evitar alimentos processados, embutidos e enlatados com alto sódio. Incentivar o uso de temperos naturais."
            )

        if condicoes_especiais_prompt:
            prompt_partes.append("\nConsiderações Especiais de Saúde (baseadas no objetivo):")
            prompt_partes.extend(condicoes_especiais_prompt)

        prompt_partes.append(
            "\nIMPORTANTE: Se o usuário listar preferências alimentares que são claramente contraindicadas para o objetivo de saúde selecionado (ex: doces para diabéticos, alimentos salgados para hipertensos), o cardápio NÃO deve incluir esses alimentos. Em vez disso, após gerar o cardápio adequado, adicione uma seção de ALERTA ao final, explicando de forma amigável por que certos alimentos preferidos não foram incluídos e sugerindo alternativas saudáveis se possível."
        )
        prompt_completo = "\n".join(prompt_partes)

        st.markdown("---")
        st.subheader("⏳ Gerando seu cardápio...")
        st.caption("Lembre-se: O NutriPlanner AI oferece sugestões e não substitui o aconselhamento de um nutricionista ou médico. Consulte um profissional para orientações personalizadas.")
        #st.info(f"**Debug do Prompt (para você, desenvolvedor):**\n```\n{prompt_completo}\n```") # Linha de debug, remova ou comente depois

        try:
            with st.spinner("O NutriPlanner AI está pensando no seu cardápio... Aguarde um instante! 🧑‍🍳"):
                response = model.generate_content(prompt_completo)

            texto_resposta = response.text
            alerta_inicio = texto_resposta.upper().find("ALERTA:")

            if alerta_inicio != -1:
                cardapio_texto = texto_resposta[:alerta_inicio].strip()
                alerta_texto = texto_resposta[alerta_inicio:].strip()

                st.markdown("---")
                st.subheader("📅 Seu Cardápio Personalizado by NutriPlanner AI:")
                st.markdown(cardapio_texto)

                st.markdown("---")
                st.warning(alerta_texto)
            else:
                st.markdown("---")
                st.subheader("📅 Seu Cardápio Personalizado by NutriPlanner AI:")
                st.markdown(texto_resposta)

            # Salvar no histórico de cardápios
            interacao_atual = {
                "inputs": {
                    "periodo": periodo_texto,
                    "refeicoes": refeicoes_selecionadas,
                    "objetivo": objetivo,
                    "preferencias": preferencias,
                    "restricoes": restricoes,
                    "ingredientes_casa": ingredientes_casa
                },
                "cardapio_gerado": texto_resposta
            }
            st.session_state.historico_cardapios.append(interacao_atual)

        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar o cardápio: {e}")
            st.error("Por favor, tente refinar seus inputs ou tente novamente mais tarde.")

st.markdown("---")
st.subheader("📜 Histórico de Cardápios Gerados")

if not st.session_state.historico_cardapios:
    st.caption("Nenhum cardápio gerado nesta sessão ainda.")
else:
    # Mostrar o histórico em ordem reversa (mais recente primeiro)
    for i, interacao in enumerate(reversed(st.session_state.historico_cardapios)):
        with st.expander(f"Cardápio {len(st.session_state.historico_cardapios) - i} (Objetivo: {interacao['inputs']['objetivo']} para {interacao['inputs']['periodo']})"):
            st.markdown("**Preferências e Restrições Informadas:**")
            st.json({key: val for key, val in interacao['inputs'].items() if key not in ['periodo', 'refeicoes', 'objetivo']}) # Mostrar outros inputs
            st.markdown("**Cardápio Gerado:**")
            st.markdown(interacao['cardapio_gerado'])

st.markdown("---")
st.caption("NutriPlanner AI - Desenvolvido para a Imersão IA da Alura.")