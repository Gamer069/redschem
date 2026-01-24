<script lang="ts">
    import type { PageProps } from './$types'
    import Schematic from '$lib/components/Schematic.svelte';
    import Input from '$lib/components/Input.svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';

    const { data } = $props<{ data: PageProps }>();

    const refreshRoute = async (e: Event) => {
        e.preventDefault();
        await goto(page.url, { replaceState: true });
    };
</script>

<div class="relative min-h-screen p-4">
    <Input value="" extra="rounded-lg float-right" extraInput="bg-text"></Input>
    <br>
    <br>

    {#if data.schematics.length === 0}
        <div class="flex flex-col items-center justify-center h-64 text-center text-gray-400">
            <p class="text-lg font-medium mb-2">No schematics found in this category</p>
            <p class="text-sm">Try <a href={page.url} on:click={refreshRoute}>refreshing</a> the page to see if new schematics have been added.</p>
        </div>
    {:else}
        <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4 p-4 mx-auto">
            {#each data.schematics as schematic}
                <div class="schem-card min-w-0 mx-auto">
                    <Schematic schematic={schematic}/>
                </div>
            {/each}
        </div>
    {/if}
</div>
