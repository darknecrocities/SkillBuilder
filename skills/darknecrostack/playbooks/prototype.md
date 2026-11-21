# Playbook: Prototype

Use when a design fork or technical unknown can be settled in minutes by running real code instead of guessing or asking.

## Steps
1. **Frame the Fork**: State the 2–3 competing options and the exact question the prototype must answer.
2. **Build Throwaway Probe in `scratch/`**: Author a minimal 20–50 line script or isolated sandbox component (`Never Block on the Human`).
3. **Run & Measure**: Execute against real inputs/runtimes (check native bindings, bundle KB, API response shape, `.riv` state trigger, or CSS layout).
4. **Decide & Clean Up**: Record the measured verdict, delete throwaway probe artifacts if outside project scope, and implement the winning choice cleanly.
