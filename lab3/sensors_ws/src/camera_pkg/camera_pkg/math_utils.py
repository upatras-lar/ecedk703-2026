import numpy as np

def rot_to_quat(R: np.ndarray):
    """
    Convert a 3x3 rotation matrix to a quaternion (x, y, z, w).
    Handles small numerical errors robustly.
    """

    R = np.asarray(R, dtype=float)

    m00, m01, m02 = R[0, 0], R[0, 1], R[0, 2]
    m10, m11, m12 = R[1, 0], R[1, 1], R[1, 2]
    m20, m21, m22 = R[2, 0], R[2, 1], R[2, 2]

    trace = m00 + m11 + m22

    if trace > 0.0:
        # qw is largest
        t = trace + 1.0
        s = 0.5 / np.sqrt(max(t, 1e-16))   # 's' is 1/(4*qw)
        qw = 0.25 / s
        qx = (m21 - m12) * s
        qy = (m02 - m20) * s
        qz = (m10 - m01) * s
    elif m00 > m11 and m00 > m22:
        # qx is largest
        t = 1.0 + m00 - m11 - m22
        s = 0.5 / np.sqrt(max(t, 1e-16))
        qw = (m21 - m12) * s
        qx = 0.25 / s
        qy = (m01 + m10) * s
        qz = (m02 + m20) * s
    elif m11 > m22:
        # qy is largest
        t = 1.0 + m11 - m00 - m22
        s = 0.5 / np.sqrt(max(t, 1e-16))
        qw = (m02 - m20) * s
        qx = (m01 + m10) * s
        qy = 0.25 / s
        qz = (m12 + m21) * s
    else:
        # qz is largest
        t = 1.0 + m22 - m00 - m11
        s = 0.5 / np.sqrt(max(t, 1e-16))
        qw = (m10 - m01) * s
        qx = (m02 + m20) * s
        qy = (m12 + m21) * s
        qz = 0.25 / s

    q = np.array([qx, qy, qz, qw])

    norm = np.linalg.norm(q)
    if norm < 1e-16:
        return np.array([0.0, 0.0, 0.0, 1.0])

    return q / norm