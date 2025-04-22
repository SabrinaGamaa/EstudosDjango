# FireBlog (Django 5 + HTMX)
> Um mini‑blog moderno com posts, comentários, respostas e likes em tempo real.

---

## ✨ Visão geral
FireBlog demonstra:

* Autenticação social com **django‑allauth**  
* Relacionamentos avançados (`ForeignKey`, `ManyToMany`, signals)  
* Atualizações assíncronas via **HTMX** (likes/curtidas sem reload)  
* Padrões DRY – decorators genéricos, partials e template inheritance  
* Pronto para deploy Render/Heroku + Docker  

---

## 📸 Screenshots
| Home | Página de Post | Onboarding de Perfil |
|------|----------------|----------------------|
| ![home](static/readme/home.png) | ![post](static/readme/post.png) | ![onboarding](static/readme/onboarding.png) |

---

## ⚙️ Funcionalidades
| Módulo | Descrição |
|--------|-----------|
| **Usuário** | Cadastro, login social, perfil com avatar (upload ou fallback SVG). Onboarding obrigatório pós‑signup. |
| **Post** | CRUD completo, categorias por tag na URL (`/category/<tag>/`). |
| **Comentário & Reply** | Thread 2 níveis – comentários em posts e respostas a comentários. |
| **Likes** | Toggle em **Posts**, **Comments** e **Replies** via HTMX; contagem e ícone atualizam instantaneamente. |
| **Admin** | Painel Django customizado para moderação rápida. |

---

## 🔧 Stack & dependências
| Tech | Versão | Uso |
|------|--------|-----|
| **Python** | 3.13 | Linguagem |
| **Django** | 5.2 | Backend MVC |
| **django‑allauth** | 0.61 | Auth & social login |
| **HTMX** | 1.9 | AJAX simplificado |
| **Tailwind CSS** | 3.x | Estilização |
| **SQLite** | Dev DB (swap fácil para PostgreSQL) |

---

## 🚀 Instalação local
```bash
git clone https://github.com/<seu‑usuario>/fireblog.git
cd fireblog
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Acesse **http://127.0.0.1:8000** ・ Admin: **/admin/**

---

## 🖥️ Estrutura
```
a_core/            # settings + urls
a_posts/           # Post, Comment, Reply models
a_users/           # perfil, signals, forms
templates/
 ├─ base.html
 ├─ a_posts/
 ├─ a_users/
 └─ snippets/      # partials HTMX (likes, etc.)
static/
```

---

## 📝 Roadmap
- [ ] Paginação infinita com HTMX  
- [ ] Notificações em tempo real (Django Channels)  
- [ ] Pesquisa full‑text (Postgres + Trigram)  
- [ ] Testes automatizados (Pytest + Factory Boy)

---

## 🤝 Contribuição
1. **Fork** → branch `feature/nome`  
2. `git commit -m "feat: descrição curta"`  
3. Pull Request  

---

## 📜 Licença
MIT © 2025 Sabrina Gama  

> *Feito com ☕, ❤️ e uma pitada de HTMX!*

