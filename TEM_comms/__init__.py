from . import buffer
from . import camera
from . import scope
from . import stage
from . import tile
from . import ui
from . import montage
from . import qc


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
    "tile.minimap": tile.Minimap,
    "tile.processed": tile.Processed,
    "tile.raw": tile.Raw,
    "tile.statistics.focus": tile.statistics.Focus,
    "tile.statistics.histogram": tile.statistics.Histogram,
    "tile.statistics.min_max_mean": tile.statistics.MinMaxMean,
    "tile.transform": tile.Transform,
    "ui.edit": ui.Edit,
    "ui.run": ui.Run,
    "ui.setup": ui.Setup,
    "montage.start": montage.Start,
    "montage.finished": montage.Finished,
    "qc.status": qc.Status,
}
