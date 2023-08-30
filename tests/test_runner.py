import logging
import os
import pickle

from tbt.loader import Loader
from tbt.runner import Runner
from tests.fixtures import SpyStep, simple_steps, spy_pipelines

load_available_method = Loader.load_available


def test_runner_prep(spy_pipelines, caplog):
    Loader.load_available = lambda *_: {"transform": None, "spy_step": SpyStep}

    with caplog.at_level(logging.INFO):
        Runner(pipelines=spy_pipelines).prep()
    assert "ran __init__" in caplog.text
    assert "ran pre_step" in caplog.text

    Loader.load_available = load_available_method


def test_runner_run(spy_pipelines, caplog):
    Loader.load_available = lambda *_: {"transform": None, "spy_step": SpyStep}

    with caplog.at_level(logging.INFO):
        Runner(pipelines=spy_pipelines).run()
    assert "ran __init__" in caplog.text
    assert "ran pre_step" in caplog.text
    assert "ran run" in caplog.text
    assert "ran post_step" in caplog.text

    Loader.load_available = load_available_method


def test_runner_instantiate_steps(spy_pipelines, caplog):
    Loader.load_available = lambda *_: {"transform": None, "spy_step": SpyStep}

    for _, p in spy_pipelines.items():
        start = len(p.instantiated_steps)
    with caplog.at_level(logging.INFO):
        Runner(pipelines=spy_pipelines).instantiate_steps()
    assert "ran __init__" in caplog.text
    for _, p in spy_pipelines.items():
        end = len(p.instantiated_steps)
    assert end > start

    Loader.load_available = load_available_method


def test_runner_run_pre_steps(spy_pipelines, caplog):
    Loader.load_available = lambda *_: {"transform": None, "spy_step": SpyStep}

    runner = Runner(pipelines=spy_pipelines)
    runner.instantiate_steps()

    with caplog.at_level(logging.INFO):
        runner.run_pre_steps()
    assert "ran pre_step" in caplog.text

    assert "ran __init__" not in caplog.text
    assert "ran run" not in caplog.text
    assert "ran post_step" not in caplog.text

    Loader.load_available = load_available_method


def test_runner_run_steps(spy_pipelines, caplog):
    Loader.load_available = lambda *_: {"transform": None, "spy_step": SpyStep}

    runner = Runner(pipelines=spy_pipelines)
    runner.instantiate_steps()

    with caplog.at_level(logging.INFO):
        runner.run_steps()
    assert "ran run" in caplog.text

    assert "ran pre_step" not in caplog.text
    assert "ran __init__" not in caplog.text
    assert "ran post_step" not in caplog.text

    Loader.load_available = load_available_method


def test_runner_run_post_steps(spy_pipelines, caplog):
    Loader.load_available = lambda *_: {"transform": None, "spy_step": SpyStep}

    runner = Runner(pipelines=spy_pipelines)
    runner.instantiate_steps()

    with caplog.at_level(logging.INFO):
        runner.run_post_steps()
    assert "ran post_step" in caplog.text

    assert "ran __init__" not in caplog.text
    assert "ran pre_step" not in caplog.text
    assert "ran run" not in caplog.text

    Loader.load_available = load_available_method
