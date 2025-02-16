from app.phase_a_tasks import *
from tests import *
import pytest

pytest.main(["-v", "--tb=line", "-s", "tests/test_phase_a.py"])