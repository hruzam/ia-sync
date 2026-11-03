# Build pipeline
Revision: current

The build pipeline runs a smoke test before artifacts are packaged. Packaging uses the release branch and records the build identifier in its output. The pipeline owner reviews flaky checks separately; its result concerns whether a binary can be packaged. It does not establish whether a planning proposal has the inputs required by its own contract. The next scheduled packaging window is Tuesday.
