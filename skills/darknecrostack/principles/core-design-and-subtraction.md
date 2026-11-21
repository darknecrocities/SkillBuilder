# Core Principles: Design & Subtraction

Read these principles before refactoring, sizing a diff, designing data structures, or breaking out of failed debug loops.

---

## 1. Laziness Protocol
- **When it applies**: Refactoring, sizing a diff, or tempted to add abstractions, helper layers, feature flags, or signal threading.
- **Rule**: Bias to deletion and the smallest diff that solves the problem. Every extra file, wrapper, or configuration knob carries permanent cognitive and maintenance debt.
- **Litmus Test**: Can this be solved by deleting dead branches or reusing an existing repository helper instead of adding a new class?

## 2. Foundational Thinking
- **When it applies**: Before writing implementation logic on any non-trivial feature or subsystem.
- **Rule**: Lock three things first: (1) core types and data structures, (2) scaffold-vs-feature sequencing, and (3) what concurrent actors or async flows share.
- **Litmus Test**: If you cannot sketch the core state transitions and data types in 20 lines, you do not understand the problem well enough to write bodies yet.

## 3. Redesign from First Principles
- **When it applies**: Integrating a new requirement that bends or breaks an existing design.
- **Rule**: Do not bolt conditional patches onto an outdated abstraction. Ask: *"If this requirement existed on day one, what clean structure would cover both old and new cases uniformly?"*
- **Litmus Test**: Prefer one clean parameterized table or state model over three `if (specialCase)` patches.

## 4. Attack the Premise
- **When it applies**: Two or more fixes sharing the same assumption have failed the same test, build, or visual gate.
- **Rule**: Halt patching immediately. Write down the shared premise you have been assuming (e.g., *"the auth header reaches the handler"*, *"the scroll container is `window`"*, *"the `.riv` state machine is named `State Machine 1`"*), and run a 10-line diagnostic probe to falsify or confirm that premise directly.
- **Litmus Test**: Never write a third fix on an unverified premise.

## 5. Subtract Before You Add
- **When it applies**: Planning an addition, refactor, or rewrite on crowded code.
- **Rule**: Remove dead code, obsolete flags, duplicate utilities, and unused parameters *first* (in a clean verifiable step), then build the new capability on the simpler base.
- **Litmus Test**: Adding features onto uncleaned sprawl multiplies edge cases quadratically.

## 6. Minimize Reader Load
- **When it applies**: Reviewing or shaping code that feels hard to trace.
- **Rule**: Count indirection layers, hidden mutable state, and side effects. Collapse one-caller wrappers, shrink variable scope, flatten nesting to `<= 3` levels via early returns, and keep functions `<= 40` lines.
- **Litmus Test**: A senior engineer reading the file top-to-bottom should understand control flow without jumping across five trivial pass-through files.
