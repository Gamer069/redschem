import type { InferSelectModel } from "drizzle-orm";
import type { schematics } from "./server/db/schema";

type Category = "arithmetics" | "combinational" | "sequential blocks";
export const categories: readonly Category[] = ["arithmetics", "combinational", "sequential blocks"] as const;

type Subcategory = "adders" | "multipliers" | "dividers" | "squarerooters" | "encoders" | "decoders" | "priority-circuits" | "other-comb" | "latches-flipflops" | "counters" | "registers" | "shift-registers" | "accumulators";
export const subcategories: Readonly<Record<Category, Subcategory[]>> = {
    "arithmetics": [
        "adders", 
        "multipliers", 
        "dividers",
        "squarerooters",
    ] as const,
    "combinational": [
        "encoders",
        "decoders",
        "priority-circuits",
        "other-comb",
    ] as const,
    "sequential blocks": [
        "latches-flipflops",
        "counters",
        "registers",
        "shift-registers",
        "accumulators",
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
