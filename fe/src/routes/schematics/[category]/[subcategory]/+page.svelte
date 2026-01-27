<script lang="ts">
    import type { PageProps } from './$types'
    import Schematic from '$lib/components/Schematic.svelte';
    import Input from '$lib/components/Input.svelte';
    import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { onDestroy, onMount } from 'svelte';
	import Link from '$lib/components/Link.svelte';
	import Button from '$lib/components/Button.svelte';

    const { data } = $props<{ data: PageProps }>();

    const refreshRoute = async (e: Event) => {
        e.preventDefault();
        await goto(page.url, { replaceState: true });
    };

    let search = $state("");
	let searchInp: Input;
    
    // Create a stable map of schematics by id
    const schematicsMap = $derived(new Map(
        data.schematics.map(s => [s.id, s])
    ));
    
    // Store only the keys, not the objects themselves
    let resultKeys: string[] = $state([]);

    $effect(() => {
        resultKeys = data.schematics.map(s => s.id);
    });
    
    // Derive the actual results from the stable map
    let results = $derived(resultKeys.map(key => schematicsMap.get(key)!));
    
    let worker: Worker | null = null;

	const handleKey = (e: KeyboardEvent) => {
		if (searchInp.focused() && e.key === "Escape") searchInp.unfocus();
		if (searchInp.focused()) return;

		if (e.key === "k" || e.key === "/") {
			e.preventDefault();
			searchInp.focus();
		}
	};

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

		window.addEventListener("keydown", handleKey);

		return () => window.removeEventListener("keydown", handleKey);
    });

    onDestroy(() => {
        worker?.terminate();
    });

    const doSearch = () => {
        if (worker !== null) {
            worker.postMessage({ type: "search", payload: search });
        }
    };

	const home = () => {
		goto("/");
	}

	const back = () => {
		// strip last /.*
		goto(page.url.toString().replace(/\/[^/]*$/, ""));
	};
</script>


<div class="relative min-h-screen p-3">
	<div class="flex gap-4 float-left">
		<Button onClick={back} icon text="arrow_back"/>
		<Button onClick={home} icon text="home"/>
	</div>

    <Input bind:this={searchInp} bind:value={search} extra="rounded-lg float-right" extraInput="bg-ctp-text" onInput={doSearch} key="/"></Input>
    <br>
    <br>
    <br>

    {#if data.schematics.length === 0 || (search.length !== 0 && results.length === 0)}
        <div class="flex flex-col items-center justify-center h-64 text-center text-gray-400">
            {#if search.length !== 0 && results.length === 0}
                <p class="text-lg font-medium mb-2">No schematics found with the specified search query.</p>
            {:else}
                <p class="text-lg font-medium mb-2">No schematics found in this category.</p>
            {/if}
            <p class="text-sm">Try <Link href={page.url} onclick={refreshRoute}>refreshing</Link> the page &ndash; new schematics may have been added!</p>
        </div>
    {:else}
		<div class="grid gap-4 p-4 mx-auto [grid-template-columns:repeat(auto-fit,minmax(380px,1fr))]">
            {#each results as schematic (schematic.id)}
                <div class="schem-card min-w-0 mx-auto">
                    <Schematic schematic={schematic}/>
                </div>
            {/each}
        </div>
    {/if}
</div>
