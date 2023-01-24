# Lingua-SDK
A user toolkit for analyzing and interfacing with Large Language Models (LLMs)

<!--
[![PyPI]()]()
[![code checks]()]()
[![integration tests]()]()
[![docs]()]()
[![codecov]()
[![license]()]()
-->

## Overview

## Getting Started

### Install

~~Install via PyPI:~~ Coming soon!

```bash
    python3 -m pip install pylingua
```
or install from source:

```bash
    pip install git+https://github.com/VectorInstitute/lingua-sdk.git
```

### Model Interface

> Note: This is a pre-release build and the public API is subject to change.

``lingua-sdk`` provides a Python SDK for interfacing with LLMs on the Vector cluster and exposes two high-level objects:


    * Client: Faciliates authentication and model loading.

    * Model: Facilitates model interaction.


### Sample
```python

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

```

## [Documentation](https://vectorinstitute.github.io/lingua-sdk/)
More information can be found on the Lingua documentation site.

## Contributing
Contributing to lingua is welcomed. See [Contributing](https://github.com/VectorInstitute/lingua-sdk/blob/main/doc/CONTRIBUTING.md) for
guidelines.

## License
[MIT](LICENSE)

## Citation
Reference to cite when you use Lingua in a project or a research paper:
```
Sivaloganathan, J., Coatsworth, M., Willes, J., Choi, M., & Shen, G. (2022). Lingua. http://VectorInstitute.github.io/lingua. computer software, Vector Institute for Artificial Intelligence. Retrieved from https://github.com/VectorInstitute/lingua-sdk.git. 
```
