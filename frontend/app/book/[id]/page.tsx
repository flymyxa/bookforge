import Link from "next/link";

import { Sidebar } from "@/components/layout/Sidebar";
import { ChapterPreview } from "@/components/pipeline/ChapterPreview";
import { FoundationPreview } from "@/components/pipeline/FoundationPreview";
import { apiGetSafe } from "@/lib/api";
import { buildFoundationAction } from "./actions";
import { writeChapterOneAction } from "./write-actions";

type BookSummary = {
  id: string;
  title: string;
  genre: string;
  status: string;
};

type DocumentsResponse = {
  documents: Array<{ id: string; name: string; status: string }>;
};

type ChapterFileResponse = {
  chapter_id: string;
  title: string;
  content: string;
};

type DocumentDetailResponse = {
  id: string;
  book_id: string;
  name: string;
  status: string;
  content: string | null;
};

export const dynamic = "force-dynamic";

export default async function BookOverviewPage({
  params,
}: {
  params: { id: string };
}) {
  const fallbackBook: BookSummary = {
    id: params.id,
    title: `Book ${params.id}`,
    genre: "Unknown",
    status: "unavailable",
  };
  const fallbackDocuments: DocumentsResponse = {
    documents: [
      { id: `${params.id}-creative-vision`, name: "Creative Vision", status: "ready" },
      { id: `${params.id}-world-bible`, name: "World Bible", status: "queued" },
    ],
  };

  const [book, documentPayload, chapterOne] = await Promise.all([
    apiGetSafe<BookSummary>(`/v1/books/${params.id}`, fallbackBook),
    apiGetSafe<DocumentsResponse>(`/v1/documents/${params.id}`, fallbackDocuments),
    apiGetSafe<ChapterFileResponse | null>(`/v1/files/${params.id}/chapters/1`, null),
  ]);
  const foundationDocumentNames = ["Creative Vision", "World Bible", "Character Bible"];
  const foundationDocuments = await Promise.all(
    documentPayload.documents
      .filter((document) => foundationDocumentNames.includes(document.name))
      .map((document) =>
        apiGetSafe<DocumentDetailResponse>(
          `/v1/documents/${params.id}/${document.id}`,
          {
            id: document.id,
            book_id: params.id,
            name: document.name,
            status: document.status,
            content: null,
          },
        ),
      ),
  );

  return (
    <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
      <Sidebar documents={documentPayload.documents} />
      <section className="space-y-4">
        <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Book Overview</p>
        <h1 className="text-3xl font-semibold">{book.title}</h1>
        <p className="text-sm uppercase tracking-[0.2em] text-signal">{book.status}</p>
        <p className="max-w-2xl text-slate-700">
          Genre: {book.genre}. This page is now pulling book and document data from the
          backend stubs and acts as the navigation hub for the main workflow surfaces.
        </p>
        <div className="flex flex-wrap gap-3 pt-2">
          <Link className="rounded-full bg-ink px-4 py-2 text-paper" href={`/book/${params.id}/chat`}>
            Open Chat
          </Link>
          <form action={buildFoundationAction}>
            <input name="bookId" type="hidden" value={params.id} />
            <button className="rounded-full bg-signal px-4 py-2 text-white" type="submit">
              Build Foundation
            </button>
          </form>
          <form action={writeChapterOneAction}>
            <input name="bookId" type="hidden" value={params.id} />
            <button className="rounded-full bg-moss px-4 py-2 text-white" type="submit">
              Write Chapter 1
            </button>
          </form>
          <Link className="rounded-full border border-ink px-4 py-2" href={`/book/${params.id}/discover`}>
            Open Wizard
          </Link>
          <Link className="rounded-full border border-ink px-4 py-2" href={`/book/${params.id}/pipeline`}>
            View Pipeline
          </Link>
        </div>
        <FoundationPreview documents={foundationDocuments} />
        <ChapterPreview
          chapter={chapterOne}
          emptyMessage="Once Writing builds Chapter 1, the draft will appear here so the browser flow ends in a readable manuscript artifact."
        />
      </section>
    </div>
  );
}
