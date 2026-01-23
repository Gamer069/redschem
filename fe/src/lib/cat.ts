import type { InferSelectModel } from "drizzle-orm";
import type { schematics } from "./server/db/schema";

type Category = "arithmetics"; // TODO: add more categories
export const categories: readonly Category[] = ["arithmetics"] as const;

type Subcategory = "add" | "mul" | "div";
export const subcategories: Readonly<Record<Category, Subcategory[]>> = {
    "arithmetics": [
        "add", 
        "mul", 
        "div"
    ] as const,
} as const;

export type Schematic = InferSelectModel<typeof schematics>;
 
export const isCategory = (value: string): value is Category => {
    return (categories as readonly string[]).includes(value)
}

export const isSubcategory = (category: string, value: string): value is Subcategory => {
    if (!isCategory(category)) return false;
    return subcategories[category].includes(value as Subcategory);
}
