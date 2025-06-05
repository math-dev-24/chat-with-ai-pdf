<script lang="ts">
	import type {PageProps} from './$types';
	import * as Card from "$lib/components/ui/card";
	import * as Alert from "$lib/components/ui/alert";
	import { Input } from "$lib/components/ui/input/index.js";
	import { Label } from "$lib/components/ui/label/index.js";
	import { Button } from '$lib/components/ui/button';
	import { User } from 'lucide-svelte';

	let { form }: PageProps = $props();

</script>

<Card.Root class="max-w-2xl mx-auto my-6">
	<Card.Header>
		<Card.Title>
			Se connecter :
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
			<Button type="submit">
				<User />
				Se connecter
			</Button>
		</form>
	</Card.Content>
	<Card.Footer class="flex flex-col items-start">
		<p>
			Vous n'avez pas de compte ?
			<a class="text-blue-600 hover:text-blue-800 transition-colors" href="/register">Créez-en un</a>
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