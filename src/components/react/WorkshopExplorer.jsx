import React, { useState, useMemo } from "react";
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
