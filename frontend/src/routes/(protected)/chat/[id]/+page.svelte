<script lang="ts">
	import MainChat from '$lib/components/chat/main-chat.svelte';
	import InputChat from '$lib/components/chat/input-chat.svelte';
	import CardConv from '$lib/components/chat/conversation/card.svelte';
	import * as Card from "$lib/components/ui/card/index.js";


	import type { StateChat } from '$lib/types';
	import { Button } from '$lib/components/ui/button';
	import { User } from 'lucide-svelte';
	let { data } = $props();

	let stateChat = $state<StateChat>({
		answer: "",
		inLoading: false,
		context: [],
		errors: [],
		showContext: false
	});

	function toggleContext() {
		stateChat.showContext = !stateChat.showContext;
	}


</script>

<svelte:head>
	<title>Chat : { data.actual_conversation.name}</title>
</svelte:head>

<section class="grid grid-cols-6 gap-4 h-[85vh]">

	<Card.Root class="flex flex-col">
		<Card.Header>
			<Card.Title>Mes conversations :</Card.Title>
		</Card.Header>
		<Card.Content class="flex-1">
			<ul>
				{#each data.list_conversations as conversation (conversation.id)}
					<CardConv conversation={conversation} />
				{/each}
			</ul>
		</Card.Content>
		<Card.Footer>
			<Button class="gap-2" variant="outline" href="/profil">
				<User />
				<span>{data.user ? data.user.username : "inconnu"}</span>
			</Button>
		</Card.Footer>
	</Card.Root>

	<section class="col-span-5">
		<MainChat
			name={data.actual_conversation.name}
			messages={data.actual_conversation.messages}
			inLoading={stateChat.inLoading}
		/>

		<InputChat
			answer={stateChat.answer}
			inLoading={stateChat.inLoading}
			error={stateChat.errors[0] || ''}
			showContext={stateChat.showContext}
			onToggleContext={toggleContext}
		/>
	</section>
</section>