import warnings
from pathlib import Path

import numpy as np
import pytest
from mne import read_epochs_eeglab
from mne.io import read_raw
from mne.io.eeglab.eeglab import _check_load_mat
from mne.preprocessing import read_ica_eeglab
from scipy.io import loadmat

from mne_icalabel.datasets import icalabel
from mne_icalabel.iclabel._utils import _mne_to_eeglab_locs
from mne_icalabel.iclabel.features import (
    _compute_ica_activations,
    _eeg_autocorr,
    _eeg_autocorr_fftw,
    _eeg_autocorr_welch,
    _eeg_rpsd_compute_psdmed,
    _eeg_rpsd_constants,
    _eeg_rpsd_format,
    _eeg_topoplot,
    _resample,
    _retrieve_eeglab_icawinv,
    _topoplotFast,
    get_iclabel_features,
)

dataset_path = icalabel.data_path() / "iclabel"

# Raw/Epochs files with ICA decomposition
raw_eeglab_path = dataset_path / "datasets/sample-raw.set"
raw_short_eeglab_path = dataset_path / "datasets/sample-short-raw.set"
raw_very_short_eeglab_path = dataset_path / "datasets/sample-very-short-raw.set"
epo_eeglab_path = dataset_path / "datasets/sample-epo.set"
epo_long_eeglab_path = dataset_path / "datasets/sample-long-epo.set"

# ICA activation matrix for raw/epochs
raw_icaact_eeglab_path = dataset_path / "icaact/icaact-raw.mat"
epo_icaact_eeglab_path = dataset_path / "icaact/icaact-epo.mat"

# Topography
raw_topo1_path = dataset_path / "topo/topo1-raw.mat"
epo_topo1_path = dataset_path / "topo/topo1-epo.mat"
raw_topo_feature_path = dataset_path / "topo/topo-feature-raw.mat"
epo_topo_feature_path = dataset_path / "topo/topo-feature-epo.mat"

# PSD
psd_constants_raw_path = dataset_path / "psd/constants-raw.mat"
psd_steps_raw_path = dataset_path / "psd/psd-step-by-step-raw.mat"
psd_raw_path = dataset_path / "psd/psd-raw.mat"
psd_constants_epo_path = dataset_path / "psd/constants-epo.mat"
psd_steps_epo_path = dataset_path / "psd/psd-step-by-step-epo.mat"
psd_epo_path = dataset_path / "psd/psd-epo.mat"
psd_constants_long_epo_path = dataset_path / "psd/constants-long-epo.mat"
psd_steps_long_epo_path = dataset_path / "psd/psd-step-by-step-long-epo.mat"
psd_long_epo_path = dataset_path / "psd/psd-long-epo.mat"

# Autocorrelations
autocorr_raw_path = dataset_path / "autocorr/autocorr-raw.mat"
autocorr_short_raw_path = dataset_path / "autocorr/autocorr-short-raw.mat"
autocorr_very_short_raw_path = dataset_path / "autocorr/autocorr-very-short-raw.mat"
autocorr_epo_path = dataset_path / "autocorr/autocorr-epo.mat"

# Complete features
features_raw_path = dataset_path / "features/features-raw.mat"
features_epo_path = dataset_path / "features/features-epo.mat"

# General readers
reader = {"raw": read_raw, "epo": read_epochs_eeglab}
kwargs = {"raw": dict(preload=True), "epo": dict()}


