# Alpha Research Harness

A personal framework for backtesting many candidate trading ideas ("alphas") through one standardized pipeline, so they can be compared honestly and the best one distilled into the capstone submission. The harness is the factory; the submission is one product of it.

## Language

**Alpha**:
A single candidate trading idea — a rule that turns market data into target positions. Time-series momentum is the first Alpha; others may be added later.
_Avoid_: Algo, strategy block, recipe

**Harness**:
The whole research framework — data layer, backtest engine, analyser, and run log — through which every Alpha runs unchanged.
_Avoid_: Platform, system, tool

**Run**:
One execution of one Alpha over one universe, period, and parameter set. Every Run is recorded in the Run Log, including failures.

**Run Log**:
The persistent record of all Runs and their metrics. Exists to answer the brief's overfitting question: "how many variations did you try?"
_Avoid_: Results Pool

**Submission Strategy**:
The single Alpha selected from the Run Log for the capstone report and notebook. Chosen for defensibility, not just backtest performance.

**Price Store**:
The single DuckDB file holding all price history and universe metadata. Every Alpha reads from it; nothing else may fetch market data directly.
_Avoid_: Stocks Database, per-asset-class databases

**Snapshot**:
An immutable, hash-recorded copy of the Price Store frozen at submission time, satisfying the brief's downloaded-data requirement. Runs used in the report must be reproducible from the Snapshot alone.

**Alpha Contract**:
The rule that every Alpha consumes the price panel and produces a date-by-ticker frame of target portfolio weights. Execution timing, costs, and metrics belong to the Backtest Engine, never to an Alpha.

**Overlay**:
A composable transform applied to an Alpha's target weights (e.g. volatility targeting, exposure caps) before execution. Paper-driven improvements become Overlays, not engine changes.
_Avoid_: Improvisation, tweak

**Holdout**:
The 2019-2026 period, untouchable during Alpha design. May be evaluated at most once per finalized Alpha; every Run is engine-tagged IN_SAMPLE or HOLDOUT so the discipline is auditable from the Run Log.
_Avoid_: Test set (ambiguous), validation period

**Interpretation**:
The LLM-written qualitative assessment of a Run's computed metrics, stored in the Run Log beside the numbers with the prompt and model version that produced it. An Interpretation never replaces, modifies, or gates a metric.
_Avoid_: Analysis report

**Complete Analysis**:
A Run's full record: parameters, deterministic metrics and plots, tag (IN_SAMPLE/HOLDOUT), and its Interpretation.
