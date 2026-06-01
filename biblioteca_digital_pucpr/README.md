# Sistema de Gerenciamento de Biblioteca Digital

Projeto desenvolvido para a disciplina **Programacao para Ciencia de Dados - PUCPR**.

## Autor

**40129956 - Gabriel Conti de Oliveira**

## Objetivo

O sistema ajuda uma biblioteca universitaria a organizar documentos digitais, como artigos, teses, livros e relatorios. Os arquivos ficam separados automaticamente por **tipo de arquivo** e **ano de publicacao**, reduzindo erros de organizacao manual.

## Funcionalidades

- Listar documentos digitais por tipo e ano.
- Adicionar documentos ja existentes a biblioteca.
- Criar documentos textuais diretamente pelo sistema.
- Renomear documentos.
- Remover documentos.
- Abrir documentos em formato de bytes.
- Ler documentos textuais, como TXT, MD, CSV, JSON, XML, HTML e PY.
- Listar diretorios internos da biblioteca.
- Criar diretorios.
- Remover diretorios vazios ou diretorios com conteudo, quando solicitado.
- Bloquear caminhos inseguros fora da pasta da biblioteca.

## Organizacao dos arquivos

Por padrao, os documentos ficam na pasta `documentos/`.

Exemplo de estrutura:

```text
documentos/
  pdf/
    2024/
      tese-inteligencia-artificial.pdf
  txt/
    2023/
      resumo-artigo.txt
```

## Como rodar

Use Python 3.10 ou superior.

Na pasta do projeto, execute:

```bash
python biblioteca.py --help
```

Se preferir instalar o comando localmente:

```bash
python -m pip install -e .
biblioteca-digital --help
```

## Exemplos de uso

Criar um documento textual:

```bash
python biblioteca.py criar resumo --extensao txt --ano 2024 --conteudo "Resumo inicial do artigo."
```

Listar documentos:

```bash
python biblioteca.py listar
```

Adicionar um PDF existente:

```bash
python biblioteca.py adicionar "C:\caminho\arquivo.pdf" --ano 2024
```

Renomear um documento:

```bash
python biblioteca.py renomear txt/2024/resumo.txt resumo-final.txt
```

Ler um documento textual:

```bash
python biblioteca.py ler txt/2024/resumo-final.txt
```

Remover um documento:

```bash
python biblioteca.py remover txt/2024/resumo-final.txt
```

Criar um diretorio:

```bash
python biblioteca.py diretorios criar epub/2025
```

Listar diretorios:

```bash
python biblioteca.py diretorios listar
```

Remover um diretorio:

```bash
python biblioteca.py diretorios remover epub/2025
```

## Como rodar os testes

O projeto usa `unittest`, biblioteca que ja vem com o Python:

```bash
python -m unittest discover -s tests -v
```

Resultado esperado:

```text
Ran 8 tests
OK
```

## Estrutura do projeto

```text
biblioteca_digital_pucpr/
  documentos/
  src/
    biblioteca_digital/
      __init__.py
      cli.py
      manager.py
  tests/
    test_cli.py
    test_manager.py
  biblioteca.py
  CONTRIBUTING.md
  README.md
  TESTES_E_FEEDBACK.md
  pyproject.toml
```

## Relacao com a rubrica

- **Manipulacao de arquivos e diretorios:** implementada em `BibliotecaDigital`, com criar, adicionar, listar, ler, renomear e remover documentos, alem de criar, listar e remover diretorios.
- **Git e GitHub:** o projeto inclui `.gitignore`, guia de contribuicao e uma proposta de fluxo com commits, pushes e pull requests.
- **Documentacao e relatorios:** o README documenta o uso do sistema e o arquivo `TESTES_E_FEEDBACK.md` registra testes e melhorias feitas com base em feedback.
