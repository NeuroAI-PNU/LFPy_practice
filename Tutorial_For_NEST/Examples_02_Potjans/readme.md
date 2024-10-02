## Cortical microcircuit model of Potjans & Diesmann (2014)
* https://nest-simulator.readthedocs.io/en/latest/auto_examples/Potjans_2014/index.html

### File structure
* run_microcircuit.py: an example script to try out the microcircuit
* network.py: the main Network class with functions to build and simulate the network
* helpers.py: helper functions for network construction, simulation and evaluation
* network_params.py: network and neuron parameters
* stimulus_params.py: parameters for optional external stimulation
* sim_params.py: simulation parameters
* reference_data: reference data and figures obtained by executing run_microcircuit.py with default parameters

### Recommendations for benchmarking
* For benchmark simulations assessing network-construction and state-propagation times, the recommended changes to the default parameters are the following:
* sim_params.py: 
    * 't_sim': 10000.0: The biological simulation time should be at least 10 s for measuring the state propagation time.
    * 'rec_dev': []: No recording devices.
    * 'local_num_threads': t: Adjust the number of threads t per MPI process as needed for the benchmarks.(must more than 4)
    * 'print_time': False': No printing of time progress.

* network_params.py:
    * 'N_scaling': 1.: Full number of neurons.
    * 'K_scaling': 1.: Full indegrees.
    * 'poisson_input': False: DC background input

