from openpyxl import load_workbook

from ons_metadata_validation.processing.processor import MetadataProcessor
from ons_metadata_validation.processing.utils import (
    apply_version_changes,
    write_dfs_to_wb,
)
from ons_metadata_validation.reference.delta_table import DELTA_TABLE
from ons_metadata_validation.reference.template import V2_TEMP


def convert_v2_to_version(
    v2_path: str,
    empty_v3_path: str,
    v3_save_path: str,
    target_version: float = 3.0,
) -> bool:
    """Convert a metadata template to another version.

    Args:
        v2_path (str): Path to the original template (assume to be V2).
        empty_v3_path (str): Path to the empty dst template.
        v3_save_path (str): Where to save the dst template.
        target_version (float, optional): The version to transform to. Defaults to 3.0.

    Returns:
        bool: True if successful. False otherwise.
    """
    try:
        mp = MetadataProcessor(v2_path, "full", False, False, False)
        mp.load_xl()
        version_template = apply_version_changes(
            V2_TEMP, DELTA_TABLE, target_version=target_version
        )
        wb = load_workbook(empty_v3_path)
        write_dfs_to_wb(version_template, mp.xl, wb)
        wb.save(v3_save_path)
        return True
    except Exception as e:
        print(
            {
                "error": e,
                "v2_path": v2_path,
                "empty_v3_path": empty_v3_path,
                "v3_save_path": v3_save_path,
                "target_version": target_version,
            }
        )
        return False
