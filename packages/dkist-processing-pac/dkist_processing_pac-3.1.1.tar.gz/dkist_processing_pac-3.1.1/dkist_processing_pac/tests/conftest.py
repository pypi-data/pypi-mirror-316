import datetime
import importlib.resources as resources
from collections import defaultdict
from copy import deepcopy

import asdf
import numpy as np
import pytest
from astropy import coordinates
from astropy.io import fits
from astropy.time import Time
from dkist_data_simulator.dataset import key_function
from dkist_data_simulator.spec122 import Spec122Dataset
from dkist_header_validator import spec122_validator
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess

from dkist_processing_pac.fitter.fitter_parameters import PolcalDresserParameters
from dkist_processing_pac.input_data.drawer import Drawer
from dkist_processing_pac.input_data.dresser import Dresser
from dkist_processing_pac.optics.calibration_unit import CalibrationUnit
from dkist_processing_pac.optics.telescope import Telescope


def compute_telgeom(time_hst: Time):
    dkist_lon = (156 + 15 / 60.0 + 21.7 / 3600.0) * (-1)
    dkist_lat = 20 + 42 / 60.0 + 27.0 / 3600.0
    hel = 3040.4
    hloc = coordinates.EarthLocation.from_geodetic(dkist_lon, dkist_lat, hel)
    sun_body = coordinates.get_body("sun", time_hst, hloc)  # get the solar ephemeris
    azel_frame = coordinates.AltAz(obstime=time_hst, location=hloc)  # Horizon coords
    sun_altaz = sun_body.transform_to(azel_frame)  # Sun in horizon coords
    alt = sun_altaz.alt.value  # Extract altitude
    azi = sun_altaz.az.value  # Extract azimuth

    tableang = alt - azi

    return {"TELEVATN": alt, "TAZIMUTH": azi, "TTBLANGL": tableang}


class CalibrationSequenceStepDataset(Spec122Dataset):
    def __init__(
        self,
        array_shape: tuple[int, ...],
        time_delta: float,
        pol_status: str,
        pol_theta: float,
        ret_status: str,
        ret_theta: float,
        dark_status: str,
        instrument: str = "visp",
        num_mod: int = 3,
        start_time: str | datetime.datetime | None = None,
    ):
        self.num_mod = num_mod

        # Make up a Calibration sequence. Mostly random except for two clears and two darks at start and end, which
        # we want to test
        self.pol_status = pol_status
        self.pol_theta = pol_theta
        self.ret_status = ret_status
        self.ret_theta = ret_theta
        self.dark_status = dark_status
        dataset_shape = (self.num_mod,) + array_shape[1:]
        super().__init__(
            dataset_shape,
            array_shape,
            time_delta,
            instrument=instrument,
            start_time=start_time or datetime.datetime.now(),
        )
        self.add_constant_key("DKIST004", "polcal")
        self.add_constant_key("WAVELNTH", 666.0)

    @key_function("VISP_011")
    def modstate(self, key: str) -> int:
        return (self.index % self.num_mod) + 1

    @key_function("VISP_010")
    def nummod(self, key: str) -> int:
        return self.num_mod

    @key_function("PAC__004")
    def polarizer_status(self, key: str) -> str:
        return self.pol_status

    @key_function("PAC__005")
    def polarizer_angle(self, key: str) -> str:
        return "none" if self.pol_status == "clear" else str(self.pol_theta)

    @key_function("PAC__006")
    def retarter_status(self, key: str) -> str:
        return self.ret_status

    @key_function("PAC__007")
    def retarder_angle(self, key: str) -> str:
        return "none" if self.ret_status == "clear" else str(self.ret_theta)

    @key_function("PAC__008")
    def gos_level3_status(self, key: str) -> str:
        return self.dark_status

    @key_function("TAZIMUTH", "TELEVATN", "TTBLANGL")
    def telescope_geometry(self, key: str):
        return compute_telgeom(Time(self.date_obs(key), format="fits"))[key]


class InstAccess(L0FitsAccess):
    def __init__(self, hdu: fits.ImageHDU | fits.PrimaryHDU | fits.CompImageHDU):
        super().__init__(hdu, auto_squeeze=False)
        self.modulator_state = self.header["VSPSTNUM"]
        self.number_of_modulator_states = self.header["VSPNUMST"]


