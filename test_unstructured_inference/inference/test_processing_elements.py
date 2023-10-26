import pytest

from unstructured_inference.constants import Source
from unstructured_inference.inference.elements import Rectangle
from unstructured_inference.inference.layout import DocumentLayout, LayoutElement, PageLayout

# A set of elements with pdfminer elements inside tables
deletable_elements_inside_table = [
    LayoutElement(
        bbox=Rectangle(0, 0, 100, 100),
        text="Table with inner elements",
        type="Table",
    ),
    LayoutElement(bbox=Rectangle(50, 50, 70, 70), text="text1", source=Source.PDFMINER),
    LayoutElement(bbox=Rectangle(70, 70, 80, 80), text="text2", source=Source.PDFMINER),
]

# A set of elements without pdfminer elements inside
# tables (no elements with source=Source.PDFMINER)
no_deletable_elements_inside_table = [
    LayoutElement(
        bbox=Rectangle(0, 0, 100, 100),
        text="Table with inner elements",
        type="Table",
        source=Source.YOLOX,
    ),
    LayoutElement(bbox=Rectangle(50, 50, 70, 70), text="text1", source=Source.YOLOX),
    LayoutElement(bbox=Rectangle(70, 70, 80, 80), text="text2", source=Source.YOLOX),
]
# A set of elements with pdfminer elements inside tables and other
# elements with source=Source.PDFMINER
# Note: there is some elements with source=Source.PDFMINER are not inside tables
mix_elements_inside_table = [
    LayoutElement(
        bbox=Rectangle(0, 0, 100, 100),
        text="Table1 with inner elements",
        type="Table",
        source=Source.YOLOX,
    ),
    LayoutElement(bbox=Rectangle(50, 50, 70, 70), text="Inside table1"),
    LayoutElement(bbox=Rectangle(70, 70, 80, 80), text="Inside table1", source=Source.PDFMINER),
    LayoutElement(
        bbox=Rectangle(150, 150, 170, 170),
        text="Outside tables",
        source=Source.PDFMINER,
    ),
    LayoutElement(
        bbox=Rectangle(180, 180, 200, 200),
        text="Outside tables",
        source=Source.PDFMINER,
    ),
    LayoutElement(
        bbox=Rectangle(0, 500, 100, 700),
        text="Table2 with inner elements",
        type="Table",
        source=Source.YOLOX,
    ),
    LayoutElement(bbox=Rectangle(0, 510, 50, 300), text="Inside table2", source=Source.PDFMINER),
    LayoutElement(bbox=Rectangle(0, 550, 70, 400), text="Inside table2", source=Source.PDFMINER),
]


@pytest.mark.parametrize(
    ("elements", "lenght_extra_info", "expected_document_lenght"),
    [
        (deletable_elements_inside_table, 1, 1),
        (no_deletable_elements_inside_table, 0, 3),
        (mix_elements_inside_table, 2, 5),
    ],
)
def test_clean_pdfminer_inner_elements(elements, lenght_extra_info, expected_document_lenght):
    # create a sample document with pdfminer elements inside tables
    page = PageLayout(number=1, image=None, layout=elements)
    page.elements = elements
    document_with_table = DocumentLayout(pages=[page])

    # call the function to clean the pdfminer inner elements
    document_with_table.clean_pdfminer_inner_elements()

    assert len(document_with_table.pages[0].elements) == expected_document_lenght
