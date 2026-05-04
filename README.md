# Mais Doces

## PT-BR

### Sobre o projeto
O **Mais Doces** é uma aplicação web para vitrine e cadastro de produtos de confeitaria.

- O frontend exibe o catálogo e a interface de navegação.
- O backend fornece uma API para listar, cadastrar, atualizar e remover produtos.
- Os dados são persistidos em arquivo JSON para facilitar uso local.

### Tecnologias utilizadas
- **Frontend:** HTML5, CSS3, JavaScript, jQuery
- **Backend:** Python, FastAPI, Uvicorn, Pydantic
- **Persistência:** JSON (`products_db.json`)

### Como rodar o backend
1. Abra um terminal na pasta `maisdoces-api`.
2. (Opcional) Crie e ative um ambiente virtual.
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a API:

```bash
python main.py
```

API disponível em: `http://localhost:8000`  
Endpoint principal de produtos: `http://localhost:8000/api/products`

### Como rodar o frontend
1. Abra o arquivo `maisdoces-front/index.html` no navegador.
2. Para melhor compatibilidade com chamadas da API, recomenda-se servir a pasta com um servidor local (exemplo com Python):

```bash
python -m http.server 5500
```

Depois, acesse: `http://localhost:5500/maisdoces-front/index.html`

---

## EN

### About the project
**Mais Doces** is a web application for showcasing and registering confectionery products.

- The frontend displays the catalog and navigation interface.
- The backend provides an API to list, create, update, and delete products.
- Data is persisted in a JSON file for simple local usage.

### Technologies used
- **Frontend:** HTML5, CSS3, JavaScript, jQuery
- **Backend:** Python, FastAPI, Uvicorn, Pydantic
- **Persistence:** JSON (`products_db.json`)

### How to run the backend
1. Open a terminal in the `maisdoces-api` folder.
2. (Optional) Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the API:

```bash
python main.py
```

API URL: `http://localhost:8000`  
Main products endpoint: `http://localhost:8000/api/products`

### How to run the frontend
1. Open `maisdoces-front/index.html` in your browser.
2. For better API-call compatibility, it is recommended to serve the folder with a local server (example using Python):

```bash
python -m http.server 5500
```

Then access: `http://localhost:5500/maisdoces-front/index.html`

