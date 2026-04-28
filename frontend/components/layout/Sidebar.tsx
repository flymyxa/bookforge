export function Sidebar({
  documents,
}: {
  documents: Array<{ id?: string; name: string; status: string }>;
}) {
  return (
    <aside className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-sm font-medium text-slate-500">Documents</p>
      <ul className="mt-4 space-y-3 text-sm">
        {documents.map((document) => (
          <li key={document.name} className="rounded-2xl bg-slate-50 px-3 py-2">
            <div className="flex items-center justify-between gap-3">
              <span>{document.name}</span>
              <span className="text-xs uppercase tracking-[0.2em] text-slate-500">
                {document.status}
              </span>
            </div>
          </li>
        ))}
      </ul>
    </aside>
  );
}
