'use client';
import { useEffect, useState } from "react";
import "./globals.css";
import { I18nProvider, useI18n } from "@/lib/i18n";

function NavContent() {
  const { t, lang, setLang } = useI18n();
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    setLoggedIn(!!sessionStorage.getItem("token"));
  }, []);

  return (
    <nav className="max-w-4xl mx-auto flex gap-6 items-center">
      <a href="/" className="font-bold">{t("nav.home")}</a>
      <a href="/chat">{t("nav.chat")}</a>
      <a href="/voice">{t("nav.voice")}</a>
      <a href="/about">{t("nav.about")}</a>
      {loggedIn ? (
        <a href="/settings">{t("nav.settings")}</a>
      ) : (
        <a href="/login">{t("nav.login")}</a>
      )}
      <button
        onClick={() => setLang(lang === "en" ? "zh" : "en")}
        className="ml-auto px-2 py-1 border rounded text-sm hover:bg-gray-100"
      >
        {t("lang.switch")}
      </button>
    </nav>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen bg-gray-50">
        <I18nProvider>
          <header className="bg-white shadow-sm p-4">
            <NavContent />
          </header>
          <main className="max-w-4xl mx-auto p-4">{children}</main>
          <footer className="text-center p-4 text-gray-500 text-sm">
            Digital Twin - Powered by Local OSS LLM
          </footer>
        </I18nProvider>
      </body>
    </html>
  );
}
