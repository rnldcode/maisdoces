# O QUE FAZ: importa as dependências necessárias para o funcionamento da API
# ONDE APARECE: no início do arquivo main.py
# QUANDO ATUA: durante a inicialização da aplicação
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
import os

# O QUE FAZ: cria a instância da aplicação FastAPI com título e descrição
# ONDE APARECE: logo após as importações
# QUANDO ATUA: durante a inicialização da aplicação
app = FastAPI(title="Mai's Doces API", description="API para gerenciamento de produtos da Mai's Doces")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "123456")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "maisdoces-admin-token")

# O QUE FAZ: configura o middleware CORS para permitir requisições de qualquer origem
# ONDE APARECE: após a criação da instância FastAPI
# QUANDO ATUA: durante cada requisição HTTP para habilitar cross-origin requests
# OBSERVAÇÃO: usar ["*"] é adequado apenas para desenvolvimento, em produção deve ser mais restrito
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (para desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# O QUE FAZ: define o modelo de dados para os produtos usando Pydantic
# ONDE APARECE: após a configuração CORS
# QUANDO ATUA: durante a validação dos dados nas requisições HTTP
# OBSERVAÇÃO: Pydantic valida automaticamente os tipos e campos obrigatórios
class Product(BaseModel):
    id: Optional[str] = None  # ID opcional, será gerado automaticamente se não fornecido
    title: str               # Título do produto (obrigatório)
    description: str         # Descrição do produto (obrigatório)
    price: str              # Preço do produto (obrigatório)
    image: str              # URL da imagem do produto (obrigatório)
    image_class: str = "dish-image-donuts"  # Classe CSS para estilização (padrão)
    rating: int = 5         # Avaliação do produto (padrão: 5 estrelas)
    rating_count: int = 500 # Número de avaliações (padrão: 500)


class AdminLogin(BaseModel):
    username: str
    password: str


def require_admin(authorization: str = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Não autorizado")
    token = authorization.replace("Bearer ", "", 1)
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")

# O QUE FAZ: define o caminho do arquivo de banco de dados JSON
# ONDE APARECE: após a definição do modelo Product
# QUANDO ATUA: durante todo o ciclo de vida da aplicação
# OBSERVAÇÃO: o arquivo products_db.json serve como banco de dados temporário
DB_FILE = "products_db.json"

# O QUE FAZ: carrega os produtos do arquivo JSON ao iniciar a aplicação
# ONDE APARECE: após a definição do caminho do banco de dados
# QUANDO ATUA: durante a inicialização da aplicação
# OBSERVAÇÃO: se o arquivo não existir, cria um com dados iniciais
def load_products():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Dados iniciais caso o arquivo não exista
        initial_products = [
            {
                "id": "1",
                "title": "Donuts artesanais",
                "description": "Massa leve e cobertura especial.",
                "price": "R$25,00",
                "image": "src/images/donutscolorido.png",
                "image_class": "dish-image-donuts",
                "rating": 5,
                "rating_count": 500
            },
            {
                "id": "2", 
                "title": "Bolo decorado",
                "description": "Perfeito para festas e datas especiais.",
                "price": "R$175,00 / kg",
                "image": "src/images/bolodecorado.png",
                "image_class": "dish-image-donuts",
                "rating": 5,
                "rating_count": 500
            },
            {
                "id": "3",
                "title": "Combo de doces",
                "description": "Seleção dos doces mais pedidos da casa.",
                "price": "R$20,00",
                "image": "src/images/combodonuts.png",
                "image_class": "dish-image-donuts",
                "rating": 5,
                "rating_count": 500
            }
        ]
        save_products(initial_products)
        return initial_products

# O QUE FAZ: salva os produtos no arquivo JSON
# ONDE APARECE: após a função de carregamento
# QUANDO ATUA: sempre que um produto é criado, atualizado ou deletado
# OBSERVAÇÃO: sobrescreve o arquivo com os dados atualizados
def save_products(products):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

# O QUE FAZ: armazena os produtos em memória (lista Python)
# ONDE APARECE: após as funções de persistência
# QUANDO ATUA: durante todo o ciclo de vida da aplicação
# OBSERVAÇÃO: os dados são carregados do arquivo JSON e mantidos em memória para performance
products_db = load_products()

# O QUE FAZ: endpoint raiz da API - mensagem de boas-vindas
# ONDE APARECE: primeiro endpoint definido
# QUANDO ATUA: quando acessado http://localhost:8000/
@app.get("/")
async def root():
    return {"message": "Bem-vindo à Mais Doces API"}

# O QUE FAZ: endpoint GET para listar todos os produtos
# ONDE APARECE: após o endpoint raiz
# QUANDO ATUA: quando acessado http://localhost:8000/api/products
@app.get("/api/products", response_model=List[Product])
async def get_products():
    """Retorna todos os produtos cadastrados"""
    return products_db


@app.post("/api/admin/login")
async def admin_login(credentials: AdminLogin):
    if credentials.username == ADMIN_USERNAME and credentials.password == ADMIN_PASSWORD:
        return {
            "access_token": ADMIN_TOKEN,
            "token_type": "bearer"
        }
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

# O QUE FAZ: endpoint GET para obter um produto específico pelo ID
# ONDE APARECE: após o endpoint de listagem
# QUANDO ATUA: quando acessado http://localhost:8000/api/products/{id}
@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Retorna um produto específico pelo ID"""
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

# O QUE FAZ: endpoint POST para criar um novo produto
# ONDE APARECE: após os endpoints GET
# QUANDO ATUA: quando enviado POST para http://localhost:8000/api/products
@app.post("/api/products", response_model=Product)
async def create_product(product: Product, authorization: str = Header(default=None)):
    """Cadastra um novo produto"""
    require_admin(authorization)
    # Gera um ID único se não for fornecido
    if not product.id:
        product.id = str(uuid.uuid4())
    
    # Converte o modelo Pydantic para dicionário
    product_dict = product.dict()
    
    # Adiciona o produto ao banco de dados em memória
    products_db.append(product_dict)
    
    # Salva os produtos no arquivo JSON para persistência
    save_products(products_db)
    
    return product_dict

# O QUE FAZ: endpoint PUT para atualizar um produto existente
# ONDE APARECE: após o endpoint POST
# QUANDO ATUA: quando enviado PUT para http://localhost:8000/api/products/{id}
@app.put("/api/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product: Product, authorization: str = Header(default=None)):
    """Atualiza um produto existente"""
    require_admin(authorization)
    # Encontra o índice do produto
    index = next((i for i, p in enumerate(products_db) if p["id"] == product_id), None)
    
    if index is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Atualiza o produto
    product_dict = product.dict()
    product_dict["id"] = product_id  # Garante que o ID permanece o mesmo
    products_db[index] = product_dict
    
    # Salva os produtos no arquivo JSON para persistência
    save_products(products_db)
    
    return product_dict

# O QUE FAZ: endpoint DELETE para remover um produto
# ONDE APARECE: após o endpoint PUT
# QUANDO ATUA: quando enviado DELETE para http://localhost:8000/api/products/{id}
@app.delete("/api/products/{product_id}")
async def delete_product(product_id: str, authorization: str = Header(default=None)):
    """Remove um produto"""
    require_admin(authorization)
    global products_db
    product = next((p for p in products_db if p["id"] == product_id), None)
    
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    products_db = [p for p in products_db if p["id"] != product_id]
    
    # Salva os produtos no arquivo JSON para persistência
    save_products(products_db)
    
    return {"message": "Produto removido com sucesso"}

# O QUE FAZ: ponto de entrada da aplicação - inicia o servidor Uvicorn
# ONDE APARECE: no final do arquivo
# QUANDO ATUA: quando o arquivo é executado diretamente (python main.py)
# OBSERVAÇÃO: host="0.0.0.0" permite acesso externo, port=8000 é a porta padrão
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
