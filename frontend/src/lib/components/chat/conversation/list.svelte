<script lang="ts">
	import type { Conversation } from '$lib/server/db/schema';
	import CardConv from "./card.svelte";

	type Props = {
		list: Conversation[]
	}

	let { list }: Props = $props();


</script>


{#each list as conversation (conversation.id)}
	<CardConv
		conversation={conversation}
	/>
{/each}