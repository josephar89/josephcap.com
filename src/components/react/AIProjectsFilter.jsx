import React, { useState, useMemo } from "react";
import { Search, Sparkles, ExternalLink, ArrowRight } from "lucide-react";

export default function AIProjectsFilter({ projects = [] }) {
  const categories = useMemo(
    () => ["All", ...Array.from(new Set(projects.map((p) => p.category)))],
    [projects]
  );
  const [selectedCat, setSelectedCat] = useState("All");
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return projects.filter((p) => {
      const catOk = selectedCat === "All" || p.category === selectedCat;
      const qOk =
        !q ||
        p.title.toLowerCase().includes(q) ||
        p.summary.toLowerCase().includes(q) ||
        p.category.toLowerCase().includes(q);
      return catOk && qOk;
    });
  }, [projects, selectedCat, query]);

  return (
    <div className="space-y-6">
      {/* Search + Category Pills */}
      <div className="space-y-3 rounded-2xl border border-stone-800 bg-stone-900/60 p-4">
        <div className="relative">
          <Search className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-stone-500" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search AI case studies (Suno, Gemini, NotebookLM, Veo, Colab)..."
            className="w-full rounded-xl border border-stone-700 bg-stone-950 py-2.5 pl-10 pr-4 text-sm text-white placeholder-stone-500 outline-none focus:border-amber-500"
          />
        </div>
        <div className="flex flex-wrap gap-1.5">
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setSelectedCat(cat)}
              className={`rounded-full px-3 py-1 text-xs font-medium transition ${
                selectedCat === cat
                  ? "bg-amber-500 text-stone-950"
                  : "border border-stone-700 bg-stone-950 text-stone-300 hover:border-stone-500 hover:text-white"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Case Studies Grid */}
      <div className="grid gap-6 md:grid-cols-2">
        {filtered.map((proj) => {
          const isExternal = proj.ctaUrl?.startsWith("http");
          return (
            <article
              key={proj.id}
              className="flex flex-col justify-between rounded-2xl border border-stone-800 bg-stone-900/60 p-6 transition hover:border-amber-500/50"
            >
              <div>
                <div className="mb-2 inline-flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-wider text-amber-400">
                  <Sparkles className="h-3.5 w-3.5" />
                  <span>{proj.category}</span>
                </div>
                <h2 className="text-lg font-bold text-white">{proj.title}</h2>
                <p className="mt-3 text-sm leading-relaxed text-stone-400">
                  {proj.summary}
                </p>
              </div>

              {proj.ctaUrl && (
                <div className="mt-6 border-t border-stone-800/80 pt-4">
                  <a
                    href={proj.ctaUrl}
                    target={isExternal ? "_blank" : undefined}
                    rel={isExternal ? "noopener noreferrer" : undefined}
                    className="inline-flex items-center gap-2 text-xs font-bold text-amber-400 hover:text-amber-300"
                  >
                    <span>{proj.ctaLabel || "Explore Case Study"}</span>
                    {isExternal ? (
                      <ExternalLink className="h-3.5 w-3.5" />
                    ) : (
                      <ArrowRight className="h-3.5 w-3.5" />
                    )}
                  </a>
                </div>
              )}
            </article>
          );
        })}
      </div>
    </div>
  );
}
