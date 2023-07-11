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

    # Get a handle to a model. In this example, let's use the OPT-175B model.
    opt_model = client.load_model("opt-175b")

    # If this model is not actively running, it will get launched in the background.
    # In this case, wait until it moves into an "ACTIVE" state before proceeding.
    while opt_model.state != "ACTIVE":
        time.sleep(1)

    # Now we wnat to generate some text. Start by defining a few generation attributes.
    generation_config = {
        "max_tokens": 5,
        "top_k": 4,
        "top_p": 0.3,
        "repetition_penalty": 1,
        "temperature": 0.5
    }

    # Sample text generation w/ input parameters
    text_gen = model.generate("What is the answer to life, the universe, and everything?", **generation_config)

    text_gen.generation['sequences'] # display only text
    text_gen.generation['logprobs'] # display logprobs
    text_gen.generation['tokens'] # display tokens

    # Now let's retrieve some activations for a given module layer
    requested_activations = ['decoder.layers.0']
    activations = opt_model.get_activations("What are activations?", requested_activations)


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
