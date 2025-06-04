<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from "$app/state";
	import type { Conversation } from '$lib/server/db/schema';

	type Props = {
		conversation: Conversation;
	};

	let { conversation }: Props = $props();

	let isEditing = $state(false);
	let name = $state(conversation.name);

	let isCurrent = $derived(conversation.id == page.params.id)

	const handleCancel = () => {
		isEditing = false;
		name = conversation.name;
	};


	function handleEnhance() {
		return async () => {
			isEditing = false
		};
	}

	const handleKeydown = (e: KeyboardEvent) => {
		if (e.key === 'Escape') {
			handleCancel();
		}
	};

</script>

<li class="py-1 flex items-center gap-1 justify-between">
	{#if isEditing}
		<form
			method="POST"
			action={`/chat/${conversation.id}?/updateNameConversation`}
			use:enhance={handleEnhance}
			class="flex gap-1 items-center flex-1"
		>
			<input
				type="hidden"
				value={conversation.id}
				name="id"
			/>
			<input
				bind:value={name}
				class="w-full bg-transparent border-b border-gray-300 focus:outline-none focus:border-blue-500"
				name="name"
				onkeydown={handleKeydown}
				autofocus
				required
				minlength="1"
				maxlength="100"
			/>
			<div class="flex gap-1">
				<button
					type="submit"
					aria-label="Confirmer"
					class="text-green-600 hover:text-green-800 transition-colors"
				>
					<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 14 14">
						<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
							<path d="m4 8l2.05 1.64a.48.48 0 0 0 .4.1a.5.5 0 0 0 .34-.24L10 4"/>
							<circle cx="7" cy="7" r="6.5"/>
						</g>
					</svg>
				</button>
				<button
					type="button"
					onclick={handleCancel}
					aria-label="Annuler"
					class="text-gray-500 hover:text-gray-700 transition-colors"
				>
					<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
						<path fill="currentColor" d="M6.4 19L5 17.6l5.6-5.6L5 6.4L6.4 5l5.6 5.6L17.6 5L19 6.4L13.4 12l5.6 5.6L17.6 19L12 13.4z"/>
					</svg>
				</button>
			</div>
		</form>
	{:else}
		<a
			href={`/chat/${conversation.id}`}
			class={isCurrent ? "block text-blue-600 flex-1 truncate" : "block hover:text-blue-600 transition-colors flex-1 truncate"}
		>
			{name}
		</a>
		<div class="flex gap-1">
			<button
				aria-label="Éditer"
				onclick={() => { isEditing = true; name = conversation.name; }}
				class="text-emerald-500 hover:text-emerald-700 transition-colors"
			>
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
					<path fill="currentColor" d="M4 21q-.425 0-.712-.288T3 20v-2.425q0-.4.15-.763t.425-.637L16.2 3.575q.3-.275.663-.425t.762-.15t.775.15t.65.45L20.425 5q.3.275.437.65T21 6.4q0 .4-.138.763t-.437.662l-12.6 12.6q-.275.275-.638.425t-.762.15zM17.6 7.8L19 6.4L17.6 5l-1.4 1.4z"/>
				</svg>
			</button>
			<form
				method="POST"
				action={`/chat/${conversation.id}?/deleteConversation`}
				use:enhance={handleEnhance}
				class="m-0 p-0 flex items-center justify-center"
			>
				<button
					aria-label="Supprimer"
					class="text-red-700 hover:text-red-900 transition-colors"
				>
					<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
						<path fill="currentColor" d="M7.616 20q-.667 0-1.141-.475T6 18.386V6h-.5q-.213 0-.356-.144T5 5.499t.144-.356T5.5 5H9q0-.31.23-.54t.54-.23h4.46q.31 0 .54.23T15 5h3.5q.213 0 .356.144t.144.357t-.144.356T18.5 6H18v12.385q0 .666-.475 1.14t-1.14.475zm2.692-3q.213 0 .357-.144t.143-.356v-8q0-.213-.144-.356T10.307 8t-.356.144t-.143.356v8q0 .213.144.356q.144.144.356.144m3.385 0q.213 0 .356-.144t.143-.356v-8q0-.213-.144-.356Q13.904 8 13.692 8q-.213 0-.357.144t-.143.356v8q0 .213.144.356t.357.144"/>
					</svg>
				</button>
			</form>
		</div>
	{/if}
</li>