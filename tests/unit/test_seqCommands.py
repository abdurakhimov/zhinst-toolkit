import pytest
from hypothesis import given, assume, strategies as st
import numpy as np

from .context import SeqCommand



@given(t=st.integers(0, 3))
def test_header_comment(t):
    types = ["None", "Simple", "T1", "T2", "T2*"]
    type = types[t]
    assert type in SeqCommand.header_comment(type)


@given(i=st.integers(-1000, -1))
def test_repeat_negative(i):
    with pytest.raises(ValueError):
        SeqCommand.repeat(i)


@given(i=st.integers(0, 1000))
def test_repeat_positive(i):
    assert str(i) in SeqCommand.repeat(i)


@given(i=st.integers(-1000, -1))
def test_wait_negative(i):
    with pytest.raises(ValueError):
        SeqCommand.wait(i)


@given(i=st.integers(0, 1000))
def test_wait_positive(i):
    if i == 0:
        assert SeqCommand.wait(i) == ""
    else:
        assert str(i) in SeqCommand.wait(i)


@given(value=st.integers(-1, 2), index=st.integers(0, 3))
def test_trigger(value, index):
    if value not in [0, 1] or index not in [1, 2]:
        with pytest.raises(ValueError):
            SeqCommand.trigger(value, index)
    else:
        SeqCommand.trigger(value, index)


@given(i=st.integers(0, 1000), n=st.integers(0, 1000))
def test_count_waveform(i, n):
    line = SeqCommand.count_waveform(i, n)
    assert str(i + 1) in line
    assert str(n) in line


@given(amp1=st.floats(-1, 1), amp2=st.floats(-1, 1))
def test_play_wave_scaled(amp1, amp2):
    line = SeqCommand.play_wave_scaled(amp1, amp2)
    assert str(amp1) in line
    assert str(amp1) in line


@given(amp1=st.floats(-2, -1.001), amp2=st.floats(1.0001, 2))
def test_play_wave_scaled_error(amp1, amp2):
    with pytest.raises(ValueError):
        SeqCommand.play_wave_scaled(amp1, amp2)


@given(i=st.integers(-10, 10))
def test_play_wave_indexed(i):
    if i < 0:
        with pytest.raises(ValueError):
            SeqCommand.play_wave_indexed(i)
    else:
        assert str(i + 1) in SeqCommand.play_wave_indexed(i)


@given(i=st.integers(-10, 10), amp=st.floats(-2, 2))
def test_play_wave_indexed_scaled(i, amp):
    if i < 0 or abs(amp) > 1:
        with pytest.raises(ValueError):
            SeqCommand.play_wave_indexed_scaled(amp, amp, i)
    else:
        assert str(i + 1) in SeqCommand.play_wave_indexed_scaled(amp, amp, i)
        assert str(amp) in SeqCommand.play_wave_indexed_scaled(amp, amp, i)


@given(l=st.integers(-10, 100), i=st.integers(-1, 10))
def test_init_buffer_indexed(l, i):
    if i < 0 or l % 16 or l < 16:
        with pytest.raises(ValueError):
            SeqCommand.init_buffer_indexed(l, i)
    else:
        line = SeqCommand.init_buffer_indexed(l, i)
        assert str(i + 1) in line
        assert str(l) in line


@given(l=st.integers(0, 10000), p=st.integers(0, 10000), w=st.integers(0, 10000))
def test_init_gauss(l, p, w):
    if not (l > p and l > w) or l % 16 or w <= 0:
        with pytest.raises(ValueError):
            SeqCommand.init_gauss([l, p, w])
    else:
        line = SeqCommand.init_gauss([l, p, w])
        assert f"({l}, {p}, {w})" in line


@given(
    amp=st.floats(-2, 2),
    l=st.integers(0, 10000),
    p=st.integers(0, 10000),
    w=st.integers(0, 10000),
)
def test_init_gauss_scaled(amp, l, p, w):
    if not (l > p and l > w) or l % 16 or w <= 0 or abs(amp) > 1:
        with pytest.raises(ValueError):
            SeqCommand.init_gauss_scaled(amp, [l, p, w])
    else:
        line = SeqCommand.init_gauss_scaled(amp, [l, p, w])
        assert f"({l}, {p}, {w})" in line
        assert str(amp) in line


@given(i=st.integers(-1, 5))
def test_wait_trigger(i):
    if i not in [0, 1, 2]:
        with pytest.raises(ValueError):
            SeqCommand.wait_dig_trigger(i)
    else:
        SeqCommand.wait_dig_trigger(i)
