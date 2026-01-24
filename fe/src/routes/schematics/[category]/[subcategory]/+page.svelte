<script lang="ts">
    import type { PageProps } from './$types'
    import Schematic from '$lib/components/Schematic.svelte';
    import Input from '$lib/components/Input.svelte';

    const { data } = $props<{ data: PageProps }>();
</script>

<div class="relative min-h-screen p-4">
    <Input value="" extra="rounded-lg float-right" extraInput="bg-text"></Input>
    <br>
    <br>

    <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4 p-4 mx-auto">
        {#each data.schematics as schematic}
            <div class="schem-card min-w-0 mx-auto">
                <Schematic schematic={schematic}/>
            </div>
        {/each}
    </div>
</div>
