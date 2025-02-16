from app.phase_b_tasks import *
from tests import *
import pytest

pytest.main(["-v", "--tb=line", "-s", "tests/test_phase_b.py"])