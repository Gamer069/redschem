import { categories } from "$lib/cat";
import type { PageLoad } from "./$types";


export const load: PageLoad = ({ params }) => {
    if (categories.includes(params.category)) {
    }
};

