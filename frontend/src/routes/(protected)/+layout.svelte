<script lang="ts">
	import type { LayoutProps } from './$types';
	import { Button } from '$lib/components/ui/button';
	import { Bot, LogOut } from 'lucide-svelte';
	import ModeToggle from '$lib/components/ModeToggle.svelte';
	import { page } from '$app/state';

	let { children }: LayoutProps = $props();

	const isCurrentPath = (href: string) => page.url.pathname === href

	const listMenu: {label: string, href: string, isCurrentPath: boolean}[] = [
		{
			label: 'Home',
			href: '/',
			isCurrentPath: isCurrentPath('/')
		},
		{
			label: 'Chat',
			href: '/chat',
			isCurrentPath: isCurrentPath('/chat')
		},
		{
			label: 'Stat',
			href: '/stat',
			isCurrentPath: isCurrentPath('/stat')
		},
		{
			label: 'Upload PDF',
			href: '/pdf/form',
			isCurrentPath: isCurrentPath('/pdf/form')
		},
		{
			label: 'Profil',
			href: '/profil',
			isCurrentPath: isCurrentPath('/profil')
		}		
	]

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
					<ul class="flex gap-1 items-center">
						{#each listMenu as menu (menu.href)}
						<li>
							<Button 
								variant="link" 
								href={menu.href} 
								class={menu.isCurrentPath ? 'text-primary' : 'text-muted-foreground'}
							>
								{menu.label}
							</Button>
						</li>
						{/each}
							<li>
								<form action="/logout" method="POST">
									<Button variant="ghost" type="submit">
										<LogOut class="h-4 w-4" />
									</Button>
								</form>
							</li>

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
