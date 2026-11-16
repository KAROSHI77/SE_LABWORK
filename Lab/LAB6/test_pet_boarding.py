
from hypothesis import given, strategies as st
from pet_boarding import parse_booking, stay_average, payable_fee


# Test 1: parse_booking should reject malformed input safely
@given(st.one_of(st.text(), st.none()))
def test_parse_booking_no_crash(s):
    try:
        result = parse_booking(s)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], float)
    except (TypeError, ValueError):
        # Rejection of invalid input is acceptable
        pass


# Test 2: stay_average should reject invalid or empty input safely
@given(st.one_of(st.text(), st.none()))
def test_stay_average_no_crash(s):
    try:
        result = stay_average(s)
        assert isinstance(result, int)
    except (TypeError, ValueError, ZeroDivisionError):
        # Rejection of invalid input is acceptable
        pass


# Test 3: payable_fee should reject invalid input safely
@given(st.one_of(st.text(), st.none()))
def test_payable_fee_no_crash(s):
    try:
        result = payable_fee(s)
        assert isinstance(result, (int, float))
    except (TypeError, ValueError):
        # Rejection of invalid input is acceptable
        pass


# Test 4: valid booking inputs should produce correct results
@given(st.text(min_size=1).filter(lambda s: ":" not in s),
       st.floats(allow_nan=False, allow_infinity=False))
def test_parse_booking_valid(pet, days):
    result = parse_booking(f"{pet}:{days}")
    assert result[0] == pet.strip().title()
    assert result[1] == days


# Test 5: stay_average should calculate the true arithmetic mean
@given(st.lists(st.integers(), min_size=1, max_size=20))
def test_stay_average_mean(values):
    csv = ",".join(map(str, values))
    result = stay_average(csv)
    assert result == sum(values) / len(values)


# Test 6: payable fee must never be negative
@given(st.floats(min_value=0, max_value=1_000_000,
                 allow_nan=False, allow_infinity=False),
       st.floats(min_value=0, max_value=1_000_000,
                 allow_nan=False, allow_infinity=False))
def test_payable_fee_nonnegative(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    assert result >= 0
