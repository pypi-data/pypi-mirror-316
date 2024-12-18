"""
Testing for Extended Isolation Forest algorithm (treeple.ensemble._eiforest).
"""

# License: BSD 3 clause

import warnings
from unittest.mock import Mock, patch

import numpy as np
import pytest
from sklearn.datasets import load_diabetes, load_iris
from sklearn.ensemble._iforest import _average_path_length
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import ParameterGrid, train_test_split
from sklearn.utils import check_random_state
from sklearn.utils._testing import (
    assert_allclose,
    assert_array_almost_equal,
    assert_array_equal,
    ignore_warnings,
)

from treeple import ExtendedIsolationForest

# load iris & diabetes dataset
iris = load_iris()
diabetes = load_diabetes()


@pytest.fixture()
def global_random_seed():
    """Fixture to ask for a random yet controllable random seed.

    All tests that use this fixture accept the contract that they should
    deterministically pass for any seed value from 0 to 99 included.

    See the documentation for the SKLEARN_TESTS_GLOBAL_RANDOM_SEED
    variable for insrtuctions on how to use this fixture.

    https://scikit-learn.org/dev/computing/parallelism.html#sklearn-tests-global-random-seed
    """
    return 42


def test_eiforest(global_random_seed):
    """Check Isolation Forest for various parameter settings."""
    X_train = np.array([[0, 1], [1, 2]])
    X_test = np.array([[2, 1], [1, 1]])

    grid = ParameterGrid(
        {"n_estimators": [3], "max_samples": [0.5, 1.0, 3], "bootstrap": [True, False]}
    )

    with ignore_warnings():
        for params in grid:
            ExtendedIsolationForest(random_state=global_random_seed, **params).fit(X_train).predict(
                X_test
            )


def test_eiforest_error():
    """Test that it gives proper exception on deficient input."""
    X = iris.data

    # The dataset has less than 256 samples, explicitly setting
    # max_samples > n_samples should result in a warning. If not set
    # explicitly there should be no warning
    warn_msg = "max_samples will be set to n_samples for estimation"
    with pytest.warns(UserWarning, match=warn_msg):
        ExtendedIsolationForest(max_samples=1000).fit(X)
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        ExtendedIsolationForest(max_samples="auto").fit(X)
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        ExtendedIsolationForest(max_samples=np.int64(2)).fit(X)

    # test X_test n_features match X_train one:
    with pytest.raises(ValueError):
        ExtendedIsolationForest().fit(X).predict(X[:, 1:])


def test_recalculate_max_depth():
    """Check max_depth recalculation when max_samples is reset to n_samples"""
    X = iris.data
    clf = ExtendedIsolationForest().fit(X)
    for est in clf.estimators_:
        assert est.max_depth == int(np.ceil(np.log2(X.shape[0])))


def test_max_samples_attribute():
    X = iris.data
    clf = ExtendedIsolationForest().fit(X)
    assert clf.max_samples_ == X.shape[0]

    clf = ExtendedIsolationForest(max_samples=500)
    warn_msg = "max_samples will be set to n_samples for estimation"
    with pytest.warns(UserWarning, match=warn_msg):
        clf.fit(X)
    assert clf.max_samples_ == X.shape[0]

    clf = ExtendedIsolationForest(max_samples=0.4).fit(X)
    assert clf.max_samples_ == 0.4 * X.shape[0]


def test_eiforest_parallel_regression(global_random_seed):
    """Check parallel regression."""
    rng = check_random_state(global_random_seed)

    X_train, X_test = train_test_split(diabetes.data, random_state=rng)

    ensemble = ExtendedIsolationForest(n_jobs=3, random_state=global_random_seed).fit(X_train)

    ensemble.set_params(n_jobs=1)
    y1 = ensemble.predict(X_test)
    ensemble.set_params(n_jobs=2)
    y2 = ensemble.predict(X_test)
    assert_array_almost_equal(y1, y2)

    ensemble = ExtendedIsolationForest(n_jobs=1, random_state=global_random_seed).fit(X_train)

    y3 = ensemble.predict(X_test)
    assert_array_almost_equal(y1, y3)


def test_eiforest_performance(global_random_seed):
    """Test Isolation Forest performs well"""

    # Generate train/test data
    rng = check_random_state(global_random_seed)
    X = 0.3 * rng.randn(600, 2)
    X = rng.permutation(np.vstack((X + 2, X - 2)))
    X_train = X[:1000]

    # Generate some abnormal novel observations
    X_outliers = rng.uniform(low=-1, high=1, size=(200, 2))
    X_test = np.vstack((X[1000:], X_outliers))
    y_test = np.array([0] * 200 + [1] * 200)

    # fit the model
    clf = ExtendedIsolationForest(max_samples=100, random_state=rng).fit(X_train)

    # predict scores (the lower, the more normal)
    y_pred = -clf.decision_function(X_test)

    # check that there is at most 6 errors (false positive or false negative)
    assert roc_auc_score(y_test, y_pred) > 0.98


@pytest.mark.parametrize("contamination", [0.25, "auto"])
def test_eiforest_works(contamination, global_random_seed):
    # toy sample (the last two samples are outliers)
    X = [[-2, -1], [-1, -1], [-1, -2], [1, 1], [1, 2], [2, 1], [7, 4], [-5, 9]]

    # Test ExtendedIsolationForest
    clf = ExtendedIsolationForest(random_state=global_random_seed, contamination=contamination)
    clf.fit(X)
    decision_func = -clf.decision_function(X)
    pred = clf.predict(X)
    # assert detect outliers:
    assert np.min(decision_func[-2:]) > np.max(decision_func[:-2])
    assert_array_equal(pred, 6 * [1] + 2 * [-1])


