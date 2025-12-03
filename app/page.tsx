"use client";

import { useState } from "react";

export default function Home() {
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e: any) => {
    const files = e.target.files;
    if (!files.length) return;

    setLoading(true);

    const form = new FormData();
    for (let f of files) form.append("files", f);

    const res = await fetch("/api/editar", {
      method: "POST",
      body: form,
    });

    const blob = await res.blob();

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "pdf_editados.zip";
    a.click();

    setLoading(false);
  };

  return (
    <div className="p-10 max-w-xl mx-auto text-center">
      <h1 className="text-3xl font-bold mb-4">
        Editor de PDFs Riverlabs
      </h1>

      <input
        type="file"
        multiple
        accept="application/pdf"
        className="border border-gray-300 p-4 rounded bg-white"
        onChange={handleUpload}
      />

      {loading && (
        <p className="mt-4 text-blue-600 font-semibold">
          Procesando PDFs...
        </p>
      )}
    </div>
  );
}
