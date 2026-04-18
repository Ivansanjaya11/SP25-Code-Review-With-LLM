#   -*- coding: utf-8 -*-
import subprocess
import sys

from pybuilder.core import init, task, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")

name = "code-review-with-llm"
default_task = "run"

@init
def set_properties(project):
    project.depends_on_requirements("requirements.txt")

    project.set_property("dir_source_main_python", "src")
    project.set_property("dir_source_unittest_python", "src/unittest")
    project.set_property("dir_source_main_scripts", "src")

@task
def run(project):
    subprocess.run([sys.executable, "-m", "src.main"])

@task
def ruff(project, logger):
    result = subprocess.run(["ruff", "check", "."], capture_output=True, text=True)

    if result.returncode != 0:
        logger.warn(result.stdout)
    else:
        logger.info("Ruff check passed!")
