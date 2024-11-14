import tkinter
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageConverter:
    @staticmethod
    def pil_to_cv2(pil_image):
        cv2_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return cv2_image

    @staticmethod
    def cv2_to_pil(cv2_image):
        rgb_cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_cv2_image)
        return pil_image

    @staticmethod
    def pil_to_tk(pil_image):
        tk_image = ImageTk.PhotoImage(pil_image)
        return tk_image

    @staticmethod
    def tk_to_cv2(tk_image):
        width = tk_image.width()
        height = tk_image.height()
        bitmap = [[list(tk_image.get(x, y)) for x in range(width)] for y in range(height)]
        cv2_rgb_image = np.array(bitmap, dtype='uint8')
        cv2_image = cv2.cvtColor(cv2_rgb_image, cv2.COLOR_RGB2BGR)
        return cv2_image

    @staticmethod
    def to_pil(image):
        if isinstance(image, str):
            return Image.open(image)
        elif isinstance(image, Image.Image):
            return image
        elif isinstance(image, np.ndarray):
            return ImageConverter.cv2_to_pil(image)
        elif isinstance(image, tkinter.PhotoImage):
            cv2_image = ImageConverter.tk_to_cv2(image)
            return ImageConverter.cv2_to_pil(cv2_image)
        else:
            raise ValueError("Unsupported image type")

    @staticmethod
    def to_cv2(image):
        if isinstance(image, str):
            return cv2.imread(image)
        elif isinstance(image, Image.Image):
            return ImageConverter.pil_to_cv2(image)
        elif isinstance(image, np.ndarray):
            return image
        elif isinstance(image, tkinter.PhotoImage):
            return ImageConverter.tk_to_cv2(image)
        else:
            raise ValueError("Unsupported image type")

    @staticmethod
    def to_tk(image):
        if isinstance(image, str):
            pil_image = Image.open(image)
            return ImageConverter.pil_to_tk(pil_image)
        elif isinstance(image, Image.Image):
            return ImageConverter.pil_to_tk(image)
        elif isinstance(image, np.ndarray):
            pil_image = ImageConverter.cv2_to_pil(image)
            return ImageConverter.pil_to_tk(pil_image)
        elif isinstance(image, tkinter.PhotoImage):
            return image
        else:
            raise ValueError("Unsupported image type")
        
    @staticmethod
    def resize(image, size):
        """
        Resize the image to the specified size.
        :param image: The input image (PIL Image, OpenCV image, or Tkinter PhotoImage)
        :param size: A tuple of (width, height)
        :return: Resized image of the same type as input
        """
        if isinstance(image, Image.Image):
            return image.resize(size, Image.LANCZOS)
        elif isinstance(image, np.ndarray):
            return cv2.resize(image, size, interpolation=cv2.INTER_LANCZOS4)
        elif isinstance(image, tkinter.PhotoImage):
            # Convert to PIL, resize, then back to Tkinter
            pil_image = ImageConverter.to_PIL(image)
            resized_pil = pil_image.resize(size, Image.LANCZOS)
            return ImageConverter.to_Tkinter(resized_pil)
        else:
            raise ValueError("Unsupported image type")  