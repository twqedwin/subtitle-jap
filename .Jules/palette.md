## 2025-05-20 - Inline Actions vs Blocking Dialogs

**Learning:** Blocking dialogs (like `messagebox.showinfo`) break the user's flow, especially for success states where no critical decision is needed. They force an extra click ("OK") and freeze the UI.

**Action:** Prefer inline UI updates or revealing action buttons (e.g., "Open File Location") that allow the user to proceed at their own pace without interruption. This is particularly effective for long-running processes where the user might have switched context; when they return, they see the result and next step immediately without a modal blocking their view.