@pytest.fixture(scope="session")
def general_cs():
    # Make up a Calibration sequence. Mostly random except for two clears and two darks at start and end, which
    # we want to test
    pol_status = [
        "clear",
        "clear",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "clear",
        "clear",
    ]
    pol_theta = [0.0, 0.0, 60.0, 0.0, 120.0, 0.0, 0.0]
    ret_status = ["clear", "clear", "clear", "SiO2 SAR", "clear", "clear", "clear"]
    ret_theta = [0.0, 0.0, 0.0, 45.0, 0.0, 0.0, 0.0]
    dark_status = [
        "DarkShutter",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "DarkShutter",
    ]
    num_steps = len(pol_theta)
    out_dict = dict()
    start_time = datetime.datetime(2001, 11, 17)
    for n in range(num_steps):
        ds = CalibrationSequenceStepDataset(
            array_shape=(1, 2, 2),
            time_delta=2.0,
            pol_status=pol_status[n],
            pol_theta=pol_theta[n],
            ret_status=ret_status[n],
            ret_theta=ret_theta[n],
            dark_status=dark_status[n],
            start_time=start_time,
        )
        header_list = [
            spec122_validator.validate_and_translate_to_214_l0(
                d.header(), return_type=fits.HDUList
            )[0].header
            for d in ds
        ]
        hdu_list = []
        for m in range(ds.num_mod):
            hdu_list.append(
                fits.PrimaryHDU(
                    data=np.ones((3, 4, 1)) * n + 100 * m, header=fits.Header(header_list.pop(0))
                )
            )

        out_dict[n] = [InstAccess(h) for h in hdu_list]
        start_time = ds.start_time + datetime.timedelta(seconds=60)

    return (
        out_dict,
        pol_status,
        pol_theta,
        ret_status,
        ret_theta,
        dark_status,
        num_steps,
        ds.num_mod,
    )


@pytest.fixture(scope="session", params=[1, 2, 3, 4, 5], ids=["1D", "2D", "3D", "4D", "5D"])
def general_cs_arbitrary_shape(general_cs, request):
    num_dims = request.param
    num_new_dims = num_dims - 1

    # deepcopy needed or else subsequent tests that use the raw "general_cs" fixture will have jacked up shapes.
    out_dict = deepcopy(general_cs[0])
    num_steps, num_mod = general_cs[-2:]
    for obj_list in out_dict.values():
        for obj in obj_list:
            data = obj.data
            # Stuff all current dimensions into the first of the new data
            data_size = np.prod(data.shape)
            new_shape = tuple([data_size] + [1] * num_new_dims)
            obj.data = np.reshape(data, new_shape)

    return out_dict, num_dims, num_steps, num_mod


@pytest.fixture(scope="session", params=[1, 5], ids=["1D", "5D"])
def global_cs(request):
    # Make up a Calibration sequence. Mostly random except for two clears and two darks at start and end, which
    # we want to test
    num_dims = request.param
    pol_status = [
        "clear",
        "clear",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "clear",
        "clear",
    ]
    pol_theta = [0.0, 0.0, 60.0, 0.0, 120.0, 0.0, 0.0]
    ret_status = ["clear", "clear", "clear", "SiO2 SAR", "clear", "clear", "clear"]
    ret_theta = [0.0, 0.0, 0.0, 45.0, 0.0, 0.0, 0.0]
    dark_status = [
        "DarkShutter",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "DarkShutter",
    ]
    num_steps = len(pol_theta)
    out_dict = dict()
    start_time = None
    for n in range(num_steps):
        ds = CalibrationSequenceStepDataset(
            array_shape=(1, 2, 2),
            time_delta=2.0,
            pol_status=pol_status[n],
            pol_theta=pol_theta[n],
            ret_status=ret_status[n],
            ret_theta=ret_theta[n],
            dark_status=dark_status[n],
            start_time=start_time,
        )
        header_list = [
            spec122_validator.validate_and_translate_to_214_l0(
                d.header(), return_type=fits.HDUList
            )[0].header
            for d in ds
        ]
        hdu_list = []
        for m in range(ds.num_mod):
            hdu_list.append(
                fits.PrimaryHDU(
                    data=np.ones(tuple(1 for _ in range(num_dims))) * n + 100 * m,
                    header=fits.Header(header_list.pop(0)),
                )
            )

        out_dict[n] = [InstAccess(h) for h in hdu_list]
        start_time = ds.start_time + datetime.timedelta(seconds=60)

    return out_dict, pol_status, pol_theta, ret_status, ret_theta, dark_status, num_dims


