import { StageNode } from "./StageNode";

import type { StageStatus } from "@shared/types";

export function StageFlow({
  stages,
}: {
  stages: Array<{ name: string; status: StageStatus; progress: number }>;
}) {
  return (
    <div className="overflow-x-auto rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex min-w-max items-center gap-4">
        {stages.map((stage) => (
          <div key={stage.name} className="space-y-2">
            <StageNode name={stage.name} status={stage.status === "blocked" || stage.status === "failed" ? "idle" : stage.status} />
            <p className="text-center text-xs uppercase tracking-[0.2em] text-slate-500">
              {stage.progress}%
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
