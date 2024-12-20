import numpy as np
from .plotting import plot_tetrahedron, plot_2D_nuclear_density
from .tetrahedron_geometry import generate_random_tetrahedron, make_2D_projection
from .alpha_particle_generation import get_alpha_particle_hotspot_positions
from .grid_oxygen import make_b_grid, one_direction
from scipy.integrate import simpson as simps


def hotspot_profile(distances, params):
    # Calculate the hotspot profile
    Bhs = params['Bhs']
    # Convert Bhs to fm^2
    Bhs = Bhs * 0.19732697**2
    return np.exp(-distances**2/(2.*Bhs))/(2.*np.pi*Bhs)

def get_hotspot_centers(x, params):
    # Do the calculations
    vertices_rotated = generate_random_tetrahedron(params)
    vertices_2D = make_2D_projection(vertices_rotated)

    hotspots = []
    for vertex in vertices_2D:
        hotspots.append(get_alpha_particle_hotspot_positions(x, vertex))
    # convert hotspots to a 2D array merging the subarrays
    hotspots = np.concatenate(hotspots)

    return hotspots, vertices_2D, vertices_rotated

def generate_oxygen_hotspot_density(x, params):
    # Initialize the grid of b vectors
    grid_of_b_vecs = make_b_grid(params['n_of_bs'], params['b_max'])

    # Get the hotspot centers
    hotspots, vertices_2D, vertices_3D = get_hotspot_centers(x, params)

    distances = np.linalg.norm(grid_of_b_vecs - hotspots[:, np.newaxis, np.newaxis, :], axis=3)
    stacked_hotspot_profiles = (hotspot_profile(distances, params).T).T
    return np.sum(stacked_hotspot_profiles, axis=0), hotspots, vertices_2D, vertices_3D


def get_density(n_of_bs=200, b_max=6., tetrahedron_length=3.42, tetrahedron_spread=0.1, Bhs=0.8, x=0.01, seed=None, plot=False, positions=False):
    params = {
        'n_of_bs': n_of_bs,
        'b_max': b_max,  # fm
        'tetrahedron_length': tetrahedron_length,  # [fm]
        'tetrahedron_spread': tetrahedron_spread,  # [fm] gaussian sigma
        # Hotspot parameters
        'Bhs': Bhs,  # GeV^-2
    }

    if seed is not None:
        np.random.seed(seed)

    density, hotspots, vertices_2D, vertices_3D = generate_oxygen_hotspot_density(x, params)
    # normalize the density to one
    single_axis = one_direction(params['n_of_bs'], params['b_max'])
    integral = simps(simps(density, x=single_axis), x=single_axis)
    density = density / integral
    # Plot the 3D density
    if plot:
        plot_tetrahedron(vertices_3D, hotspots)
        plot_2D_nuclear_density(density, params)

    if positions:
        return hotspots, vertices_2D, vertices_3D
    else:
        return single_axis, density



