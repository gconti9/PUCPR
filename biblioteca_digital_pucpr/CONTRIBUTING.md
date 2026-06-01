# Guia de Contribuicao

Este guia explica como contribuir com o projeto usando Git e GitHub.

## Fluxo recomendado

1. Crie uma branch para sua alteracao:

```bash
git checkout -b melhoria/nome-da-melhoria
```

2. Faca as alteracoes no codigo.

3. Rode os testes:

```bash
python -m unittest discover -s tests -v
```

4. Veja quais arquivos foram alterados:

```bash
git status
```

5. Adicione os arquivos ao commit:

```bash
git add .
```

6. Crie um commit claro:

```bash
git commit -m "Adiciona cadastro de documentos por ano"
```

7. Envie a branch para o GitHub:

```bash
git push origin melhoria/nome-da-melhoria
```

8. Abra um Pull Request no GitHub explicando:

- O que foi alterado.
- Por que a alteracao foi feita.
- Como a alteracao foi testada.

## Padrao de commits

Use mensagens curtas e objetivas, por exemplo:

- `Cria interface de linha de comando`
- `Adiciona testes de remocao de documentos`
- `Documenta comandos principais do sistema`
- `Corrige validacao de caminhos inseguros`

## Boas praticas de codigo

- Usar nomes claros para variaveis, funcoes e classes.
- Manter funcoes pequenas e com responsabilidade bem definida.
- Validar entradas do usuario.
- Evitar caminhos absolutos fixos no codigo.
- Rodar os testes antes de enviar alteracoes.
- Atualizar a documentacao quando uma funcionalidade mudar.

## Configuracao do repositorio no GitHub

Para aceitar contribuicoes por Pull Request:

1. Crie o repositorio no GitHub.
2. Envie este projeto para o repositorio remoto.
3. Ative a aba de Pull Requests, que ja vem disponivel em repositorios comuns do GitHub.
4. Opcionalmente, configure protecao da branch `main` para exigir revisao antes de merge.
5. Oriente colaboradores a trabalhar sempre em branches separadas.
