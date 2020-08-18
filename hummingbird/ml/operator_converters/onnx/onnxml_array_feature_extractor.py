# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
Converter for ONNX-ML Array Feature Extractor.
"""

from onnxconverter_common.registration import register_converter

from .. import constants
from .._array_feature_extractor_implementations import ArrayFeatureExtractor


def convert_onnx_array_feature_extractor(operator, device, extra_config):
    """
    Converter for `ai.onnx.ml.ArrayFeatureExtractor`.

    Args:
        operator: An operator wrapping a `ai.onnx.ml.ArrayFeatureExtractor` model
        device: String defining the type of device the converted operator should be run on
        extra_config: Extra configuration used to select the best conversion strategy

    Returns:
        A PyTorch model
    """

    # TODO, this will be tested as part of the ai.onnx.ml.OneHotEncoder tests
    initializers = extra_config[constants.ONNX_INITIALIZERS]
    for name in operator.raw_operator.origin.input:
        if name in initializers:
            column_indices = initializers[name].int64_data
            return ArrayFeatureExtractor(column_indices, device)
    raise RuntimeError("ONNXMLArrayFeatureExtractor: cannot find column inidices in initializers.")


register_converter("ONNXMLArrayFeatureExtractor", convert_onnx_array_feature_extractor)
