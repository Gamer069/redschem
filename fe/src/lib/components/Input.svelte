<script lang="ts">
	import Button from "./Button.svelte";

    let {
        number = false,
        name = "",
        value = $bindable(),
        extra = "",
        extraInput = "",
		key = "",
        increment = () => {},
        decrement = () => {},
        onInput = (val: number | string) => {}
    } = $props<{
        number?: boolean;
        name?: string;
        value?: number | string;
        extra?: string;
        extraInput?: string;
		key?: string;
        increment?: () => void;
        decrement?: () => void;
        onInput?: (val: number | string) => void;
    }>();

	let htmlInput = $state<HTMLInputElement>();

	export const focus = () => {
		htmlInput?.focus();
	};

	export const unfocus = () => {
		htmlInput?.blur();
	};

	export const focused = () => {
		return htmlInput === document.activeElement;
	}

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

<div class={`flex items-center gap-2 ${extra}`}>
	{#if number}
		<Button text="-" onClick={handleDecrement} />
		<input
			type="number"
			inputmode="numeric"
			pattern="[0-9]*"
			class={`w-16 text-center border rounded px-2 py-1 appearance-none no-spin ${extraInput}`}
			bind:this={htmlInput}
			bind:value
			oninput={handleInput}
		/>

		{#if key}
			<kbd class="absolute right-0 -translate-x-3 pointer-events-none">{key}</kbd>
		{/if}

		<Button text="+" onClick={handleIncrement} />
	{:else}
		<input
			type="text"
			class={`border rounded px-2 py-1 ${extraInput}`}
			bind:this={htmlInput}
			bind:value
			oninput={handleInput}
		/>

		{#if key}
			<kbd class="absolute right-0 -translate-x-3 pointer-events-none">{key}</kbd>
		{/if}
	{/if}

	<input type="hidden" name={name} value={value}/>
</div>
