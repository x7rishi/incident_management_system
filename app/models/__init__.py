from app.models.base import Base
from app.models.user import User
from app.models.incident import Incident

# This ensures that whenever you import 'Base', 
# both 'User' and 'Incident' are already known to SQLAlchemy.
__all__ = ["Base", "User", "Incident"]