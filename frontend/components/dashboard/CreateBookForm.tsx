export function CreateBookForm({
  action,
}: {
  action: (formData: FormData) => void | Promise<void>;
}) {
  return (
    <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5">
        <p className="text-sm font-semibold uppercase tracking-[0.25em] text-signal">
          New Book
        </p>
        <h2 className="mt-2 text-2xl font-semibold">Start a pipeline run</h2>
        <p className="mt-2 text-sm text-slate-600">
          Create a book record and jump directly into its live pipeline view.
        </p>
      </div>
      <form action={action} className="grid gap-4">
        <label className="grid gap-2">
          <span className="text-sm font-medium text-slate-700">Title</span>
          <input
            className="rounded-2xl border border-slate-300 px-4 py-3 outline-none"
            name="title"
            placeholder="Dungeon Seed Protocol"
            required
            type="text"
          />
        </label>
        <label className="grid gap-2">
          <span className="text-sm font-medium text-slate-700">Genre</span>
          <input
            className="rounded-2xl border border-slate-300 px-4 py-3 outline-none"
            defaultValue="LitRPG"
            name="genre"
            required
            type="text"
          />
        </label>
        <label className="grid gap-2">
          <span className="text-sm font-medium text-slate-700">Series</span>
          <input
            className="rounded-2xl border border-slate-300 px-4 py-3 outline-none"
            name="series"
            placeholder="Optional series name"
            type="text"
          />
        </label>
        <button
          className="mt-2 rounded-full bg-ink px-5 py-3 text-sm text-paper transition hover:opacity-90"
          type="submit"
        >
          Create And Open Pipeline
        </button>
      </form>
    </section>
  );
}
