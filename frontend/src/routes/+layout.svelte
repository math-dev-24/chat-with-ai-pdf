<script lang="ts">
	import '../app.css';
	import FlashMessage from '$lib/components/flash-message.svelte';
	import { ModeWatcher } from "mode-watcher";
	import ModeToggle from '$lib/components/ModeToggle.svelte';
	import { Button } from '$lib/components/ui/button';
	import { ArrowRight, Bot } from 'lucide-svelte';
	import type {LayoutProps} from "./$types";


	let { children, data }: LayoutProps = $props();
</script>



<FlashMessage
	flashMessage={data.flashMessage}
/>

<ModeWatcher />

{@render children()}
