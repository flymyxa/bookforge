"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

type CreateBookResponse = {
  id: string;
  title: string;
  genre: string;
  status: string;
};

export async function createBookAction(formData: FormData): Promise<void> {
  const title = formData.get("title");
  const genre = formData.get("genre");
  const series = formData.get("series");

  if (typeof title !== "string" || !title.trim()) {
    throw new Error("Title is required");
  }

  if (typeof genre !== "string" || !genre.trim()) {
    throw new Error("Genre is required");
  }

  const response = await fetch(`${API_BASE_URL}/v1/books`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
    body: JSON.stringify({
      title: title.trim(),
      genre: genre.trim(),
      series: typeof series === "string" && series.trim() ? series.trim() : null,
    }),
  });

  if (!response.ok) {
    throw new Error(`Create book request failed: ${response.status}`);
  }

  const created = (await response.json()) as CreateBookResponse;

  revalidatePath("/dashboard");
  redirect(`/book/${created.id}/pipeline`);
}
