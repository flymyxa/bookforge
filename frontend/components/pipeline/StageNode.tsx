export function StageNode({
  name,
  status,
}: {
  name: string;
  status: "idle" | "running" | "complete";
}) {
  const palette = {
    idle: "border-slate-300 bg-white text-slate-600",
    running: "border-amber-300 bg-amber-50 text-amber-900",
    complete: "border-emerald-300 bg-emerald-50 text-emerald-900",
  }[status];

  return (
    <div className={`min-w-40 rounded-3xl border px-4 py-3 ${palette}`}>
      <p className="text-xs uppercase tracking-[0.2em]">{status}</p>
      <p className="mt-2 font-medium capitalize">{name}</p>
    </div>
  );
}
