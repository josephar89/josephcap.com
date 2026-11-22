import React, { useState } from "react";
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
