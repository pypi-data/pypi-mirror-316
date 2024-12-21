import os
import numpy as np
from typing import Union
from zacrostools.simulation_input import parse_simulation_input_file
from zacrostools.general_output import parse_general_output_file
from zacrostools.specnum_output import parse_specnum_output_file
from zacrostools.custom_exceptions import enforce_types, KMCOutputError, EnergeticsModelError


class KMCOutput:
    """
    A class that represents a KMC (Kinetic Monte Carlo) simulation output.

    Attributes
    ----------
    n_gas_species : int
        Number of gas species.
    gas_specs_names : List[str]
        Gas species names.
    n_surf_species : int
        Number of surface species.
    surf_specs_names : List[str]
        Surface species names.
    n_sites : int
        Total number of lattice sites.
    area : float
        Lattice surface area (in Å²).
    site_types : Dict[str, int]
        Site type names and total number of sites of that type.
    nevents : np.ndarray
        Number of events occurred.
    time : np.ndarray
        Simulated time (in seconds).
    finaltime : float
        Final simulated time (in seconds).
    energy : np.ndarray
        Lattice energy (in eV·Å⁻²).
    av_energy : float
        Average lattice energy (in eV·Å⁻²).
    final_energy : float
        Final lattice energy (in eV·Å⁻²).
    production : Dict[str, np.ndarray]
        Gas species produced over time. Example: `KMCOutput.production['CO']`.
    total_production : Dict[str, float]
        Total number of gas species produced. Example: `KMCOutput.total_production['CO']`.
    tof : Dict[str, float]
        TOF (Turnover Frequency) of gas species (in molecules·s⁻¹·Å⁻²). Example: `KMCOutput.tof['CO2']`.
    coverage : Dict[str, np.ndarray]
        Coverage of surface species over time (in %). Example: `KMCOutput.coverage['CO']`.
    av_coverage : Dict[str, float]
        Average coverage of surface species (in %). Example: `KMCOutput.av_coverage['CO']`.
    total_coverage : np.ndarray
        Total coverage of surface species over time (in %).
    av_total_coverage : float
        Average total coverage of surface species (in %).
    dominant_ads : str
        Most dominant surface species, used for plotting kinetic phase diagrams.
    coverage_per_site_type : Dict[str, Dict[str, np.ndarray]]
        Coverage of surface species per site type over time (in %).
    av_coverage_per_site_type : Dict[str, Dict[str, float]]
        Average coverage of surface species per site type (in %).
    total_coverage_per_site_type : Dict[str, np.ndarray]
        Total coverage of surface species per site type over time (in %). Example: `KMCOutput.total_coverage_per_site_type['top']`.
    av_total_coverage_per_site_type : Dict[str, float]
        Average total coverage of surface species per site type (in %).
    dominant_ads_per_site_type : Dict[str, str]
        Most dominant surface species per site type, used for plotting kinetic phase diagrams.
    """

    def __init__(self, path: str, analysis_range: Union[list, None] = None, range_type: str = 'time',
                 weights: Union[str, None] = None):
        """
        Initialize the KMCOutput object by parsing simulation output files.

        Parameters
        ----------
        path : str
            The path where the output files are located.
        analysis_range : List[float], optional
            A list of two elements `[start_percent, end_percent]` specifying the portion of the entire simulation
            to consider for analysis. The values should be between 0 and 100, representing percentages of the
            total simulated time or the total number of events, depending on `range_type`. For example,
            `[50, 100]` would analyze only the latter half of the simulation. Default is `[0.0, 100.0]`.
        range_type : str, optional
            Determines the dimension used when applying `analysis_range`:
            - `'time'`: The percentages in `analysis_range` refer to segments of the total simulated time.
            - `'nevents'`: The percentages in `analysis_range` refer to segments of the total number of simulated events.
            Default is `'time'`.
        weights : str, optional
            Weights for calculating weighted averages. Possible values are `'time'`, `'nevents'`, or `None`.
            If `None`, all weights are set to 1. Default value is `None`.
        """

        self.path = path
        if analysis_range is None:
            analysis_range = [0.0, 100.0]

        # Parse relevant data from the simulation_input.dat file
        data_simulation = parse_simulation_input_file(
            input_file=f'{path}/simulation_input.dat')

        self.random_seed = data_simulation['random_seed']
        self.temperature = data_simulation['temperature']
        self.pressure = data_simulation['pressure']
        self.n_gas_species = data_simulation['n_gas_species']
        self.gas_specs_names = data_simulation['gas_specs_names']
        self.gas_molar_fracs = data_simulation['gas_molar_fracs']
        self.n_surf_species = data_simulation['n_surf_species']
        self.surf_specs_names = data_simulation['surf_specs_names']
        self.surf_specs_dent = data_simulation['surf_specs_dent']

        # Parse relevant data from the general_output.txt file
        data_general = parse_general_output_file(
            output_file=f'{path}/general_output.txt')

        self.n_sites = data_general['n_sites']
        self.area = data_general['area']
        self.site_types = data_general['site_types']

        # Parse relevant data from the specnum_output.txt file
        data_specnum, header = parse_specnum_output_file(
            output_file=f'{path}/specnum_output.txt',
            analysis_range=analysis_range,
            range_type=range_type)

        self.nevents = data_specnum[:, 1]
        self.time = data_specnum[:, 2]
        self.finaltime = data_specnum[-1, 2]
        self.energy = data_specnum[:, 4] / self.area  # in eV/Å2
        self.energyslope = abs(np.polyfit(self.nevents, self.energy, 1)[0])  # in eV/Å2/step
        self.final_energy = data_specnum[-1, 4] / self.area
        self.av_energy = self.get_average(array=self.energy, weights=weights)

        # Compute production and TOF
        self.production = {}  # in molecules
        self.total_production = {}  # useful when calculating selectivity (i.e., set min_total_production)
        self.tof = {}  # in molecules·s⁻¹·Å⁻²
        for i in range(5 + self.n_surf_species, len(header)):
            gas_spec = header[i]
            self.production[gas_spec] = data_specnum[:, i]
            self.total_production[gas_spec] = data_specnum[-1, i] - data_specnum[0, i]
            if len(data_specnum) > 1 and data_specnum[-1, i] != 0:
                # If the catalyst is poisoned, it could be that the last ∆t is very high and the time window only
                # contains one row. In that case (len(data_specnum) == 1), set tof = 0
                self.tof[header[i]] = np.polyfit(data_specnum[:, 2], data_specnum[:, i], 1)[0] / self.area
            else:
                self.tof[header[i]] = 0.00

        # Compute coverages (per total number of sites)
        surf_specs_data = get_surf_specs_data(self.path)
        self.coverage = {}
        self.av_coverage = {}
        for i in range(5, 5 + self.n_surf_species):
            surf_spec = header[i].replace('*', '')
            num_dentates = surf_specs_data[surf_spec]['surf_specs_dent']
            self.coverage[surf_spec] = data_specnum[:, i] * num_dentates / self.n_sites * 100
            self.av_coverage[surf_spec] = self.get_average(array=self.coverage[surf_spec], weights=weights)
        self.total_coverage = sum(self.coverage.values())
        self.av_total_coverage = min(sum(self.av_coverage.values()), 100)  # prevent numerical errors over 100%
        self.dominant_ads = max(self.av_coverage, key=self.av_coverage.get)

        # Compute partial coverages (per total number of sites of a given type)
        self.coverage_per_site_type = {}
        self.av_coverage_per_site_type = {}
        for site_type in self.site_types:
            self.coverage_per_site_type[site_type] = {}
            self.av_coverage_per_site_type[site_type] = {}
        for i in range(5, 5 + self.n_surf_species):
            surf_spec = header[i].replace('*', '')
            site_type = surf_specs_data[surf_spec]['site_type']
            num_dentates = surf_specs_data[surf_spec]['surf_specs_dent']
            self.coverage_per_site_type[site_type][surf_spec] = (
                    data_specnum[:, i] * num_dentates / self.site_types[site_type] * 100
            )
            self.av_coverage_per_site_type[site_type][surf_spec] = self.get_average(
                array=self.coverage_per_site_type[site_type][surf_spec],
                weights=weights
            )
        self.total_coverage_per_site_type = {}
        self.av_total_coverage_per_site_type = {}
        self.dominant_ads_per_site_type = {}
        for site_type in self.site_types:
            if len(self.av_coverage_per_site_type[site_type]) > 0:
                self.total_coverage_per_site_type[site_type] = sum(self.coverage_per_site_type[site_type].values())
                self.av_total_coverage_per_site_type[site_type] = min(
                    sum(self.av_coverage_per_site_type[site_type].values()), 100)  # prevent numerical errors over 100%
                self.dominant_ads_per_site_type[site_type] = max(
                    self.av_coverage_per_site_type[site_type],
                    key=self.av_coverage_per_site_type[site_type].get)
            else:  # No species are adsorbed on this site type
                self.total_coverage_per_site_type[site_type] = np.zeros_like(self.time)
                self.av_total_coverage_per_site_type[site_type] = 0.0
                self.dominant_ads_per_site_type[site_type] = None

    def get_average(self, array, weights):
        """
        Calculate the average of an array with optional weighting.

        Parameters
        ----------
        array : np.ndarray
            The array of values to average.
        weights : str or None
            The weights to apply when calculating the average. Possible values are:
            - `None`: No weighting; all weights are set to 1.
            - `'time'`: Weights based on the differences in simulated time.
            - `'nevents'`: Weights based on the differences in the number of events.

        Returns
        -------
        float
            The calculated average value.
        """
        if weights not in [None, 'time', 'nevents']:
            raise KMCOutputError(f"'weights' must be one of the following: 'none' (default), 'time', or 'nevents'.")

        if len(array) == 1:
            # If the catalyst is poisoned, it could be that the last ∆t is very high and the time window only
            # contains one row. In that case (len(array) == 1), do not compute the average
            return array
        else:
            if weights is None:
                return np.average(array)
            elif weights == 'time':
                return np.average(array[1:], weights=np.diff(self.time))
            elif weights == 'nevents':
                return np.average(array[1:], weights=np.diff(self.nevents))

    @enforce_types
    def get_selectivity(self, main_product: str, side_products: list):
        """
        Calculate the selectivity of the main product over side products.

        Parameters
        ----------
        main_product : str
            Name of the main product.
        side_products : List[str]
            Names of the side products.

        Returns
        -------
        float
            The selectivity of the main product (in %) over the side products.

        Notes
        -----
        The selectivity is calculated as:
            selectivity = (TOF_main_product / (TOF_main_product + sum(TOF_side_products))) * 100

        If the total TOF is zero, the selectivity is returned as NaN.
        """
        selectivity = float('NaN')
        tof_side_products = 0.0
        for side_product in side_products:
            tof_side_products += self.tof[side_product]
        if self.tof[main_product] + tof_side_products != 0:
            selectivity = self.tof[main_product] / (self.tof[main_product] + tof_side_products) * 100
        return selectivity


