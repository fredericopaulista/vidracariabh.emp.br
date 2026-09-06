import { defineCollection, z } from 'astro:content';

// Blog do Link Flow — o blog-publicar grava .md aqui com este frontmatter.
const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    draft: z.boolean().default(true),
    heroImage: z.string().optional(),
    cluster: z.string().optional(),
    moneyPage: z.string().optional(),
  }),
});

export const collections = { blog };
