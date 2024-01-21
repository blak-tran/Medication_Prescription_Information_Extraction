#!/bin/bash

set -m

exec uvicorn main:app --host 0.0.0.0 --port 8000

fg %1