def get_surf_specs_data(path):
    """
    Retrieve surface species data including the number of dentates and the associated site type for each species.

    Parameters
    ----------
    path : str
        The path to the directory containing the simulation input files (`simulation_input.dat` and `energetics_input.dat`).

    Returns
    -------
    dict
        A dictionary mapping each surface species name to its data, including:
        - 'surf_specs_dent': int
            Number of dentates required by the species.
        - 'site_type': str
            The site type on which the species adsorbs.
    """

    # Get data from simulation_input.dat
    parsed_sim_data = parse_simulation_input_file(input_file=f"{path}/simulation_input.dat")
    surf_specs_names = parsed_sim_data.get('surf_specs_names')
    surf_specs_dent = parsed_sim_data.get('surf_specs_dent')
    species_dentates = dict(zip(surf_specs_names, surf_specs_dent))
    species_in_simulation = set(surf_specs_names)

    surf_specs_data = {}

    # Check if the user is using a default lattice or not
    default_lattice = check_default_lattice(path)

    if default_lattice:
        for species in surf_specs_names:
            surf_specs_data[species] = {
                'surf_specs_dent': species_dentates[species],
                'site_type': 'StTp1'
            }

    else:

        with open(os.path.join(path, 'energetics_input.dat'), 'r') as f:
            lines = f.readlines()

        species_site_types = {}
        num_lines = len(lines)
        i = 0
        while i < num_lines:
            line = lines[i].strip()
            if line.startswith('cluster'):
                cluster_species = []
                site_types = []
                i += 1
                while i < num_lines:
                    line = lines[i].strip()
                    if line.startswith('end_cluster'):
                        break
                    elif line.startswith('lattice_state'):
                        # Process lattice_state block
                        i += 1  # Move to the next line after 'lattice_state'
                        while i < num_lines:
                            line = lines[i].strip()
                            if not line or line.startswith('#'):
                                i += 1
                                continue
                            if line.startswith('site_types') or line.startswith('cluster_eng') or line.startswith(
                                    'neighboring') or line.startswith('end_cluster'):
                                break  # End of lattice_state block
                            tokens = line.split()
                            if tokens and tokens[0].isdigit():
                                species_name = tokens[1].rstrip('*')
                                cluster_species.append(species_name)
                            i += 1
                    elif line.startswith('site_types'):
                        tokens = line.split()
                        site_types = tokens[1:]
                        i += 1  # Move to the next line after 'site_types'
                        continue  # Continue to process other lines in the cluster
                    else:
                        i += 1
                # After processing the cluster
                if len(cluster_species) != len(site_types):
                    raise EnergeticsModelError(f"Mismatch between number of species and site_types in a cluster in "
                                               f"line {i + 1}."
                                               f"\nCluster species: {cluster_species}"
                                               f"\nSite types: {site_types}")
                # Associate species with site types
                for species, site_type in zip(cluster_species, site_types):
                    if species not in species_in_simulation:
                        raise EnergeticsModelError(
                            f"Species '{species}' declared in energetics_input.dat but not in surf_specs_names.")
                    if species in species_site_types:
                        if species_site_types[species] != site_type:
                            raise EnergeticsModelError(
                                f"Species '{species}' is adsorbed on multiple site types: "
                                f"'{species_site_types[species]}' and '{site_type}'")
                    else:
                        species_site_types[species] = site_type
                i += 1  # Move past 'end_cluster'
            else:
                i += 1

        for species in surf_specs_names:
            if species not in species_site_types:
                raise EnergeticsModelError(f"Species '{species}' declared in surf_specs_names but not found in "
                                           f"energetics_input.dat.")
            surf_specs_data[species] = {
                'surf_specs_dent': species_dentates[species],
                'site_type': species_site_types[species]
            }
    return surf_specs_data


def check_default_lattice(path):
    """
    Check whether the simulation uses a default lattice configuration.

    Parameters
    ----------
    path : str
        The path to the directory containing the `lattice_input.dat` file.

    Returns
    -------
    bool
        True if the `lattice_input.dat` file indicates a default lattice configuration, False otherwise.
    """

    with open(os.path.join(path, 'lattice_input.dat'), 'r') as file:
        for line in file:
            # Check if both 'lattice' and 'default_choice' are in the same line
            if 'lattice' in line and 'default_choice' in line:
                return True

    return False
