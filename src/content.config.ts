import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    year: z.number(),
    role: z.string(),
    kind: z.string(),
    summary: z.string(),
    overview: z.string(),
    problem: z.string(),
    solution: z.string(),
    stack: z.array(z.string()),
    learnings: z.string(),
    featured: z.boolean().default(false),
    order: z.number(),
    codeUrl: z.string().url(),
    codePending: z.boolean().default(false),
    demoUrl: z.string().url().optional(),
    demoNote: z.string().optional(),
    architecture: z.string().optional(),
    architectureInteractive: z.boolean().default(false),
    screenshots: z.array(z.object({ path: z.string(), alt: z.string() })),
  }),
});

export const collections = { projects };
