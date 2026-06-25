from app import db
from app.models.activity_log import ActivityLog


def log_activity(user, action, target_type=None, target_id=None, description=None):
    """Record an activity in the audit log."""
    log = ActivityLog(
        user_id=user.id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        description=description,
    )
    db.session.add(log)
    # Commit is responsibility of the caller (usually after main operation)
