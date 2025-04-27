# Django RESTful API

Este repositório contém uma **API RESTful** construída com **Django 4.x** e **Django REST Framework**, fornecendo autenticação JWT, confirmação de e-mail, login via Google, CRUD de itens públicos/privados, documentação Swagger e endpoints para servir Termos de Uso e Política de Privacidade em PDF.

## 🛠️ Tecnologias e Dependências

- Python 3.11+
- Django 4.x
- Django REST Framework
- Django REST Framework - Simple JWT
- drf-yasg (Swagger e Redoc)
- PostgreSQL (psycopg2-binary) e Supabase
- Google Auth (Autenticação com o Google e OAuth2)


## 🚀 Como rodar localmente

1. **Clone** o repositório:
   ```bash
    git clone https://github.com/SEU_USUARIO/seu-repo.git
    cd seu-repo
    ```

2. **Crie** e ative um ambiente virtual:
    ```bash
    python -m venv venv

    # Linux/macOS
    source .venv/bin/activate   

    # Windows
    .\venv\Scripts\activate      
    ```

3. **Instale** as dependências:
   ```bash
    pip install -r requirements.txt
    ```

4. **Configure** variáveis de ambiente **(arquivo `.env` na raiz)**:
    ```bash
    # Configurações Django
    SECRET_KEY=
    DEBUG=False
    API_BASE_URL=

    # Configurações Email
    EMAIL_HOST_USER=
    EMAIL_HOST_PASSWORD=

    # Configurações OAuth2
    GOOGLE_OAUTH2_CLIENT_ID=
    GOOGLE_OAUTH2_CLIENT_SECRET=

    # Banco de Dados - Link Supabase Postgres
    DATABASE_URL=

    # Blob Vercel
    BLOB_READ_WRITE_TOKEN=
    ```

5. **Execute** migrações e crie usuário admin:
   ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```

6. **Execute** o seed para popular o sistema com usuários e itens de exemplo:

    ```bash
    python manage.py seed
    ```
    Este comando:
    - Cria 5 usuários de teste, sendo 2 deles com e-mail confirmado.
    - Cria alguns itens variados (públicos e privados) associados a esses usuários.

    Usuários Criados no Seed

    | Username    | Senha         | E-mail confirmado? |
    |:------------|:--------------|:-------------------|
    | demo_user_1 | password123    | ✅ |
    | demo_user_2 | password123    | ✅ |
    | demo_user_3 | password123    | ❌ |
    | demo_user_4 | password123    | ❌ |
    | demo_user_5 | password123    | ❌ |

7. **Inicie** o servidor de desenvolvimento:
   ```bash
    python manage.py runserver
    ```

Acesse o ambiente de Desenvolvimento:  
- **Swagger UI:** http://localhost:8000/swagger/  
- **Admin:** http://localhost:8000/admin/

## 📑 Documentação

- **Swagger UI** interativo em `/swagger/` (Teste todos os endpoints). 
- **OpenAPI JSON** em `/swagger/?format=openapi`.
- **Redoc** `/redoc/` (Organização de todos os endpoints). 


## 📖 Endpoints Principais

### Autenticação

| Método | Rota | Descrição |
|-------:|------|-----------|
| POST   | `/api/auth/register/` | Registrar novo usuário (username, email, senha, foto) |
| POST   | `/api/auth/login/` | Login padrão, retorna JWT (6 h) |
| POST   | `/api/auth/logout/` | Logout, revoga JTI do token atual |
| PATCH  | `/api/auth/change-password/` | Altera senha (envia `old_password` e `new_password`) |

### Confirmação de E-mail

| Método | Rota | Descrição |
|-------:|------|-----------|
| GET    | `/api/auth/email/send-token/` | Envia token de confirmação para o e-mail do usuário |
| GET    | `/api/auth/email/verify-token/?email=&token=` | Valida token e marca `email_confirmed = true` |

### Login Social (Google)

| Método | Rota | Descrição |
|-------:|------|-----------|
| POST   | `/api/auth/google/` | Recebe `{ id_token }` do Google e retorna JWT |

### Perfil de Usuário

| Método | Rota | Descrição |
|-------:|------|-----------|
| GET    | `/api/users/me/` | Retorna dados do usuário autenticado |
| PATCH  | `/api/users/me/` | Atualiza nome, foto, etc |

### Itens

| Método | Rota | Descrição |
|-------:|------|-----------|
| GET    | `/api/items/` | Lista itens públicos com paginação, busca, filtro e ordenação |
| GET    | `/api/items/restricted/` | Mesma listagem, mas só para usuários com e‑mail confirmado |

### Termos de Uso e Política de Privacidade (PDF)

| Método | Rota | Descrição |
|-------:|------|-----------|
| GET    | `/api/docs/terms/` | Retorna **Termos de Uso** em PDF |
| GET    | `/api/docs/privacy/` | Retorna **Política de Privacidade** em PDF |


## ⚙️ Testes e Qualidade

- Execução dos testes unitários/integrados:
  ```bash
    python manage.py test --pattern="test_*.py"
  ```




## 📝 License

Este projeto está licenciado sob a [MIT License](LICENSE).
