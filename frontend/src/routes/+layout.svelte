<script lang="ts">
	import '../app.css';
	import FlashMessage from '$lib/components/flash-message.svelte';
	import type {LayoutProps} from "./$types";


	let { children, data }: LayoutProps = $props();
</script>


<FlashMessage
	flashMessage={data.flashMessage}
/>


{@render children()}