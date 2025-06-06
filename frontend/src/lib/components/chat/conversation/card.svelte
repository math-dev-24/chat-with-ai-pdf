<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from '$app/state';
	import type { Conversation } from '$lib/server/db/schema';

	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Check, Pencil, Trash2, X } from 'lucide-svelte';
	import { cn } from '$lib/utils';

	type Props = {
		conversation: Conversation;
	};

	let { conversation }: Props = $props();

	let isEditing = $state(false);
	let name = $state(conversation.name);

	let isCurrent = $derived(conversation.id == page.params.id);

	const handleCancel = () => {
		isEditing = false;
		name = conversation.name;
	};


	const handleKeydown = (e: KeyboardEvent) => {
		if (e.key === 'Escape') {
			handleCancel();
		}
	};
</script>

<li class="py-2 flex items-center gap-2 justify-between group hover:bg-muted/50 px-2 rounded-md transition-colors">
	{#if isEditing}
		<form
			method="POST"
			action={`/chat/${conversation.id}?/updateNameConversation`}
			use:enhance={() => {
				isEditing = true;
				return async ({update}) => {
					await update();
					isEditing = false;
				};
			}}
			class="flex gap-2 items-center flex-1"
		>
			<input
				type="hidden"
				value={conversation.id}
				name="id"
			/>
			<Input
				bind:value={name}
				name="name"
				onkeydown={handleKeydown}
				autofocus
				required
				class="flex-1"
				placeholder="Nom de la conversation"
			/>
			<div class="flex gap-1">
				<Button
					type="submit"
					size="sm"
					variant="ghost"
					class="h-8 w-8 p-0 text-green-600 hover:text-green-700 hover:bg-green-100"
					aria-label="Confirmer"
				>
					<Check class="h-4 w-4" />
				</Button>
				<Button
					type="button"
					size="sm"
					variant="ghost"
					onclick={handleCancel}
					class="h-8 w-8 p-0 text-muted-foreground hover:text-foreground"
					aria-label="Annuler"
				>
					<X class="h-4 w-4" />
				</Button>
			</div>
		</form>
	{:else}
		<a
			href={`/chat/${conversation.id}`}
			class={cn(
        "block flex-1 truncate transition-colors rounded px-2 py-1 text-sm",
        isCurrent
          ? "text-primary font-medium bg-primary/10"
          : "text-muted-foreground hover:text-foreground hover:bg-muted/30"
      )}
		>
			{name}
		</a>
		<div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
			<Button
				size="sm"
				variant="ghost"
				onclick={() => { isEditing = true; name = conversation.name; }}
				class="h-8 w-8 p-0 text-muted-foreground hover:text-foreground"
				aria-label="Éditer"
			>
				<Pencil class="h-4 w-4" />
			</Button>
			<form
				method="POST"
				action={`/chat/${conversation.id}?/deleteConversation`}
				use:enhance={() => {
					isEditing = true;
					return async ({update}) => {
						await update();
						isEditing = false;
					};
				}}
				class="contents"
			>
				<Input type="hidden" value={page.params.id} name="from" id="from" />
				<Button
					type="submit"
					size="sm"
					variant="ghost"
					class="h-8 w-8 p-0 text-muted-foreground hover:text-destructive hover:bg-destructive/10"
					aria-label="Supprimer"
				>
					<Trash2 class="h-4 w-4" />
				</Button>
			</form>
		</div>
	{/if}
</li>