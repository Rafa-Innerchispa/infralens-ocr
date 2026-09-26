from pathlib import Path
from app.asset_passport import build_asset_passport

def test_asset_passport_extracts_fields(tmp_path: Path):
    p = tmp_path / "x.jpg"
    p.write_bytes(b"fake-image")
    out = build_asset_passport(
        p,
        "MODEL: DS-7608NI-K2 S/N: ABC12345 MAC AA:BB:CC:DD:EE:FF 12VDC",
        0.9
    )
    assert out["fields"]["model"] == "DS-7608NI-K2"
    assert out["fields"]["serial"] == "ABC12345"
    assert out["fields"]["mac"] == "AA:BB:CC:DD:EE:FF"
    assert len(out["image_sha256"]) == 64
