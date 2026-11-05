---
name: netapp-rag
description: Consulta a base de conhecimento local do NetApp Net2 Offline Client (bancos sqlite, manuais PDF, Action Plans e Job Aids) para validar e responder questões técnicas de suporte e exames ASE-2.
---

# NetApp RAG Skill

Esta skill permite consultar diretamente a base de dados local do **Net2 Offline Client** instalada no computador (`%APPDATA%\net2offlineclient`).

## Capacidades

- Consulta a árvore de navegação e menus do Net2 (`toc.sqlite`).
- Pesquisa nos mais de 11.000 documentos catalogados (`documents.sqlite`).
- Busca e extração de trechos em tempo real dentro dos 2.500+ PDFs de manuais da NetApp (`documents/`).
- Inspeção de planos de ação interativos (`scripts/*.zip`).
- Registro automático de questões e respostas no histórico de estudos.

## Como Executar Consultas

Para pesquisar no catálogo do Net2:
```bash
python "<caminho_do_script>/netapp_rag.py" "termo de busca"
```
