export function MessageBubble({
  role,
  content,
}: {
  role: "assistant" | "user";
  content: string;
}) {
  const styles =
    role === "assistant"
      ? "bg-slate-100 text-slate-800"
      : "ml-auto bg-moss text-white";

  return (
    <div className={`max-w-2xl rounded-3xl px-4 py-3 ${styles}`}>
      <p className="mb-1 text-[10px] font-semibold uppercase tracking-[0.25em] opacity-70">
        {role}
      </p>
      <p>{content}</p>
    </div>
  );
}
