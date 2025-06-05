<script lang="ts">
	import { ModeWatcher } from "mode-watcher";
	import ModeToggle from '$lib/components/ModeToggle.svelte';
	import { Button } from '$lib/components/ui/button';

	let { data, children } = $props();
</script>

<ModeWatcher />

<header class="bg-white/70 backdrop-blur-sm border-b border-slate-200/50 px-6 py-4">
	<nav>
		<ul class="flex gap-1 items-center">
			<li>
				<Button variant="link" href="/">
					Home
				</Button>
			</li>
			{#if data.user}
				<li>
					<Button variant="link" href="/chat">
						Chat
					</Button>
				</li>
				<li>
					<Button variant="link" href="/profil">
						Profil
					</Button>
				</li>
				<li>
					<form action="?/logout" method="POST">
						<Button variant="ghost">Déconnexion</Button>
					</form>
				</li>
			{:else}
				<li>
					<Button variant="link" href="/login">
						Se connecter
					</Button>
				</li>
				<li>
					<Button variant="link" href="/register">
						S'inscrire
					</Button>
				</li>
			{/if}
			<li>
				<ModeToggle />
			</li>
		</ul>
	</nav>
</header>

{@render children()}
