import logging
import threading
from time import sleep

import pytest
import time
import spin_stepper as sp
from spin_stepper import SpinDirection, SpinStatus

logger = logging.getLogger(__name__)

"""
This test requires:
* Two L6470 devices chained together.
* A stepper motor with end switch connected to tha last device (0) in the chain.
"""


def setup_motor(_motor: sp.SpinDevice):
    """
    This is a hook for running tests with motors that can't run with default config.
    """
    _motor.set_acceleration(dec=200, acc=200)
    _motor.set_speed_limits(min_speed=2.0, max_speed=500.0)
    _motor.set_micro_step(16)
    _motor.set_ocd_th(3.0)
    _motor.set_stall_th(1.5)
    _motor.set_kval(kval_hold=0.05, kval_acc=0.1, kval_run=0.1, kval_dec=0.1)


@pytest.fixture
def motor() -> sp.SpinDevice:
    st_chain = sp.SpinChain(
        total_devices=2,
        spi_select=(0, 0),
    )
    _motor = st_chain.create(1)  # first motor, but this is the last in the chain.
    _motor.reset_device()
    time.sleep(0.1)
    _motor.hard_hiz()
    yield _motor
    _motor.hard_hiz()


def test_register_enum():
    assert sp.SpinRegister.ACC.value == 0x05
    assert sp.SpinRegister.ACC.size == 2

    assert sp.SpinRegister.STALL_TH.value == 0x14
    assert sp.SpinRegister.STALL_TH.size == 1


def test_get_register(motor: sp.SpinDevice):
    assert 0 < motor.get_register(sp.SpinRegister.ADC_OUT) < 128
    print(f"\nADC out:{motor.get_register(sp.SpinRegister.ADC_OUT)}\n")

    assert 0 < motor.get_register(sp.SpinRegister.STEP_MODE) < 9
    print(f"StepMode:{motor.get_register(sp.SpinRegister.STEP_MODE)}\n")


def test_set_register(motor: sp.SpinDevice):
    old_step_mode = motor.get_register(sp.SpinRegister.STEP_MODE)
    motor.set_register(sp.SpinRegister.STEP_MODE, 3)
    assert motor.get_register(sp.SpinRegister.STEP_MODE) == 3
    motor.set_register(sp.SpinRegister.STEP_MODE, old_step_mode)
    assert motor.get_register(sp.SpinRegister.STEP_MODE) == old_step_mode


def test_get_status(motor: sp.SpinDevice):
    motor.get_status()  # clear old warnings
    status = motor.get_status()
    logger.info(f"Status:{status.name}")
    assert status is SpinStatus.HiZ


def test_is_busy(motor: sp.SpinDevice):
    motor.get_status()  # clear old warnings
    assert motor.is_busy() is False


def test_abs_pos(motor: sp.SpinDevice):
    # this should be 0 after reset
    assert motor.abs_pos == 0
    motor.move(1000)
    assert motor.is_busy() is True

    while motor.is_busy():
        time.sleep(0.1)

    assert motor.abs_pos == 1000


def test_abs_pos_negative(motor: sp.SpinDevice):
    assert motor.abs_pos == 0

    motor.direction = sp.SpinDirection.Reverse
    motor.move(1000)
    assert motor.is_busy() is True

    while motor.is_busy():
        time.sleep(0.1)

    assert motor.abs_pos == -1000


def test_get_speed_limits(motor: sp.SpinDevice):
    min_speed, max_speed = motor.get_speed_limits()
    assert min_speed == pytest.approx(0.0, abs=0.1)
    assert max_speed == pytest.approx(991.8, abs=15.25)


def test_set_speed_limits(motor: sp.SpinDevice):
    min_limit = 1.0
    max_limit = 200.0
    motor.set_speed_limits(min_speed=min_limit, max_speed=max_limit)
    min_speed, max_speed = motor.get_speed_limits()
    assert min_speed == pytest.approx(min_limit, abs=0.1)
    assert max_speed == pytest.approx(max_limit, abs=15.25)


