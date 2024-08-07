from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kscope",
    version="0.11.0",
    description="A user toolkit for analyzing and interfacing with Large Language Models (LLMs)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="python nlp machine-learning deep-learning distributed-computing neural-networks tensor llm",
    requires_python=">=3.8",
    url="https://github.com/VectorInstitute/kaleidoscope-sdk",
    author=["Vector AI Engineering"],
    author_email="ai_engineering@vectorinstitute.ai",
    license="MIT",
    packages=["kscope"],
    install_requires=[
        "certifi==2024.7.4",
        "charset-normalizer==3.3.2",
        "cloudpickle==3.0.0",
        "filelock==3.15.4",
        "fsspec==2024.6.1",
        "idna==3.7",
        "Jinja2==3.1.4",
        "MarkupSafe==2.1.5",
        "mpmath==1.3.0",
        "networkx==3.3",
        "numpy==2.0.0",
        "nvidia-cublas-cu12==12.1.3.1",
        "nvidia-cuda-cupti-cu12==12.1.105",
        "nvidia-cuda-nvrtc-cu12==12.1.105",
        "nvidia-cuda-runtime-cu12==12.1.105",
        "nvidia-cudnn-cu12==8.9.2.26",
        "nvidia-cufft-cu12==11.0.2.54",
        "nvidia-curand-cu12==10.3.2.106",
        "nvidia-cusolver-cu12==11.4.5.107",
        "nvidia-cusparse-cu12==12.1.0.106",
        "nvidia-nccl-cu12==2.20.5",
        "nvidia-nvjitlink-cu12==12.5.82",
        "nvidia-nvtx-cu12==12.1.105",
        "requests==2.32.3",
        "sympy==1.13.0",
        "torch==2.3.1",
        "triton==2.3.1",
        "typing_extensions==4.12.2",
        "urllib3==2.2.2"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
