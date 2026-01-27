<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>Logical Redstone Schematics</title>
</svelte:head>

<div class="min-w-screen min-h-screen bg-ctp-mantle">
    {@render children()}
</div>
