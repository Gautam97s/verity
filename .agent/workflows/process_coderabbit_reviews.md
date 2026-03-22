---
description: Fetch CodeRabbit review comments, apply fixes, and update the PR.
---

1. **Fetch PR Details**:
   - Run `gh pr view --json url,number,reviews,comments` to get the latest reviews.
   - If `gh` is not available, ask the user for the PR URL or the specific feedback.

2. **Analyze Reviews**:
   - Look for comments from "coderabbitai" (or similar bot name).
   - Identify the file path, line number, and the suggested change.

3. **Apply Fixes**:
   - For each actionable comment:
     - Read the target file.
     - Apply the suggested code change or refactoring.
     - Mark the comment as "addressed" (internally).

4. **Verify Changes**:
   - Run `npm run build` (frontend) or `pytest` (backend) to ensure no regressions.

5. **Update PR**:
   - Run `git add .`
   - Run `git commit -m "refactor: apply CodeRabbit review fixes"`
   - Run `git push`
