from transform.matrix import (
    translation_matrix,
    rotation_matrix,
    scaling_matrix,
    multiply_matrices,
    transform_points,
)


class Transform:
    def __init__(self, pivot=(0.0, 0.0)):
        self.tx = 0.0
        self.ty = 0.0

        self.rotation = 0.0

        self.sx = 1.0
        self.sy = 1.0

        self.pivot = pivot


    def set_pivot(self, cx, cy):
        self.pivot = (cx, cy)

    def translate(self, dx, dy):
        self.tx += dx
        self.ty += dy

    def rotate(self, d_angle_degrees):
        self.rotation = (self.rotation + d_angle_degrees) % 360.0

    def scale(self, d_sx, d_sy):
        self.sx *= d_sx
        self.sy *= d_sy

    def set_translation(self, tx, ty):
        self.tx = tx
        self.ty = ty

    def set_rotation(self, angle_degrees):
        self.rotation = angle_degrees % 360.0

    def set_scale(self, sx, sy):
        self.sx = sx
        self.sy = sy

    def reset(self):
        self.tx = 0.0
        self.ty = 0.0
        self.rotation = 0.0
        self.sx = 1.0
        self.sy = 1.0


    def get_matrix(self):
        px, py = self.pivot

        to_origin = translation_matrix(-px, -py)
        scale = scaling_matrix(self.sx, self.sy)
        rotate = rotation_matrix(self.rotation)
        back_to_pivot = translation_matrix(px, py)
        move = translation_matrix(self.tx, self.ty)

        return multiply_matrices(move, back_to_pivot, rotate, scale, to_origin)

    def apply_to(self, vertices):
        matrix = self.get_matrix()
        return transform_points(matrix, vertices)

    def __repr__(self):
        return (f"Transform(tx={self.tx:.2f}, ty={self.ty:.2f}, "
                f"rotation={self.rotation:.2f}, sx={self.sx:.2f}, sy={self.sy:.2f})")
