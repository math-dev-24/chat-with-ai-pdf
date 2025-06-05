<script lang="ts">
	import UpdateName from "$lib/components/profil/update-name.svelte";
	import UpdatePassword from "$lib/components/profil/update-password.svelte";
	import * as Tabs from "$lib/components/ui/tabs";

	let { data } = $props();

</script>


<h1 class="text-2xl text-center mb-4">Profil de {data.user.username}</h1>

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