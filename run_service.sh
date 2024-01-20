#!/bin/bash

set -m

exec uvicorn /app/main:app --host 0.0.0.0 --port 80

fg %1
