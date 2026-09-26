from app.postprocess import normalize_plate, normalize_sign

def test_us_plate_strips_state():
    assert normalize_plate("California 8ABC123") == "8ABC123"

def test_chinese_plate_keeps_province():
    assert normalize_plate("粤 B12345") == "粤B12345"

def test_sign_multiline_order():
    assert normalize_sign("ROAD\nWORK\nAHEAD") == "ROAD WORK AHEAD"

def test_advisory_plaque_drops_units():
    assert normalize_sign("35 MPH") == "35"
