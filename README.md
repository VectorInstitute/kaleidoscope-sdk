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

``lingua`` provides a few high-level APIs namely:

* `generate_text` - Returns an LLM text generation based on prompt input 
* `module_names` - Returns all modules in the LLM neural network
* `instances` - Returns all active LLMs instantiated by the model service

``lingua`` is composed of the following components:

* Python SDK - A command line tool wrapping the gateway service API endpoints
* Web service - A front-end web application tool sending requests to the gateway service
* Model service - A backend utility that loads models into GPU memory and exposes an interface to recieve requests


## Getting Started

### Install

~~Install via PyPI:~~ Coming soon!

```bash
    python3 -m pip install lingua
```
or install from source:

```bash
    pip install git+https://github.com/VectorInstitute/lingua-sdk.git
```

### Quick Start

### Retrieve personal auth key from http://llm.cluster.local:3001
A sample text generation submission from the web may be required to sign-in and generate an updated authentication key.
![Auth_demo_pic](https://user-images.githubusercontent.com/72175053/210878149-c142e36c-d61b-4b44-984f-3c0f8dec13de.png)

### Sample
```python
import lingua

# Establish a client connection to the Lingua service
client = lingua.Client(gateway_host="llm.cluster.local", gateway_port=3001)

# Show all avaiable models, including active/inactive status
client.get_models()

# Get a handle to a model. If this model is not actively running, it will get launched in the background.
model = client.load_model("ModelName")

# Sample text generation w/ input parameters
text_gen = model.generate_text("What is the answer to life, the universe, and everything?", max_tokens=5, top_k=4, top_p=3, rep_penalty=1, temperature=0.5)
dir(text_gen) # display methods associated with generated text object
text_gen.text # display only text
text_gen.logprobs # display logprobs
text_gen.tokens # display tokens
```

## [Documentation](https://vectorinstitute.github.io/lingua/)
More information can be found on the Lingua documentation site.

## Contributing
Contributing to lingua is welcomed. See [Contributing](https://github.com/VectorInstitute/lingua/blob/main/doc/CONTRIBUTING.md) for
guidelines.

## License
[MIT](LICENSE)

## Citation
Reference to cite when you use Lingua in a project or a research paper:
```
Sivaloganathan, J., Coatsworth, M., Willes, J., Choi, M., & Shen, G. (2022). Lingua. http://VectorInstitute.github.io/lingua. computer software, Vector Institute for Artificial Intelligence. Retrieved from https://github.com/VectorInstitute/lingua-sdk.git. 
```
