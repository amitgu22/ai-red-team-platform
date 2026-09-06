from pydantic import BaseModel
from typing import Optional

class ScenarioRead(BaseModel):
    id:int; key:str; name:str; category:str; severity:str; objective:str; prompt_template:str; supported_surfaces:list
    class Config: from_attributes=True

class StrategyRead(BaseModel):
    id:int; name:str; config:dict
    class Config: from_attributes=True

class TestConfigCreate(BaseModel):
    name:str
    target_id:int
    provider_ids:list[int]
    scenario_ids:list[int]
    strategy_id:int
    attempts:int=1

class TestConfigRead(TestConfigCreate):
    id:int
    class Config: from_attributes=True

class CampaignCreate(BaseModel):
    name:str
    config_id:int

class CampaignRead(BaseModel):
    id:int; name:str; config_id:int; status:str; total_tests:int; completed_tests:int
    class Config: from_attributes=True

class TestRunRead(BaseModel):
    id:int; campaign_id:int; provider:str; scenario:str; attempt:int; status:str; success:Optional[bool]; severity:Optional[str]; request:Optional[str]; response:Optional[str]; evidence:dict
    class Config: from_attributes=True
