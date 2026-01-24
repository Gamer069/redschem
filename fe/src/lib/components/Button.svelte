<script lang="ts">
    import { onDestroy, onMount } from "svelte";
    import Page from "../../routes/+page.svelte";

	let { 
		text,
		extra,
		extraBtn = "",
		extraText,
		onClick,
		formaction,
		type,
		transition = true,
		disabled = false,
		tooltip = "",
        minWidth = "0",
	}: {
		text: string,
		extra: string,
		extraBtn: string,
		extraText: string,
		onClick: () => void,
		formaction: string,
		type: "button" | "submit" | "reset",
		transition: boolean,
		disabled: boolean,
		tooltip: string,
        minWidth: string
	} = $props();

	let tooltipShown = $state(false);
	let btn: HTMLButtonElement;

	const handleClick = (e: PointerEvent) => {
		if (!btn) return;
		if (disabled && tooltip) {
			const touch = e.target as Node;

			if (btn.contains(touch)) {
				tooltipShown = true;
				setTimeout(() => tooltipShown = false, 2000);
			}
		}
	}
</script>

<div class="{extra}" onpointerup={handleClick}>
	<button
		type={type}
		formaction={formaction}
		bind:this={btn}
		onclick={onClick}
		onmouseenter={(_e) => tooltipShown = true}
		onmouseleave={(_e) => tooltipShown = false}
		disabled={disabled}
		class={`transform ${transition ? 'transition-transform hover:scale-94 duration-300' : ''} ease-[cubic-bezier(0.85, 0.05, 0.15, 0.95)] rounded-xl disabled:pointer-events-auto disabled:cursor-not-allowed px-4 py-2 bg-[#74c7ec] disabled:bg-[#a6adc8] hover:bg-[#89b4fa] focus:bg-[#89dceb] ${extraBtn}`}
        style="min-width: {minWidth};"
	>
		{text}
		<p class="text-sm text-[#313244] font-bold">{extraText}</p>
	</button>

	{#if disabled && tooltip && tooltipShown}
		<span class="absolute right-10 bg-[#11111b] text-white text-xs rounded-md px-2 py-1 whitespace-nowrap opacity-100 pointer-events-none z-50 bottom-20">
		{tooltip}
		</span>
	{/if}
</div>
