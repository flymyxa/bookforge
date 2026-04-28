export function QuestionField({ label }: { label: string }) {
  return (
    <label className="block space-y-2">
      <span className="text-sm font-medium text-slate-700">{label}</span>
      <textarea
        className="min-h-28 w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none ring-0"
        placeholder="Answer goes here..."
      />
    </label>
  );
}