def test_get_acceleration(motor: sp.SpinDevice):
    dec, acc = motor.get_acceleration()
    assert dec == pytest.approx(2008.0, abs=15.0)
    assert acc == pytest.approx(2008.0, abs=15.0)


def test_set_acceleration(motor: sp.SpinDevice):
    motor.set_acceleration(500.0, 600.0)
    dec, acc = motor.get_acceleration()
    assert dec == pytest.approx(500, abs=15.0)
    assert acc == pytest.approx(600.0, abs=15.0)

    motor.set_acceleration(500.0, 600.0)


def test_get_fs_spd(motor: sp.SpinDevice):
    assert motor.get_fs_spd() == pytest.approx(602.7, abs=15.25)


def test_set_fs_spd(motor: sp.SpinDevice):
    motor.set_fs_spd(500.0)
    assert motor.get_fs_spd() == pytest.approx(500.0, abs=15.25)


def test_get_kval(motor: sp.SpinDevice):
    kval_hold, kval_run, kval_acc, kval_dec = motor.get_kval()
    assert kval_hold == pytest.approx(0.16, abs=0.004)
    assert kval_run == pytest.approx(0.16, abs=0.004)
    assert kval_acc == pytest.approx(0.16, abs=0.004)
    assert kval_dec == pytest.approx(0.16, abs=0.004)


def test_set_kval(motor: sp.SpinDevice):
    motor.set_kval(kval_hold=0.1, kval_run=0.2, kval_acc=0.3, kval_dec=0.4)
    kval_hold, kval_run, kval_acc, kval_dec = motor.get_kval()
    assert kval_hold == pytest.approx(0.1, abs=0.004)
    assert kval_run == pytest.approx(0.2, abs=0.004)
    assert kval_acc == pytest.approx(0.3, abs=0.004)
    assert kval_dec == pytest.approx(0.4, abs=0.004)


def test_get_bemf(motor: sp.SpinDevice):
    int_speed, st_slp, fn_slp_acc, fn_slp_dec = motor.get_bemf()
    assert int_speed == pytest.approx(61.5, abs=0.06)
    assert st_slp == pytest.approx(0.038, abs=0.003)
    assert fn_slp_acc == pytest.approx(0.063, abs=0.003)
    assert fn_slp_dec == pytest.approx(0.063, abs=0.003)


def test_set_bemf(motor: sp.SpinDevice):
    motor.set_bemf(int_speed=60.0, st_slp=0.1, fn_slp_acc=0.2, fn_slp_dec=0.3)
    int_speed, st_slp, fn_slp_acc, fn_slp_dec = motor.get_bemf()
    assert int_speed == pytest.approx(60, abs=0.06)
    assert st_slp == pytest.approx(0.1, abs=0.003)
    assert fn_slp_acc == pytest.approx(0.2, abs=0.003)
    assert fn_slp_dec == pytest.approx(0.3, abs=0.003)


def test_get_k_therm(motor: sp.SpinDevice):
    assert motor.get_k_therm() == pytest.approx(1.0, abs=0.03)


def test_set_k_therm(motor: sp.SpinDevice):
    motor.set_k_therm(1.2)
    assert motor.get_k_therm() == pytest.approx(1.2, abs=0.03)


def test_get_adc(motor: sp.SpinDevice):
    value = motor.adc_out
    logger.info(f"ADC: {value}")
    assert 8 / 32 < value < 30 / 32


def test_get_ocd_th(motor: sp.SpinDevice):
    assert motor.get_ocd_th() == pytest.approx(3.38, abs=0.375)


def test_set_ocd_th(motor: sp.SpinDevice):
    motor.set_ocd_th(2.0)
    assert motor.get_ocd_th() == pytest.approx(2.0, abs=0.375)


def test_get_stall_th(motor: sp.SpinDevice):
    assert motor.get_stall_th() == pytest.approx(2.03, abs=0.032)


