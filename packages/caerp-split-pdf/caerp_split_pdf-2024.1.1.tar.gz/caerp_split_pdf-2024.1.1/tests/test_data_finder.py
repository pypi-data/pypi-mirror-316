TEST_LINE = """
Test multiline

Wrong code : 5NOOKLINETOOLONG
Code : 5OKLINE

Other code : 5NOOKLINE"""


def test_regex_datafinder():
    from ..src.caerp_split_pdf.data_finder import RegexDataFinder

    bytes_regex = rb"\s[5,9][\w]{3,9}(\s|$)"
    regex = r"\s[5,9][\w]{3,9}(\s|$)"

    finder = RegexDataFinder(bytes_regex)
    assert finder.find(TEST_LINE) == "5OKLINE"

    finder = RegexDataFinder(regex)
    assert finder.find(TEST_LINE) == "5OKLINE"
    assert finder.find("") is None

    finder = RegexDataFinder(regex, strict=True)
    assert finder.find(TEST_LINE) is None

    finder = RegexDataFinder(regex, from_line=6, strict=True)
    assert finder.find(TEST_LINE) == "5NOOKLINE"


def test_coordinate_data_finder():
    from caerp_split_pdf.data_finder import CoordinateDataFinder

    finder = CoordinateDataFinder(line=5, prefix="Code :")
    assert finder.find(TEST_LINE) == "5OKLINE"
