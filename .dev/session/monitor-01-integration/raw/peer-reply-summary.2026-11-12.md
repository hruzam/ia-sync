# Received peer evidence — 2026-11-12

Pulled ia-sync 01062e9 and reposoma a671ec1. The two received integration reply
cards are preserved verbatim in monitor's host-local archive under their original
trajectory.home/office.monitor-integration-reply.2026-11-12.md basenames; their
original contents remain recoverable from ia-sync commit 01062e9. This summary
is attributed reported evidence, not an independent replay of remote commands.

- Home reports home → monitor exit 0 using strict checking with the committed
  monitor known_hosts file. Office evidence reports office → monitor exit 0 with
  the same explicit trust file, plus both home/office directions working today.
- Neither peer has accepted monitor's client key. Home's Claude permission gate
  refused persistence to its SSH auth files; office left acceptance to Majkee.
  Do not bypass that refusal through another carrier. Default known_hosts on both
  peers still lacks monitor; explicit trust-file receipts do not establish plain
  SSH readiness. Monitor's own two outbound failures remain the latest local tests.
- The office reply was authored by the home Claude session running commands over
  SSH on office. It is not proof of an independent office Claude agent or native
  cross-host session messaging. Both replies confirm Git mail consumption.
- Both peers confirm standalone ~/nabla-lab and a real GitHub vacuole remote.
  Selected project path candidates agree where present. Pajdulium pair exists on
  office and is absent on home. Do not mirror that absence onto monitor.
- Nablarva and nabla-lab HEADs differ between hosts; their reported 0/0 tracking
  status was measured without a fetch. Do not infer freshness or copy dirty/untracked
  work. Qualify the selected remote refs before the bounded clone package.
- A cross-host-session-bus backlog proposal arrived in .dev/_backlog/. It is a
  proposal to assess separately, not authorization to build a messaging daemon.
