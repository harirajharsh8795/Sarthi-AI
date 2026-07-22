# DATABASE AUDIT

## Schema Issues (`saarthi.db` SQLite)
1. **Missing Foreign Keys Constraints:** 
   - *Severity:* HIGH. The `messages` table references `conversation_id`, but `PRAGMA foreign_keys = ON` is not explicitly enforced on connection, meaning orphaned messages can exist.
2. **JSON Blob Storage:**
   - *Severity:* MEDIUM. Citations are stored as stringified JSON inside the `messages` table. This prevents efficient querying of "which messages cited Document X".
3. **No Cascade Deletes:**
   - Deleting a conversation via the API manually deletes the messages in Python logic rather than relying on `ON DELETE CASCADE` at the DB level, opening the door for race conditions.
4. **WAL Mode Missing:**
   - *Severity:* CRITICAL. Write-Ahead Logging (WAL) is not explicitly enabled. Concurrent reads during a long write (like batch history updates) will lock the database and throw `database is locked` errors.
