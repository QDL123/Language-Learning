import type { Metadata } from "next";
import {Open_Sans } from 'next/font/google'

import "./globals.css";

export const metadata: Metadata = {
  title: "Learn language through conversation",
  description: "Learn language through AI-powered dialogs",
};

const openSans = Open_Sans({
  subsets: ['latin'],
  display: 'swap',
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={openSans.className}>
        {children}
      </body>
    </html>
  );
}
