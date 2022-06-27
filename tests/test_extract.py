import os

from tiqets import config, extract


def test_extract_output_dataset():
    try:
        os.remove(config.OUTPUT_FILE_NAME)
    except FileNotFoundError:
        pass
    dataset = [(1, 1, "2,1"), (1, 2, "5,4,3"), (2, 3, "7,6")]
    extract.extract_output_dataset(dataset)
    with open(config.OUTPUT_FILE_NAME) as out_file:
        contents = out_file.read()
        assert contents == (
            "customer_id,order_id,barcodes\n"
            '1,1,"2,1"\n'
            '1,2,"5,4,3"\n'
            '2,3,"7,6"\n'
        )
