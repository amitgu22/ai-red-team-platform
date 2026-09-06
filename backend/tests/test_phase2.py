from app.schemas import TestConfigCreate

def test_test_config_schema():
    x = TestConfigCreate(name="demo", target_id=1, provider_ids=[1,2], scenario_ids=[1], strategy_id=1, attempts=3)
    assert x.attempts == 3
    assert len(x.provider_ids) == 2
