---
program: hold-line
function: reconcile
stamp: 34ba67bc
---

# Recover the evidence before judging the outcome

1. Use the operation ID from the last request. Read its durable receipt and output hashes
   before saying work is absent. A missing tool response does not establish task failure.
   A missing receipt or null vault does not establish that no remote task started.
2. A completed receipt with valid outputs and expected identity is a completion candidate.
   Reconcile the explicit stored thread/turn through zero-target-turn read/resume when the
   grant permits it; verify the result/marker and effective runtime. Return a semantic gap
   separately if the completed answer does not meet the task.
3. A pending receipt with the recorded runner PID/start identity still alive means pending;
   poll that owned tool/process only. A dead/unverifiable pending runner means unknown.
   Nonzero exit, damaged output or mismatched identity remains failed/unknown with evidence.
   None allows another ask, fresh thread, lock deletion, process kill or blind repair.
4. With no stored thread ID, retain the unknown outcome. The current shim can create an ID
   in memory and fail before saving it after the first turn. Do not attempt broad account
   history discovery or replace the thread to force progress. Return the exact evidence gap.
5. If the caretaker or target reports compaction/lost orientation, its old load receipt is
   evidence of a past load only. Read STATUS and the exact minimum files named for recovery;
   reload affected controller/function content only when necessary. Do not run the entire
   read order, git sweep, full GUIDE or all function bodies automatically. If the approved
   inputs do not restore the needed role/authority, ask the head for one focused recovery grant.
6. If target memory is uncertain, first reconcile protocol state without a model turn. A
   recovery question is a model turn and needs an explicit remaining grant; combine it with
   substantive work where justified. Do not send an unbudgeted “are you alive?” message.

Return a precise hold containing known IDs, operation/evidence pointers, what is proved,
what remains unknown, and the smallest decision required. Receipt recovery establishes no
remote exactly-once or power-loss guarantee. Normal tool escalation may be requested for the
same known operation when it has not started; it never authorizes replay after uncertain send.
