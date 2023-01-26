Configuration
=============

The lingua SDK provides a flexible configuration interface based on the HuggingFace generation API.

These are the current acceptable values in the format (client input name = model accepted name (default - type GPT2 default value)
max_tokens = max-tokens (default - int 128)
top_k = top-k (default - int 0)
top_p = top-p (default - float 0.9)
num_sequences = num_return_sequences (default - int 1)
rep_penalty = repetition_penalty (default - float 1.0)
temperature (default - float 1.0)
stop_token (default - string None) [haven’t tested thoroughly]
use_grad (default torch.is_grad_enabled()) [unsure about this one]
do_sample= True (immutable) [static in GPT2 model]



Generation Configuration
------------------------

.. list-table::
    :header-rows: 1

    * - Parameter [type]
      - Definition
    * - num_cpus [int | string]
      - Number of CPUs to use, options are a number or 'all' (default: 1)
    * - boosted [bool]
      - Use kernel boosting (default: True)
    * - caching [bool]
      - Use kernel caching (default: True)
    * - auto_desc_gen [bool]
      - Use automatic descriptor generation (default: False)
    * - batches [int]
      - (default: 1)
    * - sampling_strategies [int]
      - (default: 2)
    * - softness [float]
      - Softness of Chimera for multiobj optimizations (default: 0.001)
    * - feas_approach [string]
      - Approach to unknown feasibility constraints, options are 'fwa' (feasibility-weighted acquisition), 'fca' (feasibility-constrained acquisition) or 'fia' (feasibility-interpolated acquisition). (default: 'fwa')
    * - feas_param [int]
      - Sensitivity to feasibility constraints (default: 1)
    * - dist_param [float]
      - Factor modulating density-based penalty in sample selector (default: 0.5)
    * - random_seed [None | int]
      - Set random seed (default: None)
    * - save_database [bool]
      - (default: False)
    * - aquisition_optimizer [string]
      - Set aquisition optimization method, options are 'adam' or 'genetic' (default: 'adam')
    * - obj_transform [None | string]
      - Set objective transform, options are None, 'sqrt', 'cbrt' or 'square' (default: 'sqrt')
    * - num_random_samples [int]
      - Number of samples per dimension to sample when optimizing acquisition function (default: 200)
    * - reject_tol [int]
      - Tolerance in rejection sampling, relevant when known constraints or fca used (default: 1000)
    * - vebosity [int]
      - Set verbosity level, from 0 to 5. 0: FATAL, 1: ERROR, 2: WARNING, 3: STATS, 4: INFO, 5: DEBUG (default: 4)
