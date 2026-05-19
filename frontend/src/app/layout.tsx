import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Adversarial AI Security Dashboard",
  description: "Real-time RAG pipeline security monitoring with adversarial attack detection",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-background text-white antialiased">{children}</body>
    </html>
  );
}
