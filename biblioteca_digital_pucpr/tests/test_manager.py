import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from biblioteca_digital import BibliotecaDigital


class TestBibliotecaDigital(unittest.TestCase):
    def test_cria_e_lista_documento_por_tipo_e_ano(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            biblioteca = BibliotecaDigital(Path(temp_dir) / "documentos")

            biblioteca.criar_documento(
                "artigo-ciencia-dados",
                extensao="txt",
                ano=2024,
                conteudo="Resumo do artigo.",
            )

            grupos = biblioteca.listar_por_tipo_e_ano()

            self.assertIn("txt", grupos)
            self.assertIn("2024", grupos["txt"])
            self.assertEqual(grupos["txt"]["2024"][0].nome, "artigo-ciencia-dados.txt")

    def test_adiciona_documento_existente(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raiz = Path(temp_dir)
            origem = raiz / "tese.pdf"
            origem.write_bytes(b"%PDF-1.4")
            biblioteca = BibliotecaDigital(raiz / "biblioteca")

            destino = biblioteca.adicionar_documento(origem, ano="2023")

            self.assertTrue(destino.exists())
            self.assertEqual(destino.name, "tese.pdf")
            self.assertEqual(destino.parent.name, "2023")
            self.assertEqual(destino.parent.parent.name, "pdf")

    def test_renomeia_documento(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raiz = Path(temp_dir)
            biblioteca = BibliotecaDigital(raiz / "documentos")
            biblioteca.criar_documento("livro", "txt", 2022, "conteudo")

            novo_caminho = biblioteca.renomear_documento("txt/2022/livro.txt", "livro-renomeado.txt")

            self.assertEqual(novo_caminho.name, "livro-renomeado.txt")
            self.assertFalse((raiz / "documentos" / "txt" / "2022" / "livro.txt").exists())

    def test_remove_documento(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            biblioteca = BibliotecaDigital(Path(temp_dir) / "documentos")
            biblioteca.criar_documento("relatorio", "md", 2021, "# Testes")

            biblioteca.remover_documento("md/2021/relatorio.md")

            self.assertEqual(biblioteca.listar_documentos(), [])

    def test_le_documento_textual(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            biblioteca = BibliotecaDigital(Path(temp_dir) / "documentos")
            biblioteca.criar_documento("notas", "txt", 2025, "Feedback incorporado.")

            conteudo = biblioteca.ler_documento("txt/2025/notas.txt")

            self.assertEqual(conteudo, "Feedback incorporado.")

    def test_impede_caminho_fora_da_biblioteca(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            biblioteca = BibliotecaDigital(Path(temp_dir) / "documentos")

            with self.assertRaises(ValueError):
                biblioteca.criar_diretorio("../fora")

    def test_cria_lista_e_remove_diretorio(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            biblioteca = BibliotecaDigital(Path(temp_dir) / "documentos")

            biblioteca.criar_diretorio("pdf/2024")
            self.assertIn("pdf", biblioteca.listar_diretorios())
            self.assertIn("pdf/2024", biblioteca.listar_diretorios())

            biblioteca.remover_diretorio("pdf/2024")
            self.assertNotIn("pdf/2024", biblioteca.listar_diretorios())


if __name__ == "__main__":
    unittest.main()
