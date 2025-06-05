<script lang="ts">
	import { Bot, Power } from 'lucide-svelte';
		import { Button } from '$lib/components/ui/button';
		import ModeToggle from '$lib/components/ModeToggle.svelte';

		let { data, children } = $props();
</script>

<header  class="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
	<div class="container mx-auto px-4 py-4">
		<nav class="flex items-center justify-between">
			<div class="flex items-center gap-2">
				<div class="flex items-center justify-center w-8 h-8 bg-primary rounded-lg">
					<Bot class="h-5 w-5 text-primary-foreground" />
				</div>
				<span class="text-xl font-bold">ChatPDF</span>
			</div>
			<div class="flex items-center gap-4">
				<nav>
					<ul class="flex gap-1 items-center gap-2">
						{#if data.user}
							<li>
								<Button href="/profil" size="sm" variant="secondary">
									Dashboard
								</Button>
							</li>
							<li>
								<form action="?/logout" method="POST">
									<Button variant="destructive" size="sm" type="submit">
										<Power class="h-5" />
									</Button>
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
			</div>
		</nav>
	</div>
</header>

{@render children()}
