type FoundationDocument = {
  id: string;
  name: string;
  status: string;
  content: string | null;
};

function renderDocumentContent(content: string | null) {
  if (!content) {
    return <p className="text-sm text-slate-500">No content generated yet.</p>;
  }

  const blocks = content
    .split("\n\n")
    .map((block) => block.trim())
    .filter(Boolean)
    .slice(0, 6);

  return blocks.map((block, index) => {
    if (block.startsWith("# ")) {
      return (
        <h3 key={`${index}-${block}`} className="text-xl font-semibold text-slate-900">
          {block.slice(2)}
        </h3>
      );
    }

    if (block.startsWith("## ")) {
      return (
        <h4
          key={`${index}-${block}`}
          className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500"
        >
          {block.slice(3)}
        </h4>
      );
    }

    const lines = block.split("\n").map((line) => line.trim()).filter(Boolean);
    const bulletLines = lines.filter((line) => line.startsWith("- "));

    if (bulletLines.length === lines.length) {
      return (
        <ul key={`${index}-${block}`} className="space-y-2 text-sm text-slate-700">
          {bulletLines.map((line) => (
            <li key={line} className="flex gap-2">
              <span aria-hidden="true" className="text-signal">
                *
              </span>
              <span>{line.slice(2)}</span>
            </li>
          ))}
        </ul>
      );
    }

    return (
      <p key={`${index}-${block}`} className="text-sm leading-6 text-slate-700">
        {lines.join(" ")}
      </p>
    );
  });
}

export function FoundationPreview({
  documents,
}: {
  documents: FoundationDocument[];
}) {
  return (
    <section className="space-y-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div>
        <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Foundation Pack</p>
        <h2 className="mt-2 text-2xl font-semibold">Discovery And Foundation Artifacts</h2>
        <p className="mt-2 max-w-3xl text-sm text-slate-600">
          These previews are loaded from the persisted document records so the browser demo shows
          the output of discovery and foundation work, not just stage state.
        </p>
      </div>
      <div className="grid gap-4 xl:grid-cols-3">
        {documents.map((document) => (
          <article key={document.id} className="rounded-[1.75rem] bg-stone-50 p-5">
            <div className="flex items-start justify-between gap-3">
              <h3 className="text-lg font-semibold text-slate-900">{document.name}</h3>
              <span className="rounded-full bg-white px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                {document.status}
              </span>
            </div>
            <div className="mt-4 space-y-4">{renderDocumentContent(document.content)}</div>
          </article>
        ))}
      </div>
    </section>
  );
}
