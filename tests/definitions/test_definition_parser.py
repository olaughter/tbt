import os
from tempfile import TemporaryDirectory

import pytest

from tbt.definitions.definition_parser import DefinitionsParser
from tests.fixtures import invalid_pipelines, simple_steps, valid_pipelines


@pytest.fixture
def fixture_dp():
    root_dir = os.path.join(os.path.dirname(__file__), "..", "fixture_project")
    dp = DefinitionsParser(root_dir=root_dir)
    return dp


def create_tbt_files(subfolder, count):
    for i in range(count):
        open(f"{subfolder}/tbt{i}.yaml", "w").close()


def test_definitions_parser_parse(fixture_dp):
    fixture_dp.parse()
    assert len(fixture_dp.definitions) == 2
    assert len(fixture_dp.pipelines) > len(fixture_dp.definitions)


def test_definitions_parser_find_definitions():
    with TemporaryDirectory(dir=os.path.dirname(__file__)) as tmpdir:
        subdir = f"{tmpdir}/subdir"
        os.mkdir(subdir)

        subsubdir = f"{subdir}/subsubdir"
        os.mkdir(subsubdir)

        create_tbt_files(tmpdir, 3)
        create_tbt_files(subdir, 8)
        create_tbt_files(subsubdir, 4)

        dp = DefinitionsParser(root_dir=tmpdir)
        definitions = dp.find_definitions()
        assert len(definitions) == 15
        for d in definitions:
            assert os.path.isfile(d.path)
            assert d.path.startswith(tmpdir)
            assert d.path.endswith(".yaml")
            assert "tbt" in d.path


def test_definitions_parser_load_pipelines(fixture_dp):
    def_files = fixture_dp.find_definitions()
    pipelines = fixture_dp.load_pipelines(def_files)

    assert len(pipelines) == 3

    for label, pipeline in pipelines.items():
        assert label.startswith("test_pipeline")
        assert pipeline is not None


def test_definitions_parser_sort_pipelines_valid(valid_pipelines):
    dp = DefinitionsParser(root_dir=None)
    result = dp.sort_pipelines(valid_pipelines)
    assert len(valid_pipelines) == len(result), "length changed"
    assert list(valid_pipelines.keys()) != list(result.keys()), "order failed to change"


def test_definitions_parser_sort_pipelines_invalid(invalid_pipelines):
    dp = DefinitionsParser(root_dir="")
    with pytest.raises(ValueError) as err:
        dp.sort_pipelines(invalid_pipelines)

    assert "circular dependencies" in err.value.__str__()