def test_set_stall_th(motor: sp.SpinDevice):
    motor.set_stall_th(1.0)
    assert motor.get_stall_th() == pytest.approx(1.0, abs=0.032)


def test_get_micro_step(motor: sp.SpinDevice):
    assert motor.get_micro_step() == 128


def test_set_step_mode(motor: sp.SpinDevice):
    motor.set_micro_step(8)
    assert motor.get_micro_step() == 8


def test_set_illegal_tep_mode(motor: sp.SpinDevice):
    with pytest.raises(ValueError):
        motor.set_micro_step(3)


@pytest.mark.timeout(10)
def test_move(motor: sp.SpinDevice):
    setup_motor(motor)
    motor.move(10000, direction=sp.SpinDirection.Forward)
    assert motor.is_busy() is True
    while motor.is_busy():
        time.sleep(0.1)

    assert motor.abs_pos == 10000

    motor.move(8000, direction=sp.SpinDirection.Reverse)
    assert motor.is_busy() is True
    while motor.is_busy():
        time.sleep(0.1)

    assert motor.abs_pos == 2000


@pytest.mark.timeout(10)
def test_go_to(motor: sp.SpinDevice):
    motor.go_to(10000)
    while motor.is_busy():
        time.sleep(0.1)
    assert motor.abs_pos == 10000

    # negative position
    motor.reset_position()
    motor.go_to(-1000)
    while motor.is_busy():
        time.sleep(0.1)
    assert motor.abs_pos < 0


@pytest.mark.timeout(10)
def test_go_home(motor: sp.SpinDevice):
    motor.go_to(10000)
    while motor.is_busy():
        time.sleep(0.1)
    assert motor.abs_pos == 10000

    motor.go_home()
    while motor.is_busy():
        time.sleep(0.1)
    assert motor.abs_pos == 0


@pytest.mark.timeout(10)
def test_go_mark(motor: sp.SpinDevice):
    motor.mark = 5000
    assert motor.mark == 5000
    motor.go_mark()
    while motor.is_busy():
        time.sleep(0.1)

    assert motor.abs_pos == 5000


def test_speed(motor: sp.SpinDevice):
    setup_motor(motor)
    time.sleep(1.0)
    assert motor.speed < 5.0
    motor.run(speed=200)
    time.sleep(1.0)
    speed = motor.speed
    assert speed > 190
    motor.soft_hiz()


@pytest.mark.timeout(10)
def test_reset_position(motor: sp.SpinDevice):
    assert motor.abs_pos == 0
    motor.move(1000)
    while motor.is_busy():
        time.sleep(0.1)
    assert motor.abs_pos == 1000
    motor.reset_position()
    assert motor.abs_pos == 0


def test_hard_stop(motor: sp.SpinDevice):
    motor.run(100)
    time.sleep(1.0)
    motor.hard_stop()
    assert motor.is_busy() is False
    assert sp.SpinStatus.HiZ not in motor.get_status()


def test_hard_hiz(motor: sp.SpinDevice):
    motor.run(100)
    time.sleep(1.0)
    motor.hard_hiz()
    assert motor.is_busy() is False
    assert sp.SpinStatus.HiZ in motor.get_status()


@pytest.mark.timeout(10)
def test_soft_stop(motor: sp.SpinDevice):
    setup_motor(motor)
    motor.run(2000)
    time.sleep(2.0)
    motor.soft_stop()
    assert motor.is_busy() is True
    assert sp.SpinStatus.HiZ not in motor.get_status()
    while motor.is_busy():
        time.sleep(0.1)
    assert sp.SpinStatus.HiZ not in motor.get_status()


@pytest.mark.timeout(10)
def test_soft_hiz(motor: sp.SpinDevice):
    motor.run(200)
    time.sleep(1.0)
    motor.soft_hiz()
    assert motor.is_busy() is True
    start = time.monotonic()
    while motor.is_busy():
        time.sleep(0.1)
    assert sp.SpinStatus.HiZ in motor.get_status()


