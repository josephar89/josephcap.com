import React, { useState, useEffect } from "react";
import {
  Play,
  X,
  ExternalLink,
  Sparkles,
  Cpu,
  Clapperboard,
  Globe,
  FolderCode,
} from "lucide-react";

function FilmModal({ film, onClose }) {
  useEffect(() => {
    if (!film) return;
    const onKey = (e) => {
      if (e.key === "Escape") onClose();
    };
    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", onKey);
    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", onKey);
    };
  }, [film, onClose]);

  if (!film) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 p-4 backdrop-blur-md"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
    >
      <div
        className="relative max-h-[92vh] w-full max-w-4xl overflow-y-auto rounded-2xl border border-stone-700 bg-stone-950 text-stone-100 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="sticky top-0 z-10 flex items-center justify-between border-b border-stone-800 bg-stone-950/95 px-6 py-4 backdrop-blur">
          <div>
            <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-amber-400">
              <Clapperboard className="h-3.5 w-3.5" />
              <span>{film.institution}</span>
            </div>
            <h3 className="mt-0.5 text-xl font-bold text-white sm:text-2xl">
              {film.title}
            </h3>
            <p className="text-xs text-stone-400">{film.alternateTitle}</p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close modal"
            className="rounded-full border border-stone-700 bg-stone-900 p-2 text-stone-300 hover:border-amber-500 hover:text-white"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="aspect-video w-full bg-black">
          {film.youtubeId ? (
            <iframe
              className="h-full w-full"
              src={`https://www.youtube.com/embed/${film.youtubeId}?autoplay=1&rel=0`}
              title={film.title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          ) : (
            <div className="flex h-full w-full flex-col items-center justify-center bg-gradient-to-br from-emerald-950 via-cyan-950 to-stone-950 p-8 text-center">
              <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-emerald-400/40 bg-emerald-500/15 px-4 py-1 text-xs font-semibold uppercase tracking-widest text-emerald-300">
                <Cpu className="h-4 w-4 animate-pulse" />
                In Production • Hybrid AI Studio
              </div>
              <h4 className="font-mono text-2xl font-bold text-white sm:text-4xl">
                EDEN_OS // SYSTEM_RESTORE
              </h4>
              <p className="mt-3 max-w-lg text-sm text-stone-300">
                Final 4K render is currently in post-production at DBIMA Paris.
                Inspect the interactive HTML simulator files built for on-set
                shooting below.
              </p>
              {film.resourceUrl && (
                <a
                  href={film.resourceUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-6 inline-flex items-center gap-2 rounded-full bg-emerald-500 px-6 py-2.5 text-sm font-bold text-stone-950 hover:bg-emerald-400"
                >
                  <FolderCode className="h-4 w-4" />
                  Explore Eden OS Emulator Files
                  <ExternalLink className="h-3.5 w-3.5" />
                </a>
              )}
            </div>
          )}
        </div>

        <div className="space-y-6 p-6 sm:p-8">
          <div className="flex flex-wrap items-center gap-3 text-xs text-stone-300">
            <span className="rounded-full border border-amber-500/40 bg-amber-500/10 px-3 py-1 font-semibold text-amber-300">
              {film.status}
            </span>
            <span className="rounded-full border border-stone-700 bg-stone-900 px-3 py-1">
              {film.year}
            </span>
            <span className="inline-flex items-center gap-1.5 rounded-full border border-stone-700 bg-stone-900 px-3 py-1">
              <Globe className="h-3.5 w-3.5 text-stone-400" />
              {film.language}
            </span>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <div>
              <h4 className="mb-2 text-xs font-bold uppercase tracking-wider text-amber-400">
                Synopsis
              </h4>
              <p className="text-sm leading-relaxed text-stone-300">
                {film.synopsis}
              </p>
            </div>
            <div>
              <h4 className="mb-2 text-xs font-bold uppercase tracking-wider text-amber-400">
                Director&apos;s &amp; Production Note
              </h4>
              <p className="text-sm leading-relaxed text-stone-300">
                {film.directorNotes}
              </p>
            </div>
          </div>

          <div className="rounded-xl border border-stone-800 bg-stone-900/60 p-4">
            <div className="mb-3 flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-stone-300">
              <Sparkles className="h-4 w-4 text-amber-400" />
              <span>Hybrid Cinema &amp; AI Pipeline</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {(film.techStack || []).map((t) => (
                <span
                  key={t}
                  className="rounded-lg border border-stone-700 bg-stone-950 px-3 py-1.5 text-xs font-medium text-stone-200"
                >
                  {t}
                </span>
              ))}
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-3 border-t border-stone-800 pt-4">
            <p className="text-xs italic text-stone-400">
              &ldquo;{film.tagline}&rdquo;
            </p>
            {film.youtubeId && (
              <a
                href={`https://www.youtube.com/watch?v=${film.youtubeId}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-lg border border-amber-500/40 bg-amber-500/10 px-4 py-2 text-xs font-semibold text-amber-300 hover:bg-amber-500 hover:text-stone-950"
              >
                Watch on YouTube
                <ExternalLink className="h-3.5 w-3.5" />
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function CinemaPortfolio({ films = [] }) {
  const [selectedFilm, setSelectedFilm] = useState(null);

  return (
    <>
      <div className="grid grid-cols-1 gap-7 md:grid-cols-2 lg:grid-cols-3">
        {films.map((film) => {
          const poster = film.youtubeId
            ? `https://img.youtube.com/vi/${film.youtubeId}/maxresdefault.jpg`
            : null;
          const fallback = film.youtubeId
            ? `https://img.youtube.com/vi/${film.youtubeId}/hqdefault.jpg`
            : null;

          return (
            <article
              key={film.id}
              onClick={() => setSelectedFilm(film)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  setSelectedFilm(film);
                }
              }}
              className="group flex cursor-pointer flex-col overflow-hidden rounded-2xl border border-stone-800 bg-stone-900/70 shadow-lg transition duration-300 hover:-translate-y-1 hover:border-amber-500/60 focus:outline-none focus:ring-2 focus:ring-amber-500"
            >
              <div className="relative aspect-[16/10] w-full overflow-hidden bg-stone-950">
                {poster ? (
                  <img
                    src={poster}
                    onError={(e) => {
                      if (fallback) e.currentTarget.src = fallback;
                    }}
                    alt={film.title}
                    className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
                  />
                ) : (
                  <div className="flex h-full w-full flex-col items-center justify-center bg-gradient-to-br from-emerald-950 via-cyan-950 to-stone-950 p-6 text-center">
                    <Cpu className="mb-3 h-10 w-10 text-emerald-400 transition group-hover:scale-110" />
                    <span className="font-mono text-[11px] tracking-[0.2em] text-emerald-300/80">
                      EDEN OS // 4K HYBRID VFX
                    </span>
                    <p className="mt-1 text-base font-bold text-white">
                      {film.title}
                    </p>
                  </div>
                )}

                <div className="absolute inset-0 bg-gradient-to-t from-stone-950 via-stone-950/30 to-transparent" />
                <div className="absolute left-3.5 right-3.5 top-3.5 flex items-center justify-between">
                  <span
                    className={`rounded-full px-2.5 py-1 text-[11px] font-semibold backdrop-blur-md ${
                      film.youtubeId
                        ? "border border-amber-400/40 bg-stone-950/75 text-amber-300"
                        : "border border-emerald-400/40 bg-emerald-950/80 text-emerald-300"
                    }`}
                  >
                    {film.status}
                  </span>
                  <span className="rounded-full border border-white/15 bg-stone-950/70 px-2.5 py-1 text-[11px] font-medium text-stone-200 backdrop-blur-md">
                    {film.year}
                  </span>
                </div>

                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="flex h-14 w-14 items-center justify-center rounded-full border border-white/30 bg-black/55 text-white backdrop-blur-sm transition group-hover:scale-110 group-hover:border-amber-400 group-hover:bg-amber-500 group-hover:text-stone-950">
                    {film.youtubeId ? (
                      <Play className="ml-0.5 h-6 w-6 fill-current" />
                    ) : (
                      <FolderCode className="h-6 w-6" />
                    )}
                  </div>
                </div>
              </div>

              <div className="flex flex-1 flex-col justify-between p-5">
                <div>
                  <h3 className="text-lg font-bold text-white group-hover:text-amber-300">
                    {film.title}
                  </h3>
                  <p className="text-xs font-medium text-amber-400/80">
                    {film.alternateTitle}
                  </p>
                  <p className="mt-3 line-clamp-3 text-sm leading-relaxed text-stone-400">
                    {film.synopsis}
                  </p>
                </div>

                <div className="mt-5 space-y-3 border-t border-stone-800/80 pt-4">
                  <div className="flex flex-wrap gap-1.5">
                    {(film.techStack || []).slice(0, 2).map((tech) => (
                      <span
                        key={tech}
                        className="rounded-md border border-stone-700/70 bg-stone-950 px-2 py-0.5 text-[11px] text-stone-300"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                  <div className="flex items-center justify-between text-xs font-semibold text-amber-400">
                    <span>
                      {film.youtubeId
                        ? "Watch Film & Notes"
                        : "Inspect Production & Eden OS"}
                    </span>
                    <span className="transition-transform group-hover:translate-x-1">
                      →
                    </span>
                  </div>
                </div>
              </div>
            </article>
          );
        })}
      </div>

      <FilmModal film={selectedFilm} onClose={() => setSelectedFilm(null)} />
    </>
  );
}
