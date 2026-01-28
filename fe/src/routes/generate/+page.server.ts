import type { Field } from "$lib/cat";
import { schematics } from "$lib/server/db/schema";

export const load = ({ params }): { fields: Field[] } => {
	let fields = Object.entries(schematics)
		.filter(([name]) => !['id', 'schem', 'image', 'category', 'subcategory', 'extra_data', 'enableRLS'].includes(name))
		.map(([name, col]) => ({
			name,
			optional: !col.notNull && col.default === undefined,
			type: col.dataType ?? "string",
		}));

	return {
		fields,
	}
};
