import { ChapterPreview } from "@/components/pipeline/ChapterPreview";
import { AgentFeed } from "@/components/pipeline/AgentFeed";
import { StageDetail } from "@/components/pipeline/StageDetail";
import { StageFlow } from "@/components/pipeline/StageFlow";
import { apiGetSafe } from "@/lib/api";
import { advancePipelineAction } from "./actions";

type PipelineStageResponse = Array<{
  id: string;
  book_id: string;
  stage: string;
  status: "idle" | "running" | "blocked" | "complete" | "failed";
  progress: number;
}>;

type ActivityResponse = {
  activity: string[];
};

type ChapterFileResponse = {
  chapter_id: string;
  title: string;
  content: string;
};

export const dynamic = "force-dynamic";

export default async function PipelinePage({
  params,
}: {
  params: { id: string };
}) {
  const fallbackStages: PipelineStageResponse = [
    { id: `${params.id}-1`, book_id: params.id, stage: "discovery", status: "complete", progress: 100 },
    { id: `${params.id}-2`, book_id: params.id, stage: "foundation", status: "running", progress: 40 },
    { id: `${params.id}-3`, book_id: params.id, stage: "writing", status: "idle", progress: 0 },
  ];
  const fallbackActivity: ActivityResponse = {
    activity: [
      "Kate generated Creative Vision",
      "Ruth seeded canon ledger",
      "Foundation builder is drafting the world bible",
    ],
  };

  const [stages, activity, chapterOne] = await Promise.all([
    apiGetSafe<PipelineStageResponse>(`/v1/pipeline/${params.id}`, fallbackStages),
    apiGetSafe<ActivityResponse>(`/v1/pipeline/${params.id}/activity`, fallbackActivity),
    apiGetSafe<ChapterFileResponse | null>(`/v1/files/${params.id}/chapters/1`, null),
  ]);
  const currentStage =
    stages.find((stage) => stage.status === "running" || stage.status === "blocked") ??
    stages.find((stage) => stage.status !== "complete") ??
    stages[stages.length - 1] ??
    null;

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold">Pipeline</h1>
        <p className="text-slate-600">Stage progress and agent activity are loaded from the API.</p>
      </div>
      <StageFlow
        stages={stages.map((stage) => ({
          name: stage.stage,
          status: stage.status,
          progress: stage.progress,
        }))}
      />
      <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
        <StageDetail
          bookId={params.id}
          advanceAction={advancePipelineAction}
          currentStage={
            currentStage
              ? {
                  name: currentStage.stage,
                  status: currentStage.status,
                  progress: currentStage.progress,
                }
              : null
          }
        />
        <AgentFeed feed={activity.activity} />
      </div>
      <ChapterPreview
        chapter={chapterOne}
        emptyMessage="Writing has not generated Chapter 1 yet. Once it does, this page will show the persisted chapter content for the browser demo."
      />
    </section>
  );
}
