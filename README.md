# 🥗 NutriStream: Planejador de Dieta (Padrão MVC)

O **NutriStream** é uma aplicação web de alta performance para planejamento nutricional. O projeto utiliza a base científica **TACO** para cálculos precisos de macronutrientes, permitindo que o usuário gerencie sua dieta com base em dados oficiais brasileiros.

Este projeto foi desenhado seguindo o padrão **MVC (Model-View-Controller)** para garantir separação de responsabilidades, facilitando a manutenção e os testes automatizados, preparando o ambiente para um cenário real de desenvolvimento em estágio.

---

## 🏗️ Arquitetura e Estrutura de Diretórios

A aplicação segue uma estrutura modular para separar a interface (Streamlit) da lógica de negócio e do acesso aos dados.


```text
nutristream/
├── data/                   # Bases de dados (TACO CSV, JSON de usuários)
├── src/
│   ├── models/             # MODEL: Classes de dados (Alimento, Usuario, Dieta)
│   ├── controllers/        # CONTROLLER: Orquestração entre View e Model
│   ├── services/           # SERVICES: Lógica externa (Leitura de CSV, Cálculos TMB)
│   └── views/              # VIEW: Componentes de interface do Streamlit
├── app.py                  # Ponto de entrada (Main)
├── requirements.txt        # Dependências
└── README.md
```

---

## Componentes do MVC:

- Model: Define a estrutura dos dados. Ex: A classe Alimento garante que cada item tenha nome, proteína, carbo e gordura.

- View: Arquivos .py que contêm apenas st.title, st.sidebar, etc. Elas não fazem cálculos, apenas chamam o Controller.

- Controller: Faz a "ponte". Ele recebe o clique do botão da View, pede ao Service para calcular o TMB e devolve o resultado para a View exibir.

---

## 🛠️ Tecnologias Principais

- Python 3.10+

- Streamlit: Framework para interface web.

- Pandas: Manipulação e filtragem da base TACO.

- Base TACO: Fonte oficial de dados nutricionais.

--- 

## 📌 Funcionalidades por Módulos (Abas)

- 📊 Perfil & Metas: Cálculo de TMB (Harris-Benedict) e definição de macros alvo.

- 🍎 Biblioteca TACO: Busca filtrada na base de dados e cadastro de novos alimentos/receitas.

- 📝 Diário Alimentar: Montagem do cardápio e visualização do balanço de macros vs. meta diária.