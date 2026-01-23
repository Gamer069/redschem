<script lang="ts">
	import Button from "./Button.svelte";

	export let number: boolean = false;
	export let name: string = "";
	export let value: number | string = 0;
	export let increment: () => void = () => {};
	export let decrement: () => void = () => {};
	export let onInput: (val: number | string) => void = (val: number | string) => {};
	
	const handleInput = (e: Event) => {
		const target = e.target as HTMLInputElement;
		value = number ? parseInt(target.value) : target.value; 
		onInput(value);
	};

	const handleIncrement = () => {
		increment();
	};

	const handleDecrement = () => {
		decrement();
	};
</script>

<div class="flex items-center gap-2">
	{#if number}
		<Button text="-" onClick={handleDecrement} />
		<input
			type="number"
			inputmode="numeric"
			pattern="[0-9]*"
			class="w-16 text-center border rounded px-2 py-1 appearance-none no-spin"
			bind:value
			on:input={handleInput}
		/>
		<Button text="+" onClick={handleIncrement} />
	{:else}
		<input
			type="text"
			class="border rounded px-2 py-1"
			bind:value
			on:input={handleInput}
		/>
	{/if}

	<input type="hidden" name={name} value={value}/>
</div>
