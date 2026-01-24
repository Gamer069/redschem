<script lang="ts">
    import type { Schematic } from "$lib/cat";
    import pako from "pako";
	import Button from "./Button.svelte";

    let { schematic } = $props();

    const decodeGzipBase64 = (b64Gzip: string): Uint8Array => {
        const compressedBytes = Uint8Array.from(atob(b64Gzip), c => c.charCodeAt(0));

        return pako.ungzip(compressedBytes);
    };

    const decodeGzipBase64Image = (b64Gzip: string, mimeType = 'image/png'): { bytes: Uint8Array, dataUrl: string } => {
        const compressedBytes = Uint8Array.from(atob(b64Gzip), c => c.charCodeAt(0));
        const bytes = pako.ungzip(compressedBytes);
        let binary = '';
        const chunkSize = 0x8000;
        for (let i = 0; i < bytes.length; i += chunkSize) {
            binary += String.fromCharCode(...bytes.subarray(i, i + chunkSize));
        }
        return { bytes, dataUrl: `data:${mimeType};base64,${btoa(binary)}` };
    };


    // svelte-ignore state_referenced_locally
    const { bytes: imageBytes, dataUrl: image } = decodeGzipBase64Image(schematic.image);

    // svelte-ignore state_referenced_locally
    const extraData =
        schematic.extra_data !== null
        ? new TextDecoder()
            .decode(decodeGzipBase64(schematic.extra_data))
        : null;

    let showExtraDataState = $state(false);

    // svelte-ignore state_referenced_locally
    const schem = decodeGzipBase64(schematic.schem);

    const downloadFile = (data: Uint8Array | string, filename: string, mimeType = "text/plain") => {
        const blob = new Blob([data], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
    };

    // Usage:
    const downloadExtraData = () => downloadFile(
        extraData,
        `${schematic.title.replace(/\s+/g, "_")}_extra.txt`
    );

    const downloadImage = () => downloadFile(
        imageBytes,
        `${schematic.title.replace(/\s+/g, "_")}_image.png`,
        "image/png"
    );

    const downloadSchematic = () => downloadFile(
        schem,
        `${schematic.title.replace(/\s+/g, "_")}_schem.schem`
    );

    const showExtraData = () => {
        showExtraDataState = !showExtraDataState;
    };
</script>

<div class="schematic bg-base rounded-xl border-text border w-90 p-4 flex flex-col min-h-[450px]">
    <div class="flex-shrink-0">
        <p>{schematic.title}</p>
        <p>By: {schematic.authors}</p>
    </div>

    <div class="flex-shrink-0 flex items-center justify-center my-2">
        <img src={image} class="scale-120" alt={`Schematic for ${schematic.title} by ${schematic.authors}`}/>
    </div>

    <div class="flex-grow"></div>

    <div class="controls flex flex-col gap-2 mt-2">
        {#if extraData !== null}
            <div class="flex gap-2 w-max">
                <Button onClick={showExtraData} text="Toggle Data"/>
                <Button onClick={downloadExtraData} text="Download Data"/>
            </div>
            {#if showExtraDataState}
                <pre class="overflow-auto rounded-xl bg-surface0 p-2 text-sm text-text font-mono max-h-[calc(8*1.5rem)]">
<code>{extraData}</code>
                </pre>
            {/if}
        {/if}


        <Button onClick={downloadImage} minWidth="330px" text="Download Preview Image"/>
        <Button onClick={downloadSchematic} minWidth="330px" text="Download .schem file"/>
    </div>
</div>
