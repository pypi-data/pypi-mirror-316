import argparse
import logging
import pathlib
import sys

from PIL import Image

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.JPG', '.JPEG']

def resize_image(
        path: pathlib.Path,
        size: int,
        output: pathlib.Path,
        quality: int = 80,
        optimize: bool = True) -> pathlib.Path | None:

    output = pathlib.Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        image = Image.open(path.as_posix())
        image.thumbnail((size, size))
        image.save(output.as_posix(), quality=quality, optimize=optimize)
    except Exception as e:
        logger.error(f'🔴 Error While Pillow Read, Convert or Save: \n\n {e}')

    return output


def run_impressify(
        path: pathlib.Path,
        size: int,
        output: pathlib.Path | None = None,
        quality: int = 80,
        optimize: bool = True):

    if not path.is_dir():
        if path.suffix not in ALLOWED_EXTENSIONS:
            logger.info(f'🟡 Your path is not in ALLOWED_EXTENSIONS: {ALLOWED_EXTENSIONS}')
            return

        output_dir = pathlib.Path(output) if output else path.parent
        try:
            output_dir.mkdir(exist_ok=True, parents=True)
        except Exception as e:
            logger.error(f'🔴 Error During Mkdir: \n\n {e}')
            return

        output_img = output_dir.joinpath(f'{path.stem}-{size}px{path.suffix}')

        output_img = resize_image(path, size, output_img, quality, optimize)

        if output_img and output_img.exists():
            logger.info(f'🟢 Succeffully: {output_img}')

    else:
        output_dir = pathlib.Path(output) if output else path
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f'🔴 Error During Mkdir: \n\n {e}')
            return

        try:
            images = list(filter(lambda f: f.suffix in ALLOWED_EXTENSIONS, path.iterdir()))
        except Exception as e:
            logger.error(f'🔴 Error During Iter: \n\n {e}')
            return

        for image in images:
            output_img = output_dir.joinpath(f'{image.stem}-{size}px{image.suffix}')

            output_img = resize_image(image, size, output_img, quality, optimize)
            if output_img and output_img.exists():
                logger.info(f'🟢 Succeffully: {output_img}')



def main():
    try:
        parser = argparse.ArgumentParser(description="⏰ Run and kill a subprocess after a specified time.")

        parser.add_argument("path", type=str, help="The path to the bash script to run.")
        parser.add_argument("size", type=int, help="An integer parameter that is required.")

        parser.add_argument("--output", type=str, default=None, help="The output path (optional).")
        parser.add_argument("--quality", type=int, default=80,
            help="An optional integer parameter with a default value of 80.")

        # Произвольный параметр optimize с значением по умолчанию
        parser.add_argument("--optimize", action="store_true",
                            help="An optional boolean flag. Default is True if provided, otherwise False.")

        args = parser.parse_args()

        # Пример обработки параметров
        print(f"Path: {args.path}")
        path = pathlib.Path(args.path)
        if not path.exists():
            logger.info('🟡 Input path not exists. Exit')
            sys.exit()

        output = None
        if args.output:
            output = pathlib.Path(args.output)

        if args.size < 1:
            logger.info('🟡 Your size is < 1. Exit')
            sys.exit()

        if  args.quality < 1 or args.quality > 100:
            logger.info('🟡 Your quality is not in [1, .. , 100]. Exit')
            sys.exit()

        run_impressify(path, args.size, output=output, quality=args.quality, optimize=args.optimize)

        logger.info(f"🚀 RUN: ")


    except KeyboardInterrupt:
        logger.warning("❗ Program interrupted by the user.")
    except Exception as e:
        logger.error(f"❌ An unexpected error occurred in main(): {e}")

if __name__ == "__main__":
    main()