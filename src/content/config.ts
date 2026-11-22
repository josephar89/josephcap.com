import { defineCollection, z } from "astro:content";

const magnificaHumanitas = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    order: z.number(),
    prev: z.string().nullable().optional(),
    next: z.string().nullable().optional(),
  }),
});

const seraphicWay = defineCollection({
  type: "content",
  schema: z.object({
    langCode: z.string(),
    englishName: z.string(),
    nativeName: z.string(),
    title: z.string(),
    aiTranslated: z.boolean().optional().default(false),
    needsReview: z.boolean().optional().default(false),
  }),
});

const writings = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    language: z.string().optional().default("Tamil"),
    category: z.string().optional(),
  }),
});

export const collections = {
  "magnifica-humanitas": magnificaHumanitas,
  "seraphic-way": seraphicWay,
  writings,
};
