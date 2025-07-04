from pigeon import BaseMessage
from . import buffer, camera, montage, qc, roi, scope, stage, tile, ui, calibration


class State(BaseMessage):
    state: str


topics = {
    "buffer.status": buffer.Status,
    "camera.command": camera.Command,
    "camera.image": camera.Image,
    "camera.settings": camera.Settings,
    "camera.status": camera.Status,
    "scope.command": scope.Command,
    "scope.status": scope.Status,
    "stage.aperture.command": stage.aperture.Command,
    "stage.aperture.status": stage.aperture.Status,
    "stage.motion.command": stage.motion.Command,
    "stage.motion.status": stage.motion.Status,
    "stage.rotation.command": stage.rotation.Command,
    "stage.rotation.status": stage.rotation.Status,
    "tile.preview": tile.Preview,
    "tile.mini": tile.Mini,
    "tile.processed": tile.Processed,
    "tile.raw": tile.Raw,
    "tile.statistics.focus": tile.statistics.Focus,
    "tile.statistics.histogram": tile.statistics.Histogram,
    "tile.statistics.min_max_mean": tile.statistics.MinMaxMean,
    "tile.transform": tile.Transform,
    "ui.edit": ui.Edit,
    "ui.run": ui.Run,
    "ui.setup": ui.Setup,
    "montage.complete": montage.Complete,
    "qc.status": qc.Status,
    "roi.load": roi.LoadROI,
    "roi.create": roi.CreateROI,
    "roi.current": roi.ROI,
    "montage.minimaps": montage.Minimaps,
    "calibration.resolution": calibration.Resolution,
    "calibration.centroid": calibration.Centroid,
    "state": State,
}
