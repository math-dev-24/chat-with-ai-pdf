<script>
	import * as Card from "$lib/components/ui/card";
	import { Label } from '$lib/components/ui/label';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button/index.js';
	import {enhance} from '$app/forms';
	import { Pencil } from 'lucide-svelte';

	let { action, currentUsername } = $props();

</script>

<Card.Root>
	<Card.Header>
		<Card.Title>
			Profil :
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
				<Label for="username">Username :</Label>
				<Input type="text" value={currentUsername} name="username" id="username" />
			</div>
			<Button class="gap-1" type="submit">
				<Pencil />
				Modifier
			</Button>
		</form>
	</Card.Content>
</Card.Root>

