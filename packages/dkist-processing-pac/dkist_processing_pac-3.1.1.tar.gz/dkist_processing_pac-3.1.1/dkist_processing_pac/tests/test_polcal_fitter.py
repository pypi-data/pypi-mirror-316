import numpy as np
import pytest

from dkist_processing_pac.fitter.polcal_fitter import PolcalFitter


def test_polcal_fitter_init(general_dresser, global_dresser, test_fit_mode, test_init_set):
    """
    Given: a Dresser and names of a fit mode and init set
    When: initializing a PolcalFitter object with these inputs
    Then: everything needed for the fit (including FitObjects objects) is correctly set up
    """
    mode_name, true_switches, true_vary = test_fit_mode
    init_name, true_CU_pars, true_TM_pars = test_init_set
    global_dresser, global_num_dims = global_dresser
    fitter = PolcalFitter(
        local_dresser=general_dresser,
        global_dresser=global_dresser,
        init_set=init_name,
        fit_mode=mode_name,
        _dont_fit=True,
    )
    wave_idx = np.argmin(np.abs(general_dresser.wavelength - true_CU_pars["wave"]))

    for obj in ["calibration_unit", "telescope", "dresser", "full_parameters"]:
        assert getattr(fitter.local_objects, obj) is not getattr(fitter.global_objects, obj)

    for par_name, prop_name in zip(
        ["t_ret", "t_pol", "ret0h", "ret045", "ret0r"],
        ["t_ret_0", "t_pol_0", "ret_0_h", "ret_0_45", "ret_0_r"],
    ):
        assert (
            getattr(fitter.local_objects.calibration_unit, prop_name)[0]
            == true_CU_pars["params"][par_name][wave_idx, 1]
        )
        assert (
            getattr(fitter.global_objects.calibration_unit, prop_name)[0]
            == true_CU_pars["params"][par_name][wave_idx, 1]
        )

    for p in ["x12", "t12", "x34", "t34", "x56", "t56"]:
        assert (
            getattr(fitter.local_objects.telescope, p)
            == fitter.local_objects.init_parameters[0, 0, 0][p]
        )
        assert (
            getattr(fitter.global_objects.telescope, p)
            == fitter.global_objects.init_parameters[tuple(0 for _ in range(global_num_dims))][p]
        )

    for s in true_switches.keys():
        assert true_switches[s] == fitter.local_objects.full_parameters.switches[s]
        assert true_switches[s] == fitter.global_objects.full_parameters.switches[s]

    for v in true_vary.keys():
        assert true_vary[v] == fitter.local_objects.full_parameters.vary[v]
        assert true_vary[v] == fitter.global_objects.full_parameters.vary[v]


def test_polcal_fitter_init_bad_global_shape(general_dresser, test_fit_mode, test_init_set):
    """
    Given: a dresser with more than a single bin
    When: using that dresser as the global dresser in the initialization of a PolcalFitter object
    Then: the correct error is raised
    """
    with pytest.raises(ValueError, match="Global dresser is expected to only have a single point"):
        PolcalFitter(
            local_dresser=general_dresser,
            global_dresser=general_dresser,
            init_set="use_M12",
            fit_mode="OCCal_VIS",
            _dont_fit=True,
        )


def test_polcal_fitter_init_nan_I_clears(general_dresser, global_dresser):
    """
    Given: dressers that have NaNs in their I_clear values
    When: initializing a `PolcalFitter` object
    Then: the correct error is raised
    """
    global_dresser = global_dresser[0]
    global_dresser.drawers[0].I_clear = np.array([np.nan])
    with pytest.raises(ValueError, match="Global dresser has NaNs in its I_clear:"):
        PolcalFitter(
            local_dresser=general_dresser,
            global_dresser=global_dresser,
            init_set="use_M12",
            fit_mode="OCCal_VIS",
            _dont_fit=True,
        )

    general_dresser.drawers[0].I_clear = np.array([np.nan])
    with pytest.raises(ValueError, match="Local dresser has NaNs in its I_clear:"):
        PolcalFitter(
            local_dresser=general_dresser,
            global_dresser=global_dresser,
            init_set="use_M12",
            fit_mode="OCCal_VIS",
            _dont_fit=True,
        )


def test_polcal_fitter_correct(fully_realistic_dresser, visp_modulation_matrix, test_fit_mode):
    """
    Given: a realistic set of polcal input data
    When: actually running the fit
    Then: the correct demodulation matrices are computed
    """
    fit_mode, _, _ = test_fit_mode
    fitter = PolcalFitter(
        local_dresser=fully_realistic_dresser,
        global_dresser=fully_realistic_dresser,
        fit_mode=fit_mode,
        init_set="OCCal_VIS",
        suppress_local_starting_values=True,
    )
    assert fitter.demodulation_matrices.shape == (1, 1, 1, 4, 10)
    np.testing.assert_allclose(
        fitter.demodulation_matrices[0, 0, 0], np.linalg.pinv(visp_modulation_matrix), rtol=1e-3
    )


@pytest.mark.parametrize(
    "data_fixture_name",
    [pytest.param("dresser_with_zeros", id="zeros"), pytest.param("dresser_all_nans", id="nans")],
)
def test_polcal_fitter_local_nan_handling(data_fixture_name, request, fully_realistic_dresser):
    """
    Given: A set of local polcal data with zero values in the uncertainty (i.e., will produce NaN when normalizing by
            uncertainty) OR a set of polcal data that have NaN values.
    When: Fitting the polcal data
    Then: Errors caused by NaNs in the objective function are caught and the resulting fit parameters all set to NaN
    """
    bad_local_dresser = request.getfixturevalue(data_fixture_name)
    fitter = PolcalFitter(
        local_dresser=bad_local_dresser,
        global_dresser=fully_realistic_dresser,
        fit_mode="use_M12_I_sys_per_step",
        init_set="OCCal_VIS",
        suppress_local_starting_values=True,
    )
    fit_params = fitter.local_objects.fit_parameters[0, 0, 0]
    for param_value in fit_params.valuesdict().values():
        assert param_value is np.nan


@pytest.mark.parametrize(
    "data_fixture_name",
    [pytest.param("dresser_with_zeros", id="zeros"), pytest.param("dresser_all_nans", id="nans")],
)
def test_polcal_fitter_global_nan_error(data_fixture_name, request, fully_realistic_dresser):
    """
    Given: A global Dresser that will cause NaN values in the fit
    When: Fitting the polcal data
    Then: The correct error is raised
    """
    bad_global_dresser = request.getfixturevalue(data_fixture_name)
    with pytest.raises(ValueError, match="NaN values detected in global fit"):
        fitter = PolcalFitter(
            local_dresser=fully_realistic_dresser,
            global_dresser=bad_global_dresser,
            fit_mode="use_M12_I_sys_per_step",
            init_set="OCCal_VIS",
            suppress_local_starting_values=True,
        )
