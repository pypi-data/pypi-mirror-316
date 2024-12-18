#!/usr/bin/env python3

import yaml

from provisioner_shared.components.vcs.domain.config import VersionControlConfig
from provisioner_shared.components.vcs.typer_vcs_opts import (
    CliVersionControlOpts,
    TyperVersionControl,
)

TEST_DATA_GITHUB_ORGANIZATION = "test-organization"
TEST_DATA_GITHUB_REPOSITORY = "test-repository"
TEST_DATA_GITHUB_BRANCH = "test-branch"
TEST_DATA_GITHUB_ACCESS_TOKEN = "test-access-token"

TEST_DATA_YAML_TEXT = f"""
vcs:
  github:
    organization: {TEST_DATA_GITHUB_ORGANIZATION}
    repository: {TEST_DATA_GITHUB_REPOSITORY}
    branch: {TEST_DATA_GITHUB_BRANCH}
    git_access_token: {TEST_DATA_GITHUB_ACCESS_TOKEN}
"""


class TestDataVersionControlOpts:
    @staticmethod
    def create_fake_vcs_cfg() -> VersionControlConfig:
        cfg_dict = yaml.safe_load(TEST_DATA_YAML_TEXT)
        return VersionControlConfig(cfg_dict)

    @staticmethod
    def create_fake_typer_vcs() -> TyperVersionControl:
        return TyperVersionControl(TestDataVersionControlOpts.create_fake_vcs_cfg())

    @staticmethod
    def create_fake_cli_vcs_opts() -> CliVersionControlOpts:
        return CliVersionControlOpts(
            github_organization=TEST_DATA_GITHUB_ORGANIZATION,
            repository_name=TEST_DATA_GITHUB_REPOSITORY,
            branch_name=TEST_DATA_GITHUB_BRANCH,
            git_access_token=TEST_DATA_GITHUB_ACCESS_TOKEN,
        )
