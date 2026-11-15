district = "jaipur"
_district = district

state = "rajasthan"
_state = state

d_type = "Earthquake"
_d_type = d_type

date = "2026"
_date = "2027"

d1 = {"disaster": d_type, "date": date, "state": state, "district": district}

d2 = {"disaster": _d_type, "state": _state, "date": _date, "district": _district}


if d1 == d2:
    print("YES")
else:
    print("NO")
