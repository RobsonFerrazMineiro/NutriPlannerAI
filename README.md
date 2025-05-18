# NutriPlanner AI 🥗

<!-- Badges das Tecnologias Utilizadas -->
<p align="left">
  <a href="https://www.python.org/" target="_blank">
    <img src="https://img.shields.io/badge/Python-0078D4?style=for-the-badge&logo=python&logoColor=FFD43B&labelColor=282C34&color=0078D4" alt="Python Badge" style="border-radius: 8px;"/>
  </a>
  <a href="https://streamlit.io/" target="_blank">
    <img src="https://img.shields.io/badge/Streamlit-FF2968?style=for-the-badge&logo=streamlit&logoColor=white&labelColor=282C34&color=FF2968" alt="Streamlit Badge" style="border-radius: 8px;"/>
  </a>
  <a href="https://ai.google.dev/" target="_blank">
    <img src="https://img.shields.io/badge/Gemini%20API-00CFFF?style=for-the-badge&logo=google&logoColor=white&labelColor=282C34&color=00CFFF" alt="Google Gemini Badge" style="border-radius: 8px;"/>
  </a>
  <a href="https://pypi.org/project/python-dotenv/" target="_blank">
    <img src="https://img.shields.io/badge/python--dotenv-33C481?style=for-the-badge&logo=python&logoColor=white&labelColor=282C34&color=33C481" alt="dotenv Badge" style="border-radius: 8px;"/>
  </a>
</p>

Seu Planejador de Cardápio Semanal Inteligente, desenvolvido com Streamlit e a API do Google Gemini.

**Acesse o NutriPlanner AI aqui:** [https://nutriplannerai.streamlit.app/](https://nutriplannerai.streamlit.app/)

## Screenshots da Aplicação

Aqui estão algumas visualizações do NutriPlanner AI em ação:

**Visualização Mobile (ou Detalhe dos Inputs)/Interface Principal (Desktop)**

<table>
  <tr>
<td><img src="assets/screenshot1.png" alt="Interface Mobile" width="250"></td>

<td><img src="assets/screenshot2.png" alt="Interface Desktop" width="1000"></td>

  </tr>
</table>

## Descrição

O NutriPlanner AI ajuda usuários a criar cardápios semanais personalizados com base em seus objetivos (alimentação saudável, perda de peso, controle de diabetes, etc.), preferências alimentares, restrições e ingredientes disponíveis em casa. Ele também pode fornecer uma lista de compras sugerida.

## Funcionalidades

- Planejamento de cardápio por dias ou semanas.
- Seleção de refeições a incluir.
- Consideração de objetivos de saúde, incluindo opções para diabéticos e hipertensos.
- Inputs para preferências, restrições e ingredientes já disponíveis.
- Geração de lista de compras sugerida.
- Histórico de cardápios gerados na sessão.
- Alertas sobre alimentos contraindicados (quando detectado pela IA).

## Como Configurar e Rodar Localmente

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/SEU_USUARIO/NutriPlannerAI.git
    cd NutriPlannerAI
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # No Windows (usando py launcher)
    py -m venv .venv
    .\.venv\Scripts\Activate.ps1

    # No Linux/macOS
    # python3 -m venv .venv
    # source .venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure sua API Key:**

    - Crie um arquivo chamado `.env` na raiz do projeto.
    - Adicione sua API Key do Google AI Studio (Gemini):
      ```
      GOOGLE_API_KEY="SUA_API_KEY_AQUI"
      ```

5.  **Execute a aplicação Streamlit:**
    ```bash
    streamlit run app.py
    ```

## Tecnologias Utilizadas

- Python
- Streamlit
- Google Generative AI (Gemini API)
- python-dotenv

## Desenvolvido para

Imersão IA da Alura (Edição 3 - Ano 2025)
