<script lang="ts">
	import type {PageProps} from './$types';
	import * as Card from "$lib/components/ui/card";
	import * as Alert from "$lib/components/ui/alert";
	import { Input } from "$lib/components/ui/input/index.js";
	import { Label } from "$lib/components/ui/label/index.js";
	import { Button } from '$lib/components/ui/button';
	import { UserPlus } from 'lucide-svelte';

	let { form }: PageProps = $props();
</script>

<Card.Root class="max-w-2xl mx-auto my-6">
	<Card.Header>
		<Card.Title>
			S'inscrire :
		</Card.Title>
	</Card.Header>
	<Card.Content>
		<form
			class="flex flex-col gap-2"
			method="POST"
		>
				<Label for="username">Username</Label>
				<Input id="username" name="username" required type="text" />

				<Label for="password">Password</Label>
				<Input id="password" name="password" required type="password" />

			<Button
				class="gap-2"
				type="submit"
			>
				<UserPlus />
				<span>S'enregistrer</span>
			</Button>
		</form>
	</Card.Content>
	<Card.Footer class="flex flex-col items-start">
		<p>
			Vous avez déjà un compte ?
			<a class="text-blue-600 hover:text-blue-800 transition-colors" href="/login">se connecter !</a>
		</p>
		{#if form?.message}
			<Alert.Root variant="destructive" class="my-2">
				<Alert.Title>
					Erreur !
				</Alert.Title>
				<Alert.Description>
					{form.message}
				</Alert.Description>
			</Alert.Root>
		{/if}
	</Card.Footer>
</Card.Root>