# ----------------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Estimated head radius.*:RuntimeWarning")
@pytest.mark.parametrize(
    ("file", "psd_constant_file", "eeglab_feature_file"),
    [
        (raw_eeglab_path, psd_constants_raw_path, features_raw_path),
        (epo_eeglab_path, psd_constants_epo_path, features_epo_path),
    ],
)
def test_get_features_from_precomputed_ica(
    file, psd_constant_file, eeglab_feature_file
):
    """Test that we get the correct set of features from an MNE instance.

    Corresponds to the output from 'ICL_feature_extractor.m'.
    """
    type_ = str(Path(file).stem)[-3:]
    inst = reader[type_](file, **kwargs[type_])
    ica = read_ica_eeglab(file)

    # Retrieve topo and autocorr
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        topo, _, autocorr = get_iclabel_features(inst, ica)

    # Build PSD feature manually to match the subset
    # retrieve activation
    icaact = _compute_ica_activations(inst, ica)
    # retrieve subset from eeglab
    constants_eeglab = loadmat(psd_constant_file)["constants"][0, 0]
    assert constants_eeglab["subset"].shape[0] == 1
    subset_eeglab = constants_eeglab["subset"][0, :] - 1
    # retrieve constants from python
    ncomp, nfreqs, n_points, nyquist, index, window, _ = _eeg_rpsd_constants(inst, ica)
    # compute psd
    psdmed = _eeg_rpsd_compute_psdmed(
        inst, icaact, ncomp, nfreqs, n_points, nyquist, index, window, subset_eeglab
    )
    psd = _eeg_rpsd_format(psdmed)
    psd *= 0.99

    # Compare with MATLAB
    features_eeglab = loadmat(eeglab_feature_file)["features"]
    topo_eeglab = features_eeglab[0, 0]
    psd_eeglab = features_eeglab[0, 1]
    autocorr_eeglab = features_eeglab[0, 2]
    assert np.allclose(topo, topo_eeglab)
    assert np.allclose(psd, psd_eeglab, atol=1e-6)
    # the autocorr for epoch does not have the same tolerance
    atol = 1e-8 if type_ == "raw" else 1e-4
    assert np.allclose(autocorr, autocorr_eeglab, atol=atol)


# ----------------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Estimated head radius.*:RuntimeWarning")
@pytest.mark.parametrize("file", [raw_eeglab_path, epo_eeglab_path])
def test_retrieve_eeglab_icawinv(file):
    """Test that the icawinv is correctly retrieved from an MNE ICA object."""
    ica = read_ica_eeglab(file)
    icawinv, _ = _retrieve_eeglab_icawinv(ica)

    eeg = _check_load_mat(file, None)
    assert np.allclose(icawinv, eeg.icawinv)


@pytest.mark.filterwarnings("ignore:Estimated head radius.*:RuntimeWarning")
@pytest.mark.parametrize(
    ("file", "eeglab_result_file"),
    [
        (raw_eeglab_path, raw_icaact_eeglab_path),
        (epo_eeglab_path, epo_icaact_eeglab_path),
    ],
)
def test_compute_ica_activations(file, eeglab_result_file):
    """Test that the icaact is correctly retrieved from an MNE ICA object."""
    type_ = str(Path(file).stem)[-3:]
    inst = reader[type_](file, **kwargs[type_])
    ica = read_ica_eeglab(file)
    icaact = _compute_ica_activations(inst, ica)

    icaact_eeglab = loadmat(eeglab_result_file)["icaact"]
    assert np.allclose(icaact, icaact_eeglab, atol=1e-4)


# ----------------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Estimated head radius.*:RuntimeWarning")
@pytest.mark.parametrize(
    ("file", "eeglab_result_file"),
    [(raw_eeglab_path, raw_topo1_path), (epo_eeglab_path, epo_topo1_path)],
)
def test_topoplotFast(file, eeglab_result_file):
    """Test topoplotFast on a single component."""
    # load inst
    type_ = str(Path(file).stem)[-3:]
    inst = reader[type_](file, **kwargs[type_])
    ica = read_ica_eeglab(file)
    # convert coordinates
    rd, th = _mne_to_eeglab_locs(inst, ica.ch_names)
    th = np.pi / 180 * th
    # get icawinv
    icawinv, _ = _retrieve_eeglab_icawinv(ica)
    # compute topo feature for the first component
    topo1 = _topoplotFast(icawinv[:, 0], rd, th)
    # load from eeglab
    topo1_eeglab = loadmat(eeglab_result_file)["topo1"]
    # convert nan to num
    assert np.allclose(topo1, topo1_eeglab, equal_nan=True)


@pytest.mark.filterwarnings("ignore:Estimated head radius.*:RuntimeWarning")
@pytest.mark.parametrize(
    ("file", "eeglab_result_file"),
    [
        (raw_eeglab_path, raw_topo_feature_path),
        (epo_eeglab_path, epo_topo_feature_path),
    ],
)
def test_eeg_topoplot(file, eeglab_result_file):
    """Test eeg_topoplot feature extraction."""
    # load inst
    type_ = str(Path(file).stem)[-3:]
    inst = reader[type_](file, **kwargs[type_])
    ica = read_ica_eeglab(file)
    # get icawinv
    icawinv, _ = _retrieve_eeglab_icawinv(ica)
    # compute feature
    topo = _eeg_topoplot(inst, icawinv, ica.ch_names)
    # load from eeglab
    topo_eeglab = loadmat(eeglab_result_file)["topo"]
    # compare
    assert np.allclose(topo, topo_eeglab, equal_nan=True)


