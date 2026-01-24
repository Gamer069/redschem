import { isCategory } from "$lib/cat";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = ({ params }) => {
    if (isCategory(params.category)) {
        return {
            category: params.category
        }
    }

    throw error(404, "Invalid category")
}
