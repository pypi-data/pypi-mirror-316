"""TMTCrunch defaults and settings functions."""

__all__ = ["DEFAULT_CONFIG", "update_settings", "format_settings"]


from argparse import Namespace

DEFAULT_CONFIG = """
# TMT labels used in Identipy.
# tmt10plex_tags = ['126', '127C', '127N', '128C', '128N', '129C', '129N', '130C', '130N', '131']
# tmt11plex_tags = ['126', '127C', '127N', '128C', '128N', '129C', '129N', '130C', '130N', '131', '131C']

# Specimen TMT labels.
specimen_tags = ['127C', '127N', '128C', '128N', '129C', '129N', '130C', '130N', '131']
# Global internal standard (GIS) TMT labels.
gis_tags = ['126', '131C']

# Prefix of decoy proteins.
decoy_prefix = 'DECOY_'

# List of column names from input files to save in the output.
keep_columns = []

# If true, perform PSM groupwise analysis.
groupwise = true

# Keys below are only applicable if groupwise analysis is requested.

# Prefixes of target proteins. If not set, `target_prefixes` will be deduced
# from the prefixes of PSM groups.
# target_prefixes = ['alt_', 'canon_']

# Each PSM group is named after its subkey and defined by three keys:
# `descr` - group description
# `prefixes` - prefixes of target proteins
# `fdr` - groupwise false discovery rate

# Isoform PSMs: protein group of each PSM should consist of target proteins
# with 'alt_' prefix only and any decoy proteins.
[psm_group.isoform]
descr = 'Isoform PSMs'
prefixes = [['alt_']]
fdr = 0.05

# Canonical PSMs: protein group of each PSM should consist of target proteins
# with 'canon_' prefix only and any decoy proteins.
[psm_group.canon]
descr = 'Canonical PSMs'
prefixes = [['canon_']]
fdr = 0.01

# Shared PSMs: protein group of each PSM should consist both of
# 'canon_' and 'alt_' target proteins and any decoy proteins.
[psm_group.shared]
descr = 'Shared PSMs'
prefixes = [['canon_', 'alt_']]
fdr = 0.01
"""


def update_settings(settings: dict, args: Namespace) -> dict:
    """
    Update settings by command line arguments.

    :param settings: TMTCrunch settings.
    :param args: Command line arguments.
    :return: Updated settings.
    """
    if args.gis_tags:
        settings["gis_tags"] = [f"{tag}" for tag in args.gis_tags.split(",")]
    if args.specimen_tags:
        settings["specimen_tags"] = [f"{tag}" for tag in args.specimen_tags.split(",")]
    if args.keep_columns:
        settings["keep_columns"] = args.keep_columns
    # tmt columns returned by Identipy/Scavager
    settings["gis_columns"] = [f"tag_tmt_{tag}" for tag in settings["gis_tags"]]
    settings["specimen_columns"] = [
        f"tag_tmt_{tag}" for tag in settings["specimen_tags"]
    ]
    return settings


def format_settings(settings: dict, pretty=True) -> str:
    """
    Return formatted representation of `settings`.

    :param settings: TMTCrunch settings.
    :param pretty: If True, add header and footer.
    :return: Formatted string.
    """
    header = "====  settings  ===="
    footer = "=" * len(header)

    settings_str = ""
    if pretty:
        settings_str += header + "\n"
    for key, value in settings.items():
        if key == "psm_group":
            settings_str += f"{key}: " + "{\n"
            for group, group_cfg in value.items():
                settings_str += f"  {group}: {group_cfg},\n"
            settings_str += "}\n"
        else:
            settings_str += f"{key}: {value}\n"
    if pretty:
        settings_str += footer
    else:
        settings_str = settings_str[:-1]
    return settings_str
