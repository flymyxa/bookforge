from dataclasses import dataclass


@dataclass(slots=True)
class StageTransition:
    current_stage: str
    next_stage: str
    reason: str


class PipelineOrchestrator:
    """Minimal placeholder for the MVP state machine."""

    def advance(self, current_stage: str) -> StageTransition:
        order = ["discovery", "foundation", "summaries", "writing", "editing", "assembly"]
        index = order.index(current_stage)
        if index == len(order) - 1:
            return StageTransition(current_stage=current_stage, next_stage=current_stage, reason="pipeline_complete")
        return StageTransition(
            current_stage=current_stage,
            next_stage=order[index + 1],
            reason="linear_mvp_progression",
        )
