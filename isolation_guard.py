import logging
from config import settings

logger = logging.getLogger("saarthi.security.isolation")

class IsolationGuard:
    """
    Validates document and conversation isolated boundaries.
    Prevents cross-session document and message leakages.
    """
    
    def verify_document_isolation(self, metadata: dict, requested_session: str, requested_conv: str = None) -> bool:
        """
        Validates if document chunk metadata belongs to requested session + conversation.
        """
        doc_session = metadata.get("session_id")
        doc_conv = metadata.get("conversation_id")
        
        # If metadata is missing session markers, we trust the database lookup,
        # but if present, they MUST match the requested context
        if doc_session and doc_session != requested_session:
            logger.error(
                f"ISOLATION VIOLATION: Session {requested_session} attempted to retrieve "
                f"document chunk belonging to session {doc_session}!"
            )
            return False
            
        if requested_conv and doc_conv and doc_conv != requested_conv:
            logger.error(
                f"ISOLATION VIOLATION: Conversation {requested_conv} attempted to retrieve "
                f"document chunk belonging to conversation {doc_conv}!"
            )
            return False
            
        return True

    def verify_message_isolation(self, msg_session: str, requested_session: str) -> bool:
        """Checks message thread ownership."""
        if msg_session != requested_session:
            logger.error(
                f"ISOLATION VIOLATION: Requested session {requested_session} does not match "
                f"message owner session {msg_session}!"
            )
            return False
        return True

isolation_guard = IsolationGuard()
