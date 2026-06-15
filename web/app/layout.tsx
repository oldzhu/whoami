import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "数字分身 | Digital Twin",
  description: "AI Digital Twin - Your Personal AI Clone",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm p-4">
          <nav className="max-w-4xl mx-auto flex gap-6">
            <a href="/" className="font-bold">数字分身</a>
            <a href="/chat">Chat</a>
            <a href="/voice">Voice</a>
            <a href="/about">About</a>
          </nav>
        </header>
        <main className="max-w-4xl mx-auto p-4">{children}</main>
        <footer className="text-center p-4 text-gray-500 text-sm">
          Digital Twin - Powered by Local OSS LLM
        </footer>
      </body>
    </html>
  );
}
