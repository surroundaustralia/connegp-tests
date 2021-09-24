import os
from pathlib import Path
import pytest
import yaml

@pytest.hookimpl()
def pytest_sessionstart(session):
    # This pre-session hook is used to generate YAML files to support dynamic
    # parametrized marks based on TEST_SUPPORTED_MEDIATYPES and TEST_SUPPORTED_PROFILES
    # https://tavern.readthedocs.io/en/latest/basics.html#directly-including-test-data

    for required_variable in [
        'TEST_HOST', 'TEST_SUPPORTED_MEDIATYPES', 'TEST_SUPPORTED_PROFILES'
    ]:
        if required_variable not in os.environ:
            pytest.exit(f"'{required_variable}' was not passed as an envionment variable!")

    (Path() / "tests" / "supported_mediatypes.yaml").write_text(yaml.dump(
      os.environ['TEST_SUPPORTED_MEDIATYPES'].split(',')
    ))

    (Path() / "tests" / "supported_profiles.yaml").write_text(yaml.dump(
      os.environ['TEST_SUPPORTED_PROFILES'].split(',')
      # If prefix needs to be included:
      #[
      #   {'prefix': el[0], 'uri': el[1] }
      #   for el in map(
      #     lambda x: (x.split(':', 1)),
      #     os.environ['TEST_SUPPORTED_PROFILES'].split(',')
      #   )
      #]
    ))

def pytest_sessionfinish(session, exitstatus):
    for filename in [
        "supported_mediatypes.yaml",
        "supported_profiles.yaml"
    ]:
        (Path() / "tests" / filename).unlink()

