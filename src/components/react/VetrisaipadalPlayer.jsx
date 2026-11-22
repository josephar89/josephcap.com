import React, { useState, useMemo } from "react";
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
