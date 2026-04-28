export function StageDetail({
  currentStage,
  bookId,
  advanceAction,
}: {
  currentStage: { name: string; status: string; progress: number } | null;
  bookId: string;
  advanceAction: (formData: FormData) => void | Promise<void>;
}) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Current Stage</p>
      <h2 className="mt-2 text-2xl font-semibold capitalize">
        {currentStage?.name ?? "No active stage"}
      </h2>
      <p className="mt-3 max-w-2xl text-slate-700">
        {currentStage
          ? `Status: ${currentStage.status}. Progress: ${currentStage.progress}%. This panel will grow into stage metadata, generated files, token usage, and human gate controls.`
          : "No stage data is available yet."}
      </p>
      <form action={advanceAction} className="mt-5">
        <input type="hidden" name="bookId" value={bookId} />
        <button
          className="rounded-full bg-ink px-4 py-2 text-sm text-paper transition hover:opacity-90"
          type="submit"
        >
          Advance Pipeline
        </button>
      </form>
    </section>
  );
}
