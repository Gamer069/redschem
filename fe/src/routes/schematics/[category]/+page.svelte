<script lang="ts">
    import type { PageProps } from './$types'
	import { goto } from "$app/navigation";
    import { subcategories, type Subcategory, categories } from "$lib/cat";

    export let data: PageProps;

    const gotoSubcat = (subcategory: Subcategory) => {
        goto("/schematics/" + data.category + "/" + subcategory);
    }

    const newSubcategories = subcategories[data.category];
</script>

<div class="flex items-center justify-center min-h-screen">
    <div class="grid squares gap-8">
        {#each newSubcategories as subcategory}
            <button class="square bg-base w-80 h-60 rounded-xl border-2 border-text p-4 transition-transform duration-200 hover:scale-90" onclick={() => gotoSubcat(subcategory)}>
                <p class="text-2xl">{subcategory}</p>
            </button>
        {/each}
    </div>
</div>
