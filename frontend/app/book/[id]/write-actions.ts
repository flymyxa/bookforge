"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function writeChapterOneAction(formData: FormData): Promise<void> {
  const bookId = formData.get("bookId");

  if (typeof bookId !== "string" || !bookId) {
    throw new Error("Missing book ID");
  }

  const response = await fetch(`${API_BASE_URL}/v1/pipeline/${bookId}/writing/chapter-1`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
    body: "{}",
  });

  if (!response.ok) {
    throw new Error(`Chapter generation failed: ${response.status}`);
  }

  revalidatePath(`/book/${bookId}`);
  revalidatePath(`/book/${bookId}/pipeline`);
  redirect(`/book/${bookId}/pipeline`);
}
