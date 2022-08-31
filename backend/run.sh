#!/bin/bash

python -m uvicorn main:app --reload --host=0.0.0.0 --port=5000 --log-level=debug --log-config=config.yaml --reload-include=*.yaml
