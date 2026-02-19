"""Tests for packaging metadata in pyproject.toml.

Guards against regressions like an invalid build-backend declaration
(see GitHub issue #9).
"""

import importlib
import pathlib
import sys

import pytest

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        tomllib = None

PYPROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent / "pyproject.toml"


@pytest.fixture(scope="module")
def pyproject():
    if tomllib is None:
        pytest.skip("tomllib/tomli not available")
    with open(PYPROJECT_PATH, "rb") as f:
        return tomllib.load(f)


class TestBuildSystem:
    def test_build_backend_is_setuptools_build_meta(self, pyproject):
        backend = pyproject["build-system"]["build-backend"]
        assert backend == "setuptools.build_meta", (
            f"build-backend should be 'setuptools.build_meta', got '{backend}'"
        )

    def test_build_backend_is_importable(self, pyproject):
        backend = pyproject["build-system"]["build-backend"]
        module_path = backend.split(":")[0]
        try:
            importlib.import_module(module_path)
        except ModuleNotFoundError:
            pytest.fail(f"build-backend module '{module_path}' is not importable")

    def test_build_requires_includes_setuptools(self, pyproject):
        requires = pyproject["build-system"].get("requires", [])
        assert any("setuptools" in r for r in requires), (
            "build-system.requires should include setuptools"
        )
