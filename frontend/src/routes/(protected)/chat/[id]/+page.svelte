<script lang="ts">
	import MainChat from '$lib/components/chat/main-chat.svelte';
	import InputChat from '$lib/components/chat/input-chat.svelte';
	import ListConversation from '$lib/components/chat/conversation/list.svelte'

	import type { StateChat } from '$lib/types';
	let { data } = $props();

	let stateChat = $state<StateChat>({
		answer: "",
		inLoading: false,
		context: [],
		dialog: data.actual_conversation.messages,
		errors: [],
		showContext: false
	});

	function toggleContext() {
		stateChat.showContext = !stateChat.showContext;
	}

	$effect(() => {
		stateChat.dialog = data.actual_conversation.messages;
	});

</script>

<svelte:head>
	<title>Chat : { data.actual_conversation.name}</title>
</svelte:head>
<section class="grid grid-cols-6 gap-4 h-[88vh]">
	<aside class="card py-2 px-4">
		<ul>
			<li>Mes conversations :</li>
			<ListConversation
				list={data.list_conversations}
			/>
		</ul>
	</aside>
	<div class="col-span-5 flex-1 flex flex-col">
		<MainChat
			dialog={stateChat.dialog}
			inLoading={stateChat.inLoading}
		/>

		<InputChat
			answer={stateChat.answer}
			inLoading={stateChat.inLoading}
			error={stateChat.errors[0] || ''}
			showContext={stateChat.showContext}
			onToggleContext={toggleContext}
		/>
	</div>
</section>