@pytest.fixture
def general_drawer(general_cs) -> Drawer:
    out_dict = general_cs[0]
    return Drawer(out_dict)


@pytest.fixture
def general_dresser(general_drawer) -> Dresser:
    dresser = Dresser()
    dresser.add_drawer(general_drawer)
    return dresser


@pytest.fixture
def global_dresser(global_cs) -> tuple[Dresser, int]:
    out_dict = global_cs[0]
    num_dims = global_cs[-1]
    dresser = Dresser()
    dresser.add_drawer(Drawer(out_dict))

    return dresser, num_dims


@pytest.fixture(scope="session")
def session_dresser(general_cs) -> Dresser:
    dresser = Dresser()
    dresser.add_drawer(Drawer(general_cs[0]))
    return dresser


@pytest.fixture(scope="session")
def cs_with_correct_geometry():
    dark_status = [
        "DarkShutter",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "DarkShutter",
    ]
    ret_theta = [0, 0, 0, 0, 0, 0, 60, 120, 30, 90, 150, 0, 0, 0]
    ret_status = [
        "clear",
        "clear",
        "clear",
        "clear",
        "clear",
        "SiO2 SAR",
        "SiO2 SAR",
        "SiO2 SAR",
        "SiO2 SAR",
        "SiO2 SAR",
        "SiO2 SAR",
        "SiO2 SAR",
        "clear",
        "clear",
    ]
    pol_theta = [0, 0, 0, 60, 120, 0, 0, 0, 45, 45, 45, 45, 0, 0]
    pol_status = [
        "clear",
        "clear",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "Sapphire Polarizer",
        "clear",
        "clear",
    ]
    data_shape = (1, 1, 1)
    num_steps = len(pol_theta)
    out_dict = dict()
    start_time = datetime.datetime.fromisoformat("2022-05-25T12:00:00")
    for n in range(num_steps):
        ds = CalibrationSequenceStepDataset(
            array_shape=(1, 2, 2),
            time_delta=2.0,
            pol_status=pol_status[n],
            pol_theta=pol_theta[n],
            ret_status=ret_status[n],
            ret_theta=ret_theta[n],
            dark_status=dark_status[n],
            start_time=start_time,
            num_mod=10,
        )
        header_list = [
            spec122_validator.validate_and_translate_to_214_l0(
                d.header(), return_type=fits.HDUList
            )[0].header
            for d in ds
        ]
        hdu_list = []
        for m in range(ds.num_mod):
            hdu_list.append(
                fits.PrimaryHDU(
                    data=np.ones(data_shape) * 1e3, header=fits.Header(header_list.pop(0))
                )
            )

        out_dict[n] = [InstAccess(h) for h in hdu_list]
        start_time = ds.start_time + datetime.timedelta(seconds=60)

    return out_dict, data_shape


@pytest.fixture(scope="session")
def visp_modulation_matrix() -> np.ndarray:
    # Modulation matrix for AdW's synthetic ViSP data from mod_matrix_630.out
    return np.array(
        [
            [1.0, 0.19155013, 0.80446989, -0.47479524],
            [1.0, -0.65839661, 0.68433984, 0.00466389],
            [1.0, -0.80679413, -0.16112977, 0.48234158],
            [1.0, -0.04856211, -0.56352868, 0.77578117],
            [1.0, 0.56844858, 0.03324473, 0.77289873],
            [1.0, 0.19155013, 0.80446989, 0.47479524],
            [1.0, -0.65839661, 0.68433984, -0.00466389],
            [1.0, -0.80679413, -0.16112977, -0.48234158],
            [1.0, -0.04856211, -0.56352868, -0.77578117],
            [1.0, 0.56844858, 0.03324473, -0.77289873],
        ],
        dtype=np.float64,
    )


