<script lang="ts">
	import { onMount } from "svelte";
	import type { PageProps } from "../$types";
	import Input from "$lib/components/Input.svelte";
	import Button from "$lib/components/Button.svelte";
	import { map } from "$lib/cat";
	import { goto } from "$app/navigation";
	import { page } from "$app/state";

    const { data } = $props<{ data: PageProps }>();
	const fields = $derived(data.fields);

	let values: Record<string, string> = $state({});
	let generated = $state("");

	const upd = (field, val) => {
		values[field.name] = val;
		refresh();
	}

	const refresh = () => {
		generated = "";

		Object.entries(values).forEach(([k, v]) => {
			const field = fields.filter(field => field.name === k)[0];

			if (v.length !== 0) {
				generated += map[k] ?? k[0].toUpperCase() + k.slice(1);

				generated += ": ";

				generated += v;

				generated += "\n";
			} else if (!field.optional) {
				generated += map[k] ?? k[0].toUpperCase() + k.slice(1);

				generated += ": ";

				generated += "<value not provided>";

				generated += "\n";
			}
		});
	}

	const copy = () => {
		if (!generated) return;

		let copied = `\`\`\`${generated.trimEnd()}\`\`\``;

		navigator.clipboard.writeText(copied)
			.then(() => {
				console.log("Copied!");
			})
			.catch(err => {
				console.error("Failed to copy:", err);
			});
	}

	const home = () => {
		goto("/");
	}

	const back = () => {
		// strip last /.*
		goto(page.url.toString().replace(/\/[^/]*$/, ""));
	};

	const generate = () => {
		goto("/generate");
	}

	onMount(() => {
		refresh();
	})
</script>

<div class="p-4 flex flex-col gap-4 min-w-screen">
	<div class="flex gap-4 float-left">
		<Button onClick={back} icon text="arrow_back"/>
		<Button onClick={generate} icon text="build"/>
		<Button onClick={home} icon text="home"/>
	</div>

	<div class="flex gap-4">
		<div class="grid gap-3">
			{#each fields as field}
				<Input nameText={field.optional ? field.name[0].toUpperCase() + field.name.slice(1) : field.name[0].toUpperCase() + field.name.slice(1) + "*"} bind:value={values[field.name]} onInput={(val) => upd(field, val)} extraInput="flex-1" textClass="w-32 shrink-0"></Input>
			{/each}
		</div>

		<pre class="flex-1 max-w-full border border-ctp-text whitespace-pre-wrap overflow-auto break-words rounded-xl bg-ctp-surface0 p-2 text-sm text-text font-mono"><code>{generated}</code></pre>
	</div>

	<Button text="Copy to clipboard" extraBtn="w-full" onClick={copy}/>
</div>
