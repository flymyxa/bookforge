import type { PipelineStageName } from "./constants";

export type StageStatus = "idle" | "running" | "blocked" | "complete" | "failed";

export interface StageSummary {
  id: string;
  name: PipelineStageName;
  status: StageStatus;
  progress: number;
  updatedAt: string;
}

export interface BookSummary {
  id: string;
  title: string;
  genre: string;
  status: string;
  updatedAt: string;
}
