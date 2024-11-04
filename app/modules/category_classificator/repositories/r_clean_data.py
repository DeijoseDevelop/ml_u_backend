import typing as t
from pathlib import Path

import polars as pl


class CleanDataRepository:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.df: pl.DataFrame = self._load_data()
        self.texts: t.List[str] = []
        self.labels: t.List[str] = []

    def _load_data(self) -> pl.DataFrame:
        if not self.file_path.exists():
            raise FileNotFoundError(f"El archivo {self.file_path} no existe.")
        try:
            df = pl.read_excel(str(self.file_path))
            return df
        except Exception as e:
            raise Exception(f"Error al leer el archivo Excel: {e}")

    def clean(self) -> t.Tuple[t.List[str], t.List[str]]:
        """
        Limpia y procesa los datos, retornando textos y etiquetas.
        """
        data = self._extract_data()
        self.texts = [item['text'] for item in data]
        self.labels = [item['label'] for item in data]
        return self.texts, self.labels

    def _extract_data(self) -> t.List[t.Dict[str, str]]:
        """
        Extrae los textos y etiquetas de cada fila del DataFrame.
        """
        data: t.List[t.Dict[str, str]] = []

        for row in self.df.iter_rows(named=True):
            for label in ["wait for", "rent book", "use computer", "other"]:
                text = row.get(label)
                if text and isinstance(text, str):
                    data.append({"text": text.strip(), "label": label})
        return data