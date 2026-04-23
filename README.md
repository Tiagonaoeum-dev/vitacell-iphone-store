# 📱 VitaCell - iPhone Store

![Django](https://img.shields.io/badge/Django-6.0-green)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

------------------------------------------------------------------------

## 🎯 Sobre o Projeto

**VitaCell** é uma plataforma de e-commerce completa desenvolvida para a
venda de iPhones novos e usados.

O sistema foi projetado com uma interface elegante inspirada no design
da Apple, oferecendo uma experiência de compra fluida tanto para
clientes quanto para administradores.

Este projeto foi desenvolvido como parte de um portfólio para demonstrar
habilidades em desenvolvimento Fullstack com Django.

------------------------------------------------------------------------

## ✨ Funcionalidades

### 👥 Clientes

-   Loja virtual moderna
-   Página de detalhes
-   Compra simplificada
-   Controle de estoque em tempo real

### 🔐 Admin

-   Dashboard
-   CRUD completo
-   Controle de estoque
-   Gestão de vendas

### 🔌 API

-   CRUD completo via REST
-   Integração externa

------------------------------------------------------------------------

## 🛠️ Tecnologias

-   Django
-   Django REST Framework
-   SQLite
-   HTML, CSS, JS
-   Bootstrap
-   Pillow

------------------------------------------------------------------------

## 🚀 Execução

``` bash
git clone https://github.com/Tiagonaoeum-dev/vitacell-iphone-store.git
cd vitacell-iphone-store

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

------------------------------------------------------------------------

## 📁 Estrutura

    vitacell-iphone-store/
    ├── core/
    ├── static/
    ├── media/
    ├── manage.py
    └── README.md

------------------------------------------------------------------------

## 🔌 API

  Método   Endpoint
  -------- ---------------------
  GET      /api/produtos/
  POST     /api/produtos/
  PUT      /api/produtos/{id}/
  DELETE   /api/produtos/{id}/

------------------------------------------------------------------------

## 📝 Melhorias Futuras

-   Carrinho
-   Pagamentos
-   Avaliações
-   Deploy

------------------------------------------------------------------------

## 👤 Autor

Tiago Martins

------------------------------------------------------------------------

## 📄 Licença

MIT
