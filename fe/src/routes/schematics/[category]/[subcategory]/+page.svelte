<script lang="ts">
    import type { PageProps } from './$types'
    import Schematic from '$lib/components/Schematic.svelte';
    import Input from '$lib/components/Input.svelte';
    import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { onDestroy, onMount } from 'svelte';

    const { data } = $props<{ data: PageProps }>();

    const refreshRoute = async (e: Event) => {
        e.preventDefault();
        await goto(page.url, { replaceState: true });
    };

    let search = $state("");
    
    // Create a stable map of schematics by id
    const schematicsMap = new Map(
        data.schematics.map(s => [s.id, s])
    );
    
    // Store only the keys, not the objects themselves
    let resultKeys: string[] = $state(data.schematics.map(s => s.id));
    
    // Derive the actual results from the stable map
    let results = $derived(resultKeys.map(key => schematicsMap.get(key)!));
    
    let worker: Worker | null = null;

    onMount(() => {
        worker = new Worker(new URL("$lib/workers/search.worker.ts", import.meta.url), {
            type: "module"
        });

        worker.onmessage = (e: MessageEvent) => {
            const { type, payload } = e.data;
            if (type === "results") {
                // Update only the keys, objects stay the same
                resultKeys = payload.map((s: any) => s.id);
            }
        };

        worker.postMessage({ type: "init", payload: data.schematics });
    });

    onDestroy(() => {
        worker?.terminate();
    });

    const doSearch = () => {
        if (worker !== null) {
            worker.postMessage({ type: "search", payload: search });
        }
    };
</script>

<div class="relative min-h-screen p-4">
    <Input bind:value={search} extra="rounded-lg float-right" extraInput="bg-ctp-text" onInput={doSearch}></Input>
    <br>
    <br>

    {#if data.schematics.length === 0 || (search.length !== 0 && results.length === 0)}
        <div class="flex flex-col items-center justify-center h-64 text-center text-gray-400">
            {#if search.length !== 0 && results.length === 0}
                <p class="text-lg font-medium mb-2">No schematics found with the specified search query.</p>
            {:else}
                <p class="text-lg font-medium mb-2">No schematics found in this category.</p>
            {/if}
            <p class="text-sm">Try <a href={page.url} onclick={refreshRoute}>refreshing</a> the page &ndash; new schematics may have been added!</p>
        </div>
    {:else}
        <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4 p-4 mx-auto">
            {#each results as schematic (schematic.id)}
                <div class="schem-card min-w-0 mx-auto">
                    <Schematic schematic={schematic}/>
                </div>
            {/each}
        </div>
    {/if}
</div>
