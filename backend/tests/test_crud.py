import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.models import User, Incident, Action, Report, Log, KnowledgeBase


@pytest.mark.anyio
async def test_user_crud(db_session: AsyncSession):
    # 1. Create
    new_user = User(
        username="crud_user",
        hashed_password="hashed_crud_password",
        roles=["operator"]
    )
    db_session.add(new_user)
    await db_session.flush()
    user_id = new_user.id
    assert user_id is not None
    
    # 2. Read
    result = await db_session.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    assert user is not None
    assert user.username == "crud_user"
    assert "operator" in user.roles
    
    # 3. Update
    user.roles = ["operator", "admin"]
    db_session.add(user)
    await db_session.flush()
    
    result = await db_session.execute(select(User).filter_by(id=user_id))
    updated_user = result.scalar_one()
    assert "admin" in updated_user.roles
    
    # 4. Delete
    await db_session.delete(updated_user)
    await db_session.flush()
    
    result = await db_session.execute(select(User).filter_by(id=user_id))
    assert result.scalar_one_or_none() is None


@pytest.mark.anyio
async def test_incident_crud(db_session: AsyncSession):
    # 1. Create
    incident_id = "INC-TEST-99"
    new_incident = Incident(
        id=incident_id,
        title="Test Database Issue",
        description="SQL connection latency exceeded threshold",
        service="laboratory",
        severity="medium",
        status="triage"
    )
    db_session.add(new_incident)
    await db_session.flush()
    
    # 2. Read
    result = await db_session.execute(select(Incident).filter_by(id=incident_id))
    incident = result.scalar_one_or_none()
    assert incident is not None
    assert incident.title == "Test Database Issue"
    assert incident.status == "triage"
    
    # 3. Update
    incident.status = "active"
    db_session.add(incident)
    await db_session.flush()
    
    result = await db_session.execute(select(Incident).filter_by(id=incident_id))
    updated_incident = result.scalar_one()
    assert updated_incident.status == "active"
    
    # 4. Delete
    await db_session.delete(updated_incident)
    await db_session.flush()
    
    result = await db_session.execute(select(Incident).filter_by(id=incident_id))
    assert result.scalar_one_or_none() is None


@pytest.mark.anyio
async def test_action_crud(db_session: AsyncSession):
    # Setup dependent incident
    incident = Incident(
        id="INC-ACT-01",
        title="Action Test Incident",
        description="Testing action mapping",
        service="billing",
        severity="low",
        status="active"
    )
    db_session.add(incident)
    await db_session.flush()

    # 1. Create
    new_action = Action(
        incident_id="INC-ACT-01",
        action_type="service_restart",
        command="systemctl restart billing",
        status="running"
    )
    db_session.add(new_action)
    await db_session.flush()
    action_id = new_action.id
    assert action_id is not None
    
    # 2. Read
    result = await db_session.execute(select(Action).filter_by(id=action_id))
    action = result.scalar_one_or_none()
    assert action is not None
    assert action.command == "systemctl restart billing"
    
    # 3. Update
    action.status = "success"
    action.log_output = "Restart complete, process running with PID 891"
    db_session.add(action)
    await db_session.flush()
    
    result = await db_session.execute(select(Action).filter_by(id=action_id))
    updated_action = result.scalar_one()
    assert updated_action.status == "success"
    assert "PID 891" in updated_action.log_output
    
    # 4. Delete
    await db_session.delete(updated_action)
    await db_session.flush()
    await db_session.delete(incident)
    await db_session.flush()
    
    result = await db_session.execute(select(Action).filter_by(id=action_id))
    assert result.scalar_one_or_none() is None


@pytest.mark.anyio
async def test_report_crud(db_session: AsyncSession):
    # Setup dependent incident
    incident = Incident(
        id="INC-REP-01",
        title="Report Test Incident",
        description="Testing report mapping",
        service="pharmacy",
        severity="low",
        status="active"
    )
    db_session.add(incident)
    await db_session.flush()

    # 1. Create
    new_report = Report(
        incident_id="INC-REP-01",
        title="Postmortem - Pharmacy latency",
        content="Incident description and actions summary details.",
        status="draft"
    )
    db_session.add(new_report)
    await db_session.flush()
    report_id = new_report.id
    
    # 2. Read
    result = await db_session.execute(select(Report).filter_by(id=report_id))
    report = result.scalar_one_or_none()
    assert report is not None
    assert report.title == "Postmortem - Pharmacy latency"
    
    # 3. Update
    report.status = "finalized"
    db_session.add(report)
    await db_session.flush()
    
    result = await db_session.execute(select(Report).filter_by(id=report_id))
    updated_report = result.scalar_one()
    assert updated_report.status == "finalized"
    
    # 4. Delete
    await db_session.delete(updated_report)
    await db_session.flush()
    await db_session.delete(incident)
    await db_session.flush()
    
    result = await db_session.execute(select(Report).filter_by(id=report_id))
    assert result.scalar_one_or_none() is None


@pytest.mark.anyio
async def test_log_crud(db_session: AsyncSession):
    # 1. Create
    new_log = Log(
        timestamp=datetime.now(timezone.utc),
        log_level="ERROR",
        service="patient_portal",
        message="Simulated DB error occurred during lookup",
        extra={"error_code": "PG-500"}
    )
    db_session.add(new_log)
    await db_session.flush()
    log_id = new_log.id
    
    # 2. Read
    result = await db_session.execute(select(Log).filter_by(id=log_id))
    log = result.scalar_one_or_none()
    assert log is not None
    assert log.log_level == "ERROR"
    assert log.extra["error_code"] == "PG-500"
    
    # 3. Update
    log.message = "Updated log error message"
    db_session.add(log)
    await db_session.flush()
    
    result = await db_session.execute(select(Log).filter_by(id=log_id))
    updated_log = result.scalar_one()
    assert updated_log.message == "Updated log error message"
    
    # 4. Delete
    await db_session.delete(updated_log)
    await db_session.flush()
    
    result = await db_session.execute(select(Log).filter_by(id=log_id))
    assert result.scalar_one_or_none() is None


@pytest.mark.anyio
async def test_knowledge_base_crud(db_session: AsyncSession):
    # 1. Create
    new_kb = KnowledgeBase(
        title="Restoring billing replicas",
        content="Follow troubleshooting playbook page 24.",
        tags=["postgres", "billing", "failover"]
    )
    db_session.add(new_kb)
    await db_session.flush()
    kb_id = new_kb.id
    
    # 2. Read
    result = await db_session.execute(select(KnowledgeBase).filter_by(id=kb_id))
    kb = result.scalar_one_or_none()
    assert kb is not None
    assert kb.title == "Restoring billing replicas"
    assert "postgres" in kb.tags
    
    # 3. Update
    kb.title = "Restoring billing replicas v2"
    db_session.add(kb)
    await db_session.flush()
    
    result = await db_session.execute(select(KnowledgeBase).filter_by(id=kb_id))
    updated_kb = result.scalar_one()
    assert updated_kb.title == "Restoring billing replicas v2"
    
    # 4. Delete
    await db_session.delete(updated_kb)
    await db_session.flush()
    
    result = await db_session.execute(select(KnowledgeBase).filter_by(id=kb_id))
    assert result.scalar_one_or_none() is None
