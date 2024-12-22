from __future__ import annotations

import pytest
import polars as pl
import pandas as pd

import numpy as np
import polars_ds as pds
import polars_ds.expr_linear as pds_linear
import polars_ds.num as pds_num
import polars_ds.string as pds_str
import polars_ds.stats as pds_stats
import polars_ds.ts_features as pds_ts
import polars_ds.expr_knn as pds_knn
import polars_ds.metrics as pds_metrics
from polars.testing import assert_frame_equal, assert_series_equal

from polars_ds.compat import compat as pds2

# --- All functions can be Wrapped ---
# Test compatibility works (able to wrap the function for all the expression functions pds provides)

def test_lin_reg_works():

    # If this doesn't fail, the returned function is correct.
    # The rest of the usage depends on the user.
    for expr in pds_linear.__all__:
        _ = getattr(pds2, expr) 
    else:
        assert True

def test_metrics_works():

    for expr in pds_metrics.__all__:
        _ = getattr(pds2, expr) 
    else:
        assert True

def test_num_works():

    for expr in pds_num.__all__:
        _ = getattr(pds2, expr) 
    else:
        assert True

def test_str_works():

    for expr in pds_str.__all__:
        _ = getattr(pds2, expr) 
    else:
        assert True

def test_stats_works():

    for expr in pds_stats.__all__:
        _ = getattr(pds2, expr) 
    else:
        assert True

def test_ts_works():

    for expr in pds_ts.__all__:
        _ = getattr(pds2, expr) 
    else:
        assert True

def test_expr_knn_works():

    for expr in pds_knn.__all__:
        _ = getattr(pds2, expr) 
    else:
        assert True


