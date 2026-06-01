"""Regras principais do sistema de biblioteca digital."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".xml", ".html", ".py"}


@dataclass(frozen=True)
class Documento:
    """Representa um documento encontrado na biblioteca."""

    nome: str
    caminho_relativo: str
    tipo: str
    ano: str
    tamanho_bytes: int


class BibliotecaDigital:
    """Gerencia documentos digitais organizados por tipo e ano."""

    def __init__(self, pasta_base: str | os.PathLike[str]) -> None:
        self.pasta_base = Path(pasta_base).expanduser().resolve()
        self.pasta_base.mkdir(parents=True, exist_ok=True)

    def listar_documentos(self) -> list[Documento]:
        """Lista todos os arquivos da biblioteca."""

        documentos: list[Documento] = []
        for caminho in sorted(self.pasta_base.rglob("*")):
            if not caminho.is_file():
                continue

            relativo = caminho.relative_to(self.pasta_base)
            tipo = caminho.suffix.lower().lstrip(".") or "sem_extensao"
            ano = self._descobrir_ano(relativo)
            documentos.append(
                Documento(
                    nome=caminho.name,
                    caminho_relativo=relativo.as_posix(),
                    tipo=tipo,
                    ano=ano,
                    tamanho_bytes=caminho.stat().st_size,
                )
            )
        return documentos

    def listar_por_tipo_e_ano(self) -> dict[str, dict[str, list[Documento]]]:
        """Agrupa documentos por extensao de arquivo e ano de publicacao."""

        grupos: dict[str, dict[str, list[Documento]]] = {}
        for documento in self.listar_documentos():
            grupos.setdefault(documento.tipo, {}).setdefault(documento.ano, []).append(documento)
        return grupos

    def adicionar_documento(
        self,
        origem: str | os.PathLike[str],
        ano: str | int,
        novo_nome: str | None = None,
        sobrescrever: bool = False,
    ) -> Path:
        """Copia um documento externo para a biblioteca."""

        origem_path = Path(origem).expanduser().resolve()
        if not origem_path.is_file():
            raise FileNotFoundError(f"Arquivo de origem nao encontrado: {origem_path}")

        nome_final = novo_nome or origem_path.name
        destino = self._pasta_tipo_ano(nome_final, ano) / nome_final
        self._validar_nome_arquivo(nome_final)

        if destino.exists() and not sobrescrever:
            raise FileExistsError(f"Ja existe um documento com este nome: {destino.name}")

        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem_path, destino)
        return destino

    def criar_documento(
        self,
        nome: str,
        extensao: str,
        ano: str | int,
        conteudo: str = "",
        sobrescrever: bool = False,
    ) -> Path:
        """Cria um documento textual dentro da biblioteca."""

        extensao = extensao if extensao.startswith(".") else f".{extensao}"
        nome_completo = nome if nome.lower().endswith(extensao.lower()) else f"{nome}{extensao}"
        self._validar_nome_arquivo(nome_completo)

        destino = self._pasta_tipo_ano(nome_completo, ano) / nome_completo
        if destino.exists() and not sobrescrever:
            raise FileExistsError(f"Ja existe um documento com este nome: {destino.name}")

        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(conteudo, encoding="utf-8")
        return destino

    def renomear_documento(self, caminho_relativo: str, novo_nome: str) -> Path:
        """Renomeia um documento mantendo-o na mesma pasta."""

        atual = self._resolver_caminho_seguro(caminho_relativo)
        if not atual.is_file():
            raise FileNotFoundError(f"Documento nao encontrado: {caminho_relativo}")

        self._validar_nome_arquivo(novo_nome)
        novo_caminho = atual.with_name(novo_nome)
        if novo_caminho.exists():
            raise FileExistsError(f"Ja existe um arquivo chamado: {novo_nome}")

        atual.rename(novo_caminho)
        return novo_caminho

    def remover_documento(self, caminho_relativo: str) -> None:
        """Remove um documento da biblioteca."""

        caminho = self._resolver_caminho_seguro(caminho_relativo)
        if not caminho.is_file():
            raise FileNotFoundError(f"Documento nao encontrado: {caminho_relativo}")
        caminho.unlink()

    def abrir_documento(self, caminho_relativo: str) -> bytes:
        """Abre um documento e retorna seu conteudo em bytes."""

        caminho = self._resolver_caminho_seguro(caminho_relativo)
        if not caminho.is_file():
            raise FileNotFoundError(f"Documento nao encontrado: {caminho_relativo}")
        return caminho.read_bytes()

    def ler_documento(self, caminho_relativo: str) -> str:
        """Le o conteudo de documentos textuais."""

        caminho = self._resolver_caminho_seguro(caminho_relativo)
        if caminho.suffix.lower() not in TEXT_EXTENSIONS:
            raise ValueError("Leitura textual disponivel apenas para arquivos de texto.")
        return caminho.read_text(encoding="utf-8")

    def listar_diretorios(self) -> list[str]:
        """Lista todos os diretorios cadastrados dentro da biblioteca."""

        diretorios = [
            caminho.relative_to(self.pasta_base).as_posix()
            for caminho in sorted(self.pasta_base.rglob("*"))
            if caminho.is_dir()
        ]
        return diretorios

    def criar_diretorio(self, caminho_relativo: str) -> Path:
        """Cria um diretorio dentro da biblioteca."""

        destino = self._resolver_caminho_seguro(caminho_relativo, precisa_existir=False)
        destino.mkdir(parents=True, exist_ok=True)
        return destino

    def remover_diretorio(self, caminho_relativo: str, recursivo: bool = False) -> None:
        """Remove um diretorio vazio ou, se solicitado, toda a sua arvore."""

        destino = self._resolver_caminho_seguro(caminho_relativo)
        if not destino.is_dir():
            raise FileNotFoundError(f"Diretorio nao encontrado: {caminho_relativo}")

        if recursivo:
            shutil.rmtree(destino)
        else:
            destino.rmdir()

    def _pasta_tipo_ano(self, nome_arquivo: str, ano: str | int) -> Path:
        extensao = Path(nome_arquivo).suffix.lower().lstrip(".") or "sem_extensao"
        ano_validado = self._validar_ano(ano)
        return self.pasta_base / extensao / ano_validado

    def _descobrir_ano(self, caminho_relativo: Path) -> str:
        for parte in caminho_relativo.parts:
            if parte.isdigit() and len(parte) == 4:
                return parte
        return "sem_ano"

    def _validar_ano(self, ano: str | int) -> str:
        ano_texto = str(ano)
        if not (ano_texto.isdigit() and len(ano_texto) == 4):
            raise ValueError("O ano deve ter quatro digitos, por exemplo: 2024.")
        return ano_texto

    def _validar_nome_arquivo(self, nome: str) -> None:
        if not nome or Path(nome).name != nome:
            raise ValueError("Informe apenas o nome do arquivo, sem pastas.")

    def _resolver_caminho_seguro(
        self,
        caminho_relativo: str,
        precisa_existir: bool = True,
    ) -> Path:
        caminho = (self.pasta_base / caminho_relativo).resolve()
        if self.pasta_base not in caminho.parents and caminho != self.pasta_base:
            raise ValueError("Caminho fora da biblioteca nao permitido.")
        if precisa_existir and not caminho.exists():
            raise FileNotFoundError(f"Caminho nao encontrado: {caminho_relativo}")
        return caminho
