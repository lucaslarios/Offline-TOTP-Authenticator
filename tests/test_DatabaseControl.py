import pytest

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.DatabaseControl import DatabaseControl




def test_database_singleton():
    first_instance = DatabaseControl()
    second_instance = DatabaseControl()
    first_instance.close_connection()
    assert first_instance is second_instance,"they should be the same instance"