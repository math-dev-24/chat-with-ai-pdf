<script lang="ts">
	import type { ChatMessage } from '$lib/types';
	import Loader from "./loader.svelte";

	interface Props {
		dialog: ChatMessage[];
		inLoading: boolean
	}

	let { dialog, inLoading }: Props = $props();
</script>

<div
	class=" bg-white/60 backdrop-blur-sm rounded-2xl border border-slate-200/50 shadow-sm mb-6 flex flex-col h-4/5">
	<div class="flex-1 overflow-y-auto p-6 space-y-4">
		{#each dialog as message, index (index)}
			<div
				class="flex { (message.role === 'system' || message.role === 'assistant') ? 'justify-start' : 'justify-end'}"
			>
				<div
					class="px-4 py-3 rounded-2xl border backdrop-blur-sm min-w-1/3 {(message.role === 'system' || message.role === 'assistant')
            ? 'bg-purple-100/70 text-purple-800 border-purple-200/50'
            : 'bg-blue-100/70 text-blue-800 border-blue-200/50'}"
				>
					<div class="text-xs font-medium opacity-60 mb-1 capitalize">{message.role}</div>
					<div class="text-sm leading-relaxed">{@html message.message}</div>
				</div>
			</div>
		{/each}
		{#if inLoading}
			<Loader />
		{/if}
	</div>
</div>