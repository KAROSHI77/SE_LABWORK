from hypothesis import given, strategies as st
from pet_boarding import parse_booking, stay_average, payable_fee


@given(st.one_of(st.text(), st.none()))
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except (TypeError, ValueError):
        pass


@given(st.one_of(st.text(), st.none()))
def test_stay_average_no_crash(s):
    try:
        stay_average(s)
    except (TypeError, ValueError, ZeroDivisionError):
        pass


@given(st.one_of(st.text(), st.none()))
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except (TypeError, ValueError):
        pass


@given(st.lists(st.integers(min_value=0), min_size=1, max_size=20))
def test_stay_average_mean(values):
    csv = ",".join(map(str, values))
    result = stay_average(csv)
    assert result == sum(values) / len(values)


@given(
    st.floats(min_value=0, max_value=100000,
              allow_nan=False, allow_infinity=False),
    st.floats(min_value=0, max_value=100000,
              allow_nan=False, allow_infinity=False)
)
def test_payable_fee_nonnegative(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    assert result >= 0
