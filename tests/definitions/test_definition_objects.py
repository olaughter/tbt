from tbt.definitions.definition_objects import Definition, Pipeline, Step


def test_definition():
    d = Definition(root=".", file_name="tbt.yml")
    assert d.path == "./tbt.yml"


def test_pipeline():
    p = Pipeline(
        label="test",
        definition=Definition(root=".", file_name="tbt.yml"),
        steps=[{"source": {"type": "from_file", "path": "documents/input/frank.txt"}}],
    )
    assert p.label == "test"
    assert p.depends_on is None
    assert p.step_defs[0].meta_type == "source"
    assert p.step_defs[0].name == "from_file"
    assert p.step_defs[0].kwargs["path"] == "documents/input/frank.txt"


def test_step():
    s = Step(
        step_def={"source": {"type": "from_file", "path": "documents/input/frank.txt"}},
        root_dir=".",
    )
    assert s.meta_type == "source"
    assert s.name == "from_file"
    assert s.kwargs["path"] == "documents/input/frank.txt"
    assert s.kwargs["root_dir"] == "."
