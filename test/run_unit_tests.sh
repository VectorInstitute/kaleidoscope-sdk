#!/bin/bash

export PYTHONPATH=$PYTHONPATH:"../"

pytest -q unit_tests/test_batch_prompting.py