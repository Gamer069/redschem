<script lang="ts">
	import { goto } from "$app/navigation";
    import { type Category, categories } from "$lib/cat";

    const gotoCat = (category: Category) => {
        goto("/schematics/" + category);
    }
</script>

<div class="flex items-center justify-center min-h-screen">
    <div class="grid squares gap-8">
        {#each categories as category}
            <button class="square bg-ctp-base w-80 h-60 rounded-xl border-2 border-ctp-text p-4 transition-transform duration-200 hover:scale-90" onclick={() => gotoCat(category)}>
                <p class="text-2xl">{category}</p>
            </button>
        {/each}
    </div>
</div>
