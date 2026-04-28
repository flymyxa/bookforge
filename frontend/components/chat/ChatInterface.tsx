import { MessageBubble } from "./MessageBubble";

export function ChatInterface({
  messages,
  bookId,
  sendAction,
}: {
  messages: Array<{ role: "assistant" | "user"; content: string }>;
  bookId: string;
  sendAction: (formData: FormData) => void | Promise<void>;
}) {
  return (
    <section className="mx-auto flex w-full max-w-4xl flex-col gap-6">
      <div>
        <h1 className="text-3xl font-semibold">Chat Mode</h1>
        <p className="text-slate-600">Conversational creative discovery is now persisted through the API.</p>
      </div>
      <div className="space-y-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        {messages.map((message, index) => (
          <MessageBubble key={index} {...message} />
        ))}
      </div>
      <form action={sendAction} className="rounded-3xl border border-slate-200 bg-white p-4 shadow-sm">
        <input name="bookId" type="hidden" value={bookId} />
        <label className="block space-y-2">
          <span className="text-sm font-medium text-slate-700">Add a discovery message</span>
          <textarea
            className="min-h-28 w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none"
            name="message"
            placeholder="Describe the book idea, tone, character arc, or promise to the reader."
            required
          />
        </label>
        <button
          className="mt-4 rounded-full bg-ink px-5 py-3 text-sm text-paper transition hover:opacity-90"
          type="submit"
        >
          Send Message
        </button>
      </form>
    </section>
  );
}
