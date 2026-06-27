import math


def identity_matrix():
    return [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]


def translation_matrix(tx, ty):
    m = identity_matrix()
    m[0][2] = tx
    m[1][2] = ty
    return m


def rotation_matrix(angle_degrees):
    theta = math.radians(angle_degrees)
    c, s = math.cos(theta), math.sin(theta)
    m = identity_matrix()
    m[0][0] = c
    m[0][1] = -s
    m[1][0] = s
    m[1][1] = c
    return m


def scaling_matrix(sx, sy):
    m = identity_matrix()
    m[0][0] = sx
    m[1][1] = sy
    return m


def matmul(a, b):
    result = [[0.0, 0.0, 0.0] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            result[i][j] = sum(a[i][k] * b[k][j] for k in range(3))
    return result


def multiply_matrices(*matrices):
    result = identity_matrix()
    for m in matrices:
        result = matmul(result, m)
    return result


def transform_point(matrix, x, y):
    px = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2]
    py = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2]
    return (px, py)


def transform_points(matrix, vertices):
    return [transform_point(matrix, x, y) for (x, y) in vertices]


def to_opengl_array(matrix):
    a, b, tx = matrix[0]
    c, d, ty = matrix[1]
    return [
        a,   c,   0.0, 0.0,
        b,   d,   0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        tx,  ty,  0.0, 1.0,
    ]
