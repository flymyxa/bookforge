import Link from "next/link";

export default function HomePage() {
  return (
    <section className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
      <div className="space-y-6">
        <p className="text-sm font-semibold uppercase tracking-[0.25em] text-signal">
          AI Book Publishing Pipeline
        </p>
        <h1 className="max-w-3xl text-5xl font-semibold leading-tight">
          Turn a rough book idea into a KDP-ready manuscript through one visible pipeline.
        </h1>
        <p className="max-w-2xl text-lg text-slate-700">
          BookForge packages discovery, foundation building, chapter writing, editing,
          and assembly into a browser-based workflow with chat mode, form mode, and a
          live pipeline dashboard.
        </p>
        <div className="flex gap-4">
          <Link className="rounded-full bg-ink px-5 py-3 text-paper" href="/dashboard">
            Open Dashboard
          </Link>
          <Link className="rounded-full border border-ink px-5 py-3" href="/book/demo/pipeline">
            View Pipeline Demo
          </Link>
        </div>
      </div>
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
        <p className="mb-4 text-sm font-medium text-slate-500">MVP Targets</p>
        <ul className="space-y-3 text-sm text-slate-700">
          <li>Chat-based creative discovery</li>
          <li>25-question form wizard</li>
          <li>Foundation document generation</li>
          <li>Three demo chapters with continuity gating</li>
          <li>Live Factorio-style pipeline view</li>
          <li>Assembled manuscript download</li>
        </ul>
      </div>
    </section>
  );
}
