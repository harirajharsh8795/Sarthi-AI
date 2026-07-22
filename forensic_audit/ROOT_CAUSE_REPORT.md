# ROOT CAUSE REPORT (Historical & Current)

## 1. History Rendering Regression (Resolved)
- **Root Cause:** `validation_service.py` split text by `
+` and re-joined with spaces, destroying markdown.
- **Severity:** CRITICAL
- **Suggested Fix:** (Already implemented in Sprint 7) - preserve original text and only append tags.

## 2. Input Box Frozen During Upload (Resolved)
- **Root Cause:** `uploadingFile` boolean was indiscriminately applied to the `textarea`'s disabled prop.
- **Severity:** HIGH
- **Suggested Fix:** (Already implemented in Sprint 7) - decouple upload state from input.

## 3. Streaming Bleed Across Chats
- **Root Cause:** React closures capture outdated `conversationId` during rapid switching, but `eventSource` continues appending to global state.
- **Severity:** HIGH
- **Suggested Fix:** Use a Ref to track `activeConvId` and immediately discard incoming SSE packets if they do not match the currently active Ref.
