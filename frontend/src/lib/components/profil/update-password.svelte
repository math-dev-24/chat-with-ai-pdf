<script lang="ts">
	import * as Card from "$lib/components/ui/card";
	import { Label } from '$lib/components/ui/label';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import {enhance} from '$app/forms';
	import { Pencil } from 'lucide-svelte';

	let { action } = $props();

</script>

<Card.Root>
	<Card.Header>
		<Card.Title>
			Mot de passe :
		</Card.Title>
	</Card.Header>
	<Card.Content>
		<form
			method="POST"
			{action}
			use:enhance
			class="space-y-4"
		>
			<div>
				<Label for="password">Mot de passe actuel :</Label>
				<Input name="password" id="password" type="password" />
			</div>
			<div>
				<Label for="newPassword">Nouveau mot de passe :</Label>
				<Input name="newPassword" id="newPassword" type="password"/>
			</div>
			<div>
				<Label for="newPasswordCheck">Confirmez :</Label>
				<Input name="newPasswordCheck" id="newPasswordCheck" type="password"/>
			</div>
			<Button class="gap-1">
				<Pencil />
				Modifier
			</Button>
		</form>
	</Card.Content>
</Card.Root>