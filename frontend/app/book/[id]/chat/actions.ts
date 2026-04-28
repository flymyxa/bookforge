"use server";

import { revalidatePath } from "next/cache";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function sendChatMessageAction(formData: FormData): Promise<void> {
  const bookId = formData.get("bookId");
  const message = formData.get("message");

  if (typeof bookId !== "string" || !bookId) {
    throw new Error("Missing book ID");
  }

  if (typeof message !== "string" || !message.trim()) {
    throw new Error("Message is required");
  }

  const response = await fetch(`${API_BASE_URL}/v1/chat/${bookId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
    body: JSON.stringify({
      message: message.trim(),
    }),
  });

  if (!response.ok) {
    throw new Error(`Chat request failed: ${response.status}`);
  }

  revalidatePath(`/book/${bookId}/chat`);
}
