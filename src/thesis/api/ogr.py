import logging
import shutil
import subprocess
import tempfile
import time
import warnings
from pathlib import Path
from typing import Optional, Sequence, cast

from alive_progress import alive_bar
from osgeo import ogr, os

from thesis.events import creation_event, deletion_event, modification_event
from thesis.protobuf import (CreationEvent, DeletionEvent,
                                  ModificationEvent)
from thesis.types import (ChangeType, ElementIdentifier, ElementType, FileName,
                          OSCInfo)

_logger = logging.getLogger(__name__)

# Singleton
class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(
        self, osm_conf_path: Optional[Path] = None, osm_max_tmpfile_size: int = 4000
    ):
        if not hasattr(self, "_initialized"):
            self._osm_conf_path = osm_conf_path
            self._osm_max_tmpfile_size = osm_max_tmpfile_size
            tmp_fd = None
            try:
                tmp_fd, osm_out_tmp = tempfile.mkstemp(suffix=".osm.pbf")
            finally:
                if tmp_fd:
                    os.close(tmp_fd)
            self._osm_out_tmp = osm_out_tmp
            self._initialized = True
        else:
            warnings.warn("Config already initialized. Skipping reinitialization.")

    @property
    def osm_conf_path(self) -> Optional[Path]:
        return self._osm_conf_path

    @property
    def osm_max_tmpfile_size(self) -> int:
        return self._osm_max_tmpfile_size


    @property
    def osm_out_tmp(self) -> str:
        return self._osm_out_tmp

def osm2gpkg(osm_file_path: str, gpkg_out_path: str):
    """Convert osm file to gpkg file using `ogr2ogr`.

    Requires `ogr2ogr` to be in $PATH.
    """
    _logger.info("Trying to convert OSM to GPKG")
    config = Config()
    OGR_CONFIG = {
        "OSM_MAX_TMPFILE_SIZE": str(config.osm_max_tmpfile_size),
    }

    if config.osm_conf_path:
        OGR_CONFIG["OSM_CONFIG_FILE"] = str(config.osm_conf_path.resolve())

    ogr2ogr_path = shutil.which("ogr2ogr")
    command = [
        ogr2ogr_path,
        "-f",
        "GPKG",
        "-if",
        "OSM",
        "-preserve_fid",
        "-overwrite",
        gpkg_out_path,
        osm_file_path,
    ]
    _logger.debug(
        f"Executing command: `{' '.join(command)}`. Using variables: {OGR_CONFIG}"
    )
    with (
        alive_bar(
            monitor=False,
            elapsed="{elapsed}",
            stats=False,
            monitor_end=False,
            stats_end=False,
            elapsed_end="Total time: {elapsed}",
            dual_line=True,
        ) as bar,
        subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=2,
            env=OGR_CONFIG,
        ) as proc,
    ):
        bar.title("osm2gpkg")
        while proc.poll() is None:
            bar()
            time.sleep(0.02)
        outb, errb = proc.communicate()
        outs, errs = outb.decode("utf-8"), errb.decode("utf-8")

        if len(outs) > 0:
            _logger.debug(f"Output from ogr2ogr: \n\t{outs}")

        if len(errs) > 0:
            _logger.error(f"Error from ogr2ogr: \n\t{errs}")
        else:
            _logger.info("ogr2ogr ran without errors.")
        _logger.info("Done with converting OSM to GPKG.")


def get_all_features(gpkg_fpath: FileName, layer_name: str):
    """Get all features from a layer in a gpkg file."""
    with ogr.Open(gpkg_fpath) as ds:
        layer = cast(ogr.Layer, ds.GetLayerByName(layer_name))
        return [cast(ogr.Feature, feat) for feat in layer]


def remove_layers(gpkg_file_path: str, *args: str):
    with ogr.Open(gpkg_file_path, 1) as ds:
        ds = cast(ogr.DataSource, ds)
        i = 0
        while i < ds.GetLayerCount():
            layer = cast(ogr.Layer, ds.GetLayer(i))
            if layer.GetName() in args:
                ds.DeleteLayer(i)
            else:
                i += 1


def _find_feature(
    ds: ogr.DataSource, identifier: ElementIdentifier
) -> ogr.Feature | None:
    """Find feature in data source."""
    # If entity_type is node, search in points layer.
    # If entity_type is way or relation, search in lines and linearrings layer.
    # If feature is not found, return None.
    match identifier.etype:
        case ElementType.NODE:
            layer = cast(ogr.Layer, ds.GetLayerByName("points"))
            point = cast(ogr.Feature | None, layer.GetFeature(identifier.id))
            if point:
                return point
            else:
                return None
        case ElementType.WAY | ElementType.RELATION:
            # Search in lines layer
            layer = cast(ogr.Layer, ds.GetLayerByName("lines"))
            line = cast(ogr.Feature | None, layer.GetFeature(identifier.id))
            if line:
                return line
            # Search in linearrings layer
            layer = cast(ogr.Layer, ds.GetLayerByName("linearrings"))
            polygon = cast(ogr.Feature | None, layer.GetFeature(identifier.id))
            if polygon:
                return polygon


