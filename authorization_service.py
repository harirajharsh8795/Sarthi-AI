import logging

logger = logging.getLogger("saarthi.security.auth")

class AuthorizationService:
    """
    Role-Based Access Control (RBAC) authorization service.
    Scaffolds Guest, User, Admin, and Auditor roles.
    """
    
    def __init__(self):
        # Define roles and allowed actions
        self.role_permissions = {
            "Guest": {"read_conversations"},
            "User": {"read_conversations", "write_conversations", "upload_documents", "stream_inference"},
            "Auditor": {"read_conversations", "read_telemetry", "read_audit"},
            "Admin": {
                "read_conversations", "write_conversations", "upload_documents", 
                "stream_inference", "read_telemetry", "read_audit", "delete_database", "configure_secrets"
            }
        }

    def check_permission(self, role: str, action: str) -> bool:
        """Checks if a role has the required permission action."""
        if role not in self.role_permissions:
            role = "Guest"
            
        allowed = action in self.role_permissions[role]
        if not allowed:
            logger.warning(f"Access Denied: Role '{role}' lacks permission for '{action}'")
        return allowed

    def get_role_for_session(self, session_id: str) -> str:
        """Determines role based on session identifiers. Scaffolds Guest/User default role."""
        if not session_id:
            return "Guest"
        if session_id.startswith("admin_"):
            return "Admin"
        if session_id.startswith("auditor_"):
            return "Auditor"
        return "User"

authorization_service = AuthorizationService()
