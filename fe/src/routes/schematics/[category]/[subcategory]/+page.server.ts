import { isSubcategory } from "$lib/cat";
import { db } from "$lib/server/db";
import { schematics } from "$lib/server/db/schema";
import { error } from "@sveltejs/kit";
import { and, eq } from "drizzle-orm";

export const load = async ({ params }) => {
    if (!isSubcategory(params.category, params.subcategory)) {
        throw error(404, "Invalid category/subcategory")
    }

    try {
        const result = await db
            .select()
            .from(schematics)
            .where(
                and(
                    eq(schematics.category, params.category),
                    eq(schematics.subcategory, params.subcategory)
                )
            )

        return {
            schematics: result,
            category: params.category,
            subcategory: params.subcategory,
        };
    } catch (err) {
        console.error("Error querying schematics: ", err);
        throw new Error("Failed to fetch schematics");
    }

};
