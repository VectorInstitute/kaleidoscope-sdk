lingua-sdk
==========

Welcome to the **lingua-sdk**!

``lingua-sdk`` is a Python module used to interact with large language models
hosted via the Lingua service (available at https://github.com/VectorInstitute/lingua).
It provides a simple interface launch LLMs on an HPC cluster, ask them to
perform basic features like text generation, but also retrieve intermediate
information from inside the model such as log probabilities and activations.
These features are exposed via a few high-level APIs, namely:

*  ``generate_text`` - Returns an LLM text generation based on prompt input
*  ``module_names`` - Returns all modules in the LLM neural network
*  ``instances`` - Returns all active LLMs instantiated by the model service

.. toctree::
   :maxdepth: 2
   :caption: Contents

   getting_started
   api
   configuration

Contributing
------------
Contributing to lingua is welcomed. See `Contributing <https://github.com/VectorInstitute/lingua-sdk/blob/main/doc/CONTRIBUTING.md>`_ for
guidelines.

License
-------

``lingua-sdk`` is disributed under the MIT license. See `LICENSE <https://github.com/VectorInstitute/lingua-sdk/blob/main/doc/LICENSE>`_

Citation
--------
Reference to cite when you use Lingua in a project or a research paper:

::

   Sivaloganathan, J., Coatsworth, M., Willes, J., Choi, M., & Shen, G. (2022). Lingua. http://VectorInstitute.github.io/lingua. computer software, Vector Institute for Artificial Intelligence. Retrieved from https://github.com/VectorInstitute/lingua-sdk.git. 