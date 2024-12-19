# -*- coding: utf-8 -*-
from typing import Any, Iterable, Mapping, Union

from jinja2 import Template

from kiara.api import JobDesc
from kiara.models.module.pipeline.pipeline import Pipeline
from kiara.renderers import RenderInputsSchema, SourceTransformer
from kiara.renderers.included_renderers.job import JobDescTransformer
from kiara.renderers.jinja import BaseJinjaRenderer, JinjaEnv
from kiara.utils import log_message


class PipelineRenderer(BaseJinjaRenderer[Pipeline, RenderInputsSchema]):
    """Renders a basic Jupyter notebook from a job description.

    ## Examples

    ### Terminal

    Example invoication from the command line (using [this](https://github.com/DHARPA-Project/kiara_plugin.tabular/blob/develop/examples/jobs/init.yaml) job description):

    ```
    kiara render --source-type job_desc --target-type jupyter_notebook item init.yaml > example_notebook.ipynb

    jupyter-lab example_notebook.ipynb
    ```

    ### Python API

    Example usage from the Python API:

    ``` python
    from kiara.api import KiaraAPI

    kiara = KiaraAPI.instance()

    rendered = kiara.render("init.yaml", source_type="job_desc", target_type="jupyter_notebook")
    print("# Rendered notebook for job 'init.yaml':")
    print(rendered)
    ```

    """

    _renderer_name = "job_desc_notebook"
    _inputs_schema = RenderInputsSchema

    def retrieve_supported_render_sources(self) -> str:
        return "job_desc"

    def retrieve_supported_render_targets(cls) -> Union[Iterable[str], str]:
        return "jupyter_notebook"

    def retrieve_source_transformers(self) -> Iterable[SourceTransformer]:
        return [JobDescTransformer(kiara=self._kiara)]

    def retrieve_jinja_env(self) -> JinjaEnv:

        jinja_env = JinjaEnv(template_base="kiara_plugin.jupyter")
        return jinja_env

    def get_template(self, render_config: RenderInputsSchema) -> Template:

        return self.get_jinja_env().get_template("pipeline/jupyter_notebook.ipynb.j2")

    def assemble_render_inputs(
        self, instance: Any, render_config: RenderInputsSchema
    ) -> Mapping[str, Any]:

        from kiara.utils.rendering import create_pipeline_render_inputs

        job_desc: JobDesc = instance

        pipeline = Pipeline.create_pipeline(
            kiara=self._kiara, pipeline=job_desc.operation
        )

        result: Mapping[str, Any] = create_pipeline_render_inputs(
            pipeline, job_desc.inputs
        )
        return result

    def _post_process(self, rendered: str) -> str:

        is_notebook = True
        if is_notebook:
            import jupytext

            notebook = jupytext.reads(rendered, fmt="py:percent")
            converted: str = jupytext.writes(notebook, fmt="notebook")
            return converted
        else:
            try:
                import black
                from black import Mode  # type: ignore

                cleaned: str = black.format_str(rendered, mode=Mode())
                return cleaned

            except Exception as e:
                log_message(
                    f"Could not format python code, 'black' not in virtual environment: {e}."
                )
                return rendered
