import React from 'react';
import ClientLayout from '../components/ClientLayout';
import "./globals.css";

export const metadata = {
  title: "Verity",
  description: "Empowering MSMEs",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-300">
        <ClientLayout>
          {children}
        </ClientLayout>
      </body>
    </html>
  );
}