_blacklist: list[ElementIdentifier] = []


def find_changes(
    prev_gpkg_path: str, curr_gpkg_path: str, osc_info: OSCInfo
) -> Sequence[CreationEvent | ModificationEvent | DeletionEvent]:
    """Find changes from two gpkg files.

    Uses inforamtion from an OSC file to find the features that have changed.
    """
    result: list[CreationEvent | ModificationEvent | DeletionEvent] = []
    with (
        cast(ogr.DataSource, ogr.Open(prev_gpkg_path, driver="GPKG")) as prev_ds,
        cast(ogr.DataSource, ogr.Open(curr_gpkg_path, driver="GPKG")) as curr_ds,
    ):
        _logger.info("Detecting changes.")
        # FIXME:
        # If a node that is referenced by a way or relation is updated with
        # new coordinates, it is not sertain that the way or relation will be
        # marked as "changed" in the OSC file. The same can be claimed about
        # a way that is referenced by a relation.
        # For this reason we need to iterate over all lines and polygons and
        # check if they have been changed.

        for change_info in osc_info:
            identifier = change_info.element_identifier
            if identifier in _blacklist:
                _logger.info(
                    f"Skipping {identifier.etype} with ID {identifier.id}. Found in blacklist."
                )
                continue
            if change_info.change_type is ChangeType.CREATE:
                _logger.info(
                    f"Processing creation of {identifier.etype} with ID {identifier.id}"
                )
                feature = _find_feature(curr_ds, identifier)
                if feature is None:
                    _logger.warning(
                        f"Could not find {identifier.etype.name} with ID {identifier.id} in gpkg file. Skipping diff and adding to blacklist."
                    )
                    _blacklist.append(identifier)
                    continue
                event = creation_event(feature)
            elif change_info.change_type is ChangeType.MODIFY:
                _logger.info(
                    f"Processing modification of {identifier.etype} with ID {identifier.id}"
                )
                feat1 = _find_feature(prev_ds, identifier)
                feat2 = _find_feature(curr_ds, identifier)
                if feat1 is None:
                    _logger.warning(
                        f"Could not find previous version of {identifier.etype.name} with ID {identifier.id} in gpkg file. Skipping diff and adding to blacklist."
                    )
                    _blacklist.append(identifier)
                    continue
                if feat2 is None:
                    _logger.warning(
                        f"Could not find current version of {identifier.etype.name} with ID {identifier.id} in gpkg file. Skipping diff and adding to blacklist."
                    )
                    _blacklist.append(identifier)
                    continue
                event = modification_event(feat1, feat2)
            elif change_info.change_type is ChangeType.DELETE:
                _logger.info(
                    f"Processing deletion of {identifier.etype} with ID {identifier.id}"
                )
                feature = _find_feature(prev_ds, identifier)
                if feature is None:
                    _logger.warning(
                        f"Could not find {identifier.etype.name} with ID {identifier.id} in gpkg file."
                    )
                    _blacklist.append(identifier)
                    continue
                event = deletion_event(feature)
            else:
                raise ValueError(f"Unexpected change type: {change_info.change_type}")

            result.append(event)

    return result


def osmium_apply_changes(osm_fpath: str, osc_fpath: str) -> None:
    """Apply changes from osc file to osm file.

    Overwrites the input osm file.
    Requires `osmium` to be in $PATH.
    """
    config = Config()
    osm_tmp_out = config.osm_out_tmp

    def get_command():
        osmium_cmd = shutil.which("osmium")
        return [ osmium_cmd,
            "apply-changes",
            "-f",
            "pbf",
            "--overwrite",
            "-o",
            osm_tmp_out,
            osm_fpath,
            osc_fpath,
        ]
    
    command = get_command()
    with (
        subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ) as proc,
        alive_bar(
            monitor=False,
            elapsed="{elapsed}",
            stats=False,
            monitor_end=False,
            stats_end=False,
            elapsed_end="Total time: {elapsed}",
        ) as bar
    ):
        _logger.info(f"Applying change file with: `{' '.join(command)}`")
        bar.title("Applying changes")
        while proc.poll() is None:
            bar()
            time.sleep(0.02)
        outs, errs = proc.communicate()

        if len(outs) > 0:
            _logger.debug("Output from osmium: \n", outs.decode("utf-8"))

        if len(errs) > 0:
            _logger.error("Error from osmium: \n", errs.decode("utf-8"))

        if proc.returncode != 0:
            raise RuntimeError(
                f"Applying changes failed with return code {proc.returncode}."
            )

    _logger.debug("Copying temporary osm file to output file.")
    shutil.copy(osm_tmp_out, osm_fpath)
    _logger.info(f"Applied changes and wrote to file: {osm_fpath}")
