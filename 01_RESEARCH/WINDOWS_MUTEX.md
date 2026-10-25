# Named mutex execution control

`Local\WindowsLL.WINLL001.ResearchHarness` is opened without initial ownership. The immediate CreateMutexW result distinguishes an existing object. Keeping the handle alive prevents another harness command in the same session; destructor cleanup removes the last reference when appropriate. Constructor failure also closes its member handle through RAII.

This is an instance guard, not a lock around shared mutable data, so ReleaseMutex is not used without ownership. A deliberately precreated object can deny availability. It does not prevent instances in other sessions. The integration procedure starts a bounded `hold` command, waits for its readiness event, verifies duplicate rejection, ends it, then checks reacquisition.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
