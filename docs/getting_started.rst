Getting Started
===============

Integrate the Kaleidoscope SDK (kscope) into your project quickly!

Requirements
------------

* Python version >= 3.8


Installation
------------

To install the Kaleidoscope SDK from `PyPI <https://pypi.org/project/kscope/>`_:

    .. code-block:: console

        $ pip install kscope

To install the Kaleidoscope SDK from source:

    .. code-block:: console

        $ git clone git@github.com:VectorInstitute/kaleidoscope-sdk.git
        $ cd kaleidoscope-sdk
        $ pip install .


Example Usage
-------------

This is a minimalist example of the SDK in action.

.. code-block:: python

    import kscope
    import time

    # Establish a client connection to the Kaleidoscope service
    client = kscope.Client(gateway_host="llm.cluster.local", gateway_port=3001)

    # Show all supported models
    client.models

    # Show all model instances that are currently active
    client.model_instances

    # Get a handle to a model. In this example, let's use the Llama2 7b model.
    llama2_model = client.load_model("llama2-7b")

    # If this model is not actively running, it will get launched in the background.
    # In this case, wait until it moves into an "ACTIVE" state before proceeding.
    while llama2_model.state != "ACTIVE":
        time.sleep(1)

    # Now we wnat to generate some text. Start by defining a few generation attributes.
    generation_config = {
        "max_tokens": 32,
        "top_k": 4,
        "top_p": 0.3,
        "repetition_penalty": 1,
        "temperature": 0.5
    }

    # Sample text generation w/ input parameters
    text_gen = model.generate("What is Vector Institute?", **generation_config)

    text_gen.generation['sequences'] # display only text
    text_gen.generation['logprobs'] # display logprobs
    text_gen.generation['tokens'] # display tokens

    # Now let's retrieve some activations for a given module layer
    requested_activations = ['layers.0']
    activations = llama2_model.get_activations("What is Vector Institute?", requested_activations)

    # Next, let's manipulate the activations in the model. First, we need to import a few more modules.
    import cloudpickle
    import codecs
    import torch
    from torch import Tensor
    from typing import Callable, Dict

    # Define a function to manipulate the activations
    def replace_with_ones(act: Tensor) -> Tensor:
        """Replace an activation with an activation filled with ones."""
        out = torch.ones_like(act, dtype=act.dtype).cuda()
        return out

    # Now send the edit request
    editing_fns: Dict[str, Callable] = {}
    editing_fns['layers.0'] = replace_with_ones
    edited_activations = llama2_model.edit_activations("What is Vector Institute?", editing_fns)
    print(edited_activations)


Authentication
--------------

Users must authenticate using their Vector Institute cluster credentials. This can be done interactively instantiating a client object:

.. code-block:: console

    >>> import kscope
    >>> client = kscope.Client(gateway_host="llm.cluster.local", gateway_port=3001)
    You must authenticate with your LDAP credentials to use the Kaleidoscope service
    Username: <username>
    Password: <password>

This will generate an authentication token that will be used for all subsequent requests. The token will expire after 30 days, at which point the user will be prompted to re-authenticate.
The token is cached in the user's home directory, and will be reused if it is still valid.
