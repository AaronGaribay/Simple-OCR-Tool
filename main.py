from PIL import Image
import fitz

import imghdr
import argparse
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class File:
    """The File class represent a document file
    """
    def __init__(self, path: str) -> None:
        """Method for initializing a File object

        Arguments:
            path {str}

        Attributes:
            path {str}: the absolute or relative filepath
        """
        self.path = Path(path).absolute()

    def convert_to_png(self, remove: bool = False, poi: int = 0) -> None:
        """Take the self.path and convert it to a PNG file
        The file must be an Image or a PDF (Scanned or not)

        Keyword Arguments:
            remove {bool} -- Deletes the original file (default: {False})
            poi {int} -- The Page OF Interest (POI)
                from a PDF file (default: {0})

        Returns: None

        Raises:
            Exception: The POI must be integer greater or equeal to 0
        """

        if poi < 0:
            logger.error(f"poi (page of interest) must be positive")
            raise Exception("poi must be a zero or positive int")

        filename = self.path
        new_filename = Path(''.join([
            str(self.path.parent / self.path.stem),
            '.png']
            )
        )

        if filename.suffix.upper() == '.PNG':
            logger.info(f"File {filename.stem} is png")

        elif imghdr.what(self.path):
            im = Image.open(self.path).convert("RGB")
            im.save(str(new_filename), "png")
            logger.info(
                f"File converted to {new_filename.name} "
                "updated path in class")
            im.close()

        elif filename.suffix.upper() == '.PDF':
            pdf = fitz.open(filename)
            page = pdf.loadPage(poi-1)
            pix = page.getPixmap(alpha=False)
            new_filename = Path(''.join([
                str(new_filename.parent / new_filename.stem),
                str(poi),
                str(new_filename.suffix)]
                )
            )
            pix.writePNG(str(new_filename))
            logger.info(
                f"page {poi} from PDF converted to {new_filename.name} "
                "updated path in class"
                )
            pdf.close()

        if remove:
            filename.unlink()
            logger.info("Originak file '{filename.name}' has been deleted")
        self.path = new_filename


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-f",
        "--file",
        required=True,
        type=str,
        help="path to input file to be OCR'd"
        )

    ap.add_argument(
        "-p",
        "--preprocess",
        type=str,
        default="thresh",
        help="type of preprocessing to be done"
        )

    args = vars(ap.parse_args())
    newFile = File(args['file'])
    newFile.convert_to_png()
