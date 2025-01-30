# Sistema de Gerenciamento de Notas com IA

Este é um sistema de gerenciamento de notas que utiliza Inteligência Artificial para melhorar a organização e classificação das anotações do usuário. O sistema possui um backend robusto em Django, um frontend moderno em React e um banco de dados PostgreSQL.

## 🚀 Recursos Principais
- **Autenticação de Usuários**: Cada usuário pode acessar e gerenciar suas próprias notas de forma segura.
- **Classificação com IA**: Utiliza modelos de NLP para categorizar automaticamente as notas com base no conteúdo.
- **Busca Avançada**: Pesquisa notas por palavras-chave e contexto utilizando algoritmos de IA.
- **Interface Intuitiva**: Um design responsivo e amigável para melhorar a experiência do usuário.
- **Sincronização em Nuvem**: As notas podem ser acessadas de qualquer lugar com sincronização automática.

## 🛠️ Tecnologias Utilizadas
- **Backend**: Django (Python)
- **Banco de Dados**: PostgreSQL
- **Frontend**: React.js
- **IA**: Modelos de NLP (Natural Language Processing) com TensorFlow/PyTorch
- **Autenticação**: JWT

## 📥 Instalação e Execução

### 1️⃣ Clone o repositório
```sh
    git clone https://github.com/seu-usuario/sistema-notas-ia.git
    cd sistema-notas-ia
```

### 2️⃣ Configure o Backend
#### Crie um ambiente virtual e instale as dependências:
```sh
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate  # Windows
    pip install -r requirements.txt
```

#### Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto e adicione:
```env
    SECRET_KEY=suachave
    DATABASE_URL=postgresql://usuario:senha@localhost:5432/notasdb
    AI_API_KEY=sua_chave_de_ia
```

#### Execute as migrações do banco de dados:
```sh
    python manage.py migrate
```

#### Inicie o servidor backend:
```sh
    python manage.py runserver
```

### 3️⃣ Configure o Frontend
#### Instale as dependências e inicie o React:
```sh
    cd frontend
    npm install
    npm start
```

## ✅ Testes
Para rodar os testes, utilize:
```sh
    python manage.py test  # Para o backend
    cd frontend && npm test  # Para o frontend
```

## 📜 Contribuição
Fique à vontade para contribuir! Para isso:
1. Faça um fork do repositório
2. Crie uma branch (`git checkout -b feature-nova`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature-nova`)
5. Abra um Pull Request

## 📄 Licença
Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Feito com ❤️ por [Seu Nome](https://github.com/Ingleson10).

