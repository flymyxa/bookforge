type ChapterPreviewData = {
  title: string;
  content: string;
};

function renderParagraphs(content: string) {
  const blocks = content
    .split("\n\n")
    .map((block) => block.trim())
    .filter(Boolean);

  return blocks.map((block, index) => {
    if (block.startsWith("# ")) {
      return (
        <h3 key={`${index}-${block}`} className="text-2xl font-semibold text-slate-900">
          {block.slice(2)}
        </h3>
      );
    }

    if (block.startsWith("## ")) {
      return (
        <h4
          key={`${index}-${block}`}
          className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500"
        >
          {block.slice(3)}
        </h4>
      );
    }

    const lines = block.split("\n").map((line) => line.trim()).filter(Boolean);
    const bulletLines = lines.filter((line) => line.startsWith("- "));

    if (bulletLines.length === lines.length) {
      return (
        <ul key={`${index}-${block}`} className="space-y-2 text-slate-700">
          {bulletLines.map((line) => (
            <li key={line} className="flex gap-3">
              <span aria-hidden="true" className="mt-1 text-signal">
                *
              </span>
              <span>{line.slice(2)}</span>
            </li>
          ))}
        </ul>
      );
    }

    return (
      <p key={`${index}-${block}`} className="text-[15px] leading-7 text-slate-700">
        {lines.join(" ")}
      </p>
    );
  });
}

export function ChapterPreview({
  chapter,
  emptyMessage = "Run the writing step to generate a readable Chapter 1 draft here.",
}: {
  chapter: ChapterPreviewData | null;
  emptyMessage?: string;
}) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Chapter Preview</p>
          <h2 className="mt-2 text-2xl font-semibold">
            {chapter?.title ?? "Chapter 1 not generated yet"}
          </h2>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-slate-600">
          Persisted Artifact
        </span>
      </div>

      {chapter ? (
        <div className="mt-6 space-y-5 rounded-[2rem] bg-stone-50 p-6">
          {renderParagraphs(chapter.content)}
        </div>
      ) : (
        <p className="mt-4 max-w-2xl text-slate-600">{emptyMessage}</p>
      )}
    </section>
  );
}
