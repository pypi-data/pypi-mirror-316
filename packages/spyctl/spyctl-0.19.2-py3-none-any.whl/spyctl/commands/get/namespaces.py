"""Handles retrieval of namespaces."""

import click

import spyctl.api.source_query_resources as sq_api
import spyctl.commands.get.shared_options as _so
import spyctl.config.configs as cfg
import spyctl.resources as _r
import spyctl.resources.api_filters as _af
import spyctl.spyctl_lib as lib
from spyctl import cli
from spyctl.commands.get import get_lib


@click.command("namespaces", cls=lib.CustomCommand, epilog=lib.SUB_EPILOG)
@_so.source_query_options
@_so.container_context_options
def get_namespaces_cmd(name_or_id, output, st, et, **filters):
    """Get namespaces by name or id."""
    exact = filters.pop("exact")
    get_lib.output_time_log(lib.NAMESPACES_RESOURCE.name_plural, st, et)
    name_or_id = get_lib.wildcard_name_or_id(name_or_id, exact)
    filters = {
        key: value for key, value in filters.items() if value is not None
    }
    handle_get_namespaces(name_or_id, output, st, et, **filters)


def handle_get_namespaces(name_or_id, output, st, et, **filters):
    """Output namespaces by name or id."""
    ctx = cfg.get_current_context()
    sources, filters = _af.Namespaces.build_sources_and_filters(**filters)
    pipeline = _af.Namespaces.generate_pipeline(name_or_id, filters=filters)
    if output in [lib.OUTPUT_DEFAULT, lib.OUTPUT_WIDE]:
        summary = _r.namespaces.namespace_summary_output(
            name_or_id, ctx, sources, (st, et), pipeline
        )
        cli.show(summary, lib.OUTPUT_RAW)
    else:
        for namespace in sq_api.get_namespaces(
            *ctx.get_api_data(),
            sources,
            (st, et),
            pipeline=pipeline,
            disable_pbar_on_first=not lib.is_redirected(),
        ):
            cli.show(namespace, output)
