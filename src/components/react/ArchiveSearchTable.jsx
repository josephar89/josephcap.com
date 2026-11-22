import React, { useState, useMemo } from "react";
import { Search, FileText, ExternalLink, BookOpen, Clock } from "lucide-react";

export default function ArchiveSearchTable({ archives }) {
  const [tab, setTab] = useState("philosophy");
  const [query, setQuery] = useState("");

  const current = archives?.[tab] || { institute: "", groups: [] };

  const filteredGroups = useMemo(() => {
    const q = query.trim().toLowerCase();
    return (current.groups || [])
      .map((g) => ({
        ...g,
        items: g.items.filter(
          (item) =>
            !q ||
            item.title.toLowerCase().includes(q) ||
            g.category.toLowerCase().includes(q)
        ),
      }))
      .filter((g) => g.items.length > 0);
  }, [current, query]);

  const totalCount = filteredGroups.reduce((sum, g) => sum + g.items.length, 0);

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div className="inline-flex rounded-xl border border-stone-800 bg-stone-900 p-1">
          {[
            { id: "philosophy", label: "Philosophy (2013–2016)" },
            { id: "theology", label: "Theology (2017–2020)" },
          ].map((t) => (
            <button
              key={t.id}
              type="button"
              onClick={() => setTab(t.id)}
              className={`rounded-lg px-4 py-2 text-xs font-bold transition sm:text-sm ${
                tab === t.id
                  ? "bg-amber-500 text-stone-950"
                  : "text-stone-400 hover:text-white"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        <div className="relative w-full sm:w-80">
          <Search className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-stone-500" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Filter subjects, courses, or papers..."
            className="w-full rounded-xl border border-stone-700 bg-stone-950 py-2.5 pl-10 pr-4 text-sm text-white placeholder-stone-500 outline-none focus:border-amber-500"
          />
        </div>
      </div>

      <div className="flex items-center justify-between rounded-xl border border-stone-800 bg-stone-900/50 px-4 py-3 text-xs text-stone-400">
        <span className="inline-flex items-center gap-2 font-medium text-stone-200">
          <BookOpen className="h-4 w-4 text-amber-400" />
          {current.institute}
        </span>
        <span>{totalCount} documents</span>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {filteredGroups.map((group) => (
          <section
            key={group.category}
            className="rounded-2xl border border-stone-800 bg-stone-900/60 p-5"
          >
            <h2 className="mb-4 border-b border-stone-800 pb-2 text-sm font-bold uppercase tracking-wider text-amber-400">
              {group.category}
            </h2>
            <ul className="space-y-2">
              {group.items.map((doc, idx) => (
                <li key={`${doc.title}-${idx}`}>
                  {doc.available && doc.url ? (
                    <a
                      href={doc.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="group flex items-center justify-between gap-2 rounded-lg border border-transparent px-2.5 py-2 text-sm text-stone-200 transition hover:border-amber-500/30 hover:bg-stone-950 hover:text-amber-300"
                    >
                      <span className="inline-flex items-center gap-2.5">
                        <FileText className="h-4 w-4 shrink-0 text-amber-500/80" />
                        <span>{doc.title}</span>
                      </span>
                      <ExternalLink className="h-3.5 w-3.5 shrink-0 opacity-60 group-hover:opacity-100" />
                    </a>
                  ) : (
                    <div className="flex items-center justify-between gap-2 px-2.5 py-2 text-sm text-stone-500">
                      <span className="inline-flex items-center gap-2.5">
                        <Clock className="h-4 w-4 shrink-0" />
                        <span>{doc.title}</span>
                      </span>
                      <span className="rounded bg-stone-800 px-2 py-0.5 text-[10px]">
                        Scanning Pending
                      </span>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>
    </div>
  );
}
