"""
Public commands for the RegScale CLI
"""

import click
from regscale.core.lazy_group import LazyGroup


@click.group(
    cls=LazyGroup,
    lazy_subcommands={
        "import_docx": "regscale.core.app.public.fedramp.fedramp.load_fedramp_docx",
        "import_oscal": "regscale.core.app.public.fedramp.fedramp.load_fedramp_oscal",
        "import_ssp_xml": "regscale.core.app.public.fedramp.fedramp.import_fedramp_ssp_xml",
        "import_appendix_a": "regscale.core.app.public.fedramp.fedramp.load_fedramp_appendix_a",
        "import_inventory": "regscale.core.app.public.fedramp.fedramp.import_fedramp_inventory",
        "import_poam": "regscale.core.app.public.fedramp.fedramp.import_fedramp_poam_template",
        "import_drf": "regscale.core.app.public.fedramp.fedramp.import_drf",
        "import_cis_crm": "regscale.core.app.public.fedramp.fedramp.import_ciscrm",
    },
    name="fedramp",
)
def fedramp():
    """Performs bulk processing of FedRAMP files (Upload trusted data only)."""
    pass
