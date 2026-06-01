import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from biblioteca_digital.cli import criar_parser, executar


class TestCli(unittest.TestCase):
    def test_cli_cria_e_lista_documento(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pasta = Path(temp_dir) / "documentos"
            parser = criar_parser()

            args_criar = parser.parse_args(
                [
                    "--biblioteca",
                    str(pasta),
                    "criar",
                    "guia",
                    "--extensao",
                    "txt",
                    "--ano",
                    "2024",
                    "--conteudo",
                    "Conteudo do guia.",
                ]
            )
            self.assertEqual(executar(args_criar), 0)

            args_listar = parser.parse_args(["--biblioteca", str(pasta), "listar"])
            saida = io.StringIO()
            with redirect_stdout(saida):
                self.assertEqual(executar(args_listar), 0)

            texto = saida.getvalue()
            self.assertIn("TXT", texto)
            self.assertIn("2024", texto)
            self.assertIn("guia.txt", texto)


if __name__ == "__main__":
    unittest.main()
