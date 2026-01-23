import { pgTable, serial, text } from 'drizzle-orm/pg-core';

export const schematics = pgTable('schematics', {
    id: serial('id').primaryKey(),
    category: text('category').notNull(),
    subcategory: text('subcategory').notNull(),
    image: text('image').notNull(),
    schem: text('schem').notNull(),
    title: text('title').notNull(),
    authors: text('authors').array().notNull(),
    description: text('description').notNull(),
    input: text('input'),
    output: text('output'),
    speed: text('speed'),
    notes: text('notes'),
    extra_data: text('extra_data'),
});

