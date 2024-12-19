# -*- coding: utf-8 -*-
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.validator import validate

# -*- coding: utf-8 -*-
from kiara.api import KiaraAPI

#  Copyright (c) 2021, University of Luxembourg / DHARPA project
#  Copyright (c) 2021, Markus Binsteiner
#
#  Mozilla Public License, version 2.0 (see LICENSE or https://www.mozilla.org/en-US/MPL/2.0/)


def test_render_jupyter_notebook(kiara_api: KiaraAPI):

    render_config = {"inputs": {"a": True, "b": False}}

    rendered = kiara_api._api.render(
        "logic.xor",
        source_type="pipeline",
        target_type="jupyter_notebook",
        render_config=render_config,
    )

    notebook = nbformat.reads(rendered, as_version=4)
    validate(notebook)

    # Execute notebookQ
    executor = ExecutePreprocessor(timeout=600, kernel_name="python3")
    executor.preprocess(notebook)

    # Convert notebook object to string and return
    result_str = nbformat.writes(notebook)

    test_str = """"data": {
      "text/plain": [
       "True"
      ]
     },"""

    assert test_str in result_str, "Notebook output does not contain expected output"

    # compile(rendered, "<string>", "exec")
    #
    # local_vars = {}
    # exec(rendered, {}, local_vars)
    # assert local_vars["pipeline_result_y"].data is True
