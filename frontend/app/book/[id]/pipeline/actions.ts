"use server";

import { revalidatePath } from "next/cache";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function advancePipelineAction(formData: FormData): Promise<void> {
  const bookId = formData.get("bookId");

  if (typeof bookId !== "string" || !bookId) {
    throw new Error("Missing book ID");
  }

  const response = await fetch(`${API_BASE_URL}/v1/pipeline/${bookId}/advance`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
    body: "{}",
  });

  if (!response.ok) {
    throw new Error(`Advance request failed: ${response.status}`);
  }

  revalidatePath(`/book/${bookId}/pipeline`);
  revalidatePath(`/book/${bookId}`);
  revalidatePath("/dashboard");
}
