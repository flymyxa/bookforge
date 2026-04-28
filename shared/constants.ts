export const PIPELINE_STAGES = [
  "discovery",
  "foundation",
  "summaries",
  "writing",
  "editing",
  "assembly",
] as const;

export type PipelineStageName = (typeof PIPELINE_STAGES)[number];

export const STAGE_COLORS: Record<PipelineStageName, string> = {
  discovery: "#3b82f6",
  foundation: "#14b8a6",
  summaries: "#f59e0b",
  writing: "#ef4444",
  editing: "#8b5cf6",
  assembly: "#22c55e",
};
