#  -*- coding: utf-8 -*-
import gpu.core.integrate as integrate
from gpu.core.types import Tensor1D_or_3D
import gpu.core.static.weight_funcs as wf
from gpu.atmosphere import Atmosphere
from cpu.core.const import *


def krho(sa: 'Atmosphere', frequency: float) -> float:
    """
    :param frequency: частота излучения в ГГц
    :param sa: стандартная атмосфера (объект Atmosphere)
    :return: весовая функция krho (водяной пар)
    """
    tau_water_vapor = sa.opacity.water_vapor(frequency)
    return tau_water_vapor / (integrate.full(sa.absolute_humidity, sa.dh, sa.integration_method) / 10.)
    # return Staelin(sa, frequency)[0] * dB2np


def kw(sa: 'Atmosphere', frequency: float) -> Tensor1D_or_3D:
    """
    :param frequency: частота излучения в ГГц
    :param sa: объект Atmosphere
    :return: весовая функция k_w (вода в жидкокапельной фазе).
    """
    return wf.kw(frequency, sa.temperature)


def Staelin(sa: 'Atmosphere', frequency: float) -> Tensor1D_or_3D:
    """
    :param frequency: частота излучения в ГГц
    :param sa: стандартная атмосфера (объект Atmosphere)
    :return: весовая функция Стилина
    """
    return sa.attenuation.water_vapor(frequency) / sa.absolute_humidity
