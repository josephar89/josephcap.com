#!/usr/bin/env python3
"""
JosephCap.com Interactive Islands & Final Pages Scaffold (Drop 3 of 3)
Generates all React interactive components, Art/Science/Archive pages,
and AGENT_PLAYBOOK.md for ongoing remote management in Google Antigravity.

Usage:
    python scaffold_interactive.py
    npm run build
"""

from pathlib import Path

ROOT = Path(".")

FILES = {
    # =========================================================================
    # 1. REACT ISLAND: VETRISAIPADAL 500+ KARAOKE PLAYER
    # =========================================================================
    "src/components/react/VetrisaipadalPlayer.jsx": r"""import React, { useState, useMemo } from "react";
import {
  Search,
  Play,
  SkipBack,
  SkipForward,
  Shuffle,
  Music,
  X,
  ExternalLink,
  Info,
  ListMusic,
  Volume2,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

export default function VetrisaipadalPlayer({ data }) {
  const tracks = data?.tracks || [];
  const categories = data?.categories || [];

  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [activeTrack, setActiveTrack] = useState(tracks[0] || null);
  const [showDisclaimer, setShowDisclaimer] = useState(false);
  const [visibleLimit, setVisibleLimit] = useState(60);

  const filteredTracks = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    return tracks.filter((t) => {
      const catOk = selectedCategory === "all" || t.category === selectedCategory;
      const qOk =
        !q ||
        t.title.toLowerCase().includes(q) ||
        t.code.toLowerCase().includes(q);
      return catOk && qOk;
    });
  }, [tracks, searchQuery, selectedCategory]);

  const getCategoryMeta = (catId) =>
    categories.find((c) => c.id === catId) || {
      id: "all",
      tamil: "அனைத்தும்",
      english: "All Tracks",
      playlistUrl: data?.channelUrl || "https://www.youtube.com/@Vetrisaipadal",
    };

  const handleStep = (dir) => {
    const pool = filteredTracks.length > 0 ? filteredTracks : tracks;
    if (!pool.length) return;
    const idx = pool.findIndex(
      (t) => activeTrack && t.youtubeId === activeTrack.youtubeId
    );
    const nextIdx = idx === -1 ? 0 : (idx + dir + pool.length) % pool.length;
    setActiveTrack(pool[nextIdx]);
  };

  const handleShuffle = () => {
    const pool = filteredTracks.length > 0 ? filteredTracks : tracks;
    if (pool.length <= 1) return;
    let pick = activeTrack;
    let tries = 0;
    while (pick?.youtubeId === activeTrack?.youtubeId && tries < 10) {
      pick = pool[Math.floor(Math.random() * pool.length)];
      tries += 1;
    }
    setActiveTrack(pick);
  };

  const currentCat = getCategoryMeta(selectedCategory);
  const displayedTracks = searchQuery
    ? filteredTracks
    : filteredTracks.slice(0, visibleLimit);

  return (
    <div className="space-y-6">
      {/* Header Controls */}
      <div className="flex flex-col justify-between gap-4 border-b border-stone-800 pb-6 md:flex-row md:items-end">
        <div>
          <div className="mb-2 inline-flex items-center gap-2 rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1 text-xs font-medium text-amber-300">
            <Volume2 className="h-3.5 w-3.5" />
            <span>
              AI Vocal-Isolated Tamil Catholic Karaoke • {tracks.length} Tracks
            </span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            வெற்றிசைப்பாடல்{" "}
            <span className="font-normal text-stone-400">| Vetrisaipadal</span>
          </h1>
          <p className="mt-2 text-sm text-stone-400">
            &ldquo;இசையோடு இணைந்து பாடுவோம்; இறைவனைப் புகழ்வோம்&rdquo; — Let us
            sing along with music; let us glorify God.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setShowDisclaimer((s) => !s)}
            className="inline-flex items-center gap-1.5 rounded-xl border border-stone-700 bg-stone-900 px-3.5 py-2 text-xs font-medium text-stone-300 transition hover:border-amber-500/50 hover:text-white"
          >
            <Info className="h-4 w-4 text-amber-400" />
            Liturgical Note
            {showDisclaimer ? (
              <ChevronUp className="h-3.5 w-3.5" />
            ) : (
              <ChevronDown className="h-3.5 w-3.5" />
            )}
          </button>
          <a
            href={data?.channelUrl || "https://www.youtube.com/@Vetrisaipadal"}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 rounded-xl bg-amber-500 px-4 py-2 text-xs font-bold text-stone-950 transition hover:bg-amber-400"
          >
            YouTube Channel
            <ExternalLink className="h-3.5 w-3.5" />
          </a>
        </div>
      </div>

      {/* Collapsible Bilingual Liturgical Disclaimer */}
      {showDisclaimer && (
        <div className="grid gap-4 rounded-2xl border border-amber-500/30 bg-amber-950/20 p-5 text-xs leading-relaxed text-stone-300 md:grid-cols-2">
          <div>
            <p className="mb-1 font-semibold text-amber-300">
              தமிழ் குறிப்பு (Pastoral Note)
            </p>
            <p>{data?.disclaimerTamil}</p>
          </div>
          <div>
            <p className="mb-1 font-semibold text-amber-300">
              English Disclaimer
            </p>
            <p>{data?.disclaimerEnglish}</p>
          </div>
        </div>
      )}

      {/* Main Split Workspace */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Active Player Deck */}
        <div className="flex flex-col overflow-hidden rounded-2xl border border-stone-800 bg-stone-900/70 shadow-xl lg:col-span-7">
          <div className="relative aspect-video w-full bg-black">
            {activeTrack ? (
              <iframe
                key={activeTrack.youtubeId}
                className="h-full w-full"
                src={`https://www.youtube.com/embed/${activeTrack.youtubeId}?rel=0`}
                title={activeTrack.title}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            ) : (
              <div className="flex h-full items-center justify-center text-stone-500">
                Select a track to play
              </div>
            )}
          </div>

          {activeTrack && (
            <div className="flex flex-1 flex-col justify-between gap-5 p-5 sm:p-6">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <div className="mb-1.5 flex items-center gap-2">
                    <span className="rounded bg-amber-500/20 px-2 py-0.5 font-mono text-xs font-bold text-amber-300">
                      #{activeTrack.code}
                    </span>
                    <span className="text-xs font-medium text-stone-400">
                      {getCategoryMeta(activeTrack.category).tamil} •{" "}
                      {getCategoryMeta(activeTrack.category).english}
                    </span>
                  </div>
                  <h2 className="text-xl font-bold text-white sm:text-2xl">
                    {activeTrack.title}
                  </h2>
                </div>
                <a
                  href={`https://www.youtube.com/watch?v=${activeTrack.youtubeId}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 rounded-lg border border-stone-700 bg-stone-950 px-3 py-1.5 text-xs font-medium text-stone-300 hover:border-amber-500/60 hover:text-amber-300"
                >
                  Open YouTube
                  <ExternalLink className="h-3.5 w-3.5" />
                </a>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-4 border-t border-stone-800 pt-4">
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => handleStep(-1)}
                    aria-label="Previous track"
                    className="rounded-full border border-stone-700 bg-stone-950 p-2.5 text-stone-200 transition hover:border-amber-500 hover:text-amber-400"
                  >
                    <SkipBack className="h-4 w-4" />
                  </button>
                  <button
                    type="button"
                    onClick={() => handleStep(1)}
                    className="inline-flex items-center gap-2 rounded-full bg-amber-500 px-5 py-2.5 text-xs font-bold text-stone-950 transition hover:bg-amber-400"
                  >
                    Next Track
                    <SkipForward className="h-4 w-4" />
                  </button>
                  <button
                    type="button"
                    onClick={handleShuffle}
                    aria-label="Shuffle track"
                    className="rounded-full border border-stone-700 bg-stone-950 p-2.5 text-stone-200 transition hover:border-amber-500 hover:text-amber-400"
                  >
                    <Shuffle className="h-4 w-4" />
                  </button>
                </div>

                <a
                  href={currentCat.playlistUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 text-xs font-semibold text-amber-400 hover:underline"
                >
                  <ListMusic className="h-4 w-4" />
                  Full {currentCat.english} Playlist
                </a>
              </div>
            </div>
          )}
        </div>

        {/* Search & Track Queue */}
        <div className="flex h-[580px] flex-col overflow-hidden rounded-2xl border border-stone-800 bg-stone-900/70 shadow-xl lg:col-span-5">
          <div className="border-b border-stone-800 p-4">
            <div className="relative">
              <Search className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-stone-500" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search Tamil title or track #code..."
                className="w-full rounded-xl border border-stone-700 bg-stone-950 py-2.5 pl-10 pr-9 text-sm text-white placeholder-stone-500 outline-none focus:border-amber-500"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery("")}
                  aria-label="Clear search"
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-stone-400 hover:text-white"
                >
                  <X className="h-4 w-4" />
                </button>
              )}
            </div>

            <div className="mt-3 flex gap-1.5 overflow-x-auto pb-1">
              {categories.map((cat) => {
                const isActive = selectedCategory === cat.id;
                return (
                  <button
                    key={cat.id}
                    type="button"
                    onClick={() => {
                      setSelectedCategory(cat.id);
                      setVisibleLimit(60);
                    }}
                    className={`shrink-0 rounded-full px-3 py-1 text-xs font-medium transition ${
                      isActive
                        ? "bg-amber-500 text-stone-950"
                        : "border border-stone-700 bg-stone-950 text-stone-300 hover:border-stone-500 hover:text-white"
                    }`}
                  >
                    {cat.english}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="flex items-center justify-between border-b border-stone-800 bg-stone-950/60 px-4 py-2 text-xs text-stone-400">
            <span>
              <strong className="text-stone-200">{filteredTracks.length}</strong>{" "}
              tracks found
            </span>
            <span className="truncate text-amber-400/90">{currentCat.tamil}</span>
          </div>

          <div className="flex-1 divide-y divide-stone-800/60 overflow-y-auto">
            {displayedTracks.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center p-6 text-center text-stone-500">
                <Music className="mb-2 h-8 w-8 opacity-50" />
                <p className="text-sm text-stone-300">No matching tracks.</p>
                <button
                  type="button"
                  onClick={() => {
                    setSearchQuery("");
                    setSelectedCategory("all");
                  }}
                  className="mt-2 text-xs font-semibold text-amber-400 hover:underline"
                >
                  Reset filters
                </button>
              </div>
            ) : (
              <>
                {displayedTracks.map((track) => {
                  const isPlaying = activeTrack?.youtubeId === track.youtubeId;
                  return (
                    <button
                      key={`${track.code}-${track.youtubeId}`}
                      type="button"
                      onClick={() => setActiveTrack(track)}
                      className={`group flex w-full items-center gap-3 px-4 py-3 text-left transition ${
                        isPlaying ? "bg-amber-500/15" : "hover:bg-stone-800/60"
                      }`}
                    >
                      <div
                        className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border transition ${
                          isPlaying
                            ? "border-amber-500 bg-amber-500 text-stone-950"
                            : "border-stone-700 bg-stone-950 text-stone-400 group-hover:border-amber-500/60 group-hover:text-amber-400"
                        }`}
                      >
                        <Play className="h-3.5 w-3.5 fill-current" />
                      </div>
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-[11px] font-semibold text-amber-400/80">
                            {track.code}
                          </span>
                          <p
                            className={`truncate text-sm font-semibold ${
                              isPlaying ? "text-amber-300" : "text-stone-100"
                            }`}
                          >
                            {track.title}
                          </p>
                        </div>
                        <p className="text-[11px] text-stone-500">
                          {getCategoryMeta(track.category).tamil}
                        </p>
                      </div>
                    </button>
                  );
                })}
                {!searchQuery && filteredTracks.length > visibleLimit && (
                  <div className="p-4 text-center">
                    <button
                      type="button"
                      onClick={() => setVisibleLimit((n) => n + 100)}
                      className="rounded-lg border border-amber-500/40 bg-amber-500/10 px-4 py-2 text-xs font-semibold text-amber-300 hover:bg-amber-500 hover:text-stone-950"
                    >
                      Load More ({filteredTracks.length - visibleLimit} remaining)
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
""",
    # =========================================================================
    # 2. REACT ISLAND: DBIMA PARIS CINEMA PORTFOLIO & MODAL
    # =========================================================================
    "src/components/react/CinemaPortfolio.jsx": r"""import React, { useState, useEffect } from "react";
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
""",
    # =========================================================================
    # 3. REACT ISLAND: ORIGINAL ALBUMS & LYRICS PLAYER
    # =========================================================================
    "src/components/react/AlbumLyricsPlayer.jsx": r"""import React, { useState } from "react";
import { Disc3, Play, FileText, ExternalLink } from "lucide-react";

export default function AlbumLyricsPlayer({ albums = [] }) {
  const [selectedSlug, setSelectedSlug] = useState(albums[0]?.slug || "");
  const activeAlbum =
    albums.find((a) => a.slug === selectedSlug) || albums[0] || null;
  const [selectedTrackIdx, setSelectedTrackIdx] = useState(0);

  if (!activeAlbum) return null;
  const activeTrack = activeAlbum.tracks?.[selectedTrackIdx] || activeAlbum.tracks?.[0];

  return (
    <div className="space-y-8">
      {/* Album Selector Tabs */}
      <div className="flex flex-wrap gap-2">
        {albums.map((alb) => {
          const active = alb.slug === activeAlbum.slug;
          return (
            <button
              key={alb.slug}
              type="button"
              onClick={() => {
                setSelectedSlug(alb.slug);
                setSelectedTrackIdx(0);
              }}
              className={`inline-flex items-center gap-2 rounded-xl px-4 py-2.5 text-xs font-semibold transition sm:text-sm ${
                active
                  ? "bg-amber-500 text-stone-950"
                  : "border border-stone-800 bg-stone-900 text-stone-300 hover:border-amber-500/50 hover:text-white"
              }`}
            >
              <Disc3 className="h-4 w-4" />
              <span>{alb.title}</span>
              <span className="opacity-70">({alb.year})</span>
            </button>
          );
        })}
      </div>

      {/* Active Album Workspace */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Tracklist Sidebar */}
        <div className="flex max-h-[620px] flex-col overflow-hidden rounded-2xl border border-stone-800 bg-stone-900/60 lg:col-span-4">
          <div className="border-b border-stone-800 p-4">
            <p className="text-[11px] font-bold uppercase tracking-wider text-amber-400">
              {activeAlbum.era}
            </p>
            <h2 className="mt-1 text-lg font-bold text-white">
              {activeAlbum.title}
            </h2>
            <p className="text-xs text-stone-400">
              {activeAlbum.year} • {activeAlbum.trackCount} Compositions
            </p>
          </div>
          <div className="flex-1 divide-y divide-stone-800/60 overflow-y-auto">
            {(activeAlbum.tracks || []).map((tr, idx) => {
              const isSelected = idx === selectedTrackIdx;
              return (
                <button
                  key={`${tr.title}-${idx}`}
                  type="button"
                  onClick={() => setSelectedTrackIdx(idx)}
                  className={`flex w-full items-center gap-3 px-4 py-3 text-left transition ${
                    isSelected ? "bg-amber-500/15" : "hover:bg-stone-800/60"
                  }`}
                >
                  <span
                    className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-xs font-bold ${
                      isSelected
                        ? "bg-amber-500 text-stone-950"
                        : "bg-stone-950 text-stone-400"
                    }`}
                  >
                    {tr.youtubeId ? <Play className="h-3 w-3 fill-current" /> : <FileText className="h-3 w-3" />}
                  </span>
                  <span
                    className={`truncate text-sm font-medium ${
                      isSelected ? "text-amber-300" : "text-stone-200"
                    }`}
                  >
                    {idx + 1}. {tr.title}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Audio & Lyrics Display */}
        <div className="space-y-6 rounded-2xl border border-stone-800 bg-stone-900/60 p-5 sm:p-6 lg:col-span-8">
          {activeTrack && (
            <>
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-stone-800 pb-4">
                <div>
                  <h3 className="text-xl font-bold text-white">
                    {activeTrack.title}
                  </h3>
                  <p className="text-xs text-stone-400">{activeAlbum.title}</p>
                </div>
                {activeTrack.youtubeId && (
                  <a
                    href={`https://www.youtube.com/watch?v=${activeTrack.youtubeId}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 rounded-lg border border-stone-700 px-3 py-1.5 text-xs text-amber-300 hover:bg-amber-500 hover:text-stone-950"
                  >
                    YouTube <ExternalLink className="h-3.5 w-3.5" />
                  </a>
                )}
              </div>

              {activeTrack.youtubeId ? (
                <div className="aspect-video w-full overflow-hidden rounded-xl bg-black">
                  <iframe
                    key={activeTrack.youtubeId}
                    className="h-full w-full"
                    src={`https://www.youtube.com/embed/${activeTrack.youtubeId}?rel=0`}
                    title={activeTrack.title}
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                  />
                </div>
              ) : (
                <div className="rounded-xl border border-stone-800 bg-stone-950/70 p-4 text-xs text-amber-300">
                  Lyrical Archive Entry — Studio audio tracking in progress.
                </div>
              )}

              {activeTrack.lyrics && (
                <div className="rounded-xl border border-stone-800 bg-stone-950/70 p-5">
                  <p className="mb-3 text-xs font-bold uppercase tracking-wider text-amber-400">
                    Lyrics &amp; Credits
                  </p>
                  <pre className="whitespace-pre-wrap font-sans text-sm leading-relaxed text-stone-200">
                    {activeTrack.lyrics}
                  </pre>
                </div>
              )}

              {activeTrack.lyricSheetImage && (
                <div className="overflow-hidden rounded-xl border border-stone-800 bg-white/5 p-2">
                  <img
                    src={activeTrack.lyricSheetImage}
                    alt={`${activeTrack.title} lyric sheet`}
                    className="mx-auto max-h-[640px] rounded-lg object-contain"
                    loading="lazy"
                  />
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
""",
    # =========================================================================
    # 4. REACT ISLAND: PHILOSOPHY & THEOLOGY SEARCHABLE PDF VAULT
    # =========================================================================
    "src/components/react/ArchiveSearchTable.jsx": r"""import React, { useState, useMemo } from "react";
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
""",
    # =========================================================================
    # 5. REACT ISLAND: FILTERABLE AI PROJECTS SHOWCASE
    # =========================================================================
    "src/components/react/AIProjectsFilter.jsx": r"""import React, { useState, useMemo } from "react";
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
""",
    # =========================================================================
    # 6. REACT ISLAND: GLOBAL AI WORKSHOPS EXPLORER
    # =========================================================================
    "src/components/react/WorkshopExplorer.jsx": r"""import React, { useState, useMemo } from "react";
import { MapPin, Calendar, Users, Target, Lightbulb, ExternalLink, Mail } from "lucide-react";

export default function WorkshopExplorer({ data }) {
  const workshops = data?.workshops || [];
  const countries = ["All", ...(data?.countries || [])];
  const [selectedCountry, setSelectedCountry] = useState("All");

  const filtered = useMemo(() => {
    if (selectedCountry === "All") return workshops;
    return workshops.filter((w) => w.country === selectedCountry);
  }, [workshops, selectedCountry]);

  const filteredAttendees = filtered.reduce(
    (sum, w) => sum + (w.participantsCount || 0),
    0
  );

  return (
    <div className="space-y-8">
      {/* Live Filter & Impact Strip */}
      <div className="flex flex-col justify-between gap-4 rounded-2xl border border-stone-800 bg-stone-900/60 p-5 sm:flex-row sm:items-center">
        <div className="flex flex-wrap gap-2">
          {countries.map((c) => (
            <button
              key={c}
              type="button"
              onClick={() => setSelectedCountry(c)}
              className={`rounded-full px-4 py-1.5 text-xs font-bold transition ${
                selectedCountry === c
                  ? "bg-amber-500 text-stone-950"
                  : "border border-stone-700 bg-stone-950 text-stone-300 hover:text-white"
              }`}
            >
              {c}
            </button>
          ))}
        </div>
        <div className="flex gap-6 text-xs">
          <div>
            <span className="block text-lg font-extrabold text-amber-400">
              {filtered.length}
            </span>
            <span className="text-stone-400">Workshops</span>
          </div>
          <div>
            <span className="block text-lg font-extrabold text-amber-400">
              {filteredAttendees}+
            </span>
            <span className="text-stone-400">Participants Trained</span>
          </div>
        </div>
      </div>

      {/* Workshop Cards */}
      <div className="grid gap-6 md:grid-cols-2">
        {filtered.map((ws) => (
          <article
            key={ws.id}
            className="flex flex-col overflow-hidden rounded-2xl border border-stone-800 bg-stone-900/60 transition hover:border-amber-500/50"
          >
            {ws.image && (
              <div className="aspect-[16/9] w-full overflow-hidden bg-stone-950">
                <img
                  src={ws.image}
                  alt={ws.title}
                  loading="lazy"
                  className="h-full w-full object-cover"
                />
              </div>
            )}
            <div className="flex flex-1 flex-col justify-between p-5">
              <div>
                <div className="flex items-center justify-between gap-2 text-xs text-amber-400">
                  <span className="inline-flex items-center gap-1 font-semibold">
                    <Calendar className="h-3.5 w-3.5" />
                    {ws.date}
                  </span>
                  <span className="rounded-full border border-amber-500/30 bg-amber-500/10 px-2.5 py-0.5 text-[11px] font-semibold">
                    {ws.country}
                  </span>
                </div>

                <h2 className="mt-2 text-lg font-bold text-white">{ws.title}</h2>

                <div className="mt-3 space-y-1.5 text-xs text-stone-400">
                  <p className="flex items-start gap-2">
                    <MapPin className="mt-0.5 h-3.5 w-3.5 shrink-0 text-stone-500" />
                    <span>{ws.place}</span>
                  </p>
                  <p className="flex items-start gap-2">
                    <Users className="mt-0.5 h-3.5 w-3.5 shrink-0 text-stone-500" />
                    <span>
                      {ws.targetGroup} ({ws.participantsLabel})
                    </span>
                  </p>
                  <p className="flex items-start gap-2">
                    <Target className="mt-0.5 h-3.5 w-3.5 shrink-0 text-amber-400/80" />
                    <span className="text-stone-300">{ws.focus}</span>
                  </p>
                </div>

                <div className="mt-4 rounded-xl border border-stone-800 bg-stone-950/60 p-3 text-xs leading-relaxed text-stone-300">
                  <span className="mb-1 inline-flex items-center gap-1 font-semibold text-amber-300">
                    <Lightbulb className="h-3.5 w-3.5" /> Key Takeaway
                  </span>
                  <p>{ws.takeaway}</p>
                </div>
              </div>

              <div className="mt-4 flex flex-wrap gap-2 border-t border-stone-800 pt-3 text-xs">
                {ws.linkedinUrl && (
                  <a
                    href={ws.linkedinUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 rounded-lg border border-stone-700 bg-stone-950 px-3 py-1.5 font-medium text-stone-200 hover:border-amber-500/60 hover:text-amber-300"
                  >
                    LinkedIn Post <ExternalLink className="h-3 w-3" />
                  </a>
                )}
                {ws.facebookUrl && (
                  <a
                    href={ws.facebookUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 rounded-lg border border-stone-700 bg-stone-950 px-3 py-1.5 font-medium text-stone-200 hover:border-amber-500/60 hover:text-amber-300"
                  >
                    Facebook Post <ExternalLink className="h-3 w-3" />
                  </a>
                )}
              </div>
            </div>
          </article>
        ))}
      </div>

      {/* Invite / Book a Workshop CTA */}
      <div className="rounded-2xl border border-amber-500/30 bg-gradient-to-r from-amber-950/30 via-stone-900 to-stone-900 p-6 sm:p-8">
        <h3 className="text-xl font-bold text-white">
          Invite Fr. Joseph for a Tailored AI Workshop
        </h3>
        <p className="mt-2 max-w-2xl text-sm text-stone-300">
          Available in-person (France, Europe, India) and online worldwide for Catholic
          institutions, schools, seminaries, religious congregations, and media teams.
        </p>
        <div className="mt-5 flex flex-wrap gap-3">
          <a
            href="mailto:josephar89@gmail.com?subject=AI%20Workshop%20Inquiry"
            className="inline-flex items-center gap-2 rounded-xl bg-amber-500 px-5 py-2.5 text-xs font-bold text-stone-950 hover:bg-amber-400"
          >
            <Mail className="h-4 w-4" />
            Request Workshop via Email
          </a>
          <a
            href="https://wa.me/918637668430"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-xl border border-stone-700 bg-stone-950 px-5 py-2.5 text-xs font-semibold text-white hover:border-amber-500/60"
          >
            WhatsApp Inquiry ↗
          </a>
        </div>
      </div>
    </div>
  );
}
""",
    # =========================================================================
    # 7. ASTRO PAGES FOR ART, SCIENCE & ARCHIVES
    # =========================================================================
    "src/pages/art/music/vetrisaipadal.astro": r"""---
import BaseLayout from "../../../layouts/BaseLayout.astro";
import VetrisaipadalPlayer from "../../../components/react/VetrisaipadalPlayer.jsx";
import vetriData from "../../../data/vetrisaipadal.json";
---

<BaseLayout
  title="Vetrisaipadal — Tamil Catholic AI Karaoke (500+ Tracks)"
  description="Searchable library of 500+ AI vocal-isolated Tamil Catholic devotional karaoke tracks by Fr. Joseph Arputha Raj OFM Cap."
>
  <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
    <VetrisaipadalPlayer client:load data={vetriData} />
  </div>
</BaseLayout>
""",
    "src/pages/art/music/albums.astro": r"""---
import BaseLayout from "../../../layouts/BaseLayout.astro";
import AlbumLyricsPlayer from "../../../components/react/AlbumLyricsPlayer.jsx";
import albumsData from "../../../data/albums.json";
---

<BaseLayout
  title="Original Musical Albums"
  description="Over 50 original Tamil, English, and multilingual sacred compositions spanning 2010 to 2020."
>
  <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
    <div class="mb-8 border-b border-stone-800 pb-6">
      <p class="text-xs font-bold uppercase tracking-widest text-amber-400">My Musical Anthology</p>
      <h1 class="mt-2 text-3xl font-extrabold text-white sm:text-4xl">Original Compositions &amp; Albums</h1>
      <p class="mt-2 max-w-2xl text-sm text-stone-400">
        Seven archival eras from Vizhigalile (2010) and Novitiate Carnatic explorations to Francesco Theological Institute—complete with audio and Tamil lyrics.
      </p>
    </div>
    <AlbumLyricsPlayer client:load albums={albumsData.albums} />
  </div>
</BaseLayout>
""",
    "src/pages/art/cinema.astro": r"""---
import BaseLayout from "../../layouts/BaseLayout.astro";
import CinemaPortfolio from "../../components/react/CinemaPortfolio.jsx";
import filmsData from "../../data/films.json";

const earlyFilms = [
  { title: "Short Film - 1 (St. Xavier's Primary School)", year: "2009", youtubeId: "HDToqa5AGwo" },
  { title: "Short Film - 2 (MBA Project Film)", year: "2009", youtubeId: "iAGsDwDq8Xo" },
];
---

<BaseLayout
  title="DBIMA Paris Cinema Portfolio"
  description="Digital Parables — Short films and Hybrid AI cinematography by Fr. Joseph Arputha Raj at DBIMA Paris."
>
  <div class="mx-auto max-w-7xl space-y-16 px-4 py-10 sm:px-6 lg:px-8">
    <div>
      <div class="mb-8 border-b border-stone-800 pb-6">
        <p class="text-xs font-bold uppercase tracking-widest text-amber-400">MA Cinema Arts &amp; Audiovisual • DBIMA Paris</p>
        <h1 class="mt-2 text-3xl font-extrabold text-white sm:text-4xl">Digital Parables | Film Portfolio</h1>
        <p class="mt-2 max-w-2xl text-sm text-stone-400">
          Click any film poster to launch the screening modal, read director&apos;s notes, and inspect the Hybrid AI production pipeline.
        </p>
      </div>
      <CinemaPortfolio client:load films={filmsData.dbimaFilms} />
    </div>

    <!-- Early Archives (2009) -->
    <div>
      <h2 class="mb-6 text-xl font-bold text-white">Early Short Film Archives (2009)</h2>
      <div class="grid gap-6 md:grid-cols-2">
        {earlyFilms.map((f) => (
          <div class="overflow-hidden rounded-2xl border border-stone-800 bg-stone-900/60">
            <div class="aspect-video w-full bg-black">
              <iframe
                class="h-full w-full"
                src={`https://www.youtube.com/embed/${f.youtubeId}`}
                title={f.title}
                loading="lazy"
                allowFullScreen
              />
            </div>
            <div class="p-4">
              <p class="text-xs font-semibold text-amber-400">{f.year}</p>
              <h3 class="text-sm font-bold text-white">{f.title}</h3>
            </div>
          </div>
        ))}
      </div>
    </div>
  </div>
</BaseLayout>
""",
    "src/pages/art/history.astro": r"""---
import BaseLayout from "../../layouts/BaseLayout.astro";
---

<BaseLayout title="History & Heritage — Malayadipatty & Family Tree">
  <div class="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
    <div class="mb-10 border-b border-stone-800 pb-6">
      <p class="text-xs font-bold uppercase tracking-widest text-amber-400">Heritage &amp; Genealogy</p>
      <h1 class="mt-2 text-3xl font-extrabold text-white sm:text-4xl">Preserving 350 Years of Roots</h1>
    </div>

    <div class="grid gap-8 md:grid-cols-2">
      <article class="flex flex-col justify-between rounded-2xl border border-stone-800 bg-stone-900/60 p-7">
        <div>
          <span class="text-xs font-bold uppercase text-amber-400">1660s – Present • Digital Archive</span>
          <h2 class="mt-2 text-2xl font-bold text-white">மலையடிப்பட்டி மறைப்பணித்தள வரலாறு (Malayadipatty)</h2>
          <p class="mt-3 text-sm leading-relaxed text-stone-400">
            Realizing that the proud 350-year mission history of my native village was at risk of being forgotten, I built this comprehensive digital archive during the 2020 lockdown—launched on the day of my Diaconate ordination.
          </p>
        </div>
        <a
          href="https://www.malayadipatty.com/"
          target="_blank"
          rel="noopener"
          class="mt-6 inline-block rounded-xl bg-amber-500 px-5 py-2.5 text-center text-xs font-bold text-stone-950 hover:bg-amber-400"
        >
          Visit Malayadipatty.com ↗
        </a>
      </article>

      <article class="flex flex-col justify-between rounded-2xl border border-stone-800 bg-stone-900/60 p-7">
        <div>
          <span class="text-xs font-bold uppercase text-amber-400">6 Generations Mapped • Ruby Jubilee Tribute</span>
          <h2 class="mt-2 text-2xl font-bold text-white">பட்டையதார் குடும்ப மரம் (Pattaiyathar Family Tree)</h2>
          <p class="mt-3 text-sm leading-relaxed text-stone-400">
            Created in collaboration with my uncle, Rev. Fr. Stephen Gaspar (Dindigul Diocese), tracing six generations of family heritage—launched on June 29, 2020 for his 40th Ruby Jubilee of priesthood.
          </p>
        </div>
        <div class="mt-6 flex flex-wrap gap-3">
          <a
            href="https://www.xmind.net/m/BMCAfs"
            target="_blank"
            rel="noopener"
            class="rounded-xl bg-amber-500 px-5 py-2.5 text-xs font-bold text-stone-950 hover:bg-amber-400"
          >
            Open Family Tree Map ↗
          </a>
          <a
            href="https://www.youtube.com/playlist?list=PL-483FpP8J8dDoS71rPVYrZYJ3V0UVLjF"
            target="_blank"
            rel="noopener"
            class="rounded-xl border border-stone-700 px-4 py-2.5 text-xs font-semibold text-stone-200 hover:border-amber-500/60"
          >
            Fr. Stephen Gaspar Sermons ↗
          </a>
        </div>
      </article>
    </div>
  </div>
</BaseLayout>
""",
    "src/pages/faith/archives/index.astro": r"""---
import BaseLayout from "../../../layouts/BaseLayout.astro";
import ArchiveSearchTable from "../../../components/react/ArchiveSearchTable.jsx";
import archivesData from "../../../data/archives.json";
---

<BaseLayout title="Philosophy & Theology Archives">
  <div class="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
    <a href="/faith" class="text-xs font-semibold text-amber-400 hover:underline">← Back to Faith Hub</a>
    <div class="mt-3 mb-8 border-b border-stone-800 pb-6">
      <h1 class="text-3xl font-extrabold text-white sm:text-4xl">Academic Study Archives</h1>
      <p class="mt-2 max-w-2xl text-sm text-stone-400">
        Searchable vault of seven years of Philosophy (St. Joseph&apos;s) and Theology (Francesco) study notes, scripts, and papers.
      </p>
    </div>
    <ArchiveSearchTable client:load archives={archivesData} />
  </div>
</BaseLayout>
""",
    "src/pages/science/ai-projects/index.astro": r"""---
import BaseLayout from "../../../layouts/BaseLayout.astro";
import AIProjectsFilter from "../../../components/react/AIProjectsFilter.jsx";
import projectsData from "../../../data/ai-projects.json";
---

<BaseLayout
  title="AI Lab & Applied Case Studies"
  description="14 real-world Generative AI workflows spanning audio restoration, cinema production, 12-language localization, HTML software props, and NGO grant writing."
>
  <div class="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
    <div class="mb-8 border-b border-stone-800 pb-6">
      <p class="text-xs font-bold uppercase tracking-widest text-amber-400">Applied Generative AI &amp; Algorethics</p>
      <h1 class="mt-2 text-3xl font-extrabold text-white sm:text-4xl">AI Lab &amp; Production Case Studies</h1>
      <p class="mt-2 max-w-3xl text-sm text-stone-400">
        Practical, frugal-innovation AI pipelines engineered across audio restoration, DBIMA cinema, theological localization, zero-code UI/UX, and nonprofit administration.
      </p>
    </div>
    <AIProjectsFilter client:load projects={projectsData.projects} />
  </div>
</BaseLayout>
""",
    "src/pages/science/ai-projects/sub-trans.astro": r"""---
import { getEntry } from "astro:content";
import ReaderLayout from "../../../layouts/ReaderLayout.astro";

const entry = await getEntry("writings", "sub-trans");
const rendered = entry ? await entry.render() : null;
const Content = rendered?.Content;
---

<ReaderLayout
  title={entry?.data.title || "Contextual Subtitle Translation Case Study"}
  subtitle="Cloud-based AI Pipeline (Google Colab T4 + Gemini 2.5 Flash + DaVinci Resolve 20)"
  badge="AI Engineering Case Study"
  backHref="/science/ai-projects"
  backLabel="All AI Projects"
>
  {Content ? <Content /> : <p>Run migrate_bundle.py to populate this case study.</p>}
</ReaderLayout>
""",
    "src/pages/science/ai-workshops.astro": r"""---
import BaseLayout from "../../layouts/BaseLayout.astro";
import WorkshopExplorer from "../../components/react/WorkshopExplorer.jsx";
import workshopsData from "../../data/workshops.json";
---

<BaseLayout
  title="Global AI Literacy Initiative — Workshops"
  description="15+ hands-on AI literacy workshops facilitated across India, France, Italy, and Cameroon for educators, PhD scholars, seminarians, and filmmakers."
>
  <div class="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
    <div class="mb-8 border-b border-stone-800 pb-6">
      <p class="text-xs font-bold uppercase tracking-widest text-amber-400">Global AI Literacy Initiative</p>
      <h1 class="mt-2 text-3xl font-extrabold text-white sm:text-4xl">International AI Workshops</h1>
      <p class="mt-2 max-w-3xl text-sm text-stone-400">
        Democratizing ethical AI skills across borders—from PhD researchers in India and cinema students in Paris to religious congregations in Rome and Cameroon.
      </p>
    </div>
    <WorkshopExplorer client:load data={workshopsData} />
  </div>
</BaseLayout>
""",
    # =========================================================================
    # 8. ANTIGRAVITY REMOTE-MANAGEMENT PLAYBOOK
    # =========================================================================
    "AGENT_PLAYBOOK.md": r"""# AGENT_PLAYBOOK.md — Remote Management Guide for josephcap.com

This repository powers **https://www.josephcap.com** via **Astro + React Islands + Tailwind CSS**, deployed statically to **GitHub Pages** on every push to `main`.

## 1. Golden Rules for AI Agents (Google Antigravity)
- **Static Only:** Never add SSR adapters, server API routes, or database servers. Everything must compile cleanly with `npm run build` into `dist/`.
- **Always Verify Build Before Pushing:** Run `npm run build` after any JSON/Markdown/component change to confirm zero Astro/TypeScript/schema errors.
- **Preserve `public/CNAME`:** Keep `www.josephcap.com` untouched so custom domain HTTPS never breaks.
- **Liturgical Fidelity:** Preserve the Catholic liturgical disclaimer on Vetrisaipadal (karaoke is for practice/cultural events, not Mass liturgy) and standard Tamil Roman Catholic theological terms (`நற்செய்தி`, `அருளடையாளம்`, `மனித மாண்பு`, `பொதுநலம்`).

## 2. Common Remote Update Recipes

### A. Add a New Vetrisaipadal Karaoke Track
Edit `src/data/vetrisaipadal.json` -> append to `"tracks"`:
```json
{
  "code": "555",
  "title": "தமிழ் பாடல் தலைப்பு",
  "category": "marian",
  "youtubeId": "11_CHAR_YOUTUBE_ID"
}
```

### B. Add or Update an Original Music Album
Edit `src/data/albums.json` -> add album or song object with title, lyrics, YouTube/streaming links.

### C. Add a Film / Cinema Project
Edit `src/data/films.json` -> add film object with title, role, synopsis, and poster/stills.

### D. Add an AI Project / Experiment
Edit `src/data/ai-projects.json` -> add project object with category, description, and link.

### E. Add an AI Literacy Workshop
Edit `src/data/workshops.json` -> add workshop object with organization, location, audience, and topics.

### F. Add a Philosophy or Theology Archive Document
Edit `src/data/archives.json` -> add document object with title, subject, driveId / URL, and year.

### G. Publish a New Theological Article / Writing
Create a new Markdown file in `src/content/writings/<slug>.md` with frontmatter (`title`, `description`, `date`, `language`, `tags`).

## 3. Architecture & Directory Overview
- `src/pages/`: Astro file-based static routing.
- `src/components/react/`: Interactive React client islands (e.g. `client:load` for search/audio/video filters).
- `src/layouts/`: `BaseLayout.astro` and `ReaderLayout.astro`.
- `src/data/`: Structured JSON data files.
- `src/content/`: Content collections defined in `src/content/config.ts`.
- `public/`: Static assets (`CNAME`, images, icons).

## 4. Verification & Deployment
- Run `npm run build` to generate static files in `dist/`.
- Automatic CI/CD workflow in `.github/workflows/deploy.yml` deploys `dist/` to GitHub Pages upon push to `main`.
""",
}


def main():
    for rel_path, content in FILES.items():
        path = ROOT / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"[CREATED] {rel_path}")
    print("\n[DONE] Interactive scaffold created successfully! Run `npm run build` next.")


if __name__ == "__main__":
    main()
