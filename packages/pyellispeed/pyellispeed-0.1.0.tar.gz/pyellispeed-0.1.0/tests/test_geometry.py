import numpy as np
from pyellispeed import geometry
from pyellispeed import geometry_rs
import json

def test_generate_rotation_matrix():

    with open("tests/data/rotation_matrix.json", "r") as f:
        loaded_json = json.load(f)

    loaded_data = {eval(key): np.array(value) for key, value in loaded_json.items()}

    for angles, expected_value in loaded_data.items():

        angles_rad = np.deg2rad(angles)
        matrix = geometry_rs.build_rotation_matrix(*angles_rad)

        assert (
            np.allclose(matrix, expected_value, rtol=1e-5),
            f"Rotation matrix:\n"
            f"{matrix}\n"
            f"does not match for {angles} expected result:\n"
            f"{expected_value}"
        )

def test_get_angles_from_rotation_matrix():
    with open("tests/data/rotation_matrix.json", "r") as f:
        loaded_json = json.load(f)

    loaded_data = {eval(key): np.array(value) for key, value in loaded_json.items()}

    for expected_angles, matrix in loaded_data.items():

        expected_angles_rad = np.deg2rad(expected_angles)
        angles = geometry_rs.rotation_matrix_to_angles(matrix)
        angles_deg = np.rad2deg(angles)

        assert (
            np.allclose(angles, expected_angles_rad, rtol=1e-5),
            f"Angles:\n"
            f"{angles_deg}\n"
            f"does not match for {matrix} expected result:\n"
            f"{expected_angles}"
        )

def test_relative_vector_rotation():
    angle_xyz = np.deg2rad([0, 0, 45])
    src_vec = [0, 1, 0]
    exp_vec = [-0.70710678, 0.70710678, 0.]

    # Build rotation matrix and transform the src_vector
    rotm = geometry_rs.build_rotation_matrix(*angle_xyz)
    res_vec = np.dot(rotm, src_vec)

    # Validate
    err = np.linalg.norm(res_vec - exp_vec)
    assert err < 1e-5

    # Find rotation matrix between source and res vector
    found_rotm = geometry.find_relative_vector_rotation(src_vec, exp_vec)

    # Extract Euler angles
    found_angles = geometry_rs.rotation_matrix_to_angles(found_rotm)

    # Validate
    err = np.linalg.norm(found_angles - angle_xyz)
    assert err < 1e-5

def test_sequence():
    angles = np.deg2rad([
        [0, 10, 0], [0, 10, 0], [0, 10, 5], [0, 10, 5], [0, 0, -5]
    ])
    vectors = [np.array([0, 0, 1])]
    for entry in angles:
        rotm = geometry_rs.build_rotation_matrix(*entry)
        vectors.append(np.dot(rotm, vectors[-1].T))

    for src_vec, dst_vec in zip(vectors, vectors[1:]):
        rotm = geometry.find_relative_vector_rotation(src_vec, dst_vec)
        res_vec = np.dot(rotm, src_vec.T)
        res_vec = res_vec.squeeze()
        err = np.linalg.norm(res_vec - dst_vec)
        assert err < 1e-5

def test_relative_axes_rotation():
    original_axes = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    rot_angles = np.deg2rad([60, 30, 45])  # Rotate around Z-axis by 45 deg

    # Build rotation matrix and rotate the axes
    rotm = geometry_rs.build_rotation_matrix(*rot_angles)
    rotated_axes = np.dot(rotm, original_axes.T).T

    # Find relative rotation
    rel_rotm = geometry.find_relative_axes_rotation(original_axes, rotated_axes)

    # Validate relative rotation matrix
    rel_rotated_axes = np.dot(rel_rotm, original_axes.T).T

    # Validate
    err = np.linalg.norm(rotated_axes - rel_rotated_axes)
    assert err < 1e-5

def test_scalar_projection():
    source = [1, 0, 0]
    target = [1, 0, 0]
    proj = geometry.scalar_projection(source, target)
    assert proj == 1

    # Build rotation matrices and transform the source vector
    angle_xyz = np.deg2rad([0, 0, 30])
    rotm = geometry_rs.build_rotation_matrix(*angle_xyz)
    source_30 = np.dot(rotm, source)

    angle_xyz = np.deg2rad([0, 0, 60])
    rotm = geometry_rs.build_rotation_matrix(*angle_xyz)
    source_60 = np.dot(rotm, source)

    proj_30 = abs(geometry.scalar_projection(source_30, target))
    proj_60 = abs(geometry.scalar_projection(source_60, target))

    assert proj_30 > proj_60

def validate_vectors_mapping(angles, radii, expected):
    target = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    # Rotate
    rotm = geometry_rs.build_rotation_matrix(*angles)
    source = [np.dot(rotm, v) for v in target]
    # Sort vectors order to mimic SVD
    source = [v for _, v in sorted(zip(radii, source), reverse=True)]
    # Find mapping and validate it
    indices = geometry.find_vectors_mapping(source, target)
    assert indices == expected

def test_find_vectors_mapping():
    radii = [30, 60, 20]
    validate_vectors_mapping(np.deg2rad([0, 0, 0]), radii, [1, 0, 2])
    validate_vectors_mapping(np.deg2rad([0, 0, 30]), radii, [1, 0, 2])
    validate_vectors_mapping(np.deg2rad([30, 0, 0]), radii, [1, 0, 2])
    validate_vectors_mapping(np.deg2rad([0, 30, 0]), radii, [1, 0, 2])

    # Due to the rotation, the axis along Y becomes along X, and vice versa.
    # For this reason the most elongated axis will be along X.
    validate_vectors_mapping(np.deg2rad([0, 0, 80]), radii, [0, 1, 2])

    # X`Y`Z` -> rotation -> Z`Y`X` [Z` is along X, X` is along Z] -->
    # The ellipsoid is most elongated along Y, and then along Z...
    validate_vectors_mapping(np.deg2rad([0, 80, 0]), radii, [1, 2, 0])

    # X`Y`Z` -> rotation -> X`Z`Y` [Y` is along Z, Z` is along Y] -->
    # The ellipsoid is most elongated along Z, and next along X...
    validate_vectors_mapping(np.deg2rad([80, 0, 0]), radii, [2, 0, 1])

    # X`Y`Z` -> rotation #1 -> Y`X`Z` -> rotation #2 -> Z`X`Y` -->
    # The ellipsoid is most elongated along Z, and next along Y...
    validate_vectors_mapping(np.deg2rad([80, 0, 80]), radii, [2, 1, 0])

    # X`Y`Z` -> rotation #1 -> X`Z`Y` -> rotation #2 -> X`Z`Y` --> rotation #3 -> X`Z`Y`
    # The ellipsoid is most elongated along Z, and next along X...
    validate_vectors_mapping(np.deg2rad([80, 30, 10]), radii, [2, 0, 1])

    # X`Y`Z` -> rotation #1 -> X`Z`Y` -> rotation #2 -> X`Z`Y` --> rotation #3 -> Z`X`Y`
    # The ellipsoid is most elongated along Z, and next along X...
    validate_vectors_mapping(np.deg2rad([80, 30, 80]), radii, [2, 1, 0])
