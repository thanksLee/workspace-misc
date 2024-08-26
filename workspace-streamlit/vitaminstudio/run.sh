#!/bin/bash
set -e

export PYTHONDONTWRITEBYTECODE=1

# cp -R ./products/common ./products/wordic/src
# cp -R ./products/core ./products/wordic/src

cp ./.streamlit/config.local.toml ./.streamlit/config.toml

streamlit run ./apps/app_vitaminstudio.py