@pytest.fixture(scope="session")
def fully_realistic_cs(cs_with_correct_geometry, visp_modulation_matrix):

    fit_mode = "use_M12"
    init_set = "OCCal_VIS"
    cs_dict, data_shape = cs_with_correct_geometry
    dresser = Dresser()
    dresser.add_drawer(Drawer(cs_dict, skip_darks=False))
    CM = CalibrationUnit(dresser)
    TM = Telescope(dresser)
    full_params = PolcalDresserParameters(dresser, fit_mode, init_set)

    global_params = full_params.init_params._all_parameters[0]
    pardict = global_params.valuesdict()
    CM.load_pars_from_dict(pardict)
    TM.load_pars_from_dict(pardict)

    CM.I_sys[0] = 1e4

    # Has shape (4, N)
    S = np.sum((TM.TM @ CM.CM @ TM.M12) * CM.S_in[:, None, :], axis=2).T

    # Has shape (M, N)
    observed = visp_modulation_matrix @ S

    # Now set the "observed" value for each of the input objects
    for m in range(dresser.nummod):
        for n in range(dresser.numsteps):
            cs_dict[n][m].data *= observed[m, n] / np.mean(cs_dict[n][m].data)

    return cs_dict


@pytest.fixture(scope="session")
def dresser_with_zeros(fully_realistic_cs):

    zero_cs_dict = defaultdict(list)
    for step, step_list in fully_realistic_cs.items():
        for hdu in step_list:
            zero_cs_dict[step].append(deepcopy(hdu))

    num_steps = len(zero_cs_dict)
    zero_cs_dict[num_steps - 2][2].data *= 0.0

    dresser = Dresser()
    dresser.add_drawer(Drawer(zero_cs_dict, remove_I_trend=False))

    return dresser


@pytest.fixture(scope="session")
def dresser_all_nans(fully_realistic_cs):

    nan_cs_dict = defaultdict(list)
    for step, step_list in fully_realistic_cs.items():
        for hdu in step_list:
            hdu_copy = deepcopy(hdu)
            hdu_copy.data *= np.nan
            nan_cs_dict[step].append(hdu_copy)

    dresser = Dresser()
    dresser.add_drawer(Drawer(nan_cs_dict, remove_I_trend=False))

    # We need this to be non-NaN so CM.S_in is set correctly
    dresser.drawers[0].I_clear = np.array([1e4])

    return dresser


@pytest.fixture(scope="session")
def fully_realistic_dresser(fully_realistic_cs):
    dresser = Dresser()
    dresser.add_drawer(Drawer(fully_realistic_cs))
    return dresser


mode_test_params = [("use_M12", False), ("use_M12_I_sys_per_step", True)]


@pytest.fixture(scope="session", params=mode_test_params, ids=["Single I_sys", "I_sys per step"])
def test_fit_mode(request) -> tuple[str, dict[str, bool], dict[str, bool]]:
    mode_name, I_sys_per_CS_step = request.param
    name = str(mode_name)
    switches = {
        "delta_d": False,
        "use_M12": True,
        "use_T": True,
        "global_transmission": False,
        "global_retardance": False,
        "fit_bounds": False,
        "I_sys_per_CS_step": I_sys_per_CS_step,
    }
    vary = {
        "I_sys": True,
        "t_pol": not I_sys_per_CS_step,
        "t_ret": not I_sys_per_CS_step,
        "Q_in": True,
        "U_in": False,
        "V_in": False,
        "ret0h": True,
        "ret045": True,
        "ret0r": True,
    }

    return name, switches, vary


@pytest.fixture(scope="session")
def test_init_set() -> tuple[str, dict, dict]:
    name = "OCCal_VIS"
    cu_init_location = (
        resources.files("dkist_processing_pac") / "data" / "init_values" / f"{name}_cu_pars.asdf"
    )
    with resources.as_file(cu_init_location) as cu_init_path:
        with asdf.open(cu_init_path, "rb", lazy_load=False, memmap=False) as f:
            cu_init_pars = f.tree

    telescope_init_location = (
        resources.files("dkist_processing_pac") / "data" / "init_values" / f"{name}_tm_pars.asdf"
    )
    with resources.as_file(telescope_init_location) as telescope_init_path:
        with asdf.open(telescope_init_path, "rb", lazy_load=False, memmap=False) as f:
            telescope_init_pars = f.tree

    return name, cu_init_pars, telescope_init_pars
