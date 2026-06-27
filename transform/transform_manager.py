from enum import Enum

from transform.transform import Transform  # noqa: F401  (re-exported for convenience)


class TransformMode(Enum):
    NONE = "none"
    TRANSLATE = "translate"
    ROTATE = "rotate"
    SCALE = "scale"


def compute_centroid(vertices):
    if not vertices:
        return (0.0, 0.0)
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


class TransformManager:
    def __init__(self, selection_manager=None):
        self.selection_manager = selection_manager

        self.mode = TransformMode.TRANSLATE
        self._dragging = False
        self._last_mouse = (0.0, 0.0)

        self.rotate_sensitivity = 0.5   # degrees per pixel of horizontal drag
        self.scale_sensitivity = 0.01   # scale change per pixel of drag


    def set_mode(self, mode: TransformMode):
        self.mode = mode

    def cycle_mode(self):
        order = [TransformMode.TRANSLATE, TransformMode.ROTATE, TransformMode.SCALE]
        idx = order.index(self.mode) if self.mode in order else 0
        self.mode = order[(idx + 1) % len(order)]


    def _get_selected_shape(self):
        if self.selection_manager is None:
            return None
        return getattr(self.selection_manager, "selected_shape", None)

    def _ensure_pivot(self, shape):
        if shape.transform.pivot == (0.0, 0.0) and shape.vertices:
            shape.transform.set_pivot(*compute_centroid(shape.vertices))


    def begin_drag(self, mouse_x, mouse_y, shape=None):
        target = shape or self._get_selected_shape()
        if target is None:
            return
        self._ensure_pivot(target)
        self._dragging = True
        self._last_mouse = (mouse_x, mouse_y)

    def update_drag(self, mouse_x, mouse_y, shape=None):
        if not self._dragging:
            return

        target = shape or self._get_selected_shape()
        if target is None:
            return

        last_x, last_y = self._last_mouse
        dx = mouse_x - last_x
        dy = mouse_y - last_y

        if self.mode == TransformMode.TRANSLATE:
            target.transform.translate(dx, dy)

        elif self.mode == TransformMode.ROTATE:
            target.transform.rotate(dx * self.rotate_sensitivity)

        elif self.mode == TransformMode.SCALE:
            factor = 1.0 + (dx - dy) * self.scale_sensitivity
            factor = max(0.05, factor)  
            target.transform.scale(factor, factor)

        self._last_mouse = (mouse_x, mouse_y)

    def end_drag(self):
        self._dragging = False

    def nudge_translate(self, dx, dy, shape=None):
        target = shape or self._get_selected_shape()
        if target is None:
            return
        target.transform.translate(dx, dy)

    def nudge_rotate(self, d_angle, shape=None):
        target = shape or self._get_selected_shape()
        if target is None:
            return
        self._ensure_pivot(target)
        target.transform.rotate(d_angle)

    def nudge_scale(self, factor, shape=None):
        target = shape or self._get_selected_shape()
        if target is None:
            return
        self._ensure_pivot(target)
        target.transform.scale(factor, factor)

    def reset_transform(self, shape=None):
        target = shape or self._get_selected_shape()
        if target is None:
            return
        target.transform.reset()