def test_max_samples_consistency():
    # Make sure validated max_samples in iforest and BaseBagging are identical
    X = iris.data
    clf = ExtendedIsolationForest().fit(X)
    assert clf.max_samples_ == clf._max_samples


def test_eiforest_subsampled_features():
    # It tests non-regression for #5732 which failed at predict.
    rng = check_random_state(0)
    X_train, X_test, y_train, y_test = train_test_split(
        diabetes.data[:50], diabetes.target[:50], random_state=rng
    )
    clf = ExtendedIsolationForest(max_features=0.8)
    clf.fit(X_train, y_train)
    clf.predict(X_test)


def test_eiforest_average_path_length():
    # It tests non-regression for #8549 which used the wrong formula
    # for average path length, strictly for the integer case
    # Updated to check average path length when input is <= 2 (issue #11839)
    result_one = 2.0 * (np.log(4.0) + np.euler_gamma) - 2.0 * 4.0 / 5.0
    result_two = 2.0 * (np.log(998.0) + np.euler_gamma) - 2.0 * 998.0 / 999.0
    assert_allclose(_average_path_length([0]), [0.0])
    assert_allclose(_average_path_length([1]), [0.0])
    assert_allclose(_average_path_length([2]), [1.0])
    assert_allclose(_average_path_length([5]), [result_one])
    assert_allclose(_average_path_length([999]), [result_two])
    assert_allclose(
        _average_path_length(np.array([1, 2, 5, 999])),
        [0.0, 1.0, result_one, result_two],
    )
    # _average_path_length is increasing
    avg_path_length = _average_path_length(np.arange(5))
    assert_array_equal(avg_path_length, np.sort(avg_path_length))


def test_score_samples():
    X_train = [[1, 1], [1, 2], [2, 1]]
    clf1 = ExtendedIsolationForest(contamination=0.1).fit(X_train)
    clf2 = ExtendedIsolationForest().fit(X_train)
    assert_array_equal(
        clf1.score_samples([[2.0, 2.0]]),
        clf1.decision_function([[2.0, 2.0]]) + clf1.offset_,
    )
    assert_array_equal(
        clf2.score_samples([[2.0, 2.0]]),
        clf2.decision_function([[2.0, 2.0]]) + clf2.offset_,
    )
    assert_array_equal(clf1.score_samples([[2.0, 2.0]]), clf2.score_samples([[2.0, 2.0]]))


def test_eiforest_warm_start():
    """Test iterative addition of iTrees to an iForest"""

    rng = check_random_state(0)
    X = rng.randn(20, 2)

    # fit first 10 trees
    clf = ExtendedIsolationForest(
        n_estimators=10, max_samples=20, random_state=rng, warm_start=True
    )
    clf.fit(X)
    # remember the 1st tree
    tree_1 = clf.estimators_[0]
    # fit another 10 trees
    clf.set_params(n_estimators=20)
    clf.fit(X)
    # expecting 20 fitted trees and no overwritten trees
    assert len(clf.estimators_) == 20
    assert clf.estimators_[0] is tree_1


# mock get_chunk_n_rows to actually test more than one chunk (here one
# chunk has 3 rows):
@patch(
    "sklearn.ensemble._iforest.get_chunk_n_rows",
    side_effect=Mock(**{"return_value": 3}),
)
@pytest.mark.parametrize("contamination, n_predict_calls", [(0.25, 3), ("auto", 2)])
def test_eiforest_chunks_works1(
    mocked_get_chunk, contamination, n_predict_calls, global_random_seed
):
    test_eiforest_works(contamination, global_random_seed)
    assert mocked_get_chunk.call_count == n_predict_calls


# idem with chunk_size = 10 rows
@patch(
    "sklearn.ensemble._iforest.get_chunk_n_rows",
    side_effect=Mock(**{"return_value": 10}),
)
@pytest.mark.parametrize("contamination, n_predict_calls", [(0.25, 3), ("auto", 2)])
def test_eiforest_chunks_works2(
    mocked_get_chunk, contamination, n_predict_calls, global_random_seed
):
    test_eiforest_works(contamination, global_random_seed)
    assert mocked_get_chunk.call_count == n_predict_calls


def test_eiforest_with_uniform_data():
    """Test whether iforest predicts inliers when using uniform data"""

    # 2-d array of all 1s
    X = np.ones((100, 10))
    iforest = ExtendedIsolationForest()
    iforest.fit(X)

    rng = np.random.RandomState(0)

    assert all(iforest.predict(X) == 1)
    assert all(iforest.predict(rng.randn(100, 10)) == 1)
    assert all(iforest.predict(X + 1) == 1)
    assert all(iforest.predict(X - 1) == 1)

    # 2-d array where columns contain the same value across rows
    X = np.repeat(rng.randn(1, 10), 100, 0)
    iforest = ExtendedIsolationForest()
    iforest.fit(X)

    assert all(iforest.predict(X) == 1)
    assert all(iforest.predict(rng.randn(100, 10)) == 1)
    assert all(iforest.predict(np.ones((100, 10))) == 1)

    # Single row
    X = rng.randn(1, 10)
    iforest = ExtendedIsolationForest()
    iforest.fit(X)

    assert all(iforest.predict(X) == 1)
    assert all(iforest.predict(rng.randn(100, 10)) == 1)
    assert all(iforest.predict(np.ones((100, 10))) == 1)


def test_eiforest_preserve_feature_names():
    """Check that feature names are preserved when contamination is not "auto".

    Feature names are required for consistency checks during scoring.

    Non-regression test for Issue #25844
    """
    pd = pytest.importorskip("pandas")
    rng = np.random.RandomState(0)

    X = pd.DataFrame(data=rng.randn(4), columns=["a"])
    model = ExtendedIsolationForest(random_state=0, contamination=0.05)

    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        model.fit(X)
