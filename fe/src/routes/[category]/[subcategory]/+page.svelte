<script lang="ts">
    import type { PageProps } from './$types'
    import Schematic from '$lib/components/Schematic.svelte';

    export let data: PageProps;
</script>

<p>{data.category}#{data.subcategory}</p>
<br>

<div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4 p-4 mx-auto">
    {#each data.schematics as schematic}
        <div class="schem-card min-w-0 mx-auto">
            <Schematic schematic={schematic}/>
        </div>
    {/each}
</div>
