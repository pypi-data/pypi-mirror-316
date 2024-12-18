from pathlib import Path

import magic

from tika_client.client import TikaClient


class TestRecursiveMetadataResource:
    def test_r_metadata_from_docx(self, tika_client: TikaClient, sample_google_docs_to_docx_file: Path):
        documents = tika_client.rmeta.as_html.from_file(
            sample_google_docs_to_docx_file,
            magic.from_file(str(sample_google_docs_to_docx_file), mime=True),
        )

        assert len(documents) == 1
        document = documents[0]

        assert document.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        assert document.content is not None
        assert "<body><p>This is an DOCX test document, also made September 14, 2022</p>\n</body>" in document.content
        assert document.created is None

    def test_r_metadata_from_docx_plain(self, tika_client: TikaClient, sample_google_docs_to_docx_file: Path):
        documents = tika_client.rmeta.as_text.from_file(
            sample_google_docs_to_docx_file,
            magic.from_file(str(sample_google_docs_to_docx_file), mime=True),
        )

        assert len(documents) == 1
        document = documents[0]

        assert document.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        assert document.content is not None
        assert "This is an DOCX test document, also made September 14, 2022" in document.content
        assert document.created is None

    def test_r_meta_microsoft_word_docx(self, tika_client: TikaClient, sample_docx_file: Path):
        documents = tika_client.rmeta.as_html.from_file(
            sample_docx_file,
            magic.from_file(str(sample_docx_file), mime=True),
        )

        assert len(documents) == 1
        document = documents[0]

        assert document.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        assert document.content is not None
        assert (
            "<body><p>This is a sample document, generated by Microsoft Office on Wednesday, May 17, 2023.</p>\n<p>It is in English.</p>\n</body>"  # noqa: E501
            in document.content
        )

    def test_r_metadata_from_odt(self, tika_client: TikaClient, sample_google_docs_to_libre_office_writer_file: Path):
        documents = tika_client.rmeta.as_html.from_file(
            sample_google_docs_to_libre_office_writer_file,
            magic.from_file(str(sample_google_docs_to_libre_office_writer_file), mime=True),
        )

        assert len(documents) == 2
        document = documents[0]

        assert document.type == "application/vnd.oasis.opendocument.text"
        assert document.content is not None
        assert "<body><p>This is an ODT test document, created September 14, 2022</p>\n</body>" in document.content
        assert document.created is None

    def test_r_metadata_from_odt_plain(
        self,
        tika_client: TikaClient,
        sample_google_docs_to_libre_office_writer_file: Path,
    ):
        documents = tika_client.rmeta.as_text.from_file(
            sample_google_docs_to_libre_office_writer_file,
            magic.from_file(str(sample_google_docs_to_libre_office_writer_file), mime=True),
        )

        assert len(documents) == 2

        document = documents[0]
        assert document.type == "application/vnd.oasis.opendocument.text"
        assert document.content is not None
        assert "This is an ODT test document, created September 14, 2022" in document.content

        document = documents[1]
        assert document.type == "image/png"

    def test_r_metadata_from_ods_plain(self, tika_client: TikaClient, sample_ods_file: Path):
        documents = tika_client.rmeta.as_text.from_file(
            sample_ods_file,
            magic.from_file(str(sample_ods_file), mime=True),
        )

        assert len(documents) == 2

        document = documents[0]
        assert document.content is not None
        assert "This is cell A1" in document.content
        assert "You sunk my battleship" in document.content

        document = documents[1]
        assert document.type == "image/png"

    def test_r_metadata_from_xlsx_plain(self, tika_client: TikaClient, sample_xlsx_file: Path):
        documents = tika_client.rmeta.as_text.from_file(
            sample_xlsx_file,
            magic.from_file(str(sample_xlsx_file), mime=True),
        )

        assert len(documents) == 1
        document = documents[0]

        assert document.content is not None
        assert "This is cell A1" in document.content
        assert "You sunk my battleship" in document.content
