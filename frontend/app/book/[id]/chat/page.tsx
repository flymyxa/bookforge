import { ChatInterface } from "@/components/chat/ChatInterface";
import { apiGetSafe } from "@/lib/api";
import { sendChatMessageAction } from "./actions";

type ChatResponse = {
  book_id: string;
  messages: Array<{ id: string; role: "assistant" | "user"; content: string }>;
};

export const dynamic = "force-dynamic";

export default async function ChatPage({
  params,
}: {
  params: { id: string };
}) {
  const fallback: ChatResponse = {
    book_id: params.id,
    messages: [
      { id: "fallback-1", role: "assistant", content: "Tell me about the emotional core of the series." },
    ],
  };

  const chat = await apiGetSafe<ChatResponse>(`/v1/chat/${params.id}`, fallback);

  return (
    <ChatInterface
      bookId={params.id}
      messages={chat.messages.map((message) => ({
        role: message.role,
        content: message.content,
      }))}
      sendAction={sendChatMessageAction}
    />
  );
}
