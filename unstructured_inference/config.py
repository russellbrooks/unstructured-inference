import os
from dataclasses import dataclass


@dataclass
class InferenceConfig:
    """class for configuring inference parameters"""

    def _get_string(self, var: str, default_value: str = "") -> str:
        """attempt to get the value of var from the os environment; if not present return the
        default_value"""
        return os.environ.get(var, default_value)

    def _get_int(self, var: str, default_value: int) -> int:
        if value := self._get_string(var):
            return int(value)
        return default_value

    def _get_float(self, var: str, default_value: float) -> float:
        if value := self._get_string(var):
            return float(value)
        return default_value

    @property
    def TABLE_IMAGE_CROP_PAD(self) -> int:
        """extra image content to add around an identified table region; measured in pixels

        The padding adds image data around an identified table bounding box for downstream table
        structure detection model use as input
        """
        return self._get_int("TABLE_IMAGE_CROP_PAD", 12)

    @property
    def TABLE_IMAGE_BACKGROUN_PAD(self) -> int:
        """number of pixels to pad around an table image with a white background color

        The padding adds NO image data around an identified table bounding box; it simply adds white
        background around the image
        """
        return self._get_int("TABLE_IMAGE_BACKGROUN_PAD", 0)

    @property
    def LAYOUT_SAME_REGION_THRESHOLD(self) -> float:
        """threshold for two layouts' bounding boxes to be considered as the same region

        When the intersection area over union area of the two is larger than this threshold the two
        boxes are considered the same region
        """
        return self._get_float("LAYOUT_SAME_REGION_THRESHOLD", 0.75)

    @property
    def LAYOUT_SUBREGION_THRESHOLD(self) -> float:
        """threshold for one bounding box to be considered as a sub-region of another bounding box

        When the intersection region area divided by self area is larger than this threshold self is
        considered a subregion of the other
        """
        return self._get_float("LAYOUT_SUBREGION_THRESHOLD", 0.75)

    @property
    def ELEMENTS_H_PADDING_COEF(self) -> float:
        """When extending the boundaries of a PDF object for the purpose of determining which other
        elements should be considered in the same text region, we use a relative distance based on
        some fraction of the block height (typically character height). This is the fraction used
        for the horizontal extension applied to the left and right sides.
        """
        return self._get_float("ELEMENTS_H_PADDING_COEF", 0.4)

    @property
    def ELEMENTS_V_PADDING_COEF(self) -> float:
        """Same as ELEMENTS_H_PADDING_COEF but the vertical extension."""
        return self._get_float("ELEMENTS_V_PADDING_COEF", 0.3)


inference_config = InferenceConfig()