def test_eeg_topoplot_invalid_montage():
    """Test that we raise an error if the montage is badly set."""
    raw = read_raw(raw_eeglab_path, preload=True)
    ica = read_ica_eeglab(raw_eeglab_path)
    # get icawinv
    icawinv, _ = _retrieve_eeglab_icawinv(ica)
    # compute feature
    raw.info["chs"][0]["loc"] = np.array([np.nan] * 12)
    with pytest.raises(ValueError, match="Channel position for .* is missing"):
        _eeg_topoplot(raw, icawinv, ica.ch_names)
    raw.set_montage(None)
    with pytest.raises(ValueError, match="Montage is not set"):
        _eeg_topoplot(raw, icawinv, ica.ch_names)


# ----------------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Estimated head radius.*:RuntimeWarning")
@pytest.mark.parametrize(
    ("fname", "constants_fname", "type_"),
    [
        (raw_eeglab_path, psd_constants_raw_path, "raw"),
        (epo_eeglab_path, psd_constants_epo_path, "epo"),
        (epo_long_eeglab_path, psd_constants_long_epo_path, "epo"),
    ],
)
def test_eeg_rpsd_constants(fname, constants_fname, type_):
    """Test _eeg_rpsd_constants function."""
    inst = reader[type_](fname, **kwargs[type_])
    ica = read_ica_eeglab(fname)
    ncomp, nfreqs, n_points, nyquist, index, window, subset = _eeg_rpsd_constants(
        inst, ica
    )

    constants_eeglab = loadmat(constants_fname)["constants"][0, 0]
    ncomp_eeglab = constants_eeglab["ncomp"][0, 0]
    nfreqs_eeglab = constants_eeglab["nfreqs"][0, 0]
    n_points_eeglab = constants_eeglab["n_points"][0, 0]
    nyquist_eeglab = constants_eeglab["nyquist"][0, 0]
    index_eeglab = constants_eeglab["index"]
    window_eeglab = constants_eeglab["window"]
    subset_eeglab = constants_eeglab["subset"]

    assert ncomp == ncomp_eeglab
    assert nfreqs == nfreqs_eeglab
    assert n_points == n_points_eeglab
    assert nyquist == nyquist_eeglab
    assert np.allclose(index, index_eeglab - 1)

    # window and subset are not squeezed in matlab
    assert window_eeglab.shape[0] == 1
    assert np.allclose(window, window_eeglab[0, :])

    # for subsets, compare if the same elements are in both
    assert subset_eeglab.shape[0] == 1
    assert len(set(list(subset)).difference(set(list(subset_eeglab[0, :] - 1)))) == 0
    assert len(set(list(subset_eeglab[0, :] - 1)).difference(set(list(subset)))) == 0


@pytest.mark.filterwarnings("ignore:Estimated head radius.*")
@pytest.mark.parametrize(
    ("fname", "constants_fname", "step_by_step_fname", "psd_fname", "type_"),
    [
        (
            raw_eeglab_path,
            psd_constants_raw_path,
            psd_steps_raw_path,
            psd_raw_path,
            "raw",
        ),
        (
            epo_eeglab_path,
            psd_constants_epo_path,
            psd_steps_epo_path,
            psd_epo_path,
            "epo",
        ),
        (
            epo_long_eeglab_path,
            psd_constants_long_epo_path,
            psd_steps_long_epo_path,
            psd_long_epo_path,
            "epo",
        ),
    ],
)
def test_eeg_rpsd(fname, constants_fname, step_by_step_fname, psd_fname, type_):
    """Test eeg_rpsd function that extract the PSD feature from the IC."""
    psd1 = loadmat(step_by_step_fname)["psd"]
    psd2 = loadmat(psd_fname)["psd"]
    assert np.allclose(psd1, psd2, atol=1e-4)

    # clean-up
    psd_eeglab = psd2.copy()
    del psd1
    del psd2

    # compute psd in Python
    inst = reader[type_](fname, **kwargs[type_])
    ica = read_ica_eeglab(fname)
    icaact = _compute_ica_activations(inst, ica)

    # retrieve subset from eeglab
    constants_eeglab = loadmat(constants_fname)["constants"][0, 0]
    assert constants_eeglab["subset"].shape[0] == 1
    subset_eeglab = constants_eeglab["subset"][0, :] - 1

    # retrieve the rest from python
    ncomp, nfreqs, n_points, nyquist, index, window, _ = _eeg_rpsd_constants(inst, ica)

    # compute psdmed
    psdmed = _eeg_rpsd_compute_psdmed(
        inst, icaact, ncomp, nfreqs, n_points, nyquist, index, window, subset_eeglab
    )

    # format and compare
    psd = _eeg_rpsd_format(psdmed)
    assert np.allclose(psd, psd_eeglab, atol=1e-5)


