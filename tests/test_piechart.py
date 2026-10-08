import os
import runpy
import sys
import tempfile
import types
import unittest
from unittest import mock

import pandas  # noqa: F401  keep pandas/numpy loaded across patched runs

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'piechart.py')


def _fake_pyplot():
    plt = types.ModuleType('matplotlib.pyplot')
    plt.calls = {}

    def record(name):
        def fn(*args, **kwargs):
            plt.calls[name] = (args, kwargs)
        return fn

    for name in ('figure', 'pie', 'title', 'show'):
        setattr(plt, name, record(name))
    mpl = types.ModuleType('matplotlib')
    mpl.pyplot = plt
    return mpl, plt


class PieChartScriptTest(unittest.TestCase):
    def run_script_from(self, cwd):
        mpl, plt = _fake_pyplot()
        old_cwd = os.getcwd()
        os.chdir(cwd)
        try:
            with mock.patch.dict(sys.modules, {'matplotlib': mpl, 'matplotlib.pyplot': plt}):
                runpy.run_path(SCRIPT, run_name='__main__')
        finally:
            os.chdir(old_cwd)
        return plt

    def assert_chart_from_csv(self, plt):
        self.assertIn('pie', plt.calls)
        args, kwargs = plt.calls['pie']
        self.assertEqual(list(args[0]), [30, 20, 50])
        self.assertEqual(list(kwargs['labels']), ['Apples', 'Bananas', 'Cherries'])
        self.assertIn('show', plt.calls)

    def test_loads_csv_and_plots_from_repo_root(self):
        self.assert_chart_from_csv(self.run_script_from(os.path.dirname(SCRIPT)))

    def test_loads_csv_from_another_working_directory(self):
        with tempfile.TemporaryDirectory() as other:
            self.assert_chart_from_csv(self.run_script_from(other))


if __name__ == '__main__':
    unittest.main()
