import "../styles/globals.css";
import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";

export const metadata: Metadata = {
  title: "BookForge",
  description: "AI book publishing pipeline for indie authors."
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-paper text-ink">
        <Header />
        <main className="mx-auto flex min-h-[calc(100vh-64px)] w-full max-w-7xl flex-col px-6 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
