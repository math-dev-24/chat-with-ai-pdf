<script lang="ts">
	import UpdateName from "$lib/components/profil/update-name.svelte";
	import UpdatePassword from "$lib/components/profil/update-password.svelte";
	import * as Tabs from "$lib/components/ui/tabs";
	import { AlertCircle } from 'lucide-svelte';
	import { Alert, AlertDescription, AlertTitle } from '$lib/components/ui/alert';
	import { CardContent } from '$lib/components/ui/card';

	let { data, form } = $props();

</script>


<h1 class="text-2xl text-center mb-4 mt-8">Profil de {data.user.username}</h1>

<Tabs.Root value="account" class="container max-w-2xl mx-auto">
	<Tabs.List>
		<Tabs.Trigger value="account">Account</Tabs.Trigger>
		<Tabs.Trigger value="password">Mot de passe</Tabs.Trigger>
	</Tabs.List>

	<Tabs.Content value="account">
			<UpdateName action="?/updateName" currentUsername={data.user.username} />
	</Tabs.Content>
	<Tabs.Content value="password">
		<UpdatePassword action="?/updatePassword"/>
	</Tabs.Content>
</Tabs.Root>

{#if form?.message}
	<CardContent class="pt-4 max-w-2xl container mx-auto">
		<Alert variant={form.status === 'error' ? 'destructive' : 'default'} class="animate-in slide-in-from-top-2 duration-300">
			<AlertCircle class="h-4 w-4" />
			<AlertTitle>{form.status === 'error' ? 'Erreur' : 'Succès'}</AlertTitle>
			<AlertDescription>
				{form.message}
			</AlertDescription>
		</Alert>
	</CardContent>
{/if}