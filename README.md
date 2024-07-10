![Kaleidoscope](https://user-images.githubusercontent.com/72175053/229659396-2a61cd69-eafa-4a96-8e1c-d93519a8f617.png)
-----------------
# Kaleidoscope-SDK
![PyPI](https://img.shields.io/pypi/v/kscope)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kscope)
![GitHub](https://img.shields.io/github/license/VectorInstitute/kaleidoscope-sdk)
![DOI](https://img.shields.io/badge/DOI-in--progress-blue)
[![Documentation](https://img.shields.io/badge/api-reference-lightgrey.svg)](https://kaleidoscope-sdk.readthedocs.io/en/latest/)

A user toolkit for analyzing and interfacing with Large Language Models (LLMs)


## Overview

``kaleidoscope-sdk`` is a Python module used to interact with large language models
hosted via the Kaleidoscope service available at: https://github.com/VectorInstitute/kaleidoscope.
It provides a simple interface to launch LLMs on an HPC cluster and perform basic, fast inference.
These features are exposed via a few high-level APIs, namely:

* `model_instances` - Shows a list of all active LLMs instantiated by the model service
* `load_model` - Loads an LLM via the model service
* `generate` - Returns an LLM text generation based on prompt input, or list of inputs



## Getting Started

Requires Python version >= 3.8

### Install

```bash
python3 -m pip install kscope
```
or install from source:

```bash
pip install git+https://github.com/VectorInstitute/kaleidoscope-sdk.git
```

### Authentication

In order to submit generation jobs, a designated Vector Institute cluster account is required. Please contact the
[AI Engineering Team](mailto:ai_engineering@vectorinstitute.ai?subject=[Github]%20Kaleidoscope)
in charge of Kaleidoscope for more information.

### Sample Workflow

The following workflow shows how to load and interact with an OPT-175B model
on the Vector Institute Vaughan cluster.

```python
#!/usr/bin/env python3
import kscope
import time

# Establish a client connection to the Kaleidoscope service
# If you have not previously authenticated with the service, you will be prompted to now
client = kscope.Client(gateway_host="llm.cluster.local", gateway_port=3001)

# See which models are supported
client.models

# See which models are instantiated and available to use
client.model_instances

# Get a handle to a model. If this model is not actively running, it will get launched in the background.
# In this example we want to use the Llama3 8b model
llama3_model = client.load_model("llama3-8b")

# If the model was not actively running, this it could take several minutes to load. Wait for it come online.
while llama3_model.state != "ACTIVE":
    time.sleep(1)

# Sample text generation w/ input parameters
text_gen = llama3_model.generate("What is Vector Institute?", {'max_tokens': 5, 'top_k': 4, 'temperature': 0.5})
dir(text_gen) # display methods associated with generated text object
text_gen.generation['sequences'] # display only text
text_gen.generation['logprobs'] # display logprobs
text_gen.generation['tokens'] # display tokens

```

## Documentation
Full documentation and API reference are available at: http://kaleidoscope-sdk.readthedocs.io.


## Contributing
Contributing to kaleidoscope is welcomed. See [Contributing](CONTRIBUTING) for
guidelines.


## License
[MIT](LICENSE)


## Citation
Reference to cite when you use Kaleidoscope in a project or a research paper:
```
Willes, J., Choi, M., Coatsworth, M., Shen, G., & Sivaloganathan, J (2022). Kaleidoscope. http://VectorInstitute.github.io/kaleidoscope. computer software, Vector Institute for Artificial Intelligence. Retrieved from https://github.com/VectorInstitute/kaleidoscope-sdk.git.
```
