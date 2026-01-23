<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<title>Logical Redstone Schematics</title>

<div class="min-w-screen min-h-screen bg-mantle">
    {@render children()}
</div>
