Getting Started
===============

Integrate the Lingua SDK into your project quickly!

Requirements
------------

* Python version >= 3.7


Installation
------------

To install ``lingua-sdk`` from `PyPI <https://pypi.org/project/pylingua/>`_:

.. code-block:: console

    $ pip install pylingua

or directly from GitHub:

.. code-block:: console

    $ pip install git+install git+https://github.com/VectorInstitute/lingua-sdk.git

To install ``lingua-sdk`` from source:

.. code-block:: console

    $ git clone git@github.com:VectorInstitute/lingua-sdk.git
    $ cd lingua-sdk
    $ pip install .

Example Usage 
-------------

This is a minimalist example of the SDK in action.

.. code-block:: python

    import lingua

    # Establish a client connection to the Lingua service
    client = lingua.Client(gateway_host="llm.cluster.local", gateway_port=3001)

    # Show all avaiable models, including active/inactive status
    client.get_models()

    # Get a handle to a model. If this model is not actively running, it will get launched in the background.
    model = client.load_model("ModelName")

    generation_config = {
        "max_tokens": 5,
        "top_k": 4,
        "top_p": 3,
        "rep_penalty": 1,
        "temperature": 0.5
    }

    # Sample text generation w/ input parameters
    text_gen = model.generate_text("What is the answer to life, the universe, and everything?", **generation_config)

    dir(text_gen) # display methods associated with generated text object
    text_gen.text # display only text
    text_gen.logprobs # display logprobs
    text_gen.tokens # display tokens

