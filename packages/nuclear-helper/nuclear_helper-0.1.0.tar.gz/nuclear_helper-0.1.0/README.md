# Nuclear Hot-Spot Model Library

This Python library provides tools to generate and analyze the stochastic structure of atomic nuclei including the "hot-spot" model density. It is designed for use in nuclear physics and Quantum Chromodynamics (QCD) calculations. The library currently supports an oxygen nucleus modeled as a tetrahedron of alpha-clusters, with plans to expand to other nuclei and models in future releases.

## Features

- **3D Nuclear Structure Generation:**  
  Generate a 3D configuration of constituent hadrons (and hot-spots) within the nucleus.
  
- **2D Transverse Plane Projection:**  
  Project the 3D nuclear structure onto a 2D transverse plane for simplified analysis.
  
- **Density Calculation:**  
  Compute a spatial density map of hot-spots and normalize it to unity.
  
- **Plotting Capabilities:**  
  Visualize the 3D arrangement of hot-spots and their density distribution in 2D.
  
- **Random Seed Control:**  
  Set a seed for reproducible, deterministic configurations—useful for debugging and consistency checks.

## Installation

**Dependencies:**
- [NumPy](https://numpy.org/)
- [SciPy](https://www.scipy.org/)
- [Matplotlib](https://matplotlib.org/) (for plotting)
- Additional dependencies may be listed in `requirements.txt`.

## Usage

The main function provided by this library is `get_density`, which computes the hot-spot density distribution for the oxygen nucleus.

**Function Signature:**
```python
def get_density(
    n_of_bs=200,
    b_max=6.0,
    tetrahedron_length=3.42,
    tetrahedron_spread=0.1,
    Bhs=0.8,
    x=0.01,
    seed=None,
    plot=False,
    positions=False
):
    ...
```

### Parameters and Default Values

- **n_of_bs (int, default=200)**:  
  Number of discrete points in each dimension of the 2D grid for density calculation.

- **b_max (float, default=6.0)**:  
  The maximum extent from the center of the nucleus of the spatial grid in femtometers (fm).

- **tetrahedron_length (float, default=3.42)**:  
  The typical size scale (in fm) of the tetrahedral arrangement of alpha-clusters inside the nucleus.

- **tetrahedron_spread (float, default=0.1)**:  
  The standard deviation (in fm) describing fluctuations in the positions of the clusters.

- **Bhs (float, default=0.8)**:  
  The hot-spot size parameter (in GeV^-2).

- **x (float, default=0.01)**:  
  The Bjorken-x variable related to the partonic structure of the nucleus.

- **seed (int or None, default=None)**:  
  Seed for the random number generator. If `None`, a random seed is used.

- **plot (bool, default=False)**:  
  If `True`, the code produces a 3D plot of hadron positions and a 2D density contour plot.

- **positions (bool, default=False)**:  
  If `True`, returns the hadron positions and tetrahedron vertices instead of the density array.

### Basic Example

```python
import numpy as np
from nuclear_helper.oxygen import get_density

# Compute the density with default parameters and plot the results
axis, density = get_density(plot=True)

print("Axis shape:", axis.shape)
print("Density shape:", density.shape)
```

This will generate:
- A 3D visualization of the constituent hadrons arranged in a tetrahedral pattern.
- A 2D contour plot showing the normalized nuclear hot-spot density.

### Setting a Random Seed

To ensure reproducible results, set the `seed` parameter:

```python
from nuclear_helper.oxygen import get_density

# Generate a density map with a fixed seed for debugging and reproducibility
axis, density = get_density(seed=42, plot=False)
```

### Accessing Hot-Spot Positions

If you need the 3D coordinates of hadrons or the projected 2D coordinates of the tetrahedron vertices, use `positions=True`:

```python
from nuclear_helper.oxygen import get_density

hotspots, vertices_2D, vertices_3D = get_density(positions=True)
print("Hotspots shape:", hotspots.shape)
print("2D vertices shape:", vertices_2D.shape)
print("3D vertices shape:", vertices_3D.shape)
```

### Changing Parameters

You can vary parameters like `b_max` or `n_of_bs` to adjust the resolution and size of the grid:

```python
from nuclear_helper.oxygen import get_density

# Increase the resolution and maximum grid size
axis, density = get_density(n_of_bs=300, b_max=8.0, plot=True)
```

### Future Work

- **Additional Nuclei:**  
  We plan to add support for other nuclei beyond oxygen, allowing for more general nuclear structure studies.
  
- **Improved Physical Models:**  
  The library will incorporate more sophisticated models of QCD and nuclear structure as it evolves.
  
- **Integrations and Utilities:**  
  Integration with external physics frameworks and utilities for statistical analyses are planned.

## Contributing

Contributions are welcome! Please open an issue or submit a merge request to discuss changes and improvements.

## License

This project is licensed under the [GNU License](LICENSE).
