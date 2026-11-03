# Recovery contract
Revision: current

Before any retry of P9, the recovery contract requires checking its durable receipt, the current target and the current permit. A missing report alone is not permission to repeat an operation. Inspection and proposals for reconciliation are available without treating them as a retry. The contract does not specify the desired final digest, so an authorized decision about desired state remains necessary.
