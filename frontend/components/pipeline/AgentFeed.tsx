export function AgentFeed({ feed }: { feed: string[] }) {
  return (
    <aside className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <h2 className="text-lg font-semibold">Agent Feed</h2>
      <ul className="mt-4 space-y-3 text-sm text-slate-600">
        {feed.map((item) => (
          <li key={item} className="rounded-2xl bg-slate-50 px-3 py-2">
            {item}
          </li>
        ))}
      </ul>
    </aside>
  );
}
