#!/usr/bin/env bash

set -e

echo "🔧 Installing Poetry..."
curl -sSL https://install.python-poetry.org | python3 -

echo "📦 Installing dependencies from pyproject.toml..."
poetry install

