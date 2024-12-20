import numpy as np

# * Generate random orientation of the tetrahedron (two angles)
def generate_random_orientation():
    # The angles are generated randomly
    theta = np.random.rand() * np.pi
    phi = np.random.rand() * 2 * np.pi
    return theta, phi

# * Generate four vectors pointing the edges of a tetrahedron with a fixed arm length
def generate_random_tetrahedron(params):
    sigma = params['tetrahedron_spread']
    # The tetrahedron has a fixed arm length
    # Distance between two vertices is np.sqrt(4*x_shift**2 + 4*x_shift**2) = 2*np.sqrt(2)*x_shift
    # That is why I need to divide the arm length by 2
    r = params['tetrahedron_length'] / (2. * np.sqrt(2))
    V0 = np.array([r, r, r])
    V1 = np.array([-r, -r, r])
    V2 = np.array([-r, r, -r])
    V3 = np.array([r, -r, -r])
    # distance between two edges is

    # List of vertices
    vertices = [V0, V1, V2, V3]

    # Move each vertex by a random amount given by a Gaussian distribution
    for vertex in vertices:
        vertex += np.random.normal(0., sigma, 3)

    # Generate random orientation of the tetrahedron
    theta, phi = generate_random_orientation()

    return rotate_tetrahedron(theta, phi, vertices)

def rotate_tetrahedron(theta, phi, vertices):
    # Rotate the tetrahedron by the angles
    Rz = np.array([
        [np.cos(phi), -np.sin(phi), 0],
        [np.sin(phi), np.cos(phi), 0],
        [0, 0, 1]
    ])

    Ry = np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

    R = Ry @ Rz  # Combined rotation matrix

    # Apply rotation to each vertex
    vertices_rotated = []
    for i in range(len(vertices)):
        vertices_rotated.append(R.dot(vertices[i]))
    return vertices_rotated

def make_2D_projection(vertices):
    # drop the z-coordinate
    vertices_2D = []
    for vertex in vertices:
        vertices_2D.append(vertex[:2])
    return vertices_2D

