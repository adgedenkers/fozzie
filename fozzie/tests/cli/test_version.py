import pytest
from click.testing import CliRunner
from fozzie.cli.version import version
from fozzie.version.version_manager import VersionManager
import tempfile
import os

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    # ✅ Manually initialize the database
    vm = VersionManager(db_path=path)
    vm.initialize_db(vm.conn)
    vm.close()

    yield path
    os.remove(path)

def test_version_show(temp_db):
    vm = VersionManager(db_path=temp_db)
    runner = CliRunner()
    result = runner.invoke(version, ["show", "--db-path", temp_db])
    assert "0.7" in result.output

def test_version_minor_increment(temp_db):
    vm = VersionManager(db_path=temp_db)
    runner = CliRunner()
    runner.invoke(version, ["minor", "--db-path", temp_db])
    version_after = vm.get_version()
    assert round(version_after, 1) == 0.8

def test_version_major_increment(temp_db):
    vm = VersionManager(db_path=temp_db)
    runner = CliRunner()
    runner.invoke(version, ["major", "--db-path", temp_db])
    version_after = vm.get_version()
    assert version_after == 1.0
