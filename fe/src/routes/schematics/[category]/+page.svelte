<script lang="ts">
    import type { PageProps } from './$types'
	import { goto } from "$app/navigation";
    import { subcategories, type Subcategory, categories } from "$lib/cat";
	import Button from '$lib/components/Button.svelte';
	import { page } from '$app/state';

    export let data: PageProps;

    const gotoSubcat = (subcategory: Subcategory) => {
        goto("/schematics/" + data.category + "/" + subcategory);
    }

    const newSubcategories = subcategories[data.category];

	// in this case home and back are the same but we should keeep two buttons to ensure good UX
	const home = () => {
		goto("/");
	}

	const back = () => {
		goto("/");
	};
</script>

<div class="relative min-h-screen p-3">
	<div class="flex gap-4 absolute top-3 left-3 z-10">
		<Button onClick={back} icon text="arrow_back"/>
		<Button onClick={home} icon text="home"/>
	</div>

	<div class="flex items-center justify-center min-h-screen">
		<div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4 p-4 mx-auto squares">
			{#each newSubcategories as subcategory}
				<button class="square bg-ctp-base w-80 h-60 rounded-xl border-2 border-ctp-text p-4 transition-transform duration-200 hover:scale-90" onclick={() => gotoSubcat(subcategory)}>
					<p class="text-2xl">{subcategory}</p>
				</button>
			{/each}
		</div>
	</div>
</div>
