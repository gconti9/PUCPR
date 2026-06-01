"""Interface de linha de comando para a biblioteca digital."""

from __future__ import annotations

import argparse
from pathlib import Path

from .manager import BibliotecaDigital


def _relativo(caminho: Path, pasta_base: str) -> str:
    return caminho.relative_to(Path(pasta_base).resolve()).as_posix()


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="biblioteca-digital",
        description="Sistema de gerenciamento de documentos digitais.",
    )
    parser.add_argument(
        "--biblioteca",
        default="documentos",
        help="Pasta onde os documentos da biblioteca ficam armazenados.",
    )

    subparsers = parser.add_subparsers(dest="comando", required=True)

    subparsers.add_parser("listar", help="Lista documentos por tipo e ano.")

    adicionar = subparsers.add_parser("adicionar", help="Adiciona um documento existente.")
    adicionar.add_argument("origem", help="Caminho do arquivo a ser copiado.")
    adicionar.add_argument("--ano", required=True, help="Ano de publicacao.")
    adicionar.add_argument("--nome", help="Novo nome do arquivo dentro da biblioteca.")
    adicionar.add_argument("--sobrescrever", action="store_true", help="Substitui arquivo existente.")

    criar = subparsers.add_parser("criar", help="Cria um documento textual.")
    criar.add_argument("nome", help="Nome do documento.")
    criar.add_argument("--extensao", default="txt", help="Extensao do documento.")
    criar.add_argument("--ano", required=True, help="Ano de publicacao.")
    criar.add_argument("--conteudo", default="", help="Conteudo inicial do documento.")
    criar.add_argument("--sobrescrever", action="store_true", help="Substitui arquivo existente.")

    renomear = subparsers.add_parser("renomear", help="Renomeia um documento.")
    renomear.add_argument("caminho", help="Caminho relativo dentro da biblioteca.")
    renomear.add_argument("novo_nome", help="Novo nome do arquivo.")

    remover = subparsers.add_parser("remover", help="Remove um documento.")
    remover.add_argument("caminho", help="Caminho relativo dentro da biblioteca.")

    ler = subparsers.add_parser("ler", help="Mostra o conteudo de um documento textual.")
    ler.add_argument("caminho", help="Caminho relativo dentro da biblioteca.")

    diretorios = subparsers.add_parser("diretorios", help="Gerencia diretorios.")
    dir_sub = diretorios.add_subparsers(dest="acao", required=True)
    dir_sub.add_parser("listar", help="Lista diretorios.")
    dir_criar = dir_sub.add_parser("criar", help="Cria diretorio.")
    dir_criar.add_argument("caminho", help="Caminho relativo do diretorio.")
    dir_remover = dir_sub.add_parser("remover", help="Remove diretorio.")
    dir_remover.add_argument("caminho", help="Caminho relativo do diretorio.")
    dir_remover.add_argument("--recursivo", action="store_true", help="Remove diretorio com conteudo.")

    return parser


def executar(args: argparse.Namespace) -> int:
    biblioteca = BibliotecaDigital(args.biblioteca)

    if args.comando == "listar":
        grupos = biblioteca.listar_por_tipo_e_ano()
        if not grupos:
            print("Nenhum documento cadastrado.")
            return 0
        for tipo, anos in sorted(grupos.items()):
            print(f"{tipo.upper()}")
            for ano, documentos in sorted(anos.items()):
                print(f"  {ano}")
                for documento in documentos:
                    print(f"    - {documento.nome} ({documento.caminho_relativo})")
        return 0

    if args.comando == "adicionar":
        destino = biblioteca.adicionar_documento(
            args.origem,
            ano=args.ano,
            novo_nome=args.nome,
            sobrescrever=args.sobrescrever,
        )
        print(f"Documento adicionado: {_relativo(destino, args.biblioteca)}")
        return 0

    if args.comando == "criar":
        destino = biblioteca.criar_documento(
            args.nome,
            extensao=args.extensao,
            ano=args.ano,
            conteudo=args.conteudo,
            sobrescrever=args.sobrescrever,
        )
        print(f"Documento criado: {_relativo(destino, args.biblioteca)}")
        return 0

    if args.comando == "renomear":
        destino = biblioteca.renomear_documento(args.caminho, args.novo_nome)
        print(f"Documento renomeado: {_relativo(destino, args.biblioteca)}")
        return 0

    if args.comando == "remover":
        biblioteca.remover_documento(args.caminho)
        print("Documento removido.")
        return 0

    if args.comando == "ler":
        print(biblioteca.ler_documento(args.caminho))
        return 0

    if args.comando == "diretorios":
        if args.acao == "listar":
            diretorios = biblioteca.listar_diretorios()
            if not diretorios:
                print("Nenhum diretorio cadastrado.")
            else:
                for diretorio in diretorios:
                    print(diretorio)
            return 0
        if args.acao == "criar":
            destino = biblioteca.criar_diretorio(args.caminho)
            print(f"Diretorio criado: {_relativo(destino, args.biblioteca)}")
            return 0
        if args.acao == "remover":
            biblioteca.remover_diretorio(args.caminho, recursivo=args.recursivo)
            print("Diretorio removido.")
            return 0

    return 1


def main() -> int:
    parser = criar_parser()
    args = parser.parse_args()
    try:
        return executar(args)
    except Exception as erro:
        print(f"Erro: {erro}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
