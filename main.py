"""
'The dataset above consists of mass measurements (in lb) of a baby elephant. Using Excel or otherwise, estimate the mass of the elephant at 
21 months of age in kg (use the conversion, 1 lb = 0.454 kg). Express your answer to three significant figures.'
"""

import numpy as np
import matplotlib.pyplot as plt
from random import random
import os
import csv

def create_data(fname, seed=0):
    """
    Create a .csv file containing two columns: Age (months) and Mass (lb).
    Generate 12 datapoints over 30 months.
    """

    # Set random seed
    np.random.seed(seed)

    # Generate time data
    time = np.arange(0, 30, 2.5)

    # Generate mass data
    mass = np.zeros(len(time))
    mass[0] = 264 
    for i in range(1, len(time)):
        mass[i] = mass[i-1] + 100

    # Add noise to mass data
    mass_noise = np.zeros(len(time))
    for i in range(len(time)):

        mass_noise[i] = mass[i] + (random() - 0.5)*100

    # Format mass_noise data to 4 significant figures
    mass_noise = np.around(mass_noise, decimals=2)

    # Save data to file
    np.savetxt(fname, np.c_[time, mass_noise], delimiter=',', header='Age (months), Mass (lb)')

def read_data(fname):
    """
    Read data from .csv file.
    """

    # Read data from file
    data = np.genfromtxt(fname, delimiter=',', skip_header=1)

    # Split data into time and mass
    time = data[:, 0]
    mass = data[:, 1]

    return time, mass

def calculate_mass_at_time(fname, x=21):
    """
    Create a linear model between x and y data.
    Use the model to determine the y value at a given x value.
    """

    # Read data
    time_data, mass_data = read_data(fname)

    mass_data = mass_data*0.454

    # Create linear model
    model = np.polyfit(time_data, mass_data, 1)

    # Calculate mass at x
    mass_at_x = np.polyval(model, x)

    # Format mass_at_x to 3 significant figures
    mass_at_x = '{:.3g}'.format(mass_at_x)

    return mass_at_x

def save_list_of_dicts_to_csv(list_of_dicts, fname):
    """
    Save a list of dictionaries to a .csv file.
    """

    # Get keys from first dictionary
    keys = list_of_dicts[0].keys()

    # Save list of dictionaries to .csv file
    with open(fname, 'w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)



if __name__ == "__main__":

    # Use calculate_mass_at_time on all files in data directory.
    # Save results to a list of dictionaries.
    results = []
    for fname in os.listdir('data'):
        results.append({'Filename': fname, 'Mass (kg)': calculate_mass_at_time('data/' + fname)})

    # Save results to .csv file
    save_list_of_dicts_to_csv(results, 'results.csv')