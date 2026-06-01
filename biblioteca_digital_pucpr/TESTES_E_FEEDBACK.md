# Relatorio de Testes e Feedback

## Objetivo dos testes

Os testes verificam se o sistema consegue manipular arquivos e diretorios de forma correta e segura, conforme solicitado na atividade.

## Testes automatizados realizados

Comando usado:

```bash
python -m unittest discover -s tests -v
```

Resultado obtido:

```text
Ran 8 tests in 0.071s
OK
```

## Casos testados

| Caso | Resultado |
| --- | --- |
| Criar documento textual e listar por tipo e ano | Aprovado |
| Adicionar documento externo a biblioteca | Aprovado |
| Renomear documento existente | Aprovado |
| Remover documento existente | Aprovado |
| Ler conteudo de documento textual | Aprovado |
| Criar, listar e remover diretorios | Aprovado |
| Impedir acesso a caminhos fora da biblioteca | Aprovado |
| Usar a interface de linha de comando para criar e listar | Aprovado |

## Feedback considerado

Durante a validacao do prototipo, foram considerados os seguintes pontos de melhoria para o uso por bibliotecarios:

| Feedback | Ajuste incorporado |
| --- | --- |
| A listagem deveria mostrar os documentos agrupados de forma clara. | O comando `listar` passou a exibir primeiro o tipo do arquivo e depois o ano. |
| O sistema deveria evitar remocao ou criacao de arquivos fora da biblioteca. | Foi adicionada validacao de caminho seguro, bloqueando `../` e caminhos externos. |
| O bibliotecario precisa renomear arquivos sem mudar toda a estrutura de pastas. | A funcao de renomear mantem o documento na mesma pasta. |
| A avaliacao exige diretorios, nao apenas arquivos. | Foram incluidas funcoes para listar, criar e remover diretorios. |
| Os testes precisam ser simples de executar. | O projeto usa `unittest`, que ja vem instalado com Python. |

## Ajustes feitos apos os testes

Foi identificado que, no Windows, alguns caminhos eram exibidos com barra invertida. A saida foi padronizada com `/`, deixando a visualizacao mais clara e mais adequada para documentacao e GitHub.

## Conclusao

O sistema atende ao cenario proposto porque organiza documentos digitais por tipo e ano, permite as principais operacoes de manipulacao de arquivos e diretorios, possui interface de linha de comando, inclui testes automatizados e apresenta documentacao de uso e contribuicao.

## Observacao final

Após a organização do repositório no GitHub, os arquivos foram estruturados com documentação na raiz e na pasta principal do projeto, facilitando a navegação, a avaliação e a execução do sistema.
