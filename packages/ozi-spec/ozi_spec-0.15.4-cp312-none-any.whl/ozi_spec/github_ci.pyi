# ozi/spec/ci.py
# Part of the OZI Project.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Unlicense
"""Continuous integration specification."""
from __future__ import annotations

from collections.abc import Mapping  # noqa: TCH003,TC003,RUF100
from dataclasses import dataclass
from dataclasses import field

from ozi_spec.base import Default

@dataclass(slots=True, frozen=True, eq=True)
class Publish(Default):
    """Publishing patterns for packaged project."""

    include: tuple[str, ...] = ('*.tar.gz', '*.whl', 'sig/*')
    version: str = '1.7.2'


@dataclass(slots=True, frozen=True, eq=True)
class Draft(Default):
    """Draft release patterns for packaged project."""

    version: str = '1.7.0'


@dataclass(slots=True, frozen=True, eq=True)
class Release(Default):
    """Release patterns for packaged project."""

    version: str = '1.1.2'


@dataclass(slots=True, frozen=True, eq=True)
class GenerateProvenance(Default):
    """SLSA provenance generator metadata.
    
    .. versionadded:: 0.11.7
    """

    version: str = 'v2.0.0'


@dataclass(slots=True, frozen=True, eq=True)
class Checkpoint(Default):
    """Checkpoint suites to run."""

    suites: tuple[str, ...] = ('dist', 'lint', 'test')
    version: str = '1.4.0'


@dataclass(slots=True, frozen=True, eq=True)
class HardenRunner(Default):
    """Github Step-Security harden runner."""
    version: str = '0080882f6c36860b6ba35c610c98ce87d4e2f26f'


@dataclass(slots=True, frozen=True, eq=True)
class GithubActionPyPI(Default):
    """pypa/gh-action-pypi-publish"""
    version: str = '67339c736fd9354cd4f8cb0b744f2b82a74b5c70'