# ----------------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Estimated head radius.*:RuntimeWarning")
def test_eeg_autocorr_welch():
    """Test eeg_autocorr_welch feature used on long raw datasets."""
    raw = read_raw(raw_eeglab_path, preload=True)
    ica = read_ica_eeglab(raw_eeglab_path)
    icaact = _compute_ica_activations(raw, ica)
    autocorr = _eeg_autocorr_welch(raw, ica, icaact)
    assert autocorr.shape[1] == 100  # check resampling
    autocorr_eeglab = loadmat(autocorr_raw_path)["autocorr"]
    assert np.allclose(autocorr, autocorr_eeglab)


@pytest.mark.filterwarnings("ignore:Estimated head radius.*:RuntimeWarning")
def test_eeg_autocorr():
    """Test eeg_autocorr feature used on short raw datasets."""
    # Raw between 1 and 5 seconds
    raw = read_raw(raw_short_eeglab_path, preload=True)
    ica = read_ica_eeglab(raw_short_eeglab_path)
    icaact = _compute_ica_activations(raw, ica)
    autocorr = _eeg_autocorr(raw, ica, icaact)
    assert autocorr.shape[1] == 100  # check resampling
    autocorr_eeglab = loadmat(autocorr_short_raw_path)["autocorr"]
    assert np.allclose(autocorr, autocorr_eeglab, atol=1e-7)

    # Raw shorter than 1 second
    raw = read_raw(raw_very_short_eeglab_path, preload=True)
    ica = read_ica_eeglab(raw_very_short_eeglab_path)
    icaact = _compute_ica_activations(raw, ica)
    autocorr = _eeg_autocorr(raw, ica, icaact)

    autocorr_eeglab = loadmat(autocorr_very_short_raw_path)["autocorr"]
    assert np.allclose(autocorr, autocorr_eeglab, atol=1e-6)


@pytest.mark.filterwarnings("ignore:Estimated head radius.*:RuntimeWarning")
def test_eeg_autocorr_fftw():
    """Test eeg_autocorr_fftw feature used on epoch datasets."""
    epochs = read_epochs_eeglab(epo_eeglab_path)
    ica = read_ica_eeglab(epo_eeglab_path)
    icaact = _compute_ica_activations(epochs, ica)
    autocorr = _eeg_autocorr_fftw(epochs, ica, icaact)
    assert autocorr.shape[1] == 100  # check resampling
    autocorr_eeglab = loadmat(autocorr_epo_path)["autocorr"]
    assert np.allclose(autocorr, autocorr_eeglab, atol=1e-7)


def test_resampling(rng):
    """Test that we correctly resample the autocorrelation feature."""
    # similar dataset shape to the MNE sample dataset
    data = rng.integers(1, 10, (15, 601))

    # with integer
    resamp = _resample(data, fs=600)
    assert resamp.shape[1] == 101

    # with floats
    for fs in np.arange(599.2, 600, 0.1):
        resamp = _resample(data, fs=fs)
        assert resamp.shape[1] == 101
    for fs in np.arange(600.1, 600.9, 0.1):
        resamp = _resample(data, fs=fs)
        assert resamp.shape[1] == 101

    # similar dataset shape to the EEGLAB sample dataset
    data = rng.integers(1, 10, (30, 129))

    # with integer
    resamp = _resample(data, fs=128)
    assert resamp.shape[1] == 101

    # with floats
    for fs in np.arange(127.2, 128, 0.1):
        resamp = _resample(data, fs=fs)
        assert resamp.shape[1] == 101
    for fs in np.arange(128.1, 128.9, 0.1):
        resamp = _resample(data, fs=fs)
        assert resamp.shape[1] == 101
