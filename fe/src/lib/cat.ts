import subcategories from "../../../shared/categories.json";

export { subcategories, type Field };

export const categories = Object.keys(subcategories) as (keyof typeof subcategories)[];

import type { InferSelectModel } from "drizzle-orm";
import type { schematics } from "./server/db/schema";

/** Single source of truth */
/** Derived types */
export type Category = keyof typeof subcategories;

export type Subcategory =
	(typeof subcategories)[Category][number];

interface Field {
	name: string;
	optional: boolean;
	type: string;
}

/** Drizzle type */
export type Schematic = InferSelectModel<typeof schematics>;

/** Type guards */
export const isCategory = (value: string): value is Category => {
	return value in subcategories;
};

export const isSubcategory = (
	category: string,
	value: string
): value is Subcategory => {
	if (!isCategory(category)) return false;
	return (subcategories[category] as readonly string[]).includes(value);
};

export const map = { authors: "Author" };
