from datetime import datetime
from sqlalchemy import String, Text, Boolean, DateTime, JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Provider(Base):
    __tablename__="providers"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(100),unique=True,index=True)
    capabilities:Mapped[list]=mapped_column(JSON,default=list)
    execution_modes:Mapped[list]=mapped_column(JSON,default=list)
    enabled:Mapped[bool]=mapped_column(Boolean,default=True)

class Target(Base):
    __tablename__="targets"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(150),unique=True,index=True)
    target_type:Mapped[str]=mapped_column(String(50))
    endpoint:Mapped[str]=mapped_column(String(500))
    capabilities:Mapped[list]=mapped_column(JSON,default=list)
    enabled:Mapped[bool]=mapped_column(Boolean,default=True)

class Scenario(Base):
    __tablename__="scenarios"
    id:Mapped[int]=mapped_column(primary_key=True)
    key:Mapped[str]=mapped_column(String(100),unique=True,index=True)
    name:Mapped[str]=mapped_column(String(200))
    category:Mapped[str]=mapped_column(String(100))
    severity:Mapped[str]=mapped_column(String(30))
    objective:Mapped[str]=mapped_column(Text)
    prompt_template:Mapped[str]=mapped_column(Text)
    supported_surfaces:Mapped[list]=mapped_column(JSON,default=list)
    enabled:Mapped[bool]=mapped_column(Boolean,default=True)

class Strategy(Base):
    __tablename__="strategies"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(100),unique=True)
    config:Mapped[dict]=mapped_column(JSON,default=dict)

class TestConfiguration(Base):
    __tablename__="test_configurations"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(200))
    target_id:Mapped[int]=mapped_column(ForeignKey("targets.id"))
    provider_ids:Mapped[list]=mapped_column(JSON,default=list)
    scenario_ids:Mapped[list]=mapped_column(JSON,default=list)
    strategy_id:Mapped[int]=mapped_column(ForeignKey("strategies.id"))
    attempts:Mapped[int]=mapped_column(Integer,default=1)

class Campaign(Base):
    __tablename__="campaigns"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(200))
    config_id:Mapped[int]=mapped_column(ForeignKey("test_configurations.id"))
    status:Mapped[str]=mapped_column(String(30),default="DRAFT")
    total_tests:Mapped[int]=mapped_column(Integer,default=0)
    completed_tests:Mapped[int]=mapped_column(Integer,default=0)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

class TestRun(Base):
    __tablename__="test_runs"
    id:Mapped[int]=mapped_column(primary_key=True)
    campaign_id:Mapped[int]=mapped_column(ForeignKey("campaigns.id"))
    provider:Mapped[str]=mapped_column(String(100))
    scenario:Mapped[str]=mapped_column(String(100))
    attempt:Mapped[int]=mapped_column(Integer,default=1)
    status:Mapped[str]=mapped_column(String(30),default="QUEUED")
    success:Mapped[bool|None]=mapped_column(Boolean,nullable=True)
    severity:Mapped[str|None]=mapped_column(String(30),nullable=True)
    request:Mapped[str|None]=mapped_column(Text,nullable=True)
    response:Mapped[str|None]=mapped_column(Text,nullable=True)
    evidence:Mapped[dict]=mapped_column(JSON,default=dict)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)


class Finding(Base):
    __tablename__="findings"
    id:Mapped[int]=mapped_column(primary_key=True)
    test_run_id:Mapped[int]=mapped_column(ForeignKey("test_runs.id"), unique=True)
    campaign_id:Mapped[int]=mapped_column(ForeignKey("campaigns.id"), index=True)
    title:Mapped[str]=mapped_column(String(250))
    fingerprint:Mapped[str]=mapped_column(String(128), index=True)
    severity:Mapped[str]=mapped_column(String(30))
    risk_score:Mapped[float]=mapped_column(default=0)
    confidence:Mapped[float]=mapped_column(default=0)
    category:Mapped[str]=mapped_column(String(100))
    mitre_atlas:Mapped[list]=mapped_column(JSON,default=list)
    owasp_llm:Mapped[list]=mapped_column(JSON,default=list)
    impact:Mapped[str]=mapped_column(Text)
    recommendation:Mapped[str]=mapped_column(Text)
    evidence:Mapped[dict]=mapped_column(JSON,default=dict)
    status:Mapped[str]=mapped_column(String(30),default="OPEN")
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)


class Remediation(Base):
    __tablename__="remediations"
    id:Mapped[int]=mapped_column(primary_key=True)
    finding_id:Mapped[int]=mapped_column(ForeignKey("findings.id"), unique=True)
    owner:Mapped[str|None]=mapped_column(String(150),nullable=True)
    due_date:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
    status:Mapped[str]=mapped_column(String(30),default="OPEN")
    notes:Mapped[str|None]=mapped_column(Text,nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
