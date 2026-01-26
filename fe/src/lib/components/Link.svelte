<script lang="ts">
	const { href, children } = $props();
</script>

<a href={href} class="hover:scale-110 inline-block transition-transform duration-200 ease-[cubic-bezier(0.85, 0.05, 0.15, 0.95)]">{@render children?.()}</a>
