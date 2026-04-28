import Link from "next/link";

import { CreateBookForm } from "@/components/dashboard/CreateBookForm";
import { apiGetSafe } from "@/lib/api";
import { createBookAction } from "./actions";

type BookSummary = {
  id: string;
  title: string;
  genre: string;
  status: string;
};

export const dynamic = "force-dynamic";

const fallbackBooks: BookSummary[] = [
  { id: "demo", title: "Dungeon Seed Protocol", genre: "LitRPG", status: "discovery" },
  { id: "ghost-market", title: "The Ghost Market Index", genre: "Non-fiction", status: "foundation" },
];

export default async function DashboardPage() {
  const books = await apiGetSafe<BookSummary[]>("/v1/books", fallbackBooks);

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold">Library</h1>
        <p className="text-slate-600">Books in progress are loaded from the API.</p>
      </div>
      <div className="grid gap-6 lg:grid-cols-[360px_1fr]">
        <CreateBookForm action={createBookAction} />
        <div className="grid gap-4 md:grid-cols-2">
          {books.map((book) => (
            <Link key={book.id} href={`/book/${book.id}`} className="block">
              <article className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-signal">
                  {book.status}
                </p>
                <h2 className="mt-2 text-xl font-semibold">{book.title}</h2>
                <p className="mt-1 text-sm text-slate-600">{book.genre}</p>
              </article>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
