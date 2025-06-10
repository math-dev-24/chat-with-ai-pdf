<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Loader2, MessageCircle } from 'lucide-svelte';

	let name = $state('Nouvelle conversation');
	let inLoading = $state(false);
</script>

<Card class="w-full max-w-2xl mx-auto">
	<CardHeader>
		<CardTitle class="flex items-center gap-2 text-lg">
			<MessageCircle class="h-5 w-5 text-primary" />
			Nouvelle conversation
		</CardTitle>
	</CardHeader>
	<CardContent>
		<form
			method="POST"
			action="?/createNewConversation"
			use:enhance={() => {
				inLoading = true;
				return async ({ update }) => {
					await update();
					inLoading = false;
				};
			}}
			class="space-y-4"
		>
			<Input
				bind:value={name}
				name="name"
				placeholder="Nom de la conversation"
				required
				class="w-full"
			/>
			<Button type="submit" class="w-full" disabled={inLoading}>	
				{#if inLoading}
					<Loader2 class="h-4 w-4 animate-spin" />
				{:else}
					Créer la conversation
				{/if}
			</Button>
		</form>
	</CardContent>
</Card> 