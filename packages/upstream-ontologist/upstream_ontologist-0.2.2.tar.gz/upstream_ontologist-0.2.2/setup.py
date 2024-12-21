#!/usr/bin/python3
import sys

from setuptools import setup
from setuptools_rust import Binding, RustExtension

extra_features = []

if sys.platform != "win32":
    extra_features.append("debcargo")

setup(
    rust_extensions=[
        RustExtension(
            "upstream_ontologist._upstream_ontologist",
            "Cargo.toml",
            binding=Binding.PyO3,
            features=["extension-module"] + extra_features,
        ),
    ],
)