@pytest.mark.timeout(30)
def test_go_until(motor: sp.SpinDevice):
    setup_motor(motor)
    motor.move(2000)
    while motor.is_busy():
        time.sleep(0.1)
    assert sp.SpinStatus.SwitchFlag not in motor.get_status()

    motor.go_until(direction=sp.SpinDirection.Reverse, speed=200)

    while motor.is_busy():
        time.sleep(0.1)
    assert sp.SpinStatus.SwitchFlag in motor.get_status()
    assert 0 <= motor.abs_pos <= 5


@pytest.mark.timeout(60)
def test_go_until_and_release(motor: sp.SpinDevice):
    """
    Test homing using a switch.
    First move towards switch for course home position.
    Then move away from switch until released to get accurate home position.
    :param motor:
    :return:
    """
    setup_motor(motor)
    motor.direction = sp.SpinDirection.Forward
    motor.move(20000)
    while motor.is_busy():
        time.sleep(0.1)
    motor.go_until(direction=sp.SpinDirection.Reverse, speed=200)
    while motor.is_busy():
        time.sleep(0.1)
    assert 0 <= motor.abs_pos <= 5
    time.sleep(0.1)
    assert sp.SpinStatus.SwitchFlag in motor.get_status()

    motor.release_switch(direction=sp.SpinDirection.Forward)
    while motor.is_busy():
        time.sleep(0.1)
    assert motor.abs_pos < 100

    motor.move(10000)
    start = time.monotonic()
    while motor.is_busy():
        time.sleep(0.1)
    time.sleep(0.1)
    assert sp.SpinStatus.SwitchFlag not in motor.get_status()

    motor.go_home()
    while motor.is_busy() and time.monotonic():
        time.sleep(0.1)
    assert 0 <= motor.abs_pos <= 5


def test_multi_thread(motor: sp.SpinDevice):
    def loop(_motor, name):
        while run:
            speed = _motor.speed
            pos = _motor.abs_pos
            status = _motor.status
            logger.info(f"{name} {speed=} ({pos=} {status=})")
            time.sleep(0.001)

    run = True
    setup_motor(motor)
    thread1 = threading.Thread(target=loop, args=(motor, 'thread_1'), daemon=True)
    thread1.start()
    thread2 = threading.Thread(target=loop, args=(motor, 'thread_2'), daemon=True)
    thread2.start()
    motor.run(200, SpinDirection.Forward)
    last_pos = motor.abs_pos
    for i in range(100):
        time.sleep(0.05)
        speed = motor.speed
        pos = motor.abs_pos
        assert pos > last_pos
        last_pos = pos
        logger.info(f"for {speed=} ({pos=})")
    motor.soft_hiz()
    run = False
    thread1.join(1.0)
    thread2.join(1.0)


def test_step_modes_speed(motor: sp.SpinDevice):
    """
    Speed settings does not depend on micro step mode.
    :param motor:
    :return:
    """
    setup_motor(motor)
    speed = 200
    step_modes = [2, 16, 128]

    for step_mode in step_modes:
        motor.set_micro_step(step_mode)
        logger.info(f"{motor.get_micro_step()} micro steps")
        assert motor.get_micro_step() == step_mode
        motor.run(speed)
        time.sleep(5)
        assert motor.speed == pytest.approx(speed, abs=20)
        motor.soft_hiz()
        time.sleep(2)

def test_step_modes_move(motor: sp.SpinDevice):
    """
    Position and distance settings do depend on micro step mode.
    :param motor:
    :return:
    """
    setup_motor(motor)
    motor.set_speed_limits(max_speed=500)
    distance = 1000
    step_modes = [2, 16, 128]

    for step_mode in step_modes:
        motor.set_micro_step(step_mode)
        logger.info(f"{motor.get_micro_step()} micro steps")
        assert motor.get_micro_step() == step_mode
        motor.move(distance * step_mode)
        while motor.is_busy():
            time.sleep(0.1)
        motor.soft_hiz()
        time.sleep(2)
