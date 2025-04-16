import pytest
from click.testing import CliRunner
from fozzie.cli.version import version
from fozzie.version.version_manager import VersionManager
import os
import tempfile
import sqlite3

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    vm = VersionManager(db_path=path)
    vm.initialize_db(vm.conn)
    yield path
    vm.close()
    os.remove(path)

def test_version_show(temp_db):
    runner = CliRunner()
    result = runner.invoke(version, ["show", "--db-path", temp_db])
    assert "0.7" in result.output

def test_version_minor_increment(temp_db):
    runner = CliRunner()
    runner.invoke(version, ["minor", "--db-path", temp_db])
    vm = VersionManager(db_path=temp_db)
    assert round(vm.get_version(), 1) == 0.8
    vm.close()

def test_version_major_increment(temp_db):
    runner = CliRunner()
    runner.invoke(version, ["major", "--db-path", temp_db])
    vm = VersionManager(db_path=temp_db)
    assert vm.get_version() == 1.0
    vm.close()